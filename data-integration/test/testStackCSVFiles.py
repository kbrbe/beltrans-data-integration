import unittest
import tempfile
import csv
import os
import utils
import subprocess
from tools.csv.stack_csv_files import main as stack_csv_files

# Don't show the traceback of an AssertionError, because the AssertionError already says what the issue is!
__unittest = True

# -----------------------------------------------------------------------------
def getNumberOfRows(filename):
  with open(filename, 'r') as inFile:
    numberOfLines = sum(1 for l in inFile)
    # Don't count the header (we assume a CSV file with header)
    return numberOfLines - 1

# -----------------------------------------------------------------------------
def getColumnValues(filename, columnName):
  with open(filename, 'r') as inFile:
    reader = csv.DictReader(inFile, delimiter=',')
    return sorted({s[columnName] for s in reader})


# -----------------------------------------------------------------------------
class TestStackCSVFiles(unittest.TestCase):

  # ---------------------------------------------------------------------------
  def setUp(self):
    self.outputFile = os.path.join(tempfile.gettempdir(), 'combined.csv')

  # ---------------------------------------------------------------------------
  def tearDown(self):
    if os.path.isfile(self.outputFile):
      os.remove(self.outputFile)

  # ---------------------------------------------------------------------------
  def testAppendMode(self):
    """When the optional append parameter is given, the output file should not be overwritten"""
    inputFile1 = './test/resources/tools/persons.csv'
    inputFile2 = './test/resources/tools/more-persons.csv'
    stack_csv_files([inputFile1, inputFile2], self.outputFile, ["authorityID"], ",")
    expectedNumberOfOutputRows = getNumberOfRows(inputFile1) + getNumberOfRows(inputFile2)
    self.assertEqual(getNumberOfRows(self.outputFile), expectedNumberOfOutputRows, msg="Wrong number of lines in output")

  # ---------------------------------------------------------------------------
  def testCSVAppend(self):
    """All authority ID column values are in the output file"""
    inputFile1 = './test/resources/tools/persons.csv'
    inputFile2 = './test/resources/tools/more-persons.csv'
    stack_csv_files([inputFile1, inputFile2], self.outputFile, ["authorityID", "name"], ",",)
    expectedValues = ['123', '456', '789', '111', '222']
    self.assertListEqual(getColumnValues(self.outputFile, "authorityID"), sorted(expectedValues), msg="Wrong values in appended CSV")


  # ---------------------------------------------------------------------------
  def testUnknownColumn(self):
    """When a column is selected that does not exist in all input files an error is thrown"""
    with self.assertRaises(Exception):
      inputFile1 = './test/resources/tools/persons.csv'
      inputFile2 = './test/resources/tools/more-persons.csv'
      stack_csv_files([inputFile1, inputFile2], self.outputFile, ["otherColumn"], ",")

