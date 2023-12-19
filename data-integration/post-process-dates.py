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
  """This script filters the SPARQL query result fetching initial textual date information."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing CSV data')
  parser.add_option('-d', '--date-column', action='store', help='The column prefix name of the column that contain dates to combine, e.g. dateOfPublication will look for dateOfPublicationKBR, dateOfPublicationBnF, ...')
  parser.add_option('--id-column', action='store', help='The name of the column with row identifiers')
  parser.add_option('-o', '--output-file', action='store', help='The file in which the postprocessed data are stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) or (not options.date_column) or (not options.id_column) ):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r', encoding="utf-8") as inFile, \
       open(options.output_file, 'w', encoding="utf-8") as outFile:

    inputReader = csv.DictReader(inFile, delimiter=',')
    headers = inputReader.fieldnames.copy()
    outputHeaders = [options.id_column, options.date_column]

    # used to parse certain columns based on their name, e.g. authorBirthDateKBR and authorBirthDateISNI
    sources = ['KBR', 'BnF', 'KB', 'Unesco']
    inputDateColumns = [f'{options.date_column}{s}' for s in sources]
    utils.checkIfColumnsExist(headers, [options.id_column] + inputDateColumns)

    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=outputHeaders)
    outputWriter.writeheader()

    mismatchLog = {}
    # write relevant data to output
    for row in inputReader:

      outputRow = {f'{options.date_column}{s}': row[f'{options.date_column}{s}'] for s in sources}
      outputRow[options.id_column] = row[options.id_column]
      utils_date.selectDate(outputRow, options.date_column, sources, options.id_column, mismatchLog, options.date_column)
      outputWriter.writerow(outputRow)


if __name__ == '__main__':
  main()
