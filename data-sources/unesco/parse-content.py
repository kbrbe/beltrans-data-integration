import requests
import os
from dotenv import load_dotenv
from datetime import date
from tqdm import tqdm
import logging
import time
import csv
import urllib
from io import BytesIO
import argparse
import lib


# -----------------------------------------------------------------------------
def parseFile(filename, foundFields, records, isbn10Records, isbn13Records, contributionRecords):
  """This function parses a single file."""

  with open(filename, 'r') as fIn:

    htmlString = fIn.read()
    (newRecords, newISBN10Relations, newISBN13Relations, newContributionRelations) = lib.getStructuredRecord(htmlString, foundFields)

    if newRecords:
      records.extend(newRecords)
    else:
      print(f'Issue for file {filename}, no records found!')

    if newISBN10Relations:
      isbn10Records.extend(newISBN10Relations)

    if newISBN13Relations:
      isbn13Records.extend(newISBN13Relations)

    if newContributionRelations:
      contributionRecords.extend(newContributionRelations)



# -----------------------------------------------------------------------------
def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input-folder', action='store', help="The folder in which HTML files are stored which should be parsed")
  parser.add_argument('-o', '--output-file', action='store', help='The name of the output CSV file containing the parsed content')
  parser.add_argument('--isbn10-file', action='store', help='The name of the output CSV file containing 1:n relations between translations and ISBN 10 identifiers')
  parser.add_argument('--isbn13-file', action='store', help='The name of the output CSV file containing 1:n relations between translations and ISBN 13 identifiers')
  parser.add_argument('--contribution-file', action='store', help='The name of the output CSV file containing 1:n relations between translations and contributors')
  parser.add_argument('input', nargs='+')
  options = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if not options.input:
    print(f'No input given! Input folders or files have to be given as arguments')
    parser.print_help()
    exit(1)

  if( (not options.output_file) or (not options.isbn10_file) or (not options.isbn13_file) or (not options.contribution_file) ):
    parser.print_help()
    exit(1)

  outputFilename = options.output_file
  isbn10Filename = options.isbn10_file
  isbn13Filename = options.isbn13_file
  contributionFilename = options.contribution_file


  # declaring data structures to keep (counts of) parsed content
  records = []
  isbn10Records = []
  isbn13Records = []
  contributionRecords = []
  foundFields = set(['id'])

  # try to parse each file or folder given via arguments
  for fileOrFolder in options.input:
    
    if os.path.isdir(fileOrFolder):
      print(f'Processing directory "{fileOrFolder}"')
      for filename in os.listdir(fileOrFolder):
        #print(f'Processing file "{filename}" of directory "{fileOrFolder}"')
        parseFile(os.path.join(fileOrFolder, filename), foundFields, records, isbn10Records, isbn13Records, contributionRecords)
    elif os.path.isfile(fileOrFolder):
      print(f'Processing file "{fileOrFolder}"')
      parseFile(fileOrFolder, foundFields, records, isbn10Records, isbn13Records, contributionRecords)
    else:
      print(f'Skipping "{fileOrFolder}", it is not a directory nor a file!')

  # it is difficult to immediately write parsed content in a streaming fashion
  # because we do not yet know all possible headers
  # Therefore we store all parsed content in the records variable
  # and write it to a file after all the input was parsed
  with open(outputFilename, 'w', encoding='utf-8') as outFile, \
       open(isbn10Filename, 'w') as isbn10Out, \
       open(isbn13Filename, 'w') as isbn13Out, \
       open(contributionFilename, 'w') as contributionOut:

    outputWriter = csv.DictWriter(outFile, fieldnames=foundFields)
    outputWriter.writeheader()
    outputWriter.writerows(records)
      
    isbn10Writer = csv.DictWriter(isbn10Out, fieldnames=['id', 'isbn10'])
    isbn13Writer = csv.DictWriter(isbn13Out, fieldnames=['id', 'isbn13'])
    contributionWriter = csv.DictWriter(contributionOut, fieldnames=['contributorID', 'id', 'contributorType', 'type', 'name', 'firstname', 'place'])

    isbn10Writer.writeheader()
    isbn13Writer.writeheader()
    contributionWriter.writeheader()

    isbn10Writer.writerows(isbn10Records)
    isbn13Writer.writerows(isbn13Records)
    contributionWriter.writerows(contributionRecords)


main()
