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

    outputWriter = csv.writer(fOut, delimiter=' ', quotechar=' ')

    for row in inputReader:
      isbn10 = ''
      isbn13 = ''
      if row['isbn10'] == '' and row['isbn13'] == '':
        # both are empty, nothing we can do
        pass
      elif row['isbn10'] != '' and row['isbn13'] != '':
        # both have a value, it might not be formatted
        isbn10 = utils.getNormalizedISBN10(row['isbn10'])
        isbn13 = utils.getNormalizedISBN13(row['isbn13'])
      elif row['isbn10'] == '' and row['isbn13'] != '': 
        # compute ISBN identifiers based on given ISBN13
        isbn10 = utils.getNormalizedISBN10(row['isbn13'])
        isbn13 = utils.getNormalizedISBN13(row['isbn13'])
      elif row['isbn10'] != '' and row['isbn13'] == '':
        # compute ISBN identifiers based on given ISBN10
        isbn10 = utils.getNormalizedISBN10(row['isbn10'])
        isbn13 = utils.getNormalizedISBN13(row['isbn10'])

      subject = f'<{row["manifestation"]}>'
      if isbn10 != '':
        predicate = f'<http://purl.org/ontology/bibo/isbn10>'
        objectValue = f'"{isbn10}" .'
        outputWriter.writerow([subject, predicate, objectValue])

      if isbn13 != '':
        predicate = f'<http://purl.org/ontology/bibo/isbn13>'
        objectValue = f'"{isbn13}" .'
        outputWriter.writerow([subject, predicate, objectValue])

main()
