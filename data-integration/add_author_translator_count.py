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
def addColumn(row, inputCol, outputCol, trueValue, falseValue, lookup, personDelimiter=';'):
  """
  Checking for each contributor in inputCol (delimited by personDelimiter) if the contributor
  is present in lookup. If yes, trueValue will be put in outputCol, otherwise falseValue.
  If trueValue is a string, it is interpreted as a key for lookup, if it is a boolean value,
  the boolean value will be added.
  >>> row0 = {'authorIdentifiers': 'Lieber, Sven (123)'}
  >>> addColumn(row0, 'authorIdentifiers', 'authorIsAuthorTranslator', True, False, {'Lieber, Sven'})
  >>> row0['authorIsAuthorTranslator']
  True
  >>> addColumn(row0, 'authorIdentifiers', 'authorIsAuthorTranslator', True, False, {'Other', 'Persons'})
  >>> row0['authorIsAuthorTranslator']
  False
  >>> row1 = {'translatorIdentifiers': 'Doe, John (123)'}
  >>> addColumn(row1, 'translatorIdentifiers', 'translatorNationalities', 'nationalities', '', {'Doe, John': ['Germany','Belgium']})
  >>> row1['translatorNationalities']
  'Belgium;Germany'
  >>> addColumn(row1, 'translatorIdentifiers', 'translatorNationalities', 'nationalities', '', {'Doe, John': ['Belgium']})
  >>> row1['translatorNationalities']
  'Belgium'
  """

  contributors = []
  if personDelimiter in row[inputCol]:
    contributors = row[inputCol].split(personDelimiter)
  else:
    contributors = [row[inputCol]]

  for c in contributors:
    contributorName = utils_stats.getContributorName(c)
    if contributorName in lookup:
      if type(trueValue) == bool:
        row[outputCol] = trueValue
      else:
        row[outputCol] = personDelimiter.join(sorted(lookup[contributorName]))
    else:
      row[outputCol] = falseValue

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
    manifestationAuthoredByAT = 'authoredByAuthorTranslator'
    manifestationTranslatedByAT = 'translatedByAuthorTranslator'
    manifestationTranslatorNat = 'translatorNationalities'

    # and then add the single columns we want
    headers.insert(13, manifestationAuthoredByAT)
    headers.insert(14, manifestationTranslatedByAT)
    headers.insert(50, manifestationTranslatorNat)

    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
    outputWriter.writeheader()

    authorTranslators = set()

    translatorNationalities = {}

    for row in contributorsReader:

      #
      # store person contributor's nationality information
      #
      nationalities = []
      if ';' in row['nationalities']:
        nationalities = row['nationalities'].split(';')
      else:
        nationalities = [row['nationalities']]

      translatorNationalities[row['name']] = nationalities

      #
      # store information about the roles of the person contributor
      if int(row['authorIn']) > 0 and int(row['translatorIn']) > 0:
        authorTranslators.add(row['name'])


    personDelimiter=';'

    for row in manifestationsReader:
       
      addColumn(row, manifestationAuthorCol, manifestationAuthoredByAT, True, False, authorTranslators, personDelimiter=';')
      addColumn(row, manifestationTranslatorCol, manifestationTranslatedByAT, True, False, authorTranslators, personDelimiter=';')
      addColumn(row, manifestationTranslatorCol, manifestationTranslatorNat, '', '', translatorNationalities, personDelimiter=';')
      
      outputWriter.writerow(row)
      
     

if __name__ == '__main__':
  main()
