#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import json
import itertools
import xlsxwriter

# -----------------------------------------------------------------------------
def checkArguments():

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-o', '--output-file', action='store', help='The Excel file in which content is stored')
  parser.add_option('-s', '--sheet-names', action='append', help='sheet names for the different input CSV files')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if not args:
    print("You need to provide at least one CSV file")
    parser.print_help()
    exit(1)

  if not options.output_file or not options.sheet_names:
    print("You need to specify an output filename")
    parser.print_help()
    exit(1)

  if not options.sheet_names:
    print("You need to provide names for the sheets in the output Excel file")
    parser.print_help()
    exit(1)

  if len(args) != len(options.sheet_names):
    print("You provided too much or to less names for sheets for the input")
    parser.print_help()
    exit(1)

  return (options, args)

# -----------------------------------------------------------------------------
def main(output_file, sheet_names, csvFiles):
  """This script creates an Excel file based on the CSV input. One or more CSV files can be given via arguments, each becomes a new sheet in the output Excel workbook"""


  wb = xlsxwriter.Workbook(output_file, {'strings_to_formulas': False, 'strings_to_numbers': True})

  for filename in csvFiles:
    with open(filename, 'r', encoding="utf-8") as inFile:

      rowCountReader, colCountReader, inputReader = itertools.tee(csv.reader(inFile, delimiter=','), 3)

      rowCount = sum(1 for row in rowCountReader)
      header = next(colCountReader)
      colCount = len(header)
      del rowCountReader
      del colCountReader
      print(f'{filename} has {rowCount} rows and {colCount} cols')

      sheet = wb.add_worksheet(sheet_names.pop(0))

      headerDict = [ {'header': e} for e in header]
      table = sheet.add_table(0,0,rowCount,colCount-1, {'style': 'Table Style Light 11', 'header_row': True, 'columns': headerDict})
      for r, row in enumerate(inputReader):
        #print(f'r {r} and row {row}')
        #for c, val in enumerate(row):
        #  sheet.write_row(r, c, row)
        sheet.write_row(r, 0, row)

  wb.close()

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  (options, args) = checkArguments()
  main(options.output_file, options.sheet_names, args)
