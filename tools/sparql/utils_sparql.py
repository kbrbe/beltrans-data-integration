import os
import re
import sys
import lxml.etree as ET
import requests
import time
#import rdflib
import pandas as pd
from io import StringIO

# -----------------------------------------------------------------------------
def addTestData(target, loadConfig):
  """This function reads the test data and stores it into several named graphs (one file for one named graph).
  The config looks like the following: 'http://first-named-graph': ['filename1'], 'http://second-named-graph': ['filename2']}

  The data could already be in quad format, but we are more flexible if we can configure which data is stored in which named graph.
  """
  for ng in loadConfig:
    files = loadConfig[ng]
    for filename in files:
      if os.path.isfile(filename):
        with open(filename, 'r') as dataIn:
          if isinstance(target, rdflib.ConjunctiveGraph):
            namedGraphURI = rdflib.URIRef(ng)
            target.get_context(namedGraphURI).parse(filename, format='turtle')
          else:
            addDataToBlazegraph(url=target, namedGraph=ng, filename=filename, fileFormat='text/turtle')

# -----------------------------------------------------------------------------
def loadData(url, loadConfig):
  """This function reads the given config containing the source of RDF data and its type to store it in a SPARQL endpoint at 'url'."""

  for graph in loadConfig:
    filename = loadConfig['graph']
    if os.path.isfile(filename):
      if filename.endswith('.ttl'):
        addDataToBlazegraph(url=url, namedGraph=graph, filename=filename, fileFormat='text/turtle')
      elif filename.endswith('.sparql'):
        addDataToBlazegraph(url=url, namedGraph=graph, filename=filename, fileFormat='application/sparql-update')

# -----------------------------------------------------------------------------
def addDataToBlazegraph(url, filename, fileFormat, namedGraph=None, auth=None):
  print(f'## Add data from {filename} to {namedGraph} of {url}\n')
  with open(filename, 'rb') as fileIn:
    #r = requests.post(url, files={'file': (filename, fileIn, fileFormat)}, headers={'Content-Type': fileFormat}, params={'context-uri': namedGraph})
    if namedGraph:
      r = requests.post(url, data=fileIn.read(), headers={'Content-Type': fileFormat}, params={'context-uri': namedGraph}, auth=auth)
    else:
      r = requests.post(url, data=fileIn.read(), headers={'Content-Type': fileFormat}, auth=auth)
    print(r.headers)
    print(r.content)

# -----------------------------------------------------------------------------
def query(target, queryString, outputWriter, auth=None):
  """This function executes the given SPARQL query against the target and writes the output to outputWriter."""
  res = None
  if isinstance(target, rdflib.ConjunctiveGraph):
    # target is a local rdflib graph
    print(target)
    res = target.query(queryString)
    for row in res:
      print(row)
  else:
    # SPARQLWrapper has issues retrieving CSV from Blazegraph, thus we send the query low level via a request
    res = requests.post(target, data=queryString, headers={'Accept': 'text/csv', 'Content-Type': 'application/sparql-query'}, auth=auth)
    res.raise_for_status()
    outputWriter.write(res.content.decode('utf-8'))

# ------------------------------------------------------------
def queryToDataframe(target, queryFilename, indexCol):
  # using get such that we do not have to authenticate
  #res = requests.get(target, data=queryString, headers={'Accept': 'text/csv', 'Content-Type': 'application/sparql-query'})
  res = sparqlSelectToString(target, queryFilename, "text/csv", httpMethod='get')
  csvWrapper = StringIO(res)
  return pd.read_csv(csvWrapper, index_col=indexCol)

# ------------------------------------------------------------
def readSPARQLQuery(filename):
    """Read a SPARQL query from file and return the content as a string."""
    content = ""
    with open(filename, 'r') as reader:
        content = reader.read()
    return content


# -----------------------------------------------------------------------------
def deleteNamedGraph(url, namedGraph, auth=None):

  try:
    #namedGraphURL = f'{url}?context-uri=<{}>'
    #r = requests.delete(url, params={'c': f'<{namedGraph}>'}, auth=auth)
    payload = {'update': f'DROP GRAPH <{namedGraph}>;'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, data=payload, headers=headers, auth=auth)
    r.raise_for_status()
  except requests.HTTPError as he:
    statusCode = he.response.status_code
    print(f'{statusCode} error while deleting named graph {namedGraph} (first 100 characters): ' + he.response.content.decode('utf-8')[0:100])
    #print(he.response.content.decode('utf-8'))
    sys.exit(1)
  except Exception as e:
    print(f'Error while trying to delete named graph {namedGraph} with url {url}')
    print(e)
    sys.exit(1)


# -----------------------------------------------------------------------------
def sparqlSelectToString(url, queryFilename, acceptFormat, auth=None, httpMethod='post'):

  if not os.path.isfile(queryFilename):
    print(f'"{queryFilename}" is not a file!')
    return
  with open(queryFilename, 'rb') as query:
    print(f'\tProcessing query {queryFilename}')
    r = None
    try:
      start = time.time()
      if httpMethod == 'post':
        r = requests.post(url, data=query.read(), headers={'Content-Type': 'application/sparql-query', 'Accept': acceptFormat}, auth=auth)
      elif httpMethod == 'get':
        r = requests.get(url, data=query.read(), headers={'Content-Type': 'application/sparql-query', 'Accept': acceptFormat}, auth=auth)
      else:
        raise Exception(f'Supported HTTP methods are "post" and "get", but "{httpMethod}" was given')
      end = time.time()
      r.raise_for_status()

      queryTime = time.strftime('%H:%M:%S', time.gmtime(end - start))
      print(f'successfully queried in time {queryTime}')
      return r.content.decode('utf-8')

    except requests.HTTPError as he:
      statusCode = he.response.status_code
      print(f'{statusCode} error while updating {queryFilename} (first 40 characters): ' + he.response.content.decode('utf-8')[0:40])
      print(he.response.content.decode('utf-8'))
    except Exception as e:
      print(f'Error while querying {url} with {queryFilename} and acceptFormat {acceptFormat}')
      print(e)



# -----------------------------------------------------------------------------
def sparqlSelect(url, queryFilename, outputFilename, acceptFormat, auth=None):

  response = sparqlSelectToString(url, queryFilename, acceptFormat, auth=auth)
  with open(outputFilename, 'w', encoding='utf-8') as outputFile:
    numberChars = outputFile.write(response)
    print(f'successfully wrote {numberChars} characters to file {outputFilename}!')


# -----------------------------------------------------------------------------
def sparqlUpdateFile(url, filename, fileFormat, queryName, auth=None):

  if not os.path.isfile(filename):
    print(f'"{filename}" is not a file!')
    return
  with open(filename, 'rb') as fileIn:
    print(f'\tProcessing file {filename} (url: {url})')
    sparqlUpdate(url, fileIn.read(), fileFormat, queryName, auth)

# -----------------------------------------------------------------------------
def sparqlUpdate(url, queryString, fileFormat, queryName, auth=None):

  r = None
  try:
    r = requests.post(url, data=queryString, headers={'Content-Type': fileFormat}, auth=auth)
    r.raise_for_status()

    response = r.content.decode('utf-8')
    try:
      m = re.search(r".*totalElapsed=(\d+)ms.*mutationCount=(\d+).*", response)
      timeElapsed = m.group(1)
      mutations = m.group(2)
      print(f'\t{queryName}: {mutations} changes in {timeElapsed}ms')
    except Exception as e:
      # if the content was a file and no query the answer might be XML
      try:
        responseXML = ET.fromstring(response)
        modified = responseXML.get('modified')
        timeElapsed = responseXML.get('milliseconds')
        print(f'\t{queryName}: {modified} changes in {timeElapsed}ms')
      except Exception as e:
        print(f'Unexpected answer, first 200 characters of answer:' + response[0:200])
        print(e)
        print(response)

  except requests.HTTPError as he:
    statusCode = he.response.status_code
    print(f'{statusCode} error while updating {queryName}: ' + he.response.content.decode('utf-8')[0:40])
    print(he.response.content.decode('utf-8'))
  except Exception as e:
    print(f'Error while updating {url} with query {queryName} and type {fileFormat}')
    print(e)


# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
