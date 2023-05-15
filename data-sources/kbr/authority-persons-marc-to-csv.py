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
def isPseudonym(value, sep=','):

  if value:
    # always make a list such that we do not have to repeat the conditional checks
    values = value.split(sep) if sep in value else [value]
    for v in values:
      if value == 'p' or value == 'P' or value.startswith('pseud') or value.startswith('Pseud'):
        return True
      else:
        return False
  else:
    return False


# -----------------------------------------------------------------------------
def extractAndWriteAlternativeNames(authorityID, elem, writer, stats):

  
  authorityInfo = utils.getElementValue(elem.findall('./marc:subfield[@code="c"]', ALL_NS), sep=',')
  namePerson = utils.getElementValue(elem.find('./marc:subfield[@code="a"]', ALL_NS))
  nameLanguage = utils.getElementValue(elem.find('./marc:subfield[@code="l"]', ALL_NS))
  nameSequenceNumber = utils.getElementValue(elem.find('./marc:subfield[@code="#"]', ALL_NS))

  authorityType = 'Pseudonym' if isPseudonym(authorityInfo) else 'Person'
  (familyName, givenName) = utils.extractNameComponents(namePerson)

  writer.writerow({'authorityID': authorityID,
                   'authorityType': authorityType,
                   'name': namePerson,
                   'family_name': familyName,
                   'given_name': givenName,
                   'language': nameLanguage,
                   'sequence_number': nameSequenceNumber})



# -----------------------------------------------------------------------------
def addAuthorityFieldsToCSV(elem, writer, natWriter, nameWriter, identifierWriter, stats):
  """This function extracts authority relevant data from the given XML element 'elem' and writes it to the given CSV file writer."""

  #
  # extract relevant data from the current record
  #
  authorityID = utils.getElementValue(elem.find('./marc:controlfield[@tag="001"]', ALL_NS))
  authorityInfo = utils.getElementValue(elem.findall('./marc:datafield[@tag="100"]/marc:subfield[@code="c"]', ALL_NS), sep=',')
  namePerson = utils.getElementValue(elem.find('./marc:datafield[@tag="100"]/marc:subfield[@code="a"]', ALL_NS))
  nameOrg = utils.getElementValue(elem.find('./marc:datafield[@tag="110"]/marc:subfield[@code="a"]', ALL_NS))
  nationalities = utils.getElementValue(elem.findall('./marc:datafield[@tag="370"]/marc:subfield[@code="c"]', ALL_NS))
  gender = utils.getElementValue(elem.find('./marc:datafield[@tag="375"]/marc:subfield[@code="a"]', ALL_NS))
  birthDateRaw = utils.getElementValue(elem.find('./marc:datafield[@tag="046"]/marc:subfield[@code="f"]', ALL_NS))
  deathDateRaw = utils.getElementValue(elem.find('./marc:datafield[@tag="046"]/marc:subfield[@code="g"]', ALL_NS))
  isniRaw = utils.getElementValue(elem.xpath('./marc:datafield[@tag="024"]/marc:subfield[@code="2" and (text()="isni" or text()="ISNI")]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  viafRaw = utils.getElementValue(elem.xpath('./marc:datafield[@tag="024"]/marc:subfield[@code="2" and (text()="viaf" or text()="VIAF")]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  countryCode = utils.getElementValue(elem.find('./marc:datafield[@tag="043"]/marc:subfield[@code="c"]', ALL_NS))

  alternativeNames = elem.findall('./marc:datafield[@tag="400"]', ALL_NS)
  if alternativeNames:
    for alternativeName in alternativeNames:
      extractAndWriteAlternativeNames(authorityID, alternativeName, nameWriter, stats)
 

  authorityType = 'Pseudonym' if isPseudonym(authorityInfo) else 'Person'
  
  (familyName, givenName) = utils.extractNameComponents(namePerson)
  birthDate = ''
  deathDate = ''

  datePatterns = ['%Y', '(%Y)', '[%Y]', '%Y-%m-%d', '%d/%m/%Y', '%Y%m%d']
  if birthDateRaw:
    birthDate = utils.parseDate(birthDateRaw, datePatterns)

  if deathDateRaw:
    deathDate = utils.parseDate(deathDateRaw, datePatterns)

  name = f'{namePerson} {nameOrg}'.strip()

  # Write 1:n nationality relationships to a separate file (one row = one nationality relationship)
  #
  if nationalities:
    # create a semicolon-separated list of country URIs
    nationalityURIString = utils.createURIString(nationalities, ';', 'http://id.loc.gov/vocabulary/countries/')

    # split by semicolon to create 1:n relationships
    for n in nationalityURIString.split(';'):
      natWriter.writerow({'authorityID': authorityID, 'nationality': n})

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
    'authorityType': authorityType,
    'name': name,
    'family_name': familyName,
    'given_name': givenName,
    'gender': gender,
    'birth_date': birthDate,
    'death_date': deathDate,
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
  parser.add_option('--identifier-csv', action='store', help='The output CSV file containing the IDs of authorities and linked 1:n identifiers')
  parser.add_option('--names-csv', action='store', help='The output CSV file containing alternate names and pseudonym information')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) or (not options.nationality_csv) or (not options.names_csv) or (not options.identifier_csv) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  with open(options.output_file, 'w') as outFile, \
       open(options.names_csv, 'w') as namesFile, \
       open(options.identifier_csv, 'w') as identifierFile, \
       open(options.nationality_csv, 'w') as natFile:

    stats = {'authorityType': {}, 'more-than-one-ISNI': 0, 'more-than-one-VIAF': 0}
    outputFields = ['authorityID', 'authorityType', 'name', 'family_name', 'given_name', 'gender', 'birth_date', 'death_date', 'country_code']
    outputWriter = csv.DictWriter(outFile, fieldnames=outputFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    outputWriter.writeheader()

    nationalityWriter = csv.DictWriter(natFile, fieldnames=['authorityID', 'nationality'], delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    nationalityWriter.writeheader()

    identifierWriter = csv.DictWriter(identifierFile, fieldnames=['authorityID', 'type', 'identifier'], delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    identifierWriter.writeheader()

    namesWriter = csv.DictWriter(namesFile, fieldnames=['authorityID', 'authorityType', 'name', 'family_name', 'given_name', 'language', 'sequence_number'],
                                 delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


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
        addAuthorityFieldsToCSV(elem, outputWriter, nationalityWriter, namesWriter, identifierWriter, stats)
        root.clear()
    elem.clear()
    #print(stats['more-than-one-isni'])
    #print(json.dumps(stats['authorityType'], indent=2, ensure_ascii=False))

main()
