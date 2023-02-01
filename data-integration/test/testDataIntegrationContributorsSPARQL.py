import unittest
import shutil
import tempfile
import rdflib
import time
import utils
import csv
import os
import integration
from interlink_named_graph_data_files import main as integrateDataSPARQLFiles
from interlink_named_graph_data import main as integrateDataSPARQLConfig
from dataprofileTestHelper import DataprofileTestHelper
from BlazegraphIntegrationTestContainer import BlazegraphIntegrationTestContainer

# Don't show the traceback of an AssertionError, because the AssertionError already says what the issue is!
__unittest = True

# -----------------------------------------------------------------------------
class TestDataIntegrationContributorsSPARQL():
  """This base class contains test cases for integrated contributor data.
     Different implementations are tested in subclasses which inherit these test cases
     but use their own setup method.
  """
   
 # ---------------------------------------------------------------------------
  def testCorpusSize(self):
    """This function tests if the number of corpus rows is correct, thus that contributors from KBR, BnF and KB with a common identifier are listed in the same row."""
    self.assertEqual(self.getData().numberRows(), 23, msg="Corpus too big or too small")


  # ---------------------------------------------------------------------------
  def testMatchingKBRBnFAndKB(self):
    """This function tests if there is a match across KBR, BnF and KB based on ISNI, VIAF and Wikidata."""
    contributorIDs = [1, 5, 9]
    results = {}
    for i in contributorIDs:
      try:
        results[i] = self.getData().identifiersOnSameRow(('kbrIDs', f'kbrAuthorBE{i}'), [('bnfIDs', f'bnfAuthorBE{i}'),('ntaIDs', f'kbAuthorBE{i}')])
      except:
        results[i] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing contributor identifier matches for the following identifiers: {errors}')


  # ---------------------------------------------------------------------------
  def testMatchingKBRAndBnF(self):
    """This function tests if there is a match across KBR and BnF based on ISNI, VIAF and Wikidata."""
    contributorIDs = [2, 6, 10]
    results = {}
    for i in contributorIDs:
      try:
        results[i] = self.getData().identifiersOnSameRow(('kbrIDs', f'kbrAuthorBE{i}'), [('bnfIDs', f'bnfAuthorBE{i}')])
      except:
        results[i] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing contributor identifier matches for the following identifiers: {errors}')


  # ---------------------------------------------------------------------------
  def testMatchingKBRAndKB(self):
    """This function tests if there is a match across KBR and KB based on ISNI, VIAF and Wikidata."""
    contributorIDs = [(3,2), (11,10), (7,6) ]
    results = {}
    for kbrID, kbID in contributorIDs:
      try:
        results[f'{kbrID},{kbID}'] = self.getData().identifiersOnSameRow(('kbrIDs', f'kbrAuthorBE{kbrID}'), [('ntaIDs', f'kbAuthorBE{kbID}')])
      except:
        results[f'{kbrID},{kbID}'] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing contributor identifier matches for the following identifiers: {errors}')


  # ---------------------------------------------------------------------------
  def testMatchingBnFAndKB(self):
    """This function tests if there is a match across BnF and KB based on ISNI, VIAF and Wikidata (or BnF and KB correlation list)."""
    contributorIDs = [3,11,7]
    results = {}
    for i in contributorIDs:
      try:
        results[i] = self.getData().identifiersOnSameRow(('bnfIDs', f'bnfAuthorBE{i}'), [('ntaIDs', f'kbAuthorBE{i}')])
      except:
        results[i] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing contributor identifier matches for the following identifiers: {errors}')

  # ---------------------------------------------------------------------------
  def testCorrectCorrelationBnFandKB(self):
    """This function tests if the entry of the correlation list with BnF and KB is part of the integrated authority records."""
    bnfID = 'bnfAuthorBE13'
    kbID = 'kbAuthorBE13'
    result  = self.getData().identifiersOnSameRow(('bnfIDs', bnfID), [('ntaIDs', kbID)])
    
    self.assertTrue(result, msg=f'Missing contributor match from correlation list "{bnfID}" and "{kbID}"')

  # ---------------------------------------------------------------------------
  def testCorrectCorrelationKBRBnFAndKB(self):
    """This function tests if the entry of the correlation list with KBR, BnF and KB is part of the integrated authority recors."""
    kbrID = 'kbrAuthorBE14'
    bnfID = 'bnfAuthorBE14'
    kbID = 'kbAuthorBE14'
    result  = self.getData().identifiersOnSameRow(('kbrIDs', kbrID), [('bnfIDs', bnfID), ('ntaIDs', kbID)])
    
    self.assertTrue(result, msg=f'Missing contributor match from correlation list "{kbrID}", "{bnfID}" and "{kbID}"')

  # ---------------------------------------------------------------------------
  def testNoAutomaticIntegrationForCorrelationList(self):
    """This function tests if the entry KBR authority with a wrong ISNI is not automatically integrated because it is part of the correlation list."""
    kbrID = 'kbrAuthorBE14'
    bnfID = 'bnfAuthorBE8'
    result  = self.getData().identifiersOnSameRow(('kbrIDs', kbrID), [('bnfIDs', bnfID)])
    
    self.assertFalse(result, msg=f'There is a wrong match between "{kbrID}" and "{bnfID}" (they have a common ID, but this should be neglected for {kbrID} because it was added via a correlation list)')


  # ---------------------------------------------------------------------------
  def testThirdPartyIdentifiersAddedAfterIntegration(self):
    """This function tests if mentioned third party identifiers of local records are still added after the automatic data integration."""
    # to be determined if this feature is needed (https://github.com/kbrbe/beltrans-data-integration/issues/176)
    pass


# -----------------------------------------------------------------------------
# class TestDataIntegrationContributorsSPARQLHardCoded(TestDataIntegrationContributorsSPARQL, unittest.TestCase):
#
#   def getData(self):
#     return TestDataIntegrationContributorsSPARQLHardCoded.data
#
#   # ---------------------------------------------------------------------------
#   @classmethod
#   def setUpClass(cls):
#
#     # use temporary files which will be deleted in the tearDownClass function
#     cls.tempAgg = os.path.join(tempfile.gettempdir(), 'aggregated-data.csv')
#
#     # start a local Blazegraph and insert our test data
#     internalBlazegraphHostname='blz'
#     with BlazegraphIntegrationTestContainer(imageName="data-integration_blazegraph-test", hostName=internalBlazegraphHostname) as blazegraph:
#       time.sleep(10)
#
#       loadConfig = {
#         'http://kbr-linked-authorities': ['./test/resources/data-integration-sparql/kbr-contributors.ttl'],
#         'http://bnf-contributors': ['./test/resources/data-integration-sparql/bnf-contributors.ttl'],
#         'http://kb-linked-authorities': ['./test/resources/data-integration-sparql/kb-contributors.ttl'],
#         'http://master-data': ['./test/resources/data-integration-sparql/master-data.ttl'],
#       }
#       #uploadURL = 'http://' + internalBlazegraphHostname + '/namespace/kb'
#       uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
#       utils.addTestData(uploadURL, loadConfig)
#
#       # integrate the data (this integration we actually want to test)
#       numberUpdates = 3
#       integrateDataSPARQLFiles(uploadURL, numberUpdates, 'contributors-create-queries.csv', 'contributors-update-queries.csv')
#
#       # query data from our test fixture
#       with open(cls.tempAgg, 'wb') as resultFileAgg:
#
#         queryAgg = utils.readSPARQLQuery('./sparql-queries/get-integrated-contributors.sparql')
#         #queryAgg = utils.readSPARQLQuery('sparql-queries/get-all.sparql')
#         utils.query(uploadURL, queryAgg, resultFileAgg)
#
#
#       # read and store the queried/integrated data such that we can easily use it in the test functions
#       with open(cls.tempAgg, 'r') as allIn:
#         csvReader = csv.DictReader(allIn, delimiter=',')
#         csvData = [dict(d) for d in csvReader]
#         cls.data = DataprofileTestHelper(csvData)
#         print(cls.data.df[['contributorID', 'kbrIDs', 'bnfIDs', 'ntaIDs', 'isniIDs', 'viafIDs', 'wikidataIDs']])
#
#   # ---------------------------------------------------------------------------
#   @classmethod
#   def tearDownClass(cls):
#     if os.path.isfile(cls.tempAgg):
#       os.remove(cls.tempAgg)


# -----------------------------------------------------------------------------
class TestDataIntegrationContributorsSPARQLConfig(TestDataIntegrationContributorsSPARQL, unittest.TestCase):

  def getData(self):
    return TestDataIntegrationContributorsSPARQLConfig.data

  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):
    # use temporary files which will be deleted in the tearDownClass function
    cls.tempAgg = os.path.join(tempfile.gettempdir(), 'aggregated-data.csv')
    cls.tempLogDir = os.path.join(tempfile.gettempdir(), 'integration-sparql-test-log')
    os.makedirs(cls.tempLogDir)

    # start a local Blazegraph and insert our test data
    internalBlazegraphHostname = 'blz'
    with BlazegraphIntegrationTestContainer(imageName="data-integration_blazegraph-test",
                                            hostName=internalBlazegraphHostname) as blazegraph:
      time.sleep(10)

      loadConfig = {
        'http://kbr-linked-authorities': ['./test/resources/data-integration-sparql/kbr-contributors.ttl'],
        'http://bnf-contributors': ['./test/resources/data-integration-sparql/bnf-contributors.ttl'],
        'http://kb-linked-authorities': ['./test/resources/data-integration-sparql/kb-contributors.ttl'],
        'http://master-data': ['./test/resources/data-integration-sparql/master-data.ttl'],
        'http://beltrans-contributors': ['./test/resources/data-integration-sparql/correlation-list-contributors.ttl']
      }
      # uploadURL = 'http://' + internalBlazegraphHostname + '/namespace/kb'
      uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
      utils.addTestData(uploadURL, loadConfig)


      # integrate the data (this integration we actually want to test)
      numberUpdates = 3
      integrateDataSPARQLConfig(url=uploadURL, queryType='contributors', targetGraph="http://beltrans-contributors",
                                createQueriesConfig='config-integration-contributors-create.csv',
                                updateQueriesConfig='config-integration-contributors-update.csv',
                                numberUpdates=numberUpdates,
                                queryLogDir=cls.tempLogDir)


      # query data from our test fixture
      with open(cls.tempAgg, 'wb') as resultFileAgg:
        queryAgg = utils.readSPARQLQuery('./sparql-queries/get-integrated-contributors.sparql')
        # queryAgg = utils.readSPARQLQuery('sparql-queries/get-all.sparql')
        utils.query(uploadURL, queryAgg, resultFileAgg)

      # read and store the queried/integrated data such that we can easily use it in the test functions
      with open(cls.tempAgg, 'r') as allIn:
        csvReader = csv.DictReader(allIn, delimiter=',')
        csvData = [dict(d) for d in csvReader]
        cls.data = DataprofileTestHelper(csvData)
        print(cls.data.df[['contributorID', 'kbrIDs', 'bnfIDs', 'ntaIDs', 'isniIDs', 'viafIDs', 'wikidataIDs']])

      # In case we want to debug the test fixture (using the query interface on localhost:8080)
      #print("sleep")
      #time.sleep(5000)

  # ---------------------------------------------------------------------------
  @classmethod
  def tearDownClass(cls):
    if os.path.isfile(cls.tempAgg):
      os.remove(cls.tempAgg)
    if os.path.isdir(cls.tempLogDir):
      shutil.rmtree(cls.tempLogDir)


if __name__ == '__main__':
  unittest.main()
