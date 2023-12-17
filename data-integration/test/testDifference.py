import unittest
import tempfile
import csv
import os
import utils
import subprocess
from tools.csv.difference import main as diff

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
class TestDifference(unittest.TestCase):

  # ---------------------------------------------------------------------------
  def setUp(self):
    self.outputFile = os.path.join(tempfile.gettempdir(), 'computed-diff.csv')

  # ---------------------------------------------------------------------------
  def tearDown(self):
    if os.path.isfile(self.outputFile):
      os.remove(self.outputFile)

  # ---------------------------------------------------------------------------
  def testInvalidCombinationOfMinusOperators(self):
    """When both minus flags are set to true the script should exit with error code 1"""
    with self.assertRaises(SystemExit):
      inputFile1 = './test/resources/tools/persons.csv'
      inputFile2 = './test/resources/tools/persons-duplicate-of-persons-with-added-identifiers.csv'
      diff([inputFile1, inputFile2], self.outputFile, "id", True, True, ['missing-column-name'], ",")
    
  # ---------------------------------------------------------------------------
  def testMissingColumnWarningSingleColumn(self):
    """When the single provided column is missing in one of the input files, an early warning should be created"""
    with self.assertRaises(Exception):
      inputFile1 = './test/resources/tools/persons.csv'
      inputFile2 = './test/resources/tools/persons-duplicate-of-persons-with-added-identifiers.csv'
      diff([inputFile1, inputFile2], self.outputFile, "id", True, False, ['missing-column-name'], ",")

  # ---------------------------------------------------------------------------
  def testMissingColumnWarningMultipleColumns(self):
    """When a column is missing in one of the input files, an early warning should be created"""
    with self.assertRaises(Exception):
      inputFile1 = './test/resources/tools/persons.csv'
      inputFile2 = './test/resources/tools/persons-duplicate-of-persons-with-added-identifiers.csv'
      diff([inputFile1, inputFile2], self.outputFile, "id", True, False, ['authorityID', 'contributorID'], ",")
    
  # ---------------------------------------------------------------------------
  def testCorrectMinusRestDifferenceTwoInputs(self):
    """When two input files and the minusRest options are given, the output should be all identifiers of the first minus the ones in the second file."""
    inputFile1 = './test/resources/tools/persons.csv'
    inputFile2 = './test/resources/tools/persons-duplicate-of-persons-with-added-identifiers.csv'
    outputColumnName = "id"
    diff([inputFile2, inputFile1], self.outputFile, outputColumnName, True, False, ['authorityID'], ",")
    expectedValues = ['111','222']
    self.assertListEqual(getColumnValues(self.outputFile, outputColumnName), expectedValues, msg="Wrong minusRest result")

  # ---------------------------------------------------------------------------
  def testCorrectMinusRestDifferenceMultipleInputs(self):
    """When multiple input files and the minusRest options are given, the output should be all identifiers of the first minus the union of the ones in the rest."""
    inputFile1 = './test/resources/tools/persons.csv'
    inputFile2 = './test/resources/tools/persons-duplicate-of-persons-with-added-identifiers.csv'
    inputFile3 = './test/resources/tools/other-persons.csv'
    outputColumnName = "id"
    diff([inputFile2, inputFile1, inputFile3], self.outputFile, outputColumnName, True, False, ['authorityID'], ",")
    expectedValues = []
    self.assertListEqual(getColumnValues(self.outputFile, outputColumnName), expectedValues, msg="Wrong minusRest result")

   # ---------------------------------------------------------------------------
  def testCorrectMinusLastDifferenceMultipleInputs(self):
    """When multiple input files and the minusRest options are given, the output should be all identifiers of the first minus the union of the ones in the rest."""
    inputFile1 = './test/resources/tools/persons.csv'
    inputFile2 = './test/resources/tools/persons-duplicate-of-persons-with-added-identifiers.csv'
    inputFile3 = './test/resources/tools/other-persons.csv'
    outputColumnName = "id"
    diff([inputFile2, inputFile1, inputFile3], self.outputFile, outputColumnName, False, True, ['authorityID'], ",")
    expectedValues = ['123','456','789']
    self.assertListEqual(getColumnValues(self.outputFile, outputColumnName), expectedValues, msg="Wrong minusRest result")
    
