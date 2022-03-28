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
  """This script reads a CSV containing book descriptions where at least one 'isbn' column exists. That identifier is read and properly formatted ISBN-10 and ISBN-13 columns are added."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The name of the file with book descriptions in CSV.')
  parser.add_option('-o', '--output-file', action='store', help='The name of the file in which ISBN-10 and ISBN-13 columns are added')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r') as fIn, \
       open(options.output_file, 'w') as fOut:

    inputReader = csv.DictReader(fIn, delimiter=',')
    fieldnames = inputReader.fieldnames.copy()

    fieldnames.append('isbn10')
    fieldnames.append('isbn13')
    outputWriter = csv.DictWriter(fOut, delimiter=',', fieldnames=fieldnames)

    outputWriter.writeheader()

    for row in inputReader:
      row['isbn10'] = ''
      row['isbn13'] = ''
      if 'isbn' in row:
        row['isbn10'] = utils.getNormalizedISBN10(row['isbn'])
        row['isbn13'] = utils.getNormalizedISBN13(row['isbn'])
      outputWriter.writerow(row)

main()
