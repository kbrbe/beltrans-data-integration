#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import os
import re
import requests
import sys
import utils_sparql
from optparse import OptionParser
from dotenv import load_dotenv

def parseArguments():

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-u', '--url', action='store', help='The URL of the SPARQL endpoint which is queried')
  parser.add_option('--content-type', action='store', help='The content type, for example application/sparql-update or text/turtle')
  parser.add_option('--named-graph', action='store', help='The name of an optional named graph')
  (options, args) = parser.parse_args()

  if( (not options.url) or (not options.content_type) ):
    parser.print_help()
    exit(1)

  if(options.named_graph):
    options.url = options.url + '?context-uri=' + options.named_graph

  return (options, args)

def main(url, contentType, namedGraph, files):

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
 
  for inputFile in files:
    queryName = ''
    if contentType == 'application/sparql-update':
      queryName = f'SPARQL-UPDATE (named graph "{namedGraph}")' if namedGraph else 'SPARQL-UPDATE'
    else:
      queryName = f'file uploaded (named graph "{namedGraph}")' if namedGraph else 'file uploaded'
    utils_sparql.sparqlUpdateFile(url, inputFile, contentType, queryName, auth=auth)

if __name__ == '__main__':
  (options, args) = parseArguments()
  main(options.url, options.content_type, options.named_graph, args)
 
