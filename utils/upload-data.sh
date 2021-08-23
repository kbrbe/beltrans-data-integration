
if [ $# -ne 3 ];
then
  echo "Please provide a namespace, the file to be imported and the format for the content type header"
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
  --user $SPARQL_ENDPOINT_USER_$SPARQL_ENDPOINT_PASSWORD \
  --header "Content-Type: $3" \
  --upload-file $2 \
$SPARQL_ENDPOINT_PUBLIC/namespace/$1/sparql

# if in quad mode a named graph could be specified by attaching the following to the namespace/<ns>/sparql?context-uri=https://my-namespace

