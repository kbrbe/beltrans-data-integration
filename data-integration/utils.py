import itertools
from datetime import datetime
import requests
import rdflib
import re
import os
import unicodedata as ud
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, TURTLE, JSON, POST

# -----------------------------------------------------------------------------
def addTestData(target, loadConfig):
  """This function reads the test data and stores it into several named graphs (one file for one named graph).
  The config looks like the following: {'http://first-named-graph': 'filename1', 'http://second-named-graph': 'filename2'}

  The data could already be in quad format, but we are more flexible if we can configure which data is stored in which named graph.
  """
  for ng in loadConfig:
    filename = loadConfig[ng]
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

  >>> mostCompleteDate(['1988', '1987'])
  '1987 or 1988'
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
def selectDateFromRole(row, role, dateType, sources, rowIDCol, mismatchLog):
  """This function chooses the most complete date for the given role and row, possible dateTypes are 'Birth' and 'Death'.

  Select the most complete date betwen the sources
  >>> row = {'authorBirthDateKBR': '1988-04-25', 'authorBirthDateISNI': '1988'}
  >>> selectDateFromRole(row, 'author', 'Birth', ['KBR', 'ISNI'], 'authorKBRIdentifier', {})
  >>> row['authorBirthDate'] == '1988-04-25'
  True

  >>> row = {'authorBirthDateKBR': '', 'authorBirthDateISNI': '1988'}
  >>> selectDateFromRole(row, 'author', 'Birth', ['KBR', 'ISNI'], 'authorKBRIdentifier', {})
  >>> row['authorBirthDate'] == '1988'
  True

  Keep it empty if none of the sources provide a date
  >>> row = {'authorBirthDateKBR': '', 'authorBirthDateISNI': ''}
  >>> selectDateFromRole(row, 'author', 'Birth', ['KBR', 'ISNI'], 'authorKBRIdentifier', {})
  >>> row['authorBirthDate'] == ''
  True

  It also works for other roles than author
  >>> row = {'translatorBirthDateKBR': '1988-04-25', 'translatorBirthDateISNI': '1988'}
  >>> selectDateFromRole(row, 'translator', 'Birth', ['KBR', 'ISNI'], 'translatorKBRIdentifier', {})
  >>> row['translatorBirthDate'] == '1988-04-25'
  True

  >>> row = {'illustratorBirthDateKBR': '1988-04-25', 'illustratorBirthDateISNI': '1988'}
  >>> selectDateFromRole(row, 'illustrator', 'Birth', ['KBR', 'ISNI'], 'illustratorKBRIdentifier', {})
  >>> row['illustratorBirthDate'] == '1988-04-25'
  True

  >>> row = {'scenaristBirthDateKBR': '1988-04-25', 'scenaristBirthDateISNI': '1988'}
  >>> selectDateFromRole(row, 'scenarist', 'Birth', ['KBR', 'ISNI'], 'scenaristKBRIdentifier', {})
  >>> row['scenaristBirthDate'] == '1988-04-25'
  True

  Log an error if a mismatch was found and keep both in the output
  >>> row = {'authorKBRIdentifier': '1234', 'authorBirthDateKBR': '1988-04-25', 'authorBirthDateISNI': '1989'}
  >>> selectDateFromRole(row, 'author', 'Birth', ['KBR', 'ISNI'], 'authorKBRIdentifier', {})
  >>> row['authorBirthDate'] == '1988-04-25 or 1989'
  True

  The same works also for death dates
  >>> row = {'authorDeathDateKBR': '1988-04-25', 'authorDeathDateISNI': '1988'}
  >>> selectDateFromRole(row, 'author', 'Death', ['KBR', 'ISNI'], 'authorKBRIdentifier', {})
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
def selectDate(row, dateType, sources, rowIDCol, mismatchLog, mismatchLogKey):
  """This function chooses the most complete date for the given row, possible dateTypes are 'Birth' and 'death'.

  Select the most complete date betwen the sources
  >>> row = {'birthDateKBR': '1988-04-25', 'birthDateISNI': '1988'}
  >>> selectDate(row, 'birthDate', ['KBR', 'ISNI'], 'authorKBRIdentifier', {}, 'key')
  >>> row['birthDate'] == '1988-04-25'
  True

  >>> row = {'birthDateKBR': '', 'birthDateISNI': '1988'}
  >>> selectDate(row, 'birthDate', ['KBR', 'ISNI'], 'authorKBRIdentifier', {}, 'key')
  >>> row['birthDate'] == '1988'
  True

  Keep it empty if none of the sources provide a date
  >>> row = {'birthDateKBR': '', 'birthDateISNI': ''}
  >>> selectDate(row, 'birthDate', ['KBR', 'ISNI'], 'authorKBRIdentifier', {}, 'key')
  >>> row['birthDate'] == ''
  True

  Log an error if a mismatch was found and keep both in the output
  >>> row = {'authorKBRIdentifier': '1234', 'birthDateKBR': '1988-04-25', 'birthDateISNI': '1989'}
  >>> selectDate(row, 'birthDate', ['KBR', 'ISNI'], 'authorKBRIdentifier', {}, 'key')
  >>> row['birthDate'] == '1988-04-25 or 1989'
  True

  The same works also for death dates
  >>> row = {'deathDateKBR': '1988-04-25', 'deathDateISNI': '1988'}
  >>> selectDate(row, 'deathDate', ['KBR', 'ISNI'], 'authorKBRIdentifier', {}, 'key')
  >>> row['deathDate'] == '1988-04-25'
  True
  """

  # extract all possible dates based on different sources
  dates = []
  for s in sources:
    colName = f'{dateType}{s}'
    if colName in row:
      dates.append(row[colName])

  outputColName = f'{dateType}'

  # set the selected value
  row[outputColName] = mostCompleteDate(dates)

  # In case the different dates do not match log it
  # the date should then be e.g. "1972-04 or 1970"
  if 'or' in row[outputColName]:

    contributorURI = row[rowIDCol]
    # log the mismatching data and then remove the initial sources
    for s in sources:
      colName = f'{dateType}{s}'
      value = row[colName]
      addToMismatchLog(mismatchLog, dateType, mismatchLogKey, contributorURI, s, value)
      row.pop(colName)

  else:
    # only remove the initial sources
    for s in sources:
      colName = f'{dateType}{s}'
      if colName in row:
        row.pop(colName)

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
def getNormalizedString(s):
  """This function returns a normalized copy of the given string.

  >>> getNormalizedString("HeLlO")
  'hello'
  >>> getNormalizedString("judaïsme, islam, christianisme, ET sectes apparentées")
  'judaisme islam christianisme et sectes apparentees'
  >>> getNormalizedString("chamanisme, de l’Antiquité…)")
  'chamanisme de lantiquite...)'

  >>> getNormalizedString("Abe Ce De ?")
  'abe ce de'
  >>> getNormalizedString("Abe Ce De !")
  'abe ce de'
  >>> getNormalizedString("Abe Ce De :")
  'abe ce de'

  >>> getNormalizedString("A. W. Bruna & zoon")
  'a. w. bruna & zoon'
  >>> getNormalizedString("A.W. Bruna & Zoon")
  'a.w. bruna & zoon'
  
  """
  noComma = s.replace(',', '')
  noQuestionMark = noComma.replace('?', '')
  noExclamationMark = noQuestionMark.replace('!', '')
  noColon = noExclamationMark.replace(':', '')
  return ud.normalize('NFKD', noColon).encode('ASCII', 'ignore').lower().strip().decode("utf-8")

# -----------------------------------------------------------------------------
def extractLocationFromLocationCountryString(value):
  """This function extracts the location from a string where the country is additionally indicates.
  >>> extractLocationFromLocationCountryString('Gent (Belgium)')
  'Gent'
  >>> extractLocationFromLocationCountryString('Gent')
  'Gent'
  >>> extractLocationFromLocationCountryString('(Belgium)')
  '(Belgium)'
  """
  if value.endswith(')') and not value.startswith('('):
    found = re.search('^(.*)\(.*', value)
    if found:
      return found.group(1).strip()
  else:
    return value

# -----------------------------------------------------------------------------
def getGeoNamesMainSpellingFromDataFrame(df, identifier):
  """This function extracts the main spelling from a pandas dataframe filled with geonames data.
  >>> data1 = [
  ... ["6693370","Bruxelles-Capitale","Bruxelles-Capitale","BRU,Brussel-Hoofdstad,Bruxelas-Capital","50.84877","4.34664","A","ADM2","BE","","BRU","BRU","","",0,"","26","Europe/Brussels","2016-12-19"],
  ... ["2797657","Gent","Gent","44021,Arrondissement de Gand,Gand,Gent,Ghent","51.07304","3.73664","A","ADM4","BE","","VLG","VOV","44","44021","262219","",4,"Europe/Brussels","2020-04-04"],
  ... ["2797659","Genovabeek","Genovabeek","Genovabeek,Genovevabeek","50.83222","5.01696","H","STM","BE","","VLG","","","",0,"","30","Europe/Brussels","2012-01-18"]]
  >>> getGeoNamesMainSpellingFromDataFrame(pd.DataFrame(data1), "2797657")
  'Gent'
  """
  return (df.loc[df[0] == identifier, 1]).item()

# -----------------------------------------------------------------------------
def getGeoNamesLatitude(df, identifier):
  """This function extracts the main spelling from a pandas dataframe filled with geonames data.
  >>> data1 = [
  ... ["6693370","Bruxelles-Capitale","Bruxelles-Capitale","BRU,Brussel-Hoofdstad,Bruxelas-Capital","50.84877","4.34664","A","ADM2","BE","","BRU","BRU","","",0,"","26","Europe/Brussels","2016-12-19"],
  ... ["2797657","Gent","Gent","44021,Arrondissement de Gand,Gand,Gent,Ghent","51.07304","3.73664","A","ADM4","BE","","VLG","VOV","44","44021","262219","",4,"Europe/Brussels","2020-04-04"],
  ... ["2797659","Genovabeek","Genovabeek","Genovabeek,Genovevabeek","50.83222","5.01696","H","STM","BE","","VLG","","","",0,"","30","Europe/Brussels","2012-01-18"]]
  >>> getGeoNamesLatitude(pd.DataFrame(data1), "2797657")
  '51.07304'
  """
  return (df.loc[df[0] == identifier, 4]).item()

# -----------------------------------------------------------------------------
def getGeoNamesLongitude(df, identifier):
  """This function extracts the main spelling from a pandas dataframe filled with geonames data.
  >>> data1 = [
  ... ["6693370","Bruxelles-Capitale","Bruxelles-Capitale","BRU,Brussel-Hoofdstad,Bruxelas-Capital","50.84877","4.34664","A","ADM2","BE","","BRU","BRU","","",0,"","26","Europe/Brussels","2016-12-19"],
  ... ["2797657","Gent","Gent","44021,Arrondissement de Gand,Gand,Gent,Ghent","51.07304","3.73664","A","ADM4","BE","","VLG","VOV","44","44021","262219","",4,"Europe/Brussels","2020-04-04"],
  ... ["2797659","Genovabeek","Genovabeek","Genovabeek,Genovevabeek","50.83222","5.01696","H","STM","BE","","VLG","","","",0,"","30","Europe/Brussels","2012-01-18"]]
  >>> getGeoNamesLongitude(pd.DataFrame(data1), "2797657")
  '3.73664'
  """
  return (df.loc[df[0] == identifier, 5]).item()

# -----------------------------------------------------------------------------
def extractStringFromBrackets(value):
  """This function extracts a string in different brackets.
  >>> extractStringFromBrackets('[Brussels]')
  'Brussels'
  >>> extractStringFromBrackets('(Ghent)')
  'Ghent'
  >>> extractStringFromBrackets('Gent')
  'Gent'
  >>> extractStringFromBrackets('')
  ''

  Nothing should be extracted when threre is content before the brackets
  >>> extractStringFromBrackets('Gent (Belgium)')
  'Gent (Belgium)'
  """
  found = None
  if value.startswith('('):
    found = re.search('^\((.*)\)', value)
  elif value.startswith('['):
    found = re.search('\[(.*)\]', value)
  else:
    return value

  if found:
    return found.group(1)
  else:
    return ''

# -----------------------------------------------------------------------------
def extract_geonames(inputDataframe):
    """This function creates a lookup dictionary based on geonames data where possible spellings of a place are the keys and their IDs the value.
    >>> data1 = [
    ... ["2800866","Brussels","Brussels","An Bhruiseil,An Bhruiséil,BRU,Brasels,Breissel,Brisel,Brisele,Briuselis,Brjuksel,Brjusel',Brjussel',Brueksel,Bruessel,Bruesszel,Bruiseal,Bruksel,Bruksela,Brukseli,Brukselo,Brusehl',Brusel,Brusela,Bruselas,Bruseles,Bruselj,Bruselo,Brusel·les,Brussel,Brussele,Brussels,Brussel·les,Bruxel,Bruxelas,Bruxellae,Bruxelles,Brwsel,Bryssel,Bryusel,Bryxelles,Bréissel,Brüksel,Brüssel,Brüsszel,Citta di Bruxelles,Città di Bruxelles,City of Brussels,Kota Brusel,beulwisel,bi lu xi,braselasa,braselsa,brassels,briuseli,brwksl,brysl,bu lu sai er,buryusseru,Βρυξέλλες,Брисел,Брусэль,Брюксел,Брюсель,Брюссель,Բրյուսել,בריסל,ﺏﺭﻮﻜﺴﻟ,ﺏﺭﻮﮑﺴﻟ,ﺏﺮﻳۇﺲﺳېﻝ,ܒܪܘܟܣܠ,ब्रसेल्स,ব্রাসেলস,บรัสเซลส์,ბრიუსელი,ブリュッセル,布魯塞爾,布鲁塞尔,比律悉,브뤼셀","50.85045","4.34878","P","PPLC","BE","BRU","BRU","21","21004","1019022","28","Europe/Brussels","2022-03-09"],
    ... ["2797656","Gent","Gent","GNE,Gaent,Gand,Gandavum,Gandawa,Gande,Gant,Gante,Ganti,Gent,Gentas,Gente,Gento,Ghent,Gint,Gænt,gen te,genta,ghnt,gnt,henteu,hento,jenta,jnt,ken t,khenta,khnt,Γάνδη,Гент,Գենտ,גנט,ﺞﻨﺗ,ﺦﻨﺗ,ﻎﻨﺗ,ﻎﯿﻧٹ,खेंट,गेंट,জেন্ট,เกนต์,ဂင့်မြိ,გენტი,ヘント,根特,헨트","51.05","3.71667","P","PPL","BE","VLG","VOV","44","44021","231493","10","Europe/Brussels","2019-09-"],
    ... ["2797657","Gent","Gent","44021,Arrondissement de Gand,Gand,Gent,Ghent","51.07304","3.73664","A","ADM4","BE","","VLG","VOV","44","44021","262219","",4,"Europe/Brussels","2020-04-04"],
    ... ["2797659","Genovabeek","Genovabeek","Genovabeek,Genovevabeek","50.83222","5.01696","H","STM","BE","","VLG","","","",0,"","30","Europe/Brussels","2012-01-18"]]
    >>> mapping = extract_geonames(pd.DataFrame(data1))
    >>> mapping['gent']
    '2797656'
    >>> mapping['ghent']
    '2797656'
    >>> mapping['bruxelles']
    '2800866'
    """ 
    geo_ids = {}

    # we are only interested in cities not administrative units (starting with AD)
    # for example we want PPL (place), PPLC (capital of political entity) or PPLA2 (seat of second-order administrative division)
    g = inputDataframe[inputDataframe[7].astype(str).str.startswith('PP')]

    # Add the column with all the alternate spellings (comma-separated list) to the lookup
    #
    messy_column = dict(zip(g[3], g[0]))

    for key, value in messy_column.items():
        if isinstance(key, str):
            new_keys = key.split(",")
            for new_key in new_keys:
                geo_ids[new_key] = value

    # Also add the two main spellings to the lookup
    #
    geo_ids.update(dict(zip(g[1], g[0])))
    geo_ids.update(dict(zip(g[2], g[0])))

    geo_ids_normalized = {}

    for key, value in geo_ids.items():
        key_normalized = getNormalizedString(key)
        geo_ids_normalized[key_normalized] = value

    return geo_ids_normalized

def normalizeDelimiters(value, delimiter=';'):
  """This function replaces other found delimiters with the given.
  >>> normalizeDelimiters('Leuven. - Paris')
  'Leuven;Paris'
  >>> normalizeDelimiters('Leuven - Paris')
  'Leuven;Paris'
  >>> normalizeDelimiters('Brussels')
  'Brussels'
  >>> normalizeDelimiters('Sint-Martens-Latem. - Paris')
  'Sint-Martens-Latem;Paris'
  """
  return value.replace('. - ', delimiter).replace(' - ', delimiter)

def extract_places_tsv(df, columnname_places, columnname_countries):
    """This function extracts places from the given dataframe
    >>> data1 = pd.DataFrame([{"place": "Arles;Montréal", "country": ""},{"place": "", "country": ""},{"place": "Gent", "country": ""}, {"place": "Brussels ; Paris", "country": ""}, {"place": "[Marcinelle]", "country": ""}])
    >>> extract_places_tsv(data1, "place", "country")
    [('arles;montreal', ''), ('', ''), ('gent', ''), ('brussels ; paris', ''), ('marcinelle', '')]
    """
    places = df[columnname_places].replace(to_replace=r'\[|\]|(\(.*?\))', value='', regex=True)
    countries = df[columnname_countries]
    places = list(places)
    countries = list(countries)

    places_clean = []
    for place in places:
        if type(place) is not float:
            place = getNormalizedString(place)
            if ". - " in place:
                place = place.replace(". - ", " ; ")
            elif " - " in place:
                place = place.replace(" - ", " ; ")
            places_clean.append(place.strip())
        else:
            places_clean.append("")

    place_country = list(zip(places_clean, countries))

    return place_country


# -----------------------------------------------------------------------------
def countRowsWithValueForColumn(df, column):
  """This function returns the number of rows for the provided column in the provided pandas dataframe which are not empty (or are not NaN).
  >>> data1 = pd.DataFrame([{'id': '1', 'value': ''},{'id': '2', 'value': '2'},{'id': 3},{'id': '4', 'value': '4'},{'id': '5', 'value': 5}])
  >>> countRowsWithValueForColumn(data1, 'value')
  3
  """
  myDf = df.fillna('')
  return (myDf[column].values != '').sum()

# -----------------------------------------------------------------------------
def countRowsWithMultipleValuesForColumn(df, column, delimiter=';'):
  """This function returns the number of rows in the given dataframe and column containing the given delimiter string.
  >>> data1 = pd.DataFrame([{'id': '1', 'value': 'hello'},{'id': '2', 'value': 'hello;world'},{'id': '3', 'value': '12;34'}])
  >>> countRowsWithMultipleValuesForColumn(data1, 'value')
  2
  """
  myDf = df.fillna('')
  return (myDf[column].str.contains(delimiter)).sum()

# -----------------------------------------------------------------------------
def createCorpusMeasurements(corpus, identifier, comment):
  timestamp = datetime.now()

  measurement = {
    'date': timestamp,
    'corpus': identifier,
    'numberTranslations': len(corpus.index),
    'withTargetISBN10': countRowsWithValueForColumn(corpus, 'targetISBN10'),
    'withTargetISBN13': countRowsWithValueForColumn(corpus, 'targetISBN13'),
    'withKBRIdentifier': countRowsWithValueForColumn(corpus, 'targetKBRIdentifier'),
    'withBnFIdentifier': countRowsWithValueForColumn(corpus, 'targetBnFIdentifier'),
    'withKBIdentifier': countRowsWithValueForColumn(corpus, 'targetKBIdentifier'),
    'withBBThesaurusID': countRowsWithValueForColumn(corpus, 'targetThesaurusBB'),
    'withSourceKBRIdentifier': countRowsWithValueForColumn(corpus, 'sourceKBRIdentifier'),
    'withSourceTitle': countRowsWithValueForColumn(corpus, 'sourceTitle'),
    'withSourceISBN10': countRowsWithValueForColumn(corpus, 'sourceISBN10'),
    'withSourceISBN13': countRowsWithValueForColumn(corpus, 'sourceISBN13'),
    'comment': comment
  }
  return measurement

# -----------------------------------------------------------------------------
def createContributorCorpusMeasurements(corpus, comment):
  timestamp = datetime.now()

  measurement = {
    'date': timestamp,
    'numberContributors': len(corpus.index),
    'withKBRIdentifier': countRowsWithValueForColumn(corpus, 'kbrIDs'),
    'withBnFIdentifier': countRowsWithValueForColumn(corpus, 'bnfIDs'),
    'withKBIdentifier': countRowsWithValueForColumn(corpus, 'ntaIDs'),
    'withISNIIdentifier': countRowsWithValueForColumn(corpus, 'isniIDs'),
    'withVIAFIdentifier': countRowsWithValueForColumn(corpus, 'viafIDs'),
    'withWikidataIdentifier': countRowsWithValueForColumn(corpus, 'wikidataIDs'),
    'withBirthDate': countRowsWithValueForColumn(corpus, 'birthDate'),
    'withDeathDate': countRowsWithValueForColumn(corpus, 'deathDate'),
    'withNationality': countRowsWithValueForColumn(corpus, 'nationalities'),
    'withMultipleKBRIdentifiers': countRowsWithMultipleValuesForColumn(corpus, 'kbrIDs'),
    'withMultipleBnFIdentifiers': countRowsWithMultipleValuesForColumn(corpus, 'bnfIDs'),
    'withMultipleNTAIdentifiers': countRowsWithMultipleValuesForColumn(corpus, 'ntaIDs'),
    'withMultipleISNIIdentifiers': countRowsWithMultipleValuesForColumn(corpus, 'isniIDs'),
    'withMultipleVIAFIdentifiers': countRowsWithMultipleValuesForColumn(corpus, 'viafIDs'),
    'withMultipleWikidataIdentifiers': countRowsWithMultipleValuesForColumn(corpus, 'wikidataIDs'),
    'withMultipleBirthDates': countRowsWithMultipleValuesForColumn(corpus, 'birthDate', delimiter='or'),
    'withMultipleDeathDates': countRowsWithMultipleValuesForColumn(corpus, 'deathDate', delimiter='or'),
    'withMultipleNationalities': countRowsWithMultipleValuesForColumn(corpus, 'nationalities'),
    'comment': comment
  }
  return measurement

# -----------------------------------------------------------------------------
def countColumnOccurrence(df, columnName, value):
  """This function counts in how many rows 'value' is part of the column with the given name.
  >>> data1 = pd.DataFrame([{'myCol': ''},{'myCol': 'Sven (1234)'},{'myCol': 'John (abc)'},{'myCol': 'Sven (abc, 1234)'}])
  >>> countColumnOccurrence(data1, 'myCol', '1234')
  2
  >>> data2 = pd.DataFrame([{'myCol': ''},{'myCol': 'Sven (111)'},{'myCol': 'John (abc)'},{'myCol': 'Sven (abc, 111)'}])
  >>> countColumnOccurrence(data2, 'myCol', '1234')
  0

  Only one occurrence per cell is counted, for example 'Sven' is counted one in the second row even though
  it mentions Sven twice, one time as "Sven Lieber" and one time as "Lieber, Sven"
  >>> data3 = pd.DataFrame([{'myCol': ''},{'myCol': 'Sven Lieber (111); Lieber, Sven (abc)'},{'myCol': 'John (abc)'},{'myCol': 'Sven (abc, 111)'}])
  >>> countColumnOccurrence(data2, 'myCol', 'Sven')
  2
  """
  return df[df[columnName].str.contains(value)].shape[0]

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
