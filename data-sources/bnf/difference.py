#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import utils
from optparse import OptionParser

# -----------------------------------------------------------------------------
def main():
  """This script reads one or more CSV files, extracts the first column and counts the symmetric difference between the ID sets. Optionally an output CSV is created containing those IDs. Optionally the difference of all sets minus the last or the first minus all last is counted"""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-o', '--output-file', action='store', help='The name of the file in which the found intersection IDs should be stored')
  parser.add_option('-r', '--minus-rest', action='store_true', help='The difference of the first set minus a union of the rest is computed')
  parser.add_option('-l', '--minus-last', action='store_true', help='The difference of the union of n-1 sets minus the last set is computed')
  parser.add_option('-d', '--delimiter', action='store', help='The name of the file in which the found union IDs should be stored')
  
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if not args:
    parser.print_help()
    exit(1)

  if options.minus_rest and options.minus_last:
    print(f'Error, values for minus-rest AND minus-last provided. Neither of the values or only one are valid combinations.') 
    parser.print_help()
    exit(1)

  delimiter = options.delimiter if options.delimiter else ','
  identifierSets = []
  fileCounter = 0
  for a in args:
    with open(a, 'r') as fIn:
      currentSet = set()
      currentFileIDCounter = 0
      reader = csv.reader(fIn, delimiter=delimiter)
      for row in reader:
        identifier = utils.extractBnFIdentifier(row[0])
        currentSet.add(identifier)
        currentFileIDCounter += 1
      numberUniqueIDs = len(currentSet)
      identifierSets.append(currentSet)
      print(f'Successfully read {currentFileIDCounter} identifiers from {numberUniqueIDs} records in given CSV file {a}')

  differenceSet = None
  if options.minus_rest:
    setA = identifierSets[0]
    setRest = identifierSets[1:len(identifierSets)]
    setB = set.union(*setRest)
    differenceSet = setA - setB
  elif options.minus_last:
    allButLast = identifierSets[0:len(identifierSets)-1]
    setA = set.union(*allButLast)
    setB = identifierSets[len(identifierSets)-1]
    differenceSet = setA - setB
  else:
    differenceSet = set.difference(*identifierSets)

  numberDifference = len(differenceSet)
  print(f'The difference between the files are {numberDifference} unique identifiers')

  if(options.output_file):
    with open(options.output_file, 'w') as outFile:
      outputWriter = csv.writer(outFile, delimiter=',')
      for identifier in differenceSet:
        outputWriter.writerow([identifier])
      print(f'Successfully wrote {numberDifference} identifiers to {options.output_file}')


main()
