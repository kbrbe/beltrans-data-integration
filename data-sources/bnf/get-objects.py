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
from predicate_object_filter import PredicateObjectConfigFilter
from predicate_object_filter import PredicateObjectLookupFilter

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
def checkArguments(parser, options, args):

  # An input an output file are needed in any case
  if( (not options.input_folder) or (not options.output_file) or (not options.predicate) or (not options.lookup_file) ):
    parser.print_help()
    exit(1)

# -----------------------------------------------------------------------------
def main():
  """This script reads RDF/XML files of the input directory and adds found objects to a CSV file if they match the given predicate/object filter criteria."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-folder', action='store', help='The input folder containing RDF/XML files which should be filtered')
  parser.add_option('-o', '--output-file', action='store', help='The name of the CSV file in which the found objects should be stored')
  parser.add_option('-l', '--lookup-file', action='store', help='The name of a CSV file which contains one column with objects used to filter the predicates given with -p')
  parser.add_option('-p', '--predicate', action='append', help='the name of a predicate which should contain objects from the lookup file')
  (options, args) = parser.parse_args()

  # check that we got all necessary options
  checkArguments(parser, options, args)

  uniqueISNIIdentifiers = set()
  processedRecords = 0
  recordsWithoutID = 0
  numRecordsTaken = 0

  for (prefix, uri) in ALL_NS.items():
    ET.register_namespace(prefix, uri)

  # Initialize the filter which will be used

  with open(options.output_file, 'w') as outFile,\
       open(options.lookup_file, 'r') as lookupFile:

    lookupFileReader = csv.reader(lookupFile, delimiter=',')
    lookupValues = set()
    for row in lookupFileReader:
      lookupValues.add(row[0])
    f = PredicateObjectLookupFilter(lookupValues)

    # open the output file
    outputWriter = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    numberParsedFiles = 0
    numberXMLFiles = 0
    numberRecords = 0
    filteredRecordIDs = set()

    #
    # read ISNI RDF records from input RDF/XML files
    #
    inputFiles = os.listdir(options.input_folder)
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
            subject = elem.attrib[RDF_ABOUT]

            # the predicates provided by the commandline arguments are stored in an array, because there can be more than one
            for predicate in options.predicate:
              # check if the currently read subject contains the predicate
              foundTriples = elem.findall(predicate, ALL_NS)

              # if we found the predicate one or more times iterate over it
              for po in foundTriples:

                # get the object value which is either an RDF resource or a literal value
                objectValue = po.attrib[RDF_RESOURCE] if RDF_RESOURCE in po.attrib else utils.getElementValue(po)

                if f.passFilter(subject):
                  filteredRecordIDs.add(objectValue)
                  outputWriter.writerow([objectValue])

              # discard record to keep space in main memory
              processedRecords += 1
              elem.clear()

    numberFilterPass = f.getNumberPassed()
    numberFilterPassUnique = len(filteredRecordIDs)
    print(f'{numberXMLFiles} XML files with {numberRecords} records read. {numberFilterPass} records ({numberFilterPassUnique} unique) matched filter criteria.')
 

main()
