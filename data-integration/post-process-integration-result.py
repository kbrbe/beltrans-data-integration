#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import utils


# -----------------------------------------------------------------------------
def main():
  """This script filters the SPARQL query result of the integrated data."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing CSV data')
  parser.add_option('-o', '--output-file', action='store', help='The file in which content with new headers is stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  #
  # Open input file with encoding 'utf-8-sig' (instead of 'utf-8') because the Syracuse export contains Byte Order marks (BOM)
  #
  with open(options.input_file, 'r', encoding="utf-8") as inFile, \
       open(options.output_file, 'w', encoding="utf-8") as outFile:

    inputReader = csv.DictReader(inFile, delimiter=',')
    headers = inputReader.fieldnames.copy()

    # In the output we only want a single birth date and a single death date column
    # thus first remove the respective columns from different data sources
    headersToRemove = ['authorBirthDateKBR', 'authorDeathDateKBR', 'authorBirthDateISNI', 'authorDeathDateISNI',
                       'translatorBirthDateKBR', 'translatorDeathDateKBR', 'translatorBirthDateISNI', 'translatorDeathDateISNI',
                       'illustratorBirthDateKBR', 'illustratorDeathDateKBR', 'illustratorBirthDateISNI', 'illustratorDeathDateISNI',
                       'scenaristBirthDateKBR', 'scenaristDeathDateKBR', 'scenaristBirthDateISNI', 'scenaristDeathDateISNI']
    for r in headersToRemove:
      headers.remove(r)

    # and then add the single columns we want
    headers.extend(['authorBirthDate', 'authorDeathDate', 
                   'translatorBirthDate', 'translatorDeathDate',
                   'illustratorBirthDate', 'illustratorDeathDate',
                   'scenaristBirthDate', 'scenaristDeathDate'])

    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)

    outputWriter.writeheader()

    belgian = 'Belgium'

    # used to parse certain columns based on their name, e.g. authorBirthDateKBR and authorBirthDateISNI
    sources = ['KBR', 'ISNI']

    # write relevant data to output
    for row in inputReader:
      if( row['authorNationality'] == belgian or row['illustratorNationality'] == belgian or row['scenaristNationality'] == belgian):

        # This is a relevant row, we process it further before writing it
        utils.selectDate(row, 'author', 'Birth', sources)
        utils.selectDate(row, 'illustrator', 'Birth', sources)
        utils.selectDate(row, 'translator', 'Birth', sources)
        utils.selectDate(row, 'scenarist', 'Birth', sources)

        utils.selectDate(row, 'author', 'Death', sources)
        utils.selectDate(row, 'illustrator', 'Death', sources)
        utils.selectDate(row, 'translator', 'Death', sources)
        utils.selectDate(row, 'scenarist', 'Death', sources)

        outputWriter.writerow(row)



main()
