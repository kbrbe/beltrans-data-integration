import os
import csv
import argparse
from tools.string import utils_string
from tools import utils

# -----------------------------------------------------------------------------
def main(manualCorrectionsFile, outputFile, dry_run):

  #
  # This configuration specifies the mapping between columns in the input data
  # and internal workings, e.g. which function to execute for which action
  #
  config = {
    'columns': {
      'actionColumn': 'To do',
      'identifierColumn': 'Targetidentifier',
      'fieldColumn': 'Field',
      'currentValueColumn': 'Wrong or blank value',
      'newValueColumn': 'Correct value',
      'namedGraphColumn': 'Named Graph',
      'labelColumn': 'Label',
      'commentColumn': 'Comment'
    },
    'actionMapping': {
      'add info to record': addInfo,
      'remove info from record': removeInfo,
      'remove record (duplicate)': removeRecord,
      'remove record (periodical)': removeRecord,
      'replace info in record': replaceInfo
    },
    'valueSplitCharacter': ';',
    'queryCounterColumnName': 'query counter',
    'queryColumnName': 'query',
    'dryRun': dry_run
  }

  with open(manualCorrectionsFile, 'r', encoding='utf-8-sig') as inputCSV,\
       open(outputFile, 'w') as outputCSV:

    # The output CSV file should contain all input columns + two query-related columns
    outputColumns = list(config['columns'].values()) + ['query counter', 'query']

    inputReader = csv.DictReader(inputCSV)
    outputWriter = csv.DictWriter(outputCSV,fieldnames=outputColumns)

    outputWriter.writeheader()

    for row in inputReader:

      action = row[config['columns']['actionColumn']].lower().strip()
      field = row[config['columns']['fieldColumn']]
      if action in config['actionMapping']:
        # call the function that is defined in the action mapping
        queries = config['actionMapping'][action](row, config)

        outputRow = row
        if queries:
          # loop over all generated queries returned by the action
          # and create one output row for each query
          for counter, query in enumerate(queries):
            queryCounterString = f'{counter+1}/{len(queries)}'
            outputRow.update({
              config['queryCounterColumnName']: queryCounterString,
              config['queryColumnName']: query
            })
            outputWriter.writerow(outputRow)
        else:
          # if not query was returned the action likely is not implemented yet
          outputRow.update({
            config['queryCounterColumnName']: '0',
            config['queryColumnName']: 'to do'
          })
          outputWriter.writerow(outputRow)

      else:
        print(f'Unknown action "{action}", it should be one of: {config["actionMapping"].keys()}')


# -----------------------------------------------------------------------------
def removeInfo(row, config):
  return None

def removeRecord(row, config):
  return None

# -----------------------------------------------------------------------------
def replaceInfo(row, config):

  sc = config['valueSplitCharacter']
  identifier = row[config['columns']['identifierColumn']]
  field = row[config['columns']['fieldColumn']].lower()
  label = row[config['columns']['labelColumn']]
  wrongValueCol = config['columns']['currentValueColumn']
  newValueRaw = row[config['columns']['newValueColumn']]
  namedGraph = row[config['columns']['namedGraphColumn']]
  queries = []

  # we might have a single value or multiple
  # use a list in any case such that the following loop always applies
  newValues = newValueRaw.split(sc) if sc in newValueRaw else [newValueRaw]

  for newValue in newValues:
   

    if field == 'workclusteridentifier':

      query = QUERY_REPLACE_CLUSTER.format(
        graph=namedGraph,
        manifestationGraph='http://beltrans-manifestations', # HARD CODED
        target_identifier=identifier,
        new_cluster_uri=buildClusterURI(newValue)
      )

      # we only have one query for workclusteridentifier
      queries.append(query)

    elif field.startswith('targetisbn'):
      # seperate ISBN branch, because for ISBN we have direct properties and additionally a bf:identifiedBy construct

      queryProperty = QUERY_REPLACE_ISBN_PROPERTY.format(
        graph=namedGraph,
        target_identifier=identifier,
        singleProperty=label,
        isbnToDelete=row[wrongValueCol],
        newISBN=newValue 
      )

      queryBibframe = QUERY_REPLACE_ISBN_BIBFRAME.format(
        graph=namedGraph,
        target_identifier=identifier,
        ISBNLabel='ISBN-10' if field.endswith('10') else 'ISBN-13',
        isbnToDelete=row[wrongValueCol],
        newISBN=newValue
      )

      queries.extend([queryProperty, queryBibframe])

    elif field == 'sourcekbridentifier':

        # add identifier according to BIBFRAME and additionally sameAs link
        queryAddIdentifier = QUERY_ADD_DATA_SOURCE_IDENTIFIER.format(
          graph=namedGraph,
          target_identifier= 'original_' + identifier,
          identifier_uri=buildIdentifierURI(newValue, label),
          identified_resource=buildIdentifiedResourceURI(newValue, label),
          label=label,
          value=row[wrongValueCol]
        ) 

        queryDeleteIdentifier = QUERY_REMOVE_DATA_SOURCE_IDENTIFIER.format(
          graph=namedGraph,
          target_identifier=identifier,
          identifier_uri=buildIdentifierURI(newValue, label),
          label=label,
          value=row[wrongValueCol]
        )
        queryDeleteSameAs = QUERY_REMOVE_DATA_SOURCE_SAMEAS.format(
          graph=namedGraph,
          target_identifier= identifier,
          identified_resource=buildIdentifiedResourceURI(newValue, label),
        )

        queries.extend([queryDeleteIdentifier, queryDeleteSameAs, queryAddIdentifier])


    elif field == 'targetthesaurusbb':
      query = QUERY_REPLACE_GENRE.format(
        graph=namedGraph,
        target_identifier=identifier,
        oldGenreURI=buildGenreURI(row[wrongValueCol]),
        newGenreURI=buildGenreURI(newValue)
      )

      queries.append(query)

    elif field == 'sourcelanguage':
      # seperate branch, because we have an annotation for the original and a direct property from the translation
      queryReplaceSource = QUERY_REPLACE_PROPERTY.format(
        graph=namedGraph,
        target_identifier=identifier,
        property='schema:inLanguage',
        objectToDelete=buildLanguageURI(row[wrongValueCol]),
        newObject=buildLanguageURI(newValue)
      )

      # hard coded target graph and property
      queryReplaceTarget = QUERY_REPLACE_PROPERTY.format(
        graph='http://beltrans-manifestations',
        target_identifier=identifier,
        property='btm:sourceLanguage',
        objectToDelete=buildLanguageURI(row[wrongValueCol]),
        newObject=buildLanguageURI(newValue)
      )

      queries = [queryReplaceSource, queryReplaceTarget]

    elif namedGraph == 'http://beltrans-originals':
      pass
    elif field in ('targettitle', 'author-scenarist'):
      pass
    else:
      print(f'No instructions how to handle replaceInfo for field "{field}" ... skipping {identifier} (named graph was "{namedGraph}")')

  return queries

# -----------------------------------------------------------------------------
def addInfo(row, config):
  
  sc = config['valueSplitCharacter']
  newValueRaw = row[config['columns']['newValueColumn']]
  identifier = row[config['columns']['identifierColumn']]
  field = row[config['columns']['fieldColumn']].lower()
  label=row[config['columns']['labelColumn']]

  # we might have a single value or multiple
  # use a list in any case such that the following loop always applies
  newValues = newValueRaw.split(sc) if sc in newValueRaw else [newValueRaw]

  for newValue in newValues:
    queries = []
  
    # TO DO: do we need a separation of the cases target and source identifier?

    # add an identifier with our BIBFRAME ontology pattern (bf:identifiedBy ... bf:Identifier)
    # as well as with schema:sameAs links
    if field.startswith('target') and field.endswith('identifier'):

      # This is addInfo, thus we do no delete existing identifiers
      #queryDeleteIdentifier = QUERY_REMOVE_DATA_SOURCE_IDENTIFIER.format(
      #  graph=row[config['columns']['namedGraphColumn']],
      #  target_identifier= row[config['columns']['identifierColumn']],
      #  identifier_uri=buildIdentifierURI(newValue, label),
      #  label=label,
      #  value=newValue
      #)
      #queryDeleteSameAs = QUERY_REMOVE_DATA_SOURCE_SAMEAS.format(
      #  graph=row[config['columns']['namedGraphColumn']],
      #  target_identifier= row[config['columns']['identifierColumn']],
      #  identified_resource=buildIdentifiedResourceURI(newValue, label),
      #)

      # including sameAs link
      query = QUERY_ADD_DATA_SOURCE_IDENTIFIER.format(
        graph=row[config['columns']['namedGraphColumn']],
        target_identifier= identifier,
        identifier_uri=buildIdentifierURI(newValue, label),
        identified_resource=buildIdentifiedResourceURI(newValue, label),
        label=label,
        value=newValue
      )

      #queries = [query, queryDeleteIdentifier, queryDeleteSameAs]
      queries.append(query)
   
    # add a link from the linked BELTRANS original to a KBR original
    elif field == 'sourcekbridentifier':

      # including sameAs link
      query = QUERY_ADD_DATA_SOURCE_IDENTIFIER.format(
        graph=row[config['columns']['namedGraphColumn']],
        target_identifier= 'original_' + identifier,
        identifier_uri=buildIdentifierURI(newValue, label),
        identified_resource=buildIdentifiedResourceURI(newValue, label),
        label=label,
        value=newValue
      ) 

      queries.append(query)

    # add links to an authority
    elif field == 'translator-adapter':

      query = QUERY_ADD_CONTRIBUTOR_LINK.format(
        graph=row[config['columns']['namedGraphColumn']],
        direct_schema_relationship="http://schema.org/translator",
        direct_marc_relationship="http://id.loc.gov/vocabulary/relators/trl",
        target_identifier=identifier,
        contributor_uri=f'http://kbr.be/id/data/{newValue}'
      )

      queries.append(query)
    else:
      print(f'No instructions how to process field  "{field}" ...')

    return queries

# -----------------------------------------------------------------------------
def buildIdentifierURI(identifier, label):
  return f'http://kbr.be/id/data/identifier_{label}_{identifier}'

# -----------------------------------------------------------------------------
def buildClusterURI(identifier):
  return f'http://kbr.be/id/data/cluster_{identifier}'

# -----------------------------------------------------------------------------
def buildGenreURI(identifier):
  return f'http://kbr.be/id/data/{identifier}'

# -----------------------------------------------------------------------------
def buildLanguageURI(identifier):
  return f'http://id.loc.gov/vocabulary/languages/{identifier}'




# -----------------------------------------------------------------------------
def buildIdentifiedResourceURI(identifier, label):
  defaultURI = f'http://example.com/{identifier}'
  if label == 'KBR':
    return f'http://kbr.be/id/data/manifestation_{identifier}'
  elif label == 'BnF':
    return f'https://data.bnf.fr/fr/ark:/12148/{identifier}#about'
  elif label == 'KB':
    return f'http://data.bibliotheken.nl/id/nbt/{identifier}'
  elif label == 'Unesco':
    return f'http://kbr.be/id/data/manifestation_unesco{identifier}'
  elif label == '':
    print(f'ERROR: No instructions how to process empty data source, will generate "{defaultURI}"')
    return defaultURI
  else:
    print(f'ERROR: No instructions how to process data source "{label}", will generate "{defaultURI}"')
    return defaultURI


# -----------------------------------------------------------------------------
QUERY_ADD_CONTRIBUTOR_LINK = """PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX bf: <http://id.loc.gov/ontologies/bibframe/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>

INSERT {{
  GRAPH <{graph}> {{
    ?book <{direct_schema_relationship}> <{contributor_uri}> ;
          <{direct_marc_relationship}> <{contributor_uri}> .
  }}
}}
WHERE {{
  GRAPH <{graph}> {{
    ?book dcterms:identifier "{target_identifier}" .
  }}
}}

"""

# -----------------------------------------------------------------------------
QUERY_REPLACE_CLUSTER = """PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX bf: <http://id.loc.gov/ontologies/bibframe/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX fabio: <http://purl.org/spar/fabio/>

DELETE {{
  GRAPH <{graph}> {{
    ?oldClusterURI fabio:manifestationOf ?book .
  }}
}}
INSERT {{
  GRAPH <{graph}> {{
    <{new_cluster_uri}> fabio:manifestationOf ?book .
  }}
}}
WHERE {{
  GRAPH <{graph}> {{
    ?oldClusterURI fabio:manifestationOf ?book .
  }}
  GRAPH <{manifestationGraph}> {{
    ?book dcterms:identifier "{target_identifier}" .
  }}
}}

"""

# -----------------------------------------------------------------------------
QUERY_REPLACE_ISBN_PROPERTY = """PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX bf: <http://id.loc.gov/ontologies/bibframe/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX fabio: <http://purl.org/spar/fabio/>

DELETE {{
  GRAPH <{graph}> {{
    ?book {singleProperty} {isbnToDelete} .
  }}
}}
INSERT {{
  GRAPH <{graph}> {{
    ?book {singleProperty} "{newISBN}" .
  }}
}}
WHERE {{
  GRAPH <{graph}> {{
    ?book dcterms:identifier "{target_identifier}" .
  }}
}}

"""

# -----------------------------------------------------------------------------
QUERY_REPLACE_ISBN_BIBFRAME = """PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX bf: <http://id.loc.gov/ontologies/bibframe/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX fabio: <http://purl.org/spar/fabio/>

DELETE {{
  GRAPH <{graph}> {{
    ?isbnEntity rdf:value {isbnToDelete} .
  }}
}}
INSERT {{
  GRAPH <{graph}> {{
    ?isbnEntity rdf:value "{newISBN}" . 
  }}
}}
WHERE {{
  GRAPH <{graph}> {{
    ?book dcterms:identifier "{target_identifier}" ;
          bf:identifiedBy ?isbnEntity .

    ?isbnEntity rdf:label "{ISBNLabel}" .
  }}
}}

"""

# -----------------------------------------------------------------------------
QUERY_REPLACE_PROPERTY = """PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX bf: <http://id.loc.gov/ontologies/bibframe/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX fabio: <http://purl.org/spar/fabio/>

DELETE {{
  GRAPH <{graph}> {{
    ?book {property} {objectToDelete} .
  }}
}}
INSERT {{
  GRAPH <{graph}> {{
    ?book {property} "{newObject}" .
  }}
}}
WHERE {{
  GRAPH <{graph}> {{
    ?book dcterms:identifier "{target_identifier}" .
  }}
}}

"""



# -----------------------------------------------------------------------------
QUERY_REPLACE_GENRE = """PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX bf: <http://id.loc.gov/ontologies/bibframe/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX fabio: <http://purl.org/spar/fabio/>

DELETE {{
  GRAPH <{graph}> {{
    ?book schema:about <{oldGenreURI}> .
  }}
}}
INSERT {{
  GRAPH <{graph}> {{
    ?book schema:about <{newGenreURI}> .
  }}
}}
WHERE {{
  GRAPH <{graph}> {{
    ?book dcterms:identifier "{target_identifier}" .
  }}

}}

"""




# -----------------------------------------------------------------------------
QUERY_ADD_DATA_SOURCE_IDENTIFIER = """PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX bf: <http://id.loc.gov/ontologies/bibframe/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>

INSERT {{
  GRAPH <{graph}> {{
    ?book bf:identifiedBy <{identifier_uri}> ;
          schema:sameAs <{identified_resource}> .

    <{identifier_uri}> a bf:Identifier ;
        rdfs:label "{label}" ;
        rdf:value "{value}" .
  }}
}}
WHERE {{
  GRAPH <{graph}> {{
    ?book dcterms:identifier "{target_identifier}" .
  }}
}}

"""

# -----------------------------------------------------------------------------
QUERY_REMOVE_DATA_SOURCE_IDENTIFIER = """PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX bf: <http://id.loc.gov/ontologies/bibframe/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>

DELETE {{
  GRAPH <{graph}> {{
    ?book bf:identifiedBy ?toBeDeletedEntity .

    ?toBeDeletedEntity a bf:Identifier ;
        rdfs:label "{label}" ;
        rdf:value "{value}" .
  }}
}}
WHERE {{
  GRAPH <{graph}> {{
    ?book dcterms:identifier "{target_identifier}" .
  }}
}}
"""

# -----------------------------------------------------------------------------
QUERY_REMOVE_DATA_SOURCE_SAMEAS = """PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX bf: <http://id.loc.gov/ontologies/bibframe/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>

DELETE {{
  GRAPH <{graph}> {{
    ?book schema:sameAs <{identified_resource}> .
  }}
}}
WHERE {{
  GRAPH <{graph}> {{
    ?book dcterms:identifier "{target_identifier}" .
  }}
}}
"""





# -----------------------------------------------------------------------------
def parseArguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('manualCorrectionsFile', help='A CSV file with the final corrections')
  parser.add_argument('-d', '--dry-run', action='store_true', help='If set, no SPARQL queries are executed')
  parser.add_argument('-o', '--output-csv', action='store', required=True, help='The output CSV file, enriched with SPARQL queries')
  options = parser.parse_args()
  return options

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  args = parseArguments()
  main(args.manualCorrectionsFile, args.output_csv, args.dry_run)
