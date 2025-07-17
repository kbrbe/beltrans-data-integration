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
  parser.add_argument('-c', '--column', action='append', required=True, help='The input column that is split')
  parser.add_argument('--output-column-name', action='store', help='The name of the output column, by default the name of extracted column, the name of the first extracted column in case multiple are given. Please note that a warning will be given in such a case.')
  parser.add_argument('-d', '--delimiter', action='store', default=',', help='The optional delimiter of the input CSV, default is a comma')
  options = parser.parse_args()

  with open(options.input_file, 'r') as inFile, \
       open(options.output_file, 'w') as outFile:

    inputReader = csv.DictReader(inFile, delimiter=options.delimiter)

    utils.checkIfColumnsExist(inputReader.fieldnames, [options.id_column] + options.column)

    if len(options.column) > 1 and not options.output_column_name:
      print('Warning: multiple input columns given, but no output column name. Default is first column name, thus "{options.column[0]}"')
      outputColumnName = options.column[0]
    elif len(options.column) == 1 and not options.output_column_name:
      outputColumnName = options.column[0]
    else:
      outputColumnName = options.output_column_name

    outputWriter = csv.DictWriter(outFile, fieldnames=[options.id_column, outputColumnName])
    outputWriter.writeheader()

    for row in inputReader:
      rowID = row[options.id_column]

      for col in options.column:
        colValue = row[col]

        if colValue != '':
          values = colValue.split(';')
          for val in values:
            result = re.search(r'.*\((.*)\).*', val)
            if result:
              newValue = result.group(1)
              outputWriter.writerow({options.id_column: rowID, outputColumnName: newValue})
            else:
              print(f'No identifier in contributor name string for row {rowID}: "{val}"')

main()
