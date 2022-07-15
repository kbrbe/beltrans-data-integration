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
class TestDataprofileQueryThreeSources(unittest.TestCase):

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
        'http://beltrans-manifestations': ['./test/resources/beltrans-graph-data-three-sources/integrated-data.ttl'],
        'http://beltrans-contributors': ['./test/resources/beltrans-graph-data-three-sources/integrated-contributors.ttl'],
        'http://kbr-syracuse': ['./test/resources/beltrans-graph-data-three-sources/kbr-data.ttl'],
        'http://kbr-linked-authorities': ['./test/resources/beltrans-graph-data-three-sources/kbr-contributors.ttl'],
        'http://bnf-publications': ['./test/resources/beltrans-graph-data-three-sources/bnf-data.ttl'],
        'http://bnf-contributors': ['./test/resources/beltrans-graph-data-three-sources/bnf-contributors.ttl'],
        'http://kb-publications': ['./test/resources/beltrans-graph-data-three-sources/kb-data.ttl'],
        'http://kb-contributors': ['./test/resources/beltrans-graph-data-three-sources/kb-contributors.ttl'],
        'http://master-data': ['./test/resources/beltrans-graph-data-three-sources/master-data.ttl'],
      }
      #uploadURL = 'http://' + internalBlazegraphHostname + '/namespace/kb'
      uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
      utils.addTestData(uploadURL, loadConfig)

      # query data from our test fixture
      with open(cls.tempAgg, 'wb') as resultFileAgg:

        queryAgg = utils.readSPARQLQuery('./dataprofile-aggregated.sparql')
        #queryAgg = utils.readSPARQLQuery('sparql-queries/get-all.sparql')
        utils.query(uploadURL, queryAgg, resultFileAgg)

      # read and store the queried/integrated data such that we can easily use it in the test functions
      with open(cls.tempAgg, 'r') as allIn:
        csvReader = csv.DictReader(allIn, delimiter=',')
        csvData = [dict(d) for d in csvReader]
        cls.data = DataprofileTestHelper(csvData)
        print(cls.data.df[['targetIdentifier', 'targetKBRIdentifier', 'targetBnFIdentifier', 'targetKBIdentifier', 'authorIdentifiers']])
    
  # ---------------------------------------------------------------------------
  @classmethod
  def tearDownClass(cls):
    if os.path.isfile(cls.tempAgg):
      os.remove(cls.tempAgg)

  # ---------------------------------------------------------------------------
  def testCorpusSize(self):
    """This function tests if the number of corpus rows is correct, thus that a book from KBR and BnF is matched in the same row if ISBN10 or ISBN13 match."""
    self.assertEqual(TestDataprofileQueryThreeSources.data.numberRows(), 6, msg="Corpus too big or too small")

  # ---------------------------------------------------------------------------
  def testIfAllBooksFound(self):
    """This function tests if the corpus contains all needed identifiers, not if they are properly matched to KBR/BnF/KB."""
    bookIDs = [1,2,3,4,7,8]
    results = {}
    for i in bookIDs:
      results[i] = TestDataprofileQueryThreeSources.data.targetIdentifierExists(f'Book {i}')

    errors = {key: value for key, value in results.items() if value is not True} 
    self.assertEqual(len(errors), 0, msg=f'books which are missing: {errors}')


  # ---------------------------------------------------------------------------
  def testIfAllKBRBooksFound(self):
    """This function tests if the corpus contains all needed KBR identifiers, not if they are properly matched to BnF/KB."""
    bookIDs = [1,3,7,8]
    results = {}
    for i in bookIDs:
      results[i] = TestDataprofileQueryThreeSources.data.kbrTargetIdentifierExists(f'KBR book {i}')

    errors = {key: value for key, value in results.items() if value is not True} 
    self.assertEqual(len(errors), 0, msg=f'KBR books which are missing: {errors}')

  # ---------------------------------------------------------------------------
  def testIfAllBnFBooksFound(self):
    """This function tests if the corpus contains all needed BnF identifiers, not if they are properly matched to KBR/KB."""
    bookIDs = [2,7]
    results = {}
    for i in bookIDs:
      results[i] = TestDataprofileQueryThreeSources.data.bnfTargetIdentifierExists(f'BnF book {i}')

    errors = {key: value for key, value in results.items() if value is not True} 
    self.assertEqual(len(errors), 0, msg=f'BnF books which are missing: {errors}')

  # ---------------------------------------------------------------------------
  def testIfAllKBBooksFound(self):
    """This function tests if the corpus contains all needed KB identifiers, not if they are properly matched to KBR/BnF."""
    bookIDs = [2,4,8]
    results = {}
    for i in bookIDs:
      results[i] = TestDataprofileQueryThreeSources.data.kbTargetIdentifierExists(f'KB book {i}')

    errors = {key: value for key, value in results.items() if value is not True} 
    self.assertEqual(len(errors), 0, msg=f'KB books which are missing: {errors}')

  # ---------------------------------------------------------------------------
  def testIfBooksFiltered(self):
    """This function tests if KBR books not matching the Belgian contributor criteria are filtered out."""
    bookIDs = [5,6]
    results = {}
    for i in bookIDs:
      results[i] = TestDataprofileQueryThreeSources.data.targetIdentifierExists(f'Book {i}')

    errors = {key: value for key, value in results.items() if value is not False} 
    self.assertEqual(len(errors), 0, msg=f'Books which should have been filtered out: {errors}')


  # ---------------------------------------------------------------------------
  def testIfKBRBooksFiltered(self):
    """This function tests if KBR books not matching the Belgian contributor criteria are filtered out."""
    bookIDs = []
    results = {}
    for i in bookIDs:
      results[i] = TestDataprofileQueryThreeSources.data.kbrTargetIdentifierExists(f'KBR book {i}')

    errors = {key: value for key, value in results.items() if value is not False} 
    self.assertEqual(len(errors), 0, msg=f'KBR books which should have been filtered out: {errors}')


  # ---------------------------------------------------------------------------
  def testIfBnFBooksFiltered(self):
    """This function tests if BnF books not matching the Belgian contributor criteria are filtered out."""
    bookIDs = [5,6]
    results = {}
    for i in bookIDs:
      results[i] = TestDataprofileQueryThreeSources.data.bnfTargetIdentifierExists(f'BnF book {i}')

    errors = {key: value for key, value in results.items() if value is not False} 
    self.assertEqual(len(errors), 0, msg=f'BnF books which should have been filtered out: {errors}')

  # ---------------------------------------------------------------------------
  def testIfKBBooksFiltered(self):
    """This function tests if KB books not matching the Belgian contributor criteria are filtered out."""
    bookIDs = []
    results = {}
    for i in bookIDs:
      results[i] = TestDataprofileQueryThreeSources.data.kbTargetIdentifierExists(f'KB book {i}')

    errors = {key: value for key, value in results.items() if value is not False} 
    self.assertEqual(len(errors), 0, msg=f'KB books which should have been filtered out: {errors}')



  # ---------------------------------------------------------------------------
  def testMatchingKBRAndBnFBooks(self):
    """This function tests if books are matched via ISBN10 and/or ISBN13."""
    bookIDs = [7]
    results = {}
    for i in bookIDs:
      try:
        results[i] = TestDataprofileQueryThreeSources.data.kbrAndBnFIdentifierOnSameRow(f'KBR book {i}', f'BnF book {i}')
      except:
        results[i] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing KBR and BnF matches for the following books: {errors}')

  # ---------------------------------------------------------------------------
  def testMatchingKBRAndKBBooks(self):
    """This function tests if books are matched via ISBN10 and/or ISBN13."""
    bookIDs = [8]
    results = {}
    for i in bookIDs:
      try:
        results[i] = TestDataprofileQueryThreeSources.data.kbrAndKBIdentifierOnSameRow(f'KBR book {i}', f'KB book {i}')
      except:
        results[i] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing KBR and KB matches for the following books: {errors}')

  # ---------------------------------------------------------------------------
  def testMatchingKBAndBnFBooks(self):
    """This function tests if books are matched via ISBN10 and/or ISBN13."""
    bookIDs = [2]
    results = {}
    for i in bookIDs:
      try:
        results[i] = TestDataprofileQueryThreeSources.data.kbAndBnFIdentifierOnSameRow(f'KB book {i}', f'BnF book {i}')
      except:
        results[i] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Missing KB and BnF matches for the following books: {errors}')


  # ---------------------------------------------------------------------------
  def testAuthorIdentifiersBook1(self):
    """This function tests if all author identifiers are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsAuthorString('Book 1', '1BE'), msg=f'Book 1 misses contributor "1BE" as author')

  # ---------------------------------------------------------------------------
  def testAuthorNameBook1(self):
    """This function tests if all author names are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsAuthorString('Book 1', 'John Van 1BE'), msg=f'Book 1 misses the name "John Van 1BE"')



  # ---------------------------------------------------------------------------
  def testAuthorIdentifiersBook8(self):
    """This function tests if all author identifiers are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsAuthorString('Book 8', '11BE'), msg=f'Book 8 misses contributor "11BE" as author')

  # ---------------------------------------------------------------------------
  def testAuthorNameBook8(self):
    """This function tests if all author names are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsAuthorString('Book 8', 'Sophie Van 11BE'), msg=f'Book 8 misses the author name "Sophie Van 11BE"')



  # ---------------------------------------------------------------------------
  def testAuthorIdentifiersBook2(self):
    """This function tests if all author identifiers are queried."""
    authorIDs = ['2BE', '3FR']
    results = {}
    for aID in authorIDs:
      try:
        results[aID] = TestDataprofileQueryThreeSources.data.targetIdentifierContainsAuthorString('Book 2', aID)
      except:
        results[aID] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Book 2 misses authors: {errors}')

  # ---------------------------------------------------------------------------
  def testAuthorNamesBook2(self):
    """This function tests if all author names are queried."""
    authorIDs = ['Jane Van 2BE', 'Ann Van 3FR']
    results = {}
    for aID in authorIDs:
      try:
        results[aID] = TestDataprofileQueryThreeSources.data.targetIdentifierContainsAuthorString('Book 2', aID)
      except:
        results[aID] = 'Not in result'
    
    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'Book 2 misses author names: {errors}')




  # ---------------------------------------------------------------------------
  def testIllustratorIdentifiersBook3(self):
    """This function tests if all illustrator identifiers are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsIllustratorString('Book 3', '4BE'), msg=f'Book 3 misses contributor "4BE" as illustrator')

  # ---------------------------------------------------------------------------
  def testIllustratorNameBook3(self):
    """This function tests if all illustrator names are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsIllustratorString('Book 3', 'Joseph Van 4BE'), msg=f'Book 3 misses the illustrator name "Joseph Van 4BE"')



  # ---------------------------------------------------------------------------
  def testIllustratorIdentifiersBook7(self):
    """This function tests if all illustrator identifiers are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsIllustratorString('Book 7', '9BE'), msg=f'Book 7 misses "contributor 9 BE" as illustrator')

  # ---------------------------------------------------------------------------
  def testIllustratorNameBook7(self):
    """This function tests if all illustrator names are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsIllustratorString('Book 7', 'missing name'), msg=f'Book 7 misses illustrator name "missing name"')



  # ---------------------------------------------------------------------------
  def testIllustratorIdentifiersBook8(self):
    """This function tests if all illustrator identifiers are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsIllustratorString('Book 8', '11BE'), msg=f'Book 8 misses contributor "11BE" as illustrator')

  # ---------------------------------------------------------------------------
  def testIllustratorNameBook8(self):
    """This function tests if all illustrator names are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsIllustratorString('Book 8', 'Sophie Van 11BE'), msg=f'Book 8 misses illustrator "Sophie Van 11BE"')




  # ---------------------------------------------------------------------------
  def testScenaristIdentifiersBook4(self):
    """This function tests if all scenarist identifiers are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsScenaristString('Book 4', '5BE'), msg=f'Book 4 misses contributor "5BE" as scenarist')

  # ---------------------------------------------------------------------------
  def testScenaristNameBook4(self):
    """This function tests if all scenarist names are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsScenaristString('Book 4', 'Alice Van 5BE'), msg=f'Book 4 misses scenarist "5BE"')



  # ---------------------------------------------------------------------------
  def testScenaristIdentifiersBook7(self):
    """This function tests if all scenarist identifiers are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsScenaristString('Book 7', '10FR'), msg=f'Book 7 misses contributor "10FR" as scenarist')

  # ---------------------------------------------------------------------------
  def testScenaristNameBook7(self):
    """This function tests if all scenarist names are queried."""
    self.assertTrue(TestDataprofileQueryThreeSources.data.targetIdentifierContainsScenaristString('Book 7', 'Eduard Van 10FR'), msg=f'Book 7 misses scenarist "Eduard Van 10FR"')




if __name__ == '__main__':
  unittest.main()
