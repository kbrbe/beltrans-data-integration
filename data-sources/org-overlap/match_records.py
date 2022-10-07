#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import os
import csv
from optparse import OptionParser

import sys
sys.path.insert(1, '../../data-integration')

import utils
import utils_string

# -----------------------------------------------------------------------------
def parseArguments():

    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('--file1', action='store', help='The name of the first file whose content is tried to be matched with the second file')
    parser.add_option('--file2', action='store', help='The name of the second file whose content is tried to be matched with the first file')
    parser.add_option('--match-column1', action='store', help='The name of the columnn of the first file used for matching')
    parser.add_option('--match-column2', action='store', help='The name of the columnn of the seconf file used for matching')
    parser.add_option('--output-column1', action='append', help='The name of a column which should be added from the first file to the output, this argument can be provided several times')
    parser.add_option('--output-column2', action='append', help='The name of a column which should be added from the second file to the output, this argument can be provided several times')
    parser.add_option('--file1-label', action='store', default='file1', help='A prefix for column names of the first file to be used in the column names of the output file')
    parser.add_option('--file2-label', action='store', default='file2', help='A prefix for column names of the second file to be used in the column names of the output file')
    parser.add_option('-o', '--output', action='store', help='The name of the correlation list CSV file')

    (options, args) = parser.parse_args()

    if (not options.file1) or (not options.file2) or (not options.match_column1) \
       or (not options.match_column2) or (not options.output) \
       or (not options.output_column1) or (not options.output_column2):
        parser.print_help()
        exit(1)

    return (options, args)

# -----------------------------------------------------------------------------
def main(file1, file2, outputFile, matchColumn1, matchColumn2, file1OutputColumns, file2OutputColumns, file1Label, file2Label):

    with open(file1, 'r') as file1In, \
         open(file2, 'r') as file2In, \
         open(outputFile, 'w') as outFile:

        file1Reader = csv.DictReader(file1In)
        file2Reader = csv.DictReader(file2In)

        # check if all needed columns exist (all requested ones including the matching column itself)
        utils.checkIfColumnsExist(file1Reader.fieldnames, file1OutputColumns + [matchColumn1]) 
        utils.checkIfColumnsExist(file2Reader.fieldnames, file2OutputColumns + [matchColumn2]) 

        # create a list of output columns (column names are prefixed with their source label)
        outputColumns1 = [ file1Label + '-' + c for c in file1OutputColumns]
        outputColumns2 = [ file2Label + '-' + c for c in file2OutputColumns]
        outputFieldnames = [file1Label, file2Label] + outputColumns1 + outputColumns2

        outputWriter = csv.DictWriter(outFile, fieldnames=outputFieldnames)

        # Create a lookup list based on the first file
        lookup = {}
        lookupOriginalNames = {}
        for row in file1Reader:
            name = row[matchColumn1]
            nameNormalized = utils_string.getNormalizedString(name) 
            lookup[nameNormalized] = row 
            lookupOriginalNames[nameNormalized] = name

        # Check if (normalized) names of the second file are present in the first
        outputWriter.writeheader()
        numberMatches = 0
        for row in file2Reader:
            name = row[matchColumn2]
            nameNormalized = utils_string.getNormalizedString(name) 
            if nameNormalized in lookup:
                outputRow = {}
                outputRow[file1Label] = lookupOriginalNames[nameNormalized]
                outputRow[file2Label] = name
                ## add wanted columns from the first file
                file1Values = lookup[nameNormalized]
                for c in file1OutputColumns:
                    outputRow[file1Label + '-' + c] = file1Values[c]
                ## add wanted columns from the second file
                for c in file2OutputColumns:
                    outputRow[file2Label + '-' + c] = row[c]

                outputWriter.writerow(outputRow)
                numberMatches += 1

        print(f'Found {numberMatches} matches!')

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    (options, args) = parseArguments()
    main(options.file1, options.file2, options.output, options.match_column1, options.match_column2, options.output_column1, options.output_column2, options.file1_label, options.file2_label)

