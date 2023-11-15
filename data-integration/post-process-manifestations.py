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
  parser.add_option('-c', '--contributions-file', action='store', help='A CSV file containing a mapping between manifestations and contributors')
  parser.add_option('-o', '--output-file', action='store', help='The file in which the postprocessed data are stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) or (not options.contributions_file) ):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r', encoding="utf-8") as inFile, \
       open(options.contributions_file, 'r', encoding="utf-8") as contFile, \
       open(options.output_file, 'w', encoding="utf-8") as outFile:

    contReader = csv.DictReader(contFile, delimiter=',')

    # Create a lookup data structure for contributions
    contributions = {}
    for row in contReader:
      manifestationID = row['manifestationID']
      role = row['contributorRole']
      contributorNameID = row['contributorNameID']

      if manifestationID in contributions:
        if role in contributions[manifestationID]:
          contributions[manifestationID][role].append(contributorNameID)
        else:
          contributions[manifestationID][role] = [contributorNameID]
      else:
        contributions[manifestationID] = {}
        contributions[manifestationID][role] = [contributorNameID]

    inputReader = csv.DictReader(inFile, delimiter=',')
    headers = inputReader.fieldnames.copy()

    # In the output we only want a single publication year column
    # thus first remove the respective columns from different data sources
    yearHeadersToRemove = ['targetYearOfPublicationKBR', 'targetYearOfPublicationBnF', 'targetYearOfPublicationKB', 'targetYearOfPublicationUnesco']

    # and then add the single output columns we want per type
    yearHeaderIndex = headers.index(yearHeadersToRemove[0])
    headers.insert(yearHeaderIndex, 'targetYearOfPublication')

    # add new columns for contributors after the targetCollectionIdentifier column
    contributionsIndex = headers.index('targetCollectionIdentifier') + 1
    headers.insert(contributionsIndex, 'targetPublisherIdentifiers')
    headers.insert(contributionsIndex, 'publishingDirectorIdentifiers')
    headers.insert(contributionsIndex, 'scenaristIdentifiers')
    headers.insert(contributionsIndex, 'illustratorIdentifiers')
    headers.insert(contributionsIndex, 'translatorIdentifiers')
    headers.insert(contributionsIndex, 'authorIdentifiers')
    headers.insert(contributionsIndex, 'author/scenarist')

    roleMapping = {
      'http://schema.org/author': 'authorIdentifiers',
      'http://schema.org/translator': 'translatorIdentifiers',
      'http://schema.org/publisher': 'targetPublisherIdentifiers',
      'http://id.loc.gov/vocabulary/relators/ill': 'illustratorIdentifiers',
      'http://id.loc.gov/vocabulary/relators/sce': 'scenaristIdentifiers',
      'http://id.loc.gov/vocabulary/relators/pbd': 'publishingDirectorIdentifiers'
    }

    for h in yearHeadersToRemove:
      headers.remove(h)


    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
    outputWriter.writeheader()

    # used to parse certain columns based on their name, e.g. authorBirthDateKBR and authorBirthDateISNI
    sources = ['KBR', 'BnF', 'KB', 'Unesco']
    mismatchLog = {}

    # write relevant data to output
    for row in inputReader:

      utils_date.selectDate(row, 'targetYearOfPublication', sources, 'targetIdentifier', mismatchLog, 'publicationYear')
      utils.addContributions(row, contributions[row['targetIdentifier']], roleMapping)

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
