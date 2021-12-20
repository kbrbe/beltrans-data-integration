#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser



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
    headers = inputReader.fieldnames
    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)

    outputWriter.writeheader()

    belgian = 'Belgium'

    # write relevant data to output
    for row in inputReader:
      if( row['authorNationality'] == belgian or row['illustratorNationality'] == belgian or row['scenaristNationality'] == belgian):
        outputWriter.writerow(row)
      #if( row['authorNationality'] == belgian or row['illustratorNationality'] == belgian or row['scenaristNationality'] == belgian
      #    or row['authorNationality'] == '' or row['illustratorNationality'] == '' or row['scenaristNationality'] == ''):
      #  outputWriter.writerow(row)


main()
