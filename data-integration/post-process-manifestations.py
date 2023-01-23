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
  """This script filters the SPARQL query result fetching manifestation information."""

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

    # In the output we only want a single publication year column
    # thus first remove the respective columns from different data sources
    yearHeadersToRemove = ['targetYearOfPublicationKBR', 'targetYearOfPublicationBnF', 'targetYearOfPublicationKB', 'targetYearOfPublicationUnesco']
    placeHeadersToRemove = ['targetPlaceOfPublicationKBR', 'targetPlaceOfPublicationBnF', 'targetPlaceOfPublicationKB', 'targetPlaceOfPublicationUnesco']
    countryHeadersToRemove = ['targetCountryOfPublicationKBR', 'targetCountryOfPublicationBnF', 'targetCountryOfPublicationKB', 'targetCountryOfPublicationUnesco']


    # and then add the single output columns we want per type
    yearHeaderIndex = headers.index(yearHeadersToRemove[0])
    placeHeaderIndex = headers.index(placeHeadersToRemove[0])
    countryHeaderIndex = headers.index(countryHeadersToRemove[0])
    headers.insert(yearHeaderIndex, 'targetYearOfPublication')
    headers.insert(placeHeaderIndex, 'targetPlaceOfPublication')
    headers.insert(countryHeaderIndex, 'targetCountryOfPublication')

    for (y,p,c) in zip(yearHeadersToRemove, placeHeadersToRemove, countryHeadersToRemove):
      headers.remove(y)
      headers.remove(p)
      headers.remove(c)


    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
    outputWriter.writeheader()

    # used to parse certain columns based on their name, e.g. authorBirthDateKBR and authorBirthDateISNI
    sources = ['KBR', 'BnF', 'KB', 'Unesco']
    mismatchLog = {}

    # write relevant data to output
    for row in inputReader:

      utils_date.selectDate(row, 'targetYearOfPublication', sources, 'targetIdentifier', mismatchLog, 'publicationYear')
      utils.mergeValues(row, 'targetPlaceOfPublication', sources)
      utils.mergeValues(row, 'targetCountryOfPublication', sources)

      outputWriter.writerow(row)

  # print statistics
  for dateType in mismatchLog:
    for contributorType in mismatchLog[dateType]:
      numberMismatches = len(mismatchLog[dateType][contributorType])
      print(f'{dateType}, {contributorType} = {numberMismatches} mismatches')

  # print mismatch log
  print(f'dateType, contributorType, contributor, KBR, ISNI')
  for dateType in mismatchLog:
    for contributorType in mismatchLog[dateType]:
      for c in mismatchLog[dateType][contributorType]:
        d = mismatchLog[dateType][contributorType][c]
        kbrValue = next(iter(d['KBR'])) if 'KBR' in d else ''
        bnfValue = next(iter(d['BnF'])) if 'BnF' in d else ''
        ntaValue = next(iter(d['NTA'])) if 'NTA' in d else ''
        isniValue = next(iter(d['ISNI'])) if 'ISNI' in d else ''
        print(f'{dateType}, {contributorType}, {c}, {kbrValue}, {bnfValue}, {ntaValue}, {isniValue}')
      

if __name__ == '__main__':
  main()
