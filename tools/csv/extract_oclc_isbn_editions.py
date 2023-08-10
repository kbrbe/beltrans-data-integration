import os
import csv
import argparse
import ast
from tools import utils
import stdnum.exceptions

# -----------------------------------------------------------------------------
def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input-file', required=True, action='store', help="The CSV file with book information, one row is one work or expression")
  parser.add_argument('-o', '--output-file', required=True, action='store', help='The name of the output CSV file where one row will be one manifestation')
  parser.add_argument('--id-column', required=True, action='store', help='The name of the book identifier column (work or expression level)')
  parser.add_argument('--isbn-column', required=True, action='store', help="The name of the column with ISBN information encoded as array")
  options = parser.parse_args()


  inputFilename = options.input_file
  outputFilename = options.output_file
  idColumn = options.id_column
  isbnColumn = options.isbn_column

  if not os.path.isfile(inputFilename):
    print(f'The given input file does not exist: "{inputFilename}"')


  with open(inputFilename, 'r') as fIn, \
       open(outputFilename, 'w') as fOut:

    inputReader = csv.DictReader(fIn)
    fieldnames = inputReader.fieldnames

    utils.checkIfColumnsExist(fieldnames, [isbnColumn, idColumn])

    outputWriter = csv.DictWriter(fOut, fieldnames=[idColumn, 'isbn-10', 'isbn-13'])
    outputWriter.writeheader()

    stats = {
      'numberRows': 0,
      'numberUnevenLength': 0,
      'singleISBN13WithPrefix979': 0
    }
    for row in inputReader:
      rowID = row[idColumn]
      isbnValuesString = row[isbnColumn]

      if isbnValuesString != '':
        isbnValues = ast.literal_eval(isbnValuesString) if isbnValuesString.startswith('[') else [isbnValuesString]
        try:
          isbnPairs = utils.getOCLCISBNPairs(isbnValues)
          for pair in isbnPairs:
            outputWriter.writerow({idColumn: rowID, 'isbn-10': pair[0], 'isbn-13': pair[1]})
        except stdnum.exceptions.InvalidFormat:
          print(f'One of the following ISBNs is invalid ({rowID}): {isbnValues}')

      stats['numberRows'] += 1

    print(stats)


main()
