#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import utils
from optparse import OptionParser

# -----------------------------------------------------------------------------
def main():
  """This script reads a CSV file and extracts the column given via the number or name parameter."""

  parser = OptionParser(usage="usage: %prog [options]") 
  parser.add_option('-i', '--input-file', action='store', help='The name of the CSV input file from which a column should be extracted')
  parser.add_option('-o', '--output-file', action='store', help='The name of the file in which the extracted column should be stored')
  parser.add_option('-c', '--column', action='store', help='The name or index of the column which should be extracted from the input')
  parser.add_option('-d', '--delimiter', action='store', help='The delimiter of the input file, default is ","')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) or (not options.column) ):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r') as fIn,\
       open(options.output_file, 'w') as fOut:

    inputDelimiter = options.delimiter if options.delimiter else ','
    reader = None
    index = None
    if options.column.isnumeric():
      index = int(options.column)
      reader = csv.reader(fIn, delimiter=inputDelimiter)
    else:
      index = options.column
      reader = csv.DictReader(fIn)

    writer = csv.writer(fOut, delimiter=inputDelimiter)
    for row in reader:
      writer.writerow([row[index]])

main()
