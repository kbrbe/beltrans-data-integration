import pandas as pd

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
def countRowsWithValueForColumns(df, columns):
  """This function returns the number of rows for the provided columns in the provided pandas dataframe which are not empty (or are not NaN).
  >>> data1 = pd.DataFrame([{'id': '1', 'value': ''},{'id': '2', 'value': '2'},{'id': 3},{'id': '4', 'value': '4'},{'id': '5', 'value': 5}])
  >>> countRowsWithValueForColumn(data1, ['value'])
  3

  >>> data1 = pd.DataFrame([{'id': '1', 'KBRID': '1', 'BnFID': '1'},{'id': '2', 'KBRID': '2', 'BnFID': '2', 'KBID': '2'},{'id': 3},{'id': '4', 'KBRID': '', 'KBID': '4'},{'id': '5', 'value': 5}])
  >>> countRowsWithValueForColumns(data1, ['KBRID'])
  2
  >>> countRowsWithValueForColumns(data1, ['BnFID'])
  2
  >>> countRowsWithValueForColumns(data1, ['KBID'])
  2
  >>> countRowsWithValueForColumns(data1, ['KBRID', 'BnFID'])
  2
  >>> countRowsWithValueForColumns(data1, ['KBRID', 'BnFID', 'KBID'])
  1
  """
  myDf = df.fillna('')
  booleanValues = myDf[columns].values != ''
  rowBoolean = []
  for row in booleanValues:
    rowBoolean.append(all(row))
  return sum(rowBoolean)



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
    'withKBRBnFAndKBIdentifier': countRowsWithValueForColumns(corpus, ['targetKBRIdentifier', 'targetBnFIdentifier', 'targetKBIdentifier']),
    'withKBRAndBnFIdentifier': countRowsWithValueForColumns(corpus, ['targetKBRIdentifier', 'targetBnFIdentifier']),
    'withKBRAndKBIdentifier': countRowsWithValueForColumns(corpus, ['targetKBRIdentifier', 'targetKBIdentifier']),
    'withBnFAndKBIdentifier': countRowsWithValueForColumns(corpus, ['targetBnFIdentifier', 'targetKBIdentifier']),
    'withBBThesaurusID': countRowsWithValueForColumn(corpus, 'targetThesaurusBB'),
    'withSourceKBRIdentifier': countRowsWithValueForColumn(corpus, 'sourceKBRIdentifier'),
    'withKBRSourceTitle': countRowsWithValueForColumn(corpus, 'sourceTitleKBR'),
    'withKBSourceTitle': countRowsWithValueForColumn(corpus, 'sourceTitleKB'),
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
    'withKBRBnFAndKBIdentifier': countRowsWithValueForColumns(corpus, ['kbrIDs', 'bnfIDs',
                                                                       'ntaIDs']),
    'withKBRAndBnFIdentifier': countRowsWithValueForColumns(corpus, ['kbrIDs', 'bnfIDs']),
    'withKBRAndKBIdentifier': countRowsWithValueForColumns(corpus, ['kbrIDs', 'ntaIDs']),
    'withBnFAndKBIdentifier': countRowsWithValueForColumns(corpus, ['bnfIDs', 'ntaIDs']),
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
def mergeMeasurementsToDataFrame(folder, files):
  """This function reads the content of the given CSV files and merges them into a Pandas dataframe."""

  filePaths = [os.path.join(folder, f) for f in files]
  df = pd.concat(map(pd.read_csv, filePaths), ignore_index=True)
  df['date'] = pd.to_datetime(df['date'])
  df['date'] = df['date'].dt.date
  return df.set_index('date')



# -----------------------------------------------------------------------------
def countContribution(value, counter, valueDelimiter=';'):
  """This function counts contributors.
  >>> counter = {}
  >>> countContribution('Lieber, Sven (123,456)', counter)
  >>> counter['Lieber, Sven']
  1
  >>> countContribution('Sven Lieber (123,456)', counter)
  >>> counter['Sven Lieber']
  1
  >>> countContribution('Lieber, Sven (123,456)', counter)
  >>> counter['Lieber, Sven']
  2
  >>> countContribution('"_$C(128,129)_"y!"_$C(138,139"', counter)
  >>> counter['"_$C']
  1
  """
  if value != '':
    contributors = value.split(valueDelimiter) if valueDelimiter in value else [value]
    alreadyProcessed = set()
    for c in contributors:
      contributorName = c.split('(')[0] if '(' in c else c
      contributorName = contributorName.strip()
      if contributorName not in alreadyProcessed:
        alreadyProcessed.add(contributorName)
        if contributorName in counter:
          counter[contributorName] = counter[contributorName] + 1
        else:
          counter[contributorName] = 1

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
