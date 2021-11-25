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
def addAuthorityRecordsToFile(assignedRecord, writer):

  
  isniID = utils.getElementValue(assignedRecord.find('./isniUnformatted'))
  dataConfidence = utils.getElementValue(assignedRecord.find('./dataConfidence'))

  nationality = utils.getElementValue(assignedRecord.find('./ISNIMetadata/identity/personOrFiction/additionalInformation/nationality'))
  gender = utils.getElementValue(assignedRecord.find('./ISNIMetadata/identity/personOrFiction/additionalInformation/gender'))

  externalInfo = utils.getElementValue(assignedRecord.find('./ISNIMetadata/externalInformation/information'))

  # According to the documentation there should be a 'identifier' field, but we often find an undocumented 'URI' field instead
  externalInfoID = utils.getElementValue(assignedRecord.find('./ISNIMetadata/externalInformation/identifier'))
  externalInfoURI = utils.getElementValue(assignedRecord.find('./ISNIMetadata/externalInformation/URI'))

  for names in assignedRecord.findall('./ISNIMetadata/identity/personOrFiction/personalName'):

    surname = utils.getElementValue(names.find('surname'))
    forename = utils.getElementValue(names.find('forename'))

    sources = names.findall('source')
    sourcesLen = len(sources)
    sourceName = None
    subSourceName = ''

    if sourcesLen == 1:
      sourceName = sources[0].text
    if sourcesLen > 1 and sourcesLen < 3:
      for s in sources:
        if s.text == 'VIAF':
          sourceName = s.text
        else:
          subSourceName = s.text
    elif sourcesLen > 2:
      print(f'number of sources for {isniID}: {sourcesLen}')


    marcDate = utils.getElementValue(names.find('marcDate'))
    sourceID = utils.getElementValue(names.find('subsourceIdentifier'))

    if sourceID != '':
      newRecord = {
        'ISNI': isniID,
        'dataConfidence': dataConfidence,
        'nationality': nationality,
        'gender': gender,
        'surname': surname,
        'forename': forename,
        'marcDate': marcDate,
        'sourceName': sourceName,
        'subSourceName': subSourceName,
        'sourceID': sourceID,
        'externalInfo': externalInfo,
        'externalInfoURI': externalInfoURI,
        'externalInfoID': externalInfoID
      }
      if(isniID.endswith('61719351')):
        print(newRecord)
      writer.writerow(newRecord)
     

# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format and generates statistics about used fields."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-folder', action='store', help='The input folder containing ISNI XML files')
  parser.add_option('-a', '--output-authority-file', action='store', help='The output file containing authority information of found ISNI entities')
  #parser.add_option('-w', '--output-works-file', action='store', help='The output file containing works of found ISNI entities')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_folder) or (not options.output_authority_file) ):#or (not options.output_works_file) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  stats = {}
  uniqueISNINumbers = set()

  with open(options.output_authority_file, 'w') as outAutFile:

    fields = ['ISNI', 'dataConfidence', 'nationality', 'gender', 'surname', 'forename', 'marcDate', 'sourceName', 'subSourceName', 'sourceID', 'externalInfo', 'externalInfoURI', 'externalInfoID']
    authorityWriter = csv.DictWriter(outAutFile, fieldnames=fields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    authorityWriter.writeheader()

    # iterate over all XML Files in the given directory and count ISNI statistics
    for filename in os.listdir(options.input_folder):
      if filename.endswith('.xml'):
        f = os.path.join(options.input_folder, filename)

        for event, elem in ET.iterparse(f, events=('start', 'end')):

          # The parser finished reading one responseRecord, get information and then discard the record
          if  event == 'end' and elem.tag == 'responseRecord':

            assignedRecord = elem.find('ISNIAssigned')
            if assignedRecord:
              addAuthorityRecordsToFile(assignedRecord, authorityWriter)
              #addWorkRecorsToFile(elem, outWorksFile)

main()
