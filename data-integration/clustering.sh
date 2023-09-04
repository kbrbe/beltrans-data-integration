
OUTPUT_DIR="2023-09-01_clustering"
FILE_KEY_COMPONENTS=$OUTPUT_DIR/"key-components.csv"
CLUSTER_INPUT=$OUTPUT_DIR/"descriptive-keys.csv"
CLUSTERS=$OUTPUT_DIR/"found-clusters.csv"
CLUSTERS_TURTLE=$OUTPUT_DIR/"found-clusters.ttl"

mkdir -p $OUTPUT_DIR

# get components of the descriptive keys
#
python -m tools.sparql.query_data \
  -u "$ENV_SPARQL_ENDPOINT" \
  -q sparql-queries/clustering/get-descriptive-keys.sparql \
  -o $FILE_KEY_COMPONENTS

# normalize key components and create descriptive keys
# 
python -m tools.csv.clustering_normalization \
  -i $FILE_KEY_COMPONENTS \
  -o $CLUSTER_INPUT \
  --id-column "m" \
  --column "title" \
  --column "keyPart2"

# perform the clustering
#
python -m tools.csv.clustering \
  -i $CLUSTER_INPUT \
  -o $CLUSTERS \
  --id-column "elementID" \
  --key-column "descriptiveKey"

# create RDF representing the cluster assignments
#
export RML_SOURCE_CLUSTERS=$CLUSTERS
. map.sh clustering/cluster-assignments.yml $CLUSTERS_TURTLE

# upload RDF to enable advanced querying of cluster information
#
python -m tools.sparql.upload_data \
  -u "$ENV_SPARQL_ENDPOINT" \
  --content-type "text/turtle" \
  --named-graph "http://clustering-2023-09-04" \
  $CLUSTERS_TURTLE
