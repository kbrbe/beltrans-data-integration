#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import utils
from optparse import OptionParser

# -----------------------------------------------------------------------------
def main():
  """This script reads one or more CSV files, extracts the first column and counts the union of IDs. Optionally an output CSV is created containing those IDs."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-o', '--output-file', action='store', help='The name of the file in which the found union IDs should be stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if not args:
    parser.print_help()
    exit(1)

  identifierSets = []
  fileCounter = 0
  for a in args:
    with open(a, 'r') as fIn:
      currentSet = set()
      currentFileIDCounter = 0
      reader = csv.reader(fIn, delimiter=';')
      for row in reader:
        identifier = utils.extractBnFIdentifier(row[0])
        currentSet.add(identifier)
        currentFileIDCounter += 1
      numberUniqueIDs = len(currentSet)
      identifierSets.append(currentSet)
      print(f'Successfully read {currentFileIDCounter} identifiers from {numberUniqueIDs} records in given CSV file {a}')

  unionIDs = set.union(*identifierSets)
  numberUnion = len(unionIDs)

  print(f'The union between the files are {numberUnion} unique identifiers')

  if(options.output_file):
    with open(options.output_file, 'w') as outFile:
      outputWriter = csv.writer(outFile, delimiter=',')
      for identifier in unionIDs:
        outputWriter.writerow([identifier])
      print(f'Successfully wrote {numberUnion} identifiers to {options.output_file}')


main()
