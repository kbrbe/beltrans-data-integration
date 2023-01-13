import os
import csv
import argparse
import hashlib
import operator
from tools.string import utils_string
from tools import utils

# -----------------------------------------------------------------------------
def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input-file', action='store', help="The CSV file with contributions")
  parser.add_argument('-o', '--output-file', action='store', help='The name of the output CSV file containing the unique contributor information')
  parser.add_argument('-c', '--column', action='append', help="The name of the column whose content should be counted, if several columns are given, their string normalized combination will be taken")
  parser.add_argument('-s', '--statistic', action='store', help="The number of occurrences for values of this column will be counted per unique value ")
  options = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.output_file) or (not options.input_file) or (not options.column) ):
    parser.print_help()
    exit(1)

  inputFilename = options.input_file
  outputFilename = options.output_file
  columns = options.column

  statsColumn = options.statistic # according to the argparse documentation the default if not given is None

  if not os.path.isfile(inputFilename):
    print(f'The given input file does not exist: "{inputFilename}"')

  with open(inputFilename, 'r') as fIn, \
       open(outputFilename, 'w') as fOut:

    inputReader = csv.DictReader(fIn)
    fieldnames = inputReader.fieldnames


    rowNumber = 0
    stats = {}
    names = {}
    statsHeaders = set()
    count = {}
    for row in inputReader:
      
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
