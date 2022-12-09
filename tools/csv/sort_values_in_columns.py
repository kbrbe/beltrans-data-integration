#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from tools import utils
from optparse import OptionParser

# -----------------------------------------------------------------------------
def main():
  """This script reads a CSV file, and sorts the values within specified columns based on a delimiter
     For example the value of row 2 and column 3 "World;Hello" with delimiter ';' will be "Hello;World"."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The name of the CSV file from which data should be extracted')
  parser.add_option('-o', '--output-file', action='store', help='The name of the CSV file in which the extrated data is stored')
  parser.add_option('-c', '--column', action='append', help='A column which should be extracted, for several colums use this option several times')
  parser.add_option('--csv-delimiter', action='store', default=',', help='The optional delimiter of the input CSV, default is a comma')
  parser.add_option('--content-delimiter', action='store', default=';', help='The optional delimiter of values within a row/column, default is a semicolon')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if (not options.input_file) and (not options.output_file) and (not options.column):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r') as inFile, \
       open(options.output_file, 'w') as outFile:

    inputReader = csv.DictReader(inFile, delimiter=options.csv_delimiter)

    # check if the columns we want to sort actually exist in the input
    utils.checkIfColumnsExist(inputReader.fieldnames, options.column)

    # create a CSV writer for all columns of the input
    outputWriter = csv.DictWriter(outFile, fieldnames=inputReader.fieldnames)
    outputWriter.writeheader()

    for row in inputReader:

      # only sort specified columns and change corresponding row[colName] to sorted value
      for colName in options.column:
        values = row[colName].split(options.content_delimiter)
        sortedValues = sorted(values)
        row[colName] = options.content_delimiter.join(sortedValues)

      # write the whole input row to the output (containing also certain sorted columns)
      outputWriter.writerow(row)

main()
