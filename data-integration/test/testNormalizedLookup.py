import unittest
import tempfile
import csv
import os
import utils
import subprocess
from tools.csv.normalized_lookup import main as lookup

# Don't show the traceback of an AssertionError, because the AssertionError already says what the issue is!
__unittest = True

# -----------------------------------------------------------------------------
def getNumberOfRows(filename):
  with open(filename, 'r') as inFile:
    return sum(1 for l in inFile)

# -----------------------------------------------------------------------------
def getColumnValues(filename, columnName):
  with open(filename, 'r') as inFile:
    reader = csv.DictReader(inFile, delimiter=',')
    return sorted({s[columnName] for s in reader})


# -----------------------------------------------------------------------------
class TestNormalizedLookup(unittest.TestCase):

  # ---------------------------------------------------------------------------
  def setUp(self):
    self.outputFile = os.path.join(tempfile.gettempdir(), 'looked-up-values.csv')

  # ---------------------------------------------------------------------------
  def tearDown(self):
    if os.path.isfile(self.outputFile):
      os.remove(self.outputFile)

  # ---------------------------------------------------------------------------
  def testMissingColumnWarningInputFile(self):
    """When a column is missing in the input file, an early warning should be created"""
    with self.assertRaises(Exception):
      lookup(
        inputFilename='./test/resources/tools/genres.csv', 
        lookupFilename='./test/resources/tools/genre-lookup.csv',
        outputFilename=self.outputFile,
        lookupKeyColumn="unknown-column",
        lookupValueColumn="id",
        inputKeyColumn="genre",
        inputIDColumn="manifestationID",
        outputValueColumn="genreID",
        inputDelimiter=",",
        lookupDelimiter=";")

  # ---------------------------------------------------------------------------
  def testMissingColumnWarningLookupFile(self):
    """When a column is missing in the lookup file, an early warning should be created"""
    with self.assertRaises(Exception):
      lookup(
        inputFilename='./test/resources/tools/genres.csv', 
        lookupFilename='./test/resources/tools/genre-lookup.csv',
        outputFilename=self.outputFile,
        lookupKeyColumn="unknown-column",
        lookupValueColumn="id",
        inputKeyColumn="genre",
        inputIDColumn="manifestationID",
        outputValueColumn="genreID",
        inputDelimiter=",",
        lookupDelimiter=";")



  # ---------------------------------------------------------------------------
  def testLookupExactAndNormalizedMatch(self):
    """When the lookup values are the same, a match should be found"""
    lookup(
      inputFilename='./test/resources/tools/genres.csv', 
      lookupFilename='./test/resources/tools/genre-lookup.csv',
      outputFilename=self.outputFile,
      lookupKeyColumn="name",
      lookupValueColumn="id",
      inputKeyColumn="genre",
      inputIDColumn="manifestationID",
      outputValueColumn="genreID",
      inputDelimiter=",",
      lookupDelimiter=";")

    expectedValues = ['LEXICON_00000014', 'LEXICON_00000085', 'LEXICON_00000090']
    self.assertListEqual(getColumnValues(self.outputFile, "genreID"), expectedValues, msg="Missing values for lookup")


