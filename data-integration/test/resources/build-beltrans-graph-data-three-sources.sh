

# build KBR test data
export RML_TEST_SOURCE_PUBLICATIONS="beltrans-graph-data-three-sources/kbr-data.csv"
export RML_TEST_SOURCE_CONTRIBUTORS="beltrans-graph-data-three-sources/kbr-contributors.csv"
. map.sh beltrans-graph-data-three-sources/manifestations.yml beltrans-graph-data-three-sources/kbr-data.ttl
. map.sh beltrans-graph-data-three-sources/contributors.yml beltrans-graph-data-three-sources/kbr-contributors.ttl

# build BnF test data
export RML_TEST_SOURCE_PUBLICATIONS="beltrans-graph-data-three-sources/bnf-data.csv"
export RML_TEST_SOURCE_CONTRIBUTORS="beltrans-graph-data-three-sources/bnf-contributors.csv"
. map.sh beltrans-graph-data-three-sources/manifestations.yml beltrans-graph-data-three-sources/bnf-data.ttl
. map.sh beltrans-graph-data-three-sources/contributors.yml beltrans-graph-data-three-sources/bnf-contributors.ttl

# build KB test data
export RML_TEST_SOURCE_PUBLICATIONS="beltrans-graph-data-three-sources/kb-data.csv"
export RML_TEST_SOURCE_CONTRIBUTORS="beltrans-graph-data-three-sources/kb-contributors.csv"
. map.sh beltrans-graph-data-three-sources/manifestations.yml beltrans-graph-data-three-sources/kb-data.ttl
. map.sh beltrans-graph-data-three-sources/contributors.yml beltrans-graph-data-three-sources/kb-contributors.ttl

# build integrated test data
# The sameas links have to be in the same turtle file as the definitions, because loading a second turtle file to a named graph overwrites existing content
export RML_TEST_SOURCE_PUBLICATIONS="beltrans-graph-data-three-sources/integrated-data.csv"
export RML_TEST_SOURCE_CONTRIBUTORS="beltrans-graph-data-three-sources/integrated-contributors.csv"
export RML_TEST_SOURCE_SAME_AS_LINKS="beltrans-graph-data-three-sources/manifestation-links.csv"
. map.sh beltrans-graph-data-three-sources/manifestations-integrated.yml beltrans-graph-data-three-sources/integrated-data.ttl
export RML_TEST_SOURCE_SAME_AS_LINKS="beltrans-graph-data-three-sources/contributor-links.csv"
. map.sh beltrans-graph-data-three-sources/contributors-integrated.yml beltrans-graph-data-three-sources/integrated-contributors.ttl

