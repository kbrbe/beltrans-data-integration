#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import utils
from optparse import OptionParser
from stdnum import isbn

# -----------------------------------------------------------------------------
def main():
  """This script reads a CSV with recordIDs in the first columns and their ISBN13 identifier in the second column. The ISBN13 identifiers will be formatted correctly and the output is a similar CSV."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The name of the file with ISBN identifiers to be formatted.')
  parser.add_option('-o', '--output-file', action='store', help='The name of the file with formatted ISBN numbers')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r') as fIn, \
       open(options.output_file, 'w') as fOut:

    inputReader = csv.reader(fIn, delimiter=',')
    outputWriter = csv.writer(fOut, delimiter=',')

    outputWriter.writerow(next(inputReader))

    for row in inputReader:
      fixedISBN = isbn.format(row[1])
      outputWriter.writerow([row[0], fixedISBN])

main()
