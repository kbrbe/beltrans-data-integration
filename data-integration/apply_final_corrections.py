import os
import csv
import argparse
from tools.string import utils_string
from tools import utils

# -----------------------------------------------------------------------------
def main(manualCorrectionsFile, outputFile, dry_run):

  config = {
    'columns': {
      'actionColumn': 'To do',
      'identifierColumn': 'Targetidentifier',
      'fieldColumn': 'Field',
      'currentValueColumn': 'Wrong or blank value',
      'newValueColumn': 'Correct value',
      'namedGraphColumn': 'Named Graph',
      'labelColumn': 'Label'
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

  with open(manualCorrectionsFile, 'r') as inputCSV,\
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
          for counter, query in enumerate(queries):
            queryCounterString = f'{counter+1}/{len(queries)}'
            outputRow.update({
              config['queryCounterColumnName']: queryCounterString,
              config['queryColumnName']: query
            })
            outputWriter.writerow(outputRow)
        else:
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
def replaceInfo(row, config):
  return None
# -----------------------------------------------------------------------------
def addInfo(row, config):
  
  sc = config['valueSplitCharacter']
  newValueRaw = row[config['columns']['newValueColumn']]
  field = row[config['columns']['fieldColumn']].lower()

  # we might have a single value or multiple
  # use a list in any case such that the following loop always applies
  newValues = newValueRaw.split(sc) if sc in newValueRaw else [newValueRaw]

  for newValue in newValues:
    queries = []
    label=row[config['columns']['labelColumn']]
  
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
        target_identifier= row[config['columns']['identifierColumn']],
        identifier_uri=buildIdentifierURI(newValue, label),
        identified_resource=buildIdentifiedResourceURI(newValue, label),
        label=label,
        value=newValue
      )



      #queries = [query, queryDeleteIdentifier, queryDeleteSameAs]
      queries = [query]
   
    # add a link from the linked BELTRANS original to a KBR original
    elif field == 'sourcekbridentifier':

      # including sameAs link
      query = QUERY_ADD_DATA_SOURCE_IDENTIFIER.format(
        graph=row[config['columns']['namedGraphColumn']],
        target_identifier= 'original_' + row[config['columns']['identifierColumn']],
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
        target_identifier=row[config['columns']['identifierColumn']],
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
def buildIdentifiedResourceURI(identifier, label):
  if label == 'KBR':
    return f'http://kbr.be/id/data/manifestation_{identifier}'
  elif label == 'BnF':
    return f'https://data.bnf.fr/fr/ark:/12148/{identifier}#about'
  elif label == 'KB':
    return f'http://data.bibliotheken.nl/id/nbt/{identifier}'
  elif label == 'Unesco':
    return f'http://kbr.be/id/data/manifestation_unesco{identifier}'
  else:
    print(f'ERROR: No instructions how to process data source "{label}"')
    return f'http://example.com/{identifier}'


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
