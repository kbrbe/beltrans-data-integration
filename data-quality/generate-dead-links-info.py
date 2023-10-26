#
# (c) 2022 Sven Lieber
# KBR Brussels
#
from tools.sparql.query_builder import DeadLinkQuery
from tools.sparql import utils_sparql
from dotenv import load_dotenv
import os

#
# This scripts generates and executes SPARQL queries to identify data quality issues int4-int9
#

output_folder = '2023-10-26_dead-links'
query_folder = output_folder

queries = [
  {'identifierName': 'KBR',
   'targetGraph': 'http://beltrans-manifestations',
   'sourceGraph': 'http://kbr-syracuse',
   'targetEntityType': 'schema:CreativeWork',
   'sourceEntityType': 'schema:CreativeWork',
   'queryFilename': 'manifestations-kbr.sparql',
   'dataFilename': 'manifestations-kbr.csv'
  },
  {'identifierName': 'BnF',
   'targetGraph': 'http://beltrans-manifestations',
   'sourceGraph': 'http://bnf-publications',
   'targetEntityType': 'schema:CreativeWork',
   'sourceEntityType': 'schema:CreativeWork',
   'queryFilename': 'manifestations-bnf.sparql',
   'dataFilename': 'manifestations-bnf.csv'
  },
  {'identifierName': 'KB',
   'targetGraph': 'http://beltrans-manifestations',
   'sourceGraph': 'http://kb-publications',
   'targetEntityType': 'schema:CreativeWork',
   'sourceEntityType': 'schema:CreativeWork',
   'queryFilename': 'manifestations-kb.sparql',
   'dataFilename': 'manifestations-kb.csv'
  },
  {'identifierName': 'Unesco',
   'targetGraph': 'http://beltrans-manifestations',
   'sourceGraph': 'http://unesco',
   'targetEntityType': 'schema:CreativeWork',
   'sourceEntityType': 'schema:CreativeWork',
   'queryFilename': 'manifestations-unesco.sparql',
   'dataFilename': 'manifestations-unesco.csv'
  },
  {'identifierName': 'KBR',
   'targetGraph': 'http://beltrans-manifestations',
   'sourceGraph': 'http://kbr-linked-authorities',
   'targetEntityType': 'schema:Person',
   'sourceEntityType': 'schema:Person',
   'queryFilename': 'contributors-kbr.sparql',
   'dataFilename': 'contributors-kbr.csv'
  },
  {'identifierName': 'BnF',
   'targetGraph': 'http://beltrans-manifestations',
   'sourceGraph': 'http://bnf-contributors',
   'targetEntityType': 'schema:Person',
   'sourceEntityType': 'foaf:Person',
   'queryFilename': 'contributors-bnf.sparql',
   'dataFilename': 'contributors-bnf.csv'
  },
  {'identifierName': 'KB',
   'targetGraph': 'http://beltrans-manifestations',
   'sourceGraph': 'http://kb-linked-authorities',
   'targetEntityType': 'schema:Person',
   'sourceEntityType': 'schema:Person',
   'queryFilename': 'contributors-kb.sparql',
   'dataFilename': 'contributors-kb.csv'
  },
  {'identifierName': 'Unesco',
   'targetGraph': 'http://beltrans-manifestations',
   'sourceGraph': 'http://unesco-linked-authorities',
   'targetEntityType': 'schema:Person',
   'sourceEntityType': 'schema:Person',
   'queryFilename': 'contributors-unesco.sparql',
   'dataFilename': 'contributors-unesco.csv'
  }
]

load_dotenv('.env')
endpointEnvVar="ENV_SPARQL_ENDPOINT_INTEGRATION"
userEnvVar="ENV_SPARQL_ENDPOINT_USER"
passwordEnvVar="ENV_SPARQL_ENDPOINT_PASSWORD"
endpointURL = os.getenv(endpointEnvVar)
user = os.getenv(userEnvVar)
password = os.getenv(passwordEnvVar)

auth=None
if(user == None or password == None):
  print(f'No SPARQL endpoint user or password specified using environment variable "{userEnvVar}" and "{passwordEnvVar}"')
  exit(1)
else:
  auth=(user,password)

os.makedirs(output_folder, exist_ok=True)

for query in queries:

    builder = DeadLinkQuery(
      sourceGraph=query['sourceGraph'],
      targetGraph=query['targetGraph'],
      entityTargetType=query['targetEntityType'],
      entitySourceType=query['sourceEntityType'],
      identifierName=query['identifierName']
    )

    file_path = os.path.join(query_folder, query['queryFilename'])
    with open(file_path, 'w') as fOut:
        fOut.write(builder.getQueryString())

    print(f'Successfully created {query["identifierName"]} query at {file_path}')
    print(f'Querying data ...')
    data_file_path = os.path.join(output_folder, query['dataFilename'])

    utils_sparql.sparqlSelect(endpointURL, file_path, data_file_path, 'text/csv', auth)
    
    with open(data_file_path, 'r') as dataFile:
      numberOfRows = len(dataFile.readlines())-1
      print(f'{query["identifierName"]} ({query["sourceGraph"]}): {numberOfRows} lines')
