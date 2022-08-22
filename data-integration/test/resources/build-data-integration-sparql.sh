
SOURCE_FOLDER="data-integration-sparql"
MAPPING_MANIFESTATIONS="manifestations.yml"
MAPPING_CONTRIBUTORS="contributors.yml"
MAPPING_SAMEAS="sameas.yml"

# build KBR data
export RML_TEST_SOURCE_PUBLICATIONS=$SOURCE_FOLDER"/kbr-manifestations.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_MANIFESTATIONS $SOURCE_FOLDER"/kbr-manifestations.ttl"

# build BnF data
export RML_TEST_SOURCE_PUBLICATIONS=$SOURCE_FOLDER"/bnf-manifestations.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_MANIFESTATIONS $SOURCE_FOLDER"/bnf-manifestations.ttl"

# build KB data
export RML_TEST_SOURCE_PUBLICATIONS=$SOURCE_FOLDER"/kb-manifestations.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_MANIFESTATIONS $SOURCE_FOLDER"/kb-manifestations.ttl"


# build KBR contributor data
export RML_TEST_SOURCE_CONTRIBUTORS=$SOURCE_FOLDER"/kbr-contributors.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_CONTRIBUTORS $SOURCE_FOLDER"/kbr-contributors.ttl"

# build BnF contributor data
export RML_TEST_SOURCE_CONTRIBUTORS=$SOURCE_FOLDER"/bnf-contributors.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_CONTRIBUTORS $SOURCE_FOLDER"/bnf-contributors.ttl"

# build KB contributor data
export RML_TEST_SOURCE_CONTRIBUTORS=$SOURCE_FOLDER"/kb-contributors.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_CONTRIBUTORS $SOURCE_FOLDER"/kb-contributors.ttl"
