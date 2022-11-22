#
# (c) 2022 Sven Lieber
# KBR Brussels
#
from tools import utils
from tools.date import utils_date
import csv
from optparse import OptionParser

# -----------------------------------------------------------------------------
def parseArguments():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('-i', '--input-file', action='store', help='The CSV file containing different date columns which should be compared')
    parser.add_option('-o', '--output-file', action='store', help='The CSV file in which the conflicting date information will be stored')
    parser.add_option('--date-column', action='append', help='The name of a date column, this parameter can be repeated for all available date columns')
    parser.add_option('--output-column', action='append', help='The name of an additional column which should be added to the output, this parameter can be repeated for more columns')
    (options, args) = parser.parse_args()

    if (not options.input_file) or (not options.output_file) or (not options.date_column) or (not options.output_column):
        parser.print_help()
        exit(1)

    return (options, args)

# -----------------------------------------------------------------------------
def main(inputFilename, outputFilename, dateColumns, outputColumns):

    with open(inputFilename, 'r', encoding='utf-8') as inFile, \
         open(outputFilename, 'w', encoding='utf-8') as outFile:

        csvDelimiter = ','
        inputReader = csv.DictReader(inFile, delimiter=csvDelimiter)

        wantedColumns = dateColumns + outputColumns
        utils.checkIfColumnsExist(inputReader.fieldnames, wantedColumns)

        outputWriter = csv.DictWriter(outFile, fieldnames=wantedColumns, delimiter=csvDelimiter)
        outputWriter.writeheader()

        for row in inputReader:
            date_values = [ row[index] for index in dateColumns ]
            mostCompleteDate = utils_date.mostCompleteDate(date_values)

            if 'or' in mostCompleteDate:
                outputRow = { key: row[key] for key in wantedColumns }
                outputWriter.writerow(outputRow)

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  (options, args) = parseArguments()
  main(options.input_file, options.output_file, options.date_column, options.output_column)

