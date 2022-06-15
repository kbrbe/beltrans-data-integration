import itertools
from datetime import datetime
import requests
import rdflib
import os
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, TURTLE, JSON, POST

# -----------------------------------------------------------------------------
def addTestData(target, loadConfig):
  """This function reads the test data and stores it into several named graphs (one file for one named graph).
  The config looks like the following: {'http://first-named-graph': ['filename1'], 'http://second-named-graph': ['filename2']}

  The data could already be in quad format, but we are more flexible if we can configure which data is stored in which named graph.
  """
  for ng in loadConfig:
    files = loadConfig[ng]
    for filename in files:
      if os.path.isfile(filename):
        with open(filename, 'r') as dataIn:
          if isinstance(target, rdflib.ConjunctiveGraph):
            namedGraphURI = rdflib.URIRef(ng)
            target.get_context(namedGraphURI).parse(filename, format='turtle')
          else:
            addDataToBlazegraph(url=target, namedGraph=ng, filename=filename, fileFormat='text/turtle')

# -----------------------------------------------------------------------------
def loadData(url, loadConfig):
  """This function reads the given config containing the source of RDF data and its type to store it in a SPARQL endpoint at 'url'."""

  for graph in loadConfig:
    filename = loadConfig['graph']
    if os.path.isfile(filename):
      if filename.endswith('.ttl'):
        addDataToBlazegraph(url=url, namedGraph=graph, filename=filename, fileFormat='text/turtle')
      elif filename.endswith('.sparql'):
        addDataToBlazegraph(url=url, namedGraph=graph, filename=filename, fileFormat='application/sparql-update')

# -----------------------------------------------------------------------------
def addDataToBlazegraph(url, filename, fileFormat, namedGraph=None, auth=None):
  print(f'## Add data from {filename} to {namedGraph} of {url}\n')
  with open(filename, 'rb') as fileIn:
    #r = requests.post(url, files={'file': (filename, fileIn, fileFormat)}, headers={'Content-Type': fileFormat}, params={'context-uri': namedGraph})
    if namedGraph:
      r = requests.post(url, data=fileIn.read(), headers={'Content-Type': fileFormat}, params={'context-uri': namedGraph}, auth=auth)
    else:
      r = requests.post(url, data=fileIn.read(), headers={'Content-Type': fileFormat}, auth=auth)
    print(r.headers)
    print(r.content)

# -----------------------------------------------------------------------------
def query(target, queryString, outputWriter):
  """This function executes the given SPARQL query against the target and writes the output to outputWriter."""
  res = None
  if isinstance(target, rdflib.ConjunctiveGraph):
    # target is a local rdflib graph
    print(target)
    res = target.query(queryString)
    for row in res:
      print(row)
  else:
    # SPARQLWrapper has issues retrieving CSV from Blazegraph, thus we send the query low level via a request
    res = requests.post(target, data=queryString, headers={'Accept': 'text/csv', 'Content-Type': 'application/sparql-query'})
    outputWriter.write(res.content)

# -----------------------------------------------------------------------------
def sparqlUpdate(target, queryString):
  """This function executes the given SPARQL query against the target and writes the output to outputWriter."""
  res = None
  # SPARQLWrapper has issues retrieving CSV from Blazegraph, thus we send the query low level via a request
  res = requests.post(target, data=queryString, headers={'Content-Type': 'application/sparql-update'})
  print(res.content)

# ------------------------------------------------------------
def readSPARQLQuery(filename):
    """Read a SPARQL query from file and return the content as a string."""
    content = ""
    with open(filename, 'r') as reader:
        content = reader.read()
    return content



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
def datesMatch(fullDates, yearMonthDates, years):
  """This function checks if the different provided dates describe the same date,
     e.g. 1988-04-25, 1988 and 1988-04 would match resulting in True, otherwise False.

  >>> datesMatch(set(['1988-04-25']), set(['1988-04']), set(['1988']))
  True

  >>> datesMatch(set(['1988-04-25']), [], set(['1988']))
  True

  >>> datesMatch(set(['1988-04-25']), set([]), set([]))
  True

  >>> datesMatch(set([]), set(['1988-04']), set([]))
  True

  >>> datesMatch(set([]), set([]), set(['1988']))
  True

  >>> datesMatch(set(['1988-04-25']), set(['1988-04']), set(['1988', '1988', '1989']))
  False

  >>> datesMatch(set(['1988-04-25']), set(['1988-04', '1988-06']), set(['1988', '1988']))
  False

  >>> datesMatch(set(['1988-04-25', '1988-05-25']), set(['1988-04']), set(['1988', '1988', '1989']))
  False

  >>> datesMatch([], [], [])
  False
  """

  # The given dates are stored in sets, if one set has more than 1 element
  # there are at least 2 different values
  if len(fullDates) > 1: return False
  if len(yearMonthDates) > 1: return False
  if len(years) > 1: return False

  # compare the differently detailed dates
  # full date with year month
  if len(fullDates) > 0 and len(yearMonthDates) > 0:
    fullDate = datetime.strptime(next(iter(fullDates)), '%Y-%m-%d').date()
    yearMonth = datetime.strptime(next(iter(yearMonthDates)), '%Y-%m').date()
    if fullDate.year != yearMonth.year or fullDate.month != yearMonth.month:
      return False

  # full date with year
  if len(fullDates) > 0 and len(years) > 0:
    fullDate = datetime.strptime(next(iter(fullDates)), '%Y-%m-%d').date()
    year = datetime.strptime(next(iter(years)), '%Y').date().year
    if fullDate.year != year:
      return False
  
  # year month with year
  if len(yearMonthDates) > 0 and len(years) > 0:
    yearMonth = datetime.strptime(next(iter(yearMonthDates)), '%Y-%m').date()
    year = datetime.strptime(next(iter(years)), '%Y').date().year
    if yearMonth.year != year:
      return False
  
  if len(fullDates) == 0 and len(yearMonthDates) == 0 and len(years) == 0:
    return False
  else:
    return True

# -----------------------------------------------------------------------------
def concatenateDates(fullDates, yearMonthDates, years):
  """This function combines several dates in a human readable fashion.

  >>> concatenateDates(set(['1988-04-25']), set(['1988-05']), set())
  '1988-04-25 or 1988-05'

  >>> concatenateDates(set(['1988-04-25', '1988-04-24']), set(['1988-05']), set())
  '1988-04-24 or 1988-04-25 or 1988-05'

  >>> concatenateDates(set(['1988-04-25', '1988-04-24']), set(['1988-05']), set(['1989']))
  '1988-04-24 or 1988-04-25 or 1988-05 or 1989'
  """

  elements = [fullDates, yearMonthDates, years]
  singleList = set().union(*elements)

  return ' or '.join(sorted(singleList))

# -----------------------------------------------------------------------------
def mostCompleteDate(dates):
  """This function returns the most complete date from the given array, if there is a mismatch both are returned.

  >>> mostCompleteDate(['1988-04-25', '1988'])
  '1988-04-25'

  >>> mostCompleteDate(['1988-04-25'])
  '1988-04-25'

  >>> mostCompleteDate(['1988', '1988-04'])
  '1988-04'

  >>> mostCompleteDate(['1988'])
  '1988'
  """

  fullDates = set()
  yearMonthDates = set()
  years = set()

  if len(dates) > 0:
    for d in dates:
      try:
        fullDate = datetime.strptime(d, '%Y-%m-%d').date()
        fullDates.add(d)
      except:
        try:
          yearMonth = datetime.strptime(d, '%Y-%m').date()
          yearMonthDates.add(d)
        except:
          try:
            year = datetime.strptime(d, '%Y').date().year
            years.add(d)
          except:
            pass
    if datesMatch(fullDates, yearMonthDates, years):
      # preferably return a full date, thus start with that
      if len(fullDates) > 0:
        return fullDates.pop()
      elif len(yearMonthDates) > 0:
        return yearMonthDates.pop()
      elif len(years) > 0:
        return years.pop()
      else:
        # the values match, but technically they are all empty
        return ''
    else:
      return concatenateDates(fullDates, yearMonthDates, years)
  else:
    return ''

# -----------------------------------------------------------------------------
def selectDate(row, role, dateType, sources, rowIDCol, mismatchLog):
  """This function chooses the most complete date for the given role and row, possible dateTypes are 'Birth' and 'Death'.

  Select the most complete date betwen the sources
  >>> row = {'authorBirthDateKBR': '1988-04-25', 'authorBirthDateISNI': '1988'}
  >>> selectDate(row, 'author', 'Birth', ['KBR', 'ISNI'], 'authorKBRIdentifier', {})
  >>> row['authorBirthDate'] == '1988-04-25'
  True

  >>> row = {'authorBirthDateKBR': '', 'authorBirthDateISNI': '1988'}
  >>> selectDate(row, 'author', 'Birth', ['KBR', 'ISNI'], 'authorKBRIdentifier', {})
  >>> row['authorBirthDate'] == '1988'
  True

  Keep it empty if none of the sources provide a date
  >>> row = {'authorBirthDateKBR': '', 'authorBirthDateISNI': ''}
  >>> selectDate(row, 'author', 'Birth', ['KBR', 'ISNI'], 'authorKBRIdentifier', {})
  >>> row['authorBirthDate'] == ''
  True

  It also works for other roles than author
  >>> row = {'translatorBirthDateKBR': '1988-04-25', 'translatorBirthDateISNI': '1988'}
  >>> selectDate(row, 'translator', 'Birth', ['KBR', 'ISNI'], 'translatorKBRIdentifier', {})
  >>> row['translatorBirthDate'] == '1988-04-25'
  True

  >>> row = {'illustratorBirthDateKBR': '1988-04-25', 'illustratorBirthDateISNI': '1988'}
  >>> selectDate(row, 'illustrator', 'Birth', ['KBR', 'ISNI'], 'illustratorKBRIdentifier', {})
  >>> row['illustratorBirthDate'] == '1988-04-25'
  True

  >>> row = {'scenaristBirthDateKBR': '1988-04-25', 'scenaristBirthDateISNI': '1988'}
  >>> selectDate(row, 'scenarist', 'Birth', ['KBR', 'ISNI'], 'scenaristKBRIdentifier', {})
  >>> row['scenaristBirthDate'] == '1988-04-25'
  True

  Log an error if a mismatch was found and keep both in the output
  >>> row = {'authorKBRIdentifier': '1234', 'authorBirthDateKBR': '1988-04-25', 'authorBirthDateISNI': '1989'}
  >>> selectDate(row, 'author', 'Birth', ['KBR', 'ISNI'], 'authorKBRIdentifier', {})
  >>> row['authorBirthDate'] == '1988-04-25 or 1989'
  True

  The same works also for death dates
  >>> row = {'authorDeathDateKBR': '1988-04-25', 'authorDeathDateISNI': '1988'}
  >>> selectDate(row, 'author', 'Death', ['KBR', 'ISNI'], 'authorKBRIdentifier', {})
  >>> row['authorDeathDate'] == '1988-04-25'
  True

  The same works also for death dates
  >>> row = {'authorDeathDate': '1988-04-25', 'authorDeathDateISNI': '1988'}
  >>> selectDate(row, 'author', 'Death', ['KBR', 'ISNI'], 'authorKBRIdentifier', {})
  >>> row['authorDeathDate'] == '1988-04-25'
  True
  """

  # extract all possible dates based on different sources
  dates = []
  for s in sources:
    colName = f'{role}{dateType}Date{s}'
    if colName in row:
      dates.append(row[colName])

  # extract all possible dates without a source identifier, e.g. authorDeathDate
  noSourceColName = f'{role}{dateType}Date'
  if noSourceColName in row:
    dates.append(row[noSourceColName])
  

  outputColName = f'{role}{dateType}Date'

  # set the selected value
  row[outputColName] = mostCompleteDate(dates)

  # In case the different dates do not match log it
  # the date should then be e.g. "1972-04 or 1970"
  if 'or' in row[outputColName]:

    contributorURI = row[rowIDCol]
    # log the mismatching data and then remove the initial sources
    for s in sources:
      colName = f'{role}{dateType}Date{s}'
      value = row[colName]
      addToMismatchLog(mismatchLog, dateType, role, contributorURI, s, value)
      row.pop(colName)

  else:
    # only remove the initial sources
    for s in sources:
      colName = f'{role}{dateType}Date{s}'
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

# ---------------------------------------------------------------------------
def getDfValues(df, idColName, idColValue, colName):
    """"Returns an array of values of a row with given identifier.
    >>> data1 = pd.DataFrame([{"targetTextKBRIdentifier": "2", "name": "john", "targetTextBnFIdentifier": ""},{"targetTextBnFIdentifier": 2, "name": "jane"}, {"targetTextKBRIdentifier": "2", "name": "jane"}])
    >>> getDfValues(data1, "targetTextKBRIdentifier", "2", "name")
    ['john', 'jane']
    """
    selection = (df.loc[df[idColName] == idColValue, colName])
    return selection.tolist()

# ---------------------------------------------------------------------------
def getDfCellValue(df, idColName, idColValue, colName):
    """Returns the value of a specific cell or raises errors in case the row isn't found or more than one value is found.
    >>> data = pd.DataFrame([{"myID": 1, "name": "john", "myCol": "sven (12, 34)"},{"myID": 2, "name": "jane"}])
    >>> getDfCellValue(data, "myID", 1, "myCol")
    'sven (12, 34)'
    >>> getDfCellValue(data, "myID", 11, "myCol")
    Traceback (most recent call last):
     ...
    ValueError: No row with ID "11" in column "myID" found!
    >>> getDfCellValue(data, "myIDColumnWhichDoesNotExist", 11, "myCol")
    Traceback (most recent call last):
     ...
    KeyError: 'ID column "myIDColumnWhichDoesNotExist" does not exist!'
    >>> getDfCellValue(data, "myID", 1, "myColWhichDoesNotExist")
    Traceback (most recent call last):
     ...
    KeyError: 'Value column "myColWhichDoesNotExist" does not exist!'
    >>> data2 = pd.DataFrame([{"myID": 1, "name": "john", "myCol": "sven (12, 34)"},{"myID": 1, "name": "jane"}])
    >>> getDfCellValue(data2, "myID", 1, "myCol")
    Traceback (most recent call last):
     ...
    ValueError: More than one row with ID "1" in column "myID" found!
    >>> data3 = pd.DataFrame([{"targetTextKBRIdentifier": 1, "name": "john", "targetTextBnFIdentifier": "", "name": ""},{"targetTextKBRIdentifier": 2, "name": "jane"}, {"targetTextBnFIdentifier": "2", "name": "jane"}])
    >>> getDfCellValue(data3, "targetTextKBRIdentifier", 2, "targetTextBnFIdentifier")
    Traceback (most recent call last):
     ...
    KeyError: 'No value found in column "targetTextKBRIdentifier"'
    """
    if idColName not in df:
      raise KeyError(f'ID column "{idColName}" does not exist!')
    if colName not in df:
      raise KeyError(f'Value column "{colName}" does not exist!')
    
    selection = (df.loc[df[idColName] == idColValue, colName])

    if selection.size > 1:
      raise ValueError(f'More than one row with ID "{idColValue}" in column "{idColName}" found!')
    elif selection.size == 1:
      if selection.isna().all():
        raise KeyError(f'No value found in column "{idColName}"')
      else:
        return selection.item()
      return selection
    else:
      raise ValueError(f'No row with ID "{idColValue}" in column "{idColName}" found!')
 

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
