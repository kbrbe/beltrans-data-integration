
# (c) 2024 Sven Lieber
# KBR Brussels
#
import csv
import os
import re
import json
import requests
import subprocess
from argparse import ArgumentParser
from dotenv import load_dotenv
import time
#from work_set_clustering.clustering import clusterFromScratch
from work_set_clustering.clustering import updateClusters
from tools.sparql import utils_sparql
from tools.sparql.query_builder import ContributorSingleUpdateQuery, \
  OrganizationContributorCreateQuery, PersonContributorCreateQuery, \
  ManifestationCreateQuery, ManifestationCreateQueryIdentifiers, ManifestationUpdateQuery, \
  ManifestationSingleUpdateQuery, IdentifiersDescriptiveKeysQuery, \
  ClustersDescriptiveKeysQuery, PropertyUpdateSimpleQuery, \
  PropertyUpdateSimpleMappingQuery, PropertyUpdateComplexMappingQuery, \
  PropertyUpdatePropertyPathQuery, ClustersDescriptiveKeysSameAsQuery


# -----------------------------------------------------------------------------
def main(url, queryType, targetGraph, configFilename, queryLogDir=None):
  """This script uses work set clustering to create a single named graph of data."""


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

  with open(configFilename, 'r', encoding='utf-8') as configFile:
    config = json.load(configFile)
    descriptiveKeyIdentifiers = config['integration']['identifiers']

    # (1) Create descriptive keys for each data source
    #
    print(f'\t1. Create descriptive keys')
    targetTypeString = config['integration']['targetType'].replace(':','_')
    descriptiveKeysFilenames = []
    for sourceName, configEntry in config['sources'].items():
      # get descriptive keys from the different data sources for clustering
      descriptiveKeysComponentsFilename = os.path.join(f'descriptive-keys-components-{targetTypeString}-{sourceName}.csv')
      descriptiveKeysFilename = os.path.join(queryLogDir, f'descriptive-keys-{targetTypeString}-{sourceName}.csv')
      descriptiveKeysQueryFilename = f'descriptive-keys-{targetTypeString}-{sourceName}-query.sparql'

      getDescriptiveKeys(url, descriptiveKeyIdentifiers, sourceName, config['integration']['targetType'], configEntry, targetGraph, auth, descriptiveKeysComponentsFilename, descriptiveKeysFilename, descriptiveKeysQueryFilename, "elementID", "descriptiveKey", queryLogDir=queryLogDir)
      descriptiveKeysFilenames.append(descriptiveKeysFilename)

    # (2) get initial cluster information from already existing records created from correlation list
    #
    #(existingClusterAssignment, existingDescriptiveKeys) = getExistingClusters(url, targetGraph, config, "elementID", "descriptiveKey", auth)
    print(f'\t2. Get initial cluster information')
    existingClusterAssignment = getExistingClusters(url, targetGraph, config, "elementID", "descriptiveKey", auth)

    clusterFilename=os.path.join(queryLogDir, f'integration-clusters-{targetTypeString}.csv')
    clusterComponentsFilename=os.path.join(queryLogDir, f'integration-cluster-components-{targetTypeString}.csv')

    # (3) perform the clustering to integrate the data
    #
    print(f'\t3. Perform the clustering')
    updateClusters(
      inputFilenames=descriptiveKeysFilenames,
      outputFilename=clusterFilename,
      idColumnName='elementID',
      keyColumnName='descriptiveKey',
      delimiter=',',
      existingClustersFilename=existingClusterAssignment
      #existingClusterKeysFilename=existingDescriptiveKeys
    )

    with open(clusterFilename, 'r') as clusterFile, \
       open(clusterComponentsFilename, 'w') as clusterComponentsFile:

      inputReader = csv.DictReader(clusterFile)
      clusterComponentsWriter = csv.DictWriter(clusterComponentsFile, fieldnames=['identifierName', 'identifier', 'clusterID'])
      clusterComponentsWriter.writeheader()
      for row in inputReader:
        identifierComponents = row['elementID'].split('/')
        clusterComponentsWriter.writerow({'identifierName': identifierComponents[0], 'identifier': identifierComponents[1], 'clusterID': row['clusterID']})


    # (4) Build and upload RDF data of integrated data based on clustering result
    #
    print(f'\t4.1 Generate RDF data')
    mappingFilename = config['integration']['mappingFile']
    integratedDataTurtleFilename = os.path.join(queryLogDir, f'integrated-data-{targetTypeString}.ttl')
    myEnv = os.environ.copy()
    myEnv['RML_SOURCE_INTEGRATION_CLUSTERS'] = clusterComponentsFilename
    subprocess.run([f'bash map.sh {mappingFilename} {integratedDataTurtleFilename}'], shell=True, env=myEnv, check=True)

    integratedDataNamedGraph = config['integration']['namedGraph']
    uploadNamedGraphURL = url + '?context-uri=' + integratedDataNamedGraph

    # 2025-08-01: use the Blazegraph data loader instead of utils_sparql.sparqlUpdateFile  (as we also do in the general integrate-data.sh script)
    #utils_sparql.sparqlUpdateFile(uploadNamedGraphURL, integratedDataTurtleFilename, 'text/turtle', f'file "{integratedDataTurtleFilename} uploaded (named graph: {integratedDataNamedGraph})', auth)

    print(f'\t4.2 Upload RDF data')
    uploadIntegratedDataCommand = f'source ./integration-functions.sh && uploadRDFData "{myEnv["ENV_SPARQL_ENDPOINT"]}" "integration" "{integratedDataNamedGraph}" "text/turtle" "{integratedDataTurtleFilename}"'
    subprocess.run([f'bash', '-c', uploadIntegratedDataCommand], env=myEnv, check=True)

    # (5a) Finalize integration by adding integration identifiers (descipritve keys) via the created sameAs links to the integrated data
    # this will use the bf:identifiedBy property
    print(f'\t5.1 adding integration identifiers')
    for sourceName, configEntry in config['sources'].items():
      queryString = ClustersDescriptiveKeysSameAsQuery(
                      targetGraph=targetGraph,
                      sourceGraph=configEntry['namedGraph'],
                      linkProperty="schema:sameAs",
                      memberIdentifiers=config['integration']['identifiers'],
                      targetType=config['integration']['targetType'],
                      sourceType=configEntry['sourceType']).getQueryString()

      # the following is a SPARQL UPDATE query, it's fine to use utils_sparql.sparqlUpdateFile directly 
      # instead of bash script that eventually would also call the same Python script for SPARQL UPDATE queries
      queryFilename = f'add-identifiers-query-{sourceName}-{config["integration"]["targetType"]}.sparql'
      queryFilename = queryFilename.replace(':', '_')
      if queryLogDir:
        logSPARQLQuery(queryLogDir, queryString, queryFilename)
      utils_sparql.sparqlUpdateFile(
        url, 
        os.path.join(queryLogDir, queryFilename), 
        'application/sparql-update', 
        f'SPARQL UPDATE {queryFilename})', 
        auth)



    targetType = config['integration']['targetType']
    # (5b) Finalize integration by adding certain data fields via the created sameAs links to the integrated data
    #
    # Iterate over each data source and add properties from it
    print(f'\t5.2 Adding data fields via sameAs links')
    for sourceName, configEntry in config['sources'].items():

      sourceType = configEntry['sourceType']
      # Add one property at a time to have a single fast query without OPTIONAL statements
      for propertyConfig in configEntry['properties']:
        queryString = ""
        if "targetProperty" in propertyConfig and "sourceProperty" in propertyConfig and "sourceGraphType" in propertyConfig and "sourceGraphLinkProperty" in propertyConfig:
          queryString = PropertyUpdateComplexMappingQuery(
                          targetGraph=targetGraph,
                          sourceGraph=configEntry['namedGraph'],
                          targetProperty=propertyConfig['targetProperty'],
                          sourceProperty=propertyConfig['sourceProperty'],
                          sourcePropertyGraph=configEntry[propertyConfig['sourceGraphType']],
                          sourceGraphLinkProperty=propertyConfig['sourceGraphLinkProperty'],
                          linkProperty="schema:sameAs",
                          targetType=targetType,
                          sourceType=sourceType).getQueryString()

        elif "targetProperty" in propertyConfig and "targetPropertyEntityUUID" in propertyConfig and "targetPropertyEntityPrefix"  in propertyConfig:
          queryString = PropertyUpdatePropertyPathQuery(
                          targetGraph=targetGraph,
                          sourceGraph=configEntry['namedGraph'],
                          targetProperty=propertyConfig['targetProperty'],
                          linkProperty="schema:sameAs",
                          targetPropertyEntityUUID=propertyConfig['targetPropertyEntityUUID'],
                          targetPropertyEntityType=propertyConfig['targetPropertyEntityType'],
                          targetPropertyEntityPrefix=propertyConfig['targetPropertyEntityPrefix'],
                          targetType=config['integration']['targetType'],
                          sourceType=configEntry['sourceType']).getQueryString()

        elif "targetProperty" in propertyConfig and "sourceProperty" in propertyConfig:
          queryString = PropertyUpdateSimpleMappingQuery(
                          targetGraph=targetGraph,
                          sourceGraph=configEntry['namedGraph'],
                          targetProperty=propertyConfig['targetProperty'],
                          sourceProperty=propertyConfig['sourceProperty'],
                          linkProperty="schema:sameAs",
                          targetType=config['integration']['targetType'],
                          sourceType=configEntry['sourceType']).getQueryString()

        elif "targetProperty" in propertyConfig:
          queryString = PropertyUpdateSimpleQuery(
                          targetGraph=targetGraph,
                          sourceGraph=configEntry['namedGraph'], 
                          property=propertyConfig['targetProperty'],
                          linkProperty="schema:sameAs",
                          targetType=config['integration']['targetType'],
                          sourceType=configEntry['sourceType']).getQueryString()
        else:
          print(f'Incomplete properties config, please provide at least a targetProperty')
          continue

        queryFilename = ""
        if isinstance(propertyConfig["targetProperty"], list):
          targetPropertyString = '-'.join(propertyConfig['targetProperty'])
          queryFilename = f'property-update-query-{sourceName}-{targetPropertyString}.sparql'
        else:
          queryFilename = f'property-update-query-{sourceName}-{sourceType}-{targetType}-{propertyConfig["targetProperty"]}.sparql'
        queryFilename = queryFilename.replace(':', '_')
        if queryLogDir:
          logSPARQLQuery(queryLogDir, queryString, queryFilename)
        utils_sparql.sparqlUpdateFile(
          url, 
          os.path.join(queryLogDir, queryFilename), 
          'application/sparql-update', 
          f'SPARQL UPDATE {queryFilename})', 
          auth)

    # (6) Finalize integration by running postprocessing queries
    #
    # Iterate over each query and execute it
    print(f'\t6. Running postprocess queries')
    if 'postIntegrationQueries' in config['integration']:
      for postQueryFilename in config['integration']['postIntegrationQueries']:
        
        utils_sparql.sparqlUpdateFile(
          url, 
          postQueryFilename, 
          'application/sparql-update', 
          f'SPARQL UPDATE {postQueryFilename})', 
          auth)


# -----------------------------------------------------------------------------
def getExistingClusters(url, targetGraph, config, entityIDColumnName, descriptiveKeyColumnName, auth, queryLogDir=None):

  descriptiveKeyIdentifiers = config['integration']['identifiers']
  namedGraph = config['existingClusters']['namedGraph']
  dataSourceIdentifiers = config['existingClusters']['dataSourceIdentifiers']

  # querying the descriptive keys from the correlation list is probably not what we want, https://github.com/kbrbe/work-set-clustering/issues/9
  # query descriptive keys
  #descriptiveKeysQueryString = ClustersDescriptiveKeysQuery(
  #  targetGraph="http://beltrans-manifestations", 
  #  memberIdentifiers=dataSourceIdentifiers, 
  #  keyIdentifiers=descriptiveKeyIdentifiers, 
  #  entitySourceClass=config['integration']['targetType']).getQueryString()

  #existingKeysComponentsFilename = f'existing-cluster-key-components.csv'
  #existingKeysFilename = f'existing-clusters-keys.csv'
  #existingKeysQueryFilename = f'existing-clusters-keys-query.sparql'

  # Optionally serialize SPARQL query
  #if queryLogDir:
  #  logSPARQLQuery(queryLogDir, descriptiveKeysQueryString, existingKeysQueryFilename)

  # Execute SPARQL query and save resulting descriptive keys to file
  #with open(existingKeysComponentsFilename, 'w', encoding='utf-8') as descriptiveKeyFile:
  #  utils_sparql.query(url, descriptiveKeysQueryString, descriptiveKeyFile, auth=auth)

  # Create descriptive key strings from the seperate columns
  # The SPARQL query could immediately CONCAT, but this goes hard on performance
  #with open(existingKeysComponentsFilename, 'r') as descriptiveKeysComponentsFile, \
  #     open(existingKeysFilename, 'w') as descriptiveKeyFile:

  #  inputReader = csv.DictReader(descriptiveKeysComponentsFile)
  #  descriptiveKeysWriter = csv.DictWriter(descriptiveKeyFile, fieldnames=[entityIDColumnName, descriptiveKeyColumnName])
  #  descriptiveKeysWriter.writeheader()
  #  for row in inputReader:
  #    descriptiveKeysWriter.writerow({entityIDColumnName: '/'.join([row['memberName'], row['memberIdentifier']]), descriptiveKeyColumnName: '/'.join([row['keyIdentifierName'], row['keyIdentifier']])})

  # query cluster assignment
  existingClusterAssignmentsComponentsFilename = f'existing-cluster-assignments-components.csv'
  existingClusterAssignmentsFilename = f'existing-clusters-assignments.csv'
  existingClusterAssignmentsQueryFilename = f'existing-clusters-assignments-query.sparql'

  getDescriptiveKeys(url, config['existingClusters']['dataSourceIdentifiers'], "", config['existingClusters']['sourceType'], config['existingClusters'], targetGraph, auth, existingClusterAssignmentsComponentsFilename, existingClusterAssignmentsFilename, existingClusterAssignmentsQueryFilename, "clusterID", "elementID", queryLogDir=queryLogDir)

  #return (existingClusterAssignmentsFilename, existingKeysFilename)
  return existingClusterAssignmentsFilename


# -----------------------------------------------------------------------------
def getDescriptiveKeys(url, descriptiveKeyIdentifiers, sourceName, targetType, configEntry, targetGraph, auth, descriptiveKeysComponentsFilename, descriptiveKeysFilename, descriptiveKeysQueryFilename, entityIDColumnName, descriptiveKeyColumnName, queryLogDir=None):

  # If an optional query log directory is given, first check if it actually exists
  if queryLogDir:
    if not os.path.isdir(queryLogDir):
      print(f'Given optional query log directory does not exist, please provide a valid directory')
      exit(1)


  namedGraph = configEntry['namedGraph']
  creationSourceType = configEntry['sourceType'] if 'sourceType' in configEntry else ''

  # generate the query string
  descriptiveKeysQueryString = generateDescriptiveKeysQuery(namedGraph, targetGraph, configEntry['sourceType'], descriptiveKeyIdentifiers)

  # Optionally serialize SPARQL query
  if queryLogDir:
    logSPARQLQuery(queryLogDir, descriptiveKeysQueryString, descriptiveKeysQueryFilename)

  # Execute SPARQL query and save resulting descriptive keys to file
  with open(descriptiveKeysComponentsFilename, 'w', encoding='utf-8') as descriptiveKeyFile:
    utils_sparql.query(url, descriptiveKeysQueryString, descriptiveKeyFile, auth=auth)

  # Create descriptive key strings from the seperate columns
  # The SPARQL query could immediately CONCAT, but this goes hard on performance
  with open(descriptiveKeysComponentsFilename, 'r') as descriptiveKeysComponentsFile, \
       open(descriptiveKeysFilename, 'w') as descriptiveKeyFile:

    inputReader = csv.DictReader(descriptiveKeysComponentsFile)
    descriptiveKeysWriter = csv.DictWriter(descriptiveKeyFile, fieldnames=[entityIDColumnName, descriptiveKeyColumnName])
    descriptiveKeysWriter.writeheader()
    for row in inputReader:
      entityID = '/'.join([sourceName, row['entityID']]) if sourceName != '' else row['entityID']
      descriptiveKeysWriter.writerow({entityIDColumnName: entityID, descriptiveKeyColumnName: '/'.join([row['identifierName'], row['identifierValue']])})

# -----------------------------------------------------------------------------
def generateDescriptiveKeysQuery(sourceGraph, targetGraph, entityClass, identifiersToAdd):
  """This function uses the imported query generation module to generate a SPARQL query fetching descriptive keys."""

  qb = IdentifiersDescriptiveKeysQuery(sourceGraph=sourceGraph, targetGraph=targetGraph,
                                identifiersToAdd=identifiersToAdd, entitySourceClass=entityClass)
                                

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
                                originalsGraph=originalsGraph, identifiersToAdd=identifiersToAdd, correlationListFilter=True)
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
    return ('', identifierName)

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
def uploadData():
  pass

# -----------------------------------------------------------------------------
def logSPARQLQuery(queryLogDir, queryString, queryFilename):

  try:
    with open(os.path.join(queryLogDir, queryFilename), 'w') as queryOut:
      queryOut.write(queryString)
  except Exception as e:
    print(f'Warning: the query log "{queryFilename}" could not be created in the folder {queryLogDir}')
    print(e)

# -----------------------------------------------------------------------------
def checkArguments():

  parser = ArgumentParser("This script integrates the data specified in the config via the OCLC work set clustering algorithm")
  parser.add_argument('-u', '--url', action='store', required=True, help='The URL of the SPARQL endpoint which is queried')
  parser.add_argument('--query-type', required=True, action='store',
                    help='Whether manifestations or contributors are updated (both require different types of queries)')
  parser.add_argument('--target-graph', required=True, action='store',
                    help='The name of the graph to which data is added from a source graph')
  parser.add_argument('--config', required=True, action='store',
                    help='A JSON file containing a data integration configuration specifying among others which identifiers to use')
  parser.add_argument('--query-log-dir', required=False, action='store',
                    help='The optional name of a directory in which generated SPARQL queries will be stored')
  options = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( options.query_type != 'manifestations' and options.query_type != 'contributors'):
    print(f'Type of queries can only be "manifestations" or "contributors", but you gave "{options.query_type}"')
    exit(1)

  if not os.path.isfile(options.config):
    print(f'The given config "{options.config} is not a file"')
    exit(1)

  return options



if __name__ == '__main__':
  options= checkArguments()
  main(options.url, options.query_type, options.target_graph,
       options.config, options.query_log_dir)
