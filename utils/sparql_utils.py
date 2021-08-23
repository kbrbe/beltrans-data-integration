from SPARQLWrapper import SPARQLWrapper, TURTLE, JSON
import os

baseDir = '/home/slieber/repos/beltrans-data'
dsDir = os.path.join(baseDir, 'data-sources')
bnfDir = os.path.join(dsDir, 'bnf/')
kbDir = os.path.join(dsDir, 'kb/')

sparqlServer = "http://wikibase-test-srv01.kbr.be/sparql/"

# ------------------------------------------------------------
def _readSPARQLQuery(filename):
    """Read a SPARQL query from file and return the content as a string."""
    content = ""
    with open(filename, 'r') as reader:
        content = reader.read()
    return content

# ------------------------------------------------------------
def _queryJSON(sparqlObject, sparqlQueryFile):
    """Queries the given SPARQL endpoint (SPARQLWrapper object)
    with the SPARQL query read from the given file and convert output to JSON."""
    sparqlObject.setQuery(_readSPARQLQuery(sparqlQueryFile))
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
def getPropertyOverview(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object) for all properties and their number."""
    result = _queryJSON(sparqlObject, os.path.join(dsDir, 'get-property-overview.sparql'))
    return _convertValueCount(result)

# ------------------------------------------------------------
def getClassOverview(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object) for all classes and number of their instances."""
    result = _queryJSON(sparqlObject, os.path.join(dsDir, 'get-class-overview.sparql'))
    return _convertValueCount(result)

# ------------------------------------------------------------
def getNationalityOverview(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object) for percentages regarding nationality."""
    result = _queryJSON(sparqlObject, os.path.join(dsDir, 'get-nationality-percentages.sparql'))
    return _convertPercentage(result)
    

