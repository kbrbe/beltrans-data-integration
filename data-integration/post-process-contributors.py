#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import utils
import json

# -----------------------------------------------------------------------------
def main():
  """This script filters the SPARQL query result fetching contributor information of translations."""

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

  with open(options.input_file, 'r', encoding="utf-8") as inFile, \
       open(options.output_file, 'w', encoding="utf-8") as outFile:

    inputReader = csv.DictReader(inFile, delimiter=',')
    headers = inputReader.fieldnames.copy()

    # In the output we only want a single birth date and a single death date column
    # thus first remove the respective columns from different data sources
    headersToRemove = ['birthDateKBR', 'deathDateKBR', 'birthDateBnF', 'deathDateBnF', 'birthDateNTA', 'deathDateNTA', 'birthDateISNI', 'deathDateISNI']

    for r in headersToRemove:
      headers.remove(r)

    # and then add the single columns we want
    headers.insert(3, 'birthDate')
    headers.insert(4, 'deathDate')
    #headers.extend(['birthDate', 'deathDate'])

    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
    outputWriter.writeheader()

    # used to parse certain columns based on their name, e.g. authorBirthDateKBR and authorBirthDateISNI
    sources = ['KBR', 'BnF', 'NTA', 'ISNI']
    mismatchLog = {}

    # write relevant data to output
    for row in inputReader:

      # This is a relevant row, we process it further before writing it
      utils.selectDate(row, 'birthDate', sources, 'contributorID', mismatchLog)
      utils.selectDate(row, 'deathDate', sources, 'contributorID', mismatchLog)

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
      

main()
