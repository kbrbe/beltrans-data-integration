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
  """This script creates an Excel file based on the CSV input."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing CSV data')
  parser.add_option('-o', '--output-file', action='store', help='The Excel file in which content is stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  #
  # Open input file with encoding 'utf-8-sig' (instead of 'utf-8') because the Syracuse export contains Byte Order marks (BOM)
  #
  with open(options.input_file, 'r', encoding="utf-8") as inFile, \
       open(options.output_file, 'w', encoding="utf-8") as outFile:

    inputReader = csv.reader(inFile, delimiter=',')

    wb = xlsxwriter.Workbook(options.output_file)
    sheet = wb.add_worksheet('data')

    for r, row in enumerate(inputReader):
      for c, val in enumerate(row):
        sheet.write(r, c, val)

  wb.close()

main()
