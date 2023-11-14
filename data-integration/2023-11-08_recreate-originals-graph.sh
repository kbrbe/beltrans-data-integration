export $(cat .env | sed 's/#.*//g' | xargs)

sparqlEndpoint=$ENV_SPARQL_ENDPOINT_INTEGRATION

echo "Start queries against '$sparqlEndpoint'"
python -m tools.sparql.delete_named_graph -u $sparqlEndpoint -n "http://beltrans-originals"
python -m tools.sparql.upload_data -u $sparqlEndpoint --content-type "application/sparql-update" sparql-queries/derive-single-title-from-bibframe-titles.sparql
python -m tools.sparql.upload_data -u $sparqlEndpoint --content-type "application/sparql-update" sparql-queries/create-beltrans-originals.sparql
python -m tools.sparql.upload_data -u $sparqlEndpoint --content-type "application/sparql-update" integration_queries/link-beltrans-original-manifestations-contributors.sparql
python -m tools.sparql.upload_data -u $sparqlEndpoint --content-type "application/sparql-update" sparql-queries/create-bibframe-titles.sparql
