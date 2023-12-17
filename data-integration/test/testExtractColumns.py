import unittest
import tempfile
import csv
import os
import utils
import subprocess
from tools.csv.extract_columns import main as extract_columns

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
class TestExtractColumns(unittest.TestCase):

  # ---------------------------------------------------------------------------
  def setUp(self):
    self.outputFile = os.path.join(tempfile.gettempdir(), 'extract-column-output-file.csv')

  # ---------------------------------------------------------------------------
  def tearDown(self):
    if os.path.isfile(self.outputFile):
      os.remove(self.outputFile)

  # ---------------------------------------------------------------------------
  def testMissingColumnWarningSingleFile(self):
    """When a column is missing in the single input file, an early warning should be created"""
    with self.assertRaises(Exception):
      extract_columns(['./test/resources/tools/persons.csv'], self.outputFile, ["non-existing-column"], ",")

  # ---------------------------------------------------------------------------
  def testMissingColumnWarningMultipleFiles(self):
    """When a column is missing in one of the input files, an early warning should be created"""
    with self.assertRaises(Exception):
      extract_columns(['./test/resources/tools/persons.csv', '.test/resources/tools/yet-other-persons.csv'], self.outputFile, ["authorityID"], ",")
    
  # ---------------------------------------------------------------------------
  def testWriteMode(self):
    """When the optional append parameter is not given, the output file should be overwritten"""
    inputFile = './test/resources/tools/persons.csv'
    extract_columns([inputFile], self.outputFile, ["authorityID"], ",")
    self.assertEqual(getNumberOfRows(self.outputFile), getNumberOfRows(inputFile), msg="Wrong number of lines in output")

  # ---------------------------------------------------------------------------
  def testAppendMode(self):
    """When the optional append parameter is given, the output file should not be overwritten"""
    inputFile1 = './test/resources/tools/persons.csv'
    inputFile2 = './test/resources/tools/other-persons.csv'
    extract_columns([inputFile1], self.outputFile, ["authorityID"], ",", appendData=True)
    extract_columns([inputFile2], self.outputFile, ["authorityID"], ",", appendData=True)
    expectedNumberOfOutputRows = getNumberOfRows(inputFile1) + getNumberOfRows(inputFile2)
    self.assertEqual(getNumberOfRows(self.outputFile), expectedNumberOfOutputRows, msg="Wrong number of lines in output")

  # ---------------------------------------------------------------------------
  def testCSVAppend(self):
    """When the optional append parameter is given, the output CSV file should contain additional values without the header"""
    inputFile1 = './test/resources/tools/persons.csv'
    inputFile2 = './test/resources/tools/other-persons.csv'
    extract_columns([inputFile1], self.outputFile, ["authorityID"], ",", appendData=True)
    extract_columns([inputFile2], self.outputFile, ["authorityID"], ",", appendData=True)
    expectedValues = ['111', '123', '222', '456', '789', 'authorityID']
    self.assertListEqual(getColumnValues(self.outputFile, "authorityID"), expectedValues, msg="Wrong values in appended CSV")


  # ---------------------------------------------------------------------------
  def testFilterEquals(self):
    """When a filter file with equal conditions is given, they should be applied"""
    inputFile = './test/resources/tools/persons.csv'
    filterFile = './test/resources/tools/filter-criteria.csv'
    extract_columns([inputFile], self.outputFile, ["authorityID"], ",", filterFilename=filterFile)
    expectedNumberOfOutputRows = 3
    self.assertEqual(getNumberOfRows(self.outputFile), expectedNumberOfOutputRows, msg="Equality filter was not applied")

  # ---------------------------------------------------------------------------
  def testCustomOutputHeadersTooMany(self):
    """When too many output headers are defined an error should be thrown"""
    with self.assertRaises(Exception):
      inputFile = './test/resources/tools/persons.csv'
      extract_columns([inputFile], self.outputFile, ["authorityID"], ",", filterFilename=filterFile, outputColumns=["aID", "bID"])

  # ---------------------------------------------------------------------------
  def testCustomOutputHeadersTooLess(self):
    """When too less output headers are defined an error should be thrown"""
    with self.assertRaises(Exception):
      inputFile = './test/resources/tools/persons.csv'
      extract_columns([inputFile], self.outputFile, ["authorityID"], ",", filterFilename=filterFile, outputColumns=[])

  # ---------------------------------------------------------------------------
  def testCustomOutputHeaders(self):
    """When output headers are defined they should be used in the output"""
    inputFile = './test/resources/tools/persons.csv'
    extract_columns([inputFile], self.outputFile, ["authorityID"], ",", outputColumns=["aID"])
    expectedValues = ['123', '456', '789']
    self.assertListEqual(getColumnValues(self.outputFile, "aID"), expectedValues, msg="Wrong values in appended CSV")
