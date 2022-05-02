import unittest
import tempfile
import csv
import os
import utils
import subprocess
from countryEnrichmentTestHelper import CountryEnrichmentTestHelper

# Don't show the traceback of an AssertionError, because the AssertionError already says what the issue is!
__unittest = True

# -----------------------------------------------------------------------------
class TestCountryEnrichment(unittest.TestCase):

  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):
    cls.tempEnriched = os.path.join(tempfile.gettempdir(), 'country-enriched.csv')

    # Run the script whose output we want to test
    #
    venv = 'py-integration-env/bin/python'
    args = [venv, 
      'add_country.py',
      '-g', 'test/resources/country-enrichment/geonames/',
      '-i', 'test/resources/country-enrichment/testdata.csv',
      '-c', 'targetCountryOfPublication',
      '-p', 'targetPlaceOfPublication',
      '-o', cls.tempEnriched]
    subprocess.run(args)

    # read the script output into an internal data structure
    #
    with open(cls.tempEnriched, 'r') as fileIn:
      csvReader = csv.DictReader(fileIn, delimiter=',')
      csvData = [dict(d) for d in csvReader]
      cls.rawData = csvData
      cls.data = CountryEnrichmentTestHelper(csvData)


  # ---------------------------------------------------------------------------
  def testEmptyLocationEmptyCountry(self):
    """When the location column is empty, the country column should be empty too"""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("2")
    self.assertEqual(foundCountry, "", msg= f'For an empty location the country {foundCountry} was found instead of left empty')
    
  # ---------------------------------------------------------------------------
  def testBelgiumFoundForGhent(self):
    """When the location is Ghent the country should be Belgium"""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("1")
    self.assertEqual(foundCountry, "Belgium", msg= f'For the location Ghent the country was "{foundCountry}" instead of Belgium')

  # ---------------------------------------------------------------------------
  def testBelgiumFoundForBruxeles(self):
    """When the location is Bruxeles the country should be Belgium"""
    foundCountry = TestCountryEnrichment.data.getKBRdentifierCountry("4")
    self.assertEqual(foundCountry, "Belgium", msg= f'For the location Bruxeles the country was "{foundCountry}" instead of Belgium')

  # ---------------------------------------------------------------------------
  def testBelgiumFoundForBruxeles(self):
    """When the location is Brussels the country should be Belgium"""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("4")
    self.assertEqual(foundCountry, "Belgium", msg= f'For the location Brussels the country was "{foundCountry}" instead of Belgium')

  # ---------------------------------------------------------------------------
  def testCorrectKBRIDs(self):
    """The KBR identifiers of the input should be the same in the output."""
    identifiers = []
    for row in TestCountryEnrichment.rawData:
      identifiers.append(row['targetKBRIdentifier'])
    self.assertEqual(identifiers, ['1','2','3','4','5','123','6'], msg="Identifiers contain non expected values")

  # ---------------------------------------------------------------------------
  def testBelgiumFoundForGentWithCountryInParenthesis(self):
    """When the location is 'Gent (Belgium)' the country should be Belgium"""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("6")
    self.assertEqual(foundCountry, "Belgium", msg= f'For the location [Gent] the country was "{foundCountry}" instead of Belgium')

