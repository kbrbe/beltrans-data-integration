import os
import csv
import argparse
import hashlib
import operator
import itertools
import json
from tools.string import utils_string
from tools import utils

# -----------------------------------------------------------------------------
def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('--new-csv', action='store', help="The new CSV file that contains changes in comparison to the old CSCV")
  parser.add_argument('--old-csv', action='store', help='The old CSV file')
  parser.add_argument('--diff', action='store', help="The name of the output file which reports the difference")
  parser.add_argument('--columns', action='append', help="An identifier column used to match the new and old CSV, if multiple repeat")
  options = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.new_csv) or (not options.old_csv) or (not options.diff) ):
    parser.print_help()
    exit(1)

  newCSVFilename = options.new_csv
  oldCSVFilename = options.old_csv
  outputFilename = options.diff
  identifierColumns = options.columns

  if not os.path.isfile(newCSVFilename):
    print(f'The given (newer) CSV file does not exist: "{newCSVFilename}"')
  if not os.path.isfile(oldCSVFilename):
    print(f'The given (older) CSV file does not exist: "{oldCSVFilename}"')

  with open(newCSVFilename, 'r') as newIn, \
       open(oldCSVFilename, 'r') as oldIn:

    newCSVReader = csv.DictReader(newIn)
    oldCSVReader = csv.DictReader(oldIn)

    useHash = True

    oldCSVLookup = {}
    hashIdentifierLookup = {}
    oldCSVRowNumber = 0
    numberOfIdentifiersInMoreThanOneRow = 0
    identifiersInMoreThanOneRow = set()

    # build lookup data structure
    for row in oldCSVReader:
      identifiers = utils.getDictValues(row, identifierColumns)
      hashIdentifierSet = utils.computeIdentifierSet(identifiers, useHashSum=useHash)
      
      csvLookupID = f'row-{oldCSVRowNumber}'
      oldCSVLookup[csvLookupID] = row
      for hashIdentifier in hashIdentifierSet:
        if hashIdentifier in hashIdentifierLookup:
          identifiersInMoreThanOneRow.add(hashIdentifier)
          alreadyLinkedRecords = hashIdentifierLookup[hashIdentifier]
          numberOfIdentifiersInMoreThanOneRow += 1
          hashIdentifierLookup[hashIdentifier].append(csvLookupID)
        else:
          hashIdentifierLookup[hashIdentifier] = [csvLookupID]
      oldCSVRowNumber += 1

    print('done')
    print(f'In {oldCSVRowNumber} records, {numberOfIdentifiersInMoreThanOneRow} identifiers are used in more than one row!')

    for identifier in identifiersInMoreThanOneRow:
      print(f'#### {identifier} ####')
      numberRecords = len(hashIdentifierLookup[identifier])
      print(f'ROWS {numberRecords}')
      for rowID in hashIdentifierLookup[identifier]:
        print(f'\t{rowID}: {oldCSVLookup[rowID]}')
      print()
    print(f'In {oldCSVRowNumber} records, {numberOfIdentifiersInMoreThanOneRow} identifiers are used in more than one row!')
    exit(1)

    for row in newCSVReader:
      
      identifiers = utils.getDictValues(row, identifierColumns)
      hashIdentifierSet = utils.computeIdentifierSet(identifiers, useHashSum=useHash)
      
      uniqueName = utils_string.getUniqueName(row, columns, delimiter=' ; ')
      if uniqueName != '':
        uniqueID = hashlib.md5(uniqueName.encode('utf-8')).hexdigest()

        # Store the unique name and input columns in a data structure
        if uniqueID not in names:
          names[uniqueID] = {'uniqueName': uniqueName}
          for col in columns:
            names[uniqueID][col] = row[col]

        # Count how often the normalized value was found
        if uniqueID in count:
          count[uniqueID] += 1
        else:
          count[uniqueID] = 1

        # additionally count optional statistics
        if statsColumn:
          statsHeaders.add(f'{statsColumn}-{row[statsColumn]}')
          utils.countValues(row, statsColumn, uniqueID, stats, valuePrefix=statsColumn)
      else:
        print(f'Empty values for columns "{columns}" when parsing row {rowNumber}: "{row}"')

      rowNumber += 1

    outputWriter = csv.DictWriter(fOut, fieldnames=['value', 'uniqueName'] + columns + ['count'] + list(statsHeaders), restval='0')
    outputWriter.writeheader()

    sortedCount = dict( sorted(count.items(), key=operator.itemgetter(1), reverse=True) )
    for uniqueValue in sortedCount:
      outputRow = {'value': uniqueValue}

      # add attributes we stored such as the unique name used to create the hash
      # or the values of the used input columns
      outputRow.update(names[uniqueValue])

      # add number of occurrences
      outputRow['count'] = count[uniqueValue]

      # add additional stats
      if statsColumn and uniqueValue in stats:
        outputRow.update(stats[uniqueValue])

      outputWriter.writerow(outputRow)

main()
