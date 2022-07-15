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
  @classmethod
  def tearDownClass(cls):
    if os.path.isfile(cls.tempEnriched):
      os.remove(cls.tempEnriched)

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
  def testBelgiumFoundForBruxelles(self):
    """When the location is Bruxelles the country should be Belgium"""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("4")
    self.assertEqual(foundCountry, "Belgium", msg= f'For the location Bruxelles the country was "{foundCountry}" instead of Belgium')

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
      identifiers.append(row['targetIdentifier'])
    self.assertEqual(identifiers, ['1','2','3','4','5','123','6', '7', '8', '9', '10', '11','12', '13', '14', '15', '16'], msg="Identifiers contain non expected values")

  # ---------------------------------------------------------------------------
  def testBelgiumFoundForGentWithCountryInParenthesis(self):
    """When the location is 'Gent (Belgium)' the country should be Belgium"""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("6")
    self.assertEqual(foundCountry, "Belgium", msg= f'For the location "Gent (Belgium)" the country was "{foundCountry}" instead of Belgium')

  # ---------------------------------------------------------------------------
  def testGentLocationFoundForGentWithCountryInParenthesis(self):
    """When the location is 'Gent (Belgium)' the location should be Gent"""
    foundLocation = TestCountryEnrichment.data.getKBRIdentifierLocation("6")
    self.assertEqual(foundLocation, "Gent", msg= f'For the location "Gent (Belgium)" the main spelling of the location was "{foundLocation}" instead of Gent')

  # ---------------------------------------------------------------------------
  def testKeepCountry(self):
    """When the location is Bruges with country MyBelgium the country should not be altered"""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("3")
    self.assertEqual(foundCountry, "Belgium;MyBelgium", msg= f'For the location Bruges and country MyBelgium the country was "{foundCountry}" instead of "Belgium;MyBelgium"')

  # ---------------------------------------------------------------------------
  def testPlaceSeparatedWithPointHyphen(self):
    """When the location is 'Leuven. - Paris' the country should be 'Belgium;France'."""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("7")
    self.assertEqual(foundCountry, "Belgium;France", msg= f'For the location "Leuven. - Paris" the country was "{foundCountry}" instead of "Belgium;France"')

  # ---------------------------------------------------------------------------
  def testThreePlaceSeparatedWithSemicolon(self):
    """When the location is 'Paris;Tielt;Houten' the country should be 'France;Belgium;Netherlands'"""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("8")
    self.assertEqual(foundCountry, "Belgium;France;Netherlands", msg= f'For the location "Paris;Tielt;Houten" the country was "{foundCountry}" instead of "Belgium;France;Netherlands"')

  # ---------------------------------------------------------------------------
  def testPlaceSeparatedAndBrackets(self):
    """When the location is 'Antwerpen;[Grenoble]' the country should be 'Belgium;France'."""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("9")
    self.assertEqual(foundCountry, "Belgium;France", msg= f'For the location "Antwerpen;[Grenoble]" the country was "{foundCountry}" instead of "Belgium;France"')

  # ---------------------------------------------------------------------------
  def testPlaceInBrackets(self):
    """When the location is '[Brussel]' the country should be Belgium."""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("10")
    self.assertEqual(foundCountry, "Belgium", msg= f'For the location "[Brussel]" the country was "{foundCountry}" instead of "Belgium"')

  # ---------------------------------------------------------------------------
  def testOnlyFirstCountryGiven(self):
    """When the location is 'Antwerpen;Amsterdam' the country should be 'Belgium;Netherlands'."""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("11")
    self.assertEqual(foundCountry, "Belgium;Netherlands", msg= f'For the location "Antwerpen;Amsterdam" the country was "{foundCountry}" instead of "Belgium;Netherlands"')

  # ---------------------------------------------------------------------------
  def testOnlySecondCountryGiven(self):
    """When the location is 'Antwerpen;Amsterdam' the country should be 'Belgium;Netherlands'."""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("12")
    self.assertEqual(foundCountry, "Belgium;Netherlands", msg= f'For the location "Antwerpen;Amsterdam" the country was "{foundCountry}" instead of "Belgium;Netherlands"')

  # ---------------------------------------------------------------------------
  def testSeveralCountriesUnknownRemains(self):
    """When the location is 'Brussels;Berlin' the country should be 'Belgium;Germany' even if we do not have data about Germany but Germany is already provided, i.e. Belgium only added."""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("13")
    self.assertEqual(foundCountry, "Belgium;Germany", msg= f'For the location "Brussels;Berlin" the country was "{foundCountry}" instead of "Belgium;Germany"')

  # ---------------------------------------------------------------------------
  def testGentLocationNormalized(self):
    """When the location is 'Ghent' the location should be altered to 'Gent'."""
    foundLocation = TestCountryEnrichment.data.getKBRIdentifierLocation("123")
    self.assertEqual(foundLocation, "Gent", msg= f'For the location "Ghent" the altered location was "{foundLocation}" instead of "Gent"')

  # ---------------------------------------------------------------------------
  def testBruxellesLocationNormalized(self):
    """When the location is 'Bruxelles' the location should be altered to 'Brussels'."""
    foundLocation = TestCountryEnrichment.data.getKBRIdentifierLocation("4")
    self.assertEqual(foundLocation, "Brussels", msg= f'For the location "Bruxelles" the altered location was "{foundLocation}" instead of "Brussels"')

  # ---------------------------------------------------------------------------
  def testBerlinLocationNormalized(self):
    """When the location is 'Brussels;Berlin' the location should stay 'Brussels;Berlin'."""
    foundLocation = TestCountryEnrichment.data.getKBRIdentifierLocation("13")
    expectedLocation="Berlin;Brussels"
    self.assertEqual(foundLocation, expectedLocation, msg=f'For the location "Brussels;Berlin" the altered location was "{foundLocation}" instead of "{expectedLocation}"')

  # ---------------------------------------------------------------------------
  def testAartselaarRoubaixBracketsMixCountry(self):
    """When the location is '[Aartselaar (Belgique)]. - [Roubaix]' the country should be 'Belgium'."""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("14")
    expectedCountries = "Belgium;France"
    self.assertEqual(foundCountry, expectedCountries, msg=f'For the location "[Aartselaar (Belgique)]. - [Roubaix]" the country was "{foundCountry}" instead of "{expectedCountries}"')

  # ---------------------------------------------------------------------------
  def testAartselaarRoubaixBracketsMixLocationNormalized(self):
    """When the location is '[Aartselaar (Belgique)]. - [Roubaix]' the location should be altered to 'Aartselaar;Roubaix'."""
    foundLocation = TestCountryEnrichment.data.getKBRIdentifierLocation("14")
    expectedLocation = "Aartselaar;Roubaix"
    self.assertEqual(foundLocation, expectedLocation, msg=f'For the location "[Aartselaar (Belgique)]. - [Roubaix]" the altered location was "{foundLocation}" instead of "{expectedLocation}"')

  # ---------------------------------------------------------------------------
  def testDoubleParisCountry(self):
    """When the location is 'Paris. - [Paris]' the country should be 'Belgium'."""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("15")
    expectedCountry = "France"
    self.assertEqual(foundCountry, expectedCountry, msg=f'For the location "Paris. - [Paris]" the country was "{foundCountry}" instead of "{expectedCountry}"')

  # ---------------------------------------------------------------------------
  def testDoubleParisNormalized(self):
    """When the location is 'Paris. - [Paris]' the location should be altered to 'Paris'."""
    foundLocation = TestCountryEnrichment.data.getKBRIdentifierLocation("15")
    expectedLocation = 'Paris'
    self.assertEqual(foundLocation, expectedLocation, msg=f'For the location "Paris. - [Paris]" the altered location was "{foundLocation}" instead of "{expectedLocation}"')

  # ---------------------------------------------------------------------------
  def testMontrealQuebecCountry(self):
    """When the location is '[Montréal (Québec)]' the country should be 'Canada'."""
    foundCountry = TestCountryEnrichment.data.getKBRIdentifierCountry("16")
    expectedCountry = "Canada"
    self.assertEqual(foundCountry, expectedCountry, msg=f'For the location "[Montréal (Québec)]" the country was "{foundCountry}" instead of "{expectedCountry}"')

  # ---------------------------------------------------------------------------
  def testMontrealQuebecLocationNormalized(self):
    """When the location is '[Montréal (Québec)]' the location should be altered to 'Montréal'."""
    foundLocation = TestCountryEnrichment.data.getKBRIdentifierLocation("16")
    expectedLocation = 'Montréal'
    self.assertEqual(foundLocation, expectedLocation, msg=f'For the location "[Montréal (Québec)]" the altered location was "{foundLocation}" instead of "{expectedLocation}"')
