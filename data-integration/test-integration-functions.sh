#!/bin/bash

set -e

cd ..
export PYTHONPATH=$(pwd)
cd -

# get environment variables
export $(cat .env | sed 's/#.*//g' | xargs)

# import functions
. integration-functions.sh

# test data
blazegraphNamespace="integration"
namedGraph="http://test"
ttlFile1="test-upload-function-1.ttl"
ttlFile2="test-upload-function-2.ttl"
queryFile1="test-upload-function-query.sparql"
selectAllQueryFile="test-upload-function-select-all.sparql"


## TEST SPARQL UPDATE
function testSPARQLUpdate {

  # prepare test environment
  deleteNamedGraph "$blazegraphNamespace" "$ENV_SPARQL_ENDPOINT" "$namedGraph"
  python upload_data.py -u "$ENV_SPARQL_ENDPOINT_INTEGRATION" --content-type "$FORMAT_TURTLE" --named-graph "$namedGraph" "$ttlFile1"


  echo "executing test function"
  # execute function to test
  uploadRDFData \
    "$ENV_SPARQL_ENDPOINT" \
    "$blazegraphNamespace" \
    "$namedGraph" \
    "$FORMAT_SPARQL_UPDATE" \
    "$queryFile1"

  # check result
  echo "## TEST SPARQL UPDATE"
  changedDataFile="$(mktemp)"
  python -m tools.sparql.query_data -u "$ENV_SPARQL_ENDPOINT_INTEGRATION" -q "$selectAllQueryFile" -o "$changedDataFile"
  cat $changedDataFile
  echo ""
}


function testSPARQLBulkInsert {
  ## ########################################
  ## TEST insert via Blazegraph bulk load api
  #deleteNamedGraph "$blazegraphNamespace" "$ENV_SPARQL_ENDPOINT" "$namedGraph"

  uploadRDFData \
    "$ENV_SPARQL_ENDPOINT" \
    "$blazegraphNamespace" \
    "$namedGraph" \
    "$FORMAT_TURTLE" \
    "$ttlFile1" \
    "$ttlFile2"

  changedDataFile="$(mktemp)"
  python -m tools.sparql.query_data -u "$ENV_SPARQL_ENDPOINT_INTEGRATION" -q "$selectAllQueryFile" -o "$changedDataFile"
  cat $changedDataFile
  echo ""
}

testSPARQLBulkInsert
