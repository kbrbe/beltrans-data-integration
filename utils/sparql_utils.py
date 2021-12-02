from SPARQLWrapper import SPARQLWrapper, TURTLE, JSON

import pandas as pd
from pandas.io.json import json_normalize
import os

baseDir = '/home/slieber/repos/beltrans-data'
queriesDir = os.path.join(baseDir, 'data-integration/sparql-queries')
bnfDir = os.path.join(queriesDir, 'bnf/')
kbDir = os.path.join(queriesDir, 'kb/')

sparqlServer = "http://wikibase-test-srv01.kbr.be/sparql/"
namedGraphKBRTranslations = "http://kbr-syracuse"

# ------------------------------------------------------------
def _readSPARQLQuery(filename):
    """Read a SPARQL query from file and return the content as a string."""
    content = ""
    with open(filename, 'r') as reader:
        content = reader.read()
    return content

# ------------------------------------------------------------
def _queryJSON(sparqlObject, sparqlQueryFile, variables={}):
    """Queries the given SPARQL endpoint (SPARQLWrapper object)
    with the SPARQL query read from the given file and convert output to JSON. Dollar variables can be replaced based on the provided parameter"""
    queryString = _readSPARQLQuery(sparqlQueryFile) 

    if variables:
      for v in variables:
        queryString = queryString.replace('$'+ v, variables[v])
    sparqlObject.setQuery(queryString)
    sparqlObject.setReturnFormat(JSON)
    return sparqlObject.queryAndConvert()

# ------------------------------------------------------------
def _convertResultsToArray(result, varNameList):
    """Extracts for each SPARQL result binding in 'result' the 'value' of variables specified in 'varNameList'
    and creates an Array of these result values."""
    resultArray = list()
    for r in result['results']['bindings']:
        resultList = list()
        for v in varNameList:
            resultList.append(r[v]['value'])
        resultArray.append(resultList)
    return resultArray

# ------------------------------------------------------------
def _convertValueCount(result):
    """Converts SPARQL result bindings of a '?value ?count' query to a common format."""
    return _convertResultsToArray(result, ['count', 'value'])

# ------------------------------------------------------------
def _convertPercentage(result):
    """Convertes SPARQL result bindings of a '?value ?percentage' query to a common format."""
    return _convertResultsToArray(result, ['value', 'number', 'percentage'])

# ------------------------------------------------------------
def _convertCount(result):
    """Converts SPARQL result bindings of a '?count' query to integer."""
    return int(_convertResultsToArray(result, ['count'])[0][0])

# ------------------------------------------------------------
def getPropertyOverview(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object) for all properties and their number."""
    result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-property-overview.sparql'))
    return _convertValueCount(result)

# ------------------------------------------------------------
def getClassOverview(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object) for all classes and number of their instances."""
    result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-class-overview.sparql'))
    return _convertValueCount(result)

# ------------------------------------------------------------
def getNationalityOverview(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object) for percentages regarding nationality."""
    result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-nationality-percentages.sparql'))
    return _convertPercentage(result)
    
# ------------------------------------------------------------
def getNumberOfBelgiansLOCURI(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    for the number of Belgian authors, i.e. instances of schema:Person
    with schema:nationality <http://id.loc.gov/vocabulary/countries/be>"""
    result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-belgians-LOC-URI.sparql'))
    return _convertCount(result)

# ------------------------------------------------------------
def getNumberOfPersonsWithISNI(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    for the number of schema:Person instances having an ISNI identifier"""
    result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-persons-with-isni.sparql'))
    return _convertCount(result)

# ------------------------------------------------------------
def getNumberOfBelgiansWithISNI(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    for the number of schema:Person instances with nationality Belgian having an ISNI identifier"""
    result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-belgians-with-isni.sparql'))
    return _convertCount(result)

# ------------------------------------------------------------
def getNumberOfPersonsWithIdentifier(sparqlObject, identifierName):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    for the number of schema:Person instances having an identifier with the given name."""
    result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-persons-with-custom-identifier.sparql'), {'identifierName': identifierName})
    return _convertCount(result)

# ------------------------------------------------------------
def getNumberOfBelgiansWithIdentifier(sparqlObject, identifierName):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    for the number of schema:Person instances with nationality Belgian having an identifier with the given name."""
    result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-belgians-with-custom-identifier.sparql'), {'identifierName': identifierName})
    return _convertCount(result)

# ------------------------------------------------------------
def getQueryResultsAsDataframe(sparqlObject, queryFile):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    with the query in the given file and return the result as pandas dataframe."""
    result = _queryJSON(sparqlObject, queryFile)
    return json_normalize(result['results']['bindings'])

# ------------------------------------------------------------
def getWikidataBelgiansIdentifiers(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    for instances of schema:Person with optional KB, BnF and ISNI identifiers."""
    results = getQueryResultsAsDataframe(sparqlObject, os.path.join(queriesDir, 'get-identifier-integration-data.sparql'))
    results = results[['wdKbrID.value', 'wdKbID.value', 'wdBnfID.value', 'wdISNI.value']]
    return results.rename(columns = lambda col: col.replace(".value", ""))

# ------------------------------------------------------------
def getKBIdentifiers(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    for instances of schema:Person to obtain VIAF and ISNI identifiers and schema:WebPage to obtain KB identifiers."""
    results = getQueryResultsAsDataframe(sparqlObject, os.path.join(queriesDir, 'get-kb-identifiers.sparql'))
    results = results[['kbKbrID.value', 'kbViafID.value', 'kbIsniID.value']]
    return results.rename(columns = lambda col: col.replace(".value", ""))

# ------------------------------------------------------------
def _convertPropertyStatResultsToArray(results):
  """This function takes the results of a property query
  in which we have the following variables in the result bindings:
  'countWith', 'total', 'countWithout', and 'percentage'"""
  return _convertResultsToArray(results, ['percentageWith', 'countWith', 'total', 'countWithout'])[0]

# ------------------------------------------------------------
def getISBNStats(sparqlObject):
  """Query the given SPARQL endpoint (SPARQLWrapper object)
  for stats regarding the use of schema:isbn for instances of schema:CreativeWork."""
  result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-translation-property-stats.sparql'), {'namedGraph': namedGraphKBRTranslations, 'property': 'schema:isbn'})
  return _convertPropertyStatResultsToArray(result)

# ------------------------------------------------------------
def getTranslationAuthorStats(sparqlObject):
  """Query the given SPARQL endpoint (SPARQLWrapper object)
  for stats regarding the use of schema:author for instances of schema:CreativeWork."""
  result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-translation-property-stats.sparql'), {'namedGraph': namedGraphKBRTranslations, 'property': 'schema:author'})
  return _convertPropertyStatResultsToArray(result)

# ------------------------------------------------------------
def getTranslatorStats(sparqlObject):
  """Query the given SPARQL endpoint (SPARQLWrapper object)
  for stats regarding the use of schema:translator for instances of schema:CreativeWork."""
  result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-translation-property-stats.sparql'), {'namedGraph': namedGraphKBRTranslations, 'property': 'schema:translator'})
  return _convertPropertyStatResultsToArray(result)

# ------------------------------------------------------------
def getPublisherStats(sparqlObject):
  """Query the given SPARQL endpoint (SPARQLWrapper object)
  for stats regarding the use of schema:publisher for instances of schema:CreativeWork."""
  result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-translation-property-stats.sparql'), {'namedGraph': namedGraphKBRTranslations, 'property': 'schema:publisher'})
  return _convertPropertyStatResultsToArray(result)

# ------------------------------------------------------------
def getIllustratorStats(sparqlObject):
  """Query the given SPARQL endpoint (SPARQLWrapper object)
  for stats regarding the use of prov:Role of an illustrator related to instances of schema:CreativeWork."""
  result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-translation-role-stats.sparql'), {'namedGraph': namedGraphKBRTranslations, 'role': 'btid:role_ill'})
  return _convertPropertyStatResultsToArray(result)

# ------------------------------------------------------------
def getScenaristStats(sparqlObject):
  """Query the given SPARQL endpoint (SPARQLWrapper object)
  for stats regarding the use of prov:Role of an illustrator related to instances of schema:CreativeWork."""
  result = _queryJSON(sparqlObject, os.path.join(queriesDir, 'get-translation-role-stats.sparql'), {'namedGraph': namedGraphKBRTranslations, 'role': 'btid:role_sce'})
  return _convertPropertyStatResultsToArray(result)

# ------------------------------------------------------------
def getPublicationStatsOverview(sparqlObject):
  """This function executes several queries with a similar output format to the given SPARQL endpoint (SPARQLWrapper object)
  and returns a data frame containing the results."""

  queryFunctions = {
    "Translations with ISBN identifiers": getISBNStats,
#    "Translation source information": getTranslationSourceStats, 
    "Translations with specified author": getTranslationAuthorStats,
    "Translations with specified translator": getTranslatorStats, 
    "Translations with specified publisher": getPublisherStats,
    "Specified illustrator": getIllustratorStats,
    "Specified scenarist": getScenaristStats
#    "Contributors without role": getNoRoleStats
  }

  results = list()
  rowIndex = list()
  for (name, fn) in queryFunctions.items():
    results.append(fn(sparqlObject))
    rowIndex.append(name)

  return pd.DataFrame(results, index=rowIndex, columns=['%', 'found', 'total', 'not having it'])
  
