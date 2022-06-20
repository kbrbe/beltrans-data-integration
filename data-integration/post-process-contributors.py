#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import utils
import pandas as pd
import json

# -----------------------------------------------------------------------------
def main():
  """This script filters the SPARQL query result fetching contributor information of translations."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-c', '--input-contributors', action='store', help='The input file containing CSV data with one contributor per line')
  parser.add_option('-m', '--input-manifestations', action='store', help='The input file containing CSV data with one manifestation per line')
  parser.add_option('-o', '--output-file', action='store', help='The file in which content with new headers is stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_contributors) or (not options.input_manifestations) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  with open(options.input_contributors, 'r', encoding="utf-8") as inFileContributors, \
       open(options.input_manifestations, 'r', encoding="utf-8") as inFileManifestations, \
       open(options.output_file, 'w', encoding="utf-8") as outFile:

    contributorsReader = csv.DictReader(inFileContributors, delimiter=',')
    headers = contributorsReader.fieldnames.copy()

    # In the output we only want a single birth date and a single death date column
    # thus first remove the respective columns from different data sources
    headersToRemove = ['birthDateKBR', 'deathDateKBR', 'birthDateBnF', 'deathDateBnF', 'birthDateNTA', 'deathDateNTA', 'birthDateISNI', 'deathDateISNI']

    for r in headersToRemove:
      headers.remove(r)

    # and then add the single columns we want
    headers.insert(3, 'birthDate')
    headers.insert(4, 'deathDate')

    # similarly, add columns for statistics we will add
    headers.insert(5, 'authorIn')
    headers.insert(6, 'translatorIn')
    headers.insert(7, 'illustratorIn')
    headers.insert(8, 'scenaristIn')
    headers.insert(9, 'publishingDirectorIn')

    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
    outputWriter.writeheader()

    # used to parse certain columns based on their name, e.g. authorBirthDateKBR and authorBirthDateISNI
    sources = ['KBR', 'BnF', 'NTA', 'ISNI']
    mismatchLog = {}

    contributions = {'authors': {}, 'translators': {}, 'illustrators': {}, 'scenarists': {}, 'publishingDirectors': {}}
    manifestationsReader = csv.DictReader(inFileManifestations, delimiter=',')
    for row in manifestationsReader:
      utils.countContribution(row['authorIdentifiers'], contributions['authors'])
      utils.countContribution(row['translatorIdentifiers'], contributions['translators'])
      utils.countContribution(row['illustratorIdentifiers'], contributions['illustrators'])
      utils.countContribution(row['scenaristIdentifiers'], contributions['scenarists'])
      utils.countContribution(row['publishingDirectorIdentifiers'], contributions['publishingDirectors'])

    # write relevant data to output
    for row in contributorsReader:
      rowID = row['contributorID']
      contributorName = row['name']

      # add a single column for birth date respectively death date
      utils.selectDate(row, 'birthDate', sources, 'contributorID', mismatchLog, 'date')
      utils.selectDate(row, 'deathDate', sources, 'contributorID', mismatchLog, 'date')

      if contributorName != '':
        contributorName = contributorName.strip()
        # add statistics about how many manifestations the contributor contributed to
        # manifestation data is looked up using the provided manifestations file residing in a Pandas dataframe
        numberAuthored = contributions['authors'][contributorName] if contributorName in contributions['authors'] else 0
        numberTranslated = contributions['translators'][contributorName] if contributorName in contributions['translators'] else 0
        numberIllustrated = contributions['illustrators'][contributorName] if contributorName in contributions['illustrators'] else 0
        numberScened = contributions['scenarists'][contributorName] if contributorName in contributions['scenarists'] else 0
        numberDirected = contributions['publishingDirectors'][contributorName] if contributorName in contributions['publishingDirectors'] else 0

        row['authorIn'] = numberAuthored
        row['translatorIn'] = numberTranslated
        row['illustratorIn'] = numberIllustrated
        row['scenaristIn'] = numberScened
        row['publishingDirectorIn'] = numberDirected
      else:
        row['authorIn'] = 0
        row['translatorIn'] = 0
        row['illustratorIn'] = 0
        row['scenaristIn'] = 0
        row['publishingDirectorIn'] = 0

      if row['authorIn'] > 0 or row['translatorIn'] > 0\
              or row['illustratorin'] > 0 or row['scenaristIn'] > 0\
              or row['publishingDirectorIn'] > 0:
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
