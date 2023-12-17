#
# (c) 2023 Sven Lieber
# KBR Brussels
#
import lxml.etree as ET
import os
import json
import itertools
import enchant
import hashlib
import csv
from optparse import OptionParser
from tools.xml.contributor import PersonContributor, OrganizationalContributor
from tools import utils

NS_MARCSLIM = 'http://www.loc.gov/MARC21/slim'

ALL_NS = {'marc': NS_MARCSLIM}

# -----------------------------------------------------------------------------
def getContributorData(elem):
  """This function extracts the ID, name, and role of a contributor and returns them."""

  cID = utils.getElementValue(elem.find('./marc:subfield[@code="*"]', ALL_NS))
  cName = utils.getElementValue(elem.find('./marc:subfield[@code="a"]', ALL_NS))
  cRole = utils.getElementValue(elem.findall('./marc:subfield[@code="4"]', ALL_NS))

  return (cID, cName, cRole)

# -----------------------------------------------------------------------------
def addContributorFieldsToContributorCSV(elem, writer, mainField, addedField):
  """This function extracts contributor relevant data from the given XML element 'elem' and writes it to the given CSV file writer."""

  kbrID = utils.getElementValue(elem.find('./marc:controlfield[@tag="001"]', ALL_NS))

  foundMainFieldContributors = []
  foundAddedFieldContributors = []

  #
  # add person/org contributors from the field 100 (https://github.com/kbrbe/beltrans-data-integration/issues/71)
  #
  mainFieldContributors = elem.findall(f'./marc:datafield[@tag="{mainField}"]', ALL_NS)
  for p in mainFieldContributors:
    c = None
    if mainField.startswith('10'):
      c = PersonContributor.fromTuple(getContributorData(p))
    elif mainField.startswith('11'):
      c = OrganizationalContributor.fromTuple(getContributorData(p))
    if c:
      # every contributor may have several roles
      for cRole in c.getRoles(): 
        foundMainFieldContributors.append({'contributorID': c.getIdentifier(), 'contributorName': c.getName(), 'contributorRole': cRole})

  #
  # add person/org contributors from the linked authorities field
  #
  addedFieldContributors = elem.findall(f'./marc:datafield[@tag="{addedField}"]', ALL_NS)
  for p in addedFieldContributors:
    c = None
    if addedField.startswith('70'):
      c = PersonContributor.fromTuple(getContributorData(p))
    elif addedField.startswith('71'):
      c = OrganizationalContributor.fromTuple(getContributorData(p))
    if c:
      for cRole in c.getRoles():
        foundAddedFieldContributors.append({'contributorID': c.getIdentifier(), 'contributorName': c.getName(), 'contributorRole': cRole})

  #
  # write all we found to a file, one row per contribution
  #
  for cont in foundMainFieldContributors + foundAddedFieldContributors:
    # we also need to add the ID of the bibliographic item the contributor contributed to
    cont['KBRID'] = kbrID
    writer.writerow(cont)
 

# -----------------------------------------------------------------------------
def main():
  """This script reads a MARCXML file and extracts linked authorities. It works in a streaming fashion and thus produces duplicate output rows."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing MARC SLIM XML records')
  parser.add_option('--output-persons', action='store', help='The output person contributor CSV file containing identifiers')
  parser.add_option('--output-orgs', action='store', help='The output org contributor CSV file containing identifiers')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_persons) or (not options.output_orgs) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  with open(options.output_persons, 'w') as personFile, \
       open(options.output_orgs, 'w') as orgFile:

    contFields = ['KBRID', 'contributorID', 'contributorName', 'contributorRole']

    personWriter = csv.DictWriter(personFile, fieldnames=contFields)
    orgWriter = csv.DictWriter(orgFile, fieldnames=contFields)

    personWriter.writeheader()
    orgWriter.writeheader()

    # iterate over all XML Files in the given directory and count ISNI statistics
    for event, elem in ET.iterparse(options.input_file, events=('start', 'end')):

      # The parser finished reading one responseRecord, get information and then discard the record
      if  event == 'end' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):

        addContributorFieldsToContributorCSV(elem, personWriter, "100", "700")
        addContributorFieldsToContributorCSV(elem, orgWriter, "110", "710")

main()
