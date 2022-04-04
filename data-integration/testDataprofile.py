import unittest
import tempfile
import rdflib
import time
import utils
import csv
import os
from dataprofileTestHelper import DataprofileTestHelper
from BlazegraphIntegrationTestContainer import BlazegraphIntegrationTestContainer


# -----------------------------------------------------------------------------
class TestAggregatedDataKBRAndBnF(unittest.TestCase):

  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):
    # use temporary files which will be deleted in the tearDownClass function
    cls.tempAggKBR = os.path.join(tempfile.gettempdir(), 'aggregated-kbr.csv')
    cls.tempAggBnF = os.path.join(tempfile.gettempdir(), 'aggregated-kbr.csv')
    cls.tempAggAll = os.path.join(tempfile.gettempdir(), 'aggregated-data.csv')

    # start a local Blazegraph and insert our test data
    internalBlazegraphHostname='blz'
    with BlazegraphIntegrationTestContainer(imageName="data-integration_blazegraph-test", hostName=internalBlazegraphHostname) as blazegraph:
      time.sleep(10)      

      loadConfig = {
        'http://kbr-syracuse': './test/resources/kbr-data.ttl',
        'http://master-data': './test/resources/master-data.ttl',
        'http://bnf-publications': './test/resources/bnf-data.ttl',
        'http://bnf-contributors': './test/resources/bnf-contributors.ttl',
        'http://kbr-linked-authorities': './test/resources/kbr-linked-authorities.ttl',
  #      'http://isni-sru': './test/resources/isni-sru.ttl',
  #      'http://isni-rdf': './test/resources/isni-rdf.ttl'
      }
      #uploadURL = 'http://' + internalBlazegraphHostname + '/namespace/kb'
      uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
      utils.addTestData(uploadURL, loadConfig)

      # query data from our test fixture
      with open(cls.tempAggKBR, 'wb') as resultFileAggKBR:
      # todo: query KBR and store data
        queryAggKBR = utils.readSPARQLQuery('./dataprofile-aggregated-kbr.sparql')
        #queryAggKBR = utils.readSPARQLQuery('./get-all.sparql')
        utils.query(uploadURL, queryAggKBR, resultFileAggKBR)

      with open(cls.tempAggKBR, 'r') as kbrIn:
        csvReader = csv.DictReader(kbrIn, delimiter=',')
        csvData = [dict(d) for d in csvReader]
        cls.data = DataprofileTestHelper(csvData)
    # todo: query BnF
    # todo: postprocessing
    
    # read the CSV query result into our own data structure
    #with open(csvResultFilename, 'r') as dataIn:
    #  csvReader = csv.DictReader(dataIn, delimiter=',')
    #  csvData = [dict(d) for d in csvReader]
    #  cls.data = DataprofileTestHelper(csvData)

  # ---------------------------------------------------------------------------
  @classmethod
  def tearDownClass(cls):
    if os.path.isfile(cls.tempAggKBR):
      print(os.path.getsize(cls.tempAggKBR))
      os.remove(cls.tempAggKBR)
    if os.path.isfile(cls.tempAggBnF):
      os.remove(cls.tempAggBnF)
    if os.path.isfile(cls.tempAggAll):
      os.remove(cls.tempAggAll)

  # ---------------------------------------------------------------------------
  def testKBRBnFLinkFoundWithISBN10(self):
    print(f'testISBN10, tmp dir is {TestAggregatedDataKBRAndBnF.tempAggAll}')
    print(TestAggregatedDataKBRAndBnF.data.numberRows())

  # ---------------------------------------------------------------------------
  def testKBRBnFLinkFoundWithISBN13(self):
    print(f'testISBN13, tmp dir is {TestAggregatedDataKBRAndBnF.tempAggAll}')

  # ---------------------------------------------------------------------------
  def testKBRBnFLinkFoundWithISBN10And13(self):
    pass

if __name__ == '__main__':
  unittest.main()
