
if [ $# -ne 1 ];
then
  echo "Please provide an import config file"
  exit 1
fi;

if [ ! -f $1 ];
then
  echo "The provided name is not a valid file";
  exit 1
fi;

# get environment variables
export $(cat .env | sed 's/#.*//g' | xargs)

curl -X POST \
  --user $SPARQL_ENDPOINT_USER:$SPARQL_ENDPOINT_PASSWORD \
  --data-binary @$1 \
  --header 'Content-Type:application/xml' \
  $SPARQL_ENDPOINT_PUBLIC/namespace
