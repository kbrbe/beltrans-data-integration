#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import utils
from optparse import OptionParser

import utils_string


# -----------------------------------------------------------------------------
def checkArguments():
  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input', action='store', help='Input CSV file')
  parser.add_option('-o', '--output', action='store', help='Second CSV file')
  parser.add_option('--id-column', action='store', help='The column containing the row identifier')
  parser.add_option('--column', action='store',
                    help='column name of the CSV in which it is checked for missing contributor overlap')
  parser.add_option('--csv-delimiter', action='store', default=',', help='Delimiter of the input CSV, default is a comma')
  parser.add_option('--column-value-delimiter', action='store', default=';', help='Delimiter used within a column to separate different names we want to compare')

  (options, args) = parser.parse_args()

  if (not options.input) or (not options.output) or (not options.column) or (not options.id_column):
    print(f'Input and output data as well as a column name are needed')
    parser.print_help()
    exit(1)

  return options, args

# -----------------------------------------------------------------------------
def addIdentifier(identifier, identifierList):
  if identifier in identifierList:
    print(f'Warning, identifier {identifier} was already found, column values are not unique!')
  else:
    identifierList.add(identifier)
    
# -----------------------------------------------------------------------------
def main(inputFile, outputFile, idColumn, columnName, csvDelimiter, columnValueDelimiter):
  """This script reads a CSV files and checks if values in a given column occur more than once in the column."""

  with open(inputFile, 'r') as inFile, \
       open(outputFile, 'w') as outFile:

    inputReader = csv.DictReader(inFile, delimiter=csvDelimiter)
    outputWriter = csv.DictWriter(outFile, fieldnames=[idColumn, columnName], delimiter=csvDelimiter)

    identifiers = set()
    numberRows = 0
    numberFound = 0
    outputWriter.writeheader()
    for row in inputReader:
      columnValue = row[columnName]
      values = columnValue.split(columnValueDelimiter)

      if len(values) > 1:
        valueNameParts = []
        for value in values:
          valueNamePart = value.split('(')[0]
          valueNameParts.append(valueNamePart)
        if utils_string.overlappingValues(valueNameParts):
          numberFound += 1
          outputWriter.writerow({idColumn: row[idColumn], columnName: row[columnName]})
      numberRows += 1

    print(f'{numberFound}/{numberRows} contain possible contributor duplicates.')

if __name__ == '__main__':
  (options, args) = checkArguments()
  main(options.input, options.output, options.id_column, options.column, options.csv_delimiter, options.column_value_delimiter)

