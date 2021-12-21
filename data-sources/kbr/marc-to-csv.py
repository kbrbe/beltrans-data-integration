#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import xml.etree.ElementTree as ET
import os
import json
import itertools
import enchant
import hashlib
import csv
from optparse import OptionParser
import utils

NS_MARCSLIM = 'http://www.loc.gov/MARC21/slim'

ALL_NS = {'': NS_MARCSLIM}

# -----------------------------------------------------------------------------
def getContributorData(elem):
  """This function extracts the ID, name, and role of a contributor and returns them."""

  cID = utils.getElementValue(elem.find('./subfield[@code="*"]', ALL_NS))
  cName = utils.getElementValue(elem.find('./subfield[@code="a"]', ALL_NS))
  cRole = utils.getElementValue(elem.find('./subfield[@code="4"]', ALL_NS))

  return (cID, cName, cRole)
  
# -----------------------------------------------------------------------------
def addContributorFieldsToContributorCSV(elem, writer, stats):
  """This function extracts contributor relevant data from the given XML element 'elem' and writes it to the given CSV file writer."""

  kbrID = utils.getElementValue(elem.find('./controlfield[@tag="001"]', ALL_NS))

  foundContributors = []
  linkedOrganizationNames = set()

  #
  # add person contributors, in case the role is empty it is the author with role 'aut'
  #
  personContributors = elem.findall('./datafield[@tag="700"]', ALL_NS)
  for p in personContributors:
    (cID, cName, cRole) = getContributorData(p)
    # If no role is set it is an author (confirmed with KBRs cataloging agency)
    if cRole == '':
      cRole = 'aut'
    # Also persons can publish, thus we should add them for the later check on publishers
    if cRole == 'pbl':
      linkedOrganizationNames.add(utils.getNormalizedString(cName))
    foundContributors.append({'contributorID': cID, 'contributorName': cName, 'contributorRole': cRole, 'uncertainty': 'no'})

  #
  # add organizational contributors such as publishers
  #
  orgContributors = elem.findall('./datafield[@tag="710"]', ALL_NS)
  for o in orgContributors:
    uncertainty = 'no'
    (cID, cName, cRole) = getContributorData(o)
    linkedOrganizationNames.add(utils.getNormalizedString(cName))
    # If no role is set it likely is an author (confirmed with KBRs cataloging agency)
    if cRole == '':
      cRole = 'pbl'
      uncertainty = 'yes'
    foundContributors.append({'contributorID': cID, 'contributorName': cName, 'contributorRole': cRole, 'uncertainty': uncertainty})

  #
  # Publishers are also indicated in field 264, but only as text string as it appeared on the book
  # If we simply map 264 we get doubles because we also map 710
  # Thus we have to identify publishers which are ONLY encoded in field 264
  # In the previous step we collected all the names of organizational contributors (field 710) of this record
  #
  orgContributorsWithoutLink = elem.findall('./datafield[@tag="264"]', ALL_NS)
  for ol in orgContributorsWithoutLink:
    textName = utils.getElementValue(ol.find('./subfield[@code="b"]', ALL_NS))
    textNameNorm = utils.getNormalizedString(textName)
    if textName != '':
      foundMatch = False
      for linked in linkedOrganizationNames:

        # check first if the 264 name is part of the 710 name or vice versa
        if textNameNorm in linked:
          utils.count(stats['counter'], 'identified-264-in-710-by-264-in-710')
          foundMatch = True
          break
        elif linked in textNameNorm:
          utils.count(stats['counter'], 'identified-264-in-710-by-710-in-264')
          foundMatch = True
          break
        else:
          # if the name is no substring of the other name, do some more sophisticated comparisons
          # based on the levenshtein distance of (parts of) the name
          if utils.smallLevenshteinDistance(stats['counter'], textNameNorm, linked):
            foundMatch = True
            break

      if not foundMatch:
        # this publisher encoded as text does not seem to be already encoded as link in a 710 field
        # thus create a new contribution and use a hash of the normalized name as ID
        # alternatively a UUID can be used, but with a hash we can identify this publisher also in other records and get other links

        if textName != 's. n' and textName != '[s.n.]':
          normalizedName = utils.getNormalizedString(textName)
          nameID = hashlib.md5(normalizedName.encode('utf-8')).hexdigest()
          utils.count(stats['counter'], 'publishers-without-authority')
          stats['unique-publishers-without-authority'].add(nameID)
          foundContributors.append({'contributorID': nameID, 'contributorName': textName, 'contributorRole': 'pbl', 'uncertainty': 'no'})
       

  #
  # write all we found to a file, one row per contribution
  #
  for cont in foundContributors:
    # we also need to add the ID of the bibliographic item the contributor contributed to
    cont['KBRID'] = kbrID
    writer.writerow(cont)
 

# -----------------------------------------------------------------------------
def addWorkFieldsToWorkCSV(elem, writer):
  """This function extracts work relevant data from the given XML element 'elem' and writes it to the given CSV file writer."""


  #
  # extract relevant data from the current record
  #
  kbrID = utils.getElementValue(elem.find('./controlfield[@tag="001"]', ALL_NS))
  isbn = utils.getElementValue(elem.find('./datafield[@tag="020"]/subfield[@code="a"]', ALL_NS))
  bindingType = utils.getElementValue(elem.find('./datafield[@tag="020"]/subfield[@code="q"]', ALL_NS))
  languagesString = utils.getElementValue(elem.findall('./datafield[@tag="041"]/subfield[@code="a"]', ALL_NS))
  countryOfPublication = utils.getElementValue(elem.find('./datafield[@tag="044"]/subfield[@code="a"]', ALL_NS))
  title = utils.getElementValue(elem.find('./datafield[@tag="245"]/subfield[@code="a"]', ALL_NS))
  responsibilityStatement = utils.getElementValue(elem.find('./datafield[@tag="245"]/subfield[@code="c"]', ALL_NS))
  placeOfPublication = utils.getElementValue(elem.find('./datafield[@tag="264"]/subfield[@code="a"]', ALL_NS))
  yearOfPublication = utils.getElementValue(elem.find('./datafield[@tag="264"]/subfield[@code="c"]', ALL_NS))
  edition = utils.getElementValue(elem.find('./datafield[@tag="250"]/subfield[@code="a"]', ALL_NS))
  belgianBibliographyClassificationsString = utils.getElementValue(elem.findall('./datafield[@tag="911"]/subfield[@code="a"]', ALL_NS))

  
  # create a URI for all languages
  langURIsString = utils.createURIString(languagesString, ';', 'http://id.loc.gov/vocabulary/languages/')

  # create a URI for all belgian bibliographic classifications
  bbURIsString = utils.createURIString(belgianBibliographyClassificationsString, ';', 'http://kbr.be/id/data/')

  newRecord = {
    'KBRID': kbrID,
    'isbn': isbn,
    'title': title,
    'languages': langURIsString,
    'placeOfPublication': placeOfPublication,
    'countryOfPublication': countryOfPublication,
    'yearOfPublication': yearOfPublication,
    'responsibilityStatement': responsibilityStatement,
    'bindingType': bindingType,
    'edition': edition,
    'belgianBibliography': bbURIsString
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
  with open(options.output_cont_file, 'w') as outContFile, \
       open(options.output_work_file, 'w') as outWorkFile:

    fields = ['ISNI', 'dataConfidence', 'nationality', 'gender', 'surname', 'forename', 'marcDate', 'sourceName', 'subSourceName', 'sourceID', 'externalInfo', 'externalInfoURI', 'externalInfoID']
    workFields = ['KBRID', 'isbn', 'title', 'languages', 'placeOfPublication', 'countryOfPublication', 'yearOfPublication', 'responsibilityStatement', 'bindingType', 'edition', 'belgianBibliography']
    contFields = ['KBRID', 'contributorID', 'contributorName', 'contributorRole', 'uncertainty']
    workWriter = csv.DictWriter(outWorkFile, fieldnames=workFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    contWriter = csv.DictWriter(outContFile, fieldnames=contFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    workWriter.writeheader()
    contWriter.writeheader()

    stats = {'unique-publishers-without-authority': set(), 'counter': {} }
    # iterate over all XML Files in the given directory and count ISNI statistics
    for event, elem in ET.iterparse(options.input_file, events=('start', 'end')):

      # The parser finished reading one responseRecord, get information and then discard the record
      if  event == 'end' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):

        addWorkFieldsToWorkCSV(elem, workWriter)
        addContributorFieldsToContributorCSV(elem, contWriter, stats)

    numberUniquePublishersWithoutAuthorityRecord = len(stats['unique-publishers-without-authority'])
    print(f'Unique publishers without authority record: {numberUniquePublishersWithoutAuthorityRecord}')
    for key,val in stats['counter'].items():
      print(f'{key},{val}')

main()
