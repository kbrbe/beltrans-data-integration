#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from tools import utils
from argparse import ArgumentParser

# -----------------------------------------------------------------------------
def main(inputFilenames, outputFilename, columnNames, delimiter):

  # First check if each input file contains the specified column
  #
  for inputFilename in inputFilenames:
    with open(inputFilename, 'r') as inFile:
      inputReader = csv.DictReader(inFile, delimiter=delimiter)
      utils.checkIfColumnsExist(inputReader.fieldnames, columnNames)

  with open(outputFilename, 'w') as outFile:
    outputWriter = csv.DictWriter(outFile, fieldnames=columnNames)
    outputWriter.writeheader()

    for inputFilename in inputFilenames:
      with open(inputFilename, 'r') as inFile:

        inputReader = csv.DictReader(inFile, delimiter=delimiter)

        for row in inputReader:
          outputRow = { key: row[key] for key in columnNames }
          outputWriter.writerow(outputRow)

# -----------------------------------------------------------------------------
def parseArguments():
  parser = ArgumentParser()
  parser.add_argument('input_files', nargs='+', help='The names of CSV files that should be stacked')
  parser.add_argument('-c', '--column-names', required=True, action='append', help='The name of the columns that are taken from the input CSV files')
  parser.add_argument('-o', '--output-file', required=True, action='store', help='The name of the CSV file in which the extrated data is stored')
  parser.add_argument('-d', '--delimiter', action='store', default=',', help='The optional delimiter of the input CSV, default is a comma')
  options = parser.parse_args()

  return options

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  options = parseArguments()
  main(options.input_files, options.output_file, options.column_names, options.delimiter)
