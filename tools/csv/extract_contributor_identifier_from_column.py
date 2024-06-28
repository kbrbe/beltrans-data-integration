#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import re
from tools import utils
import argparse

# -----------------------------------------------------------------------------
def main():
  """This script reads a CSV file, performs a split operation on the provided column and returns the specified part before or after the firs occurence of the split character"""

  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input-file', action='store', required=True, help='The name of the CSV file from which data should be extracted')
  parser.add_argument('-o', '--output-file', action='store', required=True, help='The name of the CSV file in which the extrated data is stored')
  parser.add_argument('--id-column', action='store', required=True, help='The column that contains row identifiers')
  parser.add_argument('-c', '--column', action='store', required=True, help='The input column that is split')
  parser.add_argument('-d', '--delimiter', action='store', default=',', help='The optional delimiter of the input CSV, default is a comma')
  options = parser.parse_args()

  with open(options.input_file, 'r') as inFile, \
       open(options.output_file, 'w') as outFile:

    inputReader = csv.DictReader(inFile, delimiter=options.delimiter)

    utils.checkIfColumnsExist(inputReader.fieldnames, [options.id_column, options.column])

    outputWriter = csv.DictWriter(outFile, fieldnames=[options.id_column, options.column])
    outputWriter.writeheader()

    for row in inputReader:
      rowID = row[options.id_column]
      colValue = row[options.column]

      if colValue != '':
        print(f'"{colValue}"')
        newValue = re.search(r'.*\((.*)\).*', colValue).group(1)
        outputWriter.writerow({options.id_column: rowID, options.column: newValue})

main()
