import os
import csv
import argparse
from tools.string import utils_string
from tools import utils

# -----------------------------------------------------------------------------
def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('--csv-1', action='store', required=True, help="The CSV file in which column values should be updated")
  parser.add_argument('--csv-2', action='store', required=True, help='The CSV file that contains the new values')
  parser.add_argument('--output-csv', action='store', required=True, help='The output CSV file with the updated values')
  parser.add_argument('--id-column-1', action='store', required=True, help="The name of the identifier column in the first CSV used for joining")
  parser.add_argument('--id-column-2', action='store', required=True, help="The name of the identifier column in the second CSV used for joining")
  args = parser.parse_args()

  if not os.path.isfile(args.csv_1):
    print(f'The given first CSV file does not exist: "{args.csv_1}"')
  if not os.path.isfile(args.csv_2):
    print(f'The given second CSV file does not exist: "{args.csv_2}"')


  with open(args.csv_1, 'r') as firstCSV, \
       open(args.csv_2, 'r') as secondCSV, \
       open(args.output_csv, 'w', newline='') as outputCSV:

    firstCSVReader = csv.DictReader(firstCSV)
    secondCSVReader = csv.DictReader(secondCSV)

    utils.checkIfColumnsExist(firstCSVReader.fieldnames, [args.id_column_1])
    utils.checkIfColumnsExist(secondCSVReader.fieldnames, [args.id_column_2])

    outputFieldnames = firstCSVReader.fieldnames 
    outputWriter = csv.DictWriter(outputCSV, fieldnames=outputFieldnames)
    outputWriter.writeheader()

    # storing new values in a lookup dictionary
    # we store the values in a set for the case that the input has n:1 relation
    matchIDs = set()
    counterLookupDuplicates = 0
    for row in secondCSVReader:
      rowID = row[args.id_column_2]
      if rowID != '':
        if rowID in matchIDs:
          counterLookupDuplicates += 1
        else:
          matchIDs.add(rowID)

    numberLookup = len(matchIDs)
    numberRows = 0
    numberRowsRemoved = 0
    numberRowsKept = 0
    for row in firstCSVReader:
      numberRows += 1
      rowID = row[args.id_column_1]

      # keep rows that are not part of the "to be deleted" CSV
      if rowID in matchIDs:
        matchIDs.remove(rowID)
        numberRowsRemoved += 1
      else:
        numberRowsKept += 1
        outputWriter.writerow(row)

    print()
    print(f'Read {numberLookup} unique rows in lookup CSV (plus {counterLookupDuplicates} duplicate values)')
    print(f'{numberRowsRemoved} rows matched and thus were not added to the output, {numberRowsKept} rows from {numberRows} were kept')
    print(f'The following {len(matchIDs)} identifiers from the lookup were not found: {matchIDs}')
    print()

main()
