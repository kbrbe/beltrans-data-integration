
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

curl -X POST \
  --header "Content-Type: $3" \
  --upload-file $2 \
http://localhost:8090/bigdata/namespace/$1/sparql

# if in quad mode a named graph could be specified by attaching the following to the namespace/<ns>/sparql?context-uri=https://my-namespace

