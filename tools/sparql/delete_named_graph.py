#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import os
import re
import requests
import sys
from tools.sparql import utils_sparql
from optparse import OptionParser
from dotenv import load_dotenv

def parseArguments():

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-u', '--url', action='store', help='The URL of the SPARQL endpoint')
  parser.add_option('-n', '--named-graph', action='store', help='The name of the named graph which should be deleted')
  (options, args) = parser.parse_args()

  if( (not options.url) or (not options.named_graph) ):
    parser.print_help()
    exit(1)

  return (options, args)

# -----------------------------------------------------------------------------
def main(url, namedGraph):

  load_dotenv('.env')
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
 
  utils_sparql.deleteNamedGraph(url, namedGraph, auth=auth)

if __name__ == '__main__':
  (options, args) = parseArguments()
  main(options.url, options.named_graph)
 
