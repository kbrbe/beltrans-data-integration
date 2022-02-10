import itertools
from datetime import datetime

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
if __name__ == "__main__":
  import doctest
  doctest.testmod()
