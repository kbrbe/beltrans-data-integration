#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from tools import utils
from optparse import OptionParser

# -----------------------------------------------------------------------------
def main():
  """This script reads a CSV file, and adds an auto increment number to a specified column relative to another column"""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The name of the CSV file from which data should be extracted')
  parser.add_option('-o', '--output-file', action='store', help='The name of the CSV file in which the extrated data is stored')
  parser.add_option('--identifier-column', action='store', help='The column with the relative identifier based on which sequence numbers should be numbered')
  parser.add_option('--sequence-number-column', action='store', help='The column that contains sequence numbers wthat have gaps which should be filled')
  parser.add_option('-d', '--delimiter', action='store', default=',', help='The optional delimiter of the input CSV, default is a comma')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if (not options.input_file) and (not options.output_file) and (not options.identifier_column) and (not options.sequence_number_column):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r') as inFile, \
       open(options.output_file, 'w') as outFile:

    inputReader = csv.DictReader(inFile, delimiter=options.delimiter)

    utils.checkIfColumnsExist(inputReader.fieldnames, [options.identifier_column, options.sequence_number_column])

    outputWriter = csv.DictWriter(outFile, fieldnames=inputReader.fieldnames)
    outputWriter.writeheader()

    lastRowID = None
    lastSequenceNumber = 0
    for row in inputReader:
      rowID = row[options.identifier_column]
      sequenceNumber = int(row[options.sequence_number_column]) if row[options.sequence_number_column] != '' else 0

      if sequenceNumber:
        lastSequenceNumber = sequenceNumber if sequenceNumber != '' else 0
      else:
        if rowID == lastRowID:
          lastSequenceNumber += 1
          row[options.sequence_number_column] = lastSequenceNumber
        elif lastRowID is None:
          # this is the first row and there is no sequence number yet
          row[options.sequence_number_column] = 0
          lastSequenceNumber = 0
        else:
          # the current rowID is different from the last and there is no sequence number yet
          row[options.sequence_number_column] = 0
          lastSequenceNumber = 0

      lastRowID = rowID
      outputWriter.writerow(row)
          
  print('Finished without errors!')

main()
