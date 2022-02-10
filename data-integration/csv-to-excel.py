#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import utils
import json
import xlsxwriter

# -----------------------------------------------------------------------------
def main():
  """This script creates an Excel file based on the CSV input. One or more CSV files can be given via arguments, each becomes a new sheet in the output Excel workbook"""

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

  wb = xlsxwriter.Workbook(options.output_file)

  for filename in args:
    with open(filename, 'r', encoding="utf-8") as inFile:

      inputReader = csv.reader(inFile, delimiter=',')
      sheet = wb.add_worksheet(options.sheet_names.pop(0))

      for r, row in enumerate(inputReader):
        for c, val in enumerate(row):
          sheet.write(r, c, val)

  wb.close()

main()
