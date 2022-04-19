#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import utils
from optparse import OptionParser

# -----------------------------------------------------------------------------
def main():
  """This script creates RDF in NT format for a provided list of records and their ISBN10 identifier."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The name of the file with ISBN10 identifiers to be formatted.')
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
    outputWriter = csv.writer(fOut, delimiter=' ')

    # skip header
    next(inputReader)

    biboISBN10 = "http://purl.org/ontology/bibo/isbn10"
    for row in inputReader:
      recordID = row[0]
      isbn10 = row[1]
      fOut.write(f'<{recordID}> <{biboISBN10}> "{isbn10}" .\n')

main()
