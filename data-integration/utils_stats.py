import pandas as pd
import numpy as np
from datetime import datetime
import os
import re

# -----------------------------------------------------------------------------
def countRowsWithValueForColumn(df, column):
  """This function returns the number of rows for the provided column in the provided pandas dataframe which are not empty (or are not NaN).
  >>> data1 = pd.DataFrame([{'id': '1', 'value': ''},{'id': '2', 'value': '2'},{'id': 3},{'id': '4', 'value': '4'},{'id': '5', 'value': 5}])
  >>> countRowsWithValueForColumn(data1, 'value')
  3

  A column which does not exist should lead to 0 rows with a value
  Like this we ensure that measurements on newly added columns can also be executed on old corpus versions 
  >>> countRowsWithValueForColumn(data1, 'newColumn')
  0
  """
  if column not in df.columns:
    return 0

  myDf = df.fillna('')
  return (myDf[column].values != '').sum()

# -----------------------------------------------------------------------------
def countRowsWithValueForColumns(df, columns, whereColumnsEmpty=None):
  """This function returns the number of rows for the provided columns in the provided pandas dataframe which are not empty (or are not NaN).
  If an optional list of columns is given, only the number of rows is returned with values for the given values, but where the whereColumnsEmpty columns have to be empty
  >>> data1 = pd.DataFrame([
  ... {'id': '1', 'value': ''},
  ... {'id': '2', 'value': '2'},
  ... {'id': 3},
  ... {'id': '4', 'value': '4'},
  ... {'id': '5', 'value': 5}])
  >>> countRowsWithValueForColumns(data1, ['value'])
  3

  >>> data2 = pd.DataFrame([
  ... {'id': '1', 'KBRID': '1', 'BnFID': '1'},
  ... {'id': '2', 'KBRID': '2', 'BnFID': '2', 'KBID': '2'},
  ... {'id': 3},
  ... {'id': '4', 'KBRID': '', 'KBID': '4'},
  ... {'id': '5', 'value': 5}])
  >>> countRowsWithValueForColumns(data2, ['KBRID'])
  2
  >>> countRowsWithValueForColumns(data2, ['BnFID'])
  2
  >>> countRowsWithValueForColumns(data2, ['KBID'])
  2
  >>> countRowsWithValueForColumns(data2, ['KBRID', 'BnFID'])
  2
  >>> countRowsWithValueForColumns(data2, ['KBRID', 'BnFID', 'KBID'])
  1
  >>> data3 = pd.DataFrame([
  ... {'id': '1', 'KBRID': '1', 'BnFID': '1', 'nationality': ''},
  ... {'id': '2', 'KBRID': '2', 'BnFID': '2', 'KBID': '2', 'nationality': 'Belgium'},
  ... {'id': 3},
  ... {'id': '4', 'KBRID': '', 'KBID': '4', 'nationality': 'Dutch'},
  ... {'id': '5', 'value': 5},
  ... {'id': '6', 'KBRID': '6', 'BnFID': '6', 'nationality': ''},
  ... {'id': '7', 'KBRID': '7', 'BnFID': '7', 'nationality': ''},
  ... {'id': '8', 'KBRID': '8', 'BnFID': '8'}])
  >>> countRowsWithValueForColumns(data3, ['KBRID'], ['nationality'])
  4

  It should also work if a non-existent columns is used

  >>> countRowsWithValueForColumns(data3, ['KBRID', 'targetUnescoIdentifier'])
  0
 
  """

  myDf = df.copy() 
  for col in columns:
    if col not in df.columns:
      myDf[col] = ''

  # set empty values to nan such that the isnull()/notnull() approach below will work properly
  myDf = myDf.replace('', np.nan)

  # filter step: rows with the optionally given column should have an empty value for that column
  if whereColumnsEmpty is not None:
    if pd.Series(whereColumnsEmpty).isin(myDf.columns).all():
      preSelection = myDf[whereColumnsEmpty].isnull().all(1)
      myDf = myDf[preSelection]

  # get the number of rows where the given columns have a value (based on possibly already pre-filtered data)
  return sum(myDf[columns].notnull().all(1))




# -----------------------------------------------------------------------------
def countRowsWithMultipleValuesForColumn(df, column, delimiter=';'):
  """This function returns the number of rows in the given dataframe and column containing the given delimiter string.
  >>> data1 = pd.DataFrame([{'id': '1', 'value': 'hello'},{'id': '2', 'value': 'hello;world'},{'id': '3', 'value': '12;34'}])
  >>> countRowsWithMultipleValuesForColumn(data1, 'value')
  2
  """
  myDf = df.copy() 
  if column not in df.columns:
    myDf[column] = ''

 
  myDf = myDf.fillna('')
  return (myDf[column].str.contains(delimiter)).sum()

# -----------------------------------------------------------------------------
def countValuesUsedInDifferentRows(df, column, delimiter=';'):
  """This function returns the number of values that occur in more than one row.

  The identifier '1' and '2' are used in more than one row, so the answer should be 2
  >>> data1 = pd.DataFrame([{'id': '1', 'value': '1;2'},{'id': '2', 'value': '2'},{'id': '3', 'value': '3'},{'id': '4', 'value': '1;4'}])
  >>> countValuesUsedInDifferentRows(data1, 'value')
  2
  """

  myDf = df.copy()
  myDf[column] = myDf[column].str.split(delimiter)
  explodedDf = myDf.explode(column).reset_index()

  groups = explodedDf.groupby([column]).size().reset_index(name='count')
  return groups[groups['count'] > 1].shape[0]

# -----------------------------------------------------------------------------
def createCorrelationListPersonMeasurements(correlationList, correlationListDate):

  timestamp = datetime.now()

  measurement = {
    'date': correlationListDate,
    'measurementTime': timestamp,
    'numberEntries': len(correlationList.index),
    'withGender': countRowsWithValueForColumn(correlationList, 'gender'),
    'withBirthDate': countRowsWithValueForColumn(correlationList, 'birthDate'),
    'withDeathDate': countRowsWithValueForColumn(correlationList, 'deathDate'),
    'withKBRIdentifier': countRowsWithValueForColumn(correlationList, 'kbrIDs'),
    'withBnFIdentifier': countRowsWithValueForColumn(correlationList, 'bnfIDs'),
    'withNTAIdentifier': countRowsWithValueForColumn(correlationList, 'ntaIDs'),
    'withUnescoIdentifier': countRowsWithValueForColumn(correlationList, 'unescoIDs'),
    'withVIAFIdentifier': countRowsWithValueForColumn(correlationList, 'viafIDs'),
    'withISNIIdentifier': countRowsWithValueForColumn(correlationList, 'isniIDs'),
    'withWikidataIdentifier': countRowsWithValueForColumn(correlationList, 'wikidataIDs') if 'wikidataIDs' in correlationList else 0,
    'withMultipleGender': countRowsWithMultipleValuesForColumn(correlationList, 'gender'),
    'withMultipleKBR': countRowsWithMultipleValuesForColumn(correlationList, 'kbrIDs'),
    'withMultipleBnF': countRowsWithMultipleValuesForColumn(correlationList, 'bnfIDs'),
    'withMultipleNTA': countRowsWithMultipleValuesForColumn(correlationList, 'ntaIDs'),
    'withMultipleUnesco': countRowsWithMultipleValuesForColumn(correlationList, 'unescoIDs'),
    'withMultipleVIAF': countRowsWithMultipleValuesForColumn(correlationList, 'viafIDs'),
    'withMultipleISNI': countRowsWithMultipleValuesForColumn(correlationList, 'isniIDs'),
    'withMultipleWikidata': countRowsWithMultipleValuesForColumn(correlationList, 'wikidataIDs') if 'wikidataIDs' in correlationList else 0,
    'duplicateKBR': countValuesUsedInDifferentRows(correlationList, 'kbrIDs'),
    'duplicateBnF': countValuesUsedInDifferentRows(correlationList, 'bnfIDs'),
    'duplicateNTA': countValuesUsedInDifferentRows(correlationList, 'ntaIDs'),
    'duplicateUnesco': countValuesUsedInDifferentRows(correlationList, 'unescoIDs'),
    'duplicateVIAF': countValuesUsedInDifferentRows(correlationList, 'viafIDs'),
    'duplicateISNI': countValuesUsedInDifferentRows(correlationList, 'isniIDs'),
    'duplicateWikidata': countValuesUsedInDifferentRows(correlationList, 'wikidataIDs') if 'wikidataIDs' in correlationList else 0,
  }
  return measurement

# -----------------------------------------------------------------------------
def createCorpusMeasurements(corpus, corpusDate, identifier, comment):
  timestamp = datetime.now()

  # over the time we used different column names for the target publisher
  targetPublisherColumns = ['publisherIdentifiers', 'targetPublisherIdentifiers']
  targetPublisherColumnName = 'publisherIdentifiers' # default value
  for colName in targetPublisherColumns:
    if colName in corpus:
      targetPublisherColumnName = colName
      break
  
  measurement = {
    'date': corpusDate,
    'measurementTime': timestamp,
    'corpus': identifier,
    'numberTranslations': len(corpus.index),
    'withTargetISBN10': countRowsWithValueForColumn(corpus, 'targetISBN10'),
    'withTargetISBN13': countRowsWithValueForColumn(corpus, 'targetISBN13'),
    'withKBRIdentifier': countRowsWithValueForColumn(corpus, 'targetKBRIdentifier'),
    'withBnFIdentifier': countRowsWithValueForColumn(corpus, 'targetBnFIdentifier'),
    'withKBIdentifier': countRowsWithValueForColumn(corpus, 'targetKBIdentifier'),
    'withUnescoIdentifier': countRowsWithValueForColumn(corpus, 'targetUnescoIdentifier'),
    'withCollection': countRowsWithValueForColumn(corpus, 'targetCollectionIdentifier'),
    'withKBRBnFKBAndUnescoIdentifier': countRowsWithValueForColumns(corpus, ['targetKBRIdentifier', 'targetBnFIdentifier', 'targetKBIdentifier', 'targetUnescoIdentifier']),
    'withKBRBnFAndKBIdentifier': countRowsWithValueForColumns(corpus, ['targetKBRIdentifier', 'targetBnFIdentifier', 'targetKBIdentifier']),
    'withKBRAndBnFIdentifier': countRowsWithValueForColumns(corpus, ['targetKBRIdentifier', 'targetBnFIdentifier']),
    'withKBRAndKBIdentifier': countRowsWithValueForColumns(corpus, ['targetKBRIdentifier', 'targetKBIdentifier']),
    'withKBRAndUnescoIdentifier': countRowsWithValueForColumns(corpus, ['targetKBRIdentifier', 'targetKBIdentifier', 'targetUnescoIdentifier']),
    'withBnFAndKBIdentifier': countRowsWithValueForColumns(corpus, ['targetBnFIdentifier', 'targetKBIdentifier']),
    'withBnFAndUnescoIdentifier': countRowsWithValueForColumns(corpus, ['targetBnFIdentifier', 'targetUnescoIdentifier']),
    'withKBAndUnescoIdentifier': countRowsWithValueForColumns(corpus, ['targetKBIdentifier', 'targetUnescoIdentifier']),
    'withBBThesaurusID': countRowsWithValueForColumn(corpus, 'targetThesaurusBB'),
    'withSourceBBThesaurusID': countRowsWithValueForColumn(corpus, 'sourceThesaurusBB') if 'sourceThesaurusBB' in corpus else 0,
    'withSourceKBRIdentifier': countRowsWithValueForColumn(corpus, 'sourceKBRIdentifier'),
    'withMultipleSourceKBRIdentifiers': countRowsWithMultipleValuesForColumn(corpus, 'sourceKBRIdentifier'),
    'withSourceTitle': countRowsWithValueForColumn(corpus, 'sourceTitle') if 'sourceTitle' in corpus else 0,
    'withKBRSourceTitle': countRowsWithValueForColumn(corpus, 'sourceTitleKBR'),
    'withKBSourceTitle': countRowsWithValueForColumn(corpus, 'sourceTitleKB') if 'sourceTitleKB' in corpus else 0,
    'withBnFSourceTitle': countRowsWithValueForColumn(corpus, 'sourceTitleBnF') if 'sourceTitleBnF' in corpus else 0,
    'withUnescoSourceTitle': countRowsWithValueForColumn(corpus, 'sourceTitleUnesco') if 'sourceTitleUnesco' in corpus else 0,
    'withSourceISBN10': countRowsWithValueForColumn(corpus, 'sourceISBN10'),
    'withSourceISBN13': countRowsWithValueForColumn(corpus, 'sourceISBN13'),
    'withKBRPublisher': countRowsWithValueForColumn(corpus, 'targetPublisherIdentifierKBR'),
    'withBnFPublisher': countRowsWithValueForColumn(corpus, 'targetPublisherIdentifierBnF'),
    'withKBPublisher': countRowsWithValueForColumn(corpus, 'targetPublisherIdentifierKB'),
    'withUnescoPublisher': countRowsWithValueForColumn(corpus, 'targetPublisherIdentifierUnesco'),
    'withIntegratedAuthor': countRowsWithValueForColumn(corpus, 'authorIdentifiers'),
    'withIntegratedTranslator': countRowsWithValueForColumn(corpus, 'translatorIdentifiers'),
    'withIntegratedIllustrator': countRowsWithValueForColumn(corpus, 'illustratorIdentifiers'),
    'withIntegratedScenarist': countRowsWithValueForColumn(corpus, 'scenaristIdentifiers'),
    'withIntegratedPublishingDirector': countRowsWithValueForColumn(corpus, 'publishingDirectorIdentifiers'),
    'withIntegratedPublisher': countRowsWithValueForColumn(corpus, targetPublisherColumnName) if targetPublisherColumnName in corpus else 0,
    'withIntegratedSourcePublisher': countRowsWithValueForColumn(corpus, 'sourcePublisherIdentifiers') if 'sourcePublisherIdentifiers' in corpus else 0,
    'withTargetPlaceOfPublication': countRowsWithValueForColumn(corpus, 'targetPlaceOfPublication') if 'targetPlaceOfPublication' in corpus else 0,
    'withSourcePlaceOfPublication': countRowsWithValueForColumn(corpus, 'sourcePlaceOfPublication') if 'sourcePlaceOfPublication' in corpus else 0,
    'withTargetCountryOfPublication': countRowsWithValueForColumn(corpus, 'targetCountryOfPublication') if 'targetCountryOfPublication' in corpus else 0,
    'withSourceCountryOfPublication': countRowsWithValueForColumn(corpus, 'sourceCountryOfPublication') if 'sourceCountryOfPublication' in corpus else 0,
    'comment': comment
  }
  return measurement

# -----------------------------------------------------------------------------
def createContributorCorpusMeasurements(corpus, corpusDate, comment):
  timestamp = datetime.now()

  measurement = {
    'date': corpusDate,
    'measurementTime': timestamp,
    'numberContributors': len(corpus.index),
    'withKBRIdentifier': countRowsWithValueForColumn(corpus, 'kbrIDs'),
    'withBnFIdentifier': countRowsWithValueForColumn(corpus, 'bnfIDs'),
    'withKBIdentifier': countRowsWithValueForColumn(corpus, 'ntaIDs'),
    'withUnescoIdentifier': countRowsWithValueForColumn(corpus, 'unescoIDs'),
    'withKBRBnFKBAndUnescoIdentifier': countRowsWithValueForColumns(corpus, ['kbrIDs', 'bnfIDs',
                                                                       'ntaIDs', 'unescoIDs']),
    'withKBRBnFAndKBIdentifier': countRowsWithValueForColumns(corpus, ['kbrIDs', 'bnfIDs',
                                                                       'ntaIDs']),
    'withKBRAndBnFIdentifier': countRowsWithValueForColumns(corpus, ['kbrIDs', 'bnfIDs']),
    'withKBRAndKBIdentifier': countRowsWithValueForColumns(corpus, ['kbrIDs', 'ntaIDs']),
    'withKBRAndUnescoIdentifier': countRowsWithValueForColumns(corpus, ['kbrIDs', 'unescoIDs']),
    'withBnFAndKBIdentifier': countRowsWithValueForColumns(corpus, ['bnfIDs', 'ntaIDs']),
    'withBnFAndUnescoIdentifier': countRowsWithValueForColumns(corpus, ['bnfIDs', 'unescoIDs']),
    'withKBAndUnescoIdentifier': countRowsWithValueForColumns(corpus, ['ntaIDs', 'unescoIDs']),
    'withKBRAndISNIIdentifier': countRowsWithValueForColumns(corpus, ['kbrIDs', 'isniIDs']),
    'withKBRAndVIAFIdentifier': countRowsWithValueForColumns(corpus, ['kbrIDs', 'viafIDs']),
    'withKBRAndWikidataIdentifier': countRowsWithValueForColumns(corpus, ['kbrIDs', 'wikidataIDs']),
    'withKBRAndNationality': countRowsWithValueForColumns(corpus, ['kbrIDs', 'nationalities']),
    'withBnFAndISNIIdentifier': countRowsWithValueForColumns(corpus, ['bnfIDs', 'isniIDs']),
    'withBnFAndVIAFIdentifier': countRowsWithValueForColumns(corpus, ['bnfIDs', 'viafIDs']),
    'withBnFAndWikidataIdentifier': countRowsWithValueForColumns(corpus, ['bnfIDs', 'wikidataIDs']),
    'withBnFAndNationality': countRowsWithValueForColumns(corpus, ['bnfIDs', 'nationalities']),
    'withKBAndISNIIdentifier': countRowsWithValueForColumns(corpus, ['ntaIDs', 'isniIDs']),
    'withKBAndVIAFIdentifier': countRowsWithValueForColumns(corpus, ['ntaIDs', 'viafIDs']),
    'withKBAndWikidataIdentifier': countRowsWithValueForColumns(corpus, ['ntaIDs', 'wikidataIDs']),
    'withKBAndNationality': countRowsWithValueForColumns(corpus, ['ntaIDs', 'nationalities']),
    'withUnescoAndISNIIdentifier': countRowsWithValueForColumns(corpus, ['unescoIDs', 'isniIDs']),
    'withUnescoAndVIAFIdentifier': countRowsWithValueForColumns(corpus, ['unescoIDs', 'viafIDs']),
    'withUnescoAndWikidataIdentifier': countRowsWithValueForColumns(corpus, ['unescoIDs', 'wikidataIDs']),
    'withUnescoAndNationality': countRowsWithValueForColumns(corpus, ['unescoIDs', 'nationalities']),
    'withISNIIdentifier': countRowsWithValueForColumn(corpus, 'isniIDs'),
    'withVIAFIdentifier': countRowsWithValueForColumn(corpus, 'viafIDs'),
    'withWikidataIdentifier': countRowsWithValueForColumn(corpus, 'wikidataIDs'),
    'withWikidataButWithoutISNI': countRowsWithValueForColumns(corpus, ['wikidataIDs'],
                                                               whereColumnsEmpty=['isniIDs']),
    'withKBRButWithoutNationality': countRowsWithValueForColumns(corpus, ['kbrIDs'],
                                                                  whereColumnsEmpty=['nationalities']),
    'withBnFButWithoutNationality': countRowsWithValueForColumns(corpus, ['bnfIDs'],
                                                                  whereColumnsEmpty=['nationalities']),
    'withKBButWithoutNationality': countRowsWithValueForColumns(corpus, ['ntaIDs'],
                                                                  whereColumnsEmpty=['nationalities']),
    'withISNIButWithoutNationality': countRowsWithValueForColumns(corpus, ['isniIDs'],
                                                                  whereColumnsEmpty=['nationalities']),
    'withWikidataButWithoutNationality': countRowsWithValueForColumns(corpus, ['wikidataIDs'],
                                                                      whereColumnsEmpty=['nationalities']),
    'withISNIAndWikidataButWithoutNationality': countRowsWithValueForColumns(corpus, ['isniIDs', 'wikidataIDs'],
                                                                             whereColumnsEmpty=['nationalities']),
    'withBirthDate': countRowsWithValueForColumn(corpus, 'birthDate'),
    'withDeathDate': countRowsWithValueForColumn(corpus, 'deathDate'),
    'withNationality': countRowsWithValueForColumn(corpus, 'nationalities'),
    'withMultipleKBRIdentifiers': countRowsWithMultipleValuesForColumn(corpus, 'kbrIDs'),
    'withMultipleBnFIdentifiers': countRowsWithMultipleValuesForColumn(corpus, 'bnfIDs'),
    'withMultipleNTAIdentifiers': countRowsWithMultipleValuesForColumn(corpus, 'ntaIDs'),
    'withMultipleUnescoIdentifiers': countRowsWithMultipleValuesForColumn(corpus, 'unescoIDs'),
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
  #df['date'] = df['date'].dt.date
  return df.set_index('date')



# -----------------------------------------------------------------------------
def getContributorName(nameIDString):
  """
  >>> getContributorName('Lieber, Sven (123,4546)')
  'Lieber, Sven'
  >>> getContributorName('Lieber, Sven ')
  'Lieber, Sven'
  >>> getContributorName('writehi(s)story (3c49e2c2-df3b-457f-b41a-fbe7833bd4d5)')
  'writehi(s)story' 
  """
  contributorName = nameIDString.split('(')[0] if '(' in nameIDString else nameIDString
  return contributorName.strip()

# -----------------------------------------------------------------------------
def getContributorID(nameIDString):
  """
  >>> getContributorID('Lieber, Sven (123)')
  '123'
  >>> getContributorID('Lieber, Sven ')
  ''
  >>> getContributorID('writehi(s)story (3c49e2c2-df3b-457f-b41a-fbe7833bd4d5)')
  '3c49e2c2-df3b-457f-b41a-fbe7833bd4d5'
  """
  if '(' in nameIDString:
    contributorIDs = re.findall(r'\((.*)\)', nameIDString)
    #print(contributorIDs)
    if len(contributorIDs) > 0:
      contributorID = contributorIDs[0]
    else:
      contributorID = ''
  else:
    contributorID = ''
  return contributorID.strip()



# -----------------------------------------------------------------------------
def countContributionBasedOnIdentifier(value, counter, valueDelimiter=';'):
  """This function counts contributors.
  >>> counter = {}
  >>> countContributionBasedOnIdentifier('Lieber, Sven (123)', counter)
  >>> counter['123']
  1
  >>> countContributionBasedOnIdentifier('Sven Lieber (456)', counter)
  >>> counter['456']
  1
  >>> countContributionBasedOnIdentifier('Lieber, Sven (123)', counter)
  >>> counter['123']
  2
  >>> countContributionBasedOnIdentifier('"_$C(128)_"y!"_$C(138,139"', counter)
  >>> counter['128']
  1
  >>> countContributionBasedOnIdentifier('writehi(s)story (3c49e2c2-df3b-457f-b41a-fbe7833bd4d5)', counter)
  >>> counter['3c49e2c2-df3b-457f-b41a-fbe7833bd4d5']
  1
  """
  if value != '':
    contributors = value.split(valueDelimiter) if valueDelimiter in value else [value]
    alreadyProcessed = set()
    for c in contributors:
      contributorName = getContributorID(c)
      if contributorName not in alreadyProcessed:
        alreadyProcessed.add(contributorName)
        if contributorName in counter:
          counter[contributorName] = counter[contributorName] + 1
        else:
          counter[contributorName] = 1


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
      contributorName = getContributorName(c)
      if contributorName not in alreadyProcessed:
        alreadyProcessed.add(contributorName)
        if contributorName in counter:
          counter[contributorName] = counter[contributorName] + 1
        else:
          counter[contributorName] = 1

# -----------------------------------------------------------------------------
def redoManifestationsCorpusMeasurements(config, corpusDirectory, rawDataFilename, measurementFilenameSuffix):

  for corpusVersion in config:
    contributorFile = f'{corpusDirectory}/{corpusVersion}/csv/{rawDataFilename}'
    corpusVersionDate = config[corpusVersion][0]
    corpusVersionComment = config[corpusVersion][1]
    outputFile = f'./measurements/{corpusVersion}_{measurementFilenameSuffix}.csv'
    corpus = pd.read_csv(contributorFile, index_col='targetIdentifier')

    corpusNLFR = corpus[(corpus['sourceLanguage'] == 'Dutch') & (corpus['targetLanguage'] == 'French')]
    corpusFRNL = corpus[(corpus['sourceLanguage'] == 'French') & (corpus['targetLanguage'] == 'Dutch')]
    corpusOther = corpus[((corpus['sourceLanguage'] != 'Dutch') & (corpus['sourceLanguage'] != 'French')) | (
              (corpus['targetLanguage'] != 'Dutch') & (corpus['targetLanguage'] != 'French'))]

    measurements = pd.DataFrame([
      createCorpusMeasurements(corpusFRNL, corpusVersionDate, 'FR-NL', corpusVersionComment),
      createCorpusMeasurements(corpusNLFR, corpusVersionDate, 'NL-FR', corpusVersionComment),
      createCorpusMeasurements(corpusOther, corpusVersionDate, 'OTHER', corpusVersionComment)
    ])

    measurements.to_csv(outputFile, index=False)

# -----------------------------------------------------------------------------
def redoContributorCorpusMeasurements(config, corpusDirectory, rawDataFilename, measurementFilenameSuffix):

  for corpusVersion in config:
    contributorFile = f'{corpusDirectory}/{corpusVersion}/csv/{rawDataFilename}'
    corpusVersionDate = config[corpusVersion][0]
    corpusVersionComment = config[corpusVersion][1]
    outputFile = f'./measurements/{corpusVersion}_{measurementFilenameSuffix}.csv'
    contributors = pd.read_csv(contributorFile, index_col='contributorID')
    measurements = pd.DataFrame([
      createContributorCorpusMeasurements(contributors, corpusVersionDate, corpusVersionComment)
    ])
    measurements.to_csv(outputFile, index=False)

# -----------------------------------------------------------------------------
def redoCorrelationListPersonsMeasurements(config, correlationDir):

  for correlationListVersion, filename in config.items():
    filePath = os.path.join(correlationDir, filename)
    outputFilename = f'./measurements/correlation/{filename}'
    correlationList = pd.read_csv(filePath, index_col='contributorID', dtype=str)
    measurements = pd.DataFrame([
      createCorrelationListPersonMeasurements(correlationList, correlationListVersion)
    ])
    measurements.to_csv(outputFilename, index=False)

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
