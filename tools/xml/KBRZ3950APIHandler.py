import requests
import urllib.parse
import sys
import time
import lxml.etree as ET

class KBRZ3950APIHandler:
    """This class offers an interface to consult KBRs Z3950 API. The query is asked in batches of 200 records."""

    def __init__(self, baseURL):
        self._baseURL = baseURL
        self._numberResults = None
        self._queryString = None
        self._queryURL = None
        self._batchSize = 200

    def setBatchSize(self, batchSize):
        self._batchSize = int(batchSize)

    def query(self, queryString):
        self._queryString = queryString
        queryStringQuotes = queryString.replace("'", '"')
        self._queryURL = self._baseURL + '&q=' + urllib.parse.quote(queryStringQuotes, safe='=*"()')

        # query 0 records, because we are only interested in the header mentioning the total number of records
        numberURL = self._queryURL + '&rows=0'

        try:
          response = requests.get(numberURL)
          response.raise_for_status()
          tree = ET.fromstring(response.content)
          self._numberResults = int(tree.find('./result').get('numFound'))
        except requests.exceptions.HTTPError as he:
          statusCode = he.response.status_code
          print(f'{statusCode} error while trying to determine the number of query results for base URL: "{self._baseURL}"')
          sys.exit(1)
        except Exception as e:
          print(f'Error while trying to determine the number of query results with base URL: "{self._baseURL}"')
          print(e)
          sys.exit(1)

    def numberResults(self):
        return self._numberResults

    def getRecords(self):
        """This iterator function returns record per record (of all batches)"""
        startRecord = 0
        maxRecord = self._numberResults

        if maxRecord == 0:
          return None

        for i in range(startRecord, maxRecord, self._batchSize):
            requestURL = self._queryURL + '&rows=' + str(self._batchSize) + '&start=' + str(i)
            response = requests.get(requestURL)
            tree = ET.fromstring(response.content)
            records = tree.findall('./result/record')
            for record in records:
              yield record
