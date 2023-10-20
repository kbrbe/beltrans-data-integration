#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
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
  parser.add_argument('-s', '--split-string', action='store', required=True, help='The string based on which values in the input columns are split')
  parser.add_argument('-p', '--part', choices=['before','after'], required=True, help='Indicating if the part before or after the split char should be taken, options are "before" and "after"')
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
        if options.split_string in colValue:
          values = colValue.split(options.split_string)
          if options.part == 'before':
            newValue = values[0]
          elif options.part == 'after':
            # in case the split string occurred several times
            # return everything after the first occurence
            newValue = options.split_string.join(values[1:len(values)])
        else:
          newValue = colValue
        outputWriter.writerow({options.id_column: rowID, options.column: newValue})

main()
