import unittest
import tempfile
import time
import utils
import csv
import os
import integration
from dataprofileTestHelper import DataprofileTestHelper
from BlazegraphIntegrationTestContainer import BlazegraphIntegrationTestContainer
import pandas as pd

# Don't show the traceback of an AssertionError, because the AssertionError already says what the issue is!
__unittest = True

# -----------------------------------------------------------------------------
class TestTitleRepresentation(unittest.TestCase):

  # ---------------------------------------------------------------------------
  def getData(self):
    return TestTitleRepresentation.data

  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):

    # use temporary files which will be deleted in the tearDownClass function
    cls.tempTitles = os.path.join(tempfile.gettempdir(), 'queried-titles.csv')

    # start a local Blazegraph and insert our test data
    internalBlazegraphHostname = 'blz'
    with BlazegraphIntegrationTestContainer(imageName="data-integration_blazegraph-test",
                                            hostName=internalBlazegraphHostname) as blazegraph:
      time.sleep(10)

      loadConfig = {
        'http://kbr-syracuse': ['./test/resources/title-representation/kbr-data.ttl'],
        'http://bnf-publications': ['./test/resources/title-representation/bnf-data.ttl'],
        'http://kb-publications': ['./test/resources/title-representation/kb-data.ttl']
      }

      # uploadURL = 'http://' + internalBlazegraphHostname + '/namespace/kb'
      uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
      utils.addTestData(uploadURL, loadConfig)

      # run the update queries to adapt the titles which we want to test
      createTitlesQuery = utils.readSPARQLQuery('./sparql-queries/create-bibframe-titles.sparql')
      deriveSchemaNameQuery = utils.readSPARQLQuery('./sparql-queries/derive-single-title-from-bibframe-titles.sparql')

      # First create bibframe titles for records which do not have it
      utils.sparqlUpdate(uploadURL, createTitlesQuery)

      # Then the other way around, derive a single schema:name from bibframe titles
      # if there is not yet already a schema:name
      utils.sparqlUpdate(uploadURL, deriveSchemaNameQuery)

      # query data from our test fixture
      with open(cls.tempTitles, 'wb') as resultFileTitles:
        #queryTitles = utils.readSPARQLQuery('sparql-queries/get-all.sparql')
        queryTitles = utils.readSPARQLQuery('./sparql-queries/get-bibframe-titles.sparql')
        utils.query(uploadURL, queryTitles, resultFileTitles)

      # read and store the queried/integrated data such that we can easily use it in the test functions
      with open(cls.tempTitles, 'r') as allIn:
        csvReader = csv.DictReader(allIn, delimiter=',')
        csvData = [dict(d) for d in csvReader]
        cls.data = pd.DataFrame(csvData)
        print(cls.data)

  # ---------------------------------------------------------------------------
  @classmethod
  def tearDownClass(cls):
    if os.path.isfile(cls.tempTitles):
      os.remove(cls.tempTitles)

  # ---------------------------------------------------------------------------
  def testNumberResults(self):
    """This function tests that all books were retrieved."""
    self.assertEqual(len(self.getData()), 12, msg="Too less or too many books with bf:Title")


  # ---------------------------------------------------------------------------
  def testAllGotMainTitle(self):
    """This function tests if all KBR, BnF and KB books have a bf:mainTitle according to the BIBFRAME ontology."""

    titles = {
      'http://kbr.be/id/data/kbrBook1': 'A single title KBR',
      'http://kbr.be/id/data/kbrBook2': 'Data integration',
      'http://kbr.be/id/data/kbrBook3': 'Another title KBR',
      'http://kbr.be/id/data/kbrBook4': 'Yet another title KBR',  
      'http://kbr.be/id/data/bnfBook1': 'A single title BnF',
      'http://kbr.be/id/data/bnfBook2': 'Data integration',
      'http://kbr.be/id/data/bnfBook3': 'Another title BnF',
      'http://kbr.be/id/data/bnfBook4': 'Yet another title BnF',
      'http://kbr.be/id/data/kbBook1': 'A single title KB',
      'http://kbr.be/id/data/kbBook2': 'Data integration',
      'http://kbr.be/id/data/kbBook3': 'Another title KB',
      'http://kbr.be/id/data/kbBook4': 'Yet another title KB'
    }
    results = {}
    df = self.getData()
    for bookURI in titles:
      resultValue = df.loc[df['book'] == bookURI, 'mainTitle'].tolist()[0]
      results[bookURI] = resultValue == titles[bookURI]

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing main title for the following identifiers: {errors}')

  # ---------------------------------------------------------------------------
  def testNewSubtitles(self):
    """This function tests if the specified book records contain the specified subtitle as bf:subtitle."""

    subtitles = {
      'http://kbr.be/id/data/kbrBook2': 'another approach KBR',
      'http://kbr.be/id/data/kbrBook4': 'maybe the last of : one, two and three',  
      'http://kbr.be/id/data/bnfBook2': 'another approach BnF',
      'http://kbr.be/id/data/bnfBook4': 'maybe the last of : one, two and three',
      'http://kbr.be/id/data/kbBook2': 'another approach KB',
      'http://kbr.be/id/data/kbBook4': 'maybe the last of : one, two and three'
    }
    results = {}
    df = self.getData()
    for bookURI in subtitles:
      resultValue = df.loc[df['book'] == bookURI, 'subtitle'].tolist()[0]
      results[bookURI] = resultValue == subtitles[bookURI]

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing main title for the following identifiers: {errors}')



  # ---------------------------------------------------------------------------
  def testAllGotConcatenatedTitle(self):
    """This function tests if the specified book records contain the specified concatenated title as schema:name."""

    titles = {
      'http://kbr.be/id/data/kbrBook1': 'A single title KBR',
      'http://kbr.be/id/data/kbrBook2': 'Data integration : another approach KBR',
      'http://kbr.be/id/data/kbrBook3': 'Another title KBR',
      'http://kbr.be/id/data/kbrBook4': 'Yet another title KBR : maybe the last of : one, two and three',  
      'http://kbr.be/id/data/bnfBook1': 'A single title BnF',
      'http://kbr.be/id/data/bnfBook2': 'Data integration : another approach BnF',
      'http://kbr.be/id/data/bnfBook3': 'Another title BnF',
      'http://kbr.be/id/data/bnfBook4': 'Yet another title BnF : maybe the last of : one, two and three',
      'http://kbr.be/id/data/kbBook1': 'A single title KB',
      'http://kbr.be/id/data/kbBook2': 'Data integration : another approach KB',
      'http://kbr.be/id/data/kbBook3': 'Another title KB',
      'http://kbr.be/id/data/kbBook4': 'Yet another title KB : maybe the last of : one, two and three'
    }
    results = {}
    df = self.getData()
    for bookURI in titles:
      resultValue = df.loc[df['book'] == bookURI, 'altTitle'].tolist()[0]
      results[bookURI] = resultValue == titles[bookURI]

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing main title for the following identifiers: {errors}')



if __name__ == '__main__':
  unittest.main()
