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
from contextlib import ExitStack
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
def extractAndWritePseudonymLinks(authorityID, authorityName, elem, writer, stats):

  
  authorityInfo = utils.getElementValue(elem.findall('./marc:subfield[@code="c"]', ALL_NS), sep=',')
  namePerson = utils.getElementValue(elem.find('./marc:subfield[@code="a"]', ALL_NS))
  linkedIdentifier = utils.getElementValue(elem.find('./marc:subfield[@code="*"]', ALL_NS))

  # In field 500 are also just 'related persons'
  # We are only interested in fields indicating a pseudonym
  if isPseudonym(authorityInfo):
    writer.writerow({'authorityID': authorityID,
                     'authorityName': authorityName,
                     'authorityType': 'Pseudonym',
                     'name': '',
                     'family_name': '',
                     'given_name': '',
                     'language': '',
                     'sequence_number': '',
                     'linkedIdentifier': linkedIdentifier})



# -----------------------------------------------------------------------------
def extractAndWriteAlternativeNames(authorityID, authorityName, elem, writer, stats):

  
  authorityInfo = utils.getElementValue(elem.findall('./marc:subfield[@code="c"]', ALL_NS), sep=',')
  namePerson = utils.getElementValue(elem.find('./marc:subfield[@code="a"]', ALL_NS))
  nameLanguage = utils.getElementValue(elem.find('./marc:subfield[@code="l"]', ALL_NS))
  nameSequenceNumber = utils.getElementValue(elem.find('./marc:subfield[@code="#"]', ALL_NS))

  authorityType = 'Pseudonym' if isPseudonym(authorityInfo) else 'Person'
  (familyName, givenName) = utils.extractNameComponents(namePerson)

  writer.writerow({'authorityID': authorityID,
                   'authorityName': authorityName,
                   'authorityType': authorityType,
                   'name': namePerson,
                   'family_name': familyName,
                   'given_name': givenName,
                   'language': nameLanguage,
                   'sequence_number': nameSequenceNumber,
                   'linkedIdentifier': ''})

# -----------------------------------------------------------------------------
def addOrganizationAuthorityFieldsToCSV(elem, writer, identifierWriter, stats):
  """This function extracts authority relevant org data from the given XML element 'elem' and writes it to the given CSV file writer."""

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
    'name': name,
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
def addPersonAuthorityFieldsToCSV(elem, writer, natWriter, langWriter, nameWriter, identifierWriter, stats):
  """This function extracts authority relevant person data from the given XML element 'elem' and writes it to the given CSV file writer."""

  #
  # extract relevant data from the current record
  #
  authorityID = utils.getElementValue(elem.find('./marc:controlfield[@tag="001"]', ALL_NS))
  authorityInfo = utils.getElementValue(elem.findall('./marc:datafield[@tag="100"]/marc:subfield[@code="c"]', ALL_NS), sep=',')
  namePerson = utils.getElementValue(elem.find('./marc:datafield[@tag="100"]/marc:subfield[@code="a"]', ALL_NS))
  nameOrg = utils.getElementValue(elem.find('./marc:datafield[@tag="110"]/marc:subfield[@code="a"]', ALL_NS))
  nationalities = utils.getElementValue(elem.findall('./marc:datafield[@tag="370"]/marc:subfield[@code="c"]', ALL_NS))
  languages = utils.getElementValue(elem.findall('./marc:datafield[@tag="377"]/marc:subfield[@code="a"]', ALL_NS))
  gender = utils.getElementValue(elem.find('./marc:datafield[@tag="375"]/marc:subfield[@code="a"]', ALL_NS))
  birthDateRaw = utils.getElementValue(elem.find('./marc:datafield[@tag="046"]/marc:subfield[@code="f"]', ALL_NS))
  deathDateRaw = utils.getElementValue(elem.find('./marc:datafield[@tag="046"]/marc:subfield[@code="g"]', ALL_NS))
  isniRaw = utils.getElementValue(elem.xpath('./marc:datafield[@tag="024"]/marc:subfield[@code="2" and (text()="isni" or text()="ISNI")]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  viafRaw = utils.getElementValue(elem.xpath('./marc:datafield[@tag="024"]/marc:subfield[@code="2" and (text()="viaf" or text()="VIAF")]/../marc:subfield[@code="a"]', namespaces=ALL_NS))
  countryCode = utils.getElementValue(elem.find('./marc:datafield[@tag="043"]/marc:subfield[@code="c"]', ALL_NS))

  alternativeNames = elem.findall('./marc:datafield[@tag="400"]', ALL_NS)
  if alternativeNames:
    for alternativeName in alternativeNames:
      extractAndWriteAlternativeNames(authorityID, namePerson, alternativeName, nameWriter, stats)
 
  pseudonymLinks = elem.findall('./marc:datafield[@tag="500"]', ALL_NS)
  if pseudonymLinks:
    for link in pseudonymLinks:
      extractAndWritePseudonymLinks(authorityID, namePerson, link, nameWriter, stats)

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

  # Write 1:n language relationships to a separate file (one row = one nationality relationship)
  #
  if languages:

    # create a semicolon-separated list of language URIs
    languageURIString = utils.createURIString(languages, ';', 'http://id.loc.gov/vocabulary/languages/') 

    # split by semicolon to create 1:n relationships
    for l in languageURIString.split(';'):
      langWriter.writerow({'authorityID': authorityID, 'language': l})

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
  parser.add_option('-i', '--input-files', action='append', help='One or more input files containing MARC SLIM XML records')
  parser.add_option('-p', '--output-file-persons', action='store', help='The output CSV file containing selected MARC fields for person records')
  parser.add_option('-o', '--output-file-orgs', action='store', help='The output CSV file containing selected MARC fields for organization records')
  parser.add_option('-n', '--nationality-csv', action='store', help='The output CSV file containing the IDs of authorities and their nationality')
  parser.add_option('-l', '--language-csv', action='store', help='The output CSV file containing the IDs of authorities and their language')
  parser.add_option('--identifier-csv', action='store', help='The output CSV file containing the IDs of authorities and linked 1:n identifiers')
  parser.add_option('--names-csv', action='store', help='The output CSV file containing alternate names and pseudonym information')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_files) or (not options.identifier_csv)):
    parser.print_help()
    exit(1)

  if( (not options.output_file_persons) and (not options.output_file_orgs) ):
    print(f'At least one output file needed, persons or organizations')
    parser.print_help()
    exit(1)

  if options.output_file_persons:
    if (not options.nationality_csv) or (not options.language_csv) or (not options.names_csv):
      print(f'Please provide filenames for nationality, language and names when selecting persons as output')
      parser.print_help()
      exit(1)

  files = {}
  with ExitStack() as stack:
    stats = {'authorityType': {}, 'more-than-one-ISNI': 0, 'more-than-one-VIAF': 0}

    files['identifierCSV'] = stack.enter_context(open(options.identifier_csv, 'w'))
    identifierWriter = csv.DictWriter(files['identifierCSV'], fieldnames=['authorityID', 'type', 'identifier'], delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    identifierWriter.writeheader()

    if options.output_file_persons:
      files['personOutputCSV'] = stack.enter_context(open(options.output_file_persons, 'w'))
      personOutputFields = ['authorityID', 'authorityType', 'name', 'family_name', 'given_name', 'gender', 'birth_date', 'death_date', 'country_code']
      personOutputWriter = csv.DictWriter(files['personOutputCSV'], fieldnames=personOutputFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      personOutputWriter.writeheader()

      files['nationalityCSV'] = stack.enter_context(open(options.nationality_csv, 'w'))
      nationalityWriter = csv.DictWriter(files['nationalityCSV'], fieldnames=['authorityID', 'nationality'], delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      nationalityWriter.writeheader()

      files['languageCSV'] = stack.enter_context(open(options.language_csv, 'w'))
      languageWriter = csv.DictWriter(files['languageCSV'], fieldnames=['authorityID', 'language'], delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      languageWriter.writeheader()

      files['namesCSV'] = stack.enter_context(open(options.names_csv, 'w'))
      namesWriter = csv.DictWriter(files['namesCSV'], fieldnames=['authorityID', 'authorityName', 'authorityType', 'name', 'family_name', 'given_name', 'language', 'sequence_number', 'linkedIdentifier'],
                                   delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

      namesWriter.writeheader()


    if options.output_file_orgs:
      files['orgsOutputCSV'] = stack.enter_context(open(options.output_file_orgs, 'w'))
      orgOutputFields = ['authorityID', 'name', 'nameEN', 'nameNL', 'nameFR', 'prefLabel', 'country_code', 'address_country', 'address_street', 'address_city', 'address_postcode']
      orgOutputWriter = csv.DictWriter(files['orgsOutputCSV'], fieldnames=orgOutputFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      orgOutputWriter.writeheader()

    #
    # Instead of loading everything to main memory, stream over the XML using iterparse
    #
    for inputFile in options.input_files:
      if not os.path.isfile(inputFile):
        print(f'skipping authority file because it does not exist: "{inputFile}"')
        continue
      # if the XML file is huge, memory becomes an issue even while streaming because a reference to the parent is kept
      # therefore we first get the root element
      # https://stackoverflow.com/questions/12160418/why-is-lxml-etree-iterparse-eating-up-all-my-memory
      context = ET.iterparse(inputFile, events=('start', 'end'))
      context = iter(context)
      event, root = next(context)

      # now we iterate over the children of the root and always clear the root information
      for event, elem in context:

        # The parser finished reading one authority record, get information and then discard the record
        if  event == 'end' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):

          # Parse record based on its type (person or organization)
          authorityID = utils.getElementValue(elem.find('./marc:controlfield[@tag="001"]', ALL_NS))
          authorityType = utils.getUniqueValue(utils.getElementValue(elem.xpath('./marc:datafield[@tag="075"]/marc:subfield[@code="a"]', namespaces=ALL_NS)))

          if authorityType == 'p':
            # TYPE PERSON
            if options.output_file_persons:
              addPersonAuthorityFieldsToCSV(elem, personOutputWriter, nationalityWriter, languageWriter, namesWriter, identifierWriter, stats)
          elif authorityType == 'c':
            # TYPE ORGANIZATION
            if options.output_file_orgs:
              addOrganizationAuthorityFieldsToCSV(elem, orgOutputWriter, identifierWriter, stats)
          elif authorityType == '':
            # not all KBR records might have a type indicated in 075$a
            # it can be determined indirectly based on the used name field
            name100 = utils.getElementValue(elem.findall('./marc:datafield[@tag="100"]/marc:subfield[@code="a"]', ALL_NS), sep=',')
            name110 = utils.getElementValue(elem.findall('./marc:datafield[@tag="110"]/marc:subfield[@code="a"]', ALL_NS), sep=',')
            if name100 != '' and name110 != '':
              # person AND organization name
              print(f'No direct type for authority "{authorityID}" and both person and organization name found (field 100 AND 110)')
            elif name100 != '':
              # person name
              if options.output_file_persons:
                addPersonAuthorityFieldsToCSV(elem, personOutputWriter, nationalityWriter, languageWriter, namesWriter, identifierWriter, stats)
            elif name110 != '':
              # organization name
              if options.output_file_orgs:
                addOrganizationAuthorityFieldsToCSV(elem, orgOutputWriter, identifierWriter, stats)
            else:
              # no name at all
              print(f'No direct or indirect type for authority "{authorityID}"')
              print(ET.tostring(elem, pretty_print=True))
          else:
            # unknown authority type
              print(f'Unknown authority type "{authorityType}" for authority "{authorityID}"')
           
          # Correctly clear empty references to save up RAM
          # But without clearing root to avoid namespace issues (https://github.com/kbrbe/beltrans-data-integration/issues/274)
          elem.clear()
          for ancestor in elem.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
              del ancestor.getparent()[0]

main()
