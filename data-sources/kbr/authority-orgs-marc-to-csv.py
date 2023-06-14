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
def addAuthorityFieldsToCSV(elem, writer, identifierWriter, stats):
  """This function extracts authority relevant data from the given XML element 'elem' and writes it to the given CSV file writer."""

  #
  # extract relevant data from the current record
  #
  authorityID = utils.getElementValue(elem.find('./marc:controlfield[@tag="001"]', ALL_NS))
  name = utils.getElementValue(elem.xpath('./marc:datafield[@tag="110" and count(./marc:subfield[@code="@"]) = 0]/marc:subfield[@code="a"]', namespaces=ALL_NS))
  nameEN = utils.getElementValue(elem.xpath('./marc:datafield[@tag="110"]/marc:subfield[@code="@" and text()="en-GB"]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  nameNL = utils.getElementValue(elem.xpath('./marc:datafield[@tag="110"]/marc:subfield[@code="@" and text()="nl-BE"]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  nameFR = utils.getElementValue(elem.xpath('./marc:datafield[@tag="110"]/marc:subfield[@code="@" and text()="fr-BE"]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  isniRaw = utils.getElementValue(elem.xpath('./marc:datafield[@tag="024"]/marc:subfield[@code="2" and (text()="isni" or text()="ISNI")]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  viafRaw = utils.getElementValue(elem.xpath('./marc:datafield[@tag="024"]/marc:subfield[@code="2" and (text()="viaf" or text()="VIAF")]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  countryCode = utils.getElementValue(elem.find('./marc:datafield[@tag="043"]/marc:subfield[@code="c"]', ALL_NS))
  addressCountry = utils.getElementValue(elem.find('./marc:datafield[@tag="371"]/marc:subfield[@code="d"]', ALL_NS))
  addressStreet = utils.getElementValue(elem.find('./marc:datafield[@tag="371"]/marc:subfield[@code="a"]', ALL_NS))
  addressCity = utils.getElementValue(elem.find('./marc:datafield[@tag="371"]/marc:subfield[@code="b"]', ALL_NS))
  addressPostcode = utils.getElementValue(elem.find('./marc:datafield[@tag="371"]/marc:subfield[@code="e"]', ALL_NS))
 
  # elif because we only want one of it
  prefLabel = ''
  if name != '':
    prefLabel = name
  elif nameEN != '':
    prefLabel = nameEN
  elif nameNL != '':
    prefLabel = nameNL
  elif nameFR != '':
    prefLabel = nameFR

  if isniRaw != '':
    extractedISNIIdentifiers = utils.getListOfIdentifiers(authorityID, isniRaw, 'ISNI', stats)

    # Write ISNI relationships to a separate file
    for i in extractedISNIIdentifiers:
      identifierWriter.writerow({'authorityID': authorityID, 'type': 'isni', 'identifier': i})

  if viafRaw != '':
    extractedVIAFIdentifiers = utils.getListOfIdentifiers(authorityID, viafRaw, 'VIAF', stats)

    # Write VIAF relationships to a separate file
    for i in extractedVIAFIdentifiers:
      identifierWriter.writerow({'authorityID': authorityID, 'type': 'viaf', 'identifier': i})



  newRecord = {
    'authorityID': authorityID,
    'nameEN': nameEN,
    'nameNL': nameNL,
    'nameFR': nameFR,
    'prefLabel': utils.getNormalizedString(prefLabel),
    'country_code': countryCode,
    'address_country': addressCountry,
    'address_street': addressStreet,
    'address_city': addressCity,
    'address_postcode': addressPostcode
  }

  writer.writerow(newRecord)

# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format and extracts several fields to create a CSV file."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing MARC SLIM XML records')
  parser.add_option('-o', '--output-file', action='store', help='The output CSV file containing selected MARC fields')
  parser.add_option('--identifier-csv', action='store', help='The output CSV file containing the IDs of authorities and linked 1:n identifiers')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) or (not options.identifier_csv) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  with open(options.output_file, 'w') as outFile, \
       open(options.identifier_csv, 'w') as identifierFile:

    stats = {}
    outputFields = ['authorityID', 'nameEN', 'nameNL', 'nameFR', 'prefLabel', 'country_code', 'address_country', 'address_street', 'address_city', 'address_postcode']
    outputWriter = csv.DictWriter(outFile, fieldnames=outputFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    outputWriter.writeheader()

    identifierWriter = csv.DictWriter(identifierFile, fieldnames=['authorityID', 'type', 'identifier'], delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    identifierWriter.writeheader()

    for event, elem in ET.iterparse(options.input_file, events=('start', 'end')):

      # The parser finished reading one authority record, get information and then discard the record
      if  event == 'end' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):

        addAuthorityFieldsToCSV(elem, outputWriter, identifierWriter, stats)

main()
