import unittest
import tempfile
import time
import utils
import csv
import os
from dataprofileTestHelper import DataprofileTestHelper
from BlazegraphIntegrationTestContainer import BlazegraphIntegrationTestContainer

# Don't show the traceback of an AssertionError, because the AssertionError already says what the issue is!
__unittest = True

class TestDeleteDuplicateIntegratedManifestations(unittest.TestCase):

    # ---------------------------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        # use temporary files which will be deleted in the tearDownClass function
        cls.tempData = os.path.join(tempfile.gettempdir(), 'integrated-data.csv')

        # start a local Blazegraph and insert our test data
        internalBlazegraphHostname = 'blz'
        with BlazegraphIntegrationTestContainer(imageName="data-integration_blazegraph-test", hostName=internalBlazegraphHostname) as blazegraph:
            time.sleep(10)

            loadConfig = {
                'http://kb-publications':
                    ['./test/resources/duplicate-integrated-manifestations/local-contributors.ttl',
                     './test/resources/duplicate-integrated-manifestations/local-data.ttl'],
                'http://beltrans-contributors':
                    ['./test/resources/duplicate-integrated-manifestations/contributors-sameas.ttl',
                     './test/resources/duplicate-integrated-manifestations/integrated-contributors.ttl'],
                'http://master-data': ['./test/resources/duplicate-integrated-manifestations/master-data.ttl'],
                'http://beltrans-manifestations':
                    ['./test/resources/duplicate-integrated-manifestations/manifestations-sameas.ttl',
                    './test/resources/duplicate-integrated-manifestations/integrated-data.ttl']
            }
            uploadURL = 'http://localhost:8080/bigdata/namespace/kb/sparql'
            utils.addTestData(uploadURL, loadConfig)

            # perform the duplicate removing we want to test
            queryDelete = utils.readSPARQLQuery('./sparql-queries/delete-duplicate-manifestations.sparql')
            utils.sparqlUpdate(uploadURL, queryDelete)

            # query data from our test fixture
            with open(cls.tempData, 'wb') as resultFile:
                queryAll = utils.readSPARQLQuery('./dataprofile-aggregated.sparql')
                #queryAll = utils.readSPARQLQuery('sparql-queries/get-all.sparql')
                utils.query(uploadURL, queryAll, resultFile)

            # read and store the queried/integrated data such that we can easily use it in the test functions
            with open(cls.tempData, 'r') as allIn:
                csvReader = csv.DictReader(allIn, delimiter=',')
                csvData = [dict(d) for d in csvReader]
                cls.data = DataprofileTestHelper(csvData)
                print(cls.data.df[
                          ['targetIdentifier', 'targetISBN10', 'targetISBN13', 'authorIdentifiers', 'targetKBEdition', 'targetKBIdentifier', 'targetKBResponsibilityStatement']])

    # ---------------------------------------------------------------------------
    @classmethod
    def tearDownClass(cls):
        if os.path.isfile(cls.tempData):
            os.remove(cls.tempData)

    # ---------------------------------------------------------------------------
    # Unique books with ISBN10, ISBN13 and ISBN10 and ISBN13
    #
    def testUniqueBookForISBN10StillExists(self):
        """This function tests if the unique book with only an ISBN10 still exists."""
        identifierOfRepresentativeBook = 'i1'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(identifierOfRepresentativeBook),
            msg=f'Unique book with ISBN10 which should exist {identifierOfRepresentativeBook}')

    def testUniqueBookForISBN13StillExists(self):
        """This function tests if the unique book with only an ISBN13 still exists."""
        identifierOfRepresentativeBook = 'i2'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(identifierOfRepresentativeBook),
            msg=f'Unique book with ISBN13 which should exist {identifierOfRepresentativeBook}')

    def testUniqueBookForISBN10AndISBN13StillExists(self):
        """This function tests if the unique book with an ISBN10 and ISBN13 still exists."""
        identifierOfRepresentativeBook = 'i3'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(identifierOfRepresentativeBook),
            msg=f'Unique book with ISBN10 and ISBN13 which should exist {identifierOfRepresentativeBook}')


    # ---------------------------------------------------------------------------
    # Single duplicate books with ISBN10
    #
    def testSingleSurvivorForISBN10StillExists(self):
        """This function tests if one representative of the book with only an ISBN10 which had a single duplicate still exists."""
        identifierOfRepresentativeBook = 'i4'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(identifierOfRepresentativeBook),
            msg=f'Single representative with ISBN10 which should exist {identifierOfRepresentativeBook}')

    def testSingleDuplicateRemovedForISBN10(self):
        """This function tests if the only duplicate of the book with only an ISBN10 was removed."""
        identifierOfRemovedBook = 'i5'
        self.assertFalse(TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(identifierOfRemovedBook),
                        msg=f'Single duplicate with ISBN10 which should have been deleted {identifierOfRemovedBook}')

    def testSingleSurvivorLinksToAllEditionsForISBN10(self):
        """This function tests if the single representative of the book with only an ISBN10 links to all editions."""
        identifierOfRepresentativeBook = 'i4'
        identifierOfLinkedBooks = '4;5'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierContainsKBIdentifierString(identifierOfRepresentativeBook, identifierOfLinkedBooks),
            msg=f'Single representative {identifierOfRepresentativeBook} with ISBN10 which does not link to IDs of all editions {identifierOfLinkedBooks}')

    # ---------------------------------------------------------------------------
    # Single duplicate books with ISBN13
    #
    def testSingleSurvivorForISBN13StillExists(self):
        """This function tests if one representative of the book with only an ISBN13 which had a single duplicate still exists."""
        identifierOfRepresentativeBook = 'i6'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(identifierOfRepresentativeBook),
            msg=f'Single representative with ISBN13 which should exist {identifierOfRepresentativeBook}')

    def testSingleDuplicateRemovedForISBN13(self):
        """This function tests if the only duplicate of the book with only an ISBN13 was removed."""
        identifierOfRemovedBook = 'i7'
        self.assertFalse(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(identifierOfRemovedBook),
            msg=f'Single duplicate with ISBN13 which should have been deleted {identifierOfRemovedBook}')

    def testSingleSurvivorLinksToAllEditionsForISBN13(self):
        """This function tests if the single representative of the book with only an ISBN13 links to all editions."""
        identifierOfRepresentativeBook = 'i6'
        identifierOfLinkedBooks = '6;7'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierContainsKBIdentifierString(identifierOfRepresentativeBook, identifierOfLinkedBooks),
            msg=f'Single representative {identifierOfRepresentativeBook} with ISBN13 which does not link to IDs of all editions {identifierOfLinkedBooks}')


    # ---------------------------------------------------------------------------
    # Single duplicate books with ISBN10 and ISBN13
    #
    def testSingleSurvivorForISBN10AndISBN13StillExists(self):
        """This function tests if one representative of the book with an ISBN10 and ISBN13 which had a single duplicate still exists."""
        identifierOfRepresentativeBook = 'i8'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(identifierOfRepresentativeBook),
            msg=f'Single representative with ISBN10 and ISBN13 which should exist {identifierOfRepresentativeBook}')

    def testSingleDuplicateRemovedForISBN10AndISBN13(self):
        """This function tests if the only duplicate of the book with an ISBN10 and ISBN13 was removed."""
        identifierOfRemovedBook = 'i9'
        self.assertFalse(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(identifierOfRemovedBook),
            msg=f'Single duplicate with ISBN10 and ISBN13 which should have been deleted {identifierOfRemovedBook}')

    def testSingleSurvivorLinksToAllEditionsForISBN10AndISBN13(self):
        """This function tests if the single representative of the book with an ISBN10 and ISBN13 links to all editions."""
        identifierOfRepresentativeBook = 'i8'
        identifierOfLinkedBooks = '8;9'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierContainsKBIdentifierString(identifierOfRepresentativeBook, identifierOfLinkedBooks),
            msg=f'Single representative {identifierOfRepresentativeBook} with ISBN10 and ISBN13 which does not link to IDs of all editions {identifierOfLinkedBooks}')


    # ---------------------------------------------------------------------------
    # Several duplicate books with ISBN10
    #
    def testSurvivorForSeveralDuplicatesISBN10StillExists(self):
        """This function tests if one representative of the book with only an ISBN10 which had several duplicates still exists."""
        identifierOfRepresentativeBook = 'i10'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(identifierOfRepresentativeBook),
            msg=f'Single representative of several duplicates with ISBN10 which should exist {identifierOfRepresentativeBook}')

    def testMultipleDuplicatesRemovedForISBN10(self):
        """This function tests if all duplicates of the book with only an ISBN10 were removed."""
        bookIDs = ['i11', 'i12', 'i13']
        results = {}
        for i in bookIDs:
            results[i] = TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(i)

        errors = {key: value for key, value in results.items() if value is not False}
        self.assertEqual(len(errors), 0, msg=f'Duplicates with only ISBN10 which should have been deleted: {errors}')

    def testSurvivorForSeveralDuplicatesLinksToAllEditionsForISBN10(self):
        """This function tests if the single representative of the book with only an ISBN10 which had several duplicates links to all editions."""
        identifierOfRepresentativeBook = 'i10'
        identifierOfLinkedBooks = '10;11;12;13'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierContainsKBIdentifierString(identifierOfRepresentativeBook, identifierOfLinkedBooks),
            msg=f'Single representative {identifierOfRepresentativeBook} with ISBN10 which does not link to IDs of all editions {identifierOfLinkedBooks}')

    # ---------------------------------------------------------------------------
    # Several duplicate books with ISBN13
    #
    def testSurvivorForSeveralDuplicatesISBN13StillExists(self):
        """This function tests if one representative of the book with only an ISBN13 which had several duplicates still exists."""
        identifierOfRepresentativeBook = 'i14'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(identifierOfRepresentativeBook),
            msg=f'Single representative of several duplicates with ISBN13 which should exist {identifierOfRepresentativeBook}')

    def testMultipleDuplicatesRemovedForISBN13(self):
        """This function tests if all duplicates of the book with only an ISBN13 were removed."""
        bookIDs = ['i15', 'i16', 'i17']
        results = {}
        for i in bookIDs:
            results[i] = TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(i)

        errors = {key: value for key, value in results.items() if value is not False}
        self.assertEqual(len(errors), 0, msg=f'Duplicates with only ISBN13 which should have been deleted: {errors}')

    def testSurvivorForSeveralDuplicatesLinksToAllEditionsForISBN13(self):
        """This function tests if the single representative of the book with only an ISBN13 which had several duplicates links to all editions."""
        identifierOfRepresentativeBook = 'i14'
        identifierOfLinkedBooks = '14;15;16;17'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierContainsKBIdentifierString(identifierOfRepresentativeBook, identifierOfLinkedBooks),
            msg=f'Single representative {identifierOfRepresentativeBook} with ISBN13 which does not link to IDs of all editions {identifierOfLinkedBooks}')


    # ---------------------------------------------------------------------------
    # Several duplicate books with ISBN10 and ISBN13
    #
    def testSurvivorForSeveralDuplicatesISBN10AndISBN13StillExists(self):
        """This function tests if one representative of the book with an ISBN10 and ISBN13 which had several duplicates still exists."""
        identifierOfRepresentativeBook = 'i18'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(identifierOfRepresentativeBook),
            msg=f'Single representative of several duplicates with ISBN13 which should exist {identifierOfRepresentativeBook}')

    # ---------------------------------------------------------------------------
    def testMultipleDuplicatesRemovedForISBN10AndISBN13(self):
        """This function tests if all duplicates of the book with an ISBN10 and ISBN13 were removed."""
        bookIDs = ['i19', 'i20', 'i21']
        results = {}
        for i in bookIDs:
            results[i] = TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierExists(i)

        errors = {key: value for key, value in results.items() if value is not False}
        self.assertEqual(len(errors), 0,
                         msg=f'Duplicates with ISBN10 and ISBN13 which should have been deleted: {errors}')

    def testSurvivorForSeveralDuplicatesLinksToAllEditionsForISBN10AndISBN13(self):
        """This function tests if the single representative of the book with an ISBN10 and ISBN13 which had several duplicates links to all editions."""
        identifierOfRepresentativeBook = 'i18'
        identifierOfLinkedBooks = '18;19;20;21'
        self.assertTrue(
            TestDeleteDuplicateIntegratedManifestations.data.targetIdentifierContainsKBIdentifierString(identifierOfRepresentativeBook, identifierOfLinkedBooks),
            msg=f'Single representative {identifierOfRepresentativeBook} with ISBN10 and ISBN13 which does not link to IDs of all editions {identifierOfLinkedBooks}')
