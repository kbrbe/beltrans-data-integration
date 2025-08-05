#!/bin/bash

set -euo pipefail

FORMAT_RDF_XML="application/rdf+xml"
FORMAT_TURTLE="text/turtle"
FORMAT_NT="text/rdf+n3"
FORMAT_SPARQL_UPDATE="application/sparql-update"

# -----------------------------------------------------------------------------
function deleteNamedGraph {
  local namespace=$1
  local endpoint=$2
  local namedGraph=$3

  local url="$endpoint/namespace/$namespace/sparql"
  echo "Delete existing content in namespace <$namedGraph> (url $url)"

  source ./py-integration-env/bin/activate
  python delete_named_graph.py -u "$url" --named-graph "$namedGraph"

  #. $SCRIPT_DELETE_NAMED_GRAPH "$namespace" "$endpoint" "$namedGraph"
}

# -----------------------------------------------------------------------------
function uploadRDFData {
  local endpointURL=$1
  local namespace=$2
  local namedGraph=$3
  local format=$4
  shift 4
  files=($"$@")

  if [[ "$format" == "$FORMAT_SPARQL_UPDATE" ]];
  then
    # upload data in the sense of "executing a SPARQL UPDATE" query
    # call to python script
    local uploadURL="$endpointURL/namespace/$namespace/sparql"

    if [ -z "$namedGraph" ];
    then
      echo python upload_data.py -u "$uploadURL" --content-type "$format" $files
      python upload_data.py -u "$uploadURL" --content-type "$format" $files
    else
      echo python upload_data.py -u "$uploadURL" --content-type "$format" --named-graph "$namedGraph" $files
      python upload_data.py -u "$uploadURL" --content-type "$format" --named-graph "$namedGraph" $files
    fi
  else

    # uploading data from file
    # call Blazegraph bulk import tool
    props="$(mktemp)"
    cat > "$props" <<EOF
com.bigdata.journal.AbstractJournal.file=/opt/blazegraph/data/bigdata.jnl
com.bigdata.rdf.store.AbstractTripleStore.quads=true
com.bigdata.rdf.store.DataLoader.commit=Batch
com.bigdata.rdf.store.DataLoader.flush=true
com.bigdata.rdf.store.DataLoader.bufferCapacity=30000
com.bigdata.rdf.store.DataLoader.queueCapacity=5
EOF
  #com.bigdata.rdf.store.DataLoader.commit=Batch
  #com.bigdata.rdf.store.DataLoader.flush=false

    # first stop Blazegraph service, because we need sole access to the DB journal file
    pkill -f 'java.*bigdata.jar' || true
    sleep 3

#      -Dlog4j.configuration=file:./log4j.properties \
    java -Xmx4g \
      -cp /opt/blazegraph/bigdata.jar \
      com.bigdata.rdf.store.DataLoader \
      -namespace "$namespace" \
      -defaultGraph "$namedGraph" \
      -verbose \
      "$props" \
      "${files[@]}"
    rm -f "$props"

    # restart Blazegraph service
    bash /opt/blazegraph/run_blazegraph.sh
    sleep 3
  fi
}


