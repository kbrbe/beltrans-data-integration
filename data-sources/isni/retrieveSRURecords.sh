
# stop the loop when ctrl+c is pressed
trap "exit" INT

# Read environment variables (used e.g. for the password secret)
export $(grep -v '^#' .env | xargs)

BASE_URL=https://isni-m.oclc.org/sru
USERNAME=$ISNI_SRU_USERNAME
PASSWORD=$ISNI_SRU_PASSWORD
QUERY='pica.noi%3D%22BE%22'
MAX_RECORDS="1000"
DATE_STRING=`date +"%Y-%m-%d"`
OUTPUT_BASENAME="$DATE_STRING-sru-result"

#
# There are currently 60452 records for the search term pica.noi="BE" and the number of max records per request is 1000
# Thus loop from 1 to 61000 in steps of 1000 to make 61 requests
#
for i in {1..61000..1000}
do
  echo "Requesting $MAX_RECORDS with starting record $i"
  curl "$BASE_URL/username=$USERNAME/password=$PASSWORD/DB=1.3/?operation=searchRetrieval&version=1.1&recordSchema=isni-e&query=$QUERY&maximumRecords=$MAX_RECORDS&startRecord=$i" > $OUTPUT_BASENAME"-$i.xml"
  sleep 1
done



