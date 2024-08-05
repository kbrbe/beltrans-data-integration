import argparse
import csv
import re
import os
from io import StringIO

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+', help="Input text file containing statistics that need to be reformatted")
options = parser.parse_args()

for inputFile in options.files:

  basenameWithPath = os.path.splitext(inputFile)[0]
  outputFilename = basenameWithPath + '.csv'

  with open(inputFile, 'r') as inFile, \
       open(outputFilename, 'w') as outFile:
    statsTxt = "variable,value\n" + inFile.read()

    # bring the value on the same row as the variable name
    statsTxt = statsTxt.replace('\n\t', ',')

    inputReader = csv.DictReader(StringIO(statsTxt))
    outputWriter = csv.DictWriter(outFile, fieldnames=inputReader.fieldnames)

    outputWriter.writeheader()
    for row in inputReader:

      # some rows with more sophisticated stats contain commas that are not escaped
      # the csv library will put all additional columns into a single column with value None
      # let's take the actual amount and skip the min/max/average
      if None in row:
        amountString = row[None][2]
        row['value'] = re.findall(r'\d+', amountString)[0]
        del row[None]
      outputWriter.writerow(row)
