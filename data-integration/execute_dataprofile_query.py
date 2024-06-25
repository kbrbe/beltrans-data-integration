from string import Template
from argparse import ArgumentParser
from dotenv import load_dotenv
from tools.sparql.query_builder import Query
import tools.sparql.utils_sparql as utils_sparql
import shutil
import os
import csv
import json

# -----------------------------------------------------------------------------
def main(url, outputFilename, configFilename, queryLogDir):

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


  config = parseConfig(configFilename)

  # (1) Execute all SPARQL queries
  #
  baseQueryString = buildBaseQuery(config)
  baseQueryFilename = f'base.sparql'
  baseQueryResultFilename = os.path.join(queryLogDir, f'base-result.csv')
  logAndExecuteQuery(url, "base query", baseQueryString, baseQueryFilename, baseQueryResultFilename, queryLogDir, auth=auth)
  for queryName in config['queries']:

    queryFilename = f'{queryName}.sparql'
    queryResultFilename = os.path.join(queryLogDir, f'{queryName}-result.csv')
    queryString = buildQuery(queryName, config)

    logAndExecuteQuery(url, queryName, queryString, queryFilename, queryResultFilename, queryLogDir, auth=auth)

  # (2) merge SPARQL query results
  #
  # When writing per column, we only have to store one queryResult CSV file at a time in main memory, more IO
  # When writing per row, we have to keep the CSV content of all query results in main memory for lookup, less IO
  print(f'Merge query results')
  createCSVPerColumn(outputFilename, baseQueryResultFilename, config, queryLogDir)


def logAndExecuteQuery(url, queryName, queryString, queryFilename, queryResultFilename, queryLogDir, auth=None):

  logSPARQLQuery(queryLogDir, queryString, queryFilename)

  # execute query
  print(f'Execute query {queryName}')
  with open(queryResultFilename, 'w', encoding='utf-8') as queryResultFile:
    utils_sparql.query(url, queryString, queryResultFile, auth=auth)



# -----------------------------------------------------------------------------
def createCSVPerColumn(outputFilename, baseQueryResultFilename, config, queryLogDir): 

  if os.path.exists(outputFilename):
    os.remove(outputFilename)

  shutil.copyfile(baseQueryResultFilename, outputFilename)


  for queryName in config['queries']:
    print(f'\tMerge query {queryName} results:', end=" ")
    queryConfig = config['queries'][queryName]
    queryResultFilename = os.path.join(queryLogDir, f'{queryName}-result.csv')
    subjectVarName = queryConfig['subject'][1:]

    lookup = {}
    with open(queryResultFilename, 'r') as inputFile:
      inputReader = csv.DictReader(inputFile)
      numberValues = 0
      for row in inputReader:
        rowID = row[subjectVarName]
        
        if isinstance(queryConfig['object'], list):
          substituteMapping = {varName[1:]:row[varName[1:]] for varName in queryConfig['object']}
          colValue = Template(queryConfig['objectMerge']).substitute(substituteMapping)
          if rowID in lookup:
            numberValues += 1
            lookup[rowID].append(colValue)
          else:
            numberValues += 1
            lookup[rowID] = [colValue]
        else:
          columnName = queryConfig['object'][1:]
          if rowID in lookup:
            numberValues += 1
            lookup[rowID].append(row[columnName])
          else:
            numberValues += 1
            lookup[rowID] = [row[columnName]]

      print(f'found values: {numberValues} ', end=" ")

    numberAddedValue = 0
    numberAddedEmpty = 0
    outputFilenameTmp = outputFilename + 'TMP'
    with open(outputFilename, 'r') as inputFile, \
         open(outputFilenameTmp, 'w') as outputFile:
      inputReader = csv.DictReader(inputFile)
      outputWriter = csv.DictWriter(outputFile, fieldnames=inputReader.fieldnames + [queryName])
      outputWriter.writeheader()
      for row in inputReader:
        rowID = row[queryConfig['subject'][1:]]
        outputRow = row
        if rowID in lookup:
          numberAddedValue += 1
          outputRow[queryName] = config['valueSeparator'].join(lookup[rowID])
        else:
          numberAddedEmpty += 1
          outputRow[queryName] = ""
        outputWriter.writerow(outputRow)
      print(f'added values: {numberAddedValue}, added empty: {numberAddedEmpty}')
    os.replace(outputFilenameTmp, outputFilename)

# -----------------------------------------------------------------------------
def buildBaseQuery(config):
  pattern = Template("${prefixList} SELECT DISTINCT ${subject} WHERE { ${subjectPattern} }")

  query = pattern.substitute(
    prefixList=Query._getPrefixList(),
    subject=config['primarySubject'],
    subjectPattern=config['subjectPatterns'][config['primarySubject']]
  )

  return query

# -----------------------------------------------------------------------------
def buildQuery(queryName, config):

  queryConfig = config['queries'][queryName]
  queryObjects = queryConfig['object'] if isinstance(queryConfig['object'], list) else [queryConfig['object']]

  pattern = Template("${prefixList} SELECT DISTINCT ${subject} ${objects} WHERE { ${subjectPattern} ${objectPattern} }")

  query = pattern.substitute(
    prefixList=Query._getPrefixList(),
    subject=queryConfig['subject'],
    objects=' '.join(queryObjects),
    subjectPattern=config['subjectPatterns'][queryConfig['subject']],
    objectPattern=queryConfig['pattern']
  )

  return query

# -----------------------------------------------------------------------------
def parseConfig(configFilename):
  config = None
  with open(configFilename, 'r') as configFile:
    config = json.load(configFile)
  return config

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

  parser = ArgumentParser("This script executes SPARQL queries generated based on the config and creates a single CSV output file")
  parser.add_argument('-u', '--url', action='store', required=True, help='The URL of the SPARQL endpoint which is queried')
  parser.add_argument('--output-file', required=True, action='store',
                    help='The name of the CSV output file')
  parser.add_argument('--config', required=True, action='store',
                    help='A JSON file containing the configuration to execute several SPARQL queries and create a single CSV output file')
  parser.add_argument('--query-log-dir', action='store',
                    help='The optional name of a directory in which generated SPARQL queries will be stored')
  options = parser.parse_args()

  return options



if __name__ == '__main__':
  options= checkArguments()
  main(options.url, options.output_file, options.config, options.query_log_dir)
