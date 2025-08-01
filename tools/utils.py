import time
import lxml.etree as ET
import pandas as pd
import csv
import os
import re
from stdnum import isbn
from stdnum import exceptions

# -----------------------------------------------------------------------------
def getBnFIdentifierWithControlCharacter(identifier):
  """This function computes the BnF control character based on documentation from BnF.

  It correctly works for the two following real life examples
  >>> getBnFIdentifierWithControlCharacter('cb13741679')
  'cb13741679s'
  >>> getBnFIdentifierWithControlCharacter('cb11896963')
  'cb11896963c'

  Also return the correct control character if the 'cb' prefix is missing
  >>> getBnFIdentifierWithControlCharacter('11896963')
  'cb11896963c'

  Return the same identifier if there is already a valid control character
  >>> getBnFIdentifierWithControlCharacter('cb11896963c')
  'cb11896963c'

  Return a corrected identifier if the given control character is wrong
  >>> getBnFIdentifierWithControlCharacter('cb11896963d')
  'cb11896963c'

  Throw an error if the identifier is too short
  >>> getBnFIdentifierWithControlCharacter('cb118969c')
  Traceback (most recent call last):
      ...
  Exception: Invalid BnF identifier, too short: cb118969c

  Throw an error if the identifier is too long
  >>> getBnFIdentifierWithControlCharacter('cb118969631c')
  Traceback (most recent call last):
      ...
  Exception: Invalid BnF identifier, too long: cb118969631c
  """

  correspondenceTable = ['0','1','2','3','4','5','6','7','8',
                         '9','b','c','d','f','g','h','j','k',
                         'm','n','p','q','r','s','t','v','w',
                         'x','z']

  # make sure the identifier starts with 'cb'
  identifier = f'cb{identifier}' if not identifier.startswith('cb') else identifier

  if len(identifier) == 11:
    # perfect length, so there seems to be already a control character
    # don't trust it, to be sure compute the control character again
    return getBnFIdentifierWithControlCharacter(identifier[0:10])
  elif len(identifier) > 11:
    # this identifier is too long for being a BnF identifier
    raise Exception(f'Invalid BnF identifier, too long: {identifier}')
  elif len(identifier) < 10:
    # this identifier is too short for being a BnF identifier
    raise Exception(f'Invalid BnF identifier, too short: {identifier}')

  values = []
  position = 1
  for digit in identifier:
    digitBase10Value = correspondenceTable.index(digit)
    values.append(digitBase10Value * position)
    position += 1
  sumMod29 = sum(values)%29
  return identifier + str(correspondenceTable[sumMod29])

# -----------------------------------------------------------------------------
def addToMismatchLog(mismatchLog, dateType, roleType, contributorURI, s, value):
  """This function logs mismatching dates in the given data structure.

  >>> log = {}
  >>> addToMismatchLog(log, 'Birth', 'author', '123', 'KBR', '1988')
  >>> log['Birth']['author']['123']['KBR'] == {'1988'}
  True

  A log is added also if there is already a log entry for another source of that contributor
  >>> log = { 'Birth': {'author': {'123': {'ISNI': {'1989'}}}}}
  >>> addToMismatchLog(log, 'Birth', 'author', '123', 'KBR', '1988')
  >>> log['Birth']['author']['123']['KBR'] == {'1988'} and log['Birth']['author']['123']['ISNI'] == {'1989'}
  True
  """

  if dateType in mismatchLog:
    if roleType in mismatchLog[dateType]:
      if contributorURI in mismatchLog[dateType][roleType]:
        if s in mismatchLog[dateType][roleType][contributorURI]:
          mismatchLog[dateType][roleType][contributorURI][s].add(value)
        else:
          mismatchLog[dateType][roleType][contributorURI][s] = set([value])
      else:
        mismatchLog[dateType][roleType][contributorURI] = { s: set([value]) }
    else:
      mismatchLog[dateType][roleType] = {contributorURI: { s: set([value]) } }
  else:
    mismatchLog[dateType] = {roleType: {contributorURI: { s: set([value]) } }}


# -----------------------------------------------------------------------------
def mergeValues(row, dateType, sources, delimiter=';'):
  """This function merges locations of different input columns.

  >>> row = {'targetPlaceOfPublicationKBR': 'Antwerpen;Amsterdam', 'targetPlaceOfPublicationBnF': 'Brussels'}
  >>> mergeValues(row, 'targetPlaceOfPublication', ['KBR', 'BnF'])
  >>> row['targetPlaceOfPublication']
  'Amsterdam;Antwerpen;Brussels'

  >>> row2 = {'targetPlaceOfPublicationKBR': 'Antwerpen;Amsterdam', 'targetPlaceOfPublicationBnF': 'Antwerpen'}
  >>> mergeValues(row2, 'targetPlaceOfPublication', ['KBR', 'BnF'])
  >>> row2['targetPlaceOfPublication']
  'Amsterdam;Antwerpen'

  >>> row3 = {'targetPlaceOfPublicationKBR': 'Antwerpen;Amsterdam', 'targetPlaceOfPublicationBnF': 'Antwerpen', 'targetPlaceOfPublicationKB': ''}
  >>> mergeValues(row3, 'targetPlaceOfPublication', ['KBR', 'BnF', 'KB'])
  >>> row3['targetPlaceOfPublication']
  'Amsterdam;Antwerpen'
  """
  # extract all possible dates based on different sources
  locations = set()
  for s in sources:
    colName = f'{dateType}{s}'
    if colName in row:
      # the value of this source column might be already a delimited string
      splittedValues = row[colName].split(delimiter)
      if len(splittedValues) > 0 and splittedValues[0] != '':
        locations.update(splittedValues)

  outputColName = f'{dateType}'

  # merge the values and store them in the output column
  row[outputColName] = delimiter.join(sorted(locations))

  # remove the initial sources
  for s in sources:
    colName = f'{dateType}{s}'
    if colName in row:
      row.pop(colName)

# -----------------------------------------------------------------------------
def addKeysWithoutValueToDict(valDict, keyArray):
  """This function adds keys from keyArray to valDict in case it does not exist yet, the default value is an empty string

  >>> addKeysWithoutValueToDict({'a': 'valA', 'b': 'valB'}, ['a', 'b', 'c'])
  {'a': 'valA', 'b': 'valB', 'c': ''}
  """

  for key in keyArray:
    if key not in valDict:
      valDict[key] = ''
  return valDict

# -----------------------------------------------------------------------------
def mergeDictionaries(inputDict, separator=';'):
  """This function merges two or more dictionaries whereas values from different sources for the same key are combined by indicating the provenance.
     For example sourceA = {'a': 'val1'} and sourceB = {'a': 'val2'} will be merged into {'a': 'val1 (sourceA)\nval2 (sourceB)}.
     The given dictionary contains the two dictionaries with their respective names as keys (which will be used to indicate provenance)

  >>> mergeDictionaries({'sourceA': {'a': 'val1'}, 'sourceB': {'a': 'val2'} })
  {'a': 'val1 (sourceA);val2 (sourceB)'}
  """

  keyValues = {}
  for sourceName in inputDict:
    for key in inputDict[sourceName]:
      value = inputDict[sourceName][key]
      valueString = f'{value} ({sourceName})'
      if key in keyValues:
        keyValues[key].append(valueString)
      else:
        keyValues[key] = [valueString]

  outputDict = {}
  for k in keyValues:
    outputDict[k] = separator.join(keyValues[k])

  return outputDict

# -----------------------------------------------------------------------------
def getContributorData(df, role, colNamesRaw):
  """
  >>> df = pd.DataFrame({'authorColA': [1,2,3], 'authorColB': [1,2,3], 'authorColC': [4,5,6]})
  >>> getContributorData(df, 'author', ['ColA', 'ColB'])
     ColA  ColB
  0     1     1
  1     2     2
  2     3     3
  """

  #colNamesRaw = ['Identifier', 'ISNI', 'Nationality', 'Gender', 'FamilyName', 'GivenName', 'BirthDate', 'DeathDate']
  colNames = []
  renameDict = {}
  for c in colNamesRaw:
    currentName = f'{role}{c}'
    colNames.append(currentName)
    renameDict[currentName] = c

  df = df.rename(columns=renameDict)
  return df[colNamesRaw]



# -----------------------------------------------------------------------------
def checkIfColumnsExist(inputColumnNames, outputColumnNames):
    """This function checks if all names of the second list are present in the first, if not an Error is raised.

    The function simply returns true if all names are present
    >>> checkIfColumnsExist(['a', 'b', 'c'], ['a', 'c'])
    True

    If a name is missing an Exception is thrown mentioning which names are missing
    >>> checkIfColumnsExist(['a', 'b', 'c'], ['a', 'd'])
    Traceback (most recent call last):
        ...
    Exception: The following requested column is not in the input: {'d'}

    If inputColumnNames is None throw an exception
    >>> checkIfColumnsExist(None,['a','c'])
    Traceback (most recent call last):
        ...
    Exception: "None" instead of list of input columns given!

    If outputColumnNames is None, throw an exception
    >>> checkIfColumnsExist(['a','c'], None)
    Traceback (most recent call last):
        ...
    Exception: "None" instead of list of output columns given!


    """
    if not inputColumnNames:
      raise Exception(f'"None" instead of list of input columns given!')
    if not outputColumnNames:
      raise Exception(f'"None" instead of list of output columns given!')

    inputColumns = set(inputColumnNames)
    outputColumns = set(outputColumnNames)
    nonExistentColumns = outputColumns.difference(inputColumns)
    if len(nonExistentColumns) > 0:
      text = 'columns are' if len(nonExistentColumns) > 1 else 'column is'
      raise Exception(f'The following requested {text} not in the input: {nonExistentColumns}')
    else:
        return True

# -----------------------------------------------------------------------------
def getElementValue(elem, sep=';'):
  """This function returns the value of the element if it is not None, otherwise an empty string.

  The function returns the 'text' value if there is one
  >>> class Test: text = 'hello'
  >>> obj = Test()
  >>> getElementValue(obj)
  'hello'

  It returns nothing if there is no text value
  >>> class Test: pass
  >>> obj = Test()
  >>> getElementValue(obj)
  ''

  And the function returns a semicolon separated list in case the argument is a list of objects with a 'text' attribute
  >>> class Test: text = 'hello'
  >>> obj1 = Test()
  >>> obj2 = Test()
  >>> getElementValue([obj1,obj2])
  'hello;hello'
  """
  if elem is not None:
    if isinstance(elem, list):
      valueList = list()
      for e in elem:
        if hasattr(e, 'text'):
          if e.text:
            valueList.append(e.text)
      return ';'.join(valueList)
    else:
      if hasattr(elem, 'text'):
        return elem.text
  
  return ''


# -----------------------------------------------------------------------------
def countValues(inputDict, inputKey, statsKey, statsDict, valuePrefix=''):
  """This function counts found values and adds it to the statsDict.

   >>> dict1 = {'myCol': 'author'}
   >>> dict2 = {'myCol': 'author'}
   >>> dict3 = {'myCol': 'translator'}
   >>> dict4 = {'myCol': 'author'}
   >>> dict5 = {'myCol': 'translator'}
   >>> dict6 = {'myCol': ''}
   >>> statsDict = {}
   >>> for myDict in [dict1, dict2, dict3, dict4, dict5, dict6]: countValues(myDict, 'myCol', 'myKey', statsDict)
   >>> statsDict
   {'myKey': {'author': 3, 'translator': 2, '': 1}}
  """
  if inputKey in inputDict:
    value = inputDict[inputKey]
    valueName = valuePrefix + '-' + value
    if statsKey in statsDict:
      stats = statsDict[statsKey]
      if valueName in stats:
        stats[valueName] += 1
      else:
        stats[valueName] = 1
    else:
      statsDict[statsKey] = {valueName: 1}

# -----------------------------------------------------------------------------
def preprocessISBNString(inputISBN):
  """This function normalizes a given string to return numbers only.

  >>> preprocessISBNString('978-90-8558-138-3 test')
  '9789085581383'
  >>> preprocessISBNString('9789085581383 test test')
  '9789085581383'
  >>> preprocessISBNString('9031411515')
  '9031411515'
  >>> preprocessISBNString('9791032305690')
  '9791032305690'
  >>> preprocessISBNString('978 90 448 3374')
  '978904483374'
  >>> preprocessISBNString('90 223 1348 4 (Manteau)')
  '9022313484'
  >>> preprocessISBNString('90 223 1348 4 (Manteau 123)')
  '9022313484'
  >>> preprocessISBNString('978-90-303-6744-4 (dl. 1)')
  '9789030367444'
  >>> preprocessISBNString('979-10-235-1393-613')
  '9791023513936'
  >>> preprocessISBNString('90-295-3453-2 (Deel 1)')
  '9029534532'
  >>> preprocessISBNString('I am not a ISBN number')
  ''
  >>> preprocessISBNString('')
  ''
  """

  inputISBNNorm = re.sub(r'\D', '', inputISBN)

  if len(inputISBNNorm) == 0:
    return ''
  elif len(inputISBNNorm) == 10:
    return inputISBNNorm
  elif len(inputISBNNorm) == 13:
    if inputISBNNorm.startswith('978') or inputISBNNorm.startswith('979'):
      return inputISBNNorm
    else:
      # it is a wrong ISBN number which happens to have 13 digits
      # Best shot: it probably is a 10 digit ISBN and there were other numbers as part of text
      return inputISBNNorm[:10]
  else:
    if len(inputISBNNorm) > 13:
      return inputISBNNorm[:13]
    elif len(inputISBNNorm) < 13 and len(inputISBNNorm) > 10:
      if inputISBNNorm.startswith('978') or inputISBNNorm.startswith('979'):
        # it is actually a wrong ISBN 13 number, nevertheless return all of it
        return inputISBNNorm
      else:
        # maybe number parts of the text got added by accident to a valid 10 digit ISBN
        return inputISBNNorm[:10]
    else:
      return inputISBNNorm


# -----------------------------------------------------------------------------
def getNormalizedISBN10(inputISBN):
  """This function normalizes an ISBN number.

  >>> getNormalizedISBN10('978-90-8558-138-3')
  '90-8558-138-9'
  >>> getNormalizedISBN10('978-90-8558-138-3 test')
  '90-8558-138-9'
  >>> getNormalizedISBN10('9789085581383')
  '90-8558-138-9'
  >>> getNormalizedISBN10('9031411515')
  '90-314-1151-5'
  >>> getNormalizedISBN10('9791032305690')
  ''
  >>> getNormalizedISBN10('')
  ''
  >>> getNormalizedISBN10('979-10-235-1393-613')
  ''
  >>> getNormalizedISBN10('978-10-235-1393-613')
  Traceback (most recent call last):
   ...
  stdnum.exceptions.InvalidFormat: Not a valid ISBN13.
  """

  inputISBNNorm = preprocessISBNString(inputISBN)

  if inputISBNNorm:
    isbn10 = None
    try:
      isbn10 = isbn.format(isbn.to_isbn10(inputISBNNorm))
      return isbn10
    except exceptions.InvalidComponent:
      # Probably an ISBN number with 979 prefix for which no ISBN10 can be created
      if inputISBNNorm.startswith('979'):
        return ''
      else:
        raise
  else:
    return ''

# -----------------------------------------------------------------------------
def getNormalizedISBN13(inputISBN):
  """This function normalizes an ISBN number.

  >>> getNormalizedISBN13('978-90-8558-138-3')
  '978-90-8558-138-3'
  >>> getNormalizedISBN13('978-90-8558-138-3 test')
  '978-90-8558-138-3'
  >>> getNormalizedISBN13('9789085581383')
  '978-90-8558-138-3'
  >>> getNormalizedISBN13('9031411515')
  '978-90-314-1151-1'
  >>> getNormalizedISBN13('')
  ''
  """

  inputISBNNorm = preprocessISBNString(inputISBN)

  if inputISBNNorm:
    isbn13 = None
    try:
      isbn13 = isbn.format(isbn.to_isbn13(inputISBNNorm))
      return isbn13
    except exceptions.InvalidFormat:
      print(f'Error in ISBN 13 conversion for "{inputISBN}"')
      raise
  else:
    return ''



# -----------------------------------------------------------------------------
def getOCLCISBNPairs(isbnList):
  """This function takes a list of ISBN values, mixed ISBN-10 and ISBN-13 and returns all possible valid combinations.

  Get correct pairs from unordered list of different ISBN-10 and ISBN-13 identifiers
  >>> getOCLCISBNPairs(['2853040844','2853040828','9782853040853','9782853040839','2853040836','2853040852','9782853040822','9782853040846'])
  [('2-85304-082-8', '978-2-85304-082-2'), ('2-85304-083-6', '978-2-85304-083-9'), ('2-85304-084-4', '978-2-85304-084-6'), ('2-85304-085-2', '978-2-85304-085-3')]

  Get correct pairs from unordered list of ISBN-10 and ISBN-13 identifiers which not all match with each other, e.g. for one ISBN-10 the ISBN-13 is missing
  and for one ISBN-13 the ISBN-10 is missing. Nevertheless also for those correct pairs are returned
  >>> getOCLCISBNPairs(['2853040844','2874066486','9782853040853','9789056551261','2853040836','2853040852','9782853040822','9782853040846'])
  [('2-85304-082-8', '978-2-85304-082-2'), ('2-85304-083-6', '978-2-85304-083-9'), ('2-85304-084-4', '978-2-85304-084-6'), ('2-85304-085-2', '978-2-85304-085-3'), ('2-87406-648-6', '978-2-87406-648-1'), ('90-5655-126-4', '978-90-5655-126-1')]

  It also works if there are other strings next to the ISBN
  >>> getOCLCISBNPairs(['9789044518856 (geb.)', '9044518852 (geb.)'])
  [('90-445-1885-2', '978-90-445-1885-6')]

  It also works for a combination of issues: additional strings and different books
  >>> getOCLCISBNPairs(['9789044518856 (geb.)', '2853040844 (geb.)'])
  [('2-85304-084-4', '978-2-85304-084-6'), ('90-445-1885-2', '978-90-445-1885-6')]

  The corresponding ISBN-10 value will be empty if it is a ISBN-13 with prefix 979
  >>> getOCLCISBNPairs(['9789044518856 (geb.)', '9791034731015'])
  [('', '979-10-347-3101-5'), ('90-445-1885-2', '978-90-445-1885-6')]
  """

  alreadyComputedISBN10 = set()
  isbnTuples = set()

  for isbn in isbnList:
    # Compute the ISBN-10 and ISBN-13 value for each ISBN
    try:
      isbn10 = getNormalizedISBN10(isbn)
      isbn13 = getNormalizedISBN13(isbn)

      if isbn10 not in alreadyComputedISBN10:
        isbnTuples.add( (isbn10,isbn13) )
        alreadyComputedISBN10.add(isbn10)
    except exceptions.InvalidFormat:
      print(f'Invalid ISBN: {isbn}')
      
  return sorted(isbnTuples)

# -----------------------------------------------------------------------------
def getOrderedString(values, delimiter):
  """
  >>> getOrderedString(['3','1','2'], ';')
  '1;2;3'
  >>> getOrderedString(['3'], ';')
  '3'
  >>> getOrderedString(['3','1','2', '3'], ';')
  '1;2;3;3'
  >>> getOrderedString(['hello','world'], ';')
  'hello;world'
  """
  orderedValues = sorted(values)
  return delimiter.join(orderedValues)

# -----------------------------------------------------------------------------
def getNewValue(oldValue, newValue, delimiter, mode):
  """
  >>> getNewValue('','a', ';', 'append')
  'a'
  >>> getNewValue('','abc', ';', 'append')
  'abc'
  >>> getNewValue('b','abc', ';', 'append')
  'abc;b'
  >>> getNewValue('','a', ';', 'replace')
  'a'
  >>> getNewValue('b','a', ';', 'replace')
  'a'
  >>> getNewValue('a','a', ';', 'append')
  'a'
  >>> getNewValue('a','a;a;c', ';', 'append')
  'a;c'
  """
  if mode == 'append':
    if oldValue == '':
      return getOrderedString(newValue.split(delimiter), delimiter)
    else:
      existingParts = oldValue.split(delimiter)
      newParts = newValue.split(delimiter)
      return getOrderedString(set(existingParts + newParts), delimiter)
  elif mode == 'replace':
    return getOrderedString(newValue.split(delimiter), delimiter)
  else:
    print(f'This should not happen: mode can only be "append" or "replace", but "{mode}" was given')


# -----------------------------------------------------------------------------
def replaceDictKeys(dictionary, mapping):
  """This function replaces the keys in the dictionary with the new keys.
  >>> dict0 = {"oldA": "a", "oldB": "b", "oldC": "c"}
  >>> replaceDictKeys(dict0, {"oldA": "newA", "oldB": "newB"})
  >>> dict0
  {'oldC': 'c', 'newA': 'a', 'newB': 'b'}

  >>> dict1 = {"oldA": "a", "oldB": "b", "oldC": "c"}
  >>> replaceDictKeys(dict1, {"oldA": "oldA", "oldB": "oldB"})
  >>> dict1
  {'oldA': 'a', 'oldB': 'b', 'oldC': 'c'}
  """
  for oldKey, newKey in mapping.items():
    if oldKey != newKey:
      if oldKey in dictionary:
        dictionary[newKey] = dictionary[oldKey]
        del dictionary[oldKey]

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
