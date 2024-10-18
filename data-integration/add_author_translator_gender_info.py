#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import utils

# -----------------------------------------------------------------------------
def main():
  """This script checks for each translation of a translation sheet if at least one of the authors or translators is female and adds this information to two respective columns."""

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
    manifestationAuthorFemale = 'femaleAuthor'
    manifestationTranslatorFemale = 'femaleTranslator'

    # and then add the single columns we want
    headers.insert(13, manifestationAuthorFemale)
    headers.insert(14, manifestationTranslatorFemale)

    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
    outputWriter.writeheader()

    femaleAuthors = set()
    femaleTranslators = set()

    contributorsGender = {}
    for row in contributorsReader:
      contributorsGender[row['contributorID']] = row['gender']

    personDelimiter=';'

    for row in manifestationsReader:
       
      utils.addGenderInfoColumn(row, manifestationAuthorCol, manifestationAuthorFemale, contributorsGender, personDelimiter=personDelimiter)
      utils.addGenderInfoColumn(row, manifestationTranslatorCol, manifestationTranslatorFemale, contributorsGender, personDelimiter=personDelimiter)

      outputWriter.writerow(row)


if __name__ == '__main__':
  main()
