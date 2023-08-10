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
  parser.add_argument('--column-to-be-updated', required=True, action='store', help="The column in the first CSV that should be updated")
  parser.add_argument('--column-with-new-values', required=True, action='store', help="The column in the second CSV that contains new values")
  parser.add_argument('--id-column-1', action='store', required=True, help="The name of the identifier column in the first CSV used for joining")
  parser.add_argument('--id-column-2', action='store', required=True, help="The name of the identifier column in the second CSV used for joining")
  parser.add_argument('--info-column', action='store', help="The name of the column in which information about the replacement is stored. Optional")
  parser.add_argument('--value-delimiter', action='store', default=';', help="Delimiter for values in a column (for input CSV and output CSV)")
  parser.add_argument('-m', '--mode', choices=['append', 'replace'], required=True, help="Controls what happens if there is already a value")
  parser.add_argument('--log-column-2', action='store', required=False, help="The name of a column of the second CSV whose values should be logged for each update. Optional")
  args = parser.parse_args()

  if not os.path.isfile(args.csv_1):
    print(f'The given first CSV file does not exist: "{args.csv_1}"')
  if not os.path.isfile(args.csv_2):
    print(f'The given second CSV file does not exist: "{args.csv_2}"')


  delimiter = args.value_delimiter

  with open(args.csv_1, 'r') as firstCSV, \
       open(args.csv_2, 'r') as secondCSV, \
       open(args.output_csv, 'w', newline='') as outputCSV:

    firstCSVReader = csv.DictReader(firstCSV)
    secondCSVReader = csv.DictReader(secondCSV)

    utils.checkIfColumnsExist(firstCSVReader.fieldnames, [args.id_column_1, args.column_to_be_updated])
    utils.checkIfColumnsExist(secondCSVReader.fieldnames, [args.id_column_2, args.column_with_new_values])

    outputFieldnames = firstCSVReader.fieldnames
    if args.info_column:
      outputFieldnames.append(args.info_column)
    if args.log_column_2:
      utils.checkIfColumnsExist(secondCSVReader.fieldnames, [args.log_column_2])
      logColumnName = f'log-{args.log_column_2}'
      outputFieldnames.append(logColumnName)

    outputWriter = csv.DictWriter(outputCSV, fieldnames=outputFieldnames)
    outputWriter.writeheader()

    # storing new values in a lookup dictionary
    # we store the values in a set for the case that the input has n:1 relation
    newValues = {}
    logValues = {}
    counterLookupDuplicates = 0
    counterLogValueDuplicates = 0
    for row in secondCSVReader:
      rowID = row[args.id_column_2]
      value = row[args.column_with_new_values]
      if rowID in newValues:
        counterLookupDuplicates += 1
        newValues[rowID].add(value)
      else:
        newValues[rowID] = set([value])

      if args.log_column_2:
        logValue = row[args.log_column_2]
        if logValue in logValues:
          counterLogValueDuplicates += 1
          logValues[rowID].add(logValue)
        else:
          logValues[rowID] = set([logValue])

    # update values in first CSV
    identifiersMatch = set()
    identifiersToBeUpdated = set()
    identifiersSameValue = set()
    identifiersReplacedValue = set()
    identifiersNoMatch = set()
    identifiersAddedValue = set()
    identifiersNotUpdatedWithEmptyValue = set()
    identifiersBothEmpty = set()

    for row in firstCSVReader:
      rowID = row[args.id_column_1]
      identifiersToBeUpdated.add(rowID)
      info = ''
      if rowID in newValues:
        currentValue = row[args.column_to_be_updated]
        identifiersMatch.add(rowID)
        newValue = utils.getOrderedString(newValues[rowID], delimiter)

        if currentValue == '':
          # currently empty and we can add something
          if newValue == '':
            # the new value is also empty, we do nothing
            identifiersBothEmpty.add(rowID)
            info = 'old and new were empty'
          else:
            # new value can be added and replace empty string
            identifiersAddedValue.add(rowID)
            row[args.column_to_be_updated] = utils.getNewValue(currentValue, newValue, delimiter, args.mode)
            info = 'added'
            
        else:
          # currently NOT empty
          if currentValue == newValue:
            # new value is the same as the old
            identifiersSameValue.add(rowID)
            info = 'old and new were the same'
          elif newValue == '':
            # new value is empty, we do nothing or replace depending on the mode
            identifiersNotUpdatedWithEmptyValue.add(rowID)
            if mode == 'replace':
              row[args.column_to_be_updated] = newValue 
              info = f'replaced "{currentValue}" with empty string'
            else:
              info = 'not replaced, new value would be empty'
          else:
            # new value is different than existing
            identifiersReplacedValue.add(rowID)
            info = f'replaced "{currentValue}"' if args.mode == 'replace' else f'appended "{newValue}" to "{currentValue}"'
            row[args.column_to_be_updated] = utils.getNewValue(currentValue, newValue, delimiter, args.mode)
          
      else:
        identifiersNoMatch.add(rowID)
        info = 'not part of update'
      if args.info_column:
        row[args.info_column] = info
      if args.log_column_2:
        if rowID in logValues:
          row[logColumnName] = delimiter.join(logValues[rowID])
      outputWriter.writerow(row)

    # check for identifiers of the updated list that could not be joined
    counterRows = len(identifiersToBeUpdated)
    counterMatch = len(identifiersMatch)
    counterBothEmpty = len(identifiersBothEmpty)
    counterNewValue = len(identifiersAddedValue)
    counterSame = len(identifiersSameValue)
    counterNotReplacedWithEmpty = len(identifiersNotUpdatedWithEmptyValue)
    counterReplaced = len(identifiersReplacedValue)
    counterNoNewValue = len(identifiersNoMatch)
      
   
    counterUpdateValues = len(newValues.keys())
    identifiersNotFound = newValues.keys() - identifiersToBeUpdated
    counterNotFound = len(identifiersNotFound)
    print()
    print(f'The update CSV has {counterUpdateValues} unique rows (including {counterLookupDuplicates} duplicate rows, total: {counterUpdateValues+counterLookupDuplicates} )')
    print(f'\t{counterNotFound} rows with new values had no match with CSV')
    print(f'\t{counterUpdateValues-counterNotFound} rows matched ({counterUpdateValues} minus {counterNotFound} for which no match between the CSVs was found)')
    print(f'The input CSV has {counterRows} rows')
    print(f'\t{counterNoNewValue} rows did not match with any update row')
    print(f'\t{counterMatch} rows matched, from those')
    print(f'\t\t{counterNewValue} rows were enriched')
    print(f'\t\t{counterSame} rows had the same value as the new one')
    print(f'\t\t{counterBothEmpty} rows had an empty value for both input and update')
    print(f'\t\t{counterReplaced} rows had a value that was appended or replaced from the update')
    print(f'\t\t{counterNotReplacedWithEmpty} rows had a value but the update list provided an empty value (we did not update it)')
    print()
    print(f'The following {counterNotFound} identifiers from the CSV with new values {args.csv_2} did not match any identifiers in the input CSV {args.csv_1}:')
    print()
    print(identifiersNotFound)


main()
