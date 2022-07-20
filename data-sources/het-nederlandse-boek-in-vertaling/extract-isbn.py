#
# (c) 2022 Sven Lieber
# KBR Brussels
#

import rispy
from optparse import OptionParser

# -----------------------------------------------------------------------------
def main():
  """This script reads RIS files and extracts found ISBN identifiers."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing RIS records from Endnote')
  #parser.add_option('-o', '--output-file', action='store', help='The output CSV with ISBN identifiers')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) ):# or (not options.output_file) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  with open(options.input_file, 'r') as inFile:
#       open(options.output_output_file, 'w') as outFile:

    print(f'Reading entries from {options.input_file}')
    numberEntries = 0
    entries = rispy.load(inFile)
    for e in entries:
      print(e)
      numberEntries += 1

    print(f'Successfully read {numberEntries} entries!')

main()
