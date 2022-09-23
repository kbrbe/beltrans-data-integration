#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import utils
from optparse import OptionParser

# -----------------------------------------------------------------------------
def main():
  """This script reads two CSV files, extracts the values of the given column from the first CSV file. If the read value of that column is not found in the same column of the second CSV, the whole row of the first CSV is added to the output. Hence the output will contain all rows of the first CSV which were not found in the second CSV."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-o', '--output-file', action='store', help='The name of the file in which the found intersection IDs should be stored')
  parser.add_option('--first-csv', action='store', help='Input CSV file')
  parser.add_option('--second-csv', action='store', help='Second CSV file')
  parser.add_option('--first-column', action='store', help='column name of the first CSV which is taken for comparison')
  parser.add_option('--second-column', action='store', help='column name of the second CSV which is taken for comparison')
  parser.add_option('-d', '--delimiter', action='store', default=',', help='The name of the file in which the found union IDs should be stored')
  
  (options, args) = parser.parse_args()

  if (not options.first_csv) or (not options.second_csv) or (not options.output_file) or (not options.first_column) or (not options.second_column):
    print(f'Input and output data are needed')
    parser.print_help()
    exit(1)

  
  with open(options.first_csv, 'r') as fileFirst, \
       open(options.second_csv, 'r') as fileSecond, \
       open(options.output_file, 'w') as outputFile:

    readerFirst = csv.DictReader(fileFirst, delimiter=options.delimiter)
    readerSecond = csv.DictReader(fileSecond, delimiter=options.delimiter)
    outputWriter = csv.DictWriter(outputFile, fieldnames=readerFirst.fieldnames)

    identifiers = []
    rowNumber = 0
    for row in readerSecond:
      foundIdentifier = row[options.first_column]
      identifiers.append(foundIdentifier)
      if foundIdentifier in identifiers:
        print(f'Warning, identifier {foundIdentifier} was already found, column values are not unique!')
      rowNumber += 1

    outputWriter.writeheader()
    firstRowNumber = 0
    outputRowNumber = 0
    for row in readerFirst:
      foundIdentifier = row[options.second_column]
      if foundIdentifier not in identifiers:
        outputRowNumber += 1
        outputWriter.writerow(row)
      firstRowNumber += 1
      
    print(f'{outputRowNumber}/{firstRowNumber} of the first file were not found in the second CSV ({rowNumber} lines).')

main()
