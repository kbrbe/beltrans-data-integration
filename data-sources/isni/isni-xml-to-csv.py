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


# -----------------------------------------------------------------------------
def addIdentifiersToFile(elem, writer):
  isniID = utils.getElementValue(elem.find('./isniUnformatted'))

  # it has to be a person
  if elem.find('./ISNIMetadata/identity/personOrFiction'):

    # Most other identifiers are found directly in the metadata of the record
    for source in elem.findall('./ISNIMetadata/sources'):
      sourceName = utils.getElementValue(source.find('codeOfSource'))
      identifier = utils.getElementValue(source.find('sourceIdentifier'))

      # sometimes a source of the ISNI is ISNI, but the value then is prefixed with VIAF or BnF,
      # in those cases the VIAF might not be valid and the actual VIAF is in a separate source
      # with sourceName 'VIAF', thus skip the sources with sourceName 'ISNI'
      if sourceName == 'ISNI':
        pass
      else:
        newRecord = {
         'ISNI': isniID,
         'source': sourceName,
         'identifier': identifier
        }
        writer.writerow(newRecord)

    # Wikidata identifiers are often only mentioned in a name-variant of a source of the record
    for name in elem.findall('./ISNIMetadata/identity/personOrFiction/personalName'):
      isWikidataEntry = False
      # If it is wikidata, then there is one source with the value 'WKP' and one source element with for example the value 'VIAF'
      for sourceName in name.findall('source'):
        if utils.getElementValue(sourceName) == 'WKP':
          isWikidataEntry = True

      if isWikidataEntry:
        wikidataID = utils.getElementValue(name.find('subsourceIdentifier'))
        newRecord = {
          'ISNI': isniID,
          'source': 'Wikidata',
          'identifier': wikidataID
        }
        writer.writerow(newRecord)


# -----------------------------------------------------------------------------
def addAuthorityRecordsToFile(assignedRecord, writer):

  
  isniID = utils.getElementValue(assignedRecord.find('./isniUnformatted'))
  dataConfidence = utils.getElementValue(assignedRecord.find('./dataConfidence'))

  nationality = utils.getElementValue(assignedRecord.find('./ISNIMetadata/identity/personOrFiction/additionalInformation/nationality'))
  gender = utils.getElementValue(assignedRecord.find('./ISNIMetadata/identity/personOrFiction/additionalInformation/gender'))

  externalInfo = utils.getElementValue(assignedRecord.find('./ISNIMetadata/externalInformation/information'))

  # According to the documentation there should be a 'identifier' field, but we often find an undocumented 'URI' field instead
  externalInfoID = utils.getElementValue(assignedRecord.find('./ISNIMetadata/externalInformation/identifier'))
  externalInfoURI = utils.getElementValue(assignedRecord.find('./ISNIMetadata/externalInformation/URI'))

  names = assignedRecord.find('./ISNIMetadata/identity/personOrFiction/personalName')

  #print(ET.tostring(assignedRecord, encoding='utf8', method='xml'))

  # The record can be an oganization too, then 'names' is None (checked via a print statement in 'else')
  if names:

    surname = utils.getElementValue(names.find('surname'))
    forename = utils.getElementValue(names.find('forename'))
    marcDate = utils.getElementValue(names.find('marcDate'))

    newRecord = {
      'ISNI': isniID,
      'dataConfidence': dataConfidence,
      'nationality': nationality,
      'gender': gender,
      'surname': surname,
      'forename': forename,
      'marcDate': marcDate,
      'externalInfo': externalInfo,
      'externalInfoURI': externalInfoURI,
      'externalInfoID': externalInfoID
    }
    writer.writerow(newRecord)

# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format and generates statistics about used fields."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-folder', action='store', help='The input folder containing ISNI XML files')
  parser.add_option('-a', '--output-authority-file', action='store', help='The output CSV file containing authority information of found ISNI entities')
  parser.add_option('-o', '--output-identifier-file', action='store', help='The output CSV file containing found links to other authority identifiers such as BnF or VIAF')
  #parser.add_option('-w', '--output-works-file', action='store', help='The output file containing works of found ISNI entities')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_folder) or (not options.output_authority_file) or (not options.output_identifier_file) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  stats = {}
  uniqueISNINumbers = set()

  with open(options.output_authority_file, 'w') as outAutFile, \
       open(options.output_identifier_file, 'w') as outIDFile:

    autFields = ['ISNI', 'dataConfidence', 'nationality', 'gender', 'surname', 'forename', 'marcDate', 'externalInfo', 'externalInfoURI', 'externalInfoID']
    authorityWriter = csv.DictWriter(outAutFile, fieldnames=autFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    authorityWriter.writeheader()

    idFields = ['ISNI', 'source', 'identifier']
    idWriter = csv.DictWriter(outIDFile, fieldnames=idFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    idWriter.writeheader()

    # iterate over all XML Files in the given directory and count ISNI statistics
    for filename in os.listdir(options.input_folder):
      if filename.endswith('.xml'):
        f = os.path.join(options.input_folder, filename)

        print(f'processing file {filename} ...')
        for event, elem in ET.iterparse(f, events=('start', 'end')):

          # The parser finished reading one responseRecord, get information and then discard the record
          if  event == 'end' and elem.tag == 'responseRecord':

            assignedRecord = elem.find('ISNIAssigned')
            if assignedRecord:
              addAuthorityRecordsToFile(assignedRecord, authorityWriter)
              addIdentifiersToFile(assignedRecord, idWriter)

main()
