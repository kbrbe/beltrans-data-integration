#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import os
import re
import requests
import utils_sparql
from tools.sparql.query_builder import ContributorUpdateQuery, \
  OrganizationContributorCreateQuery, PersonContributorCreateQuery, ManifestationCreateQuery, ManifestationUpdateQuery
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
  parser.add_option('--create-queries', action='store',
                    help='A CSV file containing SPARQL UPDATE generation configutation to create URIs for data not yet linked to other sources')
  parser.add_option('--number-updates', action='store', default=2, type='int',
                    help='The number of update cycles after each creation (should be number of sources-1), default is 2')
  parser.add_option('--query-log-dir', action='store',
                    help='The optional name of a directory in which generated SPARQL queries will be stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.url) or (not options.query_type) or (not options.target_graph) \
          or (not options.update_queries) or (not options.create_queries) ):
    print("Missing parameters")
    parser.print_help()
    exit(1)

  if( options.query_type != 'manifestations' and options.query_type != 'contributors'):
    print(f'Type of queries can only be "manifestations" or "contributors", but you gave "{options.query_type}"')
    exit(1)

  for configFile in [options.create_queries, options.update_queries]:
    if not os.path.isfile(configFile):
      print(f'The given config "{configFile} is not a file"')
      exit(1)

  return (options, args)

# -----------------------------------------------------------------------------
def generateCreateQueryManifestations(sourceName, sourceGraph, targetGraph, originalsGraph):
  """This function uses the imported query generation module to generate a SPARQL INSERT query for manifestations."""

  entitySourceClass = 'schema:CreativeWork'
  entityTargetClass = 'schema:CreativeWork'
  titleProperty = 'schema:name'

  qb = ManifestationCreateQuery(source=sourceName, sourceGraph=sourceGraph, targetGraph=targetGraph,
                                originalsGraph=originalsGraph, entitySourceClass=entitySourceClass,
                                entityTargetClass=entityTargetClass, titleProperty=titleProperty)

  return qb.getQueryString()

# -----------------------------------------------------------------------------
def generateCreateQueryPersons(sourceName, sourceGraph, targetGraph, identifiersToAdd):
  """This function uses the imported query generation module to generate a SPARQL INSERT query for Persons."""

  if sourceName == 'BnF' or sourceName == 'bnf':
    nationalityProperty = 'rdagroup2elements:countryAssociatedWithThePerson'
    genderProperty = 'schema:gender'
    entitySourceClass = 'foaf:Person'
    labelProperty = 'foaf:name'
    familyNameProperty = 'foaf:familyName'
    givenNameProperty = 'foaf:givenName'
  elif sourceName == 'KBR' or sourceName == 'kbr':
    nationalityProperty = 'schema:nationality'
    genderProperty = 'schema:gender'
    entitySourceClass = 'schema:Person'
    labelProperty = 'rdfs:label'
    familyNameProperty = 'schema:familyName'
    givenNameProperty = 'schema:givenName'
  elif sourceName == 'NTA' or sourceName == 'nta':
    nationalityProperty = 'schema:nationality'
    genderProperty = 'schema:gender'
    entitySourceClass = 'schema:Person'
    labelProperty = 'schema:name'
    familyNameProperty = 'schema:familyName'
    givenNameProperty = 'schema:givenName'
  else:
    nationalityProperty = 'schema:nationality'
    genderProperty = 'schema:gender'
    entitySourceClass = 'schema:Person'
    labelProperty = 'rdfs:label'
    familyNameProperty = 'schema:familyName'
    givenNameProperty = 'schema:givenName'

  entityTargetClass = 'schema:Person'

  qb = PersonContributorCreateQuery(source=sourceName, sourceGraph=sourceGraph, targetGraph=targetGraph,
                              identifiersToAdd=identifiersToAdd, entitySourceClass=entitySourceClass,
                              entityTargetClass=entityTargetClass, nationalityProperty=nationalityProperty,
                              genderProperty=genderProperty, labelProperty=labelProperty, familyNameProperty=familyNameProperty,
                              givenNameProperty=givenNameProperty)
  return qb.getQueryString()

# -----------------------------------------------------------------------------
def generateCreateQueryOrganizations(sourceName, sourceGraph, targetGraph, identifiersToAdd):
  """This function uses the imported query generation module to generate a SPARQL INSERT query for Organizations."""

  if sourceName == 'BnF' or sourceName == 'bnf':
    countryProperty = 'rdagroup2elements:placeAssociatedWithTheCorporateBody'
    entitySourceClass = 'foaf:Organization'
    labelProperty = 'foaf:name'
  elif sourceName == 'KBR' or sourceName == 'kbr':
    countryProperty = 'schema:address/schema:addressCountry'
    entitySourceClass = 'schema:Organization'
    labelProperty = 'skos:prefLabel'
  elif sourceName == 'NTA' or sourceName == 'nta':
    countryProperty = 'schema:location/schema:addressCountry'
    entitySourceClass = 'schema:Organization'
    labelProperty = 'schema:name'
  else:
    countryProperty = 'schema:location/schema:addressCountry'
    entitySourceClass = 'schema:Organization'
    labelProperty = 'rdfs:label'

  entityTargetClass = 'schema:Organization'
  qb = OrganizationContributorCreateQuery(source=sourceName, sourceGraph=sourceGraph, targetGraph=targetGraph,
                              identifiersToAdd=identifiersToAdd, entitySourceClass=entitySourceClass,
                              entityTargetClass=entityTargetClass, countryProperty=countryProperty,
                              labelProperty=labelProperty)
  return qb.getQueryString()


# -----------------------------------------------------------------------------
def generateContributorsUpdateQuery(sourceName, sourceGraph, targetGraph, linkIdentifierName, identifiersToAdd):
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

  qb = ContributorUpdateQuery(source=sourceName, sourceGraph=sourceGraph, targetGraph=targetGraph,
                              identifierName=linkIdentifierName, identifiersToAdd=identifiersToAdd,
                              nationalityProperty=nationalityProperty, genderProperty=genderProperty, 
                              personClass=personClass, organizationClass=organizationClass)

  return qb.getQueryString()

# -----------------------------------------------------------------------------
def generateManifestationsUpdateQuery(sourceName, sourceGraph, targetGraph, originalsGraph, linkIdentifierName, identifiersToAdd):
  """This function uses the imported query generation module to generate a SPARQL UPDATE query for manifestations."""

  qb = ManifestationUpdateQuery(source=sourceName, sourceGraph=sourceGraph, targetGraph=targetGraph,
                                entitySourceClass='schema:CreativeWork',
                                originalsGraph=originalsGraph, linkIdentifier=linkIdentifierName,
                                identifiersToAdd=identifiersToAdd)
  return qb.getQueryString()

# -----------------------------------------------------------------------------
def getCreateQueryString(queryType, creationSourceType, creationSourceName, sourceGraph, targetGraph, originalsGraph,
                         identifiersToAdd):
  """This function checks the given parameter and instantiates an appropriate query builder whose query is returned."""

  queryString = ''
  if queryType == 'manifestations':
    queryString = generateCreateQueryManifestations(creationSourceName, sourceGraph, targetGraph, originalsGraph)
  elif queryType == 'contributors':
    if creationSourceType == 'persons':
      queryString = generateCreateQueryPersons(creationSourceName, sourceGraph,
                                               targetGraph, identifiersToAdd)
    else:
      queryString = generateCreateQueryOrganizations(creationSourceName, sourceGraph,
                                                     targetGraph, identifiersToAdd)

  return queryString

# -----------------------------------------------------------------------------
def getLinkIdentifierTuple(identifierName):
  """This function is a workaround, given an identifier name, hard coded properties are returned,
  e.g. given 'ISBN10' a tuple ('bibo:isbn10', 'ISBN10') is returned."""
  if identifierName == 'ISBN10':
    return ('bibo:isbn10', identifierName)
  elif identifierName == 'ISBN13':
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
                                         linkIdentifier, identifiersToAdd)

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
def main(url, queryType, targetGraph, createQueriesConfig, updateQueriesConfig, numberUpdates, queryLogDir=None):
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

  with open(updateQueriesConfig, 'r', encoding='utf-8') as updateQueriesFile, \
       open(createQueriesConfig, 'r', encoding='utf-8') as createQueriesFile:

    updateQueries = list(csv.DictReader(updateQueriesFile, delimiter=','))
    createQueries = list(csv.DictReader(createQueriesFile, delimiter=','))

    # For all creation queries: create URIs, then run numDataSources-1 updates to link other data sources
    for createConfigEntry in createQueries:
      creationSourceName = createConfigEntry['sourceName']
      creationSourceType = createConfigEntry['sourceType'] if 'sourceType' in createConfigEntry else ''

      # the identifiers which should be added during the creation of an integrated record
      createIdentifiersToAdd = createConfigEntry['identifiersToAdd'].split(',')

      # this property is only needed for the generation of manifestation queries, not for contributors
      creationOriginalsGraph = createConfigEntry['originalsGraph'] if 'originalsGraph' in createConfigEntry else ''

      creationQueryName = f'Create {creationSourceName}'

      print(f'CREATE {creationSourceType} data from {creationSourceName}')
      # Generate SPARQL query
      # For manifestations, the 'identifiersToAdd' will not be added, i.e. ISBN10 and ISBN13 will not become bf:identifiedBy, bf:Identifier
      creationQueryString = getCreateQueryString(queryType, creationSourceType, creationSourceName,
                                                 createConfigEntry['sourceGraph'], targetGraph, creationOriginalsGraph,
                                                 createIdentifiersToAdd)

      # Optionally serialize SPARQL query
      if queryLogDir:
        logSPARQLQuery(queryLogDir, creationQueryString, f'create-{queryType}-{creationSourceName}.sparql')

      # Execute SPARQL query
      utils_sparql.sparqlUpdate(url, creationQueryString, 'application/sparql-update', creationQueryName, auth=auth)

      # perform update query per source to link found data to created URIs via sameAs
      for i in range(numberUpdates):
        print(f'Update cycle {i+1}/{numberUpdates}')
        for updateConfigEntry in updateQueries:
          updateSourceName = updateConfigEntry['sourceName']
          linkIdentifier = updateConfigEntry['linkIdentifier']
          updateOriginalsGraph = updateConfigEntry['originalsGraph'] if 'originalsGraph' in updateConfigEntry else ''

          # the identifiers which should be added during an update of an already existing integrated record
          updateIdentifiersToAdd = updateConfigEntry['identifiersToAdd'].split(',')
          updateQueryName = f'Update {updateSourceName} via {linkIdentifier}'

          # Generate a SPARQL UPDATE query on the fly given the configuration entry updateConfigEntry and execute it
          updateQueryString = getUpdateQueryString(queryType, updateSourceName, updateConfigEntry['sourceGraph'], targetGraph,
                                                   updateOriginalsGraph, linkIdentifier, updateIdentifiersToAdd)


          # Optionally serialize SPARQL query (only the first time of the update cyclus)
          if queryLogDir and i == 0:
            logSPARQLQuery(queryLogDir, updateQueryString, f'update-{queryType}-{updateSourceName}-{linkIdentifier}.sparql')

          # Execute SPARQL query
          utils_sparql.sparqlUpdate(url, updateQueryString, 'application/sparql-update', updateQueryName, auth=auth)

if __name__ == '__main__':
  (options, args) = checkArguments()
  main(options.url, options.query_type, options.target_graph,
       options.create_queries, options.update_queries, options.number_updates, options.query_log_dir)
