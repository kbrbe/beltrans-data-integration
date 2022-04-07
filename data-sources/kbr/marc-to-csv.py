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
from contributor import PersonContributor, OrganizationalContributor
import utils
import stdnum

NS_MARCSLIM = 'http://www.loc.gov/MARC21/slim'

ALL_NS = {'': NS_MARCSLIM}

# -----------------------------------------------------------------------------
def getContributorData(elem):
  """This function extracts the ID, name, and role of a contributor and returns them."""

  cID = utils.getElementValue(elem.find('./subfield[@code="*"]', ALL_NS))
  cName = utils.getElementValue(elem.find('./subfield[@code="a"]', ALL_NS))
  cRole = utils.getElementValue(elem.findall('./subfield[@code="4"]', ALL_NS))

  return (cID, cName, cRole)
  
# -----------------------------------------------------------------------------
def addContributorFieldsToContributorCSV(elem, writer, stats):
  """This function extracts contributor relevant data from the given XML element 'elem' and writes it to the given CSV file writer."""

  kbrID = utils.getElementValue(elem.find('./controlfield[@tag="001"]', ALL_NS))

  foundContributors = []
  linkedOrganizationNames = set()

  #
  # add person contributors from the field 100 (https://github.com/kbrbe/beltrans-data-integration/issues/71)
  #
  field100Contributors = elem.findall('./datafield[@tag="100"]', ALL_NS)
  for p in field100Contributors:
    c = PersonContributor.fromTuple(getContributorData(p))
    # every contributor may have several roles
    for cRole in c.getRoles(): 
      foundContributors.append({'contributorID': c.getIdentifier(), 'contributorName': c.getName(), 'contributorRole': cRole, 'uncertainty': 'no'})

  #
  # add person contributors from the linked authorities field
  #
  personContributors = elem.findall('./datafield[@tag="700"]', ALL_NS)
  for p in personContributors:
    c = PersonContributor.fromTuple(getContributorData(p))
    cID = c.getIdentifier()
    cName = c.getName()
    for cRole in c.getRoles():
      # Also persons can publish, thus we should add them for the later check on publishers
      if cRole == 'pbl':
        cName = utils.getNormalizedString(cName)
        linkedOrganizationNames.add(cName)
      foundContributors.append({'contributorID': cID, 'contributorName': cName, 'contributorRole': cRole, 'uncertainty': 'no'})

  #
  # add organizational contributors such as publishers
  #
  orgContributors = elem.findall('./datafield[@tag="710"]', ALL_NS)
  for o in orgContributors:
    uncertainty = 'no'
    c = OrganizationalContributor.fromTuple(getContributorData(o))
    cID = c.getIdentifier()
    cName = c.getName()
    linkedOrganizationNames.add(utils.getNormalizedString(cName))

    for cRole in c.getRoles():
      if c.roleUncertain():
        uncertainty = 'yes'
      cNameNorm = utils.getNormalizedString(cName)
      foundContributors.append({'contributorID': cID, 'contributorName': cNameNorm, 'contributorRole': cRole, 'uncertainty': uncertainty})

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
          textNameNorm = utils.getNormalizedString(textName)
          foundContributors.append({'contributorID': nameID, 'contributorName': textNameNorm, 'contributorRole': 'pbl', 'uncertainty': 'no'})
       

  #
  # write all we found to a file, one row per contribution
  #
  for cont in foundContributors:
    # we also need to add the ID of the bibliographic item the contributor contributed to
    cont['KBRID'] = kbrID
    writer.writerow(cont)
 

# -----------------------------------------------------------------------------
def addWorkFieldsToWorkCSV(elem, writer, stats):
  """This function extracts work relevant data from the given XML element 'elem' and writes it to the given CSV file writer."""

  #
  # extract relevant data from the current record
  #
  kbrID = utils.getElementValue(elem.find('./controlfield[@tag="001"]', ALL_NS))
  isbn = utils.getElementValue(elem.find('./datafield[@tag="020"]/subfield[@code="a"]', ALL_NS))
  bindingType = utils.getElementValue(elem.find('./datafield[@tag="020"]/subfield[@code="q"]', ALL_NS))
  title = utils.getElementValue(elem.find('./datafield[@tag="245"]/subfield[@code="a"]', ALL_NS))
  responsibilityStatement = utils.getElementValue(elem.find('./datafield[@tag="245"]/subfield[@code="c"]', ALL_NS))
  placeOfPublication = utils.getElementValue(elem.find('./datafield[@tag="264"]/subfield[@code="a"]', ALL_NS))
  yearOfPublication = utils.getElementValue(elem.find('./datafield[@tag="264"]/subfield[@code="c"]', ALL_NS))
  edition = utils.getElementValue(elem.find('./datafield[@tag="250"]/subfield[@code="a"]', ALL_NS))

  sourceKBRID = utils.getElementValue(elem.find('./datafield[@tag="765"]/subfield[@code="*"]', ALL_NS))
  sourceTitle = utils.getElementValue(elem.find('./datafield[@tag="765"]/subfield[@code="t"]', ALL_NS))
  sourceISBN = utils.getElementValue(elem.find('./datafield[@tag="765"]/subfield[@code="z"]', ALL_NS))

  languagesString = utils.getElementValue(elem.findall('./datafield[@tag="041"]/subfield[@code="a"]', ALL_NS))
  countryOfPublicationString = utils.getElementValue(elem.findall('./datafield[@tag="044"]/subfield[@code="a"]', ALL_NS))
  belgianBibliographyClassificationsString = utils.getElementValue(elem.findall('./datafield[@tag="911"]/subfield[@code="a"]', ALL_NS))

  
  # create a URI for all languages
  langURIsString = utils.createURIString(languagesString, ';', 'http://id.loc.gov/vocabulary/languages/')

  # create a URI for all countries
  countryURIsString = utils.createURIString(countryOfPublicationString, ';', 'http://id.loc.gov/vocabulary/countries/')

  # create a URI for all belgian bibliographic classifications
  bbURIsString = utils.createURIString(belgianBibliographyClassificationsString, ';', 'http://kbr.be/id/data/')

  isbn10 = ''
  isbn13 = ''
  try:
    isbn10 = utils.getNormalizedISBN10(isbn)
  except:
    stats['not-convertable-isbn'][isbn] = kbrID

  try:
    isbn13 = utils.getNormalizedISBN13(isbn)
  except:
    stats['erroneous-isbn'][isbn] = kbrID

  sourceISBN10 = ''
  sourceISBN13 = ''
  try:
    sourceISBN10 = utils.getNormalizedISBN10(sourceISBN)
  except:
    stats['not-convertable-isbn'][sourceISBN] = kbrID

  try:
    sourceISBN13 = utils.getNormalizedISBN13(sourceISBN)
  except:
    stats['erroneous-isbn'][sourceISBN] = kbrID



  newRecord = {
    'KBRID': kbrID,
    'isbn10': isbn10,
    'isbn13': isbn13,
    'title': title,
    'languages': langURIsString,
    'placeOfPublication': placeOfPublication,
    'countryOfPublication': countryURIsString,
    'yearOfPublication': yearOfPublication,
    'responsibilityStatement': responsibilityStatement,
    'bindingType': bindingType,
    'edition': edition,
    'belgianBibliography': bbURIsString,
    'sourceKBRID': sourceKBRID,
    'sourceISBN10': sourceISBN10,
    'sourceISBN13': sourceISBN13,
    'sourceTitle': sourceTitle
  }

  writer.writerow(newRecord)
     

# -----------------------------------------------------------------------------
def addCollectionLinksToCSV(elem, writer, stats):
  """This function extracts links to collections and writes the id of the publication, the id of the collection and name of the collection to the given CSV file writer."""

  
  kbrID = utils.getElementValue(elem.find('./controlfield[@tag="001"]', ALL_NS))
  collectionLinks = elem.findall('./datafield[@tag="773"]', ALL_NS)

  for cl in collectionLinks:
    collectionID = utils.getElementValue(cl.find('./subfield[@code="*"]', ALL_NS))
    collectionName = utils.getElementValue(cl.find('./subfield[@code="t"]', ALL_NS))

    newRecord = {
      'KBRID': kbrID,
      'collectionID': collectionID,
      'collection-name': collectionName
    }

    writer.writerow(newRecord)

# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format and generates statistics about used fields."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing MARC SLIM XML records')
  parser.add_option('-c', '--output-cont-file', action='store', help='The output contributor CSV file containing selected MARC fields (one contribution per row)')
  parser.add_option('-l', '--output-collection-links-file', action='store', help='The output work CSV file containing containing a link between publication and collections (one link per row)')
  parser.add_option('-w', '--output-work-file', action='store', help='The output work CSV file containing selected MARC fields (one work per row)')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_work_file) or (not options.output_cont_file) or (not options.output_collection_links_file) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  with open(options.output_cont_file, 'w') as outContFile, \
       open(options.output_collection_links_file, 'w') as outCollectionLinksFile, \
       open(options.output_work_file, 'w') as outWorkFile:

    workFields = ['KBRID', 'sourceKBRID', 'isbn10', 'isbn13', 'sourceISBN10', 'sourceISBN13', 'title', 'sourceTitle', 'collection', 'languages', 'placeOfPublication', 'countryOfPublication', 'yearOfPublication', 'responsibilityStatement', 'bindingType', 'edition', 'belgianBibliography']
    contFields = ['KBRID', 'contributorID', 'contributorName', 'contributorRole', 'uncertainty']
    collectionLinksFields = ['KBRID', 'collectionID', 'collection-name']

    workWriter = csv.DictWriter(outWorkFile, fieldnames=workFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    contWriter = csv.DictWriter(outContFile, fieldnames=contFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    collectionLinksWriter = csv.DictWriter(outCollectionLinksFile, fieldnames=collectionLinksFields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    workWriter.writeheader()
    contWriter.writeheader()
    collectionLinksWriter.writeheader()

    stats = {'unique-publishers-without-authority': set(), 'erroneous-isbn': {}, 'not-convertable-isbn': {}, 'counter': {} }
    # iterate over all XML Files in the given directory and count ISNI statistics
    for event, elem in ET.iterparse(options.input_file, events=('start', 'end')):

      # The parser finished reading one responseRecord, get information and then discard the record
      if  event == 'end' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):

        addWorkFieldsToWorkCSV(elem, workWriter, stats)
        addContributorFieldsToContributorCSV(elem, contWriter, stats)
        addCollectionLinksToCSV(elem, collectionLinksWriter, stats)

    numberUniquePublishersWithoutAuthorityRecord = len(stats['unique-publishers-without-authority'])
    print(f'Unique publishers without authority record: {numberUniquePublishersWithoutAuthorityRecord}')
    for key,val in stats['counter'].items():
      print(f'{key},{val}')

    numberInvalidISBNNumbers = len(stats['erroneous-isbn'])
    print(f'Invalid ISBN numbers: {numberInvalidISBNNumbers}')
    for key,val in stats['erroneous-isbn'].items():
      print(f'{key},{val}')

    numberNotConvertableISBNNumbers = len(stats['not-convertable-isbn'])
    print(f'ISBN numbers which could not be converted to ISBN 10: {numberNotConvertableISBNNumbers}')
    for key,val in stats['not-convertable-isbn'].items():
      print(f'{key},{val}')
main()
