#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import xml.etree.ElementTree as ET
import os
import json
import itertools
import csv
from optparse import OptionParser
import utils

NS_MARCSLIM = 'http://www.loc.gov/MARC21/slim'

ALL_NS = {'': NS_MARCSLIM}

# -----------------------------------------------------------------------------
def addContributorFieldsToContributorCSV(elem, writer):

  kbrID = utils.getElementValue(elem.find('./controlfield[@tag="001"]', ALL_NS))

  newRecord = {
    'KBRID': kbrID
  }
  #print(newRecord)
  #writer.writerow(newRecord)
 

# -----------------------------------------------------------------------------
def addWorkFieldsToWorkCSV(elem, writer):


  #
  # extract relevant data from the current record
  #
  kbrID = utils.getElementValue(elem.find('./controlfield[@tag="001"]', ALL_NS))
  isbn = utils.getElementValue(elem.find('./datafield[@tag="020"]/subfield[@code="a"]', ALL_NS))
  title = utils.getElementValue(elem.find('./datafield[@tag="245"]/subfield[@code="a"]', ALL_NS))
  language = utils.getElementValue(elem.find('./datafield[@tag="041"]/subfield[@code="a"]', ALL_NS))

  newRecord = {
    'KBRID': kbrID,
    'isbn': isbn,
    'title': title,
    'language': language
  }

  writer.writerow(newRecord)
     

# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format and generates statistics about used fields."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing MARC SLIM XML records')
  parser.add_option('-c', '--output-cont-file', action='store', help='The output contributor CSV file containing selected MARC fields (one contribution per row)')
  parser.add_option('-w', '--output-work-file', action='store', help='The output work CSV file containing selected MARC fields (one work per row)')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_work_file) or (not options.output_cont_file) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  stats = {}

  with open(options.output_cont_file, 'w') as outContFile, \
       open(options.output_work_file, 'w') as outWorkFile:

    fields = ['ISNI', 'dataConfidence', 'nationality', 'gender', 'surname', 'forename', 'marcDate', 'sourceName', 'subSourceName', 'sourceID', 'externalInfo', 'externalInfoURI', 'externalInfoID']
    workFields = ['KBRID', 'isbn', 'title', 'language']
    contFields = []
    workWriter = csv.DictWriter(outWorkFile, fieldnames=workFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    contWriter = csv.DictWriter(outContFile, fieldnames=contFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    workWriter.writeheader()
    contWriter.writeheader()

    # iterate over all XML Files in the given directory and count ISNI statistics
    for event, elem in ET.iterparse(options.input_file, events=('start', 'end')):

      # The parser finished reading one responseRecord, get information and then discard the record
      if  event == 'end' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):

        addWorkFieldsToWorkCSV(elem, workWriter)
        addContributorFieldsToContributorCSV(elem, contWriter)

main()
