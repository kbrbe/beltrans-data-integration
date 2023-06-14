import os
import csv
import argparse
import hashlib
import operator
from tools.string import utils_string
from tools import utils

# -----------------------------------------------------------------------------
def main():
  """This script reads one or more CSV files, groups rows where the string-normalized value of a given column is the same and generates a new CSV file where the duplicates are reported."""

  parser = argparse.ArgumentParser()
  parser.add_argument('-o', '--output-file', action='store', help='The name of the output CSV file containing the unique contributor information')
  parser.add_argument('--id-column', action='store', help='The name of the column whose value will be taken as unique identifier')
  parser.add_argument('--aggregate-column', action='store', help='The name of the column whose value will be used to aggregate')
  parser.add_argument('-c', '--column', action='append', help="The name of a column that should be in the output csv. This option can be repeated")
  parser.add_argument('inputFiles', metavar='F', nargs='+', help="A list of input CSV files")
  options = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if not options.inputFiles:
    print('No input file(s) was/were given')
    parser.print_help()
    exit(1)
  
  if( (not options.output_file) or (not options.column) or (not options.id_column) or (not options.aggregate_column) ):
    print('One or more required options are missing')
    parser.print_help()
    exit(1)

  outputFilename = options.output_file
  columns = options.column
  aggregateColumn = options.aggregate_column
  uniqueIDColumn = options.id_column


  names = {}
  for inputFilename in options.inputFiles:

    if not os.path.isfile(inputFilename):
      print(f'The given input file does not exist: "{inputFilename}"')
      continue

    with open(inputFilename, 'r') as fIn:

      inputReader = csv.DictReader(fIn)
      fieldnames = inputReader.fieldnames

      rowNumber = 0
      for row in inputReader:
        
        aggregateValue = utils_string.getNormalizedString(str(row[aggregateColumn]))
        if aggregateValue == '':
          continue
        uniqueID = str(row[uniqueIDColumn])

        # Create a dictionary with the data we want to store
        valueToAdd = {'source': inputFilename, uniqueIDColumn: uniqueID}
        for col in columns:
          valueToAdd[col] = row[col]

        # Store the unique name and input columns in a data structure
        if aggregateValue in names:
          names[aggregateValue].append(valueToAdd)
        else:
          names[aggregateValue] = [valueToAdd]

        rowNumber += 1

  with open(outputFilename, 'w') as fOut:
    outputWriter = csv.DictWriter(fOut, fieldnames=['nameID'] + [aggregateColumn] + [uniqueIDColumn] + columns + ['source'])
    outputWriter.writeheader()

    for name, sourceList in names.items():
      if len(sourceList) > 1:
        sameNameRecords = []
        processedIDs = set()
        for candidate in sourceList:
          candidateID = candidate[uniqueIDColumn]
          if candidateID not in processedIDs:
            sameNameRecords.append(candidate)
          processedIDs.add(candidateID)
        
        if len(sameNameRecords) > 1:
          nameID = hashlib.md5(name.encode('utf-8')).hexdigest()
          print(f'{name} ({nameID}): {sameNameRecords}')

          for record in sameNameRecords:
            outputRow = {'nameID': nameID, aggregateColumn: name}
            print(f'BEFORE: {outputRow}')
            for field in record:
              print(f'\tupdating field: {field}')
              outputRow.update(record)
            print(f'AFTER: {outputRow}')
            outputWriter.writerow(outputRow)


main()
