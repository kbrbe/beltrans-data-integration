
SOURCE_FOLDER="title-representation"
MAPPING_MANIFESTATIONS="manifestations.yml"

# KBR has a different mapping file, as here we already do a title/subtitle mapping according to BIBFRAME
MAPPING_MANIFESTATIONS_KBR="manifestations-kbr.yml"

# build KBR data
export RML_TEST_SOURCE_PUBLICATIONS=$SOURCE_FOLDER"/kbr-data.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_MANIFESTATIONS_KBR $SOURCE_FOLDER"/kbr-data.ttl"

# build BnF data
export RML_TEST_SOURCE_PUBLICATIONS=$SOURCE_FOLDER"/bnf-data.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_MANIFESTATIONS $SOURCE_FOLDER"/bnf-data.ttl"

# build KB data
export RML_TEST_SOURCE_PUBLICATIONS=$SOURCE_FOLDER"/kb-data.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_MANIFESTATIONS $SOURCE_FOLDER"/kb-data.ttl"

