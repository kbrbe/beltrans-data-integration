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
from tqdm import tqdm

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
NS_SKOS = "http://www.w3.org/2004/02/skos/core#"
NS_BNF = "http://data.bnf.fr/ontology/bnf-onto/"
NS_RDAA = "http://rdaregistry.info/Elements/a/" 
NS_RDAU = "http://rdaregistry.info/Elements/u/"
NS_BNF_ROLES = "http://data.bnf.fr/vocabulary/roles/"
NS_BIO = "http://vocab.org/bio/0.1/"

ALL_NS = {'rdf': NS_RDF, 'rdfs': NS_RDFS, 'schema': NS_SCHEMA, 'madsrdf': NS_MADSRDF, 'dcterms': NS_DCTERMS, 'isni': NS_ISNI, 'owl': NS_OWL, 'xsd': NS_XSD, 'foaf': NS_FOAF, 'void': NS_VOID, 'rdagroup1elements': NS_RDAGROUP1, 'rdagroup2elements': NS_RDAGROUP2, 'marcrel': NS_MARCREL, 'skos': NS_SKOS, 'bnf-onto': NS_BNF, 'bnfroles': NS_BNF_ROLES, 'rdau': NS_RDAU, 'rdaa': NS_RDAA, 'bio': NS_BIO}


RDF_ABOUT = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'
RDF_RESOURCE = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'


# -----------------------------------------------------------------------------
def processFile(xmlFilename, relevantTranslations, filteredRecordIDs, outFile, stats, subjectPrefix, subjectTerm):

  #
  # read ISNI RDF records from input RDF/XML
  #
  for event, elem in ET.iterparse(xmlFilename, events=('start', 'end')):

    #
    # The parser finished reading one RDF ISNI entity
    #
    if  event == 'end' and elem.tag == ET.QName(ALL_NS[subjectPrefix], subjectTerm):

      stats['numberRecords'] += 1
      subject = elem.attrib[RDF_ABOUT]
      #
      # add record to output if it fits the filter criteria
      #

      subjectID = subject
      if subjectID in relevantTranslations:
        stats['numberFilterPass'] += 1
        filteredRecordIDs.add(subjectID)
        outFile.write(ET.tostring(elem, encoding='utf-8'))

      # discard record to keep space in main memory
      elem.clear()



# -----------------------------------------------------------------------------
def readLookupIdentifiers(filenames):

  #
  # read relevant identifiers and store them for lookup
  # read all given files and store the identifiers in different sets
  #
  lookupSets = []
  for filterFile in filenames:
    currentLookupSet = set()
    filterFileCounter = 0
    with open(filterFile, 'r') as fIn:
      reader = csv.reader(fIn, delimiter=',')
      for row in reader:
        identifier = row[0]
        currentLookupSet.add(identifier)
        filterFileCounter += 1
      numFilterIdentifiers = len(currentLookupSet)
      lookupSets.append(currentLookupSet)
      print(f'Successfully read {numFilterIdentifiers} identifiers from {filterFileCounter} records in given CSV file {filterFile}')


  relevantTranslations = set.intersection(*lookupSets)
  numberTrl = len(relevantTranslations)
  print(f'The intersection between the filters are {numberTrl} unique identifiers')
  return relevantTranslations



# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file with RDF data and adds all found records to the output file which have a subject found in the filter file."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input', action='store', help='The input file or folder containing RDF/XML files which should be filtered')
  parser.add_option('-o', '--output-file', action='store', help='The name of the file in which the filtered RDF/XML should be stored')
  parser.add_option('-f', '--filter-file', action='append', help='The name of a CSV file which contains relevant subject identifiers in one column, used to filter the input. If several files are provided a subject of the input needs to exist in all of the filter files (AND condition)')
  parser.add_option('--subject-tag', action='store', default='rdf:Description', help='The tag name used for a subject, could be for example RDF:Description or schema:Organization, default is rdf:Description')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input) or (not options.output_file) or (not options.filter_file) ):
    parser.print_help()
    exit(1)

  subjectPrefix, subjectTerm = options.subject_tag.split(':')
  if subjectPrefix not in ALL_NS:
    print(f'Unknown prefix {subjectPrefix}, should be one of {ALL_NS.keys()}')
    exit(1)


  for (prefix, uri) in ALL_NS.items():
    ET.register_namespace(prefix, uri)

  relevantTranslations = readLookupIdentifiers(options.filter_file)

  filteredRecordIDs = set()
  processedRecords = 0
  numberXMLFiles = 0

  print(f'Opening output file {options.output_file}')
  with open(options.output_file, 'wb') as outFile:

    outFile.write(b'<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:madsrdf="http://www.loc.gov/mads/rdf/v1#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:schema="http://schema.org/" xmlns:void="http://rdfs.org/ns/void#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">')

    stats = {'numberFilterPass': 0, 'numberRecords': 0}

    if os.path.isfile(options.input) and options.input.endswith('.xml'):
      numberXMLFiles += 1
      processFile(options.input, relevantTranslations, filteredRecordIDs, outFile, stats, subjectPrefix, subjectTerm)
    elif os.path.isdir(options.input):
      inputFiles = os.listdir(options.input)
      numberFiles = len(inputFiles)
      print(f'Start processing {numberFiles} files')
      for inputFile in tqdm(inputFiles):
        if inputFile.endswith('.xml'):
          numberXMLFiles += 1
          processFile(os.path.join(options.input, inputFile), relevantTranslations, filteredRecordIDs, outFile, stats, subjectPrefix, subjectTerm)
    else:
      print(f'Error: the input {options.input} is not a folder nor a file!')

    outFile.write(b'</rdf:RDF>')

    numberFilterPassUnique = len(filteredRecordIDs)
    numberFilterPass = stats['numberFilterPass']
    numberRecords = stats['numberRecords']
    print(f'{numberXMLFiles} XML files with {numberRecords} records read. {numberFilterPass} records ({numberFilterPassUnique} unique) matched filter criteria.')
     
main()
