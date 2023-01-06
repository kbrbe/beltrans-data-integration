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
  options = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.output_file) or (not options.input_folder) ):
    parser.print_help()
    exit(1)

  inputFolder = options.input_folder
  outputFilename = options.output_file

  if not os.path.isdir(inputFolder):
    print(f'The given input folder does not exist: "{inputFolder}"')

  records = []
  foundFields = set(['id'])

  # try to parse each file found in the input directory
  for filename in os.listdir(inputFolder):
    
    with open(os.path.join(inputFolder, filename), 'r') as fIn:
      htmlString = fIn.read()
      newRecords = lib.getStructuredRecord(htmlString, foundFields)
      if newRecords:
        records.extend(newRecords)
      else:
        print(f'Issue for file {filename}, no records found!')


  # it is difficult to immediately write parsed content in a streaming fashion
  # because we do not yet know all possible headers
  # Therefore we store all parsed content in the records variable
  # and write it to a file after all the input was parsed
  with open(outputFilename, 'w', encoding='utf-8') as outFile:
    outputWriter = csv.DictWriter(outFile, fieldnames=foundFields)
    outputWriter.writeheader()
    outputWriter.writerows(records)
      


main()
