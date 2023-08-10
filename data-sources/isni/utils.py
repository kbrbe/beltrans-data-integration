

# -----------------------------------------------------------------------------
def atLeastOneIdentifierMissing(row, columnNames):
  """This function returns true if at least one of the given columns are empty.
  >>> atLeastOneIdentifierMissing({'kbrIDs': '', 'ntaIDs':''}, ['kbrIDs', 'ntaIDs'])
  True
  >>> atLeastOneIdentifierMissing({'kbrIDs': '123', 'ntaIDs':''}, ['kbrIDs', 'ntaIDs'])
  True
  >>> atLeastOneIdentifierMissing({'kbrIDs': '123', 'ntaIDs':'456'}, ['kbrIDs', 'ntaIDs'])
  False
  """
  
  relevantValues = [row[c] for c in columnNames]
  return True if any([True for v in relevantValues if v == '' ]) else False

# -----------------------------------------------------------------------------
def countISNIs(isniString, delimiter=';', validateISNI=False):
  """Counts how many ISNIs are in the delimited string.

  An empty string should be counted as 0 ISNIs
  >>> countISNIs('')
  0

  One ISNI should be counted
  >>> countISNIs('0000000000000001')
  1
  
  Multiple ISNI values should be counted
  >>> countISNIs('0000000000000001;0000000000000002')
  2

  Multiple value should be counted, in default even if not valid ISNIs
  >>> countISNIs('001;002')
  2

  If something does not seem like an ISNI (currently only checking for length) an exception is thrown
  >>> countISNIs('0001', validateISNI=True)
  Traceback (most recent call last):
   ...
  Exception: Invalid ISNI: "0001"

  >>> countISNIs('000000000001;002', validateISNI=True)
  Traceback (most recent call last):
   ...
  Exception: Invalid ISNI: "000000000001"
  
  """
  if isniString == '':
    return 0
  isniList = isniString.split(delimiter)
  if validateISNI:
    for isni in isniList:
      if len(isni) != 16:
        raise Exception(f'Invalid ISNI: "{isni}"')
  else:
    return len(isniList)

# -----------------------------------------------------------------------------
def initializeCounters(countReader, identifiers, isniColumnName, nationalityColumnName=None):
  """This function counts statistics from the given arra of dicts (or DictReader).

  >>> rows = [{'kbrIDs':'', 'isniIDs':'001','ntaIDs':''},
  ... {'kbrIDs':'123', 'isniIDs':'', 'ntaIDs':''},
  ... {'kbrIDs':'', 'ntaIDs':'', 'isniIDs':''},
  ... {'kbrIDs':'','ntaIDs':'','isniIDs':'002;003'},
  ... {'kbrIDs':'123','ntaIDs':'456','isniIDs':'002;003'}]
  >>> initializeCounters(rows, {'kbrIDs':'KBR', 'ntaIDs':'NTA'}, 'isniIDs')
  {'numberRows': 5, 'numberRowsHaveISNI': 3, 'numberISNIs': 5, 'numberRowsMissingAtLeastOneIdentifier': 4, 'KBR': {'numberMissingIdentifierRows': 3, 'numberISNIs': 5, 'numberRowsToBeEnrichedHaveISNI': 2, 'numberRowsThatCannotBeEnriched': 1}, 'NTA': {'numberMissingIdentifierRows': 4, 'numberISNIs': 5, 'numberRowsToBeEnrichedHaveISNI': 2, 'numberRowsThatCannotBeEnriched': 2}}
  """

  # initialize counters
  counters = {'numberRows': 0, 'numberRowsHaveISNI': 0, 'numberISNIs': 0, 'numberRowsMissingAtLeastOneIdentifier': 0}
  for column, isniSourceName in identifiers.items():
    counters[isniSourceName] = {
      'numberMissingIdentifierRows': 0,
      'numberISNIs': 0,
      'numberRowsToBeEnrichedHaveISNI': 0,
      'numberRowsThatCannotBeEnriched': 0,
      'numberFoundISNIRows': 0,
      'numberFoundISNIs': 0
    }
  

  identifierColumns = identifiers.keys()
  for row in countReader:

    # do some general counting for the row
    counters['numberRows'] += 1
    counters['numberISNIs'] += countISNIs(row[isniColumnName])
    if atLeastOneIdentifierMissing(row, identifierColumns):
      counters['numberRowsMissingAtLeastOneIdentifier'] += 1

    if row[isniColumnName] != '':
        counters['numberRowsHaveISNI'] += 1

    # count for the specific identifiers we want to add via ISNI
    for columnName, isniSourceName in identifiers.items():

      counters[isniSourceName]['numberISNIs'] += countISNIs(row[isniColumnName])
      # the identifier column is empty, a possible candidate to be enriched
      if row[columnName] == '':
        counters[isniSourceName]['numberMissingIdentifierRows'] += 1

        # If there is also an ISNI there is the chance that we can enrich it
        if row[isniColumnName] == '':
          counters[isniSourceName]['numberRowsThatCannotBeEnriched'] += 1
        else:
          counters[isniSourceName]['numberRowsToBeEnrichedHaveISNI'] += 1

  return counters



# -----------------------------------------------------------------------------
def count(stats, counter):
  """ This function simply adds to the given counter or creates it if not yet existing in 'stats'.

  >>> stats = {}
  >>> count(stats, 'myCounter')
  >>> stats['myCounter']
  1
  """
  if counter in stats:
    stats[counter] += 1
  else:
    stats[counter] = 1

# -----------------------------------------------------------------------------
def countStat(stats, counter, value):
  """ This function logs the value 'value' in the dictionary 'stats' under the key 'counter'. Additionally min, max and number are stored.

  An empty stats dictionary is filled.
  >>> stats = {}
  >>> countStat(stats, 'myCounter', 1)
  >>> stats['myCounter']
  {'min': 1.0, 'max': 1.0, 'avg': 1.0, 'number': 1, 'values': [1.0]}

  Stats are correctly computed and added for already existing counters.
  >>> stats =  { 'myCounter': {'min': 1.0, 'max': 3.0, 'avg': 2, 'number': 3, 'values': [1.0, 2.0, 3.0]}}
  >>> countStat(stats, 'myCounter', 7)
  >>> stats['myCounter']
  {'min': 1.0, 'max': 7.0, 'avg': 3.25, 'number': 4, 'values': [1.0, 2.0, 3.0, 7.0]}
  """
  value = float(value)
  if counter in stats:
    stats[counter]['values'].append(value)
    stats[counter]['number'] += 1
    stats[counter]['min'] = min(stats[counter]['min'], value)
    stats[counter]['max'] = max(stats[counter]['max'], value)
    stats[counter]['avg'] = sum(stats[counter]['values'])/len(stats[counter]['values'])
  else:
    stats[counter] = {'min': value, 'max': value, 'avg': value, 'number': 1, 'values': [value]}


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
