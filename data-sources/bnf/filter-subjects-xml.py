#
# (c) 2022 Sven Lieber
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
NS_RDAGROUP1 = "http://rdvocab.info/Elements/"
NS_RDAGROUP2 = "http://rdvocab.info/ElementsGr2/"
NS_MARCREL = "http://id.loc.gov/vocabulary/relators/"

ALL_NS = {'rdf': NS_RDF, 'rdfs': NS_RDFS, 'schema': NS_SCHEMA, 'madsrdf': NS_MADSRDF, 'dcterms': NS_DCTERMS, 'isni': NS_ISNI, 'owl': NS_OWL, 'xsd': NS_XSD, 'foaf': NS_FOAF, 'void': NS_VOID, 'rdagroup1elements': NS_RDAGROUP1, 'rdagroup2elements': NS_RDAGROUP2, 'marcrel': NS_MARCREL}


RDF_ABOUT = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'
RDF_RESOURCE = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'


# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format and generates statistics about used fields."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-folder', action='store', help='The input folder containing RDF/XML files which should be filtered')
  parser.add_option('-o', '--output-file', action='store', help='The name of the file in which the filtered RDF/XML should be stored')
  parser.add_option('-f', '--filter-file', action='append', help='The name of a CSV file which contains relevant subject identifiers in one column, used to filter the input. If several files are provided a subject of the input needs to exist in all of the filter files (AND condition)')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_folder) or (not options.output_file) or (not options.filter_file) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  filteredRecordIDs = set()
  processedRecords = 0
  recordsWithoutID = 0
  numRecordsTaken = 0
  numberParsedFiles = 0
  numberFilterPass = 0
  numberRecords = 0
  numberXMLFiles = 0

  for (prefix, uri) in ALL_NS.items():
    ET.register_namespace(prefix, uri)

  #
  # read relevant identifiers and store them for lookup
  # read all given files and store the identifiers in different sets
  #
  lookupSets = []
  for filterFile in options.filter_file:
    currentLookupSet = set()
    filterFileCounter = 0
    with open(filterFile, 'r') as fIn:
      reader = csv.reader(fIn, delimiter=',')
      for row in reader:
        identifier = utils.extractBnFIdentifier(row[0])
        currentLookupSet.add(identifier)
        filterFileCounter += 1
      numFilterIdentifiers = len(currentLookupSet)
      lookupSets.append(currentLookupSet)
      print(f'Successfully read {numFilterIdentifiers} unique ISNI identifiers from {filterFileCounter} records in given CSV file {filterFile}')



  with open(options.output_file, 'wb') as outFile:

    outFile.write(b'<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:madsrdf="http://www.loc.gov/mads/rdf/v1#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:schema="http://schema.org/" xmlns:void="http://rdfs.org/ns/void#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">')

    inputFiles = os.listdir(options.input_folder)
    for inputFile in inputFiles:
      numberParsedFiles += 1
      if inputFile.endswith('.xml'):
        numberXMLFiles += 1

       

        #
        # read ISNI RDF records from input RDF/XML
        for event, elem in ET.iterparse(os.path.join(options.input_folder, inputFile), events=('start', 'end')):

          #
          # The parser finished reading one RDF ISNI entity
          #
          if  event == 'end' and elem.tag == ET.QName(NS_RDF, 'Description'):

            numberRecords += 1
            subject = elem.attrib[RDF_ABOUT]
            #
            # add record to output if it fits the filter criteria
            #

            subjectID = utils.extractBnFIdentifier(subject)
            if all(subjectID in s for s in lookupSets):
              numberFilterPass += 1
              filteredRecordIDs.add(subjectID)
              outFile.write(ET.tostring(elem, encoding='utf-8'))

            # discard record to keep space in main memory
            processedRecords += 1
            elem.clear()
    outFile.write(b'</rdf:RDF>')

    numberFilterPassUnique = len(filteredRecordIDs)
    print(f'{numberXMLFiles} XML files with {numberRecords} records read. {numberFilterPass} records ({numberFilterPassUnique} unique) matched filter criteria.')
     
main()
