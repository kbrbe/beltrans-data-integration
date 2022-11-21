#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import os
import re
import requests
import sys
import tools.sparql.utils_sparql
from optparse import OptionParser
from dotenv import load_dotenv

def parseArguments():

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-u', '--url', action='store', help='The URL of the SPARQL endpoint which is queried')
  parser.add_option('-q', '--query-file', action='store', help='The SPARQL query which will be sent using Content-type application/sparql-query')
  parser.add_option('-o', '--output-file', action='store', help='The file in which the requested data will be stored')
  parser.add_option('--accept-format', action='store', default='text/csv', help='The desired output format, e.g. text/csv or application/json, default is text/csv')
  parser.add_option('--named-graph', action='store', help='The name of an optional named graph')
  (options, args) = parser.parse_args()

  if( (not options.url) or (not options.query_file) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  if(options.named_graph):
    options.url = options.url + '?context-uri=' + options.named_graph

  return (options, args)

# -----------------------------------------------------------------------------
def main(url, queryFilename, outputFilename, acceptFormat, namedGraph):

  load_dotenv()
  userEnvVar="ENV_SPARQL_ENDPOINT_USER"
  passwordEnvVar="ENV_SPARQL_ENDPOINT_PASSWORD"
  user = os.getenv(userEnvVar)
  password = os.getenv(passwordEnvVar)

  auth=None
  if(user == None or password == None):
    print(f'No SPARQL endpoint user or password specified using environment variable "{userEnvVar}" and "{passwordEnvVar}"')
    print(f'continuing with no authentication')
  else:
    auth=(user,password)
 
  utils_sparql.sparqlSelect(url, queryFilename, outputFilename, acceptFormat, auth=auth)

if __name__ == '__main__':
  (options, args) = parseArguments()
  main(options.url, options.query_file, options.output_file, options.accept_format, options.named_graph)
 
