#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import utils
import utils_date
import json

# -----------------------------------------------------------------------------
def main():
  """This script filters the SPARQL query result fetching initial textual location information."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing CSV data')
  parser.add_option('-o', '--output-file', action='store', help='The file in which the postprocessed data are stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r', encoding="utf-8") as inFile, \
       open(options.output_file, 'w', encoding="utf-8") as outFile:

    inputReader = csv.DictReader(inFile, delimiter=',')
    headers = inputReader.fieldnames.copy()

    # In the output we only want a single column for the following values
    # thus first remove the respective columns from different data sources
    placeHeadersToRemove = ['placeOfPublicationCorrelation', 'placeOfPublicationKBR', 'placeOfPublicationBnF', 'placeOfPublicationKB', 'placeOfPublicationUnesco']
    countryHeadersToRemove = ['countryOfPublicationKBR', 'countryOfPublicationBnF', 'countryOfPublicationKB', 'countryOfPublicationUnesco']


    # and then add the single output columns we want per type
    placeHeaderIndex = headers.index(placeHeadersToRemove[0])
    countryHeaderIndex = headers.index(countryHeadersToRemove[0])
    headers.insert(placeHeaderIndex, 'placeOfPublication')
    headers.insert(countryHeaderIndex, 'countryOfPublication')

    for (p,c) in zip(placeHeadersToRemove, countryHeadersToRemove):
      headers.remove(p)
      headers.remove(c)


    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
    outputWriter.writeheader()

    # used to parse certain columns based on their name, e.g. authorBirthDateKBR and authorBirthDateISNI
    sources = ['Correlation', 'KBR', 'BnF', 'KB', 'Unesco']
    mismatchLog = {}

    # write relevant data to output
    for row in inputReader:

      utils.mergeValues(row, 'placeOfPublication', sources)
      utils.mergeValues(row, 'countryOfPublication', sources)
      outputWriter.writerow(row)


if __name__ == '__main__':
  main()
