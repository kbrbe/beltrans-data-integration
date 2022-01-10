#
# (c) 2021 Sven Lieber
# KBR Brussels
#
from optparse import OptionParser
import pandas as pd
import math
import utils
import csv
from datetime import datetime



# -----------------------------------------------------------------------------
def main():
  """This script performs pre processing before the data can be mapped to RDF, e.g. by adding a given_name and family_name column based on a split on the AFAE column."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing CSV data')
  parser.add_option('-d', '--delimiter', action='store', help='The delimiter of the input file')
  parser.add_option('-o', '--output-file', action='store', help='The file in which content with new headers is stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) or (not options.delimiter) ):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r', encoding="utf-8") as inFile, \
       open(options.output_file, 'w', encoding="utf-8") as outFile:

    inputReader = csv.DictReader(inFile, delimiter=options.delimiter)
    headers = inputReader.fieldnames

    # while cleaning we will add the following additional columns to the output
    headers.extend(['family_name', 'given_name', 'isni_id', 'viaf_id', 'birth_date', 'death_date'])
    outputWriter = csv.DictWriter(outFile, fieldnames=headers, delimiter=options.delimiter)

    outputWriter.writeheader()
    for row in inputReader:
      (familyName, givenName) = utils.extractNameComponents(row['AFAE'])
      row['family_name'] = familyName
      row['given_name'] = givenName

      row['isni_id'] = utils.extractIdentifier(row['AFAE'], row['ISNI'], pattern='ISNI')
      row['viaf_id'] = utils.extractIdentifier(row['AFAE'], row['ISNI'], pattern='VIAF')

      # The following two fields are only available for person data
      datePatterns = ['%Y', '(%Y)', '[%Y]', '%Y-%m-%d', '%d/%m/%Y', '%Y%m%d']
      if 'F046' in row:
        row['birth_date'] = utils.parseDate(row['F046'], datePatterns)

      if 'G046' in row:
        row['death_date'] = utils.parseDate(row['G046'], datePatterns)

      outputWriter.writerow(row)

  print("Finished without errors")

main()
