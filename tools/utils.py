import time
import lxml.etree as ET
import requests
import rdflib
import os
import pandas as pd



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
    """
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
          valueList.append(e.text)
      return ';'.join(valueList)
    else:
      if hasattr(elem, 'text'):
        return elem.text
  
  return ''







# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()