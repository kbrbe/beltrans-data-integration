import requests
import os
from dotenv import load_dotenv
from datetime import date
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
def writeRecord(xmlContent, outFile):

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
  parser.add_option('-o', '--output-file', action='store', help='The file in which the cleaned data is stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.output_file) ):
    parser.print_help()
    exit(1)


  load_dotenv()

  BASE_URL = 'https://isni-m.oclc.org/sru'
  USERNAME = os.getenv('ISNI_SRU_USERNAME')
  PASSWORD = os.getenv('ISNI_SRU_PASSWORD')
  QUERY = 'pica.noi%3D%22BE%22'
  MAX_RECORDS = 1000
  DATE_STRING = date.today().strftime('%Y-%m-%d')
  OUTPUT_BASENAME = DATE_STRING + "-sru-result"

  namespaces = {'srw': NS_SRW}

  query = "pica.noi%3D%22BE%22"
  existingQuery = os.getenv('ISNI_RESULT_SET_NAME')
  authValue = os.getenv('ISNI_API_AUTH_TEMP')

  payload = {'operation': 'searchRetrieve', 'version': '1.1', 'recordSchema': 'isni-e', 'maximumRecords': 500, 'startRecord': 1, 'query': existingQuery, 'x-info-2-auth1.0-authenticationToken': authValue}
  #payload = {'operation': 'searchRetrieve', 'version': '1.1', 'recordSchema': 'isni-e', 'maximumRecords': 50, 'startRecord': 1, 'query': query}
  url = f'{BASE_URL}/username={USERNAME}/password={PASSWORD}/DB=1.3/'

  with open(options.output_file, 'wb') as outFile:

    outFile.write(b'<collection>')
    recordSetID = None
    counter = 1
    
    #
    # There are currently 60452 records for the search term pica.noi="BE" and the number of max records per request is 1000
    # We decided to loop from 1 to 61000 in steps of 500 to make several requests
    #
    for i in range(1, 61000,500):

      print(f'Iteration {counter}: requesting from {i}')
      payload['startRecord'] = i

      try: 
        payloadStr = urllib.parse.urlencode(payload, safe=',+')
        #print(payloadStr)
        r = requests.get(url, params=payloadStr)
        print("requesting: ")
        print(r.url)
        r.raise_for_status()
      except requests.exceptions.Timeout:
        print(f'There was a timeout in iteration {counter}')
      except requests.exceptions.TooManyRedirects:
        print(f'There were too many redirects in iteration {counter}')
      except requests.exceptions.HTTPError as err:
        print(f'There was an HTTP response code which is not 200 in iteration {counter}')
      except requests.exceptions.RequestException as e:
        raise SystemExit(e)

      #
      # set the result set ID and authentication token for further requests after obtained from the first request
      #
      #if i == 1:
      #  print("First request, obtaining values for further requests")
      #  recordSetID = getRecordSetID(r.content)
      #  print("srw.resultSetName is: '" + str(recordSetID) + "'")
      #  payload['query'] = 'srw.resultSetName=' + recordSetID
      #  if 'X-SRU-Authentication-Token' in r.headers:
      #    print("x-info-2-auth1.0-authenticationToken is: '" + r.headers['X-SRU-Authentication-Token'] + "'")
      #    payload['x-info-2-auth1.0-authenticationToken'] = r.headers['X-SRU-Authentication-Token']
      #    print("values obtained!")
      #    print("payload is now:")
      #    print(payload)
      #  else:
      #    print("No authentication token found, can't process further requests")
      #    exit(1)
    
      numRecordsWritten = writeRecord(r.content, outFile)
      if numRecordsWritten == 0:
        print("No records written, received content was:")
        print(r.content)
      counter += 1
      print(f'Wrote {numRecordsWritten} result records to the output file, now sleep 5 seconds')
      time.sleep(5)

    outFile.write(b'</collection>')

main()
