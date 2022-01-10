
if [ $# -lt 4 ] || [ $# -gt 5 ];
then
  echo "Please provide a namespace, the file to be imported, the format for the content type header, and the SPARQL endpoint you would like to upload the data to. Optionally the named graph"
  exit 1
fi;

if [ ! -f $2 ];
then
  echo "The provided name is not a valid file";
  exit 1
fi;

# get environment variables
export $(cat .env | sed 's/#.*//g' | xargs)

if [ -z $5 ];
then
  url=$4/namespace/$1/sparql
else
  url=$4/namespace/$1/sparql?context-uri=$5
fi

curl -X POST \
  --user $ENV_SPARQL_ENDPOINT_USER:$ENV_SPARQL_ENDPOINT_PASSWORD \
  --header "Content-Type: $3" \
  --upload-file $2 \
$url

# if in quad mode a named graph could be specified by attaching the following to the namespace/<ns>/sparql?context-uri=https://my-namespace

