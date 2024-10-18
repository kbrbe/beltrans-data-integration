import time
import lxml.etree as ET
import requests
import rdflib
import os
import pandas as pd
import utils_stats

# -----------------------------------------------------------------------------
def addGenderInfoColumn(row, inputCol, outputCol, lookup, personDelimiter=';'):
  """
  Checking the gender info for each contributor in inputCol (delimited by personDelimiter)
  is present in lookup. If yes, trueValue will be put in outputCol, otherwise falseValue.
  If trueValue is a string, it is interpreted as a key for lookup, if it is a boolean value,
  the boolean value will be added.

  Single male contributor leads to FALSE
  >>> row0 = {'authorIdentifiers': 'Lieber, Sven (123)'}
  >>> addGenderInfoColumn(row0, 'authorIdentifiers', 'femaleAuthor', {'123': 'Male'})
  >>> row0['femaleAuthor']
  'FALSE'

  Multiple male contributors lead to FALSE
  >>> row1 = {'authorIdentifiers': 'Lieber, Sven (123);Doe, John (456)'}
  >>> addGenderInfoColumn(row1, 'authorIdentifiers', 'femaleAuthor', {'123': 'Male', '456': 'Male'})
  >>> row1['femaleAuthor']
  'FALSE'

  Multiple contributors with mix of male and unknown lead to UNKNOWN
  >>> row2 = {'authorIdentifiers': 'Lieber, Sven (123);Doe, John (456)'}
  >>> addGenderInfoColumn(row2, 'authorIdentifiers', 'femaleAuthor', {'123': 'Male', '456': ''})
  >>> row2['femaleAuthor']
  'UNKNOWN'

  Single female contributor leads to TRUE
  >>> row3 = {'authorIdentifiers': 'Doe, Jane (789)'}
  >>> addGenderInfoColumn(row3, 'authorIdentifiers', 'femaleAuthor', {'789': 'Female'})
  >>> row3['femaleAuthor']
  'TRUE'

  Multiple female contributors lead to TRUE
  >>> row4 = {'authorIdentifiers': 'Doe, Jane (789);Doe, Sarah (100)'}
  >>> addGenderInfoColumn(row4, 'authorIdentifiers', 'femaleAuthor', {'789': 'Female', '100': 'Female'})
  >>> row4['femaleAuthor']
  'TRUE'

  Multiple contributors wiht mix of female and unknown lead to TRUE
  >>> row5 = {'authorIdentifiers': 'Doe, Jane (789);Doe, Sarah (100)'}
  >>> addGenderInfoColumn(row5, 'authorIdentifiers', 'femaleAuthor', {'789': 'Female', '100': ''})
  >>> row5['femaleAuthor']
  'TRUE'
  """

  contributors = []
  if personDelimiter in row[inputCol]:
    contributors = row[inputCol].split(personDelimiter)
  else:
    contributors = [row[inputCol]]

  atLeastOneFemale = False
  atLeastOneUnknown = False

  for c in contributors:
    contributorID = utils_stats.getContributorID(c)
    if contributorID in lookup:
      if lookup[contributorID] == 'Female':
        atLeastOneFemale = True
   
      if lookup[contributorID] == '':
        atLeastOneUnknown = True
      
  if atLeastOneFemale == True:
    row[outputCol] = 'TRUE'
  elif atLeastOneUnknown == True:
    row[outputCol] = 'UNKNOWN'
  else:
    row[outputCol] = 'FALSE'
     

# -----------------------------------------------------------------------------
def addCombinedCounting(row, contributions, roleMapping, firstRole, secondRole, combinedRole):
  """ Helper function that is indirectly tested via addContributions. """

  if (firstRole in contributions) and (secondRole in contributions):
    combinedSet = set(contributions[firstRole]).union(set(contributions[secondRole]))
    row[combinedRole] = ';'.join(sorted(combinedSet))
  elif (firstRole in contributions) and (secondRole not in contributions):
    row[combinedRole] = ';'.join(contributions[firstRole])
  elif (firstRole not in contributions) and (secondRole in contributions):
    row[combinedRole] = ';'.join(contributions[secondRole])



# -----------------------------------------------------------------------------
def addContributions(row, contributions, roleMapping):
  """This function adds the given contributor values based on the given roleMapping.

  >>> row0 = {'targetIdentifier': '1', 'authors': '', 'translators': '', 'scenarists': '', 'adapters': ''}
  >>> contributions0 = {
  ... 'http://schema.org/author': ['John (123)', 'Jane (456)'],
  ... 'http://schema.org/translator': ['David (789)'],
  ... 'http://id.loc.gov/vocabulary/relators/sce': ['Bob (111)'],
  ... 'http://id.loc.gov/vocabulary/relators/adp': ['Julia (222)'],
  ... 'http://id.loc.gov/vocabulary/relators/other': ['Anonymous (000)']
  ... }
  >>> roleMapping = {
  ... 'http://schema.org/author': 'authors', 
  ... 'http://schema.org/translator': 'translators', 
  ... 'http://id.loc.gov/vocabulary/relators/sce': 'scenarists',
  ... 'http://id.loc.gov/vocabulary/relators/adp': 'adapters'}
  >>> addContributions(row0, contributions0, roleMapping)

  Single roles will be found
  >>> row0['authors']
  'Jane (456);John (123)'
  >>> row0['translators']
  'David (789)'
  >>> row0['scenarists']
  'Bob (111)'
  >>> row0['adapters']
  'Julia (222)'

  It adds combined columns for author and scenarist
  >>> row0['author/scenarist']
  'Bob (111);Jane (456);John (123)'

  It adds combined columns for translators and adapters
  >>> row0['translator/adapter']
  'David (789);Julia (222)'

  Roles not in the mapping are not added
  >>> 'otherRole' in row0
  False
  """  
  schemaURI = 'http://schema.org/'
  locURI = 'http://id.loc.gov/vocabulary/relators/'

  addCombinedCounting(row, contributions, roleMapping, f'{schemaURI}author', f'{locURI}sce', 'author/scenarist')
  addCombinedCounting(row, contributions, roleMapping, f'{schemaURI}translator', f'{locURI}adp', 'translator/adapter')

  for contRole, contValues in contributions.items():
    #print(f'contRole: {contRole}')
    if contRole in roleMapping:
      row[roleMapping[contRole]] = ';'.join(sorted(contValues))

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
if __name__ == "__main__":
  import doctest
  doctest.testmod()
