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
def addAuthorityFieldsToCSV(elem, writer, natWriter, stats):
  """This function extracts authority relevant data from the given XML element 'elem' and writes it to the given CSV file writer."""

  #
  # extract relevant data from the current record
  #
  authorityID = utils.getElementValue(elem.find('./marc:controlfield[@tag="001"]', ALL_NS))
  namePerson = utils.getElementValue(elem.find('./marc:datafield[@tag="100"]/marc:subfield[@code="a"]', ALL_NS))
  nameOrg = utils.getElementValue(elem.find('./marc:datafield[@tag="110"]/marc:subfield[@code="a"]', ALL_NS))
  nationalities = utils.getElementValue(elem.findall('./marc:datafield[@tag="370"]/marc:subfield[@code="c"]', ALL_NS))
  gender = utils.getElementValue(elem.find('./marc:datafield[@tag="375"]/marc:subfield[@code="a"]', ALL_NS))
  birthDateRaw = utils.getElementValue(elem.find('./marc:datafield[@tag="046"]/marc:subfield[@code="f"]', ALL_NS))
  deathDateRaw = utils.getElementValue(elem.find('./marc:datafield[@tag="046"]/marc:subfield[@code="g"]', ALL_NS))
  isniRaw = utils.getElementValue(elem.xpath('./marc:datafield[@tag="024"]/marc:subfield[@code="2" and (text()="isni" or text()="ISNI")]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  viafRaw = utils.getElementValue(elem.xpath('./marc:datafield[@tag="024"]/marc:subfield[@code="2" and text()="viaf"]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  countryCode = utils.getElementValue(elem.find('./marc:datafield[@tag="043"]/marc:subfield[@code="c"]', ALL_NS))
 

  (familyName, givenName) = utils.extractNameComponents(namePerson)
  birthDate = ''
  deathDate = ''

  datePatterns = ['%Y', '(%Y)', '[%Y]', '%Y-%m-%d', '%d/%m/%Y', '%Y%m%d']
  if birthDateRaw:
    birthDate = utils.parseDate(birthDateRaw, datePatterns)

  if deathDateRaw:
    deathDate = utils.parseDate(deathDateRaw, datePatterns)

  name = f'{namePerson} {nameOrg}'.strip()

  if nationalities:
    nationalityURIString = utils.createURIString(nationalities, ';', 'http://id.loc.gov/vocabulary/countries/')
    for n in nationalityURIString.split(';'):
      natWriter.writerow({'authorityID': authorityID, 'nationality': n})

  newRecord = {
    'authorityID': authorityID,
    'name': name,
    'family_name': familyName,
    'given_name': givenName,
    'gender': gender,
    'birth_date': birthDate,
    'death_date': deathDate,
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
  parser.add_option('-n', '--nationality-csv', action='store', help='The output CSV file containing the IDs of authorities and their nationality')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) or (not options.nationality_csv) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  with open(options.output_file, 'w') as outFile, \
       open(options.nationality_csv, 'w') as natFile:

    stats = {}
    outputFields = ['authorityID', 'name', 'family_name', 'given_name', 'gender', 'birth_date', 'death_date', 'isni_id', 'viaf_id', 'country_code']
    outputWriter = csv.DictWriter(outFile, fieldnames=outputFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    outputWriter.writeheader()

    nationalityWriter = csv.DictWriter(natFile, fieldnames=['authorityID', 'nationality'], delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    nationalityWriter.writeheader()

    # if the XML file is huge, memory becomes an issue even while streaming because a reference to the parent is kept
    # therefore we first get the root element
    # https://stackoverflow.com/questions/12160418/why-is-lxml-etree-iterparse-eating-up-all-my-memory
    context = ET.iterparse(options.input_file, events=('start', 'end'))
    context = iter(context)
    event, root = next(context)

    # now we iterate over the children of the root and always clear the root information
    for event, elem in context:

      # The parser finished reading one authority record, get information and then discard the record
      if  event == 'end' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):
        addAuthorityFieldsToCSV(elem, outputWriter, nationalityWriter, stats)
        root.clear()
    elem.clear()

main()
