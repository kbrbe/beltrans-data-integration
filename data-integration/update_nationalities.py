#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import utils_stats
import utils_date
import pandas as pd
import json

# -----------------------------------------------------------------------------
def updateNationalities(row, inputCol, nationalitiesColumn, lookup, personDelimiter=';'):
  """
  Checking for each contributor in inputCol (delimited by personDelimiter) if the contributor
  is present in lookup. If yes, update the existing list of nationalities in nationalitiesColumn
  based on the values in lookup.

  Adding a nationality but do not create a duplicate
  >>> row0 = {'authorIdentifiers': 'Doe, John (123)', 'authorNationalities': 'Belgium;Netherlands'}
  >>> updateNationalities(row0, 'authorIdentifiers', 'authorNationalities', {'Doe, John': {'Belgium'}})
  >>> row0['authorNationalities']
  'Belgium;Netherlands'

  Adding a nationality if it didn't exist before
  >>> row0 = {'authorIdentifiers': 'Doe, John (123)', 'authorNationalities': 'Belgium;Netherlands'}
  >>> updateNationalities(row0, 'authorIdentifiers', 'authorNationalities', {'Doe, John': {'France'}})
  >>> row0['authorNationalities']
  'Belgium;France;Netherlands'
  """

  contributors = []
  if personDelimiter in row[inputCol]:
    contributors = row[inputCol].split(personDelimiter)
  else:
    contributors = [row[inputCol]]

  currentNationalitiesString = row[nationalitiesColumn]
  currentNationalities = set()
  if ';' in currentNationalitiesString:
    currentNationalities = set(currentNationalitiesString.split(';'))
  else:
    currentNationalities = set([currentNationalitiesString])

  for c in contributors:
    contributorName = utils_stats.getContributorName(c)
    if contributorName in lookup:
      currentNationalities.update(lookup[contributorName])
      newNationalitiesString = ';'.join(sorted(currentNationalities))
      row[nationalitiesColumn] = newNationalitiesString

# -----------------------------------------------------------------------------
def main():
  """This script checks for each translation of a translation sheet if the author and/or translator is someone who authored at least one book AND translated at least one book."""

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
    manifestationsReader = csv.DictReader(inFileManifestations, delimiter=',')
    headers = manifestationsReader.fieldnames.copy()

    manifestationAuthorCol = 'authorIdentifiers'
    manifestationTranslatorCol = 'translatorIdentifiers'
    manifestationAuthorNatCol = 'authorNationalities'
    manifestationTranslatorNatCol = 'translatorNationalities'

    # and then add the single columns we want
    headers.insert(13, manifestationAuthoredByAT)
    headers.insert(14, manifestationTranslatedByAT)
    headers.insert(50, manifestationTranslatorNat)

    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
    outputWriter.writeheader()

    personNationalities = {}

    for row in contributorsReader:

      #
      # store person contributor's nationality information
      #
      nationalities = []
      if ';' in row['nationalities']:
        nationalities = row['nationalities'].split(';')
      else:
        nationalities = [row['nationalities']]

      personNationalities[row['name']] = nationalities


    personDelimiter=';'

    for row in manifestationsReader:
       
      updateNationalities(row, manifestationAuthorCol, manifestationAuthorNatCol, personNationalities, personDelimiter=';')
      updateNationalities(row, manifestationTranslatorCol, manifestationTranslatorNatCol, personNationalities, personDelimiter=';')

      outputWriter.writerow(row)
      
     

if __name__ == '__main__':
  main()
