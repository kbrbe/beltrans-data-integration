#
# (c) 2022 Sven Lieber
# KBR Brussels
#
from tools.sparql.query_builder import DuplicateIdentifierQuery
from tools.sparql import utils_sparql
from dotenv import load_dotenv
import os

#
# This scripts generates and executes SPARQL queries to identify data quality issues int4-int9
#

query_folder = 'detectors'
output_folder = 'data'

queries = [
    {'identifierName': 'ISNI',
     'contributorNamedGraph': 'http://beltrans-contributors',
     'manifestationNamedGraph': 'http://beltrans-manifestations',
     'entityType': 'schema:Person',
     'filename': 'int4-duplicate-isni.sparql',
     'dataFilename': 'int4-duplicate-isni.csv'},
    {'identifierName': 'VIAF',
     'contributorNamedGraph': 'http://beltrans-contributors',
     'manifestationNamedGraph': 'http://beltrans-manifestations',
     'entityType': 'schema:Person',
     'filename': 'int5-duplicate-viaf.sparql',
     'dataFilename': 'int5-duplicate-viaf.csv'},
    {'identifierName': 'Wikidata',
     'contributorNamedGraph': 'http://beltrans-contributors',
     'manifestationNamedGraph': 'http://beltrans-manifestations',
     'entityType': 'schema:Person',
     'filename': 'int6-duplicate-wikidata.sparql',
     'dataFilename': 'int6-duplicate-wikidata.csv'},
    {'identifierName': 'KBR',
     'contributorNamedGraph': 'http://beltrans-contributors',
     'manifestationNamedGraph': 'http://beltrans-manifestations',
     'entityType': 'schema:Person',
     'filename': 'int7-duplicate-kbr.sparql',
     'dataFilename': 'int7-duplicate-kbr.csv'},
    {'identifierName': 'BnF',
     'contributorNamedGraph': 'http://beltrans-contributors',
     'manifestationNamedGraph': 'http://beltrans-manifestations',
     'entityType': 'schema:Person',
     'filename': 'int8-duplicate-bnf.sparql',
     'dataFilename': 'int8-duplicate-bnf.csv'},
    {'identifierName': 'NTA',
     'contributorNamedGraph': 'http://beltrans-contributors',
     'manifestationNamedGraph': 'http://beltrans-manifestations',
     'entityType': 'schema:Person',
     'filename': 'int9-duplicate-nta.sparql',
     'dataFilename': 'int9-duplicate-nta.csv'},
    {'identifierName': 'KBR',
     'contributorNamedGraph': 'http://beltrans-manifestations',
     'manifestationNamedGraph': 'http://beltrans-manifestations',
     'entityType': 'schema:CreativeWork',
     'filename': 'int10-duplicate-manif-kbr.sparql',
     'dataFilename': 'int7-duplicate-manif-kbr.csv'},
    {'identifierName': 'BnF',
     'contributorNamedGraph': 'http://beltrans-manifestations',
     'manifestationNamedGraph': 'http://beltrans-manifestations',
     'entityType': 'schema:CreativeWork',
     'filename': 'int11-duplicate-manif-bnf.sparql',
     'dataFilename': 'int8-duplicate-manif-bnf.csv'},
    {'identifierName': 'KB',
     'contributorNamedGraph': 'http://beltrans-manifestations',
     'manifestationNamedGraph': 'http://beltrans-manifestations',
     'entityType': 'schema:CreativeWork',
     'filename': 'int12-duplicate-manif-kb.sparql',
     'dataFilename': 'int9-duplicate-manif-nta.csv'}

]

load_dotenv()
userEnvVar="ENV_SPARQL_ENDPOINT_USER"
passwordEnvVar="ENV_SPARQL_ENDPOINT_PASSWORD"
user = os.getenv(userEnvVar)
password = os.getenv(passwordEnvVar)

auth=None
if(user == None or password == None):
  print(f'No SPARQL endpoint user or password specified using environment variable "{userEnvVar}" and "{passwordEnvVar}"')
  exit(1)
else:
  auth=(user,password)


for query in queries:

    builder = DuplicateIdentifierQuery(
      contributorNamedGraph=query['contributorNamedGraph'],
      manifestationNamedGraph=query['manifestationNamedGraph'],
      entityType=query['entityType'],
      identifierName=query['identifierName']
    )

    file_path = os.path.join(query_folder, query['filename'])
    with open(file_path, 'w') as fOut:
        fOut.write(builder.getQueryString())

    print(f'Successfully created {query["identifierName"]} query at {file_path}')
    print(f'Querying data ...')
    data_file_path = os.path.join(output_folder, query['dataFilename'])

    utils_sparql.sparqlSelect('http://beltrans2.kbr.be/sparql/namespace/integration/sparql', file_path, data_file_path, 'text/csv', auth)
    
