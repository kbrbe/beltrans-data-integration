source .env

trap 'echo ""; echo "ERROR: Integration stopped unexpectedly, one of the commands returned an error. ($0:$LINENO): $(sed -n "${LINENO}p" "$0")"' ERR
set -Eeuo pipefail



DOWNLOAD_DATE="2025-10-23"
NUMBER_ISNI_RECORDS="56088"

NAMED_GRAPH="http://isni-sru"
ISNI_API_BATCH_SIZE=500
ISNI_DOWNLOAD_FILES_PREFIX="isni_assigned-belgian"
DATA_PATH="/data/beltrans/data-sources/isni-sru"
ISNI_API_DOWNLOAD_FOLDER="$DATA_PATH/$DOWNLOAD_DATE""_$ISNI_DOWNLOAD_FILES_PREFIX"
AUTHORITY_FILE="$DATA_PATH/$DOWNLOAD_DATE""_isni-sru-authorities.csv"
THIRD_PARTY_LINKS_FILE="$DATA_PATH/$DOWNLOAD_DATE""_isni-sru-identifier-links.csv"
ISNI_TURTLE_FILE="$DATA_PATH/$DOWNLOAD_DATE""_isni-authorities.ttl"

# set input variables used in the YARRRML mapping file
export RML_ISNI_AUTHORITY_FILE=$AUTHORITY_FILE
export RML_ISNI_LINKS_FILE=$THIRD_PARTY_LINKS_FILE

python ../data-sources/isni/retrieveSRURecords.py \
  -r $ISNI_API_BATCH_SIZE \
  -m $NUMBER_ISNI_RECORDS \
  -o $ISNI_DOWNLOAD_FILES_PREFIX
  
mkdir -p "$ISNI_API_DOWNLOAD_FOLDER"
mv $DOWNLOAD_DATE*xml $ISNI_API_DOWNLOAD_FOLDER

# create ISNI CSV files
python ../data-sources/isni/isni-xml-to-csv.py \
  -i "$ISNI_API_DOWNLOAD_FOLDER" \
  -a $AUTHORITY_FILE \
  -o $THIRD_PARTY_LINKS_FILE \

# map data to RDF
bash ../data-sources/map.sh ../data-sources/isni/authorities.yml $ISNI_TURTLE_FILE

# delete existing ISNI named graph
python -m tools.sparql.delete_named_graph \
  -u $ENV_SPARQL_ENDPOINT_INTEGRATION \
  -n "$NAMED_GRAPH"

# upload new data
python -m tools.sparql.upload_data \
  -u $ENV_SPARQL_ENDPOINT_INTEGRATION \
  --content-type "text/turtle" \
  --named-graph "$NAMED_GRAPH" \
  "$ISNI_TURTLE_FILE"
