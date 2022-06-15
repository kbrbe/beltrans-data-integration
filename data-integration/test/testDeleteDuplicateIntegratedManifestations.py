import unittest
import tempfile
import time
import utils
import pandas as pd
import csv
import os
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
                cls.data = csvData
                print(pd.DataFrame(cls.data))

    # ---------------------------------------------------------------------------
    @classmethod
    def tearDownClass(cls):
        pass

    # ---------------------------------------------------------------------------
    def testOnlyDuplicateRemovedForISBN10(self):
        pass

    # ---------------------------------------------------------------------------
    def testOnlyDuplicateRemovedForISBN13(self):
        pass

    # ---------------------------------------------------------------------------
    def testOnlyDuplicateRemovedForISBN10AndISBN13(self):
        pass

    # ---------------------------------------------------------------------------
    def testMultipleDuplicatesRemovedForISBN10(self):
        pass

    # ---------------------------------------------------------------------------
    def testMultipleDuplicatesRemovedForISBN13(self):
        pass

    # ---------------------------------------------------------------------------
    def testMultipleDuplicatesRemovedForISBN10AndISBN13(self):
        pass