import requests
import os
from dotenv import load_dotenv
from datetime import date
import logging
import time
import xml.etree.ElementTree as ET
import urllib
from io import BytesIO
from optparse import OptionParser

NS_SRW = 'http://www.loc.gov/zing/srw/'

# -----------------------------------------------------------------------------
def getRecordSetID(xmlContent):

  recordSetID = None
  xmlInputStream = BytesIO(xmlContent)

  for event, elem in ET.iterparse(xmlInputStream, events=('start', 'end')):

    if event == 'end' and elem.tag == ET.QName(NS_SRW, 'resultSetId'):
      recordSetID = elem.text
      elem.clear()
      return recordSetID

# -----------------------------------------------------------------------------
def writeResponseRecords(xmlContent, outFile):
  """This function writes all found 'responseRecord' tags in xmlContent to file outFile."""

  counter = 0
  xmlInputStream = BytesIO(xmlContent)
  for event, elem in ET.iterparse(xmlInputStream, events=('start', 'end')):

    #
    # write each found responseRecord to the output file
    #
    if event == 'end' and elem.tag == 'responseRecord':
      outFile.write(ET.tostring(elem, encoding='utf-8'))
      counter += 1
      elem.clear()

  return counter

# -----------------------------------------------------------------------------
def main():

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-o', '--output-name-pattern', action='store', help='Files with this name pattern are created in which the downloaded data is stored')
  parser.add_option('-r', '--number-records', action='store', type='int', help='The number of records requested per API call, max is 1000')
  parser.add_option('-m', '--max-records', action='store', type='int', help='The maximum number of records which should be requested in total, e.g. 60000 in steps of "--number-records", it cannot be smaller than number-records')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.output_name_pattern) or (options.number_records > 1000) or (options.number_records > options.max_records) ):
    parser.print_help()
    exit(1)

  numberRecords = options.number_records
  maxRecords = options.max_records
  secondsBetweenAPIRequests = 10
  baseURL = 'https://isni-m.oclc.org/sru'
  query = 'pica.noi = "BE" and pica.st = "A"'
  #query = 'pica.noi="BE"'
  # query = 'pica.cn="KBR"'
  # it should not be already url encoded query = 'pica.cn%3D+%22KBR+%22'
  #query='pica.cn=KBR and pica.st=a'
  dateString = date.today().strftime('%Y-%m-%d')
  outputFilePrefix = dateString + "-sru-result"

  #
  # load environment variables from .env file
  #
  load_dotenv()

  USERNAME = os.getenv('ISNI_SRU_USERNAME')
  PASSWORD = os.getenv('ISNI_SRU_PASSWORD')
  existingQuery = os.getenv('ISNI_RESULT_SET_NAME')
  authValue = os.getenv('ISNI_API_AUTH_TEMP')

  logFormatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  logger = logging.getLogger(__file__)
  logger.setLevel(logging.INFO)

  loggingFilename = f'{outputFilePrefix}-{options.output_name_pattern}.log'
  logFilehandler = logging.FileHandler(loggingFilename)
  logFilehandler.setLevel(logging.INFO)
  logFilehandler.setFormatter(logFormatter)
  logger.addHandler(logFilehandler)

  consoleHandler = logging.StreamHandler()
  consoleHandler.setLevel(logging.INFO)
  consoleHandler.setFormatter(logFormatter)
  logger.addHandler(consoleHandler)
  #logging.basicConfig(filename=loggingFilename, level=logging.INFO)

  #payload = {'operation': 'searchRetrieve', 'version': '1.1', 'startRecord': 1, 'maximumRecords': numberRecords, 'recordSchema': 'isni-e', 'sortKeys': 'none', 'query': existingQuery, 'x-info-2-auth1.0-authenticationToken': authValue}
  payload = {'operation': 'searchRetrieve', 'version': '1.1', 'startRecord': 1, 'maximumRecords': numberRecords, 'recordSchema': 'isni-e', 'sortKeys': 'none', 'query': query}
  url = f'{baseURL}/username={USERNAME}/password={PASSWORD}/DB=1.3'

  recordSetID = None
  counter = 1
    
  #
  # There are currently 60452 records for the search term pica.noi="BE" and the number of max records per request is 1000
  # We decided to loop from 1 to 61000 in steps of 500 to make several requests
  #
  for i in range(1, maxRecords, numberRecords):

    logger.info(f'Iteration {counter}: requesting {numberRecords} from startRecord {i} (up until {maxRecords})')
    payload['startRecord'] = i

    try: 
      payloadStr = urllib.parse.urlencode(payload, safe=',+*\\')
      r = requests.get(url, params=payloadStr)
      logger.info(f'requesting URL {r.url}')
      r.raise_for_status()
    except requests.exceptions.Timeout:
      logging.error(f'There was a timeout in iteration {counter}')
    except requests.exceptions.TooManyRedirects:
      logging.error(f'There were too many redirects in iteration {counter}')
    except requests.exceptions.HTTPError as err:
      logging.error(f'There was an HTTP response code which is not 200 in iteration {counter}')
    except requests.exceptions.RequestException as e:
      raise SystemExit(e)

    #
    # set the result set ID and authentication token for further requests after obtained from the first request
    #
    if i == 1:
      logger.info("First request, obtaining values for further requests")
      recordSetID = getRecordSetID(r.content)
      logger.info(f'srw.resultSetName is {recordSetID}')
      payload['query'] = 'srw.resultSetName=' + recordSetID
      if 'X-SRU-Authentication-Token' in r.headers:
        token = r.headers['X-SRU-Authentication-Token']
        logger.info(f'x-info-2-auth1.0-authenticationToken is {token}')
        payload['x-info-2-auth1.0-authenticationToken'] = urllib.parse.unquote(token)
        logger.info(f'values obtained, new payload is {payload}')
      else:
        logging.error("No authentication token found, can't process further requests")
        exit(1)
    

    #
    # create a new file for the current paginated output
    # 
    paginatedNumber = i+numberRecords
    outputFilename = f'{outputFilePrefix}-{options.output_name_pattern}-{i}-{paginatedNumber}_{maxRecords}.xml'
    with open(outputFilename, 'wb') as outFile:
      outFile.write(b'<collection>')
      numRecordsWritten = writeResponseRecords(r.content, outFile)
      outFile.write(b'</collection>')
      if numRecordsWritten == 0:
        logger.info("No records written, received content was:")
        logger.info(r.content)
      counter += 1
      logger.info(f'Wrote {numRecordsWritten} result records to the output file {outputFilename}, now sleep {secondsBetweenAPIRequests} seconds')
    time.sleep(secondsBetweenAPIRequests)


main()
