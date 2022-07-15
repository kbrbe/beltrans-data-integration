import unittest
import tempfile
import rdflib
import time
import utils
import csv
import os
import integration
from dataprofileTestHelper import DataprofileTestHelper
from BlazegraphIntegrationTestContainer import BlazegraphIntegrationTestContainer

# Don't show the traceback of an AssertionError, because the AssertionError already says what the issue is!
__unittest = True

# -----------------------------------------------------------------------------
class TestAggregatedDataKBRAndBnF(unittest.TestCase):

  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):
    # use temporary files which will be deleted in the tearDownClass function
    cls.tempAggKBR = os.path.join(tempfile.gettempdir(), 'aggregated-kbr.csv')
    cls.tempAggBnF = os.path.join(tempfile.gettempdir(), 'aggregated-bnf.csv')
    cls.tempAggAll = os.path.join(tempfile.gettempdir(), 'aggregated-data.csv')

    # start a local Blazegraph and insert our test data
    internalBlazegraphHostname='blz'
    with BlazegraphIntegrationTestContainer(imageName="data-integration_blazegraph-test", hostName=internalBlazegraphHostname) as blazegraph:
      time.sleep(10)      

      loadConfig = {
        'http://kbr-syracuse': ['./test/resources/source-graph-data-two-sources/kbr-data.ttl'],
        'http://master-data': ['./test/resources/source-graph-data-two-sources/master-data.ttl'],
        'http://bnf-publications': ['./test/resources/source-graph-data-two-sources/bnf-data.ttl'],
        'http://bnf-contributors': ['./test/resources/source-graph-data-two-sources/bnf-contributors.ttl'],
        'http://kbr-linked-authorities': ['./test/resources/source-graph-data-two-sources/kbr-contributors.ttl'],
  #      'http://isni-sru': ['./test/resources/isni-sru.ttl'],
  #      'http://isni-rdf': ['./test/resources/isni-rdf.ttl']
      }
      #uploadURL = 'http://' + internalBlazegraphHostname + '/namespace/kb'
      uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
      utils.addTestData(uploadURL, loadConfig)

      # query data from our test fixture
      with open(cls.tempAggKBR, 'wb') as resultFileAggKBR, \
           open(cls.tempAggBnF, 'wb') as resultFileAggBnF:

        queryAggKBR = utils.readSPARQLQuery('./dataprofile-aggregated-kbr.sparql')
        utils.query(uploadURL, queryAggKBR, resultFileAggKBR)

        queryAggBnF = utils.readSPARQLQuery('./dataprofile-aggregated-bnf.sparql')
        utils.query(uploadURL, queryAggBnF, resultFileAggBnF)

      # call the postprocessing function we would like to test
      integration.combineAggregatedResults(cls.tempAggKBR, cls.tempAggBnF, cls.tempAggAll)

      # read and store the queried/integrated data such that we can easily use it in the test functions
      with open(cls.tempAggAll, 'r') as allIn:
        csvReader = csv.DictReader(allIn, delimiter=',')
        csvData = [dict(d) for d in csvReader]
        cls.data = DataprofileTestHelper(csvData)
        print(cls.data.df)
    
  # ---------------------------------------------------------------------------
  @classmethod
  def tearDownClass(cls):
    if os.path.isfile(cls.tempAggKBR):
      os.remove(cls.tempAggKBR)
    if os.path.isfile(cls.tempAggBnF):
      os.remove(cls.tempAggBnF)
    if os.path.isfile(cls.tempAggAll):
      os.remove(cls.tempAggAll)

  # ---------------------------------------------------------------------------
  def testCorpusSize(self):
    """This function tests if the number of corpus rows is correct, thus that a book from KBR and BnF is matched in the same row if ISBN10 or ISBN13 match."""
    self.assertEqual(TestAggregatedDataKBRAndBnF.data.numberRows(), 23, msg="Corpus too big or too small")

  # ---------------------------------------------------------------------------
  def testIfAllKBRBooksFound(self):
    """This function tests if the corpus contains all needed KBR identifiers, not if they are properly matched to BnF."""
    bookIDs = [1,3,4,5,7,9,10,11,13,15,16,17,19,21,22,23,25,26,27]
    results = {}
    for i in bookIDs:
      results[i] = TestAggregatedDataKBRAndBnF.data.kbrTargetIdentifierExists(f'KBR book {i}')

    errors = {key: value for key, value in results.items() if value is not True} 
    self.assertEqual(len(errors), 0, msg=f'KBR books which are missing: {errors}')

  # ---------------------------------------------------------------------------
  def testIfAllBnFBooksFound(self):
    """This function tests if the corpus contains all needed BnF identifiers, not if they are properly matched to KBR."""
    bookIDs = [1,3,4,5,7,9,10,11,13,15,16,17,19,21,22,23,25,26,27]
    results = {}
    for i in bookIDs:
      results[i] = TestAggregatedDataKBRAndBnF.data.bnfTargetIdentifierExists(f'BnF book {i}')

    errors = {key: value for key, value in results.items() if value is not True} 
    self.assertEqual(len(errors), 0, msg=f'BnF books which are missing: {errors}')

  # ---------------------------------------------------------------------------
  def testIfKBRBooksFiltered(self):
    """This function tests if KBR books not matching the Belgian contributor criteria are filtered out."""
    bookIDs = [2,6,8,12,14,18,20,24,28]
    results = {}
    for i in bookIDs:
      results[i] = TestAggregatedDataKBRAndBnF.data.kbrTargetIdentifierExists(f'KBR book {i}')

    errors = {key: value for key, value in results.items() if value is not False} 
    self.assertEqual(len(errors), 0, msg=f'KBR books which should have been filtered out: {errors}')


  # ---------------------------------------------------------------------------
  def testIfBnFBooksFiltered(self):
    """This function tests if BnF books not matching the Belgian contributor criteria are filtered out."""
    bookIDs = [2,6,8,12,14,18,20,24,28]
    results = {}
    for i in bookIDs:
      results[i] = TestAggregatedDataKBRAndBnF.data.bnfTargetIdentifierExists(f'BnF book {i}')

    errors = {key: value for key, value in results.items() if value is not False} 
    self.assertEqual(len(errors), 0, msg=f'BnF books which should have been filtered out: {errors}')

  # ---------------------------------------------------------------------------
  def testMatchingKBRAndBnFBooks(self):
    """This function tests if books are matched via ISBN10 and/or ISBN13."""
    bookIDs = [4,5,7,10,11,13,16,17,19,21,22,23,25,26,27]
    results = {}
    for i in bookIDs:
      try:
        results[i] = TestAggregatedDataKBRAndBnF.data.kbrAndBnFIdentifierOnSameRow(f'KBR book {i}', f'BnF book {i}')
      except:
        results[i] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing KBR and BnF matches for the following books: {errors}')

if __name__ == '__main__':
  unittest.main()
