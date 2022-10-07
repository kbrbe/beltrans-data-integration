#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import utils_string
import utils


# -----------------------------------------------------------------------------
def checkArguments():
  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input', action='store', help='Input CSV file')
  parser.add_option('-o', '--output', action='store', help='Second CSV file')
  parser.add_option('--output-column', action='append', help='The name of a column which should be included in the output')
  parser.add_option('--column', action='store',
                    help='column name of the CSV in which it is checked for missing contributor overlap')
  parser.add_option('--csv-delimiter', action='store', default=',', help='Delimiter of the input CSV, default is a comma')
  parser.add_option('--column-value-delimiter', action='store', default=';', help='Delimiter used within a column to separate different names we want to compare')

  (options, args) = parser.parse_args()

  if (not options.input) or (not options.output) or (not options.column) or (not options.output_column):
    print(f'Input and output data as well as a column name are needed')
    parser.print_help()
    exit(1)

  return options, args
   
# -----------------------------------------------------------------------------
def main(inputFile, outputFile, outputColumns, columnName, csvDelimiter, columnValueDelimiter):
  """This script reads a CSV files and checks if parts of the value in a given column occur more than once in the column.
     For example "Sven Lieber (abc, def); Lieber, Sven (abc)" where the first name but also the last name occur twice."""

  with open(inputFile, 'r') as inFile, \
       open(outputFile, 'w') as outFile:

    inputReader = csv.DictReader(inFile, delimiter=csvDelimiter)

    utils.checkIfColumnsExist(inputReader.fieldnames, outputColumns + [columnName])

    # not using list(wantedColumns) as fieldnames because we want to determine the order
    outputWriter = csv.DictWriter(outFile, fieldnames=outputColumns + [columnName], delimiter=csvDelimiter)

    identifiers = set()
    numberRows = 0
    numberFound = 0
    outputWriter.writeheader()
    for row in inputReader:
      columnValue = row[columnName]
      # we may have "name1 (id1, idn) ; name2 (id2, idn)" and split in this example by ';' to treat each name-ids combination seperately
      values = columnValue.split(columnValueDelimiter)

      if len(values) > 1:
        valueNameParts = []
        for value in values:
          # the input format is "name (id1, idn)", and we want the name
          valueNamePart = value.split('(')[0]
          valueNameParts.append(valueNamePart)
        if utils_string.overlappingValues(valueNameParts):
          numberFound += 1
          # adding all wanted columns to the output
          outputRow = {key: row[key] for key in wantedColumns}
          outputWriter.writerow(outputRow)
      numberRows += 1

    print(f'{numberFound}/{numberRows} contain possible contributor duplicates.')

if __name__ == '__main__':
  (options, args) = checkArguments()
  main(options.input, options.output, options.output_column, options.column, options.csv_delimiter, options.column_value_delimiter)

