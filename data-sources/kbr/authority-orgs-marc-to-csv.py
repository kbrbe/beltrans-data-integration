#
# (c) 2022 Sven Lieber
# KBR Brussels
#
#import xml.etree.ElementTree as ET
import lxml.etree as ET
import os
import json
import itertools
import enchant
import hashlib
import csv
from optparse import OptionParser
import utils
import stdnum

NS_MARCSLIM = 'http://www.loc.gov/MARC21/slim'

ALL_NS = {'marc': NS_MARCSLIM}

# -----------------------------------------------------------------------------
def addAuthorityFieldsToCSV(elem, writer, stats):
  """This function extracts authority relevant data from the given XML element 'elem' and writes it to the given CSV file writer."""

  #
  # extract relevant data from the current record
  #
  authorityID = utils.getElementValue(elem.find('./marc:controlfield[@tag="001"]', ALL_NS))
  name = utils.getElementValue(elem.find('./marc:datafield[@tag="110"]/marc:subfield[@code="a"]', ALL_NS))
  isniRaw = utils.getElementValue(elem.xpath('./marc:datafield[@tag="024"]/marc:subfield[@code="2" and text()="isni"]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  viafRaw = utils.getElementValue(elem.xpath('./marc:datafield[@tag="024"]/marc:subfield[@code="2" and text()="viaf"]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  countryCode = utils.getElementValue(elem.find('./marc:datafield[@tag="043"]/marc:subfield[@code="c"]', ALL_NS))
 
  newRecord = {
    'authorityID': authorityID,
    'name': name,
    'isni_id': utils.extractIdentifier(authorityID, f'ISNI {isniRaw}', pattern='ISNI'),
    'viaf_id': utils.extractIdentifier(authorityID, f'VIAF {viafRaw}', pattern='VIAF'),
    'country_code': countryCode
  }

  writer.writerow(newRecord)

# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format and extracts several fields to create a CSV file."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing MARC SLIM XML records')
  parser.add_option('-o', '--output-file', action='store', help='The output CSV file containing selected MARC fields')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  with open(options.output_file, 'w') as outFile:

    stats = {}
    outputFields = ['authorityID', 'name', 'isni_id', 'viaf_id', 'country_code']
    outputWriter = csv.DictWriter(outFile, fieldnames=outputFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    outputWriter.writeheader()


    for event, elem in ET.iterparse(options.input_file, events=('start', 'end')):

      # The parser finished reading one authority record, get information and then discard the record
      if  event == 'end' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):

        addAuthorityFieldsToCSV(elem, outputWriter, stats)

main()
