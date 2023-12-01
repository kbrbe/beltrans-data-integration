#
# (c) 2023 Sven Lieber
# KBR Brussels
#
import csv
from tools import utils
from argparse import ArgumentParser
from tools.xml.KBRZ3950APIHandler import KBRZ3950APIHandler as kbrAPI
import lxml.etree as ET
from tqdm import tqdm

# -----------------------------------------------------------------------------
def main(queryString, outputFilename, url, batchSize):
  """This script takes a Z3950 query and launches it against the provided URL."""

  apiHandler = kbrAPI(url)
  apiHandler.setBatchSize(batchSize)

  with open(outputFilename, 'wb') as outFile:

    outFile.write(b'<collection xmlns="http://www.loc.gov/MARC21/slim">')

    apiHandler.query(queryString)
    numberOfResults = apiHandler.numberResults() # this should be equal to the number of items the batch

    # fetch results of the query in batch
    #
    for record in tqdm(apiHandler.getRecords(), total=numberOfResults, desc='Batches'):
      outFile.write(ET.tostring(record))

    outFile.write(b'</collection>')

def parseArguments():

  parser = ArgumentParser()
  parser.add_argument('-q', '--query', action='store', required=True, help='The query that should be executed')
  parser.add_argument('-o', '--output-file', action='store', required=True, help='The name of the CSV file in which the extrated data is stored')
  parser.add_argument('-b', '--batch-size', action='store', type=int, default=200, help="The number of identifiers per request")
  parser.add_argument('-u', '--url', action='store', required=True, help='The URL of the Z3950 KBR API')
  options = parser.parse_args()

  return options


# -----------------------------------------------------------------------------
if __name__ == '__main__':
  options = parseArguments()
  main(options.query, options.output_file, options.url, options.batch_size)
