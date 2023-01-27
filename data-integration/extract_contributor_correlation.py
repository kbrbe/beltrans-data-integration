#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
from integrated_contributors import ContributorLookup
import utils_string
import utils


# -----------------------------------------------------------------------------
def checkArguments():
  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input', action='store', help='Input CSV file')
  parser.add_option('-o', '--output', action='store', help='Second CSV file')
  parser.add_option('--column', action='store',
                    help='column name of the CSV in which it is checked for missing contributor overlap')
  parser.add_option('--csv-delimiter', action='store', default=',', help='Delimiter of the input CSV, default is a comma')
  parser.add_option('--column-value-delimiter', action='store', default=';', help='Delimiter used within a column to separate different names we want to compare')

  (options, args) = parser.parse_args()

  if (not options.input) or (not options.output) or (not options.column):
    print(f'Input and output data as well as a column name are needed')
    parser.print_help()
    exit(1)

  return options, args
   
# -----------------------------------------------------------------------------
def main(inputFile, outputFile, columnName, csvDelimiter, columnValueDelimiter):
  """This script reads a CSV files and checks if parts of the value in a given column occur more than once in the column.
     For example "Sven Lieber (int1: abc, def); Lieber, Sven (int2: abc)" where the first name but also the last name occur twice."""

  with open(inputFile, 'r') as inFile:

    inputReader = csv.DictReader(inFile, delimiter=csvDelimiter)

    contributorLookup = ContributorLookup(integratedIdentifierDelimiter=':', localIdentifierDelimiter=',')

    for row in inputReader:
      contributorIdentifiersOfThisRow = []
      columnValue = row[columnName]
      # we may have "name1 (intID1: id1, idn) ; name2 (intID2: id2, idn)" and split in this example by ';' to treat each name-ids combination seperately
      values = columnValue.split(columnValueDelimiter)

      if len(values) > 1:
        valueNameParts = []
        for value in values:
          contributorID = contributorLookup.addContributor(value)
          contributorIdentifiersOfThisRow.append(contributorID)
        posssibleMatchesInThisRow = contributorLookup.computePossibleMatches(contributorIdentifiersOfThisRow)


  with open(outputFile, 'w') as outFile:

    outputFieldnames = contributorLookup.getLocalIdentifierNames()
    outputWriter = csv.DictWriter(outFile, fieldnames=['name'] + outputFieldnames, delimiter=csvDelimiter)

    outputWriter.writeheader()

    numberRows = 0
    for possibleMatch in contributorLookup.getCorrelationsLocalIdentifiers():
      outputWriter.writerow(possibleMatch)
      numberRows += 1

    print(f'Successfully wrote {numberRows} output rows!')

if __name__ == '__main__':
  (options, args) = checkArguments()
  main(options.input, options.output, options.column, options.csv_delimiter, options.column_value_delimiter)

