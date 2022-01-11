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

ALL_NS = {'rdf': NS_RDF, 'rdfs': NS_RDFS, 'schema': NS_SCHEMA, 'madsrdf': NS_MADSRDF, 'dcterms': NS_DCTERMS, 'isni': NS_ISNI, 'owl': NS_OWL, 'xsd': NS_XSD, 'foaf': NS_FOAF, 'void': NS_VOID, 'rdagroup1elements': NS_RDAGROUP1}



# -----------------------------------------------------------------------------
def main():
  """This script reads RDF/XML files of the input directory and adds found subjects to a CSV file if they match the given predicate/object filter criteria."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-folder', action='store', help='The input folder containing RDF/XML files which should be filtered')
  parser.add_option('-o', '--output-file', action='store', help='The name of the CSV file in which the found subjects should be stored')
  parser.add_option('-f', '--filter-file', action='store', help='The name of a CSV file which contains predicate/object filter conditions, used to filter the input')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_folder) or (not options.output_file) or (not options.filter_file) ):
    parser.print_help()
    exit(1)

  uniqueISNIIdentifiers = set()
  processedRecords = 0
  recordsWithoutID = 0
  numRecordsTaken = 0

  for (prefix, uri) in ALL_NS.items():
    ET.register_namespace(prefix, uri)

  with open(options.filter_file, 'r') as filterFile, \
       open(options.output_file, 'w') as outFile:

    #
    # read the filter criteria
    #
    filterReader = csv.reader(filterFile, delimiter=',')
    filterCriteria = []
    for row in filterReader:
      if ';' in row[2]:
        filterCriteria.append((row[0], row[1], row[2].split(';')))
      else:
        filterCriteria.append((row[0], row[1], row[2]))


    rdfAbout = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'
    rdfResource = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'

    # open the output file
    outputWriter = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    #
    # read ISNI RDF records from input RDF/XML
    #
    inputFiles = os.listdir(options.input_folder)
    numberParsedFiles = 0
    numberXMLFiles = 0
    numberRecords = 0
    numberFilterPass = 0
    filteredRecordIDs = set()
    for inputFile in inputFiles:
      numberParsedFiles += 1
      if inputFile.endswith('.xml'):
        numberXMLFiles += 1
        for event, elem in ET.iterparse(os.path.join(options.input_folder, inputFile), events=('start', 'end')):

          #
          # The parser finished reading one subject containing one or more predicates
          #
          if  event == 'end' and elem.tag == ET.QName(NS_RDF, 'Description'):

            numberRecords += 1
            subject = elem.attrib[rdfAbout]

            for (predicate, operator, filterValue) in filterCriteria:

              # check if the currently read subject contains the predicate
              foundTriples = elem.findall(predicate, ALL_NS)

              # if we found the predicate one or more times iterate over it
              for po in foundTriples:

                # get the object value which is either an RDF resource or a literal value
                objectValue = po.attrib[rdfResource] if rdfResource in po.attrib else utils.getElementValue(po)

                # perform filter check
                filterPass = False
                if operator == '=':
                  if objectValue == filterValue:
                    filterPass = True
                elif operator == 'in':
                  if objectValue in filterValue:
                    filterPass = True
                elif operator == '>':
                  if objectValue > filterValue:
                    filterPass = True
                elif operator == '<':
                  if objectValue < filterValue:
                    filterPass = True
                else:
                  print(f'Error: unknown operator {operator}')

                if filterPass:
                  numberFilterPass += 1
                  filteredRecordIDs.add(subject)
                  outputWriter.writerow([subject])

            # discard record to keep space in main memory
            processedRecords += 1
            elem.clear()

    numberFilterPassUnique = len(filteredRecordIDs)
    print(f'{numberXMLFiles} XML files with {numberRecords} records read. {numberFilterPass} records ({numberFilterPassUnique} unique) matched filter criteria.')
 
main()
