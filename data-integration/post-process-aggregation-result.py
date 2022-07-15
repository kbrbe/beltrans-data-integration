#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import json
import integration

# -----------------------------------------------------------------------------
def main():
  """This script filters the SPARQL query result of the aggregated integrated data."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-k', '--input-file-kbr', action='store', help='The input file containing CSV data from KBR')
  parser.add_option('-b', '--input-file-bnf', action='store', help='The input file containing CSV data from BnF')
  parser.add_option('-o', '--output-file', action='store', help='The file in which content with new headers is stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file_kbr) or (not options.input_file_bnf) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  integration.combineAggregatedResults(options.input_file_kbr, options.input_file_bnf, options.output_file)

main()
