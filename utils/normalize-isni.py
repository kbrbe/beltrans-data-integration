#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import re
from optparse import OptionParser

# -----------------------------------------------------------------------------
def main():
  """This script reads a CSV file with ISNI identifiers and replaces them with normalized ISNI identifiers (space-separated digits)."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The name of the file containing ISNI identifiers')
  parser.add_option('-o', '--output-file', action='store', help='The name of the file in which the normalized ISNI identifiers are stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if ( (not options.input_file) or (not options.output_file) ):
    parser.print_help()
    exit(1)


  with open(options.input_file, 'r') as fIn, \
       open(options.output_file, 'w') as fOut:

    pattern = '.*"ISNI (.*)".*'
    inputReader = fIn.readlines()
    for row in inputReader:
      m = re.match(pattern, row)
      unformattedISNI = m.group(1)
      formattedISNI = f'{unformattedISNI[0:4]} {unformattedISNI[4:8]} {unformattedISNI[8:12]} {unformattedISNI[12:16]}'
      #newRow = re.sub(pattern, formattedISNI, row)
      fOut.write(f'"ISNI {formattedISNI}",\n')

main()
