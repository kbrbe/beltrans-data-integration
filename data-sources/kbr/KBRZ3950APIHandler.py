import requests
import urllib.parse
import lxml.etree as ET

class KBRZ3950APIHandler:
    """This class offers an interface to consult KBRs Z3950 API. The query is asked in batches of 200 records."""

    def __init__(self, baseURL):
        self._baseURL = baseURL
        self._numberResults = None
        self._queryString = None
        self._queryURL = None
        self._batchSize = 200

    def query(self, queryString):
        self._queryString = queryString
        self._queryURL = self._baseURL + '&q=' + urllib.parse.quote(queryString)

        # query 0 records, because we are only interested in the header mentioning the total number of records
        response = requests.get(self._queryURL + '&rows=0')
        tree = ET.fromstring(response.content)
        self._numberResults = tree.find('./result').get('numFound')

    def numberResults(self):
        return self._numberResults

    def data(self):
        """This iterator function returns the search results in batches of 200"""
        startRecord = 0
        maxRecord = self._numberResults - 1

        for i in range(startRecord, maxRecord, self._batchSize):
            response = requests.get(self._queryURL + '&rows=' + self._batchSize + '&start=' + i)
            tree = ET.fromstring(response.content)
            yield tree.find('./result/record')
