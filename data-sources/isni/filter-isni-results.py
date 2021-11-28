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

NS_RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
NS_RDFS = "http://www.w3.org/2000/01/rdf-schema#"
NS_SCHEMA = "http://schema.org/"
NS_MADSRDF = "http://www.loc.gov/mads/rdf/v1#"
NS_DCTERMS = "http://purl.org/dc/terms/"
NS_ISNI = "https://isni.org/ontology#"
NS_OWL = "http://www.w3.org/2002/07/owl#"
NS_XSD = "http://www.w3.org/2001/XMLSchema#"
NS_FOAF = "http://xmlns.com/foaf/0.1/"
NS_VOID = "http://rdfs.org/ns/void#"

ALL_NS = {'rdf': NS_RDF, 'rdfs': NS_RDFS, 'schema': NS_SCHEMA, 'madsrdf': NS_MADSRDF, 'dcterms': NS_DCTERMS, 'isni': NS_ISNI, 'owl': NS_OWL, 'xsd': NS_XSD, 'foaf': NS_FOAF, 'void': NS_VOID}



# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format and generates statistics about used fields."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input ISNI RDF/XML file which should be filtered')
  parser.add_option('-o', '--output-file', action='store', help='The name of the file in which the filtered ISNI XML should be stored')
  parser.add_option('-f', '--filter-file', action='store', help='The name of a CSV file which contains relevant ISNI identifiers in one column, used to filter the input')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) or (not options.filter_file) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  uniqueISNIIdentifiers = set()
  processedRecords = 0
  recordsWithoutID = 0
  numRecordsTaken = 0

  for (prefix, uri) in ALL_NS.items():
    ET.register_namespace(prefix, uri)

  with open(options.filter_file, 'r') as filterFile, \
       open(options.output_file, 'wb') as outFile:

    #
    # read relevant ISNI identifiers and store them for lookup
    #
    filterFileCounter = 0
    reader = csv.reader(filterFile, delimiter=',')
    for row in reader:
      uniqueISNIIdentifiers.add(row[0])
      filterFileCounter += 1
    numFilterIdentifiers = len(uniqueISNIIdentifiers)
    print(f'Successfully read {numFilterIdentifiers} unique ISNI identifiers from {filterFileCounter} records in given CSV file')
    
    outFile.write(b'<catalog>')

    #
    # read ISNI RDF records from input RDF/XML
    for event, elem in ET.iterparse(options.input_file, events=('start', 'end')):

      #
      # The parser finished reading one RDF ISNI entity
      #
      if  event == 'end' and elem.tag == ET.QName(NS_RDF, 'RDF'):

        #
        # add record to output if it fits the filter criteria
        #
        isniIDElement = elem.find('./rdf:Description/schema:identifier/rdf:Description/schema:propertyID/../schema:value', ALL_NS)
        if isniIDElement is not None:
          elementISNI = isniIDElement.text
          if elementISNI in uniqueISNIIdentifiers:
            numRecordsTaken += 1
            outFile.write(ET.tostring(elem, encoding='utf-8'))
        else:
          print("No ISNI ID found via schema:PropertyValue")
          recordsWithoutID += 1

        # discard record to keep space in main memory
        processedRecords += 1
        elem.clear()
    outFile.write(b'</catalog>')

    print(f'{numRecordsTaken} records from the input matched with the {numFilterIdentifiers} of the filter')
 
main()
