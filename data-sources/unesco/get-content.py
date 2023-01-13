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
class ParseDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        d = getattr(namespace, self.dest) or {}

        if values:
            for item in values:
                split_items = item.split("=", 1)
                key = split_items[
                    0
                ].strip()  # we remove blanks around keys, as is logical
                value = split_items[1]

                d[key] = value

        setattr(namespace, self.dest, d)


# -----------------------------------------------------------------------------
def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('-u', '--url', action='store', help="The URL from which content should be retrieved")
  parser.add_argument('-m', '--number-records', action='store', type=int, help='The number of records which are requested in total')
  parser.add_argument('-r', '--number-results-per-page', action='store', type=int, help='The number of search entries in a page')
  parser.add_argument('-w', '--waiting-time', action='store', type=int, default=2, help='The number of seconds between API requests, default is 2')
  parser.add_argument('-o', '--output-folder-prefix', action='store', help='The name of the folder in which fetched HTML pages should be stored')
  parser.add_argument('--params', metavar='KEY=VALUE', nargs='+', action=ParseDict)
  options = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.output_folder_prefix) or (not options.url) or (not options.number_records) or (not options.number_results_per_page) ):
    parser.print_help()
    exit(1)


  url = options.url
  urlParameters = options.params
  numberRecords = options.number_records
  numberResultsPerPage = options.number_results_per_page
  secondsBetweenRequests = options.waiting_time

  # Create an output folder where fetched content will be stored
  outputFolderName = options.output_folder_prefix + '_' + lib.getOutputFolderName(options.params)
  os.makedirs(outputFolderName)

  request = requests.Session()
  records = []
  foundFields = set(['id'])
  for i in tqdm(range(0, numberRecords, numberResultsPerPage)):
    response = request.get(url, params=urlParameters)

    # store fetched content
    with open(os.path.join(outputFolderName, f'results_{i}-{numberRecords}.html'), 'wb') as fOut:
      fOut.write(response.content)
    urlParameters['fr'] = i
    time.sleep(secondsBetweenRequests)


main()
