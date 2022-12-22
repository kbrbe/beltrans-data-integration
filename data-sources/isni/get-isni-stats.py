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

# -----------------------------------------------------------------------------
def countDatafields(df, countDict):
  """This function counts differnt types of datafields and stores the result in 'countDict'."""
  if(df.tag == ET.QName(NS_MARCSLIM, 'datafield')):
    tagName = df.attrib['tag']
    if tagName in countDict:
      countDict[tagName]['number'] += 1
    else:
      countDict[tagName] = {'number': 1}

# -----------------------------------------------------------------------------
def countUniqueDatafields(fields, countDict):
   """This function takes a set of fields (thus unique) and adds 1 to the related-counter in countDict."""
   for f in fields:
     if 'unique' in countDict[f]:
       countDict[f]['unique'] += 1
     else:
       countDict[f]['unique'] = 1

# -----------------------------------------------------------------------------
def calculatePercentages(countDict):
  """This function counts percentages for each datafield based on 'totalRecords' and stores it in 'percentage' per field."""
  total = countDict['totalRecords']
  for df in countDict:
    # only count percentages for MARC datafields (they all are numbers)
    if df.isdigit():
      countDict[df]['percentage'] = round((countDict[df]['unique']/total)*100, 4)

# -----------------------------------------------------------------------------
def parsePersonAdditionalInformation(stats, additionalInfoTag):
  """This function parses the 'additionalInformation' tag of the 'personOrFiction' field of the ISNI extended schema: https://isni.oclc.org:2443/isni/ISNI_enquiry_response/ISNI_enquiry_response_xsd.html#personOrFiction_additionalInformation"""

  for info in additionalInfoTag:
    nationalityCounter = 0
    associatedCountriesCounter = 0
    genderCounter = 0
    if info.tag == 'nationality':
      nationalityCounter += 1
      utils.count(stats, 'person-nationality-' + info.text)
    if info.tag == 'gender':
      genderCounter += 1
      utils.count(stats, 'person-gender-' + info.text)
    if info.tag == 'countriesAssociated':
      for countryInfo in info:
        if countryInfo.tag == 'countryCode':
          associatedCountriesCounter += 1
          utils.count(stats, 'person-associated-' + countryInfo.text)
  utils.countStat(stats, 'multipleNationalities', nationalityCounter)
  utils.countStat(stats, 'multipleAssociatedCountries', associatedCountriesCounter)
  utils.countStat(stats, 'multipleGenders', genderCounter)



# -----------------------------------------------------------------------------
def parsePersonOrFiction(stats, personOrFictionTag):
  """This function parses the 'personOrFiction' field of the ISNI extended schema: https://isni.oclc.org:2443/isni/ISNI_enquiry_response/ISNI_enquiry_response_xsd.html#personOrFiction"""

  for personInfo in personOrFictionTag:
    if personInfo.tag == 'personalName':
      forename = ''
      surname = ''
      for nameInfo in personInfo:
        if nameInfo.tag == 'forename':
          forename = nameInfo.text
        if nameInfo.tag == 'surename':
          surname = nameInfo.text
        if nameInfo.tag == 'languageOfName':
          utils.count(stats, 'name-language-' + nameInfo.text)
      #print(f'{surname}, {forename}')
    if personInfo.tag == 'additionalInformation':
      parsePersonAdditionalInformation(stats, personInfo)

# -----------------------------------------------------------------------------
def parseIdentity(stats, identityTag):
  """This function parses the 'identity' field of the ISNI extended schema: https://isni.oclc.org:2443/isni/ISNI_enquiry_response/ISNI_enquiry_response_xsd.html#identity"""

  for identityField in identityTag:
    utils.count(stats, identityField.tag)
    if identityField.tag == 'personOrFiction':
      parsePersonOrFiction(stats, identityField)
    if identityField.tag == 'organisation':
      pass

# -----------------------------------------------------------------------------
def parseISNINotAssignedMetadata(stats, metadataField):
  """This function parses the 'ISNIMetadata' field of 'ISNINotAssigned' records of the ISNI extended schema: https://isni.oclc.org:2443/isni/ISNI_enquiry_response/ISNI_enquiry_response_xsd.html#responseRecord_responseRecord_ISNINotAssigned_ISNIMetadata"""

  for metadata in metadataField:
    if metadata.tag == 'identity':
      parseIdentity(stats, metadata)

# -----------------------------------------------------------------------------
def parseISNIAssignedMetadata(stats, metadataField):
  """This function parses the 'ISNIMetadata' field of 'ISNIAssigned' records of the ISNI extended schema: https://isni.oclc.org:2443/isni/ISNI_enquiry_response/ISNI_enquiry_response_xsd.html#responseRecord_responseRecord_ISNIAssigned_ISNIMetadata"""


  for metadata in metadataField:
    if metadata.tag == 'identity':
      parseIdentity(stats, metadata)

  sources = metadataField.findall('./sources')

  sourcesOfThisRecord = set()
  sourceIdentifiersOfThisRecord = {}
  for source in sources:

    # get the name and identifier of the source
    sourceName = source.find('./codeOfSource').text
    sourceIdentifierElement = source.find('./sourceIdentifier')
    sourceIdentifier = sourceIdentifierElement.text if sourceIdentifierElement else ''

    # if we already processed this source this is now (one of the) duplicate source identifier(s)
    if sourceName in sourcesOfThisRecord:

      # already count a duplicate for this sourceName, 
      # independent of how many duplicates there are for this source name
      utils.count(stats, 'duplicate-records-' + sourceName)

      # add the found identifier to a key value list, for example "kbr: [123,456]"
      # like this we can create more sophisticated statistics
      # about the number of duplicates for this source name
      sourceIdentifiersOfThisRecord[sourceName].append(sourceIdentifier)
         
    else:
      # we did not yet process any sourceName of this record, thus count it
      # like this we count the first occurrance of sourceName
      utils.count(stats, f'source-{sourceName}')
      sourcesOfThisRecord.add(sourceName)
      sourceIdentifiersOfThisRecord[sourceName] = [sourceIdentifier]

  for sourceName, identifierList in sourceIdentifiersOfThisRecord.items():
    if len(identifierList) > 1: 
      utils.count(stats, f'duplicate-{len(identifierList)}-records-{sourceName}')

# -----------------------------------------------------------------------------
def parseISNIXMLFile(stats, uniqueISNINumbers, filename):

  for event, elem in ET.iterparse(filename, events=('start', 'end')):

    #
    # The parser finished reading one responseRecord, get information and then discard the record
    #
    if  event == 'end' and elem.tag == 'responseRecord':
      utils.count(stats, 'responseRecord')

      isPerson = False
      isOrg = False
      if elem.find('.//personalName'):
        isPerson = True
        utils.count(stats, 'numberOfPersons')

      if elem.find('.//organisationName'):
        isOrg = True
        utils.count(stats, 'numberOfOrgs')

      for datafield in elem:
        if datafield.tag == 'ISNIAssigned':
          utils.count(stats, 'ISNIAssigned')
          for subfield in datafield:
            if subfield.tag == 'dataConfidence':
              utils.countStat(stats, 'assignedConfidence', subfield.text)
            elif subfield.tag == 'isniUnformatted':
              utils.count(stats, 'unformattedISNINumbers')
              uniqueISNINumbers.add(subfield.text)
            elif subfield.tag == 'ISNIMetadata':
              parseISNIAssignedMetadata(stats, subfield)
        elif datafield.tag == 'ISNINotAssigned':
          utils.count(stats, 'ISNINotAssigned')
          for subfield in datafield:
            if subfield.tag == 'ISNIMetadata':
              parseISNINotAssignedMetadata(stats, subfield)

      elem.clear()



# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format and generates statistics about used fields."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-folder', action='store', help='The input folder containing ISNI XML files')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_folder) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  stats = {}
  uniqueISNINumbers = set()

  #
  # iterate over all XML Files in the given directory and count ISNI statistics
  #
  for filename in os.listdir(options.input_folder):
    if filename.endswith('.xml'):
      f = os.path.join(options.input_folder, filename)
      parseISNIXMLFile(stats, uniqueISNINumbers, f)

  print(f'unique unformatted ISNI numbers {len(uniqueISNINumbers)}')
  for key,val in sorted(stats.items()):
    if isinstance(val, dict):
      minVal = val['min']
      maxVal = val['max']
      avgVal = val['avg']
      numVal = val['number']
      print(key)
      print(f'\tmin {minVal}, max {maxVal}, avg {avgVal}, amount {numVal}')
    else:
      print(key)
      print("\t" + str(val))

main()
