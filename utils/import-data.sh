
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

curl -X POST \
  --data-binary @$1 \
  --header 'Content-Type:text/plain' \
  http://localhost:8090/bigdata/dataloader
