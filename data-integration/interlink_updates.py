#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import os
import re
import requests
import utils_sparql
from tools.sparql.query_builder import ContributorSingleUpdateQuery, \
  OrganizationContributorCreateQuery, PersonContributorCreateQuery, \
  ManifestationCreateQuery, ManifestationCreateQueryIdentifiers, ManifestationUpdateQuery, \
  ManifestationSingleUpdateQuery
from optparse import OptionParser
from dotenv import load_dotenv
import time

# -----------------------------------------------------------------------------
def checkArguments():

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-u', '--url', action='store', help='The URL of the SPARQL endpoint which is queried')
  parser.add_option('--query-type', action='store',
                    help='Whether manifestations or contributors are updated (both require different types of queries)')
  parser.add_option('--target-graph', action='store',
                    help='The name of the graph to which data is added from a source graph')
  parser.add_option('--update-queries', action='store',
                    help='A CSV file containing SPARQL UPDATE generation configuration to add sameAs links of found data to initially identified URIs')
  parser.add_option('--number-updates', action='store', default=2, type='int',
                    help='The number of update cycles after each creation (should be number of sources-1), default is 2')
  parser.add_option('--query-log-dir', action='store',
                    help='The optional name of a directory in which generated SPARQL queries will be stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.url) or (not options.query_type) or (not options.target_graph) \
          or (not options.update_queries) ):
    print("Missing parameters")
    parser.print_help()
    exit(1)

  if( options.query_type != 'manifestations' and options.query_type != 'contributors'):
    print(f'Type of queries can only be "manifestations" or "contributors", but you gave "{options.query_type}"')
    exit(1)

  for configFile in [options.update_queries]:
    if not os.path.isfile(configFile):
      print(f'The given config "{configFile} is not a file"')
      exit(1)

  return (options, args)


# -----------------------------------------------------------------------------
def generateContributorsUpdateQuery(sourceName, sourceGraph, targetGraph, identifiersToAdd):
  """This function uses the imported query generation module to generate a SPARQL UPDATE."""

  if sourceName == 'BnF' or sourceName == 'bnf':
    nationalityProperty = 'rdagroup2elements:countryAssociatedWithThePerson'
    genderProperty = 'schema:gender'
    personClass = 'foaf:Person'
    organizationClass = 'foaf:Organization'
  else:
    nationalityProperty = 'schema:nationality'
    genderProperty = 'schema:gender'
    personClass = 'schema:Person'
    organizationClass = 'schema:Organization'

  qb = ContributorSingleUpdateQuery(source=sourceName, sourceGraph=sourceGraph, targetGraph=targetGraph,
                              identifiersToAdd=identifiersToAdd,
                              nationalityProperty=nationalityProperty, genderProperty=genderProperty, 
                              personClass=personClass, organizationClass=organizationClass, correlationListFilter=True)

  return qb.getQueryString()

# -----------------------------------------------------------------------------
def generateManifestationsUpdateQuery(sourceName, sourceGraph, targetGraph, originalsGraph, linkIdentifierName, identifiersToAdd):
  """This function uses the imported query generation module to generate a SPARQL UPDATE query for manifestations."""

  qb = ManifestationSingleUpdateQuery(source=sourceName, sourceGraph=sourceGraph, targetGraph=targetGraph,
                                entitySourceClass='schema:CreativeWork',
                                originalsGraph=originalsGraph, identifiersToAdd=identifiersToAdd)
  return qb.getQueryString()

# -----------------------------------------------------------------------------
def getLinkIdentifierTuple(identifierName):
  """This function is a workaround, given an identifier name, hard coded properties are returned,
  e.g. given 'ISBN10' a tuple ('bibo:isbn10', 'ISBN10') is returned."""
  if identifierName == 'ISBN-10':
    return ('bibo:isbn10', identifierName)
  elif identifierName == 'ISBN-13':
    return ('bibo:isbn13', identifierName)
  else:
    return ''

# -----------------------------------------------------------------------------
def getUpdateQueryString(queryType, sourceName, sourceGraph, targetGraph, originalsGraph,
                         linkIdentifier, identifiersToAdd):
  """This function checks the given parameter and instantiates an appropriate update query builder whose query is returned."""

  queryString = ''
  if queryType == 'manifestations':
    identifiersToAddTuples = [getLinkIdentifierTuple(name) for name in identifiersToAdd]
    queryString = generateManifestationsUpdateQuery(sourceName, sourceGraph, targetGraph, originalsGraph,
                                           getLinkIdentifierTuple(linkIdentifier), identifiersToAddTuples)
  elif queryType == 'contributors':
    queryString = generateContributorsUpdateQuery(sourceName, sourceGraph, targetGraph,
                                         identifiersToAdd)

  return queryString


# -----------------------------------------------------------------------------
def logSPARQLQuery(queryLogDir, queryString, queryFilename):

  try:
    with open(os.path.join(queryLogDir, queryFilename), 'w') as queryOut:
      queryOut.write(queryString)
  except Exception as e:
    print(f'Warning: the query log "{queryFilename}" could not be created in the folder {queryLogDir}')
    print(e)

# -----------------------------------------------------------------------------
def main(url, queryType, targetGraph, updateQueriesConfig, numberUpdates, queryLogDir=None):
  """This script uses SPARQL INSERT/UPDATE queries to create a single named graph of data. For all creation queries all updates are executed several times."""


  load_dotenv()
  userEnvVar="ENV_SPARQL_ENDPOINT_USER"
  passwordEnvVar="ENV_SPARQL_ENDPOINT_PASSWORD"
  user = os.getenv(userEnvVar)
  password = os.getenv(passwordEnvVar)

  auth=None
  if(user == None or password == None):
    print(f'No SPARQL endpoint user or password specified using environment variable "{userEnvVar}" and "{passwordEnvVar}"')
    print(f'continuing without authentication')
  else:
    auth=(user,password)

  # If an optional query log directory is given, first check if it actually exists
  if queryLogDir:
    if not os.path.isdir(queryLogDir):
      print(f'Given optional query log directory does not exist, please provide a valid directory')
      exit(1)

  with open(updateQueriesConfig, 'r', encoding='utf-8') as updateQueriesFile:

    updateQueries = list(csv.DictReader(updateQueriesFile, delimiter=','))

    # perform update query per source to link found data to created URIs via sameAs
    for i in range(numberUpdates):
      print(f'Update cycle {i+1}/{numberUpdates}')
      for updateConfigEntry in updateQueries:
        updateSourceName = updateConfigEntry['sourceName']
        identifierName = updateConfigEntry['linkIdentifier'] if 'linkIdentifier' in updateConfigEntry else 'all'
        updateOriginalsGraph = updateConfigEntry['originalsGraph'] if 'originalsGraph' in updateConfigEntry else ''

        # the identifiers which should be added during an update of an already existing integrated record
        updateIdentifiersToAdd = updateConfigEntry['identifiersToAdd'].split(',')
        updateQueryName = f'Update {updateSourceName} via all found identifiers'

        # Generate a SPARQL UPDATE query on the fly given the configuration entry updateConfigEntry and execute it
        updateQueryString = getUpdateQueryString(queryType, updateSourceName, updateConfigEntry['sourceGraph'], targetGraph,
                                                 updateOriginalsGraph, identifierName, updateIdentifiersToAdd)


        # Optionally serialize SPARQL query (only the first time of the update cyclus)
        if queryLogDir and i == 0:
          logSPARQLQuery(queryLogDir, updateQueryString, f'update-{queryType}-{updateSourceName}-{identifierName}.sparql')

        # Execute SPARQL query
        utils_sparql.sparqlUpdate(url, updateQueryString, 'application/sparql-update', updateQueryName, auth=auth)

if __name__ == '__main__':
  (options, args) = checkArguments()
  main(options.url, options.query_type, options.target_graph,
       options.update_queries, options.number_updates, options.query_log_dir)
