#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import utils
from optparse import OptionParser

# -----------------------------------------------------------------------------
def addLookupRecord(recordID, recordName, lookup):

  if recordName in lookup:
    lookup[recordName].add(recordID)
  else:
    lookup[recordName] = { recordID }

# -----------------------------------------------------------------------------
def duplicateCheck(lookup, warningWriter):

  numberRecords = 0
  numberWarnings = 0
  for l in lookup:
    numberRecords += 1
    if len(lookup[l]) > 1:
      numberWarnings += 1
      identifiers = str(lookup[l])
      warningWriter.writerow([l, ';'.join(lookup[l])])

  print(f'{numberWarnings} warnings in {numberRecords} records')

# -----------------------------------------------------------------------------
def main():
  """This script reads a CSV file with self-created publisher IDs and replaces the names of the self-created publishers based on a given list."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The name of the file with self-created publisher IDs and their names')
  parser.add_option('-o', '--output-file', action='store', help='The name of the file in which the names of the self-created publisher IDs are replaced based on the given list')
  parser.add_option('-l', '--lookup-file', action='store', help='The name of the file with a mapping of names to be replaced and replacement name')
  parser.add_option('', '--delimiter-input', action='store', help='The delimiter of the input file, default ","')
  parser.add_option('', '--delimiter-lookup', action='store', help='The delimiter of the lookup file, default ","')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if ( (not options.input_file) or (not options.output_file) or (not options.lookup_file) ):
    parser.print_help()
    exit(1)

  delimiterInput = options.delimiter_input if options.delimiter_input else ','
  delimiterLookup = options.delimiter_lookup if options.delimiter_lookup else ','

  with open(options.lookup_file, 'r') as fLookup, \
       open(options.input_file, 'r') as fIn, \
       open(options.output_file, 'w') as fOut:

    lookupReader = csv.DictReader(fLookup, delimiter=delimiterLookup)

    replaceNames = {}
    for row in lookupReader:
      replaceNames[row['old-name']] = row['new-name']

    inputReader = csv.DictReader(fIn, delimiter=delimiterInput)
    outputWriter = csv.DictWriter(fOut, fieldnames=inputReader.fieldnames, delimiter=delimiterInput)

    toBeReplaced = set()
    replaced = set()
    numberRecords = 0

    outputWriter.writeheader()

    for row in inputReader:
      manifestationID = row['KBRID']
      contributorID = row['contributorID']
      contributorName = row['contributorName']
      contributorRole = row['contributorRole']
      uncertainty = row['uncertainty']

      newContributorName = contributorName
      contributorNameNorm = utils.getNormalizedString(contributorName)

      if len(contributorID) > 8:
        # it is a self-created identifier
        toBeReplaced.add(contributorID)
        if contributorName in replaceNames:
          newContributorName = replaceNames[contributorName]
          replaced.add(contributorID)

      outputRow = row
      outputRow['contributorName'] = newContributorName
      outputWriter.writerow(outputRow)
      numberRecords += 1

  numberToBeReplaced = len(toBeReplaced)
  numberReplaced = len(replaced)
  print(f'Successfully replaced {numberReplaced} from {numberToBeReplaced} names of self-created identifiers such that the deduplication step identifies them')

main()
