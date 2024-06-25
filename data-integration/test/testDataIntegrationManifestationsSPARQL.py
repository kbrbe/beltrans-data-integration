import unittest
import tempfile
import shutil
import rdflib
import time
import utils
import csv
import os
import integration
from interlink_named_graph_data_files import main as integrateDataSPARQLFiles
from interlink_named_graph_data import main as integrateDataSPARQLConfig
from interlink_named_graph_data_single_update import main as integrateDataSPARQLConfigSingleUpdate
from interlink_named_graph_data_clustering import main as integrateDataClustering
from dataprofileTestHelper import DataprofileTestHelper
from BlazegraphIntegrationTestContainer import BlazegraphIntegrationTestContainer

# Don't show the traceback of an AssertionError, because the AssertionError already says what the issue is!
__unittest = True

# -----------------------------------------------------------------------------
class TestDataIntegrationManifestationsSPARQL():

  # ---------------------------------------------------------------------------
  def testCorpusSize(self):
    """This function tests if the number of corpus rows is correct, thus that contributors from KBR, BnF and KB with a common identifier are listed in the same row."""
    self.assertEqual(self.getData().numberRows(), 14, msg="Corpus too big or too small")


  # ---------------------------------------------------------------------------
  def testMatchingKBRBnFAndKB(self):
    """This function tests if there is a match across KBR, BnF and KB based on ISNI, VIAF and Wikidata."""
    contributorIDs = [1, 5]
    results = {}
    for i in contributorIDs:
      try:
        results[i] = self.getData().identifiersOnSameRow(('targetKBRIdentifier', f'kbrBook{i}'), [('targetBnFIdentifier', f'bnfBook{i}'),('targetKBIdentifier', f'kbBook{i}')])
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
        results[i] = self.getData().identifiersOnSameRow(('targetKBRIdentifier', f'kbrBook{i}'), [('targetBnFIdentifier', f'bnfBook{i}')])
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
        results[f'{kbrID},{kbID}'] = self.getData().identifiersOnSameRow(('targetKBRIdentifier', f'kbrBook{kbrID}'), [('targetKBIdentifier', f'kbBook{kbID}')])
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
        results[i] = self.getData().identifiersOnSameRow(('targetBnFIdentifier', f'bnfBook{i}'), [('targetKBIdentifier', f'kbBook{i}')])
      except:
        results[i] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing contributor identifier matches for the following identifiers: {errors}')




# # -----------------------------------------------------------------------------
#class TestDataIntegrationManifestationsSPARQLHardCoded(TestDataIntegrationManifestationsSPARQL, unittest.TestCase):


#  def getData(self):
#    return TestDataIntegrationManifestationsSPARQLHardCoded.data

  # ---------------------------------------------------------------------------
#  @classmethod
#  def setUpClass(cls):
    # use temporary files which will be deleted in the tearDownClass function
#    cls.tempAgg = os.path.join(tempfile.gettempdir(), 'aggregated-data.csv')

    # start a local Blazegraph and insert our test data
#    internalBlazegraphHostname='blz'
#    with BlazegraphIntegrationTestContainer(imageName="data-integration_blazegraph-test", hostName=internalBlazegraphHostname) as blazegraph:
#      time.sleep(10)

#      loadConfig = {
#        'http://kbr-syracuse': ['./test/resources/data-integration-sparql/kbr-manifestations.ttl'],
#        'http://bnf-publications': ['./test/resources/data-integration-sparql/bnf-manifestations.ttl'],
#        'http://kb-publications': ['./test/resources/data-integration-sparql/kb-manifestations.ttl'],
#        'http://master-data': ['./test/resources/data-integration-sparql/master-data.ttl'],
#      }
      #uploadURL = 'http://' + internalBlazegraphHostname + '/namespace/kb'
#      uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
#      utils.addTestData(uploadURL, loadConfig)

      # integrate the data (this integration we actually want to test)
#      numberUpdates = 3
#      integrateDataSPARQLFiles(uploadURL, numberUpdates, 'manifestations-create-queries.csv', 'manifestations-update-queries.csv')

      # query data from our test fixture
#      with open(cls.tempAgg, 'wb') as resultFileAgg:

#        queryAgg = utils.readSPARQLQuery('./sparql-queries/get-integrated-manifestations.sparql')
        #queryAgg = utils.readSPARQLQuery('sparql-queries/get-all.sparql')
#        utils.query(uploadURL, queryAgg, resultFileAgg)


      # read and store the queried/integrated data such that we can easily use it in the test functions
#      with open(cls.tempAgg, 'r') as allIn:
#        csvReader = csv.DictReader(allIn, delimiter=',')
#        csvData = [dict(d) for d in csvReader]
#        cls.data = DataprofileTestHelper(csvData)
#        print(cls.data.df[['targetIdentifier', 'targetISBN10', 'targetISBN13', 'targetKBRIdentifier', 'targetBnFIdentifier', 'targetKBIdentifier']])

  # ---------------------------------------------------------------------------
#  @classmethod
#  def tearDownClass(cls):
#    if os.path.isfile(cls.tempAgg):
#      os.remove(cls.tempAgg)

# -----------------------------------------------------------------------------
class TestDataIntegrationManifestationsSPARQLConfig(TestDataIntegrationManifestationsSPARQL, unittest.TestCase):

  def getData(self):
    return TestDataIntegrationManifestationsSPARQLConfig.data

  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):
    # use temporary files which will be deleted in the tearDownClass function
    cls.tempAgg = os.path.join(tempfile.gettempdir(), 'aggregated-data.csv')
    cls.tempLogDir = os.path.join(tempfile.gettempdir(), 'integration-sparql-manifestation-test-log')
    os.makedirs(cls.tempLogDir)

    # start a local Blazegraph and insert our test data
    internalBlazegraphHostname = 'blz'
    with BlazegraphIntegrationTestContainer(imageName="data-integration_blazegraph-test",
                                            hostName=internalBlazegraphHostname) as blazegraph:
      time.sleep(10)

      loadConfig = {
        'http://kbr-syracuse': ['./test/resources/data-integration-sparql/kbr-manifestations.ttl',
                                './test/resources/data-integration-sparql/kbr-isbns.ttl'],
        'http://bnf-publications': ['./test/resources/data-integration-sparql/bnf-manifestations.ttl',
                                    './test/resources/data-integration-sparql/bnf-isbns.ttl'],
        'http://kb-publications': ['./test/resources/data-integration-sparql/kb-manifestations.ttl',
                                   './test/resources/data-integration-sparql/kb-isbns.ttl'],
        'http://master-data': ['./test/resources/data-integration-sparql/master-data.ttl'],
        'http://kbr-originals': ['./test/resources/data-integration-sparql/kbr-originals.ttl'],
        'http://kb-originals': ['./test/resources/data-integration-sparql/kb-originals.ttl']
      }
      # uploadURL = 'http://' + internalBlazegraphHostname + '/namespace/kb'
      uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
      utils.addTestData(uploadURL, loadConfig)

      # integrate the data (this integration we actually want to test)
      numberUpdates = 3
      integrateDataSPARQLConfig(url=uploadURL, queryType='manifestations', targetGraph="http://beltrans-manifestations",
                                createQueriesConfig='config-integration-manifestations-create.csv',
                                updateQueriesConfig='config-integration-manifestations-update.csv',
                                numberUpdates=numberUpdates,
                                queryLogDir=cls.tempLogDir)

      # query data from our test fixture
      with open(cls.tempAgg, 'wb') as resultFileAgg:
        queryAgg = utils.readSPARQLQuery('./sparql-queries/get-integrated-manifestations.sparql')
        # queryAgg = utils.readSPARQLQuery('sparql-queries/get-all.sparql')
        utils.query(uploadURL, queryAgg, resultFileAgg)

      # read and store the queried/integrated data such that we can easily use it in the test functions
      with open(cls.tempAgg, 'r') as allIn:
        csvReader = csv.DictReader(allIn, delimiter=',')
        csvData = [dict(d) for d in csvReader]
        cls.data = DataprofileTestHelper(csvData)
        print(cls.data.df[
                ['targetIdentifier', 'targetISBN10', 'targetISBN13', 'targetKBRIdentifier', 'targetBnFIdentifier',
                 'targetKBIdentifier']])

  # ---------------------------------------------------------------------------
  @classmethod
  def tearDownClass(cls):
    if os.path.isfile(cls.tempAgg):
      os.remove(cls.tempAgg)
    if os.path.isdir(cls.tempLogDir):
      shutil.rmtree(cls.tempLogDir)

# -----------------------------------------------------------------------------
class TestDataIntegrationManifestationsSPARQLConfigSingleUpdate(TestDataIntegrationManifestationsSPARQL, unittest.TestCase):

  def getData(self):
    return TestDataIntegrationManifestationsSPARQLConfigSingleUpdate.data

  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):
    # use temporary files which will be deleted in the tearDownClass function
    cls.tempAgg = os.path.join(tempfile.gettempdir(), 'aggregated-data.csv')
    cls.tempLogDir = os.path.join(tempfile.gettempdir(), 'integration-sparql-manifestation-test-log')
    os.makedirs(cls.tempLogDir)

    # start a local Blazegraph and insert our test data
    internalBlazegraphHostname = 'blz'
    with BlazegraphIntegrationTestContainer(imageName="data-integration_blazegraph-test",
                                            hostName=internalBlazegraphHostname) as blazegraph:
      time.sleep(10)

      loadConfig = {
        'http://kbr-syracuse': ['./test/resources/data-integration-sparql/kbr-manifestations.ttl',
                                './test/resources/data-integration-sparql/kbr-isbns.ttl'],
        'http://bnf-publications': ['./test/resources/data-integration-sparql/bnf-manifestations.ttl',
                                './test/resources/data-integration-sparql/bnf-isbns.ttl'],
        'http://kb-publications': ['./test/resources/data-integration-sparql/kb-manifestations.ttl',
                                './test/resources/data-integration-sparql/kb-isbns.ttl'],
        'http://master-data': ['./test/resources/data-integration-sparql/master-data.ttl'],
        'http://kbr-originals': ['./test/resources/data-integration-sparql/kbr-originals.ttl'],
        'http://kb-originals': ['./test/resources/data-integration-sparql/kb-originals.ttl']
      }
      # uploadURL = 'http://' + internalBlazegraphHostname + '/namespace/kb'
      uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
      utils.addTestData(uploadURL, loadConfig)

      # integrate the data (this integration we actually want to test)
      numberUpdates = 3
      integrateDataSPARQLConfigSingleUpdate(url=uploadURL, queryType='manifestations', targetGraph="http://beltrans-manifestations",
                                createQueriesConfig='config-integration-manifestations-create.csv',
                                updateQueriesConfig='config-integration-manifestations-single-update.csv',
                                numberUpdates=numberUpdates, queryLogDir=cls.tempLogDir)

      # query data from our test fixture
      with open(cls.tempAgg, 'wb') as resultFileAgg:
        queryAgg = utils.readSPARQLQuery('./sparql-queries/get-integrated-manifestations.sparql')
        # queryAgg = utils.readSPARQLQuery('sparql-queries/get-all.sparql')
        utils.query(uploadURL, queryAgg, resultFileAgg)

      # read and store the queried/integrated data such that we can easily use it in the test functions
      with open(cls.tempAgg, 'r') as allIn:
        csvReader = csv.DictReader(allIn, delimiter=',')
        csvData = [dict(d) for d in csvReader]
        cls.data = DataprofileTestHelper(csvData)
        print(cls.data.df[
                ['targetIdentifier', 'targetISBN10', 'targetISBN13', 'targetKBRIdentifier', 'targetBnFIdentifier',
                 'targetKBIdentifier']])

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

# -----------------------------------------------------------------------------
class TestDataIntegrationManifestationsSPARQLConfigSingleUpdateCorrelationList(TestDataIntegrationManifestationsSPARQL, unittest.TestCase):

  def getData(self):
    return TestDataIntegrationManifestationsSPARQLConfigSingleUpdateCorrelationList.data

  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):
    # use temporary files which will be deleted in the tearDownClass function
    cls.tempAgg = os.path.join(tempfile.gettempdir(), 'aggregated-data.csv')
    cls.tempLogDir = os.path.join(tempfile.gettempdir(), 'integration-sparql-manifestation-test-log')
    os.makedirs(cls.tempLogDir)

    # start a local Blazegraph and insert our test data
    internalBlazegraphHostname = 'blz'
    with BlazegraphIntegrationTestContainer(imageName="data-integration_blazegraph-test",
                                            hostName=internalBlazegraphHostname) as blazegraph:
      time.sleep(10)

      loadConfig = {
        'http://beltrans-manifestations': ['./test/resources/data-integration-sparql/correlation-list-manifestations.ttl',
                                           './test/resources/data-integration-sparql/correlation-list-isbns.ttl'],
        'http://kbr-syracuse': ['./test/resources/data-integration-sparql/kbr-manifestations.ttl',
                                './test/resources/data-integration-sparql/kbr-isbns.ttl'],
        'http://bnf-publications': ['./test/resources/data-integration-sparql/bnf-manifestations.ttl',
                                './test/resources/data-integration-sparql/bnf-isbns.ttl'],
        'http://kb-publications': ['./test/resources/data-integration-sparql/kb-manifestations.ttl',
                                './test/resources/data-integration-sparql/kb-isbns.ttl'],
        'http://master-data': ['./test/resources/data-integration-sparql/master-data.ttl'],
        'http://kbr-originals': ['./test/resources/data-integration-sparql/kbr-originals.ttl'],
        'http://kb-originals': ['./test/resources/data-integration-sparql/kb-originals.ttl']
      }
      # uploadURL = 'http://' + internalBlazegraphHostname + '/namespace/kb'
      uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
      utils.addTestData(uploadURL, loadConfig)

      # integrate the data (this integration we actually want to test)
      numberUpdates = 3
      integrateDataSPARQLConfigSingleUpdate(url=uploadURL, queryType='manifestations', targetGraph="http://beltrans-manifestations",
                                createQueriesConfig='config-integration-manifestations-create.csv',
                                updateQueriesConfig='config-integration-manifestations-single-update.csv',
                                numberUpdates=numberUpdates, queryLogDir=cls.tempLogDir)

      # query data from our test fixture
      with open(cls.tempAgg, 'wb') as resultFileAgg:
        queryAgg = utils.readSPARQLQuery('./sparql-queries/get-integrated-manifestations.sparql')
        # queryAgg = utils.readSPARQLQuery('sparql-queries/get-all.sparql')
        utils.query(uploadURL, queryAgg, resultFileAgg)

      # read and store the queried/integrated data such that we can easily use it in the test functions
      with open(cls.tempAgg, 'r') as allIn:
        csvReader = csv.DictReader(allIn, delimiter=',')
        csvData = [dict(d) for d in csvReader]
        cls.data = DataprofileTestHelper(csvData)
        print(cls.data.df[
                ['targetIdentifier', 'targetISBN10', 'targetISBN13', 'targetKBRIdentifier', 'targetBnFIdentifier',
                 'targetKBIdentifier']])

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


# -----------------------------------------------------------------------------
class TestDataIntegrationManifestationsClustering(TestDataIntegrationManifestationsSPARQL, unittest.TestCase):

  def getData(self):
    return TestDataIntegrationManifestationsClustering.data

  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):
    # use temporary files which will be deleted in the tearDownClass function
    cls.tempAgg = os.path.join(tempfile.gettempdir(), 'aggregated-data.csv')
    cls.tempLogDir = os.path.join(tempfile.gettempdir(), 'integration-sparql-manifestation-test-log')
    os.makedirs(cls.tempLogDir)

    # start a local Blazegraph and insert our test data
    internalBlazegraphHostname = 'blz'
    with BlazegraphIntegrationTestContainer(imageName="data-integration_blazegraph-test",
                                            hostName=internalBlazegraphHostname) as blazegraph:
      time.sleep(10)

      loadConfig = {
        'http://beltrans-manifestations': ['./test/resources/data-integration-sparql/correlation-list-manifestations.ttl',
                                           './test/resources/data-integration-sparql/correlation-list-isbns.ttl'],
        'http://kbr-syracuse': ['./test/resources/data-integration-sparql/kbr-manifestations.ttl',
                                './test/resources/data-integration-sparql/kbr-isbns.ttl'],
        'http://bnf-publications': ['./test/resources/data-integration-sparql/bnf-manifestations.ttl',
                                './test/resources/data-integration-sparql/bnf-isbns.ttl'],
        'http://kb-publications': ['./test/resources/data-integration-sparql/kb-manifestations.ttl',
                                './test/resources/data-integration-sparql/kb-isbns.ttl'],
        'http://master-data': ['./test/resources/data-integration-sparql/master-data.ttl'],
        'http://kbr-originals': ['./test/resources/data-integration-sparql/kbr-originals.ttl'],
        'http://kb-originals': ['./test/resources/data-integration-sparql/kb-originals.ttl']
      }
      # uploadURL = 'http://' + internalBlazegraphHostname + '/namespace/kb'
      uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
      utils.addTestData(uploadURL, loadConfig)

      # integrate the data (this integration we actually want to test)
      # TODO: call new implementation
      numberUpdates = 3
      integrateDataClustering(url=uploadURL, queryType='manifestations', targetGraph="http://beltrans-manifestations",
                                configFilename='config-integration-manifestations.json',
                                queryLogDir=cls.tempLogDir)

      # query data from our test fixture
      with open(cls.tempAgg, 'wb') as resultFileAgg:
        queryAgg = utils.readSPARQLQuery('./sparql-queries/get-integrated-manifestations.sparql')
        # queryAgg = utils.readSPARQLQuery('sparql-queries/get-all.sparql')
        utils.query(uploadURL, queryAgg, resultFileAgg)

      # read and store the queried/integrated data such that we can easily use it in the test functions
      with open(cls.tempAgg, 'r') as allIn:
        csvReader = csv.DictReader(allIn, delimiter=',')
        csvData = [dict(d) for d in csvReader]
        cls.data = DataprofileTestHelper(csvData)
        print(f'Results from clustering implementation')
        print(cls.data.df[
                ['targetIdentifier', 'targetISBN10', 'targetISBN13', 'targetKBRIdentifier', 'targetBnFIdentifier',
                 'targetKBIdentifier']])

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
