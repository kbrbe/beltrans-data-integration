#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import os
import re
import requests
import utils
from optparse import OptionParser
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
def main():
  """This script uses SPARQL INSERT/UPDATE queries to create a single named graph of data. For all creation queries all updates are executed several times."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-u', '--url', action='store', help='The URL of the SPARQL endpoint which is queried')
  parser.add_option('--number-updates', action='store', default=2, type='int', help='The number of update cycles after each creation (should be number of sources-1), default is 2')
  parser.add_option('--update-queries', action='store', help='A CSV file containing names of SPARQL query files which add sameAs links of found data to initially identified URIs')
  parser.add_option('--create-queries', action='store', help='A CSV file containing names of SPARQL query files which create URIs for data not yet linked to other sources')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.url) or (not options.update_queries) or (not options.create_queries) ):
    parser.print_help()
    exit(1)

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
    
  with open(options.update_queries, 'r', encoding='utf-8') as updateQueriesFile, \
       open(options.create_queries, 'r', encoding='utf-8') as createQueriesFile:

    updateQueries = list(csv.reader(updateQueriesFile, delimiter=','))
    createQueries = list(csv.reader(createQueriesFile, delimiter=',')) 

    # For all creation queries: create URIs, then run numDataSources-1 updates to link other data sources
    for c in createQueries:
      # create data
      print(f'CREATE data from {c[0]}')
      utils_sparql.sparqlUpdate(options.url, c[1], 'application/sparql-update', c[0], auth=auth)

      # perform update query per source to link found data to created URIs via sameAs
      for i in range(options.number_updates):
        print(f'Update cycle {i}/{options.number_updates}')
        for u in updateQueries:
          utils_sparql.sparqlUpdate(options.url, u[1], 'application/sparql-update', u[0], auth=auth)

if __name__ == '__main__':
  main()
