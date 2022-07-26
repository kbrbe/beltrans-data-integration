#
# (c) 2022 Sven Lieber
# KBR Brussels
#

from rdflib import Graph
import csv
from optparse import OptionParser
import os


def main():
  """Execute the given SPARQL query in-memory with the given RDF input files."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-q', '--query-file', action='store', help='The input file containing the RDF data cube statistics')
  parser.add_option('-o', '--output-file', action='store', help='The CSV output file')
  (options, args) = parser.parse_args()

  if not options.query_file or not options.output_file:
    parser.print_help();
    exit(1)

  g = Graph()
  for inputFile in args:
    print(f'trying to parse {inputFile} ...')
    if inputFile.endswith('ttl'):
      g.parse(inputFile, format='turtle')
    elif inputFile.endswith('nt'):
      g.parse(inputFile, format='nt')
    elif inputFile.endswith('xml'):
      g.parse(inputFile, format='xml')
    else:
      print(f'Non recognized input format for the file "{inputFile}"')

  print(f'Parsed input files!')

  with open(options.query_file, 'r', encoding='utf-8') as sparqlFile, \
       open(options.output_file, 'w', encoding='utf-8') as outFile:

    sparqlQuery = sparqlFile.read()
    print(f'Execute SPARQL query {options.query_file} ...')
    results = g.query(sparqlQuery)
    print(f'successfully executed SPARQL query!')

    outputWriter = csv.writer(outFile)
    for row in results:
      outputWriter.writerow(row)

main()
