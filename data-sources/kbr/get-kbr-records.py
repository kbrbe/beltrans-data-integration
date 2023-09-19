#
# (c) 2023 Sven Lieber
# KBR Brussels
#
import csv
from tools import utils
from optparse import OptionParser
from tools.xml.KBRZ3950APIHandler import KBRZ3950APIHandler as kbrAPI
import lxml.etree as ET
from tqdm import tqdm

# -----------------------------------------------------------------------------
def main():
  """This script reads KBR identifiers from a specified column in a CSV file and requests their bibliographic KBR records from the Z3950 API."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The name of the CSV file from which data should be extracted')
  parser.add_option('-o', '--output-file', action='store', help='The name of the CSV file in which the extrated data is stored')
  parser.add_option('--identifier-column', action='store', help='The column with the relative identifier based on which sequence numbers should be numbered')
  parser.add_option('-b', '--batch-size', action='store', type='int', default=200, help="The number of identifiers per request")
  parser.add_option('-u', '--url', action='store', help='The URL of the Z3950 KBR API')
  parser.add_option('-d', '--delimiter', action='store', default=',', help='The optional delimiter of the input CSV, default is a comma')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if (not options.input_file) and (not options.output_file) and (not options.identifier_column) and (not options.url):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r') as inFile:

    inputReader = csv.DictReader(inFile, delimiter=options.delimiter)

    utils.checkIfColumnsExist(inputReader.fieldnames, [options.identifier_column])

    # store found KBR identifiers in a set (so we only store unique values)
    #
    kbrIdentifiers = set()
    for row in inputReader:
      rowID = row[options.identifier_column]
      if rowID != '':
        kbrIdentifiers.add(rowID)

  print(f'Successfully read {len(kbrIdentifiers)} KBR identifiers from the input CSV!')
  print(f'Starting to fetch the data in batches of {options.batch_size} ...')

  apiHandler = kbrAPI(options.url)
  apiHandler.setBatchSize(options.batch_size)

  with open(options.output_file, 'wb') as outFile:

    outFile.write(b'<collection xmlns="http://www.loc.gov/MARC21/slim">')

    # send API requests for batches of KBR identifiers
    # there is a limit with respect to the maximum length of the URL
    # this maximum is roughly 176 KBR identifiers per query
    #
    kbrIdentifiersList = list(kbrIdentifiers)
    for i in tqdm(range(0, len(kbrIdentifiers), options.batch_size), position=0, desc='Batches'):
      batch = kbrIdentifiersList[i:i+options.batch_size]

      query = 'IDNO=(' + ','.join(batch) + ')'

      # query the batch (e.g. query 100 identifiers)
      apiHandler.query(query)
      numberOfResults = apiHandler.numberResults() # this should be equal to the number of items the batch

      # iterate over all records in that batch
      #
      # with the following line you can enable a second progress bar for records in a batch
      # however, this second progress bar usually is finished before initialized properly, so it might seem that nothing is happening
      # for record in tqdm(apiHandler.data(), total=numberOfResults, position=1, leave=False, desc='Records in batch'):
      for record in apiHandler.data():
        outFile.write(ET.tostring(record))

    outFile.write(b'</collection>')

main()
