#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from tools import utils
from optparse import OptionParser

# -----------------------------------------------------------------------------
def main():
  """This script reads a CSV file, and extracts the given columns of rows"""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The name of the CSV file from which data should be extracted')
  parser.add_option('-o', '--output-file', action='store', help='The name of the CSV file in which the extrated data is stored')
  parser.add_option('-c', '--column', action='append', help='A column which should be extracted, for several colums use this option several times')
  parser.add_option('--distinct', action='store_true', help='If this flag is set, no double rows with the exact same values will be in the output, in case the input is ordered!')
  parser.add_option('-d', '--delimiter', action='store', default=',', help='The optional delimiter of the input CSV, default is a comma')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if (not options.input_file) and (not options.output_file) and (not options.column):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r') as inFile, \
       open(options.output_file, 'w') as outFile:

    inputReader = csv.DictReader(inFile, delimiter=options.delimiter)

    utils.checkIfColumnsExist(inputReader.fieldnames, options.column)

    outputWriter = csv.DictWriter(outFile, fieldnames=options.column)
    outputWriter.writeheader()

    lastRow = None
    for row in inputReader:
      emptyCol = False
      for colName in options.column:
        if row[colName] == '':
          emptyCol = True
          break
      if not emptyCol:
        outputRow = { key: row[key] for key in options.column }
        if outputRow != lastRow:
          outputWriter.writerow(outputRow)
      lastRow = outputRow

main()
