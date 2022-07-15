#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import pandas as pd
import numpy as np
import utils
import json
import xlsxwriter

# -----------------------------------------------------------------------------
def getDataTypes(filename):
  """This function reads the given filename as CSV where the first column will be a column name and the second the datatype."""
  types = {}
  with open(filename, 'r') as dTypeIn:
    dtypeReader = csv.reader(dTypeIn, delimiter=',')
    for row in dtypeReader:
      types[row[0]] = row[1]
  return types

# -----------------------------------------------------------------------------
def main():
  """This script extracts unique contributors from the given CSV about publications."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The CSV file containing one contributor publication relationship per row')
  parser.add_option('-o', '--output-file', action='store', help='The CSV file in which contributor information is stored')
  parser.add_option('-d', '--dtype-file', action='store', help='A CSV with a mapping between input CSV columns and pandas data types')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if ( (not options.input_file) or (not options.output_file) or (not options.dtype_file) ):
    parser.print_help()
    exit(1)

  dtypes = getDataTypes(options.dtype_file)
  df = pd.read_csv(options.input_file, dtype=dtypes)

  contributorColumns = ['KBRIdentifier', 'BnFIdentifier', 'ISNI', 'Nationality', 'Gender', 'FamilyName', 'GivenName', 'BirthDate', 'DeathDate']
  # get data of all authors

  authorData = utils.getContributorData(df, 'author', contributorColumns)
  authorData = authorData.drop_duplicates()

  translatorData = utils.getContributorData(df, 'translator', contributorColumns)
  translatorData = translatorData.drop_duplicates()

  illustratorData = utils.getContributorData(df, 'illustrator', contributorColumns)
  illustratorData = illustratorData.drop_duplicates()

  scenaristData = utils.getContributorData(df, 'scenarist', contributorColumns)
  scenaristData = scenaristData.drop_duplicates()

  contributorData = pd.concat([authorData, translatorData, illustratorData, scenaristData])
  contributorData = contributorData.drop_duplicates()

  contributorData.to_csv(options.output_file, index=False)

  # The number of translations can be determined in the following way (cross checked with existing result of a SPARQL query to be correct) (but only works if a publication related rowID is still int he data frame, i.e. including targetTextKBRIdentifier and targetTextBnFIdentifier in the initial selection and create a rowID with the following statement
  #authorData['rowID'] = authorData['targetTextKBRIdentifier'].fillna(authorData['targetTextBnFIdentifier'])
  #authorData = authorData.drop(['targetTextKBRIdentifier', 'targetTextBnFIdentifier'], axis=1)

  # however, does not work like this if we have authors from several data sources, thus this code is currently not in use
  #authorData['values'] = 1
  #authorData['numberAuthored'] = authorData.groupby('authorIdentifier')['values'].transform(np.sum)


if __name__ == '__main__':
  main()
