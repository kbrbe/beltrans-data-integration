#
# (c) 2021 Sven Lieber
# KBR Brussels
#
from optparse import OptionParser
import pandas as pd
import math
from datetime import datetime


def getNormalizedDate(row, sourceColumn):
  """This function takes a data frame containing a date in 'sourceColumn', normalizes the date value and returns it."""

  value = row[sourceColumn]

  if( isinstance(value, str) ):

    # Ignore rows in which dashes are used to indicate 'empty'
    if(str.startswith(value, '--')):
      pass
    else:

      # Try to parse the date either as '2021-08-11' or '20210811'
      try:
        return datetime.strptime(value, '%Y-%m-%d').date()
      except:

        try:
          return datetime.strptime(value, '%Y%m%d').date()

        except ValueError:
          if( '..' in value):
            print("Incomplete date (" + sourceColumn + ") for '" + row['AFAE'] + "': '" + value + "'")
          elif( str.endswith(value, '--')):
            print("Incomplete date (" + sourceColumn + ") for '" + row['AFAE'] + "': '" + value + "'")
          else:
            print("Unknown format (" + sourceColumn + ") for '" + row['AFAE'] + "': '" + value + "'")
  else:
    pass


def main():
  """This script performs pre processing before the data can be mapped to RDF, e.g. by adding a given_name and family_name column based on a split on the AFAE column."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing CSV data')
  parser.add_option('-d', '--delimiter', action='store', help='The delimiter of the input file')
  parser.add_option('-o', '--output-file', action='store', help='The file in which content with new headers is stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) or (not options.delimiter) ):
    parser.print_help()
    exit(1)

  inputCSV = pd.read_csv(options.input_file, sep=options.delimiter, encoding="utf-8-sig");

  #
  # create new given name and family name columns based on a split on the full name column
  #
  inputCSV['family_name'] = inputCSV['AFAE'].str.split(',').apply(lambda x: [ e.strip() for e in x]).str[0]
  inputCSV['given_name'] = inputCSV['AFAE'].str.split(',').apply(lambda x: [ e.strip() for e in x]).str[1]

  #
  # clean birth/death date column
  #
  inputCSV['birth_date'] = inputCSV.apply(lambda row: getNormalizedDate(row, 'F046'), axis=1)
  inputCSV['death_date'] = inputCSV.apply(lambda row: getNormalizedDate(row, 'G046'), axis=1)

  inputCSV.to_csv(options.output_file, sep=options.delimiter, encoding="utf-8", index=False)

main()
