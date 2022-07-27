import os
import re
import lxml.etree as ET
import requests
import time

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
def query(target, queryString, outputWriter):
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
    res = requests.post(target, data=queryString, headers={'Accept': 'text/csv', 'Content-Type': 'application/sparql-query'})
    outputWriter.write(res.content)

# ------------------------------------------------------------
def readSPARQLQuery(filename):
    """Read a SPARQL query from file and return the content as a string."""
    content = ""
    with open(filename, 'r') as reader:
        content = reader.read()
    return content


# -----------------------------------------------------------------------------
def sparqlSelect(url, queryFilename, outputFilename, acceptFormat, auth=None):

  if not os.path.isfile(queryFilename):
    print(f'"{queryFilename}" is not a file!')
    return
  with open(queryFilename, 'rb') as query:
    print(f'\tProcessing query {queryFilename}')
    r = None
    try:
      start = time.time()
      r = requests.post(url, data=query.read(), headers={'Content-Type': 'application/sparql-query', 'Accept': acceptFormat}, auth=auth)
      end = time.time()
      r.raise_for_status()

      queryTime = time.strftime('%H:%M:%S', time.gmtime(end - start))
      response = r.content.decode('utf-8')

      with open(outputFilename, 'w', encoding='utf-8') as outputFile:
        numberChars = outputFile.write(response)
        print(f'successfully queried in time {queryTime} and wrote {numberChars} characters to file {outputFilename}!')

    except requests.HTTPError as he:
      statusCode = he.response.status_code
      print(f'{statusCode} error while updating {queryFilename} (first 40 characters): ' + he.response.content.decode('utf-8')[0:40])
      print(he.response.content.decode('utf-8'))
    except Exception as e:
      print(f'Error while querying {url} with {queryFilename} and acceptFormat {acceptFormat}')
      print(e)


# -----------------------------------------------------------------------------
def sparqlUpdate(url, filename, fileFormat, queryName, auth=None):
  if not os.path.isfile(filename):
    print(f'"{filename}" is not a file!')
    return
  with open(filename, 'rb') as fileIn:
    print(f'\tProcessing file {filename}')
    r = None
    try:
      r = requests.post(url, data=fileIn.read(), headers={'Content-Type': fileFormat}, auth=auth)
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
      print(f'{statusCode} error while updating {filename}: ' + he.response.content.decode('utf-8')[0:40])
      print(he.response.content.decode('utf-8'))
    except Exception as e:
      print('Error while updating {url} with {filename} and type {fileFormat}')
      print(e)


# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
