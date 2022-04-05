
#
# CREATE KBR test data
#
export RML_TEST_SOURCE_PUBLICATIONS="./test/resources/kbr-data.csv"
export RML_TEST_SOURCE_CONTRIBUTORS="./test/resources/kbr-contributors.csv"

. map.sh test/test-data-publications.yml "./test/resources/kbr-data.ttl"
. map.sh test/test-data-contributors.yml "./test/resources/kbr-contributors.ttl"

#
# CREATE BnF test data
#
export RML_TEST_SOURCE_PUBLICATIONS="./test/resources/bnf-data.csv"
export RML_TEST_SOURCE_CONTRIBUTORS="./test/resources/bnf-contributors.csv"

. map.sh test/test-data-publications.yml "./test/resources/bnf-data.ttl"
. map.sh test/test-data-contributors.yml "./test/resources/bnf-contributors.ttl"
