#!/bin/bash

# Make the locally developed python package accessible via python -m 
export PYTHONPATH=/home/slieber/repos/beltrans-data

SCRIPT_CLEAN_TRANSLATIONS="../data-sources/kbr/clean-marc-slim.py"
SCRIPT_CLEAN_AGENTS="../data-sources/kbr/pre-process-kbr-authors.py"
SCRIPT_EXTRACT_AGENTS_ORGS="../data-sources/kbr/authority-orgs-marc-to-csv.py"
SCRIPT_EXTRACT_AGENTS_PERSONS="../data-sources/kbr/authority-persons-marc-to-csv.py"
SCRIPT_TRANSFORM_TRANSLATIONS="../data-sources/kbr/marc-to-csv.py"
SCRIPT_NORMALIZE_HEADERS="../data-sources/kbr/replace-headers.py"
SCRIPT_CHANGE_PUBLISHER_NAME="../data-sources/kbr/change-publisher-name.py"
SCRIPT_EXTRACT_IDENTIFIED_AUTHORITIES="../data-sources/kbr/get-identified-authorities.sh"
SCRIPT_EXTRACT_SEPARATED_COL="../data-sources/kbr/extract-and-normalize-separated-strings.py"
SCRIPT_DEDUPLICATE_KBR_PUBLISHERS="../data-sources/kbr/deduplicate-publishers.py"

SCRIPT_FIND_ORIGINALS="find-originals.py"

SCRIPT_CONVERT_BB="../data-sources/master-data/convert-thesaurus.py"

SCRIPT_ADD_ISBN_10_13="../data-sources/kb/add-formatted-isbn-10-13.py"
SCRIPT_BNF_ADD_ISBN_10_13="../data-sources/bnf/add-formatted-isbn-10-13.py"
SCRIPT_FIX_ISBN10="../data-sources/bnf/formatISBN10.py"
SCRIPT_FIX_ISBN13="../data-sources/bnf/formatISBN13.py"
SCRIPT_CREATE_ISBN10_TRIPLES="../data-sources/bnf/createISBN10Triples.py"
SCRIPT_CREATE_ISBN13_TRIPLES="../data-sources/bnf/createISBN13Triples.py"
SCRIPT_CSV_TO_EXCEL="csv_to_excel.py"
SCRIPT_COMPUTE_STATS="create-publication-stats.py"
SCRIPT_CREATE_CONTRIBUTOR_LIST="create-contributor-list.py"

SCRIPT_INTERLINK_DATA="interlink_named_graph_data.py"

MODULE_GET_RDF_XML_SUBJECTS="tools.xml.get-subjects"
SCRIPT_GET_RDF_XML_OBJECTS="../data-sources/bnf/get-objects.py"
MODULE_EXTRACT_COLUMNS="tools.csv.extract_columns"

# the following script is an older deprecated version of the script above
SCRIPT_EXTRACT_COLUMN="../data-sources/bnf/extractColumn.py" 

MODULE_FILTER_RDF_XML_SUBJECTS="tools.xml.filter-subjects-xml" 

SCRIPT_UNION_IDS="../data-sources/bnf/union.py"

SCRIPT_UPLOAD_DATA="../utils/upload-data.sh"
SCRIPT_DELETE_NAMED_GRAPH="../utils/delete-named-graph.sh"
SCRIPT_QUERY_DATA="../utils/query-data.sh"
SCRIPT_POSTPROCESS_QUERY_RESULT="post-process-integration-result.py"
SCRIPT_POSTPROCESS_AGG_QUERY_RESULT="post-process-manifestations.py"
SCRIPT_POSTPROCESS_QUERY_CONT_RESULT="post-process-contributors.py"
SCRIPT_POSTPROCESS_DERIVE_COUNTRIES="add_country.py"
SCRIPT_POSTPROCESS_GET_GEONAME_PLACE_OF_PUBLICATION="add_coordinates.py"

BNF_FILTER_CONFIG_CONTRIBUTORS="../data-sources/bnf/filter-config-beltrans-contributor-nationality.csv"
KBR_CSV_HEADER_CONVERSION="../data-sources/kbr/author-headers.csv"

# #############################################################################
#
# INPUT FILENAMES
#

# KBR - translations
#INPUT_KBR_TRL_NL="../data-sources/kbr/translations/KBR_1970-2020_NL-FR_2022-02-17_4745records.xml"
#INPUT_KBR_TRL_FR="../data-sources/kbr/translations/KBR_1970-2020_FR-NL_2022-02-17_13126records.xml"
INPUT_KBR_TRL_NL="../data-sources/kbr/translations/KBR_1970-2020_NL-FR_2022-09-11_5507records.xml"
INPUT_KBR_TRL_FR="../data-sources/kbr/translations/KBR_1970-2020_FR-NL_2022-09-11_16459records.xml"

INPUT_KBR_TRL_ORIG_NL_FR="../data-sources/kbr/translations/originals/BELTRANS_NL-FR_NL-gelinkte-documenten.xml"
INPUT_KBR_TRL_ORIG_FR_NL="../data-sources/kbr/translations/originals/BELTRANS_FR-NL_FR-gelinkte-documenten.xml"

INPUT_KBR_ORGS_LOOKUP="../data-sources/kbr/agents/aorg.csv"

# KBR - linked authorities
INPUT_KBR_LA_PERSON_NL="../data-sources/kbr/agents/ExportSyracuse_Autoriteit_2022-09-11_NL-FR_APEP_4591.xml"
INPUT_KBR_LA_ORG_NL="../data-sources/kbr/agents/ExportSyracuse_Autoriteit_2022-09-11_NL-FR_AORG_860.xml"
INPUT_KBR_LA_PERSON_FR="../data-sources/kbr/agents/ExportSyracuse_Autoriteit_2022-09-11_FR-NL_APEP_10656.xml"
INPUT_KBR_LA_ORG_FR="../data-sources/kbr/agents/ExportSyracuse_Autoriteit_2022-09-11_FR-NL_AORG_984.xml"

INPUT_KBR_LA_PLACES_VLG="../data-sources/kbr/agents/publisher-places-VLG.csv"
INPUT_KBR_LA_PLACES_WAL="../data-sources/kbr/agents/publisher-places-WAL.csv"
INPUT_KBR_LA_PLACES_BRU="../data-sources/kbr/agents/publisher-places-BRU.csv"

INPUT_KBR_PBL_REPLACE_LIST="../data-sources/kbr/agents/publisher-name-mapping.csv"

# KBR - Belgians
INPUT_KBR_BELGIANS="../data-sources/kbr/agents/ExportSyracuse_ANAT-belg_2022-09-05_28772records.xml"

# BNF
INPUT_BNF_PERSON_AUTHORS="../data-sources/bnf/person-authors"
INPUT_BNF_ORG_AUTHORS="../data-sources/bnf/org-authors"
INPUT_BNF_EDITIONS="../data-sources/bnf/editions"
INPUT_BNF_CONTRIBUTIONS="../data-sources/bnf/contributions"
INPUT_BNF_TRL_FR_NL="../data-sources/bnf/BnF_FR-NL_1970-2020_584notices.csv"
INPUT_BNF_TRL_NL_FR="../data-sources/bnf/BnF_NL-FR_1970-2020_3762notices.csv"
INPUT_BNF_CONT_ISNI="../data-sources/bnf/external/dump_extref-isni_exact_match.xml"
INPUT_BNF_CONT_VIAF="../data-sources/bnf/external/dump_extref-viaf_exact_match.xml"
INPUT_BNF_CONT_WIKIDATA="../data-sources/bnf/external/dump_extref-wikidata_exact_match.xml"


# KB
INPUT_KB_ORGS_DIR="../data-sources/kb/orgs"

# MASTER DATA

INPUT_MASTER_MARC_ROLES="../data-sources/master-data/marc-roles.csv"
INPUT_MASTER_MARC_BINDING_TYPES="../data-sources/master-data/binding-types.csv"
INPUT_MASTER_COUNTRIES="../data-sources/master-data/countries.nt"
INPUT_MASTER_LANGUAGES="../data-sources/master-data/languages.nt"
INPUT_MASTER_GENDER="../data-sources/master-data/gender.ttl"
INPUT_MASTER_THES_EN="../data-sources/master-data/thesaurus-belgian-bibliography-en.csv"
INPUT_MASTER_THES_NL="../data-sources/master-data/thesaurus-belgian-bibliography-nl.csv"
INPUT_MASTER_THES_FR="../data-sources/master-data/thesaurus-belgian-bibliography-fr.csv"

# WIKIDATA
INPUT_WIKIDATA_ENRICHED="../data-sources/wikidata/2022-04-14-beltrans-wikidata-manually-enriched.csv"


# #############################################################################

#
# CONFIGURATION
#
#

TRIPLE_STORE_GRAPH_INT_TRL="http://beltrans-manifestations"
TRIPLE_STORE_GRAPH_INT_CONT="http://beltrans-contributors"
TRIPLE_STORE_GRAPH_KBR_TRL="http://kbr-syracuse"
TRIPLE_STORE_GRAPH_KBR_ORIG_TRL="http://kbr-originals"
TRIPLE_STORE_GRAPH_BNF_TRL="http://bnf-publications"
TRIPLE_STORE_GRAPH_BNF_TRL_FR_NL="http://bnf-fr-nl"
TRIPLE_STORE_GRAPH_BNF_TRL_NL_FR="http://bnf-nl-fr"
TRIPLE_STORE_GRAPH_BNF_TRL_CONT_LINKS="http://bnf-trl-contributor-links"
TRIPLE_STORE_GRAPH_BNF_CONT="http://bnf-contributors"
TRIPLE_STORE_GRAPH_BNF_CONT_ISNI="http://bnf-contributors-isni"
TRIPLE_STORE_GRAPH_BNF_CONT_VIAF="http://bnf-contributors-viaf"
TRIPLE_STORE_GRAPH_BNF_CONT_WIKIDATA="http://bnf-contributors-wikidata"
TRIPLE_STORE_GRAPH_KBR_LA="http://kbr-linked-authorities"
TRIPLE_STORE_GRAPH_KBR_ORIG_LA="http://kbr-originals-linked-authorities"
TRIPLE_STORE_GRAPH_KBR_BELGIANS="http://kbr-belgians"
TRIPLE_STORE_GRAPH_KB_TRL="http://kb-publications"
TRIPLE_STORE_GRAPH_KB_TRL_ORIG="http://kb-originals"
TRIPLE_STORE_GRAPH_KB_LA="http://kb-linked-authorities"
TRIPLE_STORE_GRAPH_KB_PBL="http://kb-publishers"
TRIPLE_STORE_GRAPH_MASTER="http://master-data"
TRIPLE_STORE_GRAPH_WIKIDATA="http://wikidata"
TRIPLE_STORE_GRAPH_KBCODE="http://kbcode"

# if it is a blazegraph triple store
TRIPLE_STORE_NAMESPACE="integration"

FORMAT_RDF_XML="application/rdf+xml"
FORMAT_TURTLE="text/turtle"
FORMAT_NT="text/rdf+n3"
FORMAT_SPARQL_UPDATE="application/sparql-update"

KB_SPARQL_ENDPOINT="http://data.bibliotheken.nl/sparql"

GET_BNF_ISBN10_ISBN13_QUERY_FILE="sparql-queries/get-bnf-isbn10-13.sparql"
GET_BNF_ISBN10_WITHOUT_HYPHEN_QUERY_FILE="sparql-queries/get-bnf-isbn10-without-hyphen.sparql"
GET_BNF_ISBN13_WITHOUT_HYPHEN_QUERY_FILE="sparql-queries/get-bnf-isbn13-without-hyphen.sparql"

GET_KBCODE_HIERARCHY_INFO_QUERY_FILE="sparql-queries/get-kbcode-hierarchy.sparql"

GET_MISSING_NATIONALITIES_ISNI_QUERY_FILE="sparql-queries/get-missing-nationality-isni.sparql"

DELETE_QUERY_BNF_ISBN="sparql-queries/delete-bnf-isbn.sparql"
DELETE_QUERY_BNF_ISBN10_WITHOUT_HYPHEN="sparql-queries/delete-bnf-isbn10-without-hyphen.sparql"
DELETE_QUERY_BNF_ISBN13_WITHOUT_HYPHEN="sparql-queries/delete-bnf-isbn13-without-hyphen.sparql"
DELETE_QUERY_DUPLICATE_MANIFESTATIONS="sparql-queries/delete-duplicate-manifestations.sparql"

TRANSFORM_QUERY_BNF_TRL_NL_FR="sparql-queries/transform-bnf-data-nl-fr.sparql"
TRANSFORM_QUERY_BNF_TRL_FR_NL="sparql-queries/transform-bnf-data-fr-nl.sparql"
CREATE_QUERY_BNF_IDENTIFIER_CONT="sparql-queries/create-bnf-contributors-identifier.sparql"
CREATE_QUERY_BNF_IDENTIFIER_MANIFESTATIONS="sparql-queries/create-bnf-manifestation-identifier.sparql"
CREATE_QUERY_BNF_ISNI="sparql-queries/create-bnf-isni.sparql"
CREATE_QUERY_BNF_VIAF="sparql-queries/create-bnf-viaf.sparql"
CREATE_QUERY_BNF_WIKIDATA="sparql-queries/create-bnf-wikidata.sparql"

CREATE_QUERY_KB_TRL_PBL="sparql-queries/link-kb-translations-to-publishers.sparql"

LINK_QUERY_CONT_AUTHORS="integration_queries/link-beltrans-manifestations-authors.sparql"
LINK_QUERY_CONT_TRANSLATORS="integration_queries/link-beltrans-manifestations-translators.sparql"
LINK_QUERY_CONT_ILLUSTRATORS="integration_queries/link-beltrans-manifestations-illustrators.sparql"
LINK_QUERY_CONT_SCENARISTS="integration_queries/link-beltrans-manifestations-scenarists.sparql"
LINK_QUERY_CONT_PUBLISHING_DIRECTORS="integration_queries/link-beltrans-manifestations-publishing-directors.sparql"

DATA_PROFILE_QUERY_FILE_AGG="dataprofile-aggregated.sparql"
DATA_PROFILE_QUERY_FILE_CONT_PERSONS="dataprofile-contributors-persons.sparql"
DATA_PROFILE_QUERY_FILE_CONT_ORGS="dataprofile-contributors-orgs.sparql"
DATA_PROFILE_QUERY_FILE_KBR="dataprofile-kbr.sparql"
DATA_PROFILE_QUERY_FILE_BNF="dataprofile-bnf.sparql"
DATA_PROFILE_AGG_QUERY_FILE_KBR="dataprofile-aggregated-kbr.sparql"
DATA_PROFILE_AGG_QUERY_FILE_BNF="dataprofile-aggregated-bnf.sparql"
DATA_PROFILE_CONT_BE_QUERY_FILE="contributors-belgian.sparql"
DATA_PROFILE_CONT_ALL_QUERY_FILE="contributors-all.sparql"
DATA_PROFILE_PUBS_PER_YEAR_QUERY_FILE="translations-per-year.sparql"
DATA_PROFILE_PUBS_PER_LOC_QUERY_FILE="translations-per-location.sparql"
DATA_PROFILE_PUBS_PER_COUNTRY_QUERY_FILE="translations-per-country.sparql"
DATA_PROFILE_PUBS_PER_PBL_QUERY_FILE="translations-per-publisher.sparql"
DATA_PROFILE_SOURCE_STATS_QUERY_FILE="source-stats.sparql"

SUFFIX_DATA_PROFILE_CONT_PERSONS_ALL_DATA_FILE="contributors-persons-all-info.csv"
SUFFIX_DATA_PROFILE_CONT_PERSONS_FILE="contributors-persons.csv"
SUFFIX_DATA_PROFILE_CONT_ALL_PERSONS="all-persons.csv"
SUFFIX_DATA_PROFILE_CONT_ORGS_FILE="contributors-orgs.csv"
SUFFIX_DATA_PROFILE_FILE_KBR="integrated-data-kbr-not-filtered.csv"
SUFFIX_DATA_PROFILE_FILE_BNF="integrated-data-bnf-not-filtered.csv"
SUFFIX_DATA_PROFILE_CONT_BE_FILE="integrated-data-contributors-belgian-not-filtered.csv"
SUFFIX_DATA_PROFILE_CONT_ALL_FILE="integrated-data-contributors-all-not-filtered.csv"
SUFFIX_DATA_PROFILE_AGG_FILE_KBR="integrated-data-aggregated-kbr.csv"
SUFFIX_DATA_PROFILE_AGG_FILE_BNF="integrated-data-aggregated-bnf.csv"
SUFFIX_DATA_PROFILE_PUBS_PER_YEAR_FILE="translations-per-year.csv"
SUFFIX_DATA_PROFILE_PUBS_PER_LOC_FILE="translations-per-location.csv"
SUFFIX_DATA_PROFILE_PUBS_PER_COUNTRY_FILE="translations-per-country.csv"
SUFFIX_DATA_PROFILE_PUBS_PER_PBL_FILE="translations-per-publisher.csv"
SUFFIX_DATA_PROFILE_DTYPES="dataprofile-dtypes.csv"

SUFFIX_DATA_PROFILE_FILE_PROCESSED="integrated-data.csv"
SUFFIX_DATA_PROFILE_FILE_ALL="integrated-data-all-info.csv"
SUFFIX_DATA_PROFILE_FILE_ENRICHED="integrated-data-enriched.csv"
SUFFIX_DATA_PROFILE_AGG_FILE_PROCESSED="integrated-data-aggregated.csv"
SUFFIX_DATA_PROFILE_CONT_BE_FILE_PROCESSED="integrated-data-contributors-belgian.csv"
SUFFIX_DATA_PROFILE_CONT_ALL_FILE_PROCESSED="integrated-data-contributors-all.csv"
SUFFIX_DATA_PROFILE_SOURCE_STATS="source-translation-stats.csv"
SUFFIX_DATA_PROFILE_EXCEL_DATA="corpus-data.xlsx"
SUFFIX_DATA_PROFILE_EXCEL_STATS="corpus-stats.xlsx"
SUFFIX_DATA_PROFILE_KBCODE="kbcode-hierarchy"

SUFFIX_PLACE_OF_PUBLICATION_GEONAMES="place-of-publications-geonames.csv"
SUFFIX_UNKNOWN_GEONAMES_MAPPING="missing-geonames-mapping.csv"

#
# Filenames used within an integration directory 
# (will be produced by the extraction phase
# such that the transform phase can pick it up)
#
# DATA SOURCE - KBR TRANSLATIONS
#
SUFFIX_KBR_TRL_NL_CLEANED="nl-translations-cleaned.xml"
SUFFIX_KBR_TRL_NL_WORKS="nl-translations-works.csv"
SUFFIX_KBR_TRL_NL_CONT="nl-translations-contributors.csv"
SUFFIX_KBR_TRL_NL_CONT_REPLACE="nl-translations-contributors-replaced.csv"
SUFFIX_KBR_TRL_NL_CONT_DEDUP="nl-translations-contributors-deduplicated.csv"
SUFFIX_KBR_TRL_NL_NEWAUT="nl-translations-identified-authorities.csv"
SUFFIX_KBR_TRL_NL_BB="nl-translations-bb.csv"
SUFFIX_KBR_TRL_NL_PUB_COUNTRY="nl-translations-pub-country.csv"
SUFFIX_KBR_TRL_NL_PUB_PLACE="nl-translations-pub-place.csv"
SUFFIX_KBR_TRL_NL_COL_LINKS="nl-collection-links.csv"
SUFFIX_KBR_TRL_FR_CLEANED="fr-translations-cleaned.xml"
SUFFIX_KBR_TRL_FR_WORKS="fr-translations-works.csv"
SUFFIX_KBR_TRL_FR_CONT="fr-translations-contributors.csv"
SUFFIX_KBR_TRL_FR_CONT_REPLACE="fr-translations-contributors-replaced.csv"
SUFFIX_KBR_TRL_FR_CONT_DEDUP="fr-translations-contributors-deduplicated.csv"
SUFFIX_KBR_TRL_FR_NEWAUT="fr-translations-identified-authorities.csv"
SUFFIX_KBR_TRL_FR_BB="fr-translations-bb.csv"
SUFFIX_KBR_TRL_FR_PUB_COUNTRY="fr-translations-pub-country.csv"
SUFFIX_KBR_TRL_FR_PUB_PLACE="fr-translations-pub-place.csv"
SUFFIX_KBR_TRL_FR_COL_LINKS="fr-collection-links.csv"


SUFFIX_KBR_TRL_NL_ISBN10="nl-fr-isbn10.csv"
SUFFIX_KBR_TRL_NL_ISBN13="nl-fr-isbn13.csv"
SUFFIX_KBR_TRL_FR_ISBN10="fr-nl-isbn10.csv"
SUFFIX_KBR_TRL_FR_ISBN13="fr-nl-isbn13.csv"

SUFFIX_KBR_LA_PLACES_VLG="publisher-places-VLG.csv"
SUFFIX_KBR_LA_PLACES_WAL="publisher-places-WAL.csv"
SUFFIX_KBR_LA_PLACES_BRU="publisher-places-BRU.csv"

# DATA SOURCE - KBR LINKED AUTHORITIES
#
SUFFIX_KBR_LA_PERSONS_NL_CLEANED="nl-translations-linked-authorities-persons-cleaned.csv"
SUFFIX_KBR_LA_ORGS_NL_CLEANED="nl-translations-linked-authorities-orgs-cleaned.csv"
SUFFIX_KBR_LA_PERSONS_FR_CLEANED="fr-translations-linked-authorities-persons-cleaned.csv"
SUFFIX_KBR_LA_ORGS_FR_CLEANED="fr-translations-linked-authorities-orgs-cleaned.csv"

SUFFIX_KBR_LA_PERSONS_NL_NORM="nl-translations-linked-authorities-persons-norm.csv"
SUFFIX_KBR_LA_ORGS_NL_NORM="nl-translations-linked-authorities-orgs-norm.csv"
SUFFIX_KBR_LA_PERSONS_FR_NORM="fr-translations-linked-authorities-persons-norm.csv"
SUFFIX_KBR_LA_ORGS_FR_NORM="fr-translations-linked-authorities-orgs-norm.csv"
SUFFIX_KBR_LA_PERSONS_FR_NAT="fr-translations-linked-authorities-nationalities.csv"
SUFFIX_KBR_LA_PERSONS_NL_NAT="nl-translations-linked-authorities-nationalities.csv"

SUFFIX_KBR_BELGIANS_CSV="kbr-belgians.csv"
SUFFIX_KBR_BELGIANS_NATIONALITIES="kbr-belgians-nationalities.csv"


# DATA SOURCE - KBR ORIGINALS MATCHING
#

SUFFIX_KBR_TITLE_MATCHES_NL_FR="title-matches_nl-fr.csv"
SUFFIX_KBR_TITLE_DUPLICATES_MATCHES_NL_FR="title-duplicates-matches_nl-fr.csv"
SUFFIX_KBR_SIMILARITY_MATCHES_NL_FR="similarity-matches_nl-fr.csv"
SUFFIX_KBR_SIMILARITY_DUPLICATES_MATCHES_NL_FR="similarity-duplicates-matches_nl-fr.csv"
SUFFIX_KBR_SIMILARITY_MULTIPLE_MATCHES_NL_FR="similarity-multiple-matches-nl-fr.csv"

SUFFIX_KBR_TITLE_MATCHES_FR_NL="title-matches_fr-nl.csv"
SUFFIX_KBR_TITLE_DUPLICATES_MATCHES_FR_NL="title-duplicates-matches_fr-nl.csv"
SUFFIX_KBR_SIMILARITY_MATCHES_FR_NL="similarity-matches_fr-nl.csv"
SUFFIX_KBR_SIMILARITY_DUPLICATES_MATCHES_FR_NL="similarity-duplicates-matches_fr-nl.csv"
SUFFIX_KBR_SIMILARITY_MULTIPLE_MATCHES_FR_NL="similarity-multiple-matches_fr-nl.csv"

# DATA SOURCE - KBR BELGIANS
#
SUFFIX_KBR_BELGIANS_CLEANED="belgians-cleaned.csv"
SUFFIX_KBR_BELGIANS_NORM="belgians-norm.csv"

# DATA SOURCE - KB
#
SUFFIX_KB_TRL_FR_NL="kb-translations-fr-nl.csv"
SUFFIX_KB_TRL_NL_FR="kb-translations-nl-fr.csv"
SUFFIX_KB_CONT_PERSONS_FR_NL="kb-contributors-persons-fr-nl.csv"
SUFFIX_KB_CONT_PERSONS_NL_FR="kb-contributors-persons-nl-fr.csv"
SUFFIX_KB_CONT_ORGS_FR_NL="kb-contributors-orgs-fr-nl.csv"
SUFFIX_KB_CONT_ORGS_NL_FR="kb-contributors-orgs-nl-fr.csv"
SUFFIX_KB_AUT_PERSONS_FR_NL="kb-authors-persons-fr-nl.csv"
SUFFIX_KB_AUT_PERSONS_NL_FR="kb-authors-persons-nl-fr.csv"
SUFFIX_KB_AUT_ORGS_FR_NL="kb-authors-orgs-fr-nl.csv"
SUFFIX_KB_AUT_ORGS_NL_FR="kb-authors-orgs-nl-fr.csv"
SUFFIX_KB_TRL_PBL_NAMES_FR_NL="kb-publisher-names-fr-nl"
SUFFIX_KB_TRL_PBL_NAMES_NL_FR="kb-publisher-names-nl-fr"

SUFFIX_KB_PBL_IDENTIFIERS_FR_NL="kb-publishers-identifiers-fr-nl"
SUFFIX_KB_PBL_IDENTIFIERS_NL_FR="kb-publishers-identifiers-nl-fr"

SUFFIX_KB_TRL_ISBN_NL_FR="kb-translations-with-formatted-isbn-nl-fr.csv"
SUFFIX_KB_TRL_ISBN_FR_NL="kb-translations-with-formatted-isbn-fr-nl.csv"

SUFFIX_KB_KBCODE_FR_NL="kbcode-assignments-fr-nl.csv"
SUFFIX_KB_KBCODE_NL_FR="kbcode-assignments-nl-fr.csv"

GET_KB_TRL_FR_NL_QUERY_FILE="../data-sources/kb/extract-kb-manifestations-fr-nl.sparql"
GET_KB_TRL_NL_FR_QUERY_FILE="../data-sources/kb/extract-kb-manifestations-nl-fr.sparql"
GET_KB_KBCODE_FR_NL_QUERY_FILE="../data-sources/kb/extract-kb-kbcode-fr-nl.sparql"
GET_KB_KBCODE_NL_FR_QUERY_FILE="../data-sources/kb/extract-kb-kbcode-nl-fr.sparql"
GET_KB_CONT_PERSONS_FR_NL_QUERY_FILE="../data-sources/kb/extract-kb-contributors-persons-fr-nl.sparql"
GET_KB_CONT_PERSONS_NL_FR_QUERY_FILE="../data-sources/kb/extract-kb-contributors-persons-nl-fr.sparql"
GET_KB_CONT_ORGS_FR_NL_QUERY_FILE="../data-sources/kb/extract-kb-contributors-orgs-fr-nl.sparql"
GET_KB_CONT_ORGS_NL_FR_QUERY_FILE="../data-sources/kb/extract-kb-contributors-orgs-nl-fr.sparql"
GET_KB_AUT_PERSONS_FR_NL_QUERY_FILE="../data-sources/kb/extract-kb-authors-persons-fr-nl.sparql"
GET_KB_AUT_PERSONS_NL_FR_QUERY_FILE="../data-sources/kb/extract-kb-authors-persons-nl-fr.sparql"
GET_KB_AUT_ORGS_FR_NL_QUERY_FILE="../data-sources/kb/extract-kb-authors-orgs-fr-nl.sparql"
GET_KB_AUT_ORGS_NL_FR_QUERY_FILE="../data-sources/kb/extract-kb-authors-orgs-nl-fr.sparql"

INSERT_KBCODE_QUERY_FILE="../data-sources/kb/insert-kbcode-hierarchy.sparql"

# DATA SOURCE - BNF
#
SUFFIX_BNF_BELGIANS_IDS="bnf-belgian-contributor-ids.csv"
SUFFIX_BNF_BELGIAN_PUBS_IDS="bnf-belgian-contributor-publication-ids.csv"
SUFFIX_BNF_TRL_CONT_ORGS_IDS="bnf-translation-contributor-orgs-ids.csv"
SUFFIX_BNF_TRL_CONT_IDS="bnf-translation-contributor-persons-ids.csv"
SUFFIX_BNF_TRL_IDS_FR_NL="bnf-translation-ids-fr-nl.csv"
SUFFIX_BNF_TRL_IDS_NL_FR="bnf-translation-ids-nl-fr.csv"
SUFFIX_BNF_TRL_IDS="bnf-translation-ids.csv"

SUFFIX_BNF_ISBN10_ISBN13_CSV="bnf-isbn10-isbn13.csv"
SUFFIX_BNF_ISBN10_ISBN13_ENRICHED_CSV="bnf-isbn10-isbn13-enriched.ttl"
SUFFIX_BNF_ISBN13_NO_HYPHEN_CSV="bnf-records-no-isbn13-hyphen.csv"
SUFFIX_BNF_ISBN13_FIXED_CSV="bnf-records-fixed-isbn13.csv"
SUFFIX_BNF_ISBN13_HYPHEN_NT="bnf-fixed-isbn13.nt"

SUFFIX_BNF_ISBN10_NO_HYPHEN_CSV="bnf-records-no-isbn10-hyphen.csv"
SUFFIX_BNF_ISBN10_FIXED_CSV="bnf-records-fixed-isbn10.csv"
SUFFIX_BNF_ISBN10_HYPHEN_NT="bnf-fixed-isbn10.nt"
  
# DATA SOURCE - MASTER DATA
#
SUFFIX_MASTER_MARC_ROLES="marc-roles.csv"
SUFFIX_MASTER_BINDING_TYPES="binding-types.csv"
SUFFIX_MASTER_COUNTRIES="countries.nt"
SUFFIX_MASTER_LANGUAGES="languages.nt"
SUFFIX_MASTER_GENDER="gender.ttl"
SUFFIX_MASTER_THES_EN="thesaurus-belgian-bibliography-en-hierarchy.csv"
SUFFIX_MASTER_THES_NL="thesaurus-belgian-bibliography-nl-hierarchy.csv"
SUFFIX_MASTER_THES_FR="thesaurus-belgian-bibliography-fr-hierarchy.csv"

# DATA SOURCE - WIKIDATA
#
SUFFIX_WIKIDATA_ENRICHED="manually-enriched-wikidata.csv"

# DATA SOURCE - BNFISNI enrichment
#
SUFFIX_BNFISNI_IDENTIFIERS_ISNI="isni-identifiers-without-nationality.csv"
SUFFIX_BNFISNI_CONFIG_ISNI_EXTRACTION="config-bnf-isni-extraction.csv"
SUFFIX_BNFISNI_IDENTIFIERS_BNF="bnf-identifiers.csv"
SUFFIX_BNFISNI_CONT_LD="bnf-data-of-missing-nationalities.xml"

#
# LINKED DATA - KBR TRANSLATIONS
#
SUFFIX_KBR_BOOK_LD="book-data-and-contributions.ttl"
SUFFIX_KBR_TRL_LD="translation-data.ttl"
SUFFIX_KBR_TRL_LIMITED_ORIG_LD="limited-info-originals.ttl"
SUFFIX_KBR_NEWAUT_LD="translations-identified-authorities.ttl"
SUFFIX_KBR_TRL_BB_LD="translations-bb.ttl"
SUFFIX_KBR_TRL_PUB_COUNTRY_LD="translations-publication-countries.ttl"
SUFFIX_KBR_TRL_PUB_PLACE_LD="translations-publication-places.ttl"
SUFFIX_KBR_TRL_ISBN_LD="translations-isbn.ttl"

#
# LINKED DATA - KBR ORIGINAL LINKS
#
SUFFIX_KBR_ORIGINAL_LINKING_LD="translations-original-links.ttl"

#
# LINKED DATA - KBR LINKED AUTHORITIES
#
SUFFIX_KBR_PERSONS_FR_NL_LD="fr-nl_persons.ttl"
SUFFIX_KBR_PERSONS_NL_FR_LD="nl-fr_persons.ttl"
SUFFIX_KBR_ORGS_FR_NL_LD="fr-nl_organizations.ttl"
SUFFIX_KBR_ORGS_NL_FR_LD="nl-fr_organizations.ttl"
SUFFIX_KBR_PLACES_LD="places.ttl"
SUFFIX_KBR_BELGIANS_LD="belgians.ttl"
SUFFIX_KBR_PERSONS_IDENTIFIERS_FR_NL_LD="fr-nl_persons-identifiers.ttl"
SUFFIX_KBR_PERSONS_IDENTIFIERS_NL_FR_LD="nl-fr_persons-identifiers.ttl"
SUFFIX_KBR_ORGS_IDENTIFIERS_FR_NL_LD="fr-nl_orgs-identifiers.ttl"
SUFFIX_KBR_ORGS_IDENTIFIERS_NL_FR_LD="nl-fr_orgs-identifiers.ttl"
SUFFIX_KBR_BELGIANS_IDENTIFIERS_LD="belgians-identifiers.ttl"

#
# LINKED DATA - KB
#
SUFFIX_KB_TRL_LD="kb-translations.ttl"
SUFFIX_KB_LA_LD="kb-linked-authorities.ttl"
SUFFIX_KB_TRL_ORIG_LD="kb-limited-originals.ttl"

SUFFIX_KB_PBL_FR_NL_LD="kb-publisher-data-fr-nl.xml"
SUFFIX_KB_PBL_NL_FR_LD="kb-publisher-data-nl-fr.xml"

#
# LINKED DATA - KBR BELGIANS
#
SUFFIX_KBR_BELGIANS_LD="belgians.ttl"

#
# LINKED DATA - BNF
#
SUFFIX_BNF_TRL_FR_NL_LD="fr_nl-translations.xml"
SUFFIX_BNF_TRL_NL_FR_LD="nl_fr-translations.xml"

SUFFIX_BNF_CONT_LD="bnf-contributors-persons.xml"
SUFFIX_BNF_CONT_ORGS_LD="bnf-contributors-orgs.xml"
SUFFIX_BNF_TRL_CONT_LINKS_LD="bnf-editions-contributor-links.xml"
SUFFIX_BNF_CONT_ISNI_LD="bnf-contributor-isni.xml"
SUFFIX_BNF_CONT_VIAF_LD="bnf-contributor-viaf.xml"
SUFFIX_BNF_CONT_WIKIDATA_LD="bnf-contributor-wikidata.xml"


#
# LINKED DATA - MASTER DATA
#
SUFFIX_MASTER_LD="master-data.ttl"

#
# LINKED DATA - WIKIDATA
#
SUFFIX_WIKIDATA_LD="from-manually-enriched-wikidata.ttl"

# -----------------------------------------------------------------------------
function extract {

  local dataSource=$1
  local integrationFolderName=$2

  #
  # If we already integrated data source B, and then want to include data source A it doesn't work
  # thus we should not check if the folder already exists
  # if [ -d "$integrationFolderName" ];
  # then
  #   echo "the specified integration folder already exists, please provide the name of a new folder"
  #   exit 1
  # fi

  if [ "$dataSource" = "kbr" ];
  then
    extractKBR $integrationFolderName
  elif [ "$dataSource" = "kbr-originals" ];
  then
    extractKBROriginals $integrationFolderName
  elif [ "$dataSource" = "master-data" ];
  then
    extractMasterData $integrationFolderName
  elif [ "$dataSource" = "bnf" ];
  then
    extractBnF $integrationFolderName
  elif [ "$dataSource" = "kb" ];
  then
    extractKB $integrationFolderName
  elif [ "$dataSource" = "kbcode" ];
  then
    extractKBCode $integrationFolderName
  elif [ "$dataSource" = "wikidata" ];
  then
    extractWikidata $integrationFolderName
  elif [ "$dataSource" = "original-links-kbr" ];
  then
    extractOriginalLinksKBR $integrationFolderName "original-links-kbr" "kbr" "kbr-originals"
  elif [ "$dataSource" = "bnfisni" ];
  then
    extractNationalityFromBnFViaISNI $integrationFolderName
  elif [ "$dataSource" = "all" ];
  then
    extractKBR $integrationFolderName
    extractKBROriginals $integrationFolderName
    extractKB $integrationFolderName
    extractBnF $integrationFolderName
    extractMasterData $integrationFolderName
    extractWikidata $integrationFolderName
    extractNationalityFromBnFViaISNI $integrationFolderName
  fi
  
}

# -----------------------------------------------------------------------------
function transform {

  local dataSource=$1
  local integrationFolderName=$2

  folderHasToExist $integrationFolderName

  if [ "$dataSource" = "kbr" ];
  then
    transformKBR $integrationFolderName
  elif [ "$dataSource" = "kbr-originals" ];
  then
    transformKBROriginals $integrationFolderName
  elif [ "$dataSource" = "master-data" ];
  then
    transformMasterData $integrationFolderName
  elif [ "$dataSource" = "bnf" ];
  then
    transformBnF $integrationFolderName
  elif [ "$dataSource" = "kb" ];
  then
    transformKB $integrationFolderName
  elif [ "$dataSource" = "wikidata" ];
  then
    transformWikidata $integrationFolderName
  elif [ "$dataSource" = "original-links-kbr" ];
  then
    transformOriginalLinksKBR $integrationFolderName "original-links-kbr"
  elif [ "$dataSource" = "bnfisni" ];
  then
    transformNationalityFromBnFViaISNI $integrationFolderName
  elif [ "$dataSource" = "all" ];
  then
    transformKBR $integrationFolderName
    transformKBROriginals $integrationFolderName
    transformKB $integrationFolderName
    transformBnF $integrationFolderName
    transformMasterData $integrationFolderName
    transformWikidata $integrationFolderName
    transformNationalityFromBnFViaISNI $integrationFolderName
  fi
  
}

# -----------------------------------------------------------------------------
function load {

  local dataSource=$1
  local integrationFolderName=$2

  folderHasToExist $integrationFolderName

  if [ "$dataSource" = "kbr" ];
  then
    loadKBR $integrationFolderName
  elif [ "$dataSource" = "kbr-originals" ];
  then
    loadKBROriginals $integrationFolderName
  elif [ "$dataSource" = "master-data" ];
  then
    loadMasterData $integrationFolderName
  elif [ "$dataSource" = "bnf" ];
  then
    loadBnF $integrationFolderName
  elif [ "$dataSource" = "kb" ];
  then
    loadKB $integrationFolderName
  elif [ "$dataSource" = "wikidata" ];
  then
    loadWikidata $integrationFolderName
  elif [ "$dataSource" = "original-links-kbr" ];
  then
    loadOriginalLinksKBR $integrationFolderName "original-links-kbr"
  elif [ "$dataSource" = "bnfisni" ];
  then
    loadNationalityFromBnFViaISNI $integrationFolderName
  elif [ "$dataSource" = "all" ];
  then
    loadMasterData $integrationFolderName
    loadBnF $integrationFolderName
    loadKBR $integrationFolderName
    loadKB $integrationFolderName
    loadWikidata $integrationFolderName
    loadNationalityFromBnFViaISNI $integrationFolderName
  fi

}

# -----------------------------------------------------------------------------
function integrate {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  createManifestationsQueries="config-integration-manifestations-create.csv"
  createContributorsQueries="config-integration-contributors-create.csv"
  updateManifestationsQueries="config-integration-manifestations-update.csv"
  updateContributorsQueries="config-integration-contributors-update.csv"

  integrationNamespace="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  # first delete content of the named graph in case it already exists
  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_INT_TRL>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_INT_TRL"

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_INT_CONT>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_INT_CONT"

  source ./py-integration-env/bin/activate
  echo "Integrate manifestations ..."
  python $SCRIPT_INTERLINK_DATA -u "$integrationNamespace" --query-type "manifestations" --target-graph "$TRIPLE_STORE_GRAPH_INT_TRL" \
    --create-queries $createManifestationsQueries --update-queries $updateManifestationsQueries --number-updates 2

  echo "Integrate contributors ..."
  python $SCRIPT_INTERLINK_DATA -u "$integrationNamespace" --query-type "contributors" --target-graph "$TRIPLE_STORE_GRAPH_INT_CONT" \
    --create-queries $createContributorsQueries --update-queries $updateContributorsQueries --number-updates 3

  echo "Establish links between integrated manifestations and contributors (authors, translators, illustrators, scenarists and publishing directors) ..."

  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" \
    "$LINK_QUERY_CONT_AUTHORS" "$LINK_QUERY_CONT_TRANSLATORS" "$LINK_QUERY_CONT_ILLUSTRATORS" \
    "$LINK_QUERY_CONT_SCENARISTS" "$LINK_QUERY_CONT_PUBLISHING_DIRECTORS"

}

# -----------------------------------------------------------------------------
function query {
  local integrationName=$1

  mkdir -p $integrationName/csv
  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  queryFileAgg="$DATA_PROFILE_QUERY_FILE_AGG"
  queryFileContPersons="$DATA_PROFILE_QUERY_FILE_CONT_PERSONS"
  queryFileContOrgs="$DATA_PROFILE_QUERY_FILE_CONT_ORGS"
  queryFileKBCode="$GET_KBCODE_HIERARCHY_INFO_QUERY_FILE"

  outputFileAgg="$integrationName/csv/$SUFFIX_DATA_PROFILE_FILE_ALL"

  # persons will be "all data" as it contains several birth and death dates, it will be filtered in the postprocessing
  outputFileContPersonsAllData="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_PERSONS_ALL_DATA_FILE"
  outputFileContOrgs="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_ORGS_FILE"

  outputFileKBCode="$integrationName/csv/$SUFFIX_DATA_PROFILE_KBCODE"

  echo "Creating the dataprofile CSV file ..."
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$queryFileAgg" "$ENV_SPARQL_ENDPOINT" "$outputFileAgg"

  echo "Creating the contributor persons CSV file ..."
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$queryFileContPersons" "$ENV_SPARQL_ENDPOINT" "$outputFileContPersonsAllData"

  echo "Creating the contributor orgs CSV file ..."
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$queryFileContOrgs" "$ENV_SPARQL_ENDPOINT" "$outputFileContOrgs"

  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$queryFileKBCode" "$ENV_SPARQL_ENDPOINT" "$outputFileKBCode"

}

# -----------------------------------------------------------------------------
function postprocess {
  local integrationName=$1

  integratedAllData="$integrationName/csv/$SUFFIX_DATA_PROFILE_FILE_ALL"
  integratedData="$integrationName/csv/$SUFFIX_DATA_PROFILE_FILE_PROCESSED"
  integratedDataEnriched="$integrationName/csv/$SUFFIX_DATA_PROFILE_FILE_ENRICHED"
  placeOfPublicationsGeonames="$integrationName/csv/$SUFFIX_PLACE_OF_PUBLICATION_GEONAMES"
  unknownGeonamesMapping="$SUFFIX_UNKNOWN_GEONAMES_MAPPING"
  contributorsPersonsAllData="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_PERSONS_ALL_DATA_FILE"
  contributorsPersons="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_PERSONS_FILE"
  allPersons="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_ALL_PERSONS"
  tmp1="$integrationName/csv/kbr-enriched-not-yet-bnf-and-kb.csv"
  tmp2="$integrationName/csv/kbr-and-bnf-enriched-not-yet-kb.csv"

  contributorsOrgs="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_ORGS_FILE"

  kbCodeHierarchy="$integrationName/csv/$SUFFIX_DATA_PROFILE_KBCODE"

  excelData="$integrationName/$SUFFIX_DATA_PROFILE_EXCEL_DATA"

  source ./py-integration-env/bin/activate


  echo "Derive missing country names from place names - KBR ..."
  time python $SCRIPT_POSTPROCESS_DERIVE_COUNTRIES -i $integratedAllData -o $tmp1 -g geonames/ -c targetCountryOfPublicationKBR -p targetPlaceOfPublicationKBR

  echo "Derive missing country names from place names - BnF ..."
  time python $SCRIPT_POSTPROCESS_DERIVE_COUNTRIES -i $tmp1 -o $tmp2 -g geonames/ -c targetCountryOfPublicationBnF -p targetPlaceOfPublicationBnF

  echo "Derive missing country names from place names - KB ..."
  time python $SCRIPT_POSTPROCESS_DERIVE_COUNTRIES -i $tmp2 -o $integratedData -g geonames/ -c targetCountryOfPublicationKB -p targetPlaceOfPublicationKB

  echo "Postprocess manifestation data ..."
  time python $SCRIPT_POSTPROCESS_AGG_QUERY_RESULT -i $integratedData -o $integratedDataEnriched

  echo "Create geonames relationships for place of publications ..."
  time python $SCRIPT_POSTPROCESS_GET_GEONAME_PLACE_OF_PUBLICATION -i $integratedDataEnriched -m $unknownGeonamesMapping -g geonames/ -p targetPlaceOfPublication -o $placeOfPublicationsGeonames

  echo "Postprocess contributor data ..."
  time python $SCRIPT_POSTPROCESS_QUERY_CONT_RESULT -c $contributorsPersonsAllData -m $integratedDataEnriched -o $contributorsPersons

  echo "Postprocess contributor data ..."
  time python $SCRIPT_POSTPROCESS_QUERY_CONT_RESULT -c $contributorsPersonsAllData -m $integratedDataEnriched -o $allPersons --keep-non-contributors

  echo "Create Excel sheet for data ..."
  time python $SCRIPT_CSV_TO_EXCEL $integratedDataEnriched $contributorsPersons $contributorsOrgs $placeOfPublicationsGeonames $allPersons $kbCodeHierarchy -s "translations" -s "person contributors" -s "org contributors" -s "geonames" -s "all persons" -s "KBCode" -o $excelData

}

# -----------------------------------------------------------------------------
function folderHasToExist {
  if [ ! -d "$1" ];
  then
    echo "the specified integration folder does not exist, what should be transformed? Please provide the command 'etl' or 'et' to also execute the extraction phase."
    exit 1
  fi
}

# -----------------------------------------------------------------------------
function extractKBR {

  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # create the folders to place the extracted translations and agents
  mkdir -p $integrationName/kbr/book-data-and-contributions
  mkdir -p $integrationName/kbr/agents

  echo "EXTRACTION - Extract and clean KBR translations data"
  extractKBRTranslationsAndContributions "$integrationName" "kbr" "$INPUT_KBR_TRL_NL" "$INPUT_KBR_TRL_FR"

  echo "EXTRACTION - Extract and clean KBR linked authorities data"
  extractKBRLinkedAuthorities "$integrationName" "$INPUT_KBR_LA_PERSON_NL" "$INPUT_KBR_LA_ORG_NL" "$INPUT_KBR_LA_PERSON_FR" "$INPUT_KBR_LA_ORG_FR" "$INPUT_KBR_BELGIANS"

}

# -----------------------------------------------------------------------------
function extractKBROriginals {

  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)
  local dataSourceName="kbr-originals"

  # create the folders to place the extracted translations and agents
  mkdir -p $integrationName/$dataSourceName/book-data-and-contributions
  mkdir -p $integrationName/$dataSourceName/agents

  echo "EXTRACTION - Extract and clean KBR originals translations data"
  extractKBRTranslationsAndContributions "$integrationName" "$dataSourceName" "$INPUT_KBR_TRL_ORIG_NL_FR" "$INPUT_KBR_TRL_ORIG_FR_NL"

  # there is no linked authorities export
}

# -----------------------------------------------------------------------------
function extractKB {

  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # create the folders to place the extracted translations and agents
  mkdir -p $integrationName/kb/translations
  mkdir -p $integrationName/kb/agents

  #printf "\nUsed input (KB translations and contributors)\n* $kbrDutchTranslations\n* $kbrFrenchTranslations" >> "$integrationName/kb/README.md"

  #
  # Define file names based on current integration directory and file name patterns
  #
  kbTranslationsFRNL="$integrationName/kb/translations/$SUFFIX_KB_TRL_FR_NL"
  kbTranslationsNLFR="$integrationName/kb/translations/$SUFFIX_KB_TRL_NL_FR"
  kbContributorsPersonsFRNL="$integrationName/kb/agents/$SUFFIX_KB_CONT_PERSONS_FR_NL"
  kbContributorsPersonsNLFR="$integrationName/kb/agents/$SUFFIX_KB_CONT_PERSONS_NL_FR"
  kbContributorsOrgsFRNL="$integrationName/kb/agents/$SUFFIX_KB_CONT_ORGS_FR_NL"
  kbContributorsOrgsNLFR="$integrationName/kb/agents/$SUFFIX_KB_CONT_ORGS_NL_FR"
  kbAuthorsPersonsFRNL="$integrationName/kb/agents/$SUFFIX_KB_AUT_PERSONS_FR_NL"
  kbAuthorsPersonsNLFR="$integrationName/kb/agents/$SUFFIX_KB_AUT_PERSONS_NL_FR"
  kbAuthorsOrgsFRNL="$integrationName/kb/agents/$SUFFIX_KB_AUT_ORGS_FR_NL"
  kbAuthorsOrgsNLFR="$integrationName/kb/agents/$SUFFIX_KB_AUT_ORGS_NL_FR"

  kbCodeAssignmentsFRNL="$integrationName/kb/translations/$SUFFIX_KB_KBCODE_FR_NL"
  kbCodeAssignmentsNLFR="$integrationName/kb/translations/$SUFFIX_KB_KBCODE_NL_FR"

  kbTranslationsWithISBNFRNL="$integrationName/kb/translations/$SUFFIX_KB_TRL_ISBN_FR_NL"
  kbTranslationsWithISBNNLFR="$integrationName/kb/translations/$SUFFIX_KB_TRL_ISBN_NL_FR"

  kbTranslationsPublishersFRNL="$integrationName/kb/agents/$SUFFIX_KB_TRL_PBL_NAMES_FR_NL"
  kbTranslationsPublishersNLFR="$integrationName/kb/agents/$SUFFIX_KB_TRL_PBL_NAMES_NL_FR"

  kbPublisherIdentifiersFRNL="$integrationName/kb/agents/$SUFFIX_KB_PBL_IDENTIFIERS_FR_NL"
  kbPublisherIdentifiersNLFR="$integrationName/kb/agents/$SUFFIX_KB_PBL_IDENTIFIERS_NL_FR"
  kbPublisherDataFRNL="$integrationName/kb/rdf/$SUFFIX_KB_PBL_FR_NL_LD"
  kbPublisherDataNLFR="$integrationName/kb/rdf/$SUFFIX_KB_PBL_NL_FR_LD"

  source py-integration-env/bin/activate

  echo "EXTRACTION - Extract KB translations FR - NL"
  #queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_TRL_FR_NL_QUERY_FILE" "$kbTranslationsFRNL"

  echo "EXTRACTION - Extract KB translations NL - FR"
  #queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_TRL_NL_FR_QUERY_FILE" "$kbTranslationsNLFR"

  echo "EXTRACTION - Compute formatted ISBN10 and ISBN13 identifiers FR - NL"
  #time python $SCRIPT_ADD_ISBN_10_13 -i $kbTranslationsFRNL -o $kbTranslationsWithISBNFRNL

  echo "EXTRACTION - Compute formatted ISBN10 and ISBN13 identifiers NL - FR"
  #time python $SCRIPT_ADD_ISBN_10_13 -i $kbTranslationsNLFR -o $kbTranslationsWithISBNNLFR


  echo "EXTRACTION - Extract KB translation contributors persons FR - NL"
  #queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_CONT_PERSONS_FR_NL_QUERY_FILE" "$kbContributorsPersonsFRNL"

  echo "EXTRACTION - Extract KB translation contributors persons NL - FR"
  #queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_CONT_PERSONS_NL_FR_QUERY_FILE" "$kbContributorsPersonsNLFR"

  echo "EXTRACTION - Extract KB translation authors persons FR - NL"
  #queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_AUT_PERSONS_FR_NL_QUERY_FILE" "$kbAuthorsPersonsFRNL"

  echo "EXTRACTION - Extract KB translation authors persons NL - FR"
  #queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_AUT_PERSONS_NL_FR_QUERY_FILE" "$kbAuthorsPersonsNLFR"


  echo "EXTRACTION - Extract KB translation contributors orgs FR - NL"
  #queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_CONT_ORGS_FR_NL_QUERY_FILE" "$kbContributorsOrgsFRNL"

  echo "EXTRACTION - Extract KB translation contributors orgs NL - FR"
  #queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_CONT_ORGS_NL_FR_QUERY_FILE" "$kbContributorsOrgsNLFR"

  echo "EXTRACTION - Extract KB translation authors orgs FR - NL"
  #queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_AUT_ORGS_FR_NL_QUERY_FILE" "$kbAuthorsOrgsFRNL"

  echo "EXTRACTION - Extract KB translation authors orgs NL - FR"
  #queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_AUT_ORGS_NL_FR_QUERY_FILE" "$kbAuthorsOrgsNLFR"


  echo "EXTRACTION - Extract KBCode classifications FR-NL"
  #queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_KBCODE_FR_NL_QUERY_FILE" "$kbCodeAssignmentsFRNL"

  echo "EXTRACTION - Extract KBCode classifications NL-FR"
  #queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_KBCODE_NL_FR_QUERY_FILE" "$kbCodeAssignmentsNLFR"

  echo "EXTRACTION - Extract publisher names from publications NL-FR"
  python -m $MODULE_EXTRACT_COLUMNS -i "$kbTranslationsNLFR" -o "$kbTranslationsPublishersNLFR" -c "publisherName"

  echo "EXTRACTION - Extract publisher names from publications FR-NL"
  python -m $MODULE_EXTRACT_COLUMNS -i "$kbTranslationsFRNL" -o "$kbTranslationsPublishersFRNL" -c "publisherName"

  echo "EXTRACTION - Extract publisher identifiers based on names FR-NL"
  python -m $MODULE_GET_RDF_XML_SUBJECTS -i $INPUT_KB_ORGS_DIR -p "schema:name" -l "$kbTranslationsPublishersFRNL" -o "$kbPublisherIdentifiersFRNL" --subject-tag "schema:Organization"

  echo "EXTRACTION - Extract publisher identifiers based on names NL-FR"
  python -m $MODULE_GET_RDF_XML_SUBJECTS -i $INPUT_KB_ORGS_DIR -p "schema:name" -l "$kbTranslationsPublishersNLFR" -o "$kbPublisherIdentifiersNLFR" --subject-tag "schema:Organization"

  echo "EXTRACTION - Extract publisher records based on identifiers FR-NL"
  python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_KB_ORGS_DIR  -o $kbPublisherDataFRNL -f "$kbPublisherIdentifiersFRNL" --subject-tag "schema:Organization"

  echo "EXTRACTION - Extract publisher records based on identifiers NL-FR"
  python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_KB_ORGS_DIR  -o $kbPublisherDataNLFR -f "$kbPublisherIdentifiersNLFR" --subject-tag "schema:Organization"
  
}

# -----------------------------------------------------------------------------
function extractKBCode {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)
  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  echo "EXTRACT, TRANSFORM and LOAD the KBCode hierarchy with a federated SPARQL UPDATE query"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" "$INSERT_KBCODE_QUERY_FILE"
  
}

# -----------------------------------------------------------------------------
function extractBnF {

  local integrationName=$1

  mkdir -p $integrationName/bnf/translations
  mkdir -p $integrationName/bnf/agents
  mkdir -p $integrationName/bnf/rdf

  bnfBelgiansBELTRANS="$integrationName/bnf/agents/$SUFFIX_BNF_BELGIANS_IDS"
  bnfPersonsBELTRANS="$integrationName/bnf/agents/$SUFFIX_BNF_TRL_CONT_IDS"
  bnfOrgsBELTRANS="$integrationName/bnf/agents/$SUFFIX_BNF_TRL_CONT_ORGS_IDS"
  bnfNLFRTranslations="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_IDS_NL_FR"
  bnfFRNLTranslations="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_IDS_FR_NL"
  bnfBelgianPublications="$integrationName/bnf/translations/$SUFFIX_BNF_BELGIAN_PUBS_IDS"
  bnfTranslationIDs="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_IDS"

  bnfFRNLRelevantTranslationData="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_FR_NL_LD"
  bnfNLFRRelevantTranslationData="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_NL_FR_LD"
  bnfContributorDataPersons="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_LD"
  bnfContributorDataOrgs="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_ORGS_LD"
  bnfContributionLinksData="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_CONT_LINKS_LD"
  bnfContributorIsniData="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_ISNI_LD"
  bnfContributorVIAFData="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_VIAF_LD"
  bnfContributorWikidataData="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_WIKIDATA_LD"

  # get the IDs of BnF Belgians
  echo "EXTRACTION - Extract Belgian contributor IDs from BnF data"
  extractBnFBelgianContributors "$integrationName" "$INPUT_BNF_PERSON_AUTHORS" "$bnfBelgiansBELTRANS"

  # use the IDs of Belgians to get publication IDs with Belgian authors, illustrators or scenarists
  echo "EXTRACTION - Extract publication IDs of publications with Belgian contributors from BnF data"
  extractBnFBelgianPublications "$integrationName" "$INPUT_BNF_CONTRIBUTIONS" "$bnfBelgiansBELTRANS" "$bnfBelgianPublications"

  # get publicationIDs of a dump of publications which are known to be translations
  echo "EXTRACTION - Extract publication IDs of translations from BnF catalog export - NL-FR"
  extractBnFTranslations "$integrationName" "$INPUT_BNF_TRL_NL_FR" "$bnfNLFRTranslations" 

  echo "EXTRACTION - Extract publication IDs of translations from BnF catalog export - FR-NL"
  extractBnFTranslations "$integrationName" "$INPUT_BNF_TRL_FR_NL" "$bnfFRNLTranslations"


  # extract the actual data of translations with relevant Belgian contributors
  echo "EXTRACTION - Extract publication data about publications from BnF data - FR-NL"
  extractBnFRelevantPublicationData "$integrationName" "$INPUT_BNF_EDITIONS" "$bnfFRNLTranslations" "$bnfBelgianPublications" "$bnfFRNLRelevantTranslationData"

  echo "EXTRACTION - Extract publication data about publications from BnF data - NL-FR"
  extractBnFRelevantPublicationData "$integrationName" "$INPUT_BNF_EDITIONS" "$bnfNLFRTranslations" "$bnfBelgianPublications" "$bnfNLFRRelevantTranslationData"

  #
  # we also need related information of the identified publications from other data dumps
  #
  source py-integration-env/bin/activate

  echo "EXTRACTION - Create list of both NL and FR BnF translation IDs"
  time python $SCRIPT_UNION_IDS $bnfFRNLTranslations $bnfNLFRTranslations -o $bnfTranslationIDs -d ';'

  # extract contributor IDs of all translation contributors (also non-Belgian contributors)
  echo "EXTRACTION - Extract all BnF contributor IDs of BELTRANS translations (despite the nationality)"
  time python $SCRIPT_GET_RDF_XML_OBJECTS -i $INPUT_BNF_CONTRIBUTIONS -o $bnfPersonsBELTRANS -l $bnfTranslationIDs -p "dcterms:contributor"

  # extract contributor IDs of all translation contributors (orgs)
  echo "EXTRACTION - Extract all BnF contributor IDs of organizations"
  time python $SCRIPT_GET_RDF_XML_OBJECTS -i $INPUT_BNF_CONTRIBUTIONS -o $bnfOrgsBELTRANS -l $bnfTranslationIDs -p "marcrel:pbl"

  # extract the actual data of all BELTRANS translations contributors - persons
  echo "EXTRACTION - Extract BnF contributor data (persons)"
  time python $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_PERSON_AUTHORS -o $bnfContributorDataPersons -f $bnfPersonsBELTRANS

  # extract the actual data of all BELTRANS translations contributors - orgs
  echo "EXTRACTION - Extract BnF contributor data (orgs)"
  time python $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_ORG_AUTHORS -o $bnfContributorDataOrgs -f $bnfOrgsBELTRANS
  
  # extract the actual links between publications and contributors (not just looking up things) - ALL links are taken as the subject with all properties is extracted
  echo "EXTRACTION - Extract links between BELTRANS relevant BnF publications and BnF contributors"
  time python $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONTRIBUTIONS -o $bnfContributionLinksData -f $bnfBelgianPublications -f $bnfTranslationIDs

  echo "EXTRACTION - Extract links between BnF contributors and ISNI"
  time python $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_ISNI -o $bnfContributorIsniData -f $bnfPersonsBELTRANS

  echo "EXTRACTION - Extract links between BnF contributors and VIAF"
  time python $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_VIAF -o $bnfContributorVIAFData -f $bnfPersonsBELTRANS

  echo "EXTRACTION - Extract links between BnF contributors and Wikidata"
  time python $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_WIKIDATA -o $bnfContributorWikidataData -f $bnfPersonsBELTRANS
}

# -----------------------------------------------------------------------------
function extractNationalityFromBnFViaISNI {

  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  source ./py-integration-env/bin/activate

  mkdir -p $integrationName/bnfisni/agents
  mkdir -p $integrationName/bnfisni/rdf


  isniIdentifiers="$integrationName/bnfisni/agents/$SUFFIX_BNFISNI_IDENTIFIERS_ISNI"
  configISNIExtraction="$integrationName/bnfisni/agents/$SUFFIX_BNFISNI_CONFIG_ISNI_EXTRACTION"
  bnfIdentifiers="$integrationName/bnfisni/agents/$SUFFIX_BNFISNI_IDENTIFIERS_BNF"
  bnfContributorData="$integrationName/bnfisni/rdf/$SUFFIX_BNFISNI_CONT_LD"

  bnfContributorIsniData="$integrationName/bnfisni/rdf/$SUFFIX_BNF_CONT_ISNI_LD"
  bnfContributorVIAFData="$integrationName/bnfisni/rdf/$SUFFIX_BNF_CONT_VIAF_LD"
  bnfContributorWikidataData="$integrationName/bnfisni/rdf/$SUFFIX_BNF_CONT_WIKIDATA_LD"

  # Query ISNI identifiers with missing nationality information
  echo "EXTRACTION - Extract ISNI identifier with missing nationality information"
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$GET_MISSING_NATIONALITIES_ISNI_QUERY_FILE" "$ENV_SPARQL_ENDPOINT" "$isniIdentifiers"

  echo "EXTRACTION - Create configuration file for following step"
  echo "skos:exactMatch,inFile,$isniIdentifiers" > $configISNIExtraction

  # Extract BnF identifier from BnF dump via queried ISNI
  echo "EXTRACTION - Extract BnF identifier from BnF dump via queried ISNI"
  getSubjects "$INPUT_BNF_CONT_ISNI" "$configISNIExtraction" "$bnfIdentifiers"

  # Extract BnF contributor data via BnF identifier
  echo "EXTRACTION - Extract BnF contributor data via BnF identifier"
  time python $MODULE_FILTER_RDF_XML_SUBJECTS -i "$INPUT_BNF_PERSON_AUTHORS"  -o "$bnfContributorData" -f "$bnfIdentifiers"

  echo "EXTRACTION - Extract links between BnF contributors and ISNI"
  time python $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_ISNI -o $bnfContributorIsniData -f $bnfIdentifiers

  echo "EXTRACTION - Extract links between BnF contributors and VIAF"
  time python $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_VIAF -o $bnfContributorVIAFData -f $bnfIdentifiers

  echo "EXTRACTION - Extract links between BnF contributors and Wikidata"
  time python $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_WIKIDATA -o $bnfContributorWikidataData -f $bnfIdentifiers

  # We could query nationality which is used to immediately enrich integrated persons,
  # but we can also get all data of the newly found contributors to increase the overlap with other sources

}

# -----------------------------------------------------------------------------
function extractOriginalLinksKBR {
  local integrationName=$1
  local dataSourceName=$2
  local translationsSourceName=$3
  local originalsSourceName=$4

  mkdir -p $integrationName/$dataSourceName

  local similarityThreshold="0.9"

  local kbrOriginalsNLFR="$integrationName/$originalsSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_WORKS"
  local kbrTranslationsNLFR="$integrationName/$translationsSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_WORKS"
  local titleMatchesNLFR="$integrationName/$dataSourceName/$SUFFIX_KBR_TITLE_MATCHES_NL_FR"
  local titleDuplicatesMatchesNLFR="$integrationName/$dataSourceName/$SUFFIX_KBR_TITLE_DUPLICATES_MATCHES_NL_FR"
  local similarityMatchesNLFR="$integrationName/$dataSourceName/$SUFFIX_KBR_SIMILARITY_MATCHES_NL_FR"
  local similarityDuplicatesMatchesNLFR="$integrationName/$dataSourceName/$SUFFIX_KBR_SIMILARITY_DUPLICATES_MATCHES_NL_FR"
  local similarityMultipleMatchesNLFR="$integrationName/$dataSourceName/$SUFFIX_KBR_SIMILARITY_MULTIPLE_MATCHES_NL_FR"

  local kbrOriginalsFRNL="$integrationName/$originalsSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_WORKS"
  local kbrTranslationsFRNL="$integrationName/$translationsSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_WORKS"
  local titleMatchesFRNL="$integrationName/$dataSourceName/$SUFFIX_KBR_TITLE_MATCHES_FR_NL"
  local titleDuplicatesMatchesFRNL="$integrationName/$dataSourceName/$SUFFIX_KBR_TITLE_DUPLICATES_MATCHES_FR_NL"
  local similarityMatchesFRNL="$integrationName/$dataSourceName/$SUFFIX_KBR_SIMILARITY_MATCHES_FR_NL"
  local similarityDuplicatesMatchesFRNL="$integrationName/$dataSourceName/$SUFFIX_KBR_SIMILARITY_DUPLICATES_MATCHES_FR_NL"
  local similarityMultipleMatchesFRNL="$integrationName/$dataSourceName/$SUFFIX_KBR_SIMILARITY_MULTIPLE_MATCHES_FR_NL"

  source ./py-integration-env/bin/activate

  echo "EXTRACTION - find originals NL-FR"

  time python $SCRIPT_FIND_ORIGINALS \
  --original-works $kbrOriginalsNLFR \
  --translations $kbrTranslationsNLFR \
  --similarity "$similarityThreshold" \
  --apply-candidate-filter \
  --output-file-clear-matches $titleMatchesNLFR \
  --output-file-duplicate-id-matches $titleDuplicatesMatchesNLFR \
  --output-file-similarity-matches $similarityMatchesNLFR \
  --output-file-similarity-duplicate-id-matches $similarityDuplicatesMatchesNLFR \
  --output-file-similarity-multiple-matches $similarityMultipleMatchesNLFR

  echo "EXTRACTION - find originals FR-NL"

  time python $SCRIPT_FIND_ORIGINALS \
  --original-works $kbrOriginalsFRNL \
  --translations $kbrTranslationsFRNL \
  --similarity "$similarityThreshold" \
  --apply-candidate-filter \
  --output-file-clear-matches $titleMatchesFRNL \
  --output-file-duplicate-id-matches $titleDuplicatesMatchesFRNL \
  --output-file-similarity-matches $similarityMatchesFRNL \
  --output-file-similarity-duplicate-id-matches $similarityDuplicatesMatchesFRNL \
  --output-file-similarity-multiple-matches $similarityMultipleMatchesFRNL

}

# -----------------------------------------------------------------------------
function extractMasterData {

  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # create the folders to place the extracted translations and agents
  mkdir -p $integrationName/master-data

  local bbEnglish="$integrationName/master-data/$SUFFIX_MASTER_THES_EN"
  local bbDutch="$integrationName/master-data/$SUFFIX_MASTER_THES_NL"
  local bbFrench="$integrationName/master-data/$SUFFIX_MASTER_THES_FR"

  source ./py-integration-env/bin/activate

  echo "Convert thesaurus data"
  time python $SCRIPT_CONVERT_BB -i $INPUT_MASTER_THES_EN -o $bbEnglish
  time python $SCRIPT_CONVERT_BB -i $INPUT_MASTER_THES_NL -o $bbDutch
  time python $SCRIPT_CONVERT_BB -i $INPUT_MASTER_THES_FR -o $bbFrench

  echo "EXTRACTION - Nothing to extract from master data, copying files"
  cp "$INPUT_MASTER_MARC_ROLES" "$integrationName/master-data/$SUFFIX_MASTER_MARC_ROLES"
  cp "$INPUT_MASTER_MARC_BINDING_TYPES" "$integrationName/master-data/$SUFFIX_MASTER_BINDING_TYPES"
  cp "$INPUT_MASTER_COUNTRIES" "$integrationName/master-data/$SUFFIX_MASTER_COUNTRIES"
  cp "$INPUT_MASTER_LANGUAGES" "$integrationName/master-data/$SUFFIX_MASTER_LANGUAGES"
  cp "$INPUT_MASTER_GENDER" "$integrationName/master-data/$SUFFIX_MASTER_GENDER"

}

# -----------------------------------------------------------------------------
function extractWikidata {

  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # create the folders to place the extracted translations and agents
  mkdir -p $integrationName/wikidata

  echo "EXTRACTION - Nothing to extract from Wikidata, copying files"
  cp "$INPUT_WIKIDATA_ENRICHED" "$integrationName/wikidata/$SUFFIX_WIKIDATA_ENRICHED"

}

# -----------------------------------------------------------------------------
function transformKBR {

  local integrationName=$1

  # create the folder to place the transformed data
  mkdir -p $integrationName/kbr/rdf 

  echo "TRANSFORMATION - Map KBR book data and contributions to RDF"
  mapKBRBookInformationAndContributions $integrationName "kbr"

  echo "TRANSFORMATION - Map KBR translation data to RDF"
  mapKBRTranslationsAndContributions $integrationName "kbr"

  echo "TRANSFORMATION - Map KBR (limited) original information to RDF"
  mapKBRTranslationLimitedOriginals $integrationName "kbr"

  echo "TRANSFORMATION - Map KBR linked authorities data to RDF"
  mapKBRLinkedAuthorities $integrationName

}

# -----------------------------------------------------------------------------
function transformKBROriginals {

  local integrationName=$1

  local dataSourceName="kbr-originals"

  # create the folder to place the transformed data
  mkdir -p $integrationName/$dataSourceName/rdf 

  echo "TRANSFORMATION - Map KBR translation data to RDF"
  mapKBRBookInformationAndContributions $integrationName "$dataSourceName"

}

# -----------------------------------------------------------------------------
function transformOriginalLinksKBR {
  local integrationName=$1
  local dataSourceName=$2

  # create the folder to place the transformed data
  mkdir -p $integrationName/$dataSourceName/rdf 

  originalLinksTurtle="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_ORIGINAL_LINKING_LD"

  # map the translations

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_TITLE_MATCHES_NL_FR="$integrationName/$dataSourceName/$SUFFIX_KBR_TITLE_MATCHES_NL_FR"
  export RML_SOURCE_TITLE_DUPLICATES_MATCHES_NL_FR="$integrationName/$dataSourceName/$SUFFIX_KBR_TITLE_DUPLICATES_MATCHES_NL_FR"
  export RML_SOURCE_SIMILARITY_MATCHES_NL_FR="$integrationName/$dataSourceName/$SUFFIX_KBR_SIMILARITY_MATCHES_NL_FR"
  export RML_SOURCE_SIMILARITY_DUPLICATES_MATCHES_NL_FR="$integrationName/$dataSourceName/$SUFFIX_KBR_SIMILARITY_DUPLICATES_MATCHES_NL_FR"

  export RML_SOURCE_TITLE_MATCHES_FR_NL="$integrationName/$dataSourceName/$SUFFIX_KBR_TITLE_MATCHES_FR_NL"
  export RML_SOURCE_TITLE_DUPLICATES_MATCHES_FR_NL="$integrationName/$dataSourceName/$SUFFIX_KBR_TITLE_DUPLICATES_MATCHES_FR_NL"
  export RML_SOURCE_SIMILARITY_MATCHES_FR_NL="$integrationName/$dataSourceName/$SUFFIX_KBR_SIMILARITY_MATCHES_FR_NL"
  export RML_SOURCE_SIMILARITY_DUPLICATES_MATCHES_FR_NL="$integrationName/$dataSourceName/$SUFFIX_KBR_SIMILARITY_DUPLICATES_MATCHES_FR_NL"

  # 2) execute the mapping
  echo "Map KBR original linking ..."
  . map.sh ../data-sources/kbr/kbr-original-linking.yml $originalLinksTurtle


}

# -----------------------------------------------------------------------------
function transformKB {

  local integrationName=$1

  # create the folder to place the transformed data
  mkdir -p $integrationName/kb/rdf 

  kbTranslationsTurtle="$integrationName/kb/rdf/$SUFFIX_KB_TRL_LD"
  kbLinkedAuthoritiesTurtle="$integrationName/kb/rdf/$SUFFIX_KB_LA_LD" 
  kbOriginalsTurtle="$integrationName/kb/rdf/$SUFFIX_KB_TRL_ORIG_LD"

  # map the translations

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KB_TRL_FR_NL="$integrationName/kb/translations/$SUFFIX_KB_TRL_ISBN_FR_NL"
  export RML_SOURCE_KB_TRL_NL_FR="$integrationName/kb/translations/$SUFFIX_KB_TRL_ISBN_NL_FR"

  export RML_SOURCE_KB_CONT_PERSONS_FR_NL="$integrationName/kb/agents/$SUFFIX_KB_CONT_PERSONS_FR_NL"
  export RML_SOURCE_KB_CONT_PERSONS_NL_FR="$integrationName/kb/agents/$SUFFIX_KB_CONT_PERSONS_NL_FR"
  export RML_SOURCE_KB_AUT_PERSONS_FR_NL="$integrationName/kb/agents/$SUFFIX_KB_AUT_PERSONS_FR_NL"
  export RML_SOURCE_KB_AUT_PERSONS_NL_FR="$integrationName/kb/agents/$SUFFIX_KB_AUT_PERSONS_NL_FR"

  export RML_SOURCE_KB_CONT_ORGS_FR_NL="$integrationName/kb/agents/$SUFFIX_KB_CONT_ORGS_FR_NL"
  export RML_SOURCE_KB_CONT_ORGS_NL_FR="$integrationName/kb/agents/$SUFFIX_KB_CONT_ORGS_NL_FR"
  export RML_SOURCE_KB_AUT_ORGS_FR_NL="$integrationName/kb/agents/$SUFFIX_KB_AUT_ORGS_FR_NL"
  export RML_SOURCE_KB_AUT_ORGS_NL_FR="$integrationName/kb/agents/$SUFFIX_KB_AUT_ORGS_NL_FR"

  export RML_SOURCE_KB_TRL_KBCODE_FR_NL="$integrationName/kb/translations/$SUFFIX_KB_KBCODE_FR_NL"
  export RML_SOURCE_KB_TRL_KBCODE_NL_FR="$integrationName/kb/translations/$SUFFIX_KB_KBCODE_NL_FR"

  # 2) execute the mapping
  echo "TRANSFORMATION - Map KB translations ..."
  . map.sh ../data-sources/kb/kb-translations.yml $kbTranslationsTurtle

  echo "TRANSFORMATION - Map KB (limited) original information"
  . map.sh ../data-sources/kb/kb-translations-limited-originals.yml $kbOriginalsTurtle

  echo "TRANSFORMATION - Map KB linked authorities ..."
  . map.sh ../data-sources/kb/kb-linked-authorities.yml $kbLinkedAuthoritiesTurtle

}

# -----------------------------------------------------------------------------
function transformBnF {
  local integrationName=$1
  echo "TRANSFORMATION - Map BnF translation data to RDF (nothing to do, the extraction step already produced RDF)"
}

# -----------------------------------------------------------------------------
function transformMasterData {

  local integrationName=$1

  # create the folder to place the transformed data
  mkdir -p $integrationName/master-data/rdf 

  echo "TRANSFORMATION - Map master data to RDF"
  mapMasterData $integrationName

}

# -----------------------------------------------------------------------------
function transformWikidata {

  local integrationName=$1

  # create the folder to place the transformed data
  mkdir -p $integrationName/wikidata/rdf 

  wikidataTurtle="$integrationName/wikidata/rdf/$SUFFIX_WIKIDATA_LD"

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_WIKIDATA_ENRICHED="$integrationName/wikidata/$SUFFIX_WIKIDATA_ENRICHED"

  # 2) execute the mapping
  echo "Map enriched Wikidata dump ..."
  . map.sh ../data-sources/wikidata/authors.yml $wikidataTurtle
 
}

# -----------------------------------------------------------------------------
function transformNationalityFromBnFViaISNI {
  local integrationName=$1
  echo "TRANSFORMATION - Nothing to do for BnFVIAISNI, the extraction step already produced RDF"
}

# -----------------------------------------------------------------------------
function extractKBRTranslationsAndContributions {

  #
  # KBR TRANSLATIONS
  # XML -> XML clean -> CSV -> TURTLE (kbr-translations.ttl)
  # mapping: kbr-translations.yml
  # named graphs: <http://kbr-syracuse> and <http://kbr-originals>
  #
  local integrationName=$1
  local dataSourceName=$2
  local kbrDutchTranslations=$3
  local kbrFrenchTranslations=$4

  # DutchTranslations = NL-FR
  # FrenchTranslations = FR-NL

  # document which input was used
  printf "\nUsed input (KBR translations and contributors)\n* $kbrDutchTranslations\n* $kbrFrenchTranslations" >> "$integrationName/$dataSourceName/README.md"

  #
  # Define file names based on current integration directory and file name patterns
  #
  kbrDutchTranslationsCleaned="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_CLEANED"
  kbrFrenchTranslationsCleaned="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_CLEANED"

  kbrDutchTranslationsCSVWorks="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_WORKS"
  kbrFrenchTranslationsCSVWorks="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_WORKS"

  kbrDutchTranslationsCSVCont="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_CONT"
  kbrDutchTranslationsCSVContReplaced="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_CONT_REPLACE"
  kbrDutchTranslationsCSVContDedup="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_CONT_DEDUP"
  kbrFrenchTranslationsCSVCont="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_CONT"
  kbrFrenchTranslationsCSVContReplaced="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_CONT_REPLACE"
  kbrFrenchTranslationsCSVContDedup="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_CONT_DEDUP"

  kbrDutchTranslationsIdentifiedAuthorities="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_NEWAUT"
  kbrFrenchTranslationsIdentifiedAuthorities="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_NEWAUT"

  kbrDutchTranslationsCSVBB="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_BB"
  kbrFrenchTranslationsCSVBB="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_BB"

  kbrDutchTranslationsPubCountries="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_PUB_COUNTRY"
  kbrFrenchTranslationsPubCountries="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_PUB_COUNTRY"

  kbrDutchTranslationsPubPlaces="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_PUB_PLACE"
  kbrFrenchTranslationsPubPlaces="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_PUB_PLACE"

  kbrDutchTranslationsCollectionLinks="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_COL_LINKS"
  kbrFrenchTranslationsCollectionLinks="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_COL_LINKS"

  kbrDutchTranslationsISBN10="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_ISBN10"
  kbrDutchTranslationsISBN13="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_ISBN13"
  kbrFrenchTranslationsISBN10="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_ISBN10"
  kbrFrenchTranslationsISBN13="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_ISBN13"
  
  source py-integration-env/bin/activate

  echo "Clean Dutch translations ..."
  cleanTranslations "$kbrDutchTranslations" "$kbrDutchTranslationsCleaned"

  echo "Clean French translations ..."
  cleanTranslations "$kbrFrenchTranslations" "$kbrFrenchTranslationsCleaned"

  echo "Extract CSV from Dutch translations XML..."
  extractCSVFromXMLTranslations "$kbrDutchTranslationsCleaned" "$kbrDutchTranslationsCSVWorks" "$kbrDutchTranslationsCSVCont" "$kbrDutchTranslationsCollectionLinks"

  echo "Extract CSV from French translations XML..."
  extractCSVFromXMLTranslations "$kbrFrenchTranslationsCleaned" "$kbrFrenchTranslationsCSVWorks" "$kbrFrenchTranslationsCSVCont" "$kbrFrenchTranslationsCollectionLinks"

  echo "Replace publisher names to support deduplication - NL-FR"
  python $SCRIPT_CHANGE_PUBLISHER_NAME -l $INPUT_KBR_PBL_REPLACE_LIST -i $kbrDutchTranslationsCSVCont -o $kbrDutchTranslationsCSVContReplaced

  echo "Replace publisher names to support deduplication - FR-NL"
  python $SCRIPT_CHANGE_PUBLISHER_NAME -l $INPUT_KBR_PBL_REPLACE_LIST -i $kbrFrenchTranslationsCSVCont -o $kbrFrenchTranslationsCSVContReplaced

  echo "Deduplicate newly identified contributors - NL-FR"
  python $SCRIPT_DEDUPLICATE_KBR_PUBLISHERS -l $INPUT_KBR_ORGS_LOOKUP -i $kbrDutchTranslationsCSVContReplaced -o $kbrDutchTranslationsCSVContDedup

  echo "Deduplicate newly identified contributors - FR-NL"
  python $SCRIPT_DEDUPLICATE_KBR_PUBLISHERS -l $INPUT_KBR_ORGS_LOOKUP -i $kbrFrenchTranslationsCSVContReplaced -o $kbrFrenchTranslationsCSVContDedup

  echo "Extract BB assignments for Dutch translations ..."
  extractBBEntries "$kbrDutchTranslationsCSVWorks" "$kbrDutchTranslationsCSVBB"

  echo "Extract BB assignments for French translations ..."
  extractBBEntries "$kbrFrenchTranslationsCSVWorks" "$kbrFrenchTranslationsCSVBB"

  echo "Extract publication countries from Dutch translations ..."
  extractPubCountries "$kbrDutchTranslationsCSVWorks" "$kbrDutchTranslationsPubCountries"

  echo "Extract publication countries from French translations ..."
  extractPubCountries "$kbrFrenchTranslationsCSVWorks" "$kbrFrenchTranslationsPubCountries"

  echo "Extract publication places from Dutch translations ..."
  extractPubPlaces "$kbrDutchTranslationsCSVWorks" "$kbrDutchTranslationsPubPlaces"

  echo "Extract publication places from French translations ..."
  extractPubPlaces "$kbrFrenchTranslationsCSVWorks" "$kbrFrenchTranslationsPubPlaces"


  echo "Extract (possibly multiple) ISBN10 identifiers per translation - NL-FR"
  extractISBN10 "$kbrDutchTranslationsCSVWorks" "$kbrDutchTranslationsISBN10"

  echo "Extract (possibly multiple) ISBN13 identifiers per translation - NL-FR"
  extractISBN13 "$kbrDutchTranslationsCSVWorks" "$kbrDutchTranslationsISBN13"

  echo "Extract (possibly multiple) ISBN10 identifiers per translation - FR-NL"
  extractISBN10 "$kbrFrenchTranslationsCSVWorks" "$kbrFrenchTranslationsISBN10"

  echo "Extract (possibly multiple) ISBN13 identifiers per translation - FR-NL"
  extractISBN13 "$kbrFrenchTranslationsCSVWorks" "$kbrFrenchTranslationsISBN13"


  echo "Extract newly identified contributors ..."
  extractIdentifiedAuthorities "$kbrDutchTranslationsCSVContDedup" "$kbrDutchTranslationsIdentifiedAuthorities"
  extractIdentifiedAuthorities "$kbrFrenchTranslationsCSVContDedup" "$kbrFrenchTranslationsIdentifiedAuthorities"


}

# -----------------------------------------------------------------------------
function extractKBRLinkedAuthorities {

  local integrationName=$1
  local kbrNLPersons=$2
  local kbrNLOrgs=$3
  local kbrFRPersons=$4
  local kbrFROrgs=$5
  local kbrBelgianPersons=$6

  # document which input was used
  printf "\nUsed input (KBR linked authorities) \n* $kbrNLPersons\n* $kbrNLOrgs\n* $kbrFRPersons\n* $kbrFROrgs" >> "$integrationName/kbr/README.md"

  #
  # Define file names based on current integration directory and file name patterns
  #
  kbrNLPersonsCSV="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_NL_CLEANED"
  kbrNLOrgsCSV="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_NL_CLEANED"
  kbrFRPersonsCSV="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_FR_CLEANED"
  kbrFROrgsCSV="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_FR_CLEANED"

  kbrBelgianPersonsCSV="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_CSV"

  kbrNLPersonsNationalities="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_NL_NAT"
  kbrFRPersonsNationalities="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_FR_NAT"

  kbrBelgianPersonsNationalities="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_NATIONALITIES"

  source py-integration-env/bin/activate

  echo "Extract authorities NL-FR - Persons ..."
  python $SCRIPT_EXTRACT_AGENTS_PERSONS -i $kbrNLPersons -o $kbrNLPersonsCSV -n $kbrNLPersonsNationalities

  echo "Extract authorities NL-FR - Organizations ..."
  python $SCRIPT_EXTRACT_AGENTS_ORGS -i $kbrNLOrgs -o $kbrNLOrgsCSV

  echo "Extract authorities FR-NL - Persons ..."
  python $SCRIPT_EXTRACT_AGENTS_PERSONS -i $kbrFRPersons -o $kbrFRPersonsCSV -n $kbrFRPersonsNationalities

  echo "Extract authorities FR-NL - Organizations ..."
  python $SCRIPT_EXTRACT_AGENTS_ORGS -i $kbrFROrgs -o $kbrFROrgsCSV

  echo "Extract authorities KBR-Belgians - Persons ..."
  # these Belgians might have multiple nationalities, thus it is still important to get the nationality information
  python $SCRIPT_EXTRACT_AGENTS_PERSONS -i $kbrBelgianPersons -o $kbrBelgianPersonsCSV -n $kbrBelgianPersonsNationalities

  echo "Copy publisher location information ..."
  cp "$INPUT_KBR_LA_PLACES_VLG" "$integrationName/kbr/agents/$SUFFIX_KBR_LA_PLACES_VLG"
  cp "$INPUT_KBR_LA_PLACES_WAL" "$integrationName/kbr/agents/$SUFFIX_KBR_LA_PLACES_WAL"
  cp "$INPUT_KBR_LA_PLACES_BRU" "$integrationName/kbr/agents/$SUFFIX_KBR_LA_PLACES_BRU"
 
}

# -----------------------------------------------------------------------------
function extractKBRBelgians {

  local integrationName=$1
  local kbrBelgians=$2

  # document which input was used
  printf "\nUsed input (KBR Belgians)\n* $kbrBelgians" >> "$integrationName/kbr/README.md"

  #
  # Define file names based on current integration directory and file name patterns
  #
  kbrBelgiansNorm="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_NORM"
  kbrBelgiansCleaned="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_CLEANED"

  source py-integration-env/bin/activate

  echo "Extract Belgians ..."
  # currently this input has already normalized headers
  #normalizeCSVHeaders "$kbrBelgians" "$kbrBelgiansNorm" "$KBR_CSV_HEADER_CONVERSION"
  python $SCRIPT_EXTRACT_AGENTS_PERSONS -i $kbrBelgians -o $kbrBelgiansCleaned
}

# -----------------------------------------------------------------------------
function extractBnFBelgianContributors {

  local integrationName=$1
  local bnfPersonAuthors=$2
  local bnfBelgianContributorIDs=$3

  # document which input was used
  printf "\nUsed input (BnF Belgian contributors)\n* $bnfPersonAuthors" >> "$integrationName/bnf/README.md"

  source py-integration-env/bin/activate

  getSubjects "$bnfPersonAuthors" "$BNF_FILTER_CONFIG_CONTRIBUTORS" "$bnfBelgianContributorIDs"
}

# -----------------------------------------------------------------------------
function extractBnFBelgianPublications {
  local integrationName=$1
  local bnfEditionContributions=$2
  local bnfBelgians=$3
  local bnfBelgianPublicationIDs=$4

  # document which input was used
  printf "\nUsed input (BnF editions used to filter publication IDs from Belgian contributors)\n* $bnfEditionContributions\n* $bnfBelgians\n" >> "$integrationName/bnf/README.md"

  source py-integration-env/bin/activate
  time python -m $MODULE_GET_RDF_XML_SUBJECTS -i $bnfEditionContributions -o $bnfBelgianPublicationIDs -p "marcrel:aut" -p "marcrel:ill" -p "marcrel:sce" -l $bnfBelgians
}

# -----------------------------------------------------------------------------
function extractBnFTranslations {
  local integrationName=$1
  local bnfTranslations=$2
  local bnfTranslationIDs=$3
 
  # document which input was used
  printf "\nUsed input (BnF translations used to extract relevant publication IDs)\n* $bnfTranslations\n" >> "$integrationName/bnf/README.md"

  source py-integration-env/bin/activate
  time python $SCRIPT_EXTRACT_COLUMN -i $bnfTranslations -o $bnfTranslationIDs -d ';' -c 0
}  

# -----------------------------------------------------------------------------
function extractBnFRelevantPublicationData {
  local integrationName=$1
  local bnfEditions=$2
  local bnfTranslationIDs=$3
  local bnfBelgianPubs=$4
  local bnfRelevantData=$5

  # document which input was used
  printf "\nUsed input (BnF editions used to extract relevant publication data)\n* $bnfEditions" >> "$integrationName/bnf/README.md"

  source py-integration-env/bin/activate
  time python $MODULE_FILTER_RDF_XML_SUBJECTS -i $bnfEditions  -o $bnfRelevantData -f $bnfTranslationIDs -f $bnfBelgianPubs
}

# -----------------------------------------------------------------------------
function mapKBRTranslationsAndContributions {
  local integrationName=$1
  local dataSourceName=$2

  # map the translations

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_WORKS_FR="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_WORKS"
  export RML_SOURCE_WORKS_NL="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_WORKS"
  export RML_SOURCE_CONT_FR="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_CONT_DEDUP"
  export RML_SOURCE_CONT_NL="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_CONT_DEDUP"


  kbrTranslationsTurtle="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_TRL_LD"
  . map.sh ../data-sources/kbr/kbr-translations.yml $kbrTranslationsTurtle

}

# -----------------------------------------------------------------------------
function mapKBRBookInformationAndContributions {

  local integrationName=$1
  local dataSourceName=$2

  kbrBookDataTurtle="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_BOOK_LD"
  kbrBookDataIdentifiedAuthorities="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_NEWAUT_LD"
  kbrBookDataBBTurtle="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_TRL_BB_LD"
  kbrBookDataPubCountriesTurtle="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_TRL_PUB_COUNTRY_LD"
  kbrBookDataPubPlacesTurtle="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_TRL_PUB_PLACE_LD"
  kbrBookDataISBNTurtle="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_TRL_ISBN_LD"

  # map the translations

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_WORKS_FR="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_WORKS"
  export RML_SOURCE_WORKS_NL="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_WORKS"
  export RML_SOURCE_CONT_FR="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_CONT_DEDUP"
  export RML_SOURCE_CONT_NL="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_CONT_DEDUP"
  export RML_SOURCE_COLLECTION_LINKS_FR="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_COL_LINKS"
  export RML_SOURCE_COLLECTION_LINKS_NL="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_COL_LINKS"

  # 2) execute the mapping
  echo "Map KBR translations and contributions ..."
  . map.sh ../data-sources/kbr/kbr-book-data.yml $kbrBookDataTurtle


  # map newly identified publishers

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_CONT_NL_IDENTIFIED="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_NEWAUT"
  export RML_SOURCE_KBR_CONT_FR_IDENTIFIED="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_NEWAUT"

  # 2) execute the mapping
  echo "Map KBR newly identified contributors ..."
  . map.sh ../data-sources/kbr/kbr-identified-authorities.yml $kbrBookDataIdentifiedAuthorities

  # map belgian bibliography assignments

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_BB_NL="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_BB"
  export RML_SOURCE_KBR_BB_FR="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_BB"
  
  # 2) execute the mapping
  echo "Map KBR BB assignments ..."
  . map.sh ../data-sources/kbr/kbr-belgian-bibliography.yml $kbrBookDataBBTurtle

  # map publication countries

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_PUB_COUNTRIES_NL="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_PUB_COUNTRY"
  export RML_SOURCE_KBR_PUB_COUNTRIES_FR="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_PUB_COUNTRY"

  # 2) execute the mapping
  echo "Map KBR publication countries relationships ..."
  . map.sh ../data-sources/kbr/kbr-publication-countries.yml $kbrBookDataPubCountriesTurtle

  # map publication places

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_PUB_PLACES_NL="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_PUB_PLACE"
  export RML_SOURCE_KBR_PUB_PLACES_FR="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_PUB_PLACE"

  # 2) execute the mapping
  echo "Map KBR publication places relationships ..."
  . map.sh ../data-sources/kbr/kbr-publication-places.yml $kbrBookDataPubPlacesTurtle


  # map ISBN10/ISBN13

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_ISBN10_NL="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_ISBN10"
  export RML_SOURCE_KBR_ISBN10_FR="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_ISBN10"
  export RML_SOURCE_KBR_ISBN13_NL="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_ISBN13"
  export RML_SOURCE_KBR_ISBN13_FR="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_ISBN13"

  # 2) execute the mapping
  echo "Map KBR ISBN10/ISBN13 relationships ..."
  . map.sh ../data-sources/kbr/kbr-isbn.yml $kbrBookDataISBNTurtle
  

}

# -----------------------------------------------------------------------------
function mapKBRTranslationLimitedOriginals {
  local integrationName=$1
  local dataSourceName=$2

  kbrLimitedOriginalsTurtle="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_TRL_LIMITED_ORIG_LD"

  # map the translations

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_WORKS_FR="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_FR_WORKS"
  export RML_SOURCE_WORKS_NL="$integrationName/$dataSourceName/book-data-and-contributions/$SUFFIX_KBR_TRL_NL_WORKS"

  # 2) execute the mapping
  echo "Map KBR limited information about originals ..."
  . map.sh ../data-sources/kbr/kbr-translations-limited-originals.yml $kbrLimitedOriginalsTurtle


}

# -----------------------------------------------------------------------------
function mapKBRLinkedAuthorities {

  local integrationName=$1
  # input
  kbrPersonsFRNL="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_FR_CLEANED"
  kbrPersonsNLFR="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_NL_CLEANED"
  kbrPersonsNatFRNL="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_FR_NAT"
  kbrPersonsNatNLFR="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_NL_NAT"

  kbrOrgsFRNL="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_FR_CLEANED"
  kbrOrgsNLFR="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_NL_CLEANED"

  kbrBelgians="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_CSV"
  kbrBelgiansNat="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_NATIONALITIES"

  # output
  kbrPersonsTurtleFRNL="$integrationName/kbr/rdf/$SUFFIX_KBR_PERSONS_FR_NL_LD"
  kbrPersonsTurtleNLFR="$integrationName/kbr/rdf/$SUFFIX_KBR_PERSONS_NL_FR_LD"
  kbrOrgsTurtleFRNL="$integrationName/kbr/rdf/$SUFFIX_KBR_ORGS_FR_NL_LD"
  kbrOrgsTurtleNLFR="$integrationName/kbr/rdf/$SUFFIX_KBR_ORGS_NL_FR_LD"
  kbrBelgiansTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_BELGIANS_LD"
  kbrPlacesTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_PLACES_LD"
  kbrPersonsIdentifiersTurtleFRNL="$integrationName/kbr/rdf/$SUFFIX_KBR_PERSONS_IDENTIFIERS_FR_NL_LD"
  kbrPersonsIdentifiersTurtleNLFR="$integrationName/kbr/rdf/$SUFFIX_KBR_PERSONS_IDENTIFIERS_NL_FR_LD"
  kbrOrgsIdentifiersTurtleFRNL="$integrationName/kbr/rdf/$SUFFIX_KBR_ORGS_IDENTIFIERS_FR_NL_LD"
  kbrOrgsIdentifiersTurtleNLFR="$integrationName/kbr/rdf/$SUFFIX_KBR_ORGS_IDENTIFIERS_NL_FR_LD"
  kbrBelgiansIdentifiersTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_BELGIANS_IDENTIFIERS_LD"



  # 2) execute the mapping
  mapKBRPersons "$kbrPersonsFRNL" "$kbrPersonsNatFRNL" "$kbrPersonsTurtleFRNL"
  mapKBRPersons "$kbrPersonsNLFR" "$kbrPersonsNatNLFR" "$kbrPersonsTurtleNLFR"
  mapKBRPersons "$kbrBelgians" "$kbrBelgiansNat" "$kbrBelgiansTurtle"

  mapKBROrgs "$kbrOrgsFRNL" "$kbrOrgsTurtleFRNL"
  mapKBROrgs "$kbrOrgsNLFR" "$kbrOrgsTurtleNLFR"

  mapKBRPlaces "$integrationName" "$kbrPlacesTurtle"

  mapKBRLinkedIdentifiers "$kbrPersonsFRNL" "$kbrPersonsIdentifiersTurtleFRNL"
  mapKBRLinkedIdentifiers "$kbrPersonsNLFR" "$kbrPersonsIdentifiersTurtleNLFR"

  mapKBRLinkedIdentifiers "$kbrOrgsFRNL" "$kbrOrgsIdentifiersTurtleFRNL"
  mapKBRLinkedIdentifiers "$kbrOrgsNLFR" "$kbrOrgsIdentifiersTurtleNLFR"

  mapKBRLinkedIdentifiers "$kbrBelgians" "$kbrBelgiansIdentifiersTurtle"

}

# -----------------------------------------------------------------------------
function mapKBRPersons {
  local sourceFile=$1
  local sourceFileNat=$2
  local outputTurtle=$3

  export RML_SOURCE_KBR_PERSONS="$sourceFile"
  export RML_SOURCE_KBR_PERSONS_NAT="$sourceFileNat"

  echo "Map KBR Persons - $sourceFile"
  . map.sh ../data-sources/kbr/kbr-persons.yml $outputTurtle
}

# -----------------------------------------------------------------------------
function mapKBROrgs {
  local sourceFile=$1
  local outputTurtle=$2

  export RML_SOURCE_KBR_ORGS="$sourceFile"

  echo "Map KBR Orgs - $sourceFile"
  . map.sh ../data-sources/kbr/kbr-orgs.yml $outputTurtle
}

# -----------------------------------------------------------------------------
function mapKBRLinkedIdentifiers {
  local sourceFile=$1
  local outputTurtle=$2

  export RML_SOURCE_KBR_LINKED_AUTHORITIES="$sourceFile"

  echo "Map KBR Orgs - $sourceFile"
  . map.sh ../data-sources/kbr/kbr-linked-identifiers.yml $outputTurtle
}

# -----------------------------------------------------------------------------
function mapKBRPlaces {
  local integrationName=$1

  local kbrPlacesTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_PLACES_LD"

  export RML_SOURCE_KBR_PUBLISHER_PLACES_FLANDERS="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PLACES_VLG"
  export RML_SOURCE_KBR_PUBLISHER_PLACES_WALLONIA="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PLACES_WAL"
  export RML_SOURCE_KBR_PUBLISHER_PLACES_BRUSSELS="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PLACES_BRU"

  echo "Map KBR Places"
  . map.sh ../data-sources/kbr/kbr-places.yml $kbrPlacesTurtle
}


# -----------------------------------------------------------------------------
function mapMasterData {

  local integrationName=$1

  masterDataTurtle="$integrationName/master-data/rdf/$SUFFIX_MASTER_LD"

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_MASTER_MARC_ROLES="$integrationName/master-data/$SUFFIX_MASTER_MARC_ROLES"
  export RML_SOURCE_MASTER_BINDING_TYPES="$integrationName/master-data/$SUFFIX_MASTER_BINDING_TYPES"
  export RML_SOURCE_MASTER_THES_EN="$integrationName/master-data/$SUFFIX_MASTER_THES_EN"
  export RML_SOURCE_MASTER_THES_NL="$integrationName/master-data/$SUFFIX_MASTER_THES_NL"
  export RML_SOURCE_MASTER_THES_FR="$integrationName/master-data/$SUFFIX_MASTER_THES_FR"

  # 2) execute the mapping
  echo "Map master data ..."
  . map.sh ../data-sources/master-data/master-data.yml $masterDataTurtle
  
}


# -----------------------------------------------------------------------------
function loadKBR {
  local integrationName=$1

  local dataSourceName="kbr"

  local translationsNamedGraph="$TRIPLE_STORE_GRAPH_KBR_TRL"
  local linkedAuthoritiesNamedGraph="$TRIPLE_STORE_GRAPH_KBR_LA"

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # first delete content of the named graph in case it already exists
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$translationsNamedGraph"

  # load general book data
  loadKBRBookInformationAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph"

  # load translation specific RDF
  loadKBRTranslationsAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph" "$linkedAuthoritiesNamedGraph"

  loadKBRLimitedOriginalInfo "$integrationName" "$dataSourceName" "$TRIPLE_STORE_GRAPH_KBR_ORIG_TRL"

  loadKBRLinkedAuthorities "$integrationName" "$dataSourceName" "$linkedAuthoritiesNamedGraph"
}

# -----------------------------------------------------------------------------
function loadKBROriginals {
  local integrationName=$1

  local dataSourceName="kbr-originals"

  local translationsNamedGraph="$TRIPLE_STORE_GRAPH_KBR_ORIG_TRL"
  local linkedAuthoritiesNamedGraph="$TRIPLE_STORE_GRAPH_KBR_ORIG_LA"

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # first delete content of the named graph in case it already exists
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$translationsNamedGraph"

  # only load book information, no translation-specific triples
  loadKBRBookInformationAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph" "$linkedAuthoritiesNamedGraph"
}

# -----------------------------------------------------------------------------
function loadOriginalLinksKBR {
  local integrationName=$1
  local dataSourceName=$2

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"
  local kbrOriginalLinksTurtle="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_ORIGINAL_LINKING_LD"

  echo "Load KBR links to identified originals ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_KBR_TRL" \
    "$kbrOriginalLinksTurtle"
}

# -----------------------------------------------------------------------------
function loadKBRTranslationsAndContributions {
  local integrationName=$1
  local dataSourceName=$2
  local translationsNamedGraph=$3

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local kbrTranslations="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_TRL_LD"
  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  echo "Load KBR translations and contributions ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$translationsNamedGraph" \
    "$kbrTranslations"
}

# -----------------------------------------------------------------------------
function loadKBRBookInformationAndContributions {
  local integrationName=$1
  local dataSourceName=$2
  local translationsNamedGraph=$3
  local linkedAuthoritiesNamedGraph=$4

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local kbrBookInformationAndContributions="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_BOOK_LD"
  local kbrIdentifiedAuthorities="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_NEWAUT_LD"
  local kbrTranslationsBB="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_TRL_BB_LD"
  local kbrTranslationsPubCountries="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_TRL_PUB_COUNTRY_LD"
  local kbrTranslationsPubPlaces="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_TRL_PUB_PLACE_LD"
  local kbrTranslationsISBNTurtle="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_TRL_ISBN_LD"

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"


  echo "Load KBR translations and contributions, BB assignments, countries, places, ISBN10/ISBN13 ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$translationsNamedGraph" \
    "$kbrBookInformationAndContributions" "$kbrTranslationsBB" "$kbrTranslationsPubCountries" "$kbrTranslationsPubPlaces" "$kbrTranslationsISBNTurtle"

  # upload newly identified authorities to the linked authorities named graph
  echo "Load newly identified KBR linked authorities ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$linkedAuthoritiesNamedGraph" \
    "$kbrIdentifiedAuthorities"

}

# -----------------------------------------------------------------------------
function loadKBRLimitedOriginalInfo {
  local integrationName=$1
  local dataSourceName=$2
  local originalsNamedGraph=$3

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local kbrLimitedOriginalsTurtle="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_TRL_LIMITED_ORIG_LD"
  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  echo "Load KBR (limited) original information ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$originalsNamedGraph" \
    "$kbrLimitedOriginalsTurtle"
}

# -----------------------------------------------------------------------------
function loadKBRLinkedAuthorities {
  local integrationName=$1
  local dataSourceName=$2
  local linkedAuthoritiesNamedGraph=$3

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local kbrPersonsFRNL="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_PERSONS_FR_NL_LD"
  local kbrPersonsNLFR="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_PERSONS_NL_FR_LD"
  local kbrOrgsFRNL="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_ORGS_FR_NL_LD"
  local kbrOrgsNLFR="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_ORGS_NL_FR_LD"
  local kbrPlaces="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_PLACES_LD"
  local kbrBelgians="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_BELGIANS_LD"

  local kbrPersonsIdentifiersTurtleFRNL="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_PERSONS_IDENTIFIERS_FR_NL_LD"
  local kbrPersonsIdentifiersTurtleNLFR="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_PERSONS_IDENTIFIERS_NL_FR_LD"
  local kbrOrgsIdentifiersTurtleFRNL="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_ORGS_IDENTIFIERS_FR_NL_LD"
  local kbrOrgsIdentifiersTurtleNLFR="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_ORGS_IDENTIFIERS_NL_FR_LD"
  local kbrBelgiansIdentifiersTurtle="$integrationName/$dataSourceName/rdf/$SUFFIX_KBR_BELGIANS_IDENTIFIERS_LD"

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  # upload newly identified authorities to the linked authorities named graph
  echo "Load newly identified KBR linked authorities ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$linkedAuthoritiesNamedGraph" \
    "$kbrPersonsFRNL" "$kbrPersonsNLFR" "$kbrOrgsFRNL" "$kbrOrgsNLFR" "$kbrPlaces" \
    "$kbrPersonsIdentifiersTurtleFRNL" "$kbrPersonsIdentifiersTurtleNLFR" "$kbrOrgsIdentifiersTurtleFRNL" \
    "$kbrOrgsIdentifiersTurtleNLFR" "$kbrBelgians" "$kbrBelgiansIdentifiersTurtle"

}



# -----------------------------------------------------------------------------
function loadKB {

  local integrationName=$1

  source ./py-integration-env/bin/activate

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local kbTranslationsAndContributions="$integrationName/kb/rdf/$SUFFIX_KB_TRL_LD"
  local kbLinkedAuthorities="$integrationName/kb/rdf/$SUFFIX_KB_LA_LD"
  local kbOriginalsTurtle="$integrationName/kb/rdf/$SUFFIX_KB_TRL_ORIG_LD"
  local kbPublishersFRNL="$integrationName/kb/rdf/$SUFFIX_KB_PBL_FR_NL_LD"
  local kbPublishersNLFR="$integrationName/kb/rdf/$SUFFIX_KB_PBL_NL_FR_LD"
  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  # first delete content of the named graph in case it already exists
  #deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KB_TRL"

  #deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KB_LA"

  #deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KB_TRL_ORIG"


  echo "Load KB translations and contributions ..."
  #python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_KB_TRL" "$kbTranslationsAndContributions"

  echo "Load KB (limited) original information ..."
  #python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_KB_TRL_ORIG" "$kbOriginalsTurtle"

  echo "Load KB linked authorities ..."
  #python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_KB_LA" "$kbLinkedAuthorities"

  echo "Load KB publisher data FR-NL ..."
  #python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph $TRIPLE_STORE_GRAPH_KB_PBL "$kbPublishersFRNL"

  echo "Load KB publisher data NL-FR ..."
  #python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph $TRIPLE_STORE_GRAPH_KB_PBL "$kbPublishersNLFR"

  echo "Link KB translations to publisher authority records ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_KB_TRL_PBL"

}

# -----------------------------------------------------------------------------
function loadBnF {
  local integrationName=$1

  mkdir -p $integrationName/bnf/translations
  mkdir -p $integrationName/bnf/rdf

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # first delete content of the named graph in case it already exists
  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_BNF_TRL_FR_NL>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_TRL_FR_NL"

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_BNF_TRL_NL_FR>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_TRL_NL_FR"

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_BNF_CONT>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_CONT"

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_BNF_TRL_CONT_LINKS>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_TRL_CONT_LINKS"

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_BNF_CONT_ISNI>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_CONT_ISNI"

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_BNF_CONT_VIAF>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_CONT_VIAF"

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_BNF_CONT_WIKIDATA>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_CONT_WIKIDATA"

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_BNF_TRL>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_TRL"

  local bnfTranslationsFRNL="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_FR_NL_LD"
  local bnfTranslationsNLFR="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_NL_FR_LD"
  local bnfContributorData="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_LD"
  local bnfContributorDataOrgs="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_ORGS_LD"
  local bnfContributionLinksData="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_CONT_LINKS_LD"
  local bnfContributorIsniData="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_ISNI_LD"
  local bnfContributorVIAFData="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_VIAF_LD"
  local bnfContributorWikidataData="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_WIKIDATA_LD"

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  echo "Load BNF translations FR-NL ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_TRL_FR_NL" "$bnfTranslationsFRNL"

  echo "Load BNF translations NL-FR ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_TRL_NL_FR" "$bnfTranslationsNLFR"

  echo "Load BnF contributors persons and organizations ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_CONT" "$bnfContributorData" "$bnfContributorDataOrgs"


  echo "Load BnF publication-contributor links ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_TRL_CONT_LINKS" "$bnfContributionLinksData"

  echo "Load external links of BnF contributors - ISNI ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_CONT_ISNI" "$bnfContributorIsniData"

  echo "Load external links of BnF contributors - VIAF ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_CONT_VIAF" "$bnfContributorVIAFData"

  echo "Load external links of BnF contributors - WIKIDATA ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_CONT_WIKIDATA" "$bnfContributorWikidataData"

  echo "Load BnF publication data to a single named graph"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" "$TRANSFORM_QUERY_BNF_TRL_FR_NL" "$TRANSFORM_QUERY_BNF_TRL_NL_FR"


  bnfISBN10ISBN13="$integrationName/bnf/translations/$SUFFIX_BNF_ISBN10_ISBN13_CSV"
  bnfISBN10ISBN13Enriched="$integrationName/bnf/rdf/$SUFFIX_BNF_ISBN10_ISBN13_ENRICHED_CSV"

  bnfISBN13MissingHyphen="$integrationName/bnf/translations/$SUFFIX_BNF_ISBN13_NO_HYPHEN_CSV"
  bnfCleanedISBN13="$integrationName/bnf/translations/$SUFFIX_BNF_ISBN13_FIXED_CSV"
  bnfCleanedISBN13Triples="$integrationName/bnf/rdf/$SUFFIX_BNF_ISBN13_HYPHEN_NT"

  bnfISBN10MissingHyphen="$integrationName/bnf/translations/$SUFFIX_BNF_ISBN10_NO_HYPHEN_CSV"
  bnfCleanedISBN10="$integrationName/bnf/translations/$SUFFIX_BNF_ISBN10_FIXED_CSV"
  bnfCleanedISBN10Triples="$integrationName/bnf/rdf/$SUFFIX_BNF_ISBN10_HYPHEN_NT"

  source ./py-integration-env/bin/activate

  echo "Get BnF ISBN10 and ISBN13 identifiers ..."
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$GET_BNF_ISBN10_ISBN13_QUERY_FILE" "$ENV_SPARQL_ENDPOINT" "$bnfISBN10ISBN13"

  echo "Compute BnF ISBN10 and ISBN13 identifiers ..."
  time python $SCRIPT_BNF_ADD_ISBN_10_13 -i $bnfISBN10ISBN13 -o $bnfISBN10ISBN13Enriched

  echo "Delete existing BnF ISBN10 and ISBN13 identifiers ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" "$DELETE_QUERY_BNF_ISBN"

  echo "Add normalized BnF ISBN10 and ISBN13 identifiers ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_NT" --named-graph "$TRIPLE_STORE_GRAPH_BNF_TRL" "$bnfISBN10ISBN13Enriched"

  #echo "Fix BnF ISBN13 identifiers without hyphen - get malformed ISBN identifiers"
  #queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$GET_BNF_ISBN13_WITHOUT_HYPHEN_QUERY_FILE" "$ENV_SPARQL_ENDPOINT" "$bnfISBN13MissingHyphen"

  #echo "Fix BnF ISBN13 identifiers without hyphen - normalize ISBN identifiers"
  #time python $SCRIPT_FIX_ISBN13 -i $bnfISBN13MissingHyphen -o $bnfCleanedISBN13

  #echo "Fix BnF ISBN13 identifiers without hyphen - upload normalized ISBN identifiers"
  #time python $SCRIPT_CREATE_ISBN13_TRIPLES -i $bnfCleanedISBN13 -o $bnfCleanedISBN13Triples
  #uploadData "$TRIPLE_STORE_NAMESPACE" "$bnfCleanedISBN13Triples" "$FORMAT_NT" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_TRL"

  #echo "Fix BnF ISBN13 identifiers without hyphen - delete malformed ISBN identifiers"
  #uploadData "$TRIPLE_STORE_NAMESPACE" "$DELETE_QUERY_BNF_ISBN13_WITHOUT_HYPHEN" "$FORMAT_SPARQL_UPDATE" "$ENV_SPARQL_ENDPOINT"

  #echo "Fix BnF ISBN10 identifiers without hyphen - get malformed ISBN identifiers" 
  #queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$GET_BNF_ISBN10_WITHOUT_HYPHEN_QUERY_FILE" "$ENV_SPARQL_ENDPOINT" "$bnfISBN10MissingHyphen"

  #echo "Fix BnF ISBN10 identifiers without hyphen - normalize ISBN identifiers"
  #time python $SCRIPT_FIX_ISBN10 -i $bnfISBN10MissingHyphen -o $bnfCleanedISBN10

  #echo "Fix BnF ISBN10 identifiers without hyphen - upload normalized ISBN identifiers"
  #time python $SCRIPT_CREATE_ISBN10_TRIPLES -i $bnfCleanedISBN10 -o $bnfCleanedISBN10Triples
  #uploadData "$TRIPLE_STORE_NAMESPACE" "$bnfCleanedISBN10Triples" "$FORMAT_NT" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_TRL"

  #echo "Fix BnF ISBN10 identifiers without hyphen - delete malformed ISBN identifiers"
  #uploadData "$TRIPLE_STORE_NAMESPACE" "$DELETE_QUERY_BNF_ISBN10_WITHOUT_HYPHEN" "$FORMAT_SPARQL_UPDATE" "$ENV_SPARQL_ENDPOINT"


  echo "Add dcterms:identifier to BnF contributors, manifestations as well as add ISNI/VIAF/Wikidata identifier according to the bibframe vocabulary"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" \
    "$CREATE_QUERY_BNF_IDENTIFIER_CONT" "$CREATE_QUERY_BNF_IDENTIFIER_MANIFESTATIONS" \
    "$CREATE_QUERY_BNF_ISNI" "$CREATE_QUERY_BNF_VIAF" "$CREATE_QUERY_BNF_WIKIDATA"

}

# -----------------------------------------------------------------------------
function loadWikidata {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # first delete content of the named graph in case it already exists
  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_WIKIDATA>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_WIKIDATA"

  local wikidataTurtle="$integrationName/wikidata/rdf/$SUFFIX_WIKIDATA_LD"
  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  echo "Load wikidata data"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph $TRIPLE_STORE_GRAPH_WIKIDATA $wikidataTurtle
}

# -----------------------------------------------------------------------------
function loadMasterData {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # first delete content of the named graph in case it already exists
  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_MASTER>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_MASTER"

  local masterDataTurtle="$integrationName/master-data/rdf/$SUFFIX_MASTER_LD"
  local masterDataLanguages="$integrationName/master-data/$SUFFIX_MASTER_LANGUAGES"
  local masterDataCountries="$integrationName/master-data/$SUFFIX_MASTER_COUNTRIES"
  local masterDataGender="$integrationName/master-data/$SUFFIX_MASTER_GENDER"

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  echo "Load master data (mapped content, countries, languages and gender information)"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_MASTER" \
    "$masterDataTurtle" "$masterDataCountries" "$masterDataLanguages" "$masterDataGender"

}

# -----------------------------------------------------------------------------
function loadNationalityFromBnFViaISNI {
  local integrationName=$1


  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  local bnfContributorData="$integrationName/bnfisni/rdf/$SUFFIX_BNFISNI_CONT_LD"
  local bnfContributorIsniData="$integrationName/bnfisni/rdf/$SUFFIX_BNF_CONT_ISNI_LD"
  local bnfContributorVIAFData="$integrationName/bnfisni/rdf/$SUFFIX_BNF_CONT_VIAF_LD"
  local bnfContributorWikidataData="$integrationName/bnfisni/rdf/$SUFFIX_BNF_CONT_WIKIDATA_LD"

  # we should NOT delete the target graph, because the target graph are the BnF contributors
  # this step simply adds other data to the BnF contributors

  echo "Load newly identified BnF contributors to provide missing nationalities ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_CONT" "$bnfContributorData"


  echo "Load external links of newly identified BnF contributors - ISNI ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_CONT_ISNI" "$bnfContributorIsniData"

  echo "Load external links of newly identified BnF contributors - VIAF ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_CONT_VIAF" "$bnfContributorVIAFData"

  echo "Load external links of newly identified BnF contributors - WIKIDATA ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_CONT_WIKIDATA" "$bnfContributorWikidataData"

  echo "Add dcterms:identifier to newly identified BnF contributors and add ISNI/VIAF/Wikidata identifier according to the bibframe vocabulary"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" \
    "$CREATE_QUERY_BNF_IDENTIFIER_CONT" "$CREATE_QUERY_BNF_ISNI" \
    "$CREATE_QUERY_BNF_VIAF" "$CREATE_QUERY_BNF_WIKIDATA"

}

# -----------------------------------------------------------------------------
function checkFile {
  if [ ! -f "$1" ];
  then
    echo "File '$1' does not exist"
    exit 1
  fi
}

# -----------------------------------------------------------------------------
function cleanTranslations {
  local input=$1
  local output=$2

  checkFile $input
  python $SCRIPT_CLEAN_TRANSLATIONS -i $input -o $output
}

# -----------------------------------------------------------------------------
function cleanAgents {
  local input=$1
  local output=$2

  checkFile $input
  python $SCRIPT_CLEAN_AGENTS -i $input -o $output -d ';'
}

# -----------------------------------------------------------------------------
function extractCSVFromXMLTranslations {
  local inputXML=$1
  local outputCSVWorks=$2
  local outputCSVContributors=$3
  local outputCollectionLinks=$4

  checkFile $inputXML
  python $SCRIPT_TRANSFORM_TRANSLATIONS -i $inputXML -w $outputCSVWorks -c $outputCSVContributors -l $outputCollectionLinks
}

# -----------------------------------------------------------------------------
function normalizeCSVHeaders {
  local input=$1
  local output=$2
  local headerConversionTable=$3

  checkFile $input
  checkFile $headerConversionTable
  python $SCRIPT_NORMALIZE_HEADERS -i $input -o $output -m $headerConversionTable -d ';'
}

# -----------------------------------------------------------------------------
function extractIdentifiedAuthorities {
  local input=$1
  local output=$2

  checkFile $input
  . $SCRIPT_EXTRACT_IDENTIFIED_AUTHORITIES $input $output
}

# -----------------------------------------------------------------------------
function extractBBEntries {
  local input=$1
  local output=$2

  extractSeparatedColumn $input $output "KBRID" "belgianBibliography" "KBRID" "bbURI"
}

# -----------------------------------------------------------------------------
function extractPubCountries {
  local input=$1
  local output=$2

  extractSeparatedColumn $input $output "KBRID" "countryOfPublication" "KBRID" "pubCountryURI"
}

# -----------------------------------------------------------------------------
function extractPubPlaces {
  local input=$1
  local output=$2

  extractSeparatedColumn $input $output "KBRID" "placeOfPublication" "KBRID" "place"
}

# -----------------------------------------------------------------------------
function extractISBN10 {
  local input=$1
  local output=$2

  extractSeparatedColumn $input $output "KBRID" "isbn10" "KBRID" "isbn10"
}

# -----------------------------------------------------------------------------
function extractISBN13 {
  local input=$1
  local output=$2

  extractSeparatedColumn $input $output "KBRID" "isbn13" "KBRID" "isbn13"
}


# -----------------------------------------------------------------------------
function extractSeparatedColumn {
  local input=$1
  local output=$2
  local inputIDCol=$3
  local inputValueCol=$4
  local outputIDCol=$5
  local outputValueCol=$6

  checkFile $input
  python $SCRIPT_EXTRACT_SEPARATED_COL -i $input -o $output --input-id-column-name $inputIDCol --input-value-column-name $inputValueCol --output-id-column-name $outputIDCol --output-value-column-name $outputValueCol
}


# -----------------------------------------------------------------------------
function getSubjects {
  local input=$1
  local config=$2
  local output=$3

  python -m $MODULE_GET_RDF_XML_SUBJECTS -i $input -o $output -f $config
  #echo "python $SCRIPT_GET_RDF_XML_SUBJECTS -i $input -o $output -f $config"
}

# -----------------------------------------------------------------------------
function uploadData {
  local namespace=$1
  local fileToUpload=$2
  local format=$3
  local endpoint=$4
  local namedGraph=$5

  checkFile $fileToUpload

  echo . $SCRIPT_UPLOAD_DATA "$namespace" "$fileToUpload" "$format" "$endpoint" "$namedGraph"
  . $SCRIPT_UPLOAD_DATA "$namespace" "$fileToUpload" "$format" "$endpoint" "$namedGraph"
}

# -----------------------------------------------------------------------------
function deleteNamedGraph {
  local namespace=$1
  local endpoint=$2
  local namedGraph=$3

  local url="$endpoint/namespace/$namespace/sparql"
  echo "Delete existing content in namespace <$namedGraph> (url $url)"

  source ./py-integration-env/bin/activate
  python delete_named_graph.py -u "$url" --named-graph "$namedGraph"

  #. $SCRIPT_DELETE_NAMED_GRAPH "$namespace" "$endpoint" "$namedGraph"
}

# -----------------------------------------------------------------------------
function queryDataBlazegraph {
  local namespace=$1
  local queryFile=$2
  local endpoint=$3
  local outputFile=$4

  local queryURL="$endpoint/namespace/$namespace/sparql"
  source ./py-integration-env/bin/activate

#  . $SCRIPT_QUERY_DATA "$namespace" "$queryFile" "$endpoint" "$outputFile"
#  . $SCRIPT_QUERY_DATA "$endpoint/namespace/$namespace/sparql" "$queryFile" "$outputFile"
  python query_data.py -u "$queryURL" -q "$queryFile" -o "$outputFile"

}

# -----------------------------------------------------------------------------
function queryData {
  local url=$1
  local queryFile=$2
  local outputFile=$3

  source ./py-integration-env/bin/activate
  python query_data.py -u "$url" -q "$queryFile" -o "$outputFile"
}

# -----------------------------------------------------------------------------
function postprocessIntegratedData {

  local kbrInput=$1
  local bnfInput=$2
  local output=$3

  checkFile $kbrInput
  checkFile $bnfInput
  python $SCRIPT_POSTPROCESS_QUERY_RESULT -k "$kbrInput" -b "$bnfInput" -o "$output"

}

# -----------------------------------------------------------------------------
function postprocessContributorData {

  local input=$1
  local output=$2

  checkFile $input
  python $SCRIPT_POSTPROCESS_QUERY_CONT_RESULT -i "$input" -o "$output"

}

#
#
# BEGIN OF THE SCRIPT: CHECK COMMAND AND EXECUTE RESPECTIVE FUNCTIONS
#
#
if [ "$#" -ne 3 ];
then
  echo "use 'bash integrate-data.sh <command> <data source> <integration folder name>, whereas command are combinations of"
  echo "extract (e) transform (t) load (l)  integrate (i) query (q) and postprocess (p): 'etl', 'etliq', 'etliqp', 'e', 'et', 't', 'l', 'tl', 'q', 'i' etc"
  exit 1
else
  if [ "$1" = "etliqp" ];
  then
    extract $2 $3
    transform $2 $3
    load $2 $3
    integrate $3
    query $3
    postprocess $3

  elif [ "$1" = "etlq" ];
  then
    extract $2 $3
    transform $2 $3
    load $2 $3
    query $3

  elif [ "$1" = "tlq" ];
  then
    transform $2 $3
    load $2 $3
    query $3

  elif [ "$1" = "tlqp" ];
  then
    transform $2 $3
    load $2 $3
    query $3
    postprocess $3

  elif [ "$1" = "lq" ];
  then
    load $2 $3
    query $3

  elif [ "$1" = "lqp" ];
  then
    load $2 $3
    query $3
    postprocess $3

  elif [ "$1" = "qp" ];
  then
    query $3
    postprocess $3

  elif [ "$1" = "q" ];
  then
    query $3

  elif [ "$1" = "p" ];
  then
    postprocess $3

  elif [ "$1" = "etl" ];
  then
    extract $2 $3
    transform $2 $3
    load $2 $3

  elif [ "$1" = "etli" ];
  then
    extract $2 $3
    transform $2 $3
    load $2 $3
    integrate $3

  elif [ "$1" = "iqp" ];
  then
    integrate $2 $3
    query $3
    postprocess $3

  elif [ "$1" = "tliqp" ];
  then
    transform $2 $3
    load $2 $3
    integrate $2 $3
    query $3
    postprocess $3

  elif [ "$1" = "e" ];
  then
    extract $2 $3

  elif [ "$1" = "et" ];
  then 
    extract $2 $3
    transform $2 $3

  elif [ "$1" = "t" ];
  then
    transform $2 $3

  elif [ "$1" = "l" ];
  then
    load $2 $3

  elif [ "$1" = "i" ];
  then
    integrate $3
  elif [ "$1" = "tl" ];
  then
    transform $2 $3
    load $2 $3

  else
    echo "uknown command, please use different combinations of extract (e) transform (t) load (l) query (q) and postprocess (p): 'etl', 'etlq', 'etlqp', 'e', 'et', 't', 'l', 'tl', 'q' etc"
    exit 1
  fi
fi
