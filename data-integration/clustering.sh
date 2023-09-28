
OUTPUT_DIR="2023-09-19_clustering"
NAMED_GRAPH="http://clustering-2023-09-19"
FILE_KEY_COMPONENTS=$OUTPUT_DIR/"key-components.csv"
CLUSTER_INPUT=$OUTPUT_DIR/"descriptive-keys.csv"
CLUSTERS=$OUTPUT_DIR/"found-clusters.csv"
CLUSTERS_TURTLE=$OUTPUT_DIR/"found-clusters.ttl"

KEY_COMPONENTS_QUERY="sparql-queries/clustering/get-descriptive-keys.sparql"
#KEY_COMPONENTS_QUERY="sparql-queries/clustering/get-descriptive-keys-all.sparql"
  
export $(cat .env | sed 's/#.*//g' | xargs)

mkdir -p $OUTPUT_DIR

# get components of the descriptive keys
#
echo "Get components of the descriptive keys"
python -m tools.sparql.query_data \
  -u "$ENV_SPARQL_ENDPOINT_INTEGRATION" \
  -q $KEY_COMPONENTS_QUERY \
  -o $FILE_KEY_COMPONENTS

# normalize key components and create descriptive keys
# 
echo "Normalize key components and create descriptive keys"
python -m tools.csv.clustering_normalization \
  -i $FILE_KEY_COMPONENTS \
  -o $CLUSTER_INPUT \
  --id-column "m" \
  --column "keyPart1" \
  --column "keyPart2"

# perform the clustering
#
echo "Perform the clustering"
python -m tools.csv.clustering \
  -i $CLUSTER_INPUT \
  -o $CLUSTERS \
  --id-column "elementID" \
  --key-column "descriptiveKey"

# create RDF representing the cluster assignments
#
echo "Create RDF"
export RML_SOURCE_CLUSTERS=$CLUSTERS
. map.sh clustering/cluster-assignments.yml $CLUSTERS_TURTLE

# upload RDF to enable advanced querying of cluster information
#
echo "Delete existing cluster assignments"
python -m tools.sparql.delete_named_graph \
  -u "$ENV_SPARQL_ENDPOINT_INTEGRATION" \
  --named-graph "$NAMED_GRAPH"

echo "Upload new data"
python -m tools.sparql.upload_data \
  -u "$ENV_SPARQL_ENDPOINT_INTEGRATION" \
  --content-type "text/turtle" \
  --named-graph "$NAMED_GRAPH" \
  $CLUSTERS_TURTLE
