#
# (c) 2023 Sven Lieber
# KBR Brussels
#

import csv
import argparse
from tools import utils
from tools.string import utils_string

# -----------------------------------------------------------------------------
def main(inputFilename, outputFilename, idColumnName, valueSeparator, columnNames, delimiter):
  """This script performs two things: 
       1. the specified input columns are normalized according to normalization rules
       2. the normalized values are concatenated to a single descriptiveKey column with the provided valueSeparator.
  """

  with open(inputFilename, 'r') as inFile, \
       open(outputFilename, 'w') as outFile:

    inputReader = csv.DictReader(inFile, delimiter=delimiter)
    utils.checkIfColumnsExist(inputReader.fieldnames, [idColumnName] + columnNames)

    outputWriter = csv.DictWriter(outFile, fieldnames=['elementID', 'descriptiveKey'])
    outputWriter.writeheader()

    for row in inputReader:
      elementID = row[idColumnName]
      keyElements = []
      for col in columnNames:
        value = row[col]
        if value != '':
          # do not treat ISBN identifiers like text, do not apply normalization rules
          valueNormalized = utils_string.getNormalizedString(value) if not col.startswith('ISBN') or not col.startswith('isbn') else value
          keyElements.append(valueNormalized) 
        else:
          print(f'This should not happen, empty value for column "{col}" in row "{elementID}"')

      outputWriter.writerow({'elementID': elementID, 'descriptiveKey': valueSeparator.join(keyElements)})

    print("finished")


# -----------------------------------------------------------------------------
def parseArguments():

  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input-file', action='store', required=True, help="The CSV file with an identifier of an element and one or more other columns that can be used to create descriptive keys")
  parser.add_argument('-o', '--output-file', action='store', required=True, help='The name of the output CSV file containing two columns: elementID and descriptiveKey')
  parser.add_argument('--id-column', action='store', required=True, help='The name of the column that is used as element identifier')
  parser.add_argument('--value-separator', action='store', default='/', help='The character used to separate parts of the descriptive key, default is a slash "/"')
  parser.add_argument('--column', action='append', required=True, help="The name of an input column, there can be more that will be normalized and concatenated using value-separator")
  parser.add_argument('--delimiter', action='store', default=',', help="Optional delimiter of the input/output CSV, default is ','")
  options = parser.parse_args()

  return options

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  (options) = parseArguments()
  main(options.input_file, options.output_file, options.id_column, options.value_separator, options.column, options.delimiter)
 
