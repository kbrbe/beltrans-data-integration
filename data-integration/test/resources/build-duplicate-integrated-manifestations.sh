
SOURCE_FOLDER="duplicate-integrated-manifestations"
MAPPING_MANIFESTATIONS="manifestations.yml"
MAPPING_CONTRIBUTORS="contributors.yml"
MAPPING_SAMEAS="sameas.yml"

# build local data
export RML_TEST_SOURCE_PUBLICATIONS=$SOURCE_FOLDER"/local-data.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_MANIFESTATIONS $SOURCE_FOLDER"/local-data.ttl"

# build integrated data
export RML_TEST_SOURCE_PUBLICATIONS=$SOURCE_FOLDER"/integrated-data.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_MANIFESTATIONS $SOURCE_FOLDER"/integrated-data.ttl"

# build integrated contributor data
export RML_TEST_SOURCE_CONTRIBUTORS=$SOURCE_FOLDER"/integrated-contributors.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_CONTRIBUTORS $SOURCE_FOLDER"/integrated-contributors.ttl"

# build local contributor data
export RML_TEST_SOURCE_CONTRIBUTORS=$SOURCE_FOLDER"/local-contributors.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_CONTRIBUTORS $SOURCE_FOLDER"/local-contributors.ttl"

# build sameas links
export RML_TEST_SOURCE_SAME_AS_LINKS=$SOURCE_FOLDER"/manifestations-sameas.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_SAMEAS $SOURCE_FOLDER"/manifestations-sameas.ttl"

export RML_TEST_SOURCE_SAME_AS_LINKS=$SOURCE_FOLDER"/contributors-sameas.csv"
. map.sh $SOURCE_FOLDER"/"$MAPPING_SAMEAS $SOURCE_FOLDER"/contributors-sameas.ttl"
