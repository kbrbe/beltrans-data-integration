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
    
# ------------------------------------------------------------
def getNumberOfBelgiansLOCURI(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    for the number of Belgian authors, i.e. instances of schema:Person
    with schema:nationality <http://id.loc.gov/vocabulary/countries/be>"""
    result = _queryJSON(sparqlObject, os.path.join(dsDir, 'get-belgians-LOC-URI.sparql'))
    return _convertCount(result)

# ------------------------------------------------------------
def getNumberOfPersonsWithISNI(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    for the number of schema:Person instances having an ISNI identifier"""
    result = _queryJSON(sparqlObject, os.path.join(dsDir, 'get-persons-with-isni.sparql'))
    return _convertCount(result)

# ------------------------------------------------------------
def getNumberOfBelgiansWithISNI(sparqlObject):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    for the number of schema:Person instances with nationality Belgian having an ISNI identifier"""
    result = _queryJSON(sparqlObject, os.path.join(dsDir, 'get-belgians-with-isni.sparql'))
    return _convertCount(result)

# ------------------------------------------------------------
def getNumberOfPersonsWithIdentifier(sparqlObject, identifierName):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    for the number of schema:Person instances having an identifier with the given name."""
    result = _queryJSON(sparqlObject, os.path.join(dsDir, 'get-persons-with-custom-identifier.sparql'), {'identifierName': identifierName})
    return _convertCount(result)

# ------------------------------------------------------------
def getNumberOfBelgiansWithIdentifier(sparqlObject, identifierName):
    """Query the given SPARQL endpoint (SPARQLWrapper object)
    for the number of schema:Person instances with nationality Belgian having an identifier with the given name."""
    result = _queryJSON(sparqlObject, os.path.join(dsDir, 'get-belgians-with-custom-identifier.sparql'), {'identifierName': identifierName})
    return _convertCount(result)

