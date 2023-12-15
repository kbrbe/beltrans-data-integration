#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import json
from tools import utils
import openpyxl

# -----------------------------------------------------------------------------
def checkArguments():

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The Excel file from which data is extracted')
  parser.add_option('-s', '--sheet-names', action='append', help='sheet names for the different input CSV files')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if not args:
    print("You need to provide at least one CSV file")
    parser.print_help()
    exit(1)

  if not options.input_file or not options.sheet_names:
    print("You need to specify an input filename and names of sheets in it")
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
def main(input_file, sheet_names, csvFiles):
  """This script creates CSV files based on the Excel input. One or more CSV filenames can be given via arguments, each becomes a new CSV file based on sheets of the input Excel workbook"""

  wb = openpyxl.load_workbook(input_file)

  # check upfront if the sheet names we want extract exist
  utils.checkIfColumnsExist(sheet_names, wb.sheetnames)

  # loop over output files
  outputFileIndex = 0
  for filename in csvFiles:
    # get the sheet corresponding with the index
    sheet = wb[sheet_names[outputFileIndex]]
    with open(filename, 'w', encoding="utf-8") as outFile:

      outputWriter = csv.writer(outFile)
      for row in sheet.rows:
        outputWriter.writerow([cell.value for cell in row])

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  (options, args) = checkArguments()
  main(options.input_file, options.sheet_names, args)
