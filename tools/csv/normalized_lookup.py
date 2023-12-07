#
# (c) 2023 Sven Lieber
# KBR Brussels
#
import csv
from tools import utils
from tools.string import utils_string
from argparse import ArgumentParser


def main(inputFilename, lookupFilename, outputFilename, lookupKeyColumn, lookupValueColumn, inputKeyColumn, inputIDColumn, outputValueColumn, inputDelimiter, lookupDelimiter):

  with open(inputFilename, 'r') as inFile:
    inputReader = csv.DictReader(inFile, delimiter=inputDelimiter)
    utils.checkIfColumnsExist(inputReader.fieldnames, [inputKeyColumn])

  with open(lookupFilename, 'r') as lookupFile:
    inputReader = csv.DictReader(lookupFile, delimiter=lookupDelimiter)
    utils.checkIfColumnsExist(inputReader.fieldnames, [lookupKeyColumn, lookupValueColumn])

    lookup = {}
    # build the lookup data structure
    #
    for row in inputReader:
      lookupKey = row[lookupKeyColumn]
      lookupValue = row[lookupValueColumn]

      normKey = utils_string.getNormalizedString(lookupKey)
      if lookupKey in lookup:
        lookup[normKey].append(lookupValue)
      else:
        lookup[normKey] = [lookupValue]

  with open(inputFilename, 'r') as inFile, \
       open(outputFilename, 'w') as outFile:

    inputReader = csv.DictReader(inFile, delimiter=inputDelimiter)
    outputWriter = csv.DictWriter(outFile, fieldnames=[inputIDColumn, outputValueColumn], delimiter=inputDelimiter)
    outputWriter.writeheader()

    for row in inputReader:
      inputLookupKey = row[inputKeyColumn]
      rowID = row[inputIDColumn]
      normInputLookupKey = utils_string.getNormalizedString(inputLookupKey)

      if normInputLookupKey in lookup:
        foundValue = lookup[normInputLookupKey] 
        outputWriter.writerow({inputIDColumn: rowID, outputValueColumn: ';'.join(foundValue)})
      else:
        print(f'No matching value found for {inputLookupKey} (normalized: "{normInputLookupKey}")')


# -----------------------------------------------------------------------------
def parseArguments():
  parser = ArgumentParser()
  parser.add_argument('--input-file', required=True, action='store', help='The name of the CSV file from which data should be looked up')
  parser.add_argument('--lookup-file', required=True, action='store', help='The name of the CSV file in which data should be looked up')
  parser.add_argument('--output-file', required=True, action='store', help='The name of the CSV file in which in which the extrated data is stored')
  parser.add_argument('--lookup-key-column', required=True, action='store', help='The lookup column for string-normalized joining')
  parser.add_argument('--lookup-value-column', action='store', help='The value we want to retrieve from the lookup')
  parser.add_argument('--input-key-column', action='store', help='The input column for string-normalized joining')
  parser.add_argument('--input-id-column', action='store', help='The input column for the row identifier')
  parser.add_argument('--output-value-column', action='store', help='The output column for the looked up value')
  parser.add_argument('--input-delimiter', action='store', default=',', help='The optional delimiter of the input CSV, default is a comma')
  parser.add_argument('--lookup-delimiter', action='store', default=',', help='The optional delimiter of the lookup CSV, default is a comma')
  options = parser.parse_args()

  return options

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  options = parseArguments()
  main(options.input_file, options.lookup_file, options.output_file, options.lookup_key_column, options.lookup_value_column, options.input_key_column, options.input_id_column, options.outputValueColumn, options.input_delimiter, options.lookup_delimiter)

