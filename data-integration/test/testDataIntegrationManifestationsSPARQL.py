import unittest
import tempfile
import rdflib
import time
import utils
import csv
import os
import integration
from interlink_named_graph_data_files import main as integrateDataSPARQLFiles
from dataprofileTestHelper import DataprofileTestHelper
from BlazegraphIntegrationTestContainer import BlazegraphIntegrationTestContainer

# Don't show the traceback of an AssertionError, because the AssertionError already says what the issue is!
__unittest = True

# -----------------------------------------------------------------------------
class TestDataIntegrationManifestationsSPARQL(unittest.TestCase):

  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):
    # use temporary files which will be deleted in the tearDownClass function
    cls.tempAgg = os.path.join(tempfile.gettempdir(), 'aggregated-data.csv')

    # start a local Blazegraph and insert our test data
    internalBlazegraphHostname='blz'
    with BlazegraphIntegrationTestContainer(imageName="data-integration_blazegraph-test", hostName=internalBlazegraphHostname) as blazegraph:
      time.sleep(10)      

      loadConfig = {
        'http://kbr-syracuse': ['./test/resources/data-integration-sparql/kbr-manifestations.ttl'],
        'http://bnf-publications': ['./test/resources/data-integration-sparql/bnf-manifestations.ttl'],
        'http://kb-publications': ['./test/resources/data-integration-sparql/kb-manifestations.ttl'],
        'http://master-data': ['./test/resources/data-integration-sparql/master-data.ttl'],
      }
      #uploadURL = 'http://' + internalBlazegraphHostname + '/namespace/kb'
      uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
      utils.addTestData(uploadURL, loadConfig)

      # integrate the data (this integration we actually want to test)
      numberUpdates = 3
      integrateDataSPARQLFiles(uploadURL, numberUpdates, 'manifestations-create-queries.csv', 'manifestations-update-queries.csv')

      # query data from our test fixture
      with open(cls.tempAgg, 'wb') as resultFileAgg:

        queryAgg = utils.readSPARQLQuery('./sparql-queries/get-integrated-manifestations.sparql')
        #queryAgg = utils.readSPARQLQuery('sparql-queries/get-all.sparql')
        utils.query(uploadURL, queryAgg, resultFileAgg)


      # read and store the queried/integrated data such that we can easily use it in the test functions
      with open(cls.tempAgg, 'r') as allIn:
        csvReader = csv.DictReader(allIn, delimiter=',')
        csvData = [dict(d) for d in csvReader]
        cls.data = DataprofileTestHelper(csvData)
        print(cls.data.df[['targetIdentifier', 'targetISBN10', 'targetISBN13', 'targetKBRIdentifier', 'targetBnFIdentifier', 'targetKBIdentifier']])
    
  # ---------------------------------------------------------------------------
  @classmethod
  def tearDownClass(cls):
    if os.path.isfile(cls.tempAgg):
      os.remove(cls.tempAgg)

  # ---------------------------------------------------------------------------
  def testCorpusSize(self):
    """This function tests if the number of corpus rows is correct, thus that contributors from KBR, BnF and KB with a common identifier are listed in the same row."""
    self.assertEqual(TestDataIntegrationManifestationsSPARQL.data.numberRows(), 14, msg="Corpus too big or too small")


  # ---------------------------------------------------------------------------
  def testMatchingKBRBnFAndKB(self):
    """This function tests if there is a match across KBR, BnF and KB based on ISNI, VIAF and Wikidata."""
    contributorIDs = [1, 5]
    results = {}
    for i in contributorIDs:
      try:
        results[i] = TestDataIntegrationManifestationsSPARQL.data.identifiersOnSameRow(('targetKBRIdentifier', f'kbrBook{i}'), [('targetBnFIdentifier', f'bnfBook{i}'),('targetKBIdentifier', f'kbBook{i}')])
      except:
        results[i] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing contributor identifier matches for the following identifiers: {errors}')


  # ---------------------------------------------------------------------------
  def testMatchingKBRAndBnF(self):
    """This function tests if there is a match across KBR and BnF based on ISNI, VIAF and Wikidata."""
    contributorIDs = [2, 6]
    results = {}
    for i in contributorIDs:
      try:
        results[i] = TestDataIntegrationManifestationsSPARQL.data.identifiersOnSameRow(('targetKBRIdentifier', f'kbrBook{i}'), [('targetBnFIdentifier', f'bnfBook{i}')])
      except:
        results[i] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing contributor identifier matches for the following identifiers: {errors}')


  # ---------------------------------------------------------------------------
  def testMatchingKBRAndKB(self):
    """This function tests if there is a match across KBR and KB based on ISNI, VIAF and Wikidata."""
    contributorIDs = [(3,2), (7,6) ]
    results = {}
    for kbrID, kbID in contributorIDs:
      try:
        results[f'{kbrID},{kbID}'] = TestDataIntegrationManifestationsSPARQL.data.identifiersOnSameRow(('targetKBRIdentifier', f'kbrBook{kbrID}'), [('targetKBIdentifier', f'kbBook{kbID}')])
      except:
        results[f'{kbrID},{kbID}'] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing contributor identifier matches for the following identifiers: {errors}')


   # ---------------------------------------------------------------------------
  def testMatchingBnFAndKB(self):
    """This function tests if there is a match across BnF and KB based on ISNI, VIAF and Wikidata."""
    contributorIDs = [3,7]
    results = {}
    for i in contributorIDs:
      try:
        results[i] = TestDataIntegrationManifestationsSPARQL.data.identifiersOnSameRow(('targetBnFIdentifier', f'bnfBook{i}'), [('targetKBIdentifier', f'kbBook{i}')])
      except:
        results[i] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing contributor identifier matches for the following identifiers: {errors}')






if __name__ == '__main__':
  unittest.main()
