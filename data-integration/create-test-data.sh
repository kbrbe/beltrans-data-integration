
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

# the nationality property is different for BnF, thus a different mapping file than for KBR test data
. map.sh test/test-data-publications.yml "./test/resources/bnf-data.ttl"
. map.sh test/test-data-contributors-bnf.yml "./test/resources/bnf-contributors.ttl"
