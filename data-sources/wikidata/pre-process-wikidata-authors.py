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

  # Get the date value but without the last character, e.g. 2020-10-04 instead of 2020-10-04_
  value = row[sourceColumn]

  if( isinstance(value, str) ):

    # Ignore rows in which dashes are used to indicate 'empty'
    if(str.startswith(value, '--')):
      pass
    else:

      value = value[:-1]
      # Try to parse the date either as '2021-08-11' or '20210811'
      try:
        return datetime.strptime(value, '%Y-%m-%d').date()
      except:

        try:
          return datetime.strptime(value, '%Y%m%d').date()

        except ValueError:
          if( '..' in value):
            print("Incomplete date (" + sourceColumn + ") for '" + row['Nom complet'] + "': '" + value + "'")
          elif( str.endswith(value, '--')):
            print("Incomplete date (" + sourceColumn + ") for '" + row['Nom complet'] + "': '" + value + "'")
          else:
            print("Unknown format (" + sourceColumn + ") for '" + row['Nom complet'] + "': '" + value + "'")
  elif (math.isnan(value)):
    pass


def getNonEmptyRowPercentage(df, column):
  """This function counts the number of non empty cells of df[column] and returns the percentage based on the total number of rows."""
  notEmpty = df[column].notnull().sum()
  return (notEmpty*100)/len(df.index)


def getPatternPercentage(df, column, pattern):
  """This function counts the number of df[column] which have the given pattern and returns the percentage based on the total number of rows."""
  found = df.apply(lambda x: True if(isinstance(x[column], str) and x[column].startswith(pattern)) else False, axis=1).sum()
  return (found*100)/len(df.index)


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
  inputCSV.index.name="rowID"

  #
  # clean KBR identifier, sometimes its empty sometimes with question mark, it should be empty if not known
  #
  inputCSV['KBR Identifiant'] = inputCSV['KBR Identifiant'].str.replace('?', '')

  #
  # clean birth/death date column
  #
  inputCSV['birth_date'] = inputCSV.apply(lambda row: getNormalizedDate(row, 'Date de naissance'), axis=1)
  inputCSV['death_date'] = inputCSV.apply(lambda row: getNormalizedDate(row, 'Date de décès'), axis=1)

  print("birth dates as number with t prefix: " + str( getPatternPercentage(inputCSV, 'Date de naissance', 't')) + "%")
  print("death dates as number with t prefix: " + str( getPatternPercentage(inputCSV, 'Date de décès', 't' )) + "%")
  print("parsed birth dates (Date de naissance): " + str( getNonEmptyRowPercentage(inputCSV, 'birth_date') ) + "%")
  print("parsed death dates (Date de décès): " + str( getNonEmptyRowPercentage(inputCSV, 'death_date') ) + "%")

  inputCSV.to_csv(options.output_file, sep=options.delimiter, encoding="utf-8", index=True)

main()
