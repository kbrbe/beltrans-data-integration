#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
from tools import utils
from optparse import OptionParser

# -----------------------------------------------------------------------------
def main():
  """This script reads a CSV file containing X columns, but from which only Y columns define a row and thus X minus Y columns are functionaly dependent on X.
     A new CSV will be created by the script which creates one x->y relationship per line.
     For example, a CSV with the columns "A,B,C,d,e,f,g" where d,e,f and g are functionally dependent on A,B,C will result
     in a CSV with the following 3 rows: "A,B,C,d", "A,B,C,e", "A,B,C,f", "A,B,C,g".
     The initial use case are Unimarc exports from the BnF catalogue where one row is a book translation and if the translation is based on a compilation of different books,
     each original book is mentioned in a different column. Hence there is a variable number of columns, for example "translationURI, BnFID, bookType, originalTitle",
     but with more columns if there is more than 1 originalTitle.
  """

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The name of the CSV file with unnormalized data')
  parser.add_option('-o', '--output-file', action='store', help='The name of the CSV file in which the 1:N resolved normalize data should be stored')
  parser.add_option('-n', '--number-of-columns', type='int', action='store', help='The number of columns which should remain, for all other columns a new row will be created')
  parser.add_option('-d', '--delimiter', action='store', default=',', help='The optional delimiter of the input CSV, default is a comma')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if (not options.input_file) or (not options.output_file) or (not options.number_of_columns):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r') as inFile, \
       open(options.output_file, 'w') as outFile:

    # a DictReader also works, it would put all additional columns in an array under the key 'None'
    # But in our initial use case we even have a column with value but without heading
    inputReader = csv.reader(inFile, delimiter=options.delimiter)

    # create a CSV writer for all columns of the input
    outputWriter = csv.writer(outFile, delimiter=options.delimiter)

    # only write non-empty header values to the output
    outputHeader = [ val for val in next(inputReader) if val != '']
    outputWriter.writerow(outputHeader)

    for row in inputReader:
      if options.number_of_columns < len(row):
        fixedColumns = row[:options.number_of_columns]
        additionalColumns = row[options.number_of_columns:]
        for col in additionalColumns:
          if col != '':
            outputWriter.writerow(fixedColumns + [col])

main()
