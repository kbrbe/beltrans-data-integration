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
  """This script extracts manifestation IDs and assigned publication countries."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing CSV data')
  parser.add_option('-o', '--output-file', action='store', help='The file in which extracted values are stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file)):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r', encoding="utf-8") as inFile, \
       open(options.output_file, 'w', encoding="utf-8") as outFile:

    inputReader = csv.DictReader(inFile, delimiter=',')

    outputHeaders = ['KBRID', 'pubCountryURI']
    outputWriter = csv.DictWriter(outFile, fieldnames=outputHeaders, delimiter=',')

    outputWriter.writeheader()

    for row in inputReader:

      bbURIsString = row['countryOfPublication']

      # check if there is a value in this column
      if len(bbURIsString) > 0:
        bbURIs = bbURIsString.split(';')
        # check if there were multiple splitted values
        if len(bbURIs) > 0:
          for uri in bbURIs:
            # check if the splitted value is not just empty
            if len(uri) > 0:
              outputRow = {}
              outputRow['KBRID'] = row['KBRID']
              outputRow['pubCountryURI'] = uri
              outputWriter.writerow(outputRow)

  print("Finished without errors")

main()
