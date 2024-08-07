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

NS_MARCSLIM = 'http://www.loc.gov/MARC21/slim'
ALL_NS = {'marc': NS_MARCSLIM}

# -----------------------------------------------------------------------------
def main(inputFilenames, outputFilename, identifierColumn, batchSize, url, delimiter):
  """This script reads KBR identifiers from a specified column in a CSV file and requests their bibliographic KBR records from the Z3950 API."""

  # First check that all input files contain the needed column
  #
  for inputFilename in inputFilenames:
    with open(inputFilename, 'r') as inFile:
      inputReader = csv.DictReader(inFile, delimiter=delimiter)
      utils.checkIfColumnsExist(inputReader.fieldnames, [identifierColumn])

  kbrIdentifierLength = 8
  
  # Iterate over all input files and uniquely store found KBR identifiers
  #
  kbrIdentifiers = set()
  for inputFilename in inputFilenames:
    with open(inputFilename, 'r') as inFile:
      inputReader = csv.DictReader(inFile, delimiter=delimiter)

      # store found KBR identifiers in a set (so we only store unique values)
      #
      for row in inputReader:
        rowID = row[identifierColumn]
        if rowID != '':
          if len(rowID) == kbrIdentifierLength:
            kbrIdentifiers.add(rowID)

  if len(kbrIdentifiers) > 0:
    print(f'Successfully read {len(kbrIdentifiers)} KBR identifiers from the input CSV!')
    print(f'Starting to fetch the data in batches of {batchSize} ...')
  else:
    print(f'No valid KBR identifiers found, nothing to fetch!')
    exit(1)

  apiHandler = kbrAPI(url)
  apiHandler.setBatchSize(batchSize)

  with open(outputFilename, 'wb') as outFile:

    # the output collection will have the MARC namespace
    outFile.write(b'<collection xmlns="http://www.loc.gov/MARC21/slim">')

    # send API requests for batches of KBR identifiers
    # there is a limit with respect to the maximum length of the URL
    # this maximum is roughly 176 KBR identifiers per query
    #
    kbrIdentifiersList = list(kbrIdentifiers)
    allUnknownIDs = set()
    atLeastOneBatchUnknownIdentifiers = False
    pbar = tqdm(range(0, len(kbrIdentifiers), batchSize), position=0, desc='Batches')
    for i in pbar:
      pbar.set_description(f'Processed records: {i}, from which unknown IDs: {len(allUnknownIDs)}')
      batch = kbrIdentifiersList[i:i+batchSize]

      # Create the query string, but only take KBR identifiers of valid length
      query = 'IDNO=(' + ','.join(batch) + ')'

      # query the batch (e.g. query 100 identifiers)
      apiHandler.query(query)
      numberOfResults = apiHandler.numberResults() # this should be equal to the number of items the batch

      unknownIdentifiers = False
      retrievedRecordIDs = set()

      if numberOfResults < len(batch):
        atLeastOneBatchUnknownIdentifiers = True
        unknownIdentifiers = True

      # iterate over all records in that batch
      #
      # with the following line you can enable a second progress bar for records in a batch
      # however, this second progress bar usually is finished before initialized properly, so it might seem that nothing is happening
      # for record in tqdm(apiHandler.getRecords(), total=numberOfResults, position=1, leave=False, desc='Records in batch'):
      for record in apiHandler.getRecords():
        if unknownIdentifiers:
          # there is no namespace yet
          recordID = utils.getElementValue(record.find('./controlfield[@tag="001"]', ALL_NS))
          if recordID:
            retrievedRecordIDs.add(recordID)
        outFile.write(ET.tostring(record))

      if unknownIdentifiers:
        unknownIDs = set(batch) - retrievedRecordIDs
        allUnknownIDs.update(unknownIDs)
        numberUnknownIdentifiers = len(unknownIDs)
        #pbar.set_description(f'Processed records: {i}, from which unknown IDs: {len(allUnknownIDs)}')
        #print(f'{numberUnknownIdentifiers} unknown identifiers in batch {i}. Unknown identifiers: {unknownIDs}')

    outFile.write(b'</collection>')

    if atLeastOneBatchUnknownIdentifiers:
      print(f'{len(allUnknownIDs)} unknown identifiers in total. Unknown identifiers: {allUnknownIDs}')

def parseArguments():

  parser = ArgumentParser()
  parser.add_argument('input', nargs='+', help='One or more filenames from which the specified identifier column is read')
  parser.add_argument('-o', '--output-file', action='store', required=True, help='The name of the CSV file in which the extrated data is stored')
  parser.add_argument('--identifier-column', action='store', required=True, help='The column with the relative identifier based on which sequence numbers should be numbered')
  parser.add_argument('-b', '--batch-size', action='store', type=int, default=200, help="The number of identifiers per request")
  parser.add_argument('-u', '--url', action='store', required=True, help='The URL of the Z3950 KBR API')
  parser.add_argument('-d', '--delimiter', action='store', default=',', help='The optional delimiter of the input CSV, default is a comma')
  options = parser.parse_args()

  return options


# -----------------------------------------------------------------------------
if __name__ == '__main__':
  options = parseArguments()
  main(options.input, options.output_file, options.identifier_column, options.batch_size, options.url, options.delimiter)
