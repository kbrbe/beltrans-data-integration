
if [ $# -ne 3 ];
then
  echo "Please provide a namespace, the SPARQL endpoint you would like to query and the name of the named graph you would like to delete."
  exit 1
fi;


# get environment variables
export $(cat .env | sed 's/#.*//g' | xargs)


curl -L -D- -X DELETE \
  --user $ENV_SPARQL_ENDPOINT_USER:$ENV_SPARQL_ENDPOINT_PASSWORD \
"$2/namespace/$1/sparql?c=<$3>"


