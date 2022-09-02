#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import os
import re
import requests
import utils_sparql
from integration_queries.query_builder import ContributorUpdateQuery, OrganizationContributorCreateQuery, PersonContributorCreateQuery
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
def generateCreateQueryPersons(sourceName, sourceGraph, targetGraph, identifiersToAdd):
  """This function uses the imported query generation module to generate a SPARQL INSERT query for Persons."""

  if sourceName == 'BnF' or sourceName == 'bnf':
    nationalityProperty = 'rdagroup2elements:countryAssociatedWithThePerson'
    entitySourceClass = 'foaf:Person'
    entityTargetClass = 'schema:Person'
    labelProperty = 'foaf:name'
    familyNameProperty = 'foaf:familyName'
    givenNameProperty = 'foaf:givenName'
  else:
    nationalityProperty = 'schema:location/schema:addressCountry'
    entitySourceClass = 'schema:Person'
    entityTargetClass = 'schema:Person'
    labelProperty = 'skos:prefLabel'
    familyNameProperty = 'schema:familyName'
    givenNameProperty = 'schema:givenName'

  qb = PersonContributorCreateQuery(source=sourceName, sourceGraph=sourceGraph, targetGraph=targetGraph,
                              identifiersToAdd=identifiersToAdd, entitySourceClass=entitySourceClass,
                              entityTargetClass=entityTargetClass, nationalityProperty=nationalityProperty,
                              labelProperty=labelProperty, familyNameProperty=familyNameProperty,
                              givenNameProperty=givenNameProperty)
  return qb.getQueryString()

# -----------------------------------------------------------------------------
def generateCreateQueryOrganizations(sourceName, sourceGraph, targetGraph, identifiersToAdd):
  """This function uses the imported query generation module to generate a SPARQL INSERT query for Organizations."""

  if sourceName == 'BnF' or sourceName == 'bnf':
    countryProperty = 'rdagroup2elements:placeAssociatedWithTheCorporateBody'
    entitySourceClass = 'foaf:Organization'
    entityTargetClass = 'schema:Organization'
    labelProperty = 'foaf:name'
  else:
    countryProperty = 'schema:location/schema:country'
    entitySourceClass = 'schema:Organization'
    entityTargetClass = 'schema:Organization'
    labelProperty = 'rdfs:label'

  qb = OrganizationContributorCreateQuery(source=sourceName, sourceGraph=sourceGraph, targetGraph=targetGraph,
                              identifiersToAdd=identifiersToAdd, entitySourceClass=entitySourceClass,
                              entityTargetClass=entityTargetClass, countryProperty=countryProperty,
                              labelProperty=labelProperty)
  return qb.getQueryString()



# -----------------------------------------------------------------------------
def generateUpdateQuery(sourceName, sourceGraph, targetGraph, linkIdentifierName, identifiersToAdd):
  """This function uses the imported query generation module to generate a SPARQL UPDATE."""

  if sourceName == 'BnF' or sourceName == 'bnf':
    nationalityProperty = 'rdagroup2elements:countryAssociatedWithThePerson'
    personClass = 'foaf:Person'
    organizationClass = 'foaf:Organization'
  else:
    nationalityProperty = 'schema:nationality'
    personClass = 'schema:Person'
    organizationClass = 'schema:Organization'

  qb = ContributorUpdateQuery(source=sourceName, sourceGraph=sourceGraph, targetGraph=targetGraph,
                              identifierName=linkIdentifierName, identifiersToAdd=identifiersToAdd,
                              nationalityProperty=nationalityProperty, personClass=personClass,
                              organizationClass=organizationClass)

  return qb.getQueryString()

# -----------------------------------------------------------------------------
def main(url, queryType, targetGraph, createQueriesConfig, updateQueriesConfig, numberUpdates):
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

  with open(updateQueriesConfig, 'r', encoding='utf-8') as updateQueriesFile, \
       open(createQueriesConfig, 'r', encoding='utf-8') as createQueriesFile:

    updateQueries = list(csv.DictReader(updateQueriesFile, delimiter=','))
    createQueries = list(csv.DictReader(createQueriesFile, delimiter=','))

    # For all creation queries: create URIs, then run numDataSources-1 updates to link other data sources
    for createConfigEntry in createQueries:
      creationSourceName = createConfigEntry['sourceName']
      creationSourceType = createConfigEntry['sourceType']
      createIdentifiersToAdd = createConfigEntry['identifiersToAdd'].split(',')
      creationQueryName = f'Create {creationSourceName}'
      # create data
      print(f'CREATE {creationSourceType} data from {creationSourceName}')

      if creationSourceType == 'persons':
        creationQueryString = generateCreateQueryPersons(creationSourceName, createConfigEntry['sourceGraph'],
                                                         targetGraph, createIdentifiersToAdd)
      else:
        creationQueryString = generateCreateQueryOrganizations(creationSourceName, createConfigEntry['sourceGraph'],
                                                         targetGraph, createIdentifiersToAdd)

      utils_sparql.sparqlUpdate(url, creationQueryString, 'application/sparql-update', creationQueryName, auth=auth)

      # perform update query per source to link found data to created URIs via sameAs
      for i in range(numberUpdates):
        print(f'Update cycle {i+1}/{numberUpdates}')
        for updateConfigEntry in updateQueries:
          updateSourceName = updateConfigEntry['sourceName']
          linkIdentifier = updateConfigEntry['linkIdentifier']
          updateIdentifiersToAdd = updateConfigEntry['identifiersToAdd'].split(',')
          updateQueryName = f'Update {updateSourceName} via {linkIdentifier}'

          # Generate a SPARQL UPDATE query on the fly given the configuration entry updateConfigEntry and execute it
          updateQueryString = generateUpdateQuery(updateSourceName, updateConfigEntry['sourceGraph'], targetGraph,
                                                  linkIdentifier, updateIdentifiersToAdd)

          utils_sparql.sparqlUpdate(url, updateQueryString, 'application/sparql-update', updateQueryName, auth=auth)

if __name__ == '__main__':
  (options, args) = checkArguments()
  main(options.url, options.query_type, options.target_graph,
       options.create_queries, options.update_queries, options.number_updates)
