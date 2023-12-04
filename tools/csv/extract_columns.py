#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from tools import utils
from argparse import ArgumentParser
from tools.csv.row_filter import RowFilter

# -----------------------------------------------------------------------------
def main(inputFilenames, outputFilename, columns, delimiter, filterFilename=None, appendData=False):

  # First check if each input file contains the specified columns
  #
  for inputFilename in inputFilenames:
    with open(inputFilename, 'r') as inFile:
      inputReader = csv.DictReader(inFile, delimiter=delimiter)
      utils.checkIfColumnsExist(inputReader.fieldnames, columns)

  if filterFilename:
    with open(filterFilename, 'r') as filterFile:
      filterFileReader = csv.reader(filterFile, delimiter=',')
      filterCriteria = [(row[0], row[1], row[2]) for row in filterFileReader]
    rowFilter = RowFilter(filterCriteria) 

  outputMode = 'a' if appendData else 'w'
  with open(outputFilename, outputMode) as outFile:
    outputWriter = csv.DictWriter(outFile, fieldnames=columns)
    outputWriter.writeheader()

    for inputFilename in inputFilenames:
      with open(inputFilename, 'r') as inFile:

        inputReader = csv.DictReader(inFile, delimiter=delimiter)

        lastRow = None
        for row in inputReader:
          emptyCol = False
          for colName in columns:
            if row[colName] == '':
              emptyCol = True
              break
          if not emptyCol:
            if filterFilename:
              if rowFilter.passFilter(row):
                outputRow = { key: row[key] for key in columns }
                if outputRow != lastRow:
                  outputWriter.writerow(outputRow)
                lastRow = outputRow
            else:
              outputRow = { key: row[key] for key in columns }
              if outputRow != lastRow:
                outputWriter.writerow(outputRow)
              lastRow = outputRow

# -----------------------------------------------------------------------------
def parseArguments():
  parser = ArgumentParser()
  parser.add_argument('input_files', nargs='+', help='The names of CSV files from which data should be extracted')
  parser.add_argument('-o', '--output-file', required=True, action='store', help='The name of the CSV file in which the extrated data is stored')
  parser.add_argument('-c', '--column', required=True, action='append', help='A column which should be extracted, for several colums use this option several times')
  parser.add_argument('-a', '--append', action='store_true', help='Append data to the output file instead of overwriting existing data')
  parser.add_argument('-f', '--filter-file', action='store', help='The optional name of a file with filter criteria based on which data should be extracted')
  parser.add_argument('-d', '--delimiter', action='store', default=',', help='The optional delimiter of the input CSV, default is a comma')
  options = parser.parse_args()

  return options

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  options = parseArguments()
  main(options.input_files, options.output_file, options.column, options.delimiter, filterFilename=options.filter_file, appendData=options.append)
