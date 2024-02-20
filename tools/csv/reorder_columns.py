#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
from tools import utils

# -----------------------------------------------------------------------------
def main():
  """This script orders the columns of the given CSV file based on a config."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing CSV data')
  parser.add_option('-c', '--order-file', action='store', help='A CSV file containing the desired ordering')
  parser.add_option('-o', '--output-file', action='store', help='The file in which the re-ordered data is stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) or (not options.order_file) ):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r', encoding="utf-8") as inFile, \
       open(options.order_file, 'r', encoding="utf-8") as orderFile, \
       open(options.output_file, 'w', encoding="utf-8") as outFile:

    inputReader = csv.DictReader(inFile, delimiter=',')

    orderReader = csv.reader(orderFile, delimiter=',')
    orderedFieldnames = [row[0] for row in orderReader]

    utils.checkIfColumnsExist(inputReader.fieldnames, orderedFieldnames)

    outputWriter = csv.DictWriter(outFile, fieldnames=orderedFieldnames, delimiter=',')
    outputWriter.writeheader()

    for row in inputReader:
      outputRow = {field: row[field] for field in orderedFieldnames}
      outputWriter.writerow(row)


if __name__ == '__main__':
  main()
