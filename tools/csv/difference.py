#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from tools import utils
from optparse import OptionParser

# -----------------------------------------------------------------------------
def main(csvFilenames, outputFilename, outputColumnName, minusRest, minusLast, columns, delimiter):
  """This script reads one or more CSV files, extracts the first column and counts the symmetric difference between the ID sets. Optionally an output CSV is created containing those IDs. Optionally the difference of all sets minus the last or the first minus all last is counted"""

  if minusRest and minusLast:
    print(f'Error: values for minus-rest AND minus-last provided. Neither of the values or only one are valid combinations.') 
    exit(1)

  identifierSets = []
  fileCounter = 0

  if columns:

    if len(columns) > 1 and len(columns) != len(csvFilenames):
      print(f'Error: the number of column names should be 1 or the same number as input files')
      print(f'Given columns "{option.columns}", given files "{csvFilenames}"')
      exit(1)

    if len(columns) == len(csvFilenames):
      counter = 0
      # check if each input file contains the specified column with the same index
      for inputFilename in csvFilenames:
        with open(inputFilename, 'r') as inFile:
          inputReader = csv.DictReader(inFile, delimiter=delimiter)
          utils.checkIfColumnsExist(inputReader.fieldnames, [columns[counter]])
        counter += 1

    elif len(columns) == 1:
      # check if each input file contains the single specified column
      for inputFilename in csvFilenames:
        with open(inputFilename, 'r') as inFile:
          inputReader = csv.DictReader(inFile, delimiter=delimiter)
          utils.checkIfColumnsExist(inputReader.fieldnames, [columns[0]])
    else:
      print(f'Error: this should not happen, no implemented functionality for the number of columns and input files')
      print(f'Given columns "{option.columns}", given files "{csvFilenames}"')
      

  # Read all input files
  fileCounter = 0
  for a in csvFilenames:
    with open(a, 'r') as fIn:
      currentSet = set()
      currentFileIDCounter = 0
      reader = csv.DictReader(fIn, delimiter=delimiter)
      for row in reader:
        if columns and len(columns) == len(csvFilenames): 
          identifier = row[columns[fileCounter]]
        elif columns and len(columns) == 1:
          identifier = row[columns[0]]
        elif columns == None:
          identifier = row[fieldnames[0]]
        currentSet.add(identifier)
        currentFileIDCounter += 1
      numberUniqueIDs = len(currentSet)
      identifierSets.append(currentSet)
      print(f'Successfully read {currentFileIDCounter} identifiers from {numberUniqueIDs} records in given CSV file {a}')
    fileCounter += 1 

  differenceSet = None
  if minusRest:
    setA = identifierSets[0]
    setRest = identifierSets[1:len(identifierSets)]
    setB = set.union(*setRest)
    differenceSet = setA - setB
  elif minusLast:
    allButLast = identifierSets[0:len(identifierSets)-1]
    setA = set.union(*allButLast)
    setB = identifierSets[len(identifierSets)-1]
    differenceSet = setA - setB
  else:
    differenceSet = set.difference(*identifierSets)

  numberDifference = len(differenceSet)
  print(f'The difference between the files are {numberDifference} unique identifiers')

  if(outputFilename):
    with open(outputFilename, 'w') as outFile:
      outputWriter = csv.writer(outFile, delimiter=',')
      outputWriter.writerow([outputColumnName])
      for identifier in differenceSet:
        outputWriter.writerow([identifier])
      print(f'Successfully wrote {numberDifference} identifiers to {outputFilename}')

# -----------------------------------------------------------------------------
def parseArguments():

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-o', '--output-file', action='store', help='The name of the file in which the difference IDs should be stored')
  parser.add_option('-r', '--minus-rest', action='store_true', help='The difference of the first set minus a union of the rest is computed')
  parser.add_option('-l', '--minus-last', action='store_true', help='The difference of the union of n-1 sets minus the last set is computed')
  parser.add_option('-d', '--delimiter', action='store', help='The optional delimiter of the CSV files, default is a comma')
  parser.add_option('-c', '--columns', action='append', help='The optional column names that should be taken, default is the first column')
  parser.add_option('--output-column', action='store', help='The name of the output columns')
  
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if not args:
    parser.print_help()
    exit(1)

  if not options.output_column:
    print(f'Error: no name for output column specified')
    exit(1)

  if options.delimiter == None:
    options.delimiter = ','

  return (options, args)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
  (options, args) = parseArguments()
  main(args, options.output_file, options.output_column, options.minus_rest, options.minus_last, options.columns, options.delimiter)
