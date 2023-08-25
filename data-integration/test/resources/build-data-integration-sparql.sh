
SOURCE_FOLDER="data-integration-sparql"
MAPPING_MANIFESTATIONS="manifestations.yml"
MAPPING_MANIFESTATIONS_BNF="manifestations-bnf.yml"
MAPPING_MANIFESTATIONS_CORRELATION="manifestations-correlation.yml"
MAPPING_ORIGINALS="originals.yml"
MAPPING_CONTRIBUTORS="contributors.yml"
MAPPING_CONTRIBUTORS_BNF="contributors-bnf.yml"
MAPPING_CONTRIBUTORS_CORRELATION="contributors-correlation.yml"
MAPPING_ISBN="isbn.yml"
MAPPING_SAMEAS="sameas.yml"

# build KBR data
export RML_TEST_SOURCE_PUBLICATIONS=$SOURCE_FOLDER"/kbr-manifestations.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_MANIFESTATIONS $SOURCE_FOLDER"/kbr-manifestations.ttl"
. map.sh $SOURCE_FOLDER"/"$MAPPING_ORIGINALS $SOURCE_FOLDER"/kbr-originals.ttl"
. map.sh $SOURCE_FOLDER"/"$MAPPING_ISBN $SOURCE_FOLDER"/kbr-isbns.ttl"

# build BnF data
export RML_TEST_SOURCE_PUBLICATIONS=$SOURCE_FOLDER"/bnf-manifestations.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_MANIFESTATIONS_BNF $SOURCE_FOLDER"/bnf-manifestations.ttl"
. map.sh $SOURCE_FOLDER"/"$MAPPING_ISBN $SOURCE_FOLDER"/bnf-isbns.ttl"

# build KB data
export RML_TEST_SOURCE_PUBLICATIONS=$SOURCE_FOLDER"/kb-manifestations.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_MANIFESTATIONS $SOURCE_FOLDER"/kb-manifestations.ttl"
. map.sh $SOURCE_FOLDER"/"$MAPPING_ORIGINALS $SOURCE_FOLDER"/kb-originals.ttl"
. map.sh $SOURCE_FOLDER"/"$MAPPING_ISBN $SOURCE_FOLDER"/kb-isbns.ttl"

# build correlation list manifestation data
export RML_TEST_SOURCE_PUBLICATIONS=$SOURCE_FOLDER"/correlation-list-manifestations.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_MANIFESTATIONS_CORRELATION $SOURCE_FOLDER"/correlation-list-manifestations.ttl"
. map.sh $SOURCE_FOLDER"/"$MAPPING_ISBN $SOURCE_FOLDER"/correlation-list-isbns.ttl"

# build KBR contributor data
export RML_TEST_SOURCE_CONTRIBUTORS=$SOURCE_FOLDER"/kbr-contributors.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_CONTRIBUTORS $SOURCE_FOLDER"/kbr-contributors.ttl"

# build BnF contributor data
export RML_TEST_SOURCE_CONTRIBUTORS=$SOURCE_FOLDER"/bnf-contributors.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_CONTRIBUTORS_BNF $SOURCE_FOLDER"/bnf-contributors.ttl"

# build KB contributor data
export RML_TEST_SOURCE_CONTRIBUTORS=$SOURCE_FOLDER"/kb-contributors.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_CONTRIBUTORS $SOURCE_FOLDER"/kb-contributors.ttl"

# build correlation list contributor data
export RML_TEST_SOURCE_CONTRIBUTORS=$SOURCE_FOLDER"/correlation-list-contributors.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_CONTRIBUTORS_CORRELATION $SOURCE_FOLDER"/correlation-list-contributors.ttl"
