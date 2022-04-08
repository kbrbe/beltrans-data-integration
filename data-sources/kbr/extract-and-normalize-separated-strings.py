#
# (c) 2022 Sven Lieber
# KBR Brussels
#
from optparse import OptionParser
import pandas as pd
import math
import utils
import csv
from datetime import datetime


# -----------------------------------------------------------------------------
def main():
  """This script extracts manifestation IDs and assigned Belgian Bibliography classifications."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing CSV data')
  parser.add_option('-o', '--output-file', action='store', help='The file in which extracted values are stored')
  parser.add_option('--input-id-column-name', action='store', help='The name of the ID column in the input file')
  parser.add_option('--input-value-column-name', action='store', help='The name of the to-be-split value column in the input')
  parser.add_option('--output-id-column-name', action='store', help='The name of the ID column in the output file')
  parser.add_option('--output-value-column-name', action='store', help='The name of the value column in the output')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) or (not options.input_id_column_name) or (not options.input_id_column_name) or (not options.input_value_column_name) or (not options.output_value_column_name) ):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r', encoding="utf-8") as inFile, \
       open(options.output_file, 'w', encoding="utf-8") as outFile:

    inputReader = csv.DictReader(inFile, delimiter=',')

    outputHeaders = [options.output_id_column_name, options.output_value_column_name]
    outputWriter = csv.DictWriter(outFile, fieldnames=outputHeaders, delimiter=',')

    outputWriter.writeheader()

    for row in inputReader:

      valueString = row[options.input_value_column_name]

      # check if there is a value in this column
      if len(valueString) > 0:
        values = valueString.split(';')
        # check if there were multiple splitted values
        if len(values) > 0:
          for v in values:
            # check if the splitted value is not just empty
            if len(v) > 0:
              outputRow = {}
              outputRow[options.output_id_column_name] = row[options.input_id_column_name]
              outputRow[options.output_value_column_name] = v
              outputWriter.writerow(outputRow)

  print("Finished without errors")

main()
