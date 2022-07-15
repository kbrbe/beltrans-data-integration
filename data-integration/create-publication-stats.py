#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import pandas as pd
import numpy as np
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
def getStatsPerLanguage(column, df, dfAgg):

  #
  # Translations per column value combination (it is aggregated thus per unique combination of values in that column)
  #
  aggRelevant = dfAgg[[column, 'targetTextLanguage']]
  trlPerCombo = aggRelevant.pivot_table(index=column, columns='targetTextLanguage', aggfunc='size', fill_value=0)
  trlPerCombo.loc['TOTAL'] = trlPerCombo.sum()

  #
  # Translations per column single value
  #
  relevant = df[['targetTextKBRIdentifier', 'targetTextBnFIdentifier', column, 'targetTextLanguage']]
  # We need the identifier of the translation to eliminate duplicate trl-column relationships, but therefore we require an ID column
  # take the KBR identifier as identifier and if there is non take the BnF identifier
  relevant.loc[:,'rowID'] = relevant.loc[:,'targetTextKBRIdentifier'].fillna(relevant.loc[:,'targetTextBnFIdentifier'])
  #relevant.assign('rowID'=np.where(relevant['targetTextKBRIdentifier'].isnull(), relevant['targetTextBnFIdentifier'], relevant['targetTextKBRIdentifier']))
  #relevant.loc[:,'rowID'] = np.where(relevant['targetTextKBRIdentifier'].isnull(), relevant['targetTextBnFIdentifier'], relevant['targetTextKBRIdentifier'])

  # only the keep the new ID column and the value columns and then remove duplicates
  relevantAllID = relevant[['rowID', column, 'targetTextLanguage']]
  relevantAllUnique = relevantAllID.drop_duplicates()

  # for debugging the creation of rowIDs and the removal of duplicates
  # writer = pd.ExcelWriter(f'input_{column}.xlsx', engine='xlsxwriter')
  # relevantAllUnique.to_excel(writer, sheet_name=column)
  # writer.close()

  trlPerValue = relevantAllUnique.pivot_table(index=column, columns='targetTextLanguage', aggfunc='size', fill_value=0)
  trlPerValue.loc['TOTAL'] = trlPerValue.sum()

  return (trlPerCombo, trlPerValue)

# -----------------------------------------------------------------------------
def writeToExcelWorksheetTable(df, writer, sheetname):


  df.to_excel(writer, sheet_name=sheetname)

#  df.to_excel(writer, sheet_name=sheetname, startrow=1, header=False, index=False)
#  workbook = writer.book
#  worksheet = writer.sheets[sheetname]

#  (max_row, max_col) = df.shape

#  column_settings = [{'header': column} for column in df.columns]

#  print(column_settings)
#  worksheet.add_table(0, 0, max_row, max_col -1, {'columns': column_settings})
#  worksheet.set_column(0, max_col -1, 12)
#  writer.save()

# -----------------------------------------------------------------------------
def main():
  """This script creates statistics based on the input CSV file."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The CSV file over which statistics will be made')
  parser.add_option('-a', '--input-file-aggregated', action='store', help='The CSV file, already aggregated per translation, over which statistics will be made')
  parser.add_option('-o', '--output-file', action='store', help='The Excel file in which content is stored')
  parser.add_option('-d', '--dtype-file', action='store', help='A CSV with a mapping between input CSV columns and pandas data types')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if ( (not options.input_file) or (not options.output_file) or (not options.input_file_aggregated)  or (not options.dtype_file) ):
    parser.print_help()
    exit(1)

  dtypes = getDataTypes(options.dtype_file)
  df = pd.read_csv(options.input_file, dtype=dtypes)
  dfAgg = pd.read_csv(options.input_file_aggregated)

  writer = pd.ExcelWriter(options.output_file, engine='xlsxwriter')

  #
  # Translations per year
  #
  (trlPerYearCombo, trlPerYear) = getStatsPerLanguage('targetTextYearOfPublication', df, dfAgg)
  writeToExcelWorksheetTable(trlPerYearCombo, writer, 'perYearCombo')
  writeToExcelWorksheetTable(trlPerYear, writer, 'perYear')

  #
  # Translation per country combination
  #
  (trlPerCountryCombo, trlPerCountry) = getStatsPerLanguage('targetTextCountryOfPublication', df, dfAgg)
  writeToExcelWorksheetTable(trlPerCountryCombo, writer, 'perCountryCombo')
  writeToExcelWorksheetTable(trlPerCountry, writer, 'perCountry')

  #
  # Translation per location combination
  #
  (trlPerLocationCombo, trlPerLocation) = getStatsPerLanguage('targetTextPlaceOfPublication', df, dfAgg)
  writeToExcelWorksheetTable(trlPerLocationCombo, writer, 'perPlaceCombo')
  writeToExcelWorksheetTable(trlPerLocation, writer, 'perPlace')


  # Translations per publisher combination (from aggregated data)
  (trlPerPublisherCombo, trlPerPublisher) = getStatsPerLanguage('targetPublisherIdentifier', df, dfAgg)
  writeToExcelWorksheetTable(trlPerPublisherCombo, writer, 'perPublisherCombo')
  writeToExcelWorksheetTable(trlPerPublisher, writer, 'perPublisher')

  # todo: translations per source
  
  writer.save()

  #wb = xlsxwriter.Workbook(options.output_file)

#  for filename in args:
#    with open(filename, 'r', encoding="utf-8") as inFile:

#      inputReader = csv.reader(inFile, delimiter=',')
#      sheet = wb.add_worksheet(options.sheet_names.pop(0))

#      for r, row in enumerate(inputReader):
#        for c, val in enumerate(row):
#          sheet.write(r, c, val)

#  wb.close()

main()
