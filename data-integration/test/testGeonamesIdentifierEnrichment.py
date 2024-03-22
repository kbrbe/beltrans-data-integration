import unittest
import tempfile
import csv
import os
import utils
import subprocess
from geonameIdentifierEnrichmentTestHelper import GeonameIdentifierEnrichmentTestHelper

# Don't show the traceback of an AssertionError, because the AssertionError already says what the issue is!
__unittest = True

# -----------------------------------------------------------------------------
class TestGeonamesIdentifierEnrichment(unittest.TestCase):

  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):
    cls.tempEnriched = os.path.join(tempfile.gettempdir(), 'country-enriched.csv')

    # Run the script whose output we want to test
    #
    venv = 'py-integration-env/bin/python'
    args = [venv, 
      'add_coordinates.py',
      '-g', 'test/resources/geoname-identifier-enrichment/geonames/',
      '-i', 'test/resources/geoname-identifier-enrichment/testdata.csv',
      '-p', 'targetPlaceOfPublication',
      '--input-id-column', 'targetIdentifier',
      '--column-place', 'targetPlaceOfPublication',
      '--column-country', 'targetCountryOfPublication',
      '--column-identifier', 'targetPlaceOfPublicationIdentifier',
      '--column-longitude', 'targetPlaceOfPublicationLongitude',
      '--column-latitude', 'targetPlaceOfPublicationLatitude',
      '-o', cls.tempEnriched]
    subprocess.run(args)

    # read the script output into an internal data structure
    #
    with open(cls.tempEnriched, 'r') as fileIn:
      csvReader = csv.DictReader(fileIn, delimiter=',')
      csvData = [dict(d) for d in csvReader]
      cls.rawData = csvData
      cls.data = GeonameIdentifierEnrichmentTestHelper(csvData)

  # ---------------------------------------------------------------------------
  @classmethod
  def tearDownClass(cls):
    if os.path.isfile(cls.tempEnriched):
      os.remove(cls.tempEnriched)

  # ---------------------------------------------------------------------------
  def testEmptyLocationEmptyGeonameIdentifier(self):
    """When the location column is empty, the geoname identifier country column should be empty too"""
    foundIdentifier = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationIdentifier("2")
    self.assertEqual(foundIdentifier, "", msg= f'For an empty location the identifier {foundIdentifier} was found instead of left empty')

  def testEmptyLocationEmptyLatitude(self):
    """When the location column is empty, the target place of publication latitude column should be empty too"""
    foundLatitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLatitude("2")
    self.assertEqual(foundLatitude, "", msg= f'For an empty location the latitude {foundLatitude} was found instead of left empty')

  def testEmptyLocationEmptyLongitude(self):
    """When the location column is empty, the target place of publication longitude column should be empty too"""
    foundLongitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLongitude("2")
    self.assertEqual(foundLongitude, "", msg= f'For an empty location the longitude {foundLongitude} was found instead of left empty')

  def testEmptyLocationButStillCountry(self):
    """When the location column is empty but we have a country column, the country column should not be removed https://github.com/kbrbe/beltrans-data-integration/issues/252"""
    expectedCountry = 'Belgium'
    foundCountry = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierCountry("17")
    self.assertEqual(foundCountry, expectedCountry, f'There should be the country {expectedCountry}, but "{foundCountry}" was found')


  # ---------------------------------------------------------------------------
  def testIdentifierFoundForGhent(self):
    """When the location is Ghent the correct geoname identifier should be found"""
    foundIdentifier = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationIdentifier("1")
    self.assertEqual(foundIdentifier, "2797656", msg= f'For the location Ghent the identifier was "{foundIdentifier}" instead of 2797656')

  def testLongitudeFoundForGhent(self):
    """When the location is Ghent the correct longitude should be found"""
    foundLongitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLongitude("1")
    self.assertEqual(foundLongitude, "3.71667", msg= f'For the location Ghent the longitude was "{foundLongitude}" instead of 3.71667')

  def testLatitudeFoundForGhent(self):
    """When the location is Ghent the correct longitude should be found"""
    fountLatitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLatitude("1")
    self.assertEqual(fountLatitude, "51.05", msg= f'For the location Ghent the latitude was "{fountLatitude}" instead of 51.05')



  # ---------------------------------------------------------------------------
  def testIdentifierFoundForBruxelles(self):
    """When the location is Bruxelles the correct geoname identifier should be found"""
    foundIdentifier = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationIdentifier("4")
    self.assertEqual(foundIdentifier, "2800866", msg= f'For the location Bruxelles the identifier was "{foundIdentifier}" instead of 2800866')

  def testLongitudeFoundForBruxelles(self):
    """When the location is Bruxelles the correct longitude should be found"""
    foundLongitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLongitude("4")
    self.assertEqual(foundLongitude, "4.34878", msg= f'For the location Bruxelles the longitude was "{foundLongitude}" instead of 4.34878')

  def testLatitudeFoundForBruxelles(self):
    """When the location is Bruxelles the correct longitude should be found"""
    fountLatitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLatitude("4")
    self.assertEqual(fountLatitude, "50.85045", msg= f'For the location Bruxelles the latitude was "{fountLatitude}" instead of 50.85045')



  # ---------------------------------------------------------------------------
  def testCorrectKBRIDs(self):
    """The KBR identifiers of the input should be the same in the output."""
    identifiers = []
    for row in TestGeonamesIdentifierEnrichment.rawData:
      identifiers.append(row['targetIdentifier'])
    self.assertEqual(identifiers, ['1','2','3','4','5','123','6', '7', '7', '8', '8', '8', '9', '9', '10', '11', '11', '12', '12', '13', '13', '14', '14', '15', '16', '17'], msg="Identifiers contain non expected values")


  # ---------------------------------------------------------------------------
  def testIdentifierFoundForGentWithCountryInParenthesis(self):
    """When the location is 'Gent (Belgium)' the correct geoname identifier should be found"""
    foundIdentifier = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationIdentifier("6")
    self.assertEqual(foundIdentifier, "2797656", msg= f'For the location "Gent (Belgium)" the identifier was "{foundIdentifier}" instead of 2797656 ')

  def testLongitudeFoundForGentWithCountryInParenthesis(self):
    """When the location is 'Gent (Belgium)' the correct longitude should be found"""
    foundLongitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLongitude("6")
    self.assertEqual(foundLongitude, "3.71667", msg= f'For the location Ghent the longitude was "{foundLongitude}" instead of 3.71667')

  def testLatitudeFoundForGentWithCountryInParenthesis(self):
    """When the location is 'Gent (Belgium)' the correct longitude should be found"""
    fountLatitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLatitude("6")
    self.assertEqual(fountLatitude, "51.05", msg= f'For the location Ghent the latitude was "{fountLatitude}" instead of 51.05')


  # ---------------------------------------------------------------------------
  def testIdentifierFoundForPlaceSeparatedWithPointHyphen(self):
    """When the location is 'Leuven. - Paris' the correct geoname identifiers should be found."""
    expectedIDs = ['2792482', '2988507']
    results = {}
    for i in expectedIDs:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationIdentifierExistsforTargetIdentifier(i, "7")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'geoname identifiers which are missing: {errors}')

  def testLongitudeFoundForPlaceSeparatedWithPointHyphen(self):
    """When the location is 'Leuven. - Paris' the correct longitude should be found"""
    expectedLongitudes = ['4.70093', '2.3488']
    results = {}
    for i in expectedLongitudes:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationLongitudeExistsforTargetIdentifier(i, "7")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'longitudes for "Leuven. - Paris" which are missing: {errors}')

  def testLatitudeFoundForPlaceSeparatedWithPointHyphen(self):
    """When the location is 'Leuven. - Paris' the correct latitudes should be found"""
    expectedLatitudes = ['50.87959', '48.85341']
    results = {}
    for i in expectedLatitudes:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationLatitudeExistsforTargetIdentifier(i, "7")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'latitudes for "Leuven. - Paris" which are missing: {errors}')


  # ---------------------------------------------------------------------------
  def testIdentifierFoundForThreePlaceSeparatedWithSemicolon(self):
    """When the location is 'Paris;Tielt;Houten' the correct geoname identifiers should be found."""
    expectedIDs = ['2988507', '2785477', '2753557']
    results = {}
    for i in expectedIDs:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationIdentifierExistsforTargetIdentifier(i, "8")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'geoname identifiers for "Paris;Tielt;Houten" which are missing: {errors}')

  def testLongitudeFoundForThreePlaceSeparatedWithSemicolon(self):
    """When the location is 'Paris;Tielt;Houten' the correct longitude should be found"""
    expectedLongitudes = ['2.3488', '4.90505', '5.16806']
    results = {}
    for i in expectedLongitudes:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationLongitudeExistsforTargetIdentifier(i, "8")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'longitudes for "Paris;Tielt;Houten" which are missing: {errors}')

  def testLatitudeFoundForThreePlaceSeparatedWithSemicolon(self):
    """When the location is 'Paris;Tielt;Houten' the correct latitudes should be found"""
    expectedLatitudes = ['48.85341', '50.9421', '52.02833']
    results = {}
    for i in expectedLatitudes:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationLatitudeExistsforTargetIdentifier(i, "8")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'latitudes for "Paris;Tielt;Houten" which are missing: {errors}')


  # ---------------------------------------------------------------------------
  def testIdentifierFoundForPlaceSeparatedAndBrackets(self):
    """When the location is 'Antwerpen;[Grenoble]' the correct geoname identifiers should be found."""
    expectedIDs = ['2803138', '3014728']
    results = {}
    for i in expectedIDs:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationIdentifierExistsforTargetIdentifier(i, "9")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'geoname identifiers for "Antwerpen;[Grenoble]" which are missing: {errors}')

  def testLongitudeFoundForPlaceSeparatedAndBrackets(self):
    """When the location is 'Antwerpen;[Grenoble]' the correct longitude should be found"""
    expectedLongitudes = ['4.40026', '5.71479']
    results = {}
    for i in expectedLongitudes:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationLongitudeExistsforTargetIdentifier(i, "9")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'longitudes for "Antwerpen;[Grenoble]" which are missing: {errors}')

  def testLatitudeFoundForPlaceSeparatedAndBrackets(self):
    """When the location is 'Antwerpen;[Grenoble]' the correct latitudes should be found"""
    expectedLatitudes = ['51.22047', '45.17869']
    results = {}
    for i in expectedLatitudes:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationLatitudeExistsforTargetIdentifier(i, "9")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'latitudes for "Antwerpen;[Grenoble]" which are missing: {errors}')



  # ---------------------------------------------------------------------------
  def testIdentifierFoundForPlaceInBrackets(self):
    """When the location is '[Brussel]' the correct geoname identifier should be found"""
    foundIdentifier = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationIdentifier("10")
    self.assertEqual(foundIdentifier, "2800866", msg=f'For the location "[Brussel]" the identifier was "{foundIdentifier}" instead of 2800866')

  def testLongitudeFoundForPlaceInBrackets(self):
    """When the location is '[Brussel]' the correct longitude should be found"""
    foundLongitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLongitude("10")
    self.assertEqual(foundLongitude, "4.34878", msg= f'For the location "[Brussel]" the longitude was "{foundLongitude}" instead of 3.71667')

  def testLatitudeFoundForPlaceInBrackets(self):
    """When the location is '[Brussel]' the correct longitude should be found"""
    fountLatitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLatitude("10")
    self.assertEqual(fountLatitude, "50.85045", msg= f'For the location "[Brussel]" the latitude was "{fountLatitude}" instead of 51.05')


  # ---------------------------------------------------------------------------
  def testEmptyIdentifierForUnknownPlace(self):
    """When the location is 'Brussels;Berlin' and we only have an identifier for Brussels, Berlin should get an empty identifier."""
    expectedIDs = ['2800866', '']
    results = {}
    for i in expectedIDs:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationIdentifierExistsforTargetIdentifier(i, "13")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'geoname identifiers for "Brussels;Berlin" which are missing (there should be one empty): {errors}')

  def testEmptyLongitudeForUnknownPlace(self):
    """When the location is 'Brussels;Berlin' the correct longitude should be found"""
    expectedLongitudes = ['4.34878', '']
    results = {}
    for i in expectedLongitudes:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationLongitudeExistsforTargetIdentifier(i, "13")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'longitudes for "Brussels;Berlin" which are missing (there should be one empty): {errors}')

  def testEmptyLatitudeForUnknownPlace(self):
    """When the location is 'Brussels;Berlin' the correct latitudes should be found"""
    expectedLatitudes = ['50.85045', '']
    results = {}
    for i in expectedLatitudes:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationLatitudeExistsforTargetIdentifier(i, "13")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'latitudes for "Brussels;Berlin" which are missing (there should be one empty): {errors}')

  # ---------------------------------------------------------------------------
  def testIdentifierFoundForAartselaarRoubaixBracketsMix(self):
    """When the location is '[Aartselaar (Belgique)]. - [Roubaix]","Belgium' and we only have an identifier for Brussels, Berlin should get an empty identifier."""
    expectedIDs = ['2803420', '2982681']
    results = {}
    for i in expectedIDs:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationIdentifierExistsforTargetIdentifier(i, "14")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'geoname identifiers for "[Aartselaar (Belgique)]" which are missing: {errors}')

  def testLongitudeFoundForAartselaarRoubaixBracketsMix(self):
    """When the location is '[Aartselaar (Belgique)]. - [Roubaix]","Belgium' the correct longitude should be found"""
    expectedLongitudes = ['4.38678', '3.17456']
    results = {}
    for i in expectedLongitudes:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationLongitudeExistsforTargetIdentifier(i, "14")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'longitudes for "[Aartselaar (Belgique)]. - [Roubaix]" which are missing: {errors}')

  def testLatitudeFoundForAartselaarRoubaixBracketsMix(self):
    """When the location is '[Aartselaar (Belgique)]. - [Roubaix]"' the correct latitudes should be found"""
    expectedLatitudes = ['51.13412', '50.69421']
    results = {}
    for i in expectedLatitudes:
      results[i] = TestGeonamesIdentifierEnrichment.data.placeOfPublicationLatitudeExistsforTargetIdentifier(i, "14")

    errors = {key: value for key, value in results.items() if value is not True}
    self.assertEqual(len(errors), 0, msg=f'latitudes for "[Aartselaar (Belgique)]. - [Roubaix]" which are missing: {errors}')

  # ---------------------------------------------------------------------------
  def testIdentifierFoundForDoubleParis(self):
    """When the location is 'Paris. - [Paris]","Belgium' and we only have an identifier for Brussels, Berlin should get an empty identifier."""
    foundIdentifier = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationIdentifier("15")
    expectedIdentifier = '2988507'
    self.assertEqual(foundIdentifier, expectedIdentifier, msg=f'For the location "Paris. - [Paris]","Belgium" the identifier was "{foundIdentifier}" instead of "{expectedIdentifier}')

  def testLongitudeFoundForDoubleParis(self):
    """When the location is 'Paris. - [Paris]',"Belgium' the correct longitude should be found"""
    foundLongitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLongitude("15")
    expectedLongitude = '2.3488'
    self.assertEqual(foundLongitude, expectedLongitude, msg=f'For the location "Paris. - [Paris]","Belgium" the longitude was "{foundLongitude}" instead of "{expectedLongitude}"')

  def testLatitudeFoundForDoubleParis(self):
    """When the location is 'Paris. - [Paris]' the correct latitudes should be found"""
    foundLatitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLatitude("15")
    expectedLatitude = '48.85341'
    self.assertEqual(foundLatitude, expectedLatitude, msg=f'For the location "Paris. - [Paris]","Belgium" the longitude was "{foundLatitude}" instead of "{expectedLatitude}"')

  # ---------------------------------------------------------------------------
  def testIdentifierShouldBeFoundForMontrealQuebec(self):
    """When the location is '[Montréal (Québec)]' the correct identifier from Canada should be found."""
    foundIdentifier = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationIdentifier("16")
    expectedIdentifier = '6077243'
    self.assertEqual(foundIdentifier, expectedIdentifier, msg=f'For the location "[Montréal (Québec)]","Belgium" the identifier was "{foundIdentifier}" instead of left empty')

  def testIdentifierShouldBeFoundForMontrealQuebec(self):
    """When the location is '[Montréal (Québec)]' the correct longitude should be found"""
    foundLongitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLongitude("16")
    expectedLongitude = '-73.58781'
    self.assertEqual(foundLongitude, expectedLongitude, msg=f'For the location "[Montréal (Québec)]","Belgium" the longitude was "{foundLongitude}" instead of left empty')

  def testIdentifierShouldBeFoundForMontrealQuebec(self):
    """When the location is '[Montréal (Québec)]' the correct latitudes should be found"""
    foundLatitude = TestGeonamesIdentifierEnrichment.data.getTargetIdentifierPlaceOfPublicationLatitude("16")
    expectedLatitude = '45.50884'
    self.assertEqual(foundLatitude, expectedLatitude, msg=f'For the location "[Montréal (Québec)]","Belgium" the longitude was "{foundLatitude}" instead of left empty')

