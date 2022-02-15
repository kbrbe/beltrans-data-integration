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
  """This script reads a CSV file with self-created publisher IDs and looks up the name of the publisher in a separate CSV to identify the "real" identifier."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The name of the file with self-created publisher IDs')
  parser.add_option('-o', '--output-file', action='store', help='The name of the file in which the self-created publisher IDs are replaced with found "real" IDs')
  parser.add_option('-l', '--lookup-file', action='store', help='The name of the file in which the actual IDs are stroed')
  parser.add_option('', '--warning-log', action='store', help='A log where publishers in the lookup file with several IDs are listed')
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

    nolangNames = dict()
    dutchNames = dict()
    frenchNames = dict()

    for row in lookupReader:
      authorityID = row['KBRID']
      nolangName = utils.getNormalizedString(row['name-without-lang'])
      dutchName = utils.getNormalizedString(row['name-dutch'])
      frenchName = utils.getNormalizedString(row['name-french'])

      addLookupRecord(authorityID, nolangName, nolangNames)
      addLookupRecord(authorityID, dutchName, dutchNames)
      addLookupRecord(authorityID, frenchName, frenchNames)

    #warningWriter = csv.writer(warningOut, delimiter=delimiterInput)
    #warningWriter.writerow(['name', 'identifiers'])
    #duplicateCheck(nolangNames, warningWriter)
    #duplicateCheck(dutchNames, warningWriter)
    #duplicateCheck(frenchNames, warningWriter)
    
    inputReader = csv.reader(fIn, delimiter=delimiterInput)
    outputWriter = csv.writer(fOut, delimiter=delimiterInput)

    toBeReplaced = set()
    couldBeReplaced = set()
    replaced = set()
    numberRecords = 0
    numberNolangReplacements = 0
    numberDutchReplacements = 0
    numberFrenchReplacements = 0

    outputWriter.writerow(next(inputReader))

    for row in inputReader:
      manifestationID = row[0]
      contributorID = row[1]
      contributorName = row[2]
      contributorRole = row[3]
      uncertainty = row[4]

      newContributorID = contributorID
      newContributorName = contributorName
      contributorNameNorm = utils.getNormalizedString(contributorName)

      if len(contributorID) > 8:
        # it is a self-created identifier
        toBeReplaced.add(contributorID)

#        print(f'### check "{contributorName}"')
        if contributorNameNorm in frenchNames:
          couldBeReplaced.add(contributorID)
          if len(frenchNames[contributorNameNorm]) == 1:
            newContributorID = next(iter(frenchNames[contributorNameNorm]))
            replaced.add(contributorID)
#          print(f'found in frenchNames, will add {newContributorID} instead of {contributorID}')
        elif contributorNameNorm in dutchNames:
          couldBeReplaced.add(contributorID)
          if len(dutchNames[contributorNameNorm]) == 1:
            newContributorID = next(iter(dutchNames[contributorNameNorm]))
            replaced.add(contributorID)
#          print(f'found in dutchNames, will add {newContributorID} instead of {contributorID}')
        elif contributorNameNorm in nolangNames:
          couldBeReplaced.add(contributorID)
          if len(nolangNames[contributorNameNorm]) == 1:
            newContributorID = next(iter(nolangNames[contributorNameNorm]))
            replaced.add(contributorID)
#          print(f'found in nolangNames, will add {newContributorID} instead of {contributorID}')
         
      outputWriter.writerow([manifestationID, newContributorID, newContributorName, contributorRole, uncertainty])
      numberRecords += 1

  numberToBeReplaced = len(toBeReplaced)
  numberReplaced = len(replaced)
  numberCouldBeReplaced = len(couldBeReplaced)
  numberNotReplaced = numberCouldBeReplaced - numberReplaced
  print(f'Successfully replaced {numberReplaced} from {numberToBeReplaced} self-created identifiers (However, we could have replaced {numberCouldBeReplaced} but for {numberNotReplaced} several replacement candidates were possible)')

#  print("NOLANG")
#  print(nolangNames)
#  print("DUTCH")
#  print(dutchNames)
#  print("FRENCH")
#  print(frenchNames)

main()
