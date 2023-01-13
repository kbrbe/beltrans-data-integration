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
def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input-folder', action='store', help="The folder in which HTML files are stored which should be parsed")
  parser.add_argument('-o', '--output-file', action='store', help='The name of the output CSV file containing the parsed content')
  parser.add_argument('--isbn10-file', action='store', help='The name of the output CSV file containing 1:n relations between translations and ISBN 10 identifiers')
  parser.add_argument('--isbn13-file', action='store', help='The name of the output CSV file containing 1:n relations between translations and ISBN 13 identifiers')
  parser.add_argument('--contribution-file', action='store', help='The name of the output CSV file containing 1:n relations between translations and contributors')
  options = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.output_file) or (not options.input_folder) or (not options.isbn10_file) or (not options.isbn13_file) or (not options.contribution_file) ):
    parser.print_help()
    exit(1)

  inputFolder = options.input_folder
  outputFilename = options.output_file
  isbn10Filename = options.isbn10_file
  isbn13Filename = options.isbn13_file
  contributionFilename = options.contribution_file

  if not os.path.isdir(inputFolder):
    print(f'The given input folder does not exist: "{inputFolder}"')

  records = []
  isbn10Records = []
  isbn13Records = []
  contributionRecords = []
  foundFields = set(['id'])

  # try to parse each file found in the input directory
  for filename in os.listdir(inputFolder):
    
    with open(os.path.join(inputFolder, filename), 'r') as fIn:


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
    contributionWriter = csv.DictWriter(contributionOut, fieldnames=['id', 'contributorType', 'type', 'name', 'firstname', 'place'])

    isbn10Writer.writeheader()
    isbn13Writer.writeheader()
    contributionWriter.writeheader()

    isbn10Writer.writerows(isbn10Records)
    isbn13Writer.writerows(isbn13Records)
    contributionWriter.writerows(contributionRecords)


main()
