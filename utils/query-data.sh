
if [ $# -ne 3 ];
then
  echo "Please provide a SPARQL endpoint, the file with the query, and the name of the output file."
  exit 1
fi;

if [ ! -f $2 ];
then
  echo "The provided name is not a valid file";
  exit 1
fi;

# get environment variables
export $(cat .env | sed 's/#.*//g' | xargs)

curl -X POST \
  --user $ENV_SPARQL_ENDPOINT_USER:$ENV_SPARQL_ENDPOINT_PASSWORD \
  --header "Accept: text/csv" \
  --header "Content-Type: application/sparql-query" \
  --upload-file $2 \
  -o $3 \
$1
#$3/namespace/$1/sparql

# if in quad mode a named graph could be specified by attaching the following to the namespace/<ns>/sparql?context-uri=https://my-namespace

