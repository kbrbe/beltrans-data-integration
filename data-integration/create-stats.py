#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import pandas as pd
import utils
import json
import xlsxwriter

# -----------------------------------------------------------------------------
def getDataTypes(filename):
  """This function reads the given filename as CSV where the first column will be a column name and the second the datatype."""
  types = {}
  with open(filename, 'r') as dTypeIn:
    dtypeReader = csv.reader(dTypeIn, delimiter=',')
    for row in dtypeReader:
      types[row[0]] = row[1]
  return types

# -----------------------------------------------------------------------------
def main():
  """This script creates statistics based on the input CSV file."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The CSV file over which statistics will be made')
  parser.add_option('-o', '--output-file', action='store', help='The Excel file in which content is stored')
  parser.add_option('-d', '--dtype-file', action='store', help='A CSV with a mapping between input CSV columns and pandas data types')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if ( (not options.input_file) or (not options.output_file) or (not options.dtype_file) ):
    parser.print_help()
    exit(1)

  dtypes = getDataTypes(options.dtype_file)
  df = pd.read_csv(options.input_file, dtype=dtypes)

  # todo: translations per year
  #translationsPerYear = pd.pivot_table(df, values='targetTextYearOfPublication',
  #                                         columns='targetTextLanguage')
  #print(translationsPerYear)
  # todo: translations per country
  # todo: translations per location
  # todo: translations per publisher
  # todo: translations per source

  wb = xlsxwriter.Workbook(options.output_file)

#  for filename in args:
#    with open(filename, 'r', encoding="utf-8") as inFile:

#      inputReader = csv.reader(inFile, delimiter=',')
#      sheet = wb.add_worksheet(options.sheet_names.pop(0))

#      for r, row in enumerate(inputReader):
#        for c, val in enumerate(row):
#          sheet.write(r, c, val)

#  wb.close()

main()
