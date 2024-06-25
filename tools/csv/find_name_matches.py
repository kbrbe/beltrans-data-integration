
# (c) 2023 Sven Lieber
# KBR Brussels
#
import csv
from tools import utils
from tools.string import utils_string
from argparse import ArgumentParser
from tqdm import tqdm
from thefuzz import fuzz

SIM_ALGORITHMS = ['ratio', 'partial_ratio', 'token_sort_ratio', 'token_set_ratio']

# -----------------------------------------------------------------------------
def main(inputFilename, lookupFilename, outputFilename, similarityAlgorithm, similarityThreshold, inputIDColumn, inputValueColumn, lookupIDColumn, lookupValueColumns, additionalInputColumns, inputDelimiter, lookupDelimiter, valueDelimiter):

  with open(inputFilename, 'r') as inFile:
    inputReader = csv.DictReader(inFile, delimiter=inputDelimiter)
    utils.checkIfColumnsExist(inputReader.fieldnames, [inputIDColumn] + additionalInputColumns)

  #
  # Create lookup
  #
  with open(lookupFilename, 'r') as lookupFile:
    inputReader = csv.DictReader(lookupFile, delimiter=lookupDelimiter)
    utils.checkIfColumnsExist(inputReader.fieldnames, [lookupIDColumn] + lookupValueColumns)

    lookupNameID, lookupIDNames = buildLookup(inputReader, lookupIDColumn, lookupValueColumns)

  #
  # Iterate over input and perform matching
  #
  with open(inputFilename, 'r') as inFile, \
       open(outputFilename, 'w') as outFile:

    candidateColumnCombined = 'candidatesNameID'
    candidateColumnIDs = 'candidateIDs'
    candidateColumnNames = 'candidateNames'
    matchType = "matchType"
    inputReader = csv.DictReader(inFile, delimiter=inputDelimiter)
    outputWriter = csv.DictWriter(outFile, fieldnames=[inputIDColumn] + additionalInputColumns + [matchType, candidateColumnCombined, candidateColumnIDs, candidateColumnNames], delimiter=inputDelimiter)
    outputWriter.writeheader()

    numberNameMatch = 0
    numberSimilarityMatch = 0
    numberNoMatch = 0
    matchingFunction = getattr(fuzz, similarityAlgorithm)

    nameMatchCandidates = {}
    similarityCandidates = {}

    for row in tqdm(inputReader):
      rowID = row[inputIDColumn]
      inputValueString = row[inputValueColumn]

      # there can be more than one value to lookup
      inputValues = inputValueString.split(valueDelimiter) if valueDelimiter in inputValueString else [inputValueString]

      atLeastOneNameMatch = False
      atLeastOneSimilarityMatch = False
      atLeastOneNoMatch = False

      outputRow = {k:v for (k,v) in row.items() if k in additionalInputColumns}
      outputRow[inputIDColumn] = rowID
      
      foundValues = []
      # There are possibly several names to lookup in one row
      for inputValue in inputValues:
        if inputValue == '':
          continue
        nameMatch = True
        normInputValue = utils_string.getNormalizedString(inputValue).replace(' ','')

        # first determine direct matches
        if normInputValue in lookupNameID:
          atLeastOneNameMatch = True
          numberNameMatch += 1
          candidateIDs = lookupNameID[normInputValue] 
          candidateNames = set()
          candidateData = buildCandidateColumns(candidateIDs, lookupIDNames, valueDelimiter)

          # append found nameMatch to output of this row
          foundValues.append(["nameMatch", candidateData[0], candidateData[1], candidateData[2]])
        else:
          similarityCandidates = set()
          # if no direct match is found, try the similarity algorithm
          for lookupName in lookupNameID.keys():
            similarity = matchingFunction(normInputValue, lookupName)
            if similarity >= similarityThreshold:
              atLeastOneSimilarityMatch = True
              print(f'similarity was {similarity}, threshold is {similarityThreshold} ("{normInputValue}", "{lookupName}")')
              numberSimilarityMatch += 1
              similarityCandidates.update(lookupNameID[lookupName])
         
          if similarityCandidates:
            candidateData = buildCandidateColumns(similarityCandidates, lookupIDNames, valueDelimiter)
            # append found nameMatch to output of this row
            foundValues.append(["similarity", candidateData[0], candidateData[1], candidateData[2]])
          else:
            numberNoMatch += 1
            atLeastOneNoMatch = True
            # append found nameMatch to output of this row
            foundValues.append(["no-match", "", "", ""])

      if atLeastOneNameMatch and (not atLeastOneSimilarityMatch) and (not atLeastOneNoMatch):
        outputRow[matchType] = "nameMatches"
      elif atLeastOneSimilarityMatch and (not atLeastOneNameMatch) and (not atLeastOneNoMatch):
        outputRow[matchType] = "similarityMatches"
      elif atLeastOneNoMatch and (not atLeastOneNameMatch) and (not atLeastOneSimilarityMatch):
        outputRow[matchType] = "noMatches"
      elif any([atLeastOneNoMatch, atLeastOneNameMatch, atLeastOneSimilarityMatch]):
        outputRow[matchType] = "partialMatches"
      else:
        outputRow[matchType] = "nothingToLookup"
        

      outputRow[candidateColumnIDs] = valueDelimiter.join([e[1] for e in foundValues])
      outputRow[candidateColumnNames] = valueDelimiter.join([e[2] for e in foundValues])
      outputRow[candidateColumnCombined] = valueDelimiter.join([e[3] for e in foundValues])
      outputWriter.writerow(outputRow) 

    for rowID, matchID in nameMatchCandidates.items():
      print(f'{rowID}: {matchID}')
  print(f'Exact matches {numberNameMatch}, similarity matches {numberSimilarityMatch}, no matches {numberNoMatch}')


# -----------------------------------------------------------------------------
def buildLookup(inputReader, lookupIDColumn, lookupValueColumns):

  lookupNameID = {}
  lookupIDNames = {}
  lookupCounter = 0
  # build the lookup data structure
  #
  for row in inputReader:
    lookupID = row[lookupIDColumn]

    # there can be several lookup columns
    for lookupColumn in lookupValueColumns:
      lookupValue = row[lookupColumn]
      normValue = utils_string.getNormalizedString(lookupValue).replace(' ','')

      if normValue == '':
        continue
      # store lookup: name -> id
      if normValue in lookupNameID:
        lookupNameID[normValue].add(lookupID)
      else:
        lookupNameID[normValue] = set([lookupID])

      # store lookup: id -> name
      if lookupID in lookupIDNames:
        lookupIDNames[lookupID].add(lookupValue)
      else:
        lookupIDNames[lookupID] = set([lookupValue])
    lookupCounter += 1

  print(f'Successfully read {lookupCounter} lookup values!')
  return lookupNameID, lookupIDNames



# -----------------------------------------------------------------------------
def buildCandidateColumns(candidateIDs, lookupIDNames, valueDelimiter):

  candidateNames = set()
  for candidateID in candidateIDs:
    candidateNames.update(lookupIDNames[candidateID])
  candidateColumnIDs = valueDelimiter.join(candidateIDs)
  candidateColumnNames = valueDelimiter.join(candidateNames)
  candidateColumnCombined = valueDelimiter.join([f'{",".join(lookupIDNames[c])} ({c})' for c in candidateIDs])

  return candidateColumnIDs, candidateColumnNames, candidateColumnCombined

# -----------------------------------------------------------------------------
def parseArguments():
  parser = ArgumentParser()
  parser.add_argument('--input-file', required=True, action='store', help='The name of the CSV file from which data should be looked up')
  parser.add_argument('--lookup-file', required=True, action='store', help='The name of the CSV file in which data should be looked up')
  parser.add_argument('--output-file', required=True, action='store', help='The name of the CSV file in which the extrated data is stored')
  parser.add_argument('--similarity-algorithm', required=True, choices=SIM_ALGORITHMS, help=f'The name of the matching algorithm that should be used, one of {SIM_ALGORITHMS}')
  parser.add_argument('--similarity-threshold', required=True, type=float, action='store', help='The used threshold for similarity')
  parser.add_argument('--input-id-column', action='store', help='The input column for the row identifier')
  parser.add_argument('--input-value-column', action='store', help='The input column for string-normalized joining')
  parser.add_argument('--lookup-id-column', required=True, action='store', help='The lookup column with the unique row identifier')
  parser.add_argument('--lookup-value-column', action='append', help='Values from the lookup file that we use for similarity matching')
  parser.add_argument('--additional-input-column', action='append', help='Additional columns form the input that should be added to the output')
  parser.add_argument('--input-delimiter', action='store', default=',', help='The optional delimiter of the input CSV, default is a comma')
  parser.add_argument('--lookup-delimiter', action='store', default=',', help='The optional delimiter of the lookup CSV, default is a comma')
  parser.add_argument('--value-delimiter', action='store', default=';', help='In case a cell has more than one value, they are separated with this character')
  options = parser.parse_args()

  return options

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  options = parseArguments()
  main(options.input_file, 
    options.lookup_file, 
    options.output_file,
    options.similarity_algorithm, 
    options.similarity_threshold, 
    options.input_id_column, 
    options.input_value_column, 
    options.lookup_id_column, 
    options.lookup_value_column, 
    options.additional_input_column, 
    options.input_delimiter, 
    options.lookup_delimiter, 
    options.value_delimiter)

