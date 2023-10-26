#!/bin/bash

# Make the locally developed python package accessible via python -m 
export PYTHONPATH=/home/slieber/repos/kbr/beltrans-data

SCRIPT_CLEAN_TRANSLATIONS="../data-sources/kbr/clean-marc-slim.py"
SCRIPT_CLEAN_AGENTS="../data-sources/kbr/pre-process-kbr-authors.py"
SCRIPT_EXTRACT_AGENTS_ORGS="../data-sources/kbr/authority-orgs-marc-to-csv.py"
SCRIPT_EXTRACT_AGENTS_PERSONS="../data-sources/kbr/authority-persons-marc-to-csv.py"
SCRIPT_TRANSFORM_TRANSLATIONS="../data-sources/kbr/marc-to-csv.py"
MODULE_NORMALIZE_HEADERS="tools.csv.replace-headers"
SCRIPT_CHANGE_PUBLISHER_NAME="../data-sources/kbr/change-publisher-name.py"
SCRIPT_EXTRACT_IDENTIFIED_AUTHORITIES="../data-sources/kbr/get-identified-authorities.sh"
SCRIPT_EXTRACT_SEPARATED_COL="../data-sources/kbr/extract-and-normalize-separated-strings.py"
SCRIPT_DEDUPLICATE_KBR_PUBLISHERS="../data-sources/kbr/deduplicate-publishers.py"

SCRIPT_GET_KBR_RECORDS="../data-sources/kbr/get-kbr-records.py"

MODULE_COMPLETE_SEQUENCE_NUMBERS="tools.csv.complete_sequence_numbers"

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

SCRIPT_INTERLINK_DATA="interlink_named_graph_data_single_update.py"

MODULE_GET_RDF_XML_SUBJECTS="tools.xml.get-subjects"
SCRIPT_GET_RDF_XML_OBJECTS="../data-sources/bnf/get-objects.py"
MODULE_EXTRACT_COLUMNS="tools.csv.extract_columns"

MODULE_NORMALIZE_1_N_COLUMNS="tools.csv.normalize_1_n_relationship"

# the following script is an older deprecated version of the script above
SCRIPT_EXTRACT_COLUMN="../data-sources/bnf/extractColumn.py" 

MODULE_FILTER_RDF_XML_SUBJECTS="tools.xml.filter-subjects-xml" 

SCRIPT_UNION_IDS="../data-sources/bnf/union.py"

SCRIPT_PARSE_UNESCO_HTML="../data-sources/unesco/parse-content.py"
MODULE_EXTRACT_UNIQUE_UNESCO_CONTRIBUTORS="tools.csv.count_unique_values"
MODULE_GROUP_BY="tools.csv.group_by"

SCRIPT_UPLOAD_DATA="../utils/upload-data.sh"
SCRIPT_DELETE_NAMED_GRAPH="../utils/delete-named-graph.sh"
SCRIPT_QUERY_DATA="../utils/query-data.sh"
SCRIPT_POSTPROCESS_QUERY_RESULT="post-process-integration-result.py"
SCRIPT_POSTPROCESS_AGG_QUERY_RESULT="post-process-manifestations.py"
SCRIPT_POSTPROCESS_QUERY_CONT_RESULT="post-process-contributors.py"
SCRIPT_POSTPROCESS_DERIVE_COUNTRIES="add_country.py"
SCRIPT_POSTPROCESS_GET_GEONAME_PLACE_OF_PUBLICATION="add_coordinates.py"
MODULE_POSTPROCESS_SORT_COLUMN_VALUES="tools.csv.sort_values_in_columns"


BNF_FILTER_CONFIG_CONTRIBUTORS="../data-sources/bnf/filter-config-beltrans-contributor-nationality.csv"
BNF_CSV_HEADER_CONVERSION="../data-sources/bnf/export-headers-mapping.csv"
KBR_CSV_HEADER_CONVERSION="../data-sources/kbr/author-headers.csv"

# #############################################################################
#
# INPUT FILENAMES
#

# KBR - translations
#INPUT_KBR_TRL_NL="../data-sources/kbr/translations/KBR_1970-2020_NL-FR_2022-02-17_4745records.xml"
#INPUT_KBR_TRL_FR="../data-sources/kbr/translations/KBR_1970-2020_FR-NL_2022-02-17_13126records.xml"
INPUT_KBR_TRL_NL="../data-sources/kbr/translations/KBR_1970-2020_NL-FR_2023-10-06.xml"
INPUT_KBR_TRL_FR="../data-sources/kbr/translations/KBR_1970-2020_FR-NL_2023-10-06.xml"

INPUT_KBR_TRL_ORIG_NL_FR="../data-sources/kbr/translations/originals/BELTRANS_NL-FR_NL-gelinkte-documenten.xml"
INPUT_KBR_TRL_ORIG_FR_NL="../data-sources/kbr/translations/originals/BELTRANS_FR-NL_FR-gelinkte-documenten.xml"

INPUT_KBR_ORGS_LOOKUP="../data-sources/kbr/agents/aorg.csv"

# KBR - linked authorities
INPUT_KBR_LA_PERSON_NL="../data-sources/kbr/agents/ExportSyracuse_Autoriteit_20231006_NL-FR_APEP.xml"
INPUT_KBR_LA_ORG_NL="../data-sources/kbr/agents/ExportSyracuse_Autoriteit_20231006_NL-FR_AORG.xml"
INPUT_KBR_LA_PERSON_FR="../data-sources/kbr/agents/ExportSyracuse_Autoriteit_20231006_FR-NL_APEP.xml"
INPUT_KBR_LA_ORG_FR="../data-sources/kbr/agents/ExportSyracuse_Autoriteit_20231006_FR-NL_AORG.xml"

INPUT_KBR_LA_PLACES_VLG="../data-sources/kbr/agents/publisher-places-VLG.csv"
INPUT_KBR_LA_PLACES_WAL="../data-sources/kbr/agents/publisher-places-WAL.csv"
INPUT_KBR_LA_PLACES_BRU="../data-sources/kbr/agents/publisher-places-BRU.csv"

INPUT_KBR_PBL_REPLACE_LIST="../data-sources/kbr/agents/publisher-name-mapping.csv"

# KBR - Belgians
INPUT_KBR_BELGIANS="../data-sources/kbr/agents/ExportSyracuse_ANAT-Belg_2023-10-06.xml"

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
INPUT_BNF_TRL_ORIGINAL_LIST_FR_NL="../data-sources/bnf/Bnf_FR-NL_1970-2020_598notices_source-titles.csv"
INPUT_BNF_TRL_ORIGINAL_LIST_NL_FR="../data-sources/bnf/Bnf_NL-FR_1970-2020_3770notices_source-titles.csv"

INPUT_BNF_RAMEAU_SUBJECT_CLASSIFICATION="../data-sources/bnf/rameau-subject-classifications"
INPUT_BNF_RAMEAU_FILENAME_PATTERN="../data-sources/bnf/rameau/databnf_rameau_nosubjects__skos*"


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

# UNESCO INDEX TRANSLATIONUM
INPUT_UNESCO_HTML_DIR_FR_NL="../data-sources/unesco/2023-01-06_FR-NL_lg-0_sl-fra_l-nld_from-1970_to-2020"
INPUT_UNESCO_HTML_DIR_NL_FR="../data-sources/unesco/2023-01-06_NL-FR_lg-0_sl-nld_l-fra_from-1970_to-2020"

INPUT_UNESCO_ENRICHED_FR_NL="../data-sources/unesco/beltrans_FR-NL_index-translationum_11899.csv"
INPUT_UNESCO_ENRICHED_NL_FR="../data-sources/unesco/beltrans_NL-FR_index-translationum_3349.csv"
INPUT_UNESCO_ENRICHED_ISBN10_FR_NL="../data-sources/unesco/beltrans_FR-NL_index-translationum_isbn10.csv"
INPUT_UNESCO_ENRICHED_ISBN13_FR_NL="../data-sources/unesco/beltrans_FR-NL_index-translationum_isbn13.csv"
INPUT_UNESCO_ENRICHED_ISBN10_NL_FR="../data-sources/unesco/beltrans_NL-FR_index-translationum_isbn10.csv"
INPUT_UNESCO_ENRICHED_ISBN13_NL_FR="../data-sources/unesco/beltrans_NL-FR_index-translationum_isbn13.csv"

INPUT_CORRELATION="../data-sources/correlation/2023-10-06_person-contributors-correlation-list.csv"
INPUT_CORRELATION_TRANSLATIONS="../data-sources/correlation/2023-10-06_translations_correlation-list.csv"


# #############################################################################

#
# CONFIGURATION
#
#

#TRIPLE_STORE_GRAPH_INT_TRL="http://beltrans-manifestations"
#TRIPLE_STORE_GRAPH_INT_CONT="http://beltrans-contributors"

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
TRIPLE_STORE_GRAPH_BNF_TRL_ORIG="http://bnf-originals"
TRIPLE_STORE_GRAPH_BNF_TRL_RAMEAU_LINKS="http://bnf-trl-rameau-links"
TRIPLE_STORE_GRAPH_RAMEAU="http://rameau"
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
TRIPLE_STORE_GRAPH_UNESCO="http://unesco"
TRIPLE_STORE_GRAPH_UNESCO_ORIG="http://unesco-originals"
TRIPLE_STORE_GRAPH_UNESCO_LA="http://unesco-linked-authorities"
TRIPLE_STORE_GRAPH_WORKS="http://beltrans-works"

TRIPLE_STORE_GRAPH_KBR_PBL_MATCHES="http://kbr-publisher-matches"

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
CREATE_QUERY_BNF_GENDER="sparql-queries/create-bnf-contributors-gender.sparql"
CREATE_QUERY_BNF_MANIFESTATIONS_BIBFRAME="sparql-queries/create-bnf-bibframe-identifiers.sparql"

CREATE_QUERY_KB_TRL_PBL="sparql-queries/link-kb-translations-to-publishers.sparql"
CREATE_QUERY_KB_PBL_IDENTIFIERS="sparql-queries/create-kb-org-identifier.sparql"

CREATE_QUERY_BIBFRAME_TITLES="sparql-queries/create-bibframe-titles.sparql"
CREATE_QUERY_SCHEMA_TITLES="sparql-queries/derive-single-title-from-bibframe-titles.sparql"

ANNOTATE_QUERY_BELTRANS_CORPUS="sparql-queries/annotate-beltrans-corpus.sparql"

CREATE_QUERY_CORRELATION_DATA="sparql-queries/add-contributors-local-data.sparql"

LINK_QUERY_CONTRIBUTORS="integration_queries/link-beltrans-manifestations-contributors.sparql"

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

POSTPROCESS_SPARQL_QUERY_TRL="sparql-queries/integrated-data-postprocessing.sparql"

SUFFIX_DATA_PROFILE_POSTPROCESS_TRL="postprocessing-input.csv"

SUFFIX_DATA_PROFILE_CONT_PERSONS_ALL_DATA_FILE="contributors-persons-all-info.csv"
SUFFIX_DATA_PROFILE_CONT_PERSONS_ALL_DATA_FILE_SORTED="contributors-persons-all-info-sorted.csv"
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
SUFFIX_DATA_PROFILE_FILE_ENRICHED_SORTED="integrated-data-enriched-sorted.csv"
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
SUFFIX_KBR_TRL_CLEANED="translations-cleaned.xml"
SUFFIX_KBR_TRL_WORKS="translations-works.csv"
SUFFIX_KBR_TRL_CONT="translations-contributors.csv"
SUFFIX_KBR_TRL_CONT_REPLACE="translations-contributors-replaced.csv"
SUFFIX_KBR_TRL_CONT_DEDUP="translations-contributors-deduplicated.csv"
SUFFIX_KBR_TRL_NEWAUT="translations-identified-authorities.csv"
SUFFIX_KBR_TRL_BB="translations-bb.csv"
SUFFIX_KBR_TRL_PUB_COUNTRY="translations-pub-country.csv"
SUFFIX_KBR_TRL_PUB_PLACE="translations-pub-place.csv"
SUFFIX_KBR_TRL_COL_LINKS="collection-links.csv"

SUFFIX_KBR_PBL_NO_MATCHES="publishers-no-matches.csv"
SUFFIX_KBR_PBL_MULTIPLE_MATCHES="publishers-multiple-matches.csv"


SUFFIX_KBR_TRL_ISBN10="isbn10.csv"
SUFFIX_KBR_TRL_ISBN13="isbn13.csv"

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
SUFFIX_KBR_LA_PERSONS_FR_NAMES="fr-translations-linked-authorities-names.csv"
SUFFIX_KBR_LA_PERSONS_NL_NAMES="nl-translations-linked-authorities-names.csv"
SUFFIX_KBR_LA_PERSONS_FR_NAMES_COMPLETE="fr-translations-linked-authorities-names-complete.csv"
SUFFIX_KBR_LA_PERSONS_NL_NAMES_COMPLETE="nl-translations-linked-authorities-names-complete.csv"

SUFFIX_KBR_LA_PERSONS_NL_IDENTIFIERS="nl-translations-linked-authorities-identifiers-persons.csv"
SUFFIX_KBR_LA_PERSONS_FR_IDENTIFIERS="fr-translations-linked-authorities-identifiers-persons.csv"
SUFFIX_KBR_LA_ORGS_NL_IDENTIFIERS="nl-translations-linked-authorities-identifiers-orgs.csv"
SUFFIX_KBR_LA_ORGS_FR_IDENTIFIERS="fr-translations-linked-authorities-identifiers-orgs.csv"

SUFFIX_KBR_BELGIANS_CSV="kbr-belgians.csv"
SUFFIX_KBR_BELGIANS_NATIONALITIES="kbr-belgians-nationalities.csv"
SUFFIX_KBR_BELGIANS_NAMES="kbr-belgians-names.csv"
SUFFIX_KBR_BELGIANS_NAMES_COMPLETE="kbr-belgians-names-complete.csv"
SUFFIX_KBR_BELGIANS_IDENTIFIERS="kbr-belgians-identifiers.csv"


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
SUFFIX_BNF_TRL_IDS_ABOUT="bnf-translation-ids-about.csv"

SUFFIX_BNF_TRL_ORIG_FR_NL="bnf-originals-fr-nl.csv"
SUFFIX_BNF_TRL_ORIG_NORM_FR_NL="bnf-originals-fr-nl-normalized.csv"
SUFFIX_BNF_TRL_ORIG_NL_FR="bnf-originals-nl-fr.csv"
SUFFIX_BNF_TRL_ORIG_NORM_NL_FR="bnf-originals-nl-fr-normalized.csv"

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

# DATA SOURCE - UNESCO INDEX TRANSLATIONUM
#
SUFFIX_UNESCO_ENRICHED="unesco_translations.csv"
SUFFIX_UNESCO_ENRICHED_CONT="unesco-contributions.csv"
SUFFIX_UNESCO_ENRICHED_ISBN10="unesco-isbn10.csv"
SUFFIX_UNESCO_ENRICHED_ISBN13="unesco-isbn13.csv"
SUFFIX_UNESCO_UNIQUE_CONTRIBUTORS="unesco-unique-contributors.csv"

SUFFIX_UNESCO_TRANSLATIONS_LD="unesco-translation-data.ttl"
SUFFIX_UNESCO_TRANSLATIONS_LIMITED_ORIGINAL_LD="unesco-limited-original-data.ttl"
SUFFIX_UNESCO_ISBN_LD="unesco-isbn.ttl"
SUFFIX_UNESCO_AUTHORITIES_LD="unesco-linked-authorities.ttl"


# DATA SOURCE - BNFISNI enrichment
#
SUFFIX_BNFISNI_IDENTIFIERS_ISNI="isni-identifiers-without-nationality.csv"
SUFFIX_BNFISNI_CONFIG_ISNI_EXTRACTION="config-bnf-isni-extraction.csv"
SUFFIX_BNFISNI_IDENTIFIERS_BNF="bnf-identifiers.csv"
SUFFIX_BNFISNI_CONT_LD="bnf-data-of-missing-nationalities.xml"

#
# CORRELATIONS
#
SUFFIX_CORRELATION="correlation-entities"
SUFFIX_CORRELATION_NATIONALITY="correlation-persons-nationalities.csv"
SUFFIX_CORRELATION_KBR="correlation-persons-kbr.csv"
SUFFIX_CORRELATION_BNF="correlation-persons-bnf.csv"
SUFFIX_CORRELATION_NTA="correlation-persons-nta.csv"
SUFFIX_CORRELATION_UNESCO="correlation-persons-unesco.csv"
SUFFIX_CORRELATION_ISNI="correlation-persons-isni.csv"

SUFFIX_CORRELATION_UNESCO_LONG="correlation-persons-unesco-long.csv"
SUFFIX_CORRELATION_VIAF="correlation-persons-viaf.csv"
SUFFIX_CORRELATION_WIKIDATA="correlation-persons-wikidata.csv"
SUFFIX_CORRELATION_PSEUDONYM="correlation-persons-pseudonym.csv"
SUFFIX_CORRELATION_REAL_NAME="correlation-persons-real-name.csv"

SUFFIX_CORRELATION_TRL="correlation-translation-entities"
SUFFIX_CORRELATION_TRL_ISBN10="correlation-trl-isbn10.csv"
SUFFIX_CORRELATION_TRL_ISBN13="correlation-trl-isbn13.csv"
SUFFIX_CORRELATION_TRL_KBR="correlation-trl-kbr-id.csv"
SUFFIX_CORRELATION_TRL_BNF="correlation-trl-bnf-id.csv"
SUFFIX_CORRELATION_TRL_KB="correlation-trl-kb-id.csv"
SUFFIX_CORRELATION_TRL_UNESCO="correlation-trl-unesco-id.csv"
SUFFIX_CORRELATION_TRL_KBR_ORIGINAL_XML="correlation-original-kbr.xml"
SUFFIX_CORRELATION_TRL_SOURCE_LANG="correlation-trl-source-lang.csv"
SUFFIX_CORRELATION_TRL_TARGET_LANG="correlation-trl-target-lang.csv"

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

SUFFIX_KBR_PERSONS_NAMES_FR_NL_LD="fr-nl_persons-names.ttl"
SUFFIX_KBR_PERSONS_NAMES_NL_FR_LD="nl-fr_persons-names.ttl"
SUFFIX_KBR_PERSONS_NAMES_BELGIANS_LD="belgians-names.ttl"

SUFFIX_KBR_PBL_MULTIPLE_MATCHES_FR_NL_LD="fr-nl_orgs-multiple-matches.ttl"
SUFFIX_KBR_PBL_MULTIPLE_MATCHES_NL_FR_LD="nl-fr_orgs-multiple-matches.ttl"

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

SUFFIX_BNF_TRL_ORIG_LD="bnf-limited-originals.ttl"
SUFFIX_BNF_TRL_ORIG_LINKS_LD="bnf-limited-originals-links.ttl"


SUFFIX_BNF_TRL_RAMEAU="bnf-translations-rameau-classifications.xml"

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

#
# LINKED DATA - CORRELATION
#
SUFFIX_CORRELATION_LD="correlation-person-entities.ttl"

SUFFIX_CORRELATION_TRL_LD="correlation-translation-entities.ttl"

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
  elif [ "$dataSource" = "rameau" ];
  then
    extractRameau $integrationFolderName
  elif [ "$dataSource" = "wikidata" ];
  then
    extractWikidata $integrationFolderName
  elif [ "$dataSource" = "original-links-kbr" ];
  then
    extractOriginalLinksKBR $integrationFolderName "original-links-kbr" "kbr" "kbr-originals"
  elif [ "$dataSource" = "bnfisni" ];
  then
    extractNationalityFromBnFViaISNI $integrationFolderName
  elif [ "$dataSource" = "unesco" ];
  then
    extractUnesco $integrationFolderName
  elif [ "$dataSource" = "person-correlation" ];
  then
    extractContributorCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "translation-correlation" ];
  then
    extractTranslationCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "all" ];
  then
    extractKBR $integrationFolderName
    extractKBROriginals $integrationFolderName
    extractKB $integrationFolderName
    extractBnF $integrationFolderName
    extractMasterData $integrationFolderName
    extractWikidata $integrationFolderName
    extractNationalityFromBnFViaISNI $integrationFolderName
    extractUnesco $integrationFolderName
    extractContributorCorrelationList "$integrationFolderName"
    extractTranslationCorrelationList "$integrationFolderName"
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
  elif [ "$dataSource" = "unesco" ];
  then
    transformUnesco $integrationFolderName
  elif [ "$dataSource" = "person-correlation" ];
  then 
    transformContributorCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "translation-correlation" ];
  then
    transformTranslationCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "all" ];
  then
    transformKBR $integrationFolderName
    transformKBROriginals $integrationFolderName
    transformKB $integrationFolderName
    transformBnF $integrationFolderName
    transformMasterData $integrationFolderName
    transformWikidata $integrationFolderName
    transformNationalityFromBnFViaISNI $integrationFolderName
    transformUnesco $integrationFolderName
    transformContributorCorrelationList "$integrationFolderName"
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
  elif [ "$dataSource" = "unesco" ];
  then
    loadUnesco $integrationFolderName
  elif [ "$dataSource" = "person-correlation" ];
  then
    loadContributorCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "translation-correlation" ];
  then
    loadTranslationCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "all" ];
  then
    loadMasterData $integrationFolderName
    loadBnF $integrationFolderName
    loadKBR $integrationFolderName
    loadKB $integrationFolderName
    loadWikidata $integrationFolderName
    loadNationalityFromBnFViaISNI $integrationFolderName
    loadUnesco $integrationFolderName
    loadContributorCorrelationList "$integrationFolderName"
  fi

}
# -----------------------------------------------------------------------------
function integrate {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  mkdir -p "$integrationName/integration"

  createManifestationsQueries="config-integration-manifestations-create.csv"
  createContributorsQueries="config-integration-contributors-create.csv"
  updateManifestationsQueries="config-integration-manifestations-single-update.csv"
  updateContributorsQueries="config-integration-contributors-single-update.csv"

  queryLogDir="$integrationName/integration"

  integrationNamespace="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"
  source ./py-integration-env/bin/activate

  # first delete content of the named graph in case it already exists
  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_INT_TRL>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_INT_TRL"

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_INT_CONT>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_INT_CONT"

  echo "Create title/subtitles according to the BIBFRAME ontology for records which do not yet have those"
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_BIBFRAME_TITLES"

  #
  # schema:name properties have to exist as they are required in the triple pattern for the data integration
  #
  echo "Create schema:name properties based on BIBFRAME titles/subtitles for records which do not yet have schema:name"
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_SCHEMA_TITLES"

  #
  # CREATE CORRELATION LIST ENTRIES BEFORE THE AUTOMATIC INTEGRATION
  #
  # Contributors
  #
  echo "Create BELTRANS contributors based on correlation list"
  extractContributorCorrelationList "$integrationName"
  transformContributorCorrelationList "$integrationName"
  loadContributorCorrelationList "$integrationName"

  # Translations
  #
  echo "Create BELTRANS translations based on correlation list"
  extractTranslationCorrelationList "$integrationName"
  transformTranslationCorrelationList "$integrationName"
  loadTranslationCorrelationList "$integrationName"

  #
  # AUTOMATIC INTEGRATION
  # 
  echo "Automatically integrate manifestations ..."
  python $SCRIPT_INTERLINK_DATA -u "$integrationNamespace" --query-type "manifestations" --target-graph "$TRIPLE_STORE_GRAPH_INT_TRL" \
    --create-queries $createManifestationsQueries --update-queries $updateManifestationsQueries --number-updates 2 --query-log-dir $queryLogDir

  echo "Automatically integrate contributors ..."
  python $SCRIPT_INTERLINK_DATA -u "$integrationNamespace" --query-type "contributors" --target-graph "$TRIPLE_STORE_GRAPH_INT_CONT" \
    --create-queries $createContributorsQueries --update-queries $updateContributorsQueries --number-updates 3 --query-log-dir $queryLogDir

  # 2023-05-04 perform updates which did not finish due to a network interruption
#  python interlink_updates.py -u "$integrationNamespace" --query-type "contributors" --target-graph "$TRIPLE_STORE_GRAPH_INT_CONT" \
#    --update-queries $updateContributorsQueries --number-updates 3 --query-log-dir $queryLogDir

  # 2023-05-04 perform remaining INSERT/UPDATE operations with a modified creation config (excluding already integrated sources)
#  python $SCRIPT_INTERLINK_DATA -u "$integrationNamespace" --query-type "contributors" --target-graph "$TRIPLE_STORE_GRAPH_INT_CONT" \
#    --create-queries "2023-05-04_config-integration-contributors-create.csv" --update-queries $updateContributorsQueries --number-updates 3 --query-log-dir $queryLogDir

  echo "Establish links between integrated manifestations and contributors (authors, translators, illustrators, scenarists, publishing directors, and publishers) ..."
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$LINK_QUERY_CONTRIBUTORS"

  echo "Perform Clustering ..."
  clustering "$integrationName"

  echo "Annotate manifestations relevant for BELTRANS based on nationality ..."
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$ANNOTATE_QUERY_BELTRANS_CORPUS"

  echo "Create title/subtitles according to the BIBFRAME ontology (now also for integrated BELTRANS manifestations)"
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_BIBFRAME_TITLES"

  # Disabled on 2023-06-06
  # Otherwise the clean correlation list input gets enriched with non-curated data
  #
  #echo "Add local data to integrated contributors from a correlation list"
  #python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_CORRELATION_DATA"

  #postprocessInputFileTranslations="$integrationName/csv/$SUFFIX_DATA_PROFILE_POSTPROCESS_TRL"
  #echo "Perform automatic integration postprocessing (not the postprocessing of the query results"
  #python -m tools.sparql.query_data \
  #  -u "$ENV_SPARQL_ENDPOINT_INTEGRATION" \
  #  -q $POSTPROCESS_SPARQL_QUERY_TRL \
  #  -o $postprocessInputFileTranslations



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
  integratedDataEnrichedSorted="$integrationName/csv/$SUFFIX_DATA_PROFILE_FILE_ENRICHED_SORTED"

  placeOfPublicationsGeonames="$integrationName/csv/$SUFFIX_PLACE_OF_PUBLICATION_GEONAMES"
  unknownGeonamesMapping="$SUFFIX_UNKNOWN_GEONAMES_MAPPING"

  contributorsPersonsAllData="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_PERSONS_ALL_DATA_FILE"
  contributorsPersonsAllDataSorted="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_PERSONS_ALL_DATA_FILE_SORTED"
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

  
  echo "Sort certain columns in the contributors CSV"
  time python -m $MODULE_POSTPROCESS_SORT_COLUMN_VALUES -i $contributorsPersonsAllData -o $contributorsPersonsAllDataSorted \
       -c "nationalities" -c "gender"

  echo "Postprocess contributor data ..."
  time python $SCRIPT_POSTPROCESS_QUERY_CONT_RESULT -c $contributorsPersonsAllDataSorted -m $integratedDataEnriched -o $contributorsPersons

  echo "Postprocess contributor data (keep non-contributors)..."
  time python $SCRIPT_POSTPROCESS_QUERY_CONT_RESULT -c $contributorsPersonsAllDataSorted -m $integratedDataEnriched -o $allPersons --keep-non-contributors

  echo "Sort certain columns in the manifestation CSV"
  time python -m $MODULE_POSTPROCESS_SORT_COLUMN_VALUES -i $integratedDataEnriched -o $integratedDataEnrichedSorted \
       -c "sourceLanguage" -c "targetLanguage" -c "targetPlaceOfPublication" -c "targetCountryOfPublication"


  echo "Create Excel sheet for data ..."
  time python $SCRIPT_CSV_TO_EXCEL $integratedDataEnrichedSorted $contributorsPersons $contributorsOrgs $placeOfPublicationsGeonames $allPersons $kbCodeHierarchy -s "translations" -s "person contributors" -s "org contributors" -s "geonames" -s "all persons" -s "KBCode" -o $excelData

}

# -----------------------------------------------------------------------------
function clustering {
  local integrationName=$1

  local outputDir="$integrationName/integration/clustering"
  local fileKeyComponents="$outputDir/key-components.csv"
  
  clusterInput="$outputDir/descriptive-keys.csv"
  clusters="$outputDir/found-clusters.csv"
  clustersTurtle="$outputDir/found-clusters.ttl"

  #keyComponentsSPARQLQuery="sparql-queries/clustering/get-descriptive-keys.sparql"
  keyComponentsSPARQLQuery="sparql-queries/clustering/get-descriptive-keys-all.sparql"
   

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  mkdir -p "$outputDir"

  # get components of the descriptive keys
  #
  echo "CLUSTERING - Get components of the descriptive keys"
  python -m tools.sparql.query_data \
    -u "$ENV_SPARQL_ENDPOINT_INTEGRATION" \
    -q $keyComponentsSPARQLQuery \
    -o $fileKeyComponents

  # normalize key components and create descriptive keys
  # 
  echo "CLUSTERING - Normalize key components and create descriptive keys"
  python -m tools.csv.clustering_normalization \
    -i $fileKeyComponents \
    -o $clusterInput \
    --id-column "m" \
    --column "keyPart1" \
    --column "keyPart2"

  # perform the clustering
  #
  echo "CLUSTERING - Perform the clustering"
  python -m tools.csv.clustering \
    -i $clusterInput \
    -o $clusters \
    --id-column "elementID" \
    --key-column "descriptiveKey"

  # create RDF representing the cluster assignments
  #
  echo "CLUSTERING - Create RDF"
  export RML_SOURCE_CLUSTERS=$clusters
  . map.sh clustering/cluster-assignments.yml $clustersTurtle

  # upload RDF to enable advanced querying of cluster information
  #
  echo "CLUSTERING - Delete existing cluster assignments"
  python -m tools.sparql.delete_named_graph \
    -u "$ENV_SPARQL_ENDPOINT_INTEGRATION" \
    --named-graph "$TRIPLE_STORE_GRAPH_WORKS"

  echo "CLUSTERING - Upload new data"
  python -m tools.sparql.upload_data \
    -u "$ENV_SPARQL_ENDPOINT_INTEGRATION" \
    --content-type "text/turtle" \
    --named-graph "$TRIPLE_STORE_GRAPH_WORKS" \
    $clustersTurtle

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
  mkdir -p $integrationName/kbr/book-data-and-contributions/fr-nl
  mkdir -p $integrationName/kbr/book-data-and-contributions/nl-fr
  mkdir -p $integrationName/kbr/agents/fr-nl
  mkdir -p $integrationName/kbr/agents/nl-fr

  echo "EXTRACTION - Extract and clean KBR translations data FR-NL"
  extractKBRTranslationsAndContributions "$integrationName" "kbr" "$INPUT_KBR_TRL_FR" "fr-nl"

  echo "EXTRACTION - Extract and clean KBR translations data NL-FR"
  extractKBRTranslationsAndContributions "$integrationName" "kbr" "$INPUT_KBR_TRL_NL" "nl-fr"

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
  mkdir -p $integrationName/$dataSourceName/book-data-and-contributions/fr-nl
  mkdir -p $integrationName/$dataSourceName/book-data-and-contributions/nl-fr
  mkdir -p $integrationName/$dataSourceName/agents/fr-nl
  mkdir -p $integrationName/$dataSourceName/agents/nl-fr

  echo "EXTRACTION - Extract and clean KBR originals translations data"
  extractKBRTranslationsAndContributions "$integrationName" "$dataSourceName" "$INPUT_KBR_TRL_ORIG_FR_NL" "fr-nl"
  extractKBRTranslationsAndContributions "$integrationName" "$dataSourceName" "$INPUT_KBR_TRL_ORIG_NL_FR" "nl-fr"

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
  mkdir -p $integrationName/kb/rdf

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
  queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_TRL_FR_NL_QUERY_FILE" "$kbTranslationsFRNL"

  echo "EXTRACTION - Extract KB translations NL - FR"
  queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_TRL_NL_FR_QUERY_FILE" "$kbTranslationsNLFR"

  echo "EXTRACTION - Compute formatted ISBN10 and ISBN13 identifiers FR - NL"
  time python $SCRIPT_ADD_ISBN_10_13 -i $kbTranslationsFRNL -o $kbTranslationsWithISBNFRNL

  echo "EXTRACTION - Compute formatted ISBN10 and ISBN13 identifiers NL - FR"
  time python $SCRIPT_ADD_ISBN_10_13 -i $kbTranslationsNLFR -o $kbTranslationsWithISBNNLFR


  echo "EXTRACTION - Extract KB translation contributors persons FR - NL"
  queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_CONT_PERSONS_FR_NL_QUERY_FILE" "$kbContributorsPersonsFRNL"

  echo "EXTRACTION - Extract KB translation contributors persons NL - FR"
  queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_CONT_PERSONS_NL_FR_QUERY_FILE" "$kbContributorsPersonsNLFR"

  echo "EXTRACTION - Extract KB translation authors persons FR - NL"
  queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_AUT_PERSONS_FR_NL_QUERY_FILE" "$kbAuthorsPersonsFRNL"

  echo "EXTRACTION - Extract KB translation authors persons NL - FR"
  queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_AUT_PERSONS_NL_FR_QUERY_FILE" "$kbAuthorsPersonsNLFR"


  echo "EXTRACTION - Extract KB translation contributors orgs FR - NL"
  queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_CONT_ORGS_FR_NL_QUERY_FILE" "$kbContributorsOrgsFRNL"

  echo "EXTRACTION - Extract KB translation contributors orgs NL - FR"
  queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_CONT_ORGS_NL_FR_QUERY_FILE" "$kbContributorsOrgsNLFR"

  echo "EXTRACTION - Extract KB translation authors orgs FR - NL"
  queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_AUT_ORGS_FR_NL_QUERY_FILE" "$kbAuthorsOrgsFRNL"

  echo "EXTRACTION - Extract KB translation authors orgs NL - FR"
  queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_AUT_ORGS_NL_FR_QUERY_FILE" "$kbAuthorsOrgsNLFR"


  echo "EXTRACTION - Extract KBCode classifications FR-NL"
  queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_KBCODE_FR_NL_QUERY_FILE" "$kbCodeAssignmentsFRNL"

  echo "EXTRACTION - Extract KBCode classifications NL-FR"
  queryData "$KB_SPARQL_ENDPOINT" "$GET_KB_KBCODE_NL_FR_QUERY_FILE" "$kbCodeAssignmentsNLFR"

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
function extractRameau {
  local $integrationName

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)
  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  echo "EXTRACT, TRANSFORM and LOAD the RAMEAU entities from the BnF dumps"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_RAMEAU" $INPUT_BNF_RAMEAU_FILENAME_PATTERN
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
  bnfTranslationIDsAbout="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_IDS_ABOUT"

  bnfRameauClassifications="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_RAMEAU"

  bnfNormalizedSourceAdaptedHeaderFRNL="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_ORIG_NORM_FR_NL"
  bnfNormalizedSourceAdaptedHeaderNLFR="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_ORIG_NORM_NL_FR"
  bnfNormalizedSourceFRNL="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_ORIG_FR_NL"
  bnfNormalizedSourceNLFR="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_ORIG_NL_FR"

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

  # the following command will create a CSV file with BnF catalogue URIs
  echo "EXTRACTION - Create list of both NL and FR BnF translation IDs"
  time python $SCRIPT_UNION_IDS $bnfFRNLTranslations $bnfNLFRTranslations -o $bnfTranslationIDs -d ' '

  # we replace the 'catalogue' part of the URIs with 'data',
  # because all other files in which we want to look up things have 'data' URIs
  sed -i 's/catalogue/data/' $bnfTranslationIDs

  # Mostly the expression URLs are used which have the URI with trailing '#about'
  cp $bnfTranslationIDs $bnfTranslationIDsAbout
  sed -i 's/\r$/#about/' -i $bnfTranslationIDsAbout

  # extract contributor IDs of all translation contributors (also non-Belgian contributors)
  echo "EXTRACTION - Extract all BnF contributor IDs of BELTRANS translations (despite the nationality)"
  time python $SCRIPT_GET_RDF_XML_OBJECTS -i $INPUT_BNF_CONTRIBUTIONS -o $bnfPersonsBELTRANS -l $bnfTranslationIDs -p "dcterms:contributor"

  # extract contributor IDs of all translation contributors (orgs)
  echo "EXTRACTION - Extract all BnF contributor IDs of organizations"
  time python $SCRIPT_GET_RDF_XML_OBJECTS -i $INPUT_BNF_CONTRIBUTIONS -o $bnfOrgsBELTRANS -l $bnfTranslationIDs -p "marcrel:pbl"

  # extract the actual data of all BELTRANS translations contributors - persons
  echo "EXTRACTION - Extract BnF contributor data (persons)"
  time python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_PERSON_AUTHORS -o $bnfContributorDataPersons -f $bnfPersonsBELTRANS

  # extract the actual data of all BELTRANS translations contributors - orgs
  echo "EXTRACTION - Extract BnF contributor data (orgs)"
  time python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_ORG_AUTHORS -o $bnfContributorDataOrgs -f $bnfOrgsBELTRANS
  
  # extract the actual links between publications and contributors (not just looking up things) - ALL links are taken as the subject with all properties is extracted
  echo "EXTRACTION - Extract links between BELTRANS relevant BnF publications and BnF contributors"
  time python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONTRIBUTIONS -o $bnfContributionLinksData -f $bnfBelgianPublications -f $bnfTranslationIDs

  echo "EXTRACTION - Extract links between BnF contributors and ISNI"
  time python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_ISNI -o $bnfContributorIsniData -f $bnfPersonsBELTRANS

  echo "EXTRACTION - Extract links between BnF contributors and VIAF"
  time python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_VIAF -o $bnfContributorVIAFData -f $bnfPersonsBELTRANS

  echo "EXTRACTION - Extract links between BnF contributors and Wikidata"
  time python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_WIKIDATA -o $bnfContributorWikidataData -f $bnfPersonsBELTRANS

  #
  # There are also Rameau classifications
  #
  echo "EXTRACTION - Extract links between translations and their Rameau classifications"
  time python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_RAMEAU_SUBJECT_CLASSIFICATION -o $bnfRameauClassifications -f $bnfTranslationIDsAbout

  #
  # We also have a list of source titles for BnF translations
  #
  echo "EXTRACTION - Normalize list of BnF source titles (create 1:n relations) - FR-NL"
  time python -m $MODULE_NORMALIZE_1_N_COLUMNS -i $INPUT_BNF_TRL_ORIGINAL_LIST_FR_NL -o $bnfNormalizedSourceFRNL --delimiter ';' --number-of-columns 4

  echo "EXTRACTION - Normalize list of BnF source titles (create 1:n relations) - NL-FR"
  time python -m $MODULE_NORMALIZE_1_N_COLUMNS -i $INPUT_BNF_TRL_ORIGINAL_LIST_NL_FR -o $bnfNormalizedSourceNLFR --delimiter ';' --number-of-columns 4

  echo "EXTRACTION - Normalize header names of BnF source titles list - FR-NL"
  time python -m $MODULE_NORMALIZE_HEADERS -i $bnfNormalizedSourceFRNL --delimiter ';' --header-mapping-file $BNF_CSV_HEADER_CONVERSION -o $bnfNormalizedSourceAdaptedHeaderFRNL

  echo "EXTRACTION - Normalize header names of BnF source titles list - NL-FR"
  time python -m $MODULE_NORMALIZE_HEADERS -i $bnfNormalizedSourceNLFR --delimiter ';' --header-mapping-file $BNF_CSV_HEADER_CONVERSION -o $bnfNormalizedSourceAdaptedHeaderNLFR

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
  time python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i "$INPUT_BNF_PERSON_AUTHORS"  -o "$bnfContributorData" -f "$bnfIdentifiers"

  echo "EXTRACTION - Extract links between BnF contributors and ISNI"
  time python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_ISNI -o $bnfContributorIsniData -f $bnfIdentifiers

  echo "EXTRACTION - Extract links between BnF contributors and VIAF"
  time python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_VIAF -o $bnfContributorVIAFData -f $bnfIdentifiers

  echo "EXTRACTION - Extract links between BnF contributors and Wikidata"
  time python -m $MODULE_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_WIKIDATA -o $bnfContributorWikidataData -f $bnfIdentifiers

  # We could query nationality which is used to immediately enrich integrated persons,
  # but we can also get all data of the newly found contributors to increase the overlap with other sources

}

# -----------------------------------------------------------------------------
function extractOriginalLinksKBR {
  local integrationName=$1
  local dataSourceName=$2
  local translationsSourceName=$3
  local originalsSourceName=$4

  mkdir -p "$integrationName/$dataSourceName/fr-nl"
  mkdir -p "$integrationName/$dataSourceName/nl-fr"

  local similarityThreshold="0.9"

  local kbrOriginalsNLFR="$integrationName/$originalsSourceName/book-data-and-contributions/nl-fr/$SUFFIX_KBR_TRL_WORKS"
  local kbrTranslationsNLFR="$integrationName/$translationsSourceName/book-data-and-contributions/nl-fr/$SUFFIX_KBR_TRL_WORKS"
  local titleMatchesNLFR="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_TITLE_MATCHES_NL_FR"
  local titleDuplicatesMatchesNLFR="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_TITLE_DUPLICATES_MATCHES_NL_FR"
  local similarityMatchesNLFR="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_SIMILARITY_MATCHES_NL_FR"
  local similarityDuplicatesMatchesNLFR="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_SIMILARITY_DUPLICATES_MATCHES_NL_FR"
  local similarityMultipleMatchesNLFR="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_SIMILARITY_MULTIPLE_MATCHES_NL_FR"

  local kbrOriginalsFRNL="$integrationName/$originalsSourceName/book-data-and-contributions/fr-nl/$SUFFIX_KBR_TRL_WORKS"
  local kbrTranslationsFRNL="$integrationName/$translationsSourceName/book-data-and-contributions/fr-nl/$SUFFIX_KBR_TRL_WORKS"
  local titleMatchesFRNL="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_TITLE_MATCHES_FR_NL"
  local titleDuplicatesMatchesFRNL="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_TITLE_DUPLICATES_MATCHES_FR_NL"
  local similarityMatchesFRNL="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_SIMILARITY_MATCHES_FR_NL"
  local similarityDuplicatesMatchesFRNL="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_SIMILARITY_DUPLICATES_MATCHES_FR_NL"
  local similarityMultipleMatchesFRNL="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_SIMILARITY_MULTIPLE_MATCHES_FR_NL"

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
function extractUnesco {

  local integrationName=$1

  # create the folders to place the extracted translations and agents
  mkdir -p $integrationName/unesco

  local unescoTranslations="$integrationName/unesco/$SUFFIX_UNESCO_ENRICHED"
  local unescoISBN10="$integrationName/unesco/$SUFFIX_UNESCO_ENRICHED_ISBN10"
  local unescoISBN13="$integrationName/unesco/$SUFFIX_UNESCO_ENRICHED_ISBN13"
  local unescoContributions="$integrationName/unesco/$SUFFIX_UNESCO_ENRICHED_CONT"
  local unescoUniqueContributors="$integrationName/unesco/$SUFFIX_UNESCO_UNIQUE_CONTRIBUTORS"

  echo "EXTRACTION - parse HTML translations"
  time python $SCRIPT_PARSE_UNESCO_HTML -o $unescoTranslations \
    --isbn10-file $unescoISBN10 --isbn13-file $unescoISBN13 --contribution-file $unescoContributions \
    $INPUT_UNESCO_HTML_DIR_FR_NL $INPUT_UNESCO_HTML_DIR_NL_FR

  echo "EXTRACTION - extract unique contributors"
  time python -m $MODULE_GROUP_BY -i $unescoContributions -o $unescoUniqueContributors \
    --id-column "contributorIDShort" -c "contributorID" -c "name" -c "firstname" -c "type" -c "place" -s "contributorType"

  echo "EXTRACTION - replace extracted contributor CSV with manual curated one"
  cp "../data-sources/unesco/2023-07-04_unesco-unique-contributors.csv" $unescoUniqueContributors

}

# -----------------------------------------------------------------------------
function transformKBR {

  local integrationName=$1

  # create the folder to place the transformed data
  mkdir -p $integrationName/kbr/rdf/fr-nl
  mkdir -p $integrationName/kbr/rdf/nl-fr

  echo "TRANSFORMATION - Map KBR book data and contributions to RDF - fr-nl"
  mapKBRBookInformationAndContributions $integrationName "kbr" "fr-nl"

  echo "TRANSFORMATION - Map KBR book data and contributions to RDF - nl-fr"
  mapKBRBookInformationAndContributions $integrationName "kbr" "nl-fr"

  echo "TRANSFORMATION - Map KBR translation data to RDF - FR-NL"
  mapKBRTranslationsAndContributions $integrationName "kbr" "fr-nl"

  echo "TRANSFORMATION - Map KBR translation data to RDF - NL-FR"
  mapKBRTranslationsAndContributions $integrationName "kbr" "nl-fr"

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
  mkdir -p $integrationName/$dataSourceName/rdf/fr-nl
  mkdir -p $integrationName/$dataSourceName/rdf/nl-fr

  echo "TRANSFORMATION - Map KBR translation data to RDF"
  mapKBRBookInformationAndContributions $integrationName "$dataSourceName" "fr-nl"
  mapKBRBookInformationAndContributions $integrationName "$dataSourceName" "nl-fr"

}

# -----------------------------------------------------------------------------
function transformOriginalLinksKBR {
  local integrationName=$1
  local dataSourceName=$2

  # create the folder to place the transformed data
  mkdir -p "$integrationName/$dataSourceName/rdf/fr-nl"
  mkdir -p "$integrationName/$dataSourceName/rdf/nl-fr"

  originalLinksTurtleFRNL="$integrationName/$dataSourceName/rdf/fr-nl/$SUFFIX_KBR_ORIGINAL_LINKING_LD"
  originalLinksTurtleNLFR="$integrationName/$dataSourceName/rdf/nl-fr/$SUFFIX_KBR_ORIGINAL_LINKING_LD"

  # map the translations

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_TITLE_MATCHES="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_TITLE_MATCHES_NL_FR"
  export RML_SOURCE_TITLE_DUPLICATES_MATCHES="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_TITLE_DUPLICATES_MATCHES_NL_FR"
  export RML_SOURCE_SIMILARITY_MATCHES="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_SIMILARITY_MATCHES_NL_FR"
  export RML_SOURCE_SIMILARITY_DUPLICATES_MATCHES="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_SIMILARITY_DUPLICATES_MATCHES_NL_FR"

  # 2) execute the mapping
  echo "Map KBR original linking NL-FR ..."
  . map.sh ../data-sources/kbr/kbr-original-linking.yml $originalLinksTurtleFRNL

  export RML_SOURCE_TITLE_MATCHES="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_TITLE_MATCHES_FR_NL"
  export RML_SOURCE_TITLE_DUPLICATES_MATCHES="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_TITLE_DUPLICATES_MATCHES_FR_NL"
  export RML_SOURCE_SIMILARITY_MATCHES="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_SIMILARITY_MATCHES_FR_NL"
  export RML_SOURCE_SIMILARITY_DUPLICATES_MATCHES="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_SIMILARITY_DUPLICATES_MATCHES_FR_NL"

  # 2) execute the mapping
  echo "Map KBR original linking FR-NL ..."
  . map.sh ../data-sources/kbr/kbr-original-linking.yml $originalLinksTurtleNLFR


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

  mkdir -p $integrationName/bnf/rdf 

  local bnfLimitedOriginalInformationTurtle="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_ORIG_LD"
  local bnfLimitedOriginalInformationLinksTurtle="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_ORIG_LINKS_LD"

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_BNF_TRL_ORIG_FR_NL="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_ORIG_NORM_FR_NL"
  export RML_SOURCE_BNF_TRL_ORIG_NL_FR="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_ORIG_NORM_NL_FR"

  # 2) execute the mapping
  echo "TRANSFORMATION - Map BnF translation's limited source information ..."
  . map.sh ../data-sources/bnf/bnf-translations-limited-originals.yml $bnfLimitedOriginalInformationTurtle

  echo "TRANSFORMATION - Map links from BnF translations to limited source information ..."
  . map.sh ../data-sources/bnf/bnf-original-linking.yml $bnfLimitedOriginalInformationLinksTurtle
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
  local kbrTranslations=$3
  local language=$4

  # DutchTranslations = NL-FR
  # FrenchTranslations = FR-NL


  #
  # Define file names based on current integration directory and file name patterns
  #
  kbrTranslationsCleaned="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_CLEANED"

  kbrTranslationsCSVWorks="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_WORKS"

  kbrTranslationsCSVCont="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_CONT"
  kbrTranslationsCSVContReplaced="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_CONT_REPLACE"
  kbrTranslationsCSVContDedup="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_CONT_DEDUP"

  kbrTranslationsIdentifiedAuthorities="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_NEWAUT"

  kbrTranslationsCSVBB="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_BB"

  kbrTranslationsPubCountries="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_PUB_COUNTRY"

  kbrTranslationsPubPlaces="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_PUB_PLACE"

  kbrTranslationsCollectionLinks="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_COL_LINKS"

  kbrTranslationsISBN10="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_ISBN10"
  kbrTranslationsISBN13="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_ISBN13"

  kbrNoMatches="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_PBL_NO_MATCHES"
  kbrMultipleMatches="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_PBL_MULTIPLE_MATCHES"
  
  source py-integration-env/bin/activate

  echo "Clean $language translations ... '$kbrTranslations'"
  cleanTranslations "$kbrTranslations" "$kbrTranslationsCleaned"

  echo "Extract CSV from $language translations XML..."
  extractCSVFromXMLTranslations "$kbrTranslationsCleaned" "$kbrTranslationsCSVWorks" "$kbrTranslationsCSVCont" "$kbrTranslationsCollectionLinks"

  echo "Replace publisher names to support deduplication - $language"
  python $SCRIPT_CHANGE_PUBLISHER_NAME -l $INPUT_KBR_PBL_REPLACE_LIST -i $kbrTranslationsCSVCont -o $kbrTranslationsCSVContReplaced

  echo "Deduplicate newly identified contributors - $language"
  python $SCRIPT_DEDUPLICATE_KBR_PUBLISHERS -l $INPUT_KBR_ORGS_LOOKUP -i $kbrTranslationsCSVContReplaced -o $kbrTranslationsCSVContDedup --no-matches-log $kbrNoMatches --multiple-matches-log $kbrMultipleMatches

  echo "Extract BB assignments for $language translations ..."
  extractBBEntries "$kbrTranslationsCSVWorks" "$kbrTranslationsCSVBB"

  echo "Extract publication countries from $language translations ..."
  extractPubCountries "$kbrTranslationsCSVWorks" "$kbrTranslationsPubCountries"

  echo "Extract publication places from $language translations ..."
  extractPubPlaces "$kbrTranslationsCSVWorks" "$kbrTranslationsPubPlaces"


  echo "Extract (possibly multiple) ISBN10 identifiers per translation - $language"
  extractISBN10 "$kbrTranslationsCSVWorks" "$kbrTranslationsISBN10"

  echo "Extract (possibly multiple) ISBN13 identifiers per translation - $language"
  extractISBN13 "$kbrTranslationsCSVWorks" "$kbrTranslationsISBN13"


  echo "Extract newly identified contributors $language ..."
  extractIdentifiedAuthorities "$kbrTranslationsCSVContDedup" "$kbrTranslationsIdentifiedAuthorities"


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

  kbrNLPersonsISNIs="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_NL_IDENTIFIERS"
  kbrFRPersonsISNIs="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_FR_IDENTIFIERS"
  kbrFROrgsISNIs="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_FR_IDENTIFIERS"
  kbrNLOrgsISNIs="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_NL_IDENTIFIERS"

  kbrFRPersonsNames="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_FR_NAMES"
  kbrNLPersonsNames="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_NL_NAMES"
  kbrFRPersonsNamesComplete="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_FR_NAMES_COMPLETE"
  kbrNLPersonsNamesComplete="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_NL_NAMES_COMPLETE"

  kbrBelgianPersonsNationalities="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_NATIONALITIES"
  kbrBelgianPersonsNames="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_NAMES"
  kbrBelgianPersonsNamesComplete="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_NAMES_COMPLETE"
  kbrBelgianPersonsISNIs="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_IDENTIFIERS"

  source py-integration-env/bin/activate

  echo "Extract authorities NL-FR - Persons ..."
  python $SCRIPT_EXTRACT_AGENTS_PERSONS -i $kbrNLPersons -o $kbrNLPersonsCSV -n $kbrNLPersonsNationalities --names-csv $kbrNLPersonsNames --identifier-csv $kbrNLPersonsISNIs

  echo "Extract authorities NL-FR - Organizations ..."
  python $SCRIPT_EXTRACT_AGENTS_ORGS -i $kbrNLOrgs -o $kbrNLOrgsCSV --identifier-csv $kbrNLOrgsISNIs

  echo "Extract authorities FR-NL - Persons ..."
  python $SCRIPT_EXTRACT_AGENTS_PERSONS -i $kbrFRPersons -o $kbrFRPersonsCSV -n $kbrFRPersonsNationalities --names-csv $kbrFRPersonsNames --identifier-csv $kbrFRPersonsISNIs

  echo "Extract authorities FR-NL - Organizations ..."
  python $SCRIPT_EXTRACT_AGENTS_ORGS -i $kbrFROrgs -o $kbrFROrgsCSV --identifier-csv $kbrFROrgsISNIs

  echo "Extract authorities KBR-Belgians - Persons ..."
  # these Belgians might have multiple nationalities, thus it is still important to get the nationality information
  python $SCRIPT_EXTRACT_AGENTS_PERSONS -i $kbrBelgianPersons -o $kbrBelgianPersonsCSV -n $kbrBelgianPersonsNationalities --names-csv $kbrBelgianPersonsNames --identifier-csv $kbrBelgianPersonsISNIs

  echo "Complete author names sequence numbers - FR-NL"
  python -m $MODULE_COMPLETE_SEQUENCE_NUMBERS -i $kbrNLPersonsNames -o $kbrNLPersonsNamesComplete --identifier-column "authorityID" --sequence-number-column "sequence_number"

  echo "Complete author names sequence numbers - NL-FR"
  python -m $MODULE_COMPLETE_SEQUENCE_NUMBERS -i $kbrFRPersonsNames -o $kbrFRPersonsNamesComplete --identifier-column "authorityID" --sequence-number-column "sequence_number"

  echo "Complete author names sequence numbers - KBR-Belgians"
  python -m $MODULE_COMPLETE_SEQUENCE_NUMBERS -i $kbrBelgianPersonsNames -o $kbrBelgianPersonsNamesComplete --identifier-column "authorityID" --sequence-number-column "sequence_number"

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
  local language=$3

  # map the translations

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_WORKS="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_WORKS"
  export RML_SOURCE_CONT="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_CONT_DEDUP"


  kbrTranslationsTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_TRL_LD"
  . map.sh ../data-sources/kbr/kbr-translations.yml $kbrTranslationsTurtle

}

# -----------------------------------------------------------------------------
function mapKBRBookInformationAndContributions {

  local integrationName=$1
  local dataSourceName=$2
  local language=$3

  kbrBookDataTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_BOOK_LD"
  kbrBookDataIdentifiedAuthorities="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_NEWAUT_LD"
  kbrBookDataBBTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_TRL_BB_LD"
  kbrBookDataPubCountriesTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_TRL_PUB_COUNTRY_LD"
  kbrBookDataPubPlacesTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_TRL_PUB_PLACE_LD"
  kbrBookDataISBNTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_TRL_ISBN_LD"

  # map the translations

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_WORKS="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_WORKS"
  export RML_SOURCE_CONT="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_CONT_DEDUP"
  export RML_SOURCE_COLLECTION_LINKS="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_COL_LINKS"

  # 2) execute the mapping
  echo "Map KBR book information and contributions - $language ..."
  . map.sh ../data-sources/kbr/kbr-book-data.yml $kbrBookDataTurtle


  # map newly identified publishers

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_CONT_IDENTIFIED="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_NEWAUT"

  # 2) execute the mapping
  echo "Map KBR newly identified contributors - $language ..."
  . map.sh ../data-sources/kbr/kbr-identified-authorities.yml $kbrBookDataIdentifiedAuthorities

  # map belgian bibliography assignments

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_BB="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_BB"
  
  # 2) execute the mapping
  echo "Map KBR BB assignments - $language ..."
  . map.sh ../data-sources/kbr/kbr-belgian-bibliography.yml $kbrBookDataBBTurtle

  # map publication countries

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_PUB_COUNTRIES="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_PUB_COUNTRY"

  # 2) execute the mapping
  echo "Map KBR publication countries relationships - $language ..."
  . map.sh ../data-sources/kbr/kbr-publication-countries.yml $kbrBookDataPubCountriesTurtle

  # map publication places

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_PUB_PLACES="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_PUB_PLACE"

  # 2) execute the mapping
  echo "Map KBR publication places relationships - $language ..."
  . map.sh ../data-sources/kbr/kbr-publication-places.yml $kbrBookDataPubPlacesTurtle


  # map ISBN10/ISBN13

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_ISBN10="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_ISBN10"
  export RML_SOURCE_KBR_ISBN13="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_ISBN13"

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
  export RML_SOURCE_WORKS_FR="$integrationName/$dataSourceName/book-data-and-contributions/fr-nl/$SUFFIX_KBR_TRL_WORKS"
  export RML_SOURCE_WORKS_NL="$integrationName/$dataSourceName/book-data-and-contributions/nl-fr/$SUFFIX_KBR_TRL_WORKS"

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

  kbrPersonsISNINLFR="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_NL_IDENTIFIERS"
  kbrPersonsISNIFRNL="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_FR_IDENTIFIERS"
  kbrOrgsISNIFR="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_FR_IDENTIFIERS"
  kbrOrgsISNINL="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_NL_IDENTIFIERS"

  kbrOrgsFRNL="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_FR_CLEANED"
  kbrOrgsNLFR="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_NL_CLEANED"

  kbrBelgians="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_CSV"
  kbrBelgiansNat="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_NATIONALITIES"
  kbrBelgiansISNI="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_IDENTIFIERS"

  local kbrFRPersonsNames="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_FR_NAMES_COMPLETE"
  local kbrNLPersonsNames="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_NL_NAMES_COMPLETE"
  local kbrBelgianPersonsNames="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_NAMES_COMPLETE"
 

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

  kbrPersonsNamesTurtleFRNL="$integrationName/kbr/rdf/$SUFFIX_KBR_PERSONS_NAMES_FR_NL_LD"
  kbrPersonsNamesTurtleNLFR="$integrationName/kbr/rdf/$SUFFIX_KBR_PERSONS_NAMES_NL_FR_LD"
  kbrBelgianPersonsNamesTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_PERSONS_NAMES_BELGIANS_LD"

  kbrOrgMatchesNLFR="$integrationName/$dataSourceName/kbr/agents/nl-fr/$SUFFIX_KBR_PBL_MULTIPLE_MATCHES"
  kbrOrgMatchesFRNL="$integrationName/$dataSourceName/kbr/agents/fr-nl/$SUFFIX_KBR_PBL_MULTIPLE_MATCHES"
  kbrOrgMatchesTurtleFRNL="$integrationName/kbr/rdf/$SUFFIX_KBR_PBL_MULTIPLE_MATCHES_FR_NL_LD"
  kbrOrgMatchesTurtleNLFR="$integrationName/kbr/rdf/$SUFFIX_KBR_PBL_MULTIPLE_MATCHES_NL_FR_LD"


  # 2) execute the mapping
  mapKBRPersons "$kbrPersonsFRNL" "$kbrPersonsNatFRNL" "$kbrPersonsTurtleFRNL"
  mapKBRPersons "$kbrPersonsNLFR" "$kbrPersonsNatNLFR" "$kbrPersonsTurtleNLFR"
  mapKBRPersons "$kbrBelgians" "$kbrBelgiansNat" "$kbrBelgiansTurtle"

  mapKBRNames "$kbrFRPersonsNames" "$kbrPersonsNamesTurtleFRNL"
  mapKBRNames "$kbrNLPersonsNames" "$kbrPersonsNamesTurtleNLFR"
  mapKBRNames "$kbrBelgianPersonsNames" "$kbrBelgianPersonsNamesTurtle"

  mapKBROrgs "$kbrOrgsFRNL" "$kbrOrgsTurtleFRNL"
  mapKBROrgs "$kbrOrgsNLFR" "$kbrOrgsTurtleNLFR"

  mapKBROrgMatches "$kbrOrgMatchesFRNL" "$kbrOrgMatchesTurtleFRNL"
  mapKBROrgMatches "$kbrOrgMatchesNLFR" "$kbrOrgMatchesTurtleNLFR"

  mapKBRPlaces "$integrationName" "$kbrPlacesTurtle"

  mapKBRLinkedIdentifiers "$kbrPersonsISNIFRNL" "$kbrPersonsIdentifiersTurtleFRNL"
  mapKBRLinkedIdentifiers "$kbrPersonsISNINLFR" "$kbrPersonsIdentifiersTurtleNLFR"

  mapKBRLinkedIdentifiers "$kbrOrgsISNIFR" "$kbrOrgsIdentifiersTurtleFRNL"
  mapKBRLinkedIdentifiers "$kbrOrgsISNINL" "$kbrOrgsIdentifiersTurtleNLFR"

  mapKBRLinkedIdentifiers "$kbrBelgiansISNI" "$kbrBelgiansIdentifiersTurtle"

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

  export RML_SOURCE_KBR_LINKED_AUTHORITIES_ORGS="$sourceFile"

  echo "Map KBR Orgs - $sourceFile"
  . map.sh ../data-sources/kbr/kbr-linked-authorities-orgs.yml $outputTurtle
}

# -----------------------------------------------------------------------------
function mapKBROrgMatches {
  local sourceFile=$1
  local outputTurtle=$2
 
  export RML_SOURCE_KBR_MULTIPLE_ORG_MATCHES="$sourceFile"

  echo "Map KBR Orgs possible matches - $sourceFile"
  . map.sh ../data-sources/kbr/kbr-org-matches.yml $outputTurtle
}

# -----------------------------------------------------------------------------
function mapKBRNames {
  local sourceFile=$1
  local outputTurtle=$2

  export RML_SOURCE_KBR_NAMES="$sourceFile"

  echo "Map KBR Names - $sourceFile"
  . map.sh ../data-sources/kbr/kbr-pseudonym-names.yml $outputTurtle
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
function transformUnesco {
  local integrationName=$1

  mkdir -p "$integrationName/unesco/rdf"

  local translationTurtle="$integrationName/unesco/rdf/$SUFFIX_UNESCO_TRANSLATIONS_LD"
  local translationOriginalTurtle="$integrationName/unesco/rdf/$SUFFIX_UNESCO_TRANSLATIONS_LIMITED_ORIGINAL_LD"
  local isbnTurtle="$integrationName/unesco/rdf/$SUFFIX_UNESCO_ISBN_LD"
  local authorityTurtle="$integrationName/unesco/rdf/$SUFFIX_UNESCO_AUTHORITIES_LD"

  # export environment variables used by the YARRRML mapping files
  export RML_SOURCE_WORKS_UNESCO="$integrationName/unesco/$SUFFIX_UNESCO_ENRICHED"

  export RML_SOURCE_UNESCO_ISBN10="$integrationName/unesco/$SUFFIX_UNESCO_ENRICHED_ISBN10"
  export RML_SOURCE_UNESCO_ISBN13="$integrationName/unesco/$SUFFIX_UNESCO_ENRICHED_ISBN13"
  export RML_SOURCE_UNESCO_UNIQUE_CONTRIBUTORS="$integrationName/unesco/$SUFFIX_UNESCO_UNIQUE_CONTRIBUTORS"
  export RML_SOURCE_WORKS_UNESCO_CONTRIBUTIONS="$integrationName/unesco/$SUFFIX_UNESCO_ENRICHED_CONT"

  echo "Map Unesco translation data"
  . map.sh ../data-sources/unesco/unesco-translations.yml $translationTurtle

  echo "Map Unesco translation source data based on minimal information in the translation data"
  . map.sh ../data-sources/unesco/unesco-translations-limited-originals.yml $translationOriginalTurtle

  echo "Map Unesco ISBN relationships"
  . map.sh ../data-sources/unesco/unesco-isbn.yml $isbnTurtle

  echo "Map Unesco identified contributors"
  . map.sh ../data-sources/unesco/unesco-linked-authorities.yml $authorityTurtle
}

# -----------------------------------------------------------------------------
function extractContributorCorrelationList {
  local integrationName=$1

  mkdir -p "$integrationName/correlation"

  local correlationList="$INPUT_CORRELATION"
  local correlationListNationalities="$integrationName/correlation/$SUFFIX_CORRELATION_NATIONALITY"
  local correlationListKBRIDs="$integrationName/correlation/$SUFFIX_CORRELATION_KBR"
  local correlationListBnFIDs="$integrationName/correlation/$SUFFIX_CORRELATION_BNF"
  local correlationListNTAIDs="$integrationName/correlation/$SUFFIX_CORRELATION_NTA"
  local correlationListUnescoIDs="$integrationName/correlation/$SUFFIX_CORRELATION_UNESCO"
  local correlationListISNIIDs="$integrationName/correlation/$SUFFIX_CORRELATION_ISNI"

  local correlationListUnescoLongIDs="$integrationName/correlation/$SUFFIX_CORRELATION_UNESCO_LONG"
  local correlationListVIAFIDs="$integrationName/correlation/$SUFFIX_CORRELATION_VIAF"
  local correlationListWikidataIDs="$integrationName/correlation/$SUFFIX_CORRELATION_WIKIDATA"
  local correlationListPseudonymOfIDs="$integrationName/correlation/$SUFFIX_CORRELATION_PSEUDONYM"
  local correlationListRealNameOfIDs="$integrationName/correlation/$SUFFIX_CORRELATION_REAL_NAME"

  echo "Extract 1:n relationships of different persons correlation list columns from '$correlationList'"
  cp $correlationList "$integrationName/correlation/"
  extractSeparatedColumn $correlationList $correlationListNationalities "contributorID" "nationalityCountryCodes" "id" "nationality"
  extractSeparatedColumn $correlationList $correlationListKBRIDs "contributorID" "kbrIDs" "id" "KBR"
  extractSeparatedColumn $correlationList $correlationListBnFIDs "contributorID" "bnfIDs" "id" "BnF"
  extractSeparatedColumn $correlationList $correlationListNTAIDs "contributorID" "ntaIDs" "id" "NTA"
  extractSeparatedColumn $correlationList $correlationListVIAFIDs "contributorID" "viafIDs" "id" "VIAF"
  extractSeparatedColumn $correlationList $correlationListWikidataIDs "contributorID" "wikidataIDs" "id" "wikidata"
  extractSeparatedColumn $correlationList $correlationListUnescoIDs "contributorID" "unescoIDs" "id" "unesco"
  #extractSeparatedColumn $correlationList $correlationListUnescoLongIDs "contributorID" "unescoIDsLong" "id" "unescoLong"
  extractSeparatedColumn $correlationList $correlationListISNIIDs "contributorID" "isniIDs" "id" "ISNI"
}

# -----------------------------------------------------------------------------
function extractTranslationCorrelationList {
  local integrationName=$1

  mkdir -p "$integrationName/correlation"

  local correlationList="$INPUT_CORRELATION_TRANSLATIONS"
  local correlationListISBN10="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_ISBN10"
  local correlationListISBN13="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_ISBN13"

  local correlationListKBRIDs="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_KBR"
  local correlationListBNFIDs="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_BNF"
  local correlationListKBIDs="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_KB"
  local correlationListUNESCOIDs="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_UNESCO"

  local correlationListSourceLanguage="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_SOURCE_LANG"
  local correlationListTargetLanguage="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_TARGET_LANG"

  local correlationListKBRSOURCEIDs="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_UNESCO"
  local correlationListKBROriginalXML="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_KBR_ORIGINAL_XML"
  
  echo "Extract 1:n relationships of different translation correlation list columns from '$correlationList'"
  cp $correlationList "$integrationName/correlation/"
  extractSeparatedColumn $correlationList $correlationListISBN10 "targetIdentifier" "targetISBN10" "id" "isbn10"
  extractSeparatedColumn $correlationList $correlationListISBN13 "targetIdentifier" "targetISBN13" "id" "isbn13"
  extractSeparatedColumn $correlationList $correlationListKBRIDs "targetIdentifier" "targetKBRIdentifier" "id" "KBR"
  extractSeparatedColumn $correlationList $correlationListBNFIDs "targetIdentifier" "targetBnFIdentifier" "id" "BnF"
  extractSeparatedColumn $correlationList $correlationListKBIDs "targetIdentifier" "targetKBIdentifier" "id" "KB"
  extractSeparatedColumn $correlationList $correlationListUNESCOIDs "targetIdentifier" "targetUnescoIdentifier" "id" "unesco"
  extractSeparatedColumn $correlationList $correlationListSourceLanguage "targetIdentifier" "sourceLanguage" "id" "sourceLanguage"
  extractSeparatedColumn $correlationList $correlationListTargetLanguage "targetIdentifier" "targetLanguage" "id" "targetLanguage"

  echo "Fetch and extract KBR originals"
  getKBRRecords $correlationList "sourceKBRIdentifier" $correlationListKBROriginalXML 

  mkdir -p $integrationName/correlation/originals/book-data-and-contributions/mixed-lang
  mkdir -p $integrationName/correlation/originals/agents/mixed-lang
  extractKBRTranslationsAndContributions "$integrationName/correlation" "/originals" "$correlationListKBROriginalXML" "mixed-lang"

}

# -----------------------------------------------------------------------------
function transformContributorCorrelationList {
  local integrationName=$1

  mkdir -p "$integrationName/correlation/rdf"

  local correlationList="$INPUT_CORRELATION"
  local correlationListNationalities="$integrationName/correlation/$SUFFIX_CORRELATION_NATIONALITY"
  local correlationListKBRIDs="$integrationName/correlation/$SUFFIX_CORRELATION_KBR"
  local correlationListBnFIDs="$integrationName/correlation/$SUFFIX_CORRELATION_BNF"
  local correlationListNTAIDs="$integrationName/correlation/$SUFFIX_CORRELATION_NTA"
  local correlationListUnescoIDs="$integrationName/correlation/$SUFFIX_CORRELATION_UNESCO"
  local correlationListISNIIDs="$integrationName/correlation/$SUFFIX_CORRELATION_ISNI"

  #local correlationListUnescoLongIDs="$integrationName/correlation/$SUFFIX_CORRELATION_UNESCO_LONG"
  local correlationListVIAFIDs="$integrationName/correlation/$SUFFIX_CORRELATION_VIAF"
  local correlationListWikidataIDs="$integrationName/correlation/$SUFFIX_CORRELATION_WIKIDATA"

  local correlationTurtle="$integrationName/correlation/rdf/$SUFFIX_CORRELATION_LD"


  export RML_SOURCE_CORRELATION_CONTRIBUTORS="$correlationList"
  export RML_SOURCE_CORRELATION_NATIONALITY="$correlationListNationalities"
  export RML_SOURCE_CORRELATION_KBR="$correlationListKBRIDs"
  export RML_SOURCE_CORRELATION_BNF="$correlationListBnFIDs"
  export RML_SOURCE_CORRELATION_NTA="$correlationListNTAIDs"
  export RML_SOURCE_CORRELATION_UNESCO="$correlationListUnescoIDs"
  export RML_SOURCE_CORRELATION_ISNI="$correlationListISNIIDs"

  #export RML_SOURCE_CORRELATION_UNESCO_LONG="$correlationListUnescoLongIDs"
  export RML_SOURCE_CORRELATION_VIAF="$correlationListVIAFIDs"
  export RML_SOURCE_CORRELATION_WIKIDATA="$correlationListWikidataIDs"

  echo "Map persons correlation data"
  . map.sh ../data-sources/correlation/correlation-contributors.yml $correlationTurtle

}

# -----------------------------------------------------------------------------
function transformTranslationCorrelationList {
  local integrationName=$1

  mkdir -p "$integrationName/correlation/rdf"
  
  local correlationList="$INPUT_CORRELATION_TRANSLATIONS"
  local correlationListISBN10="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_ISBN10"
  local correlationListISBN13="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_ISBN13"

  local correlationListKBRIDs="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_KBR"
  local correlationListBNFIDs="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_BNF"
  local correlationListKBIDs="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_KB"
  local correlationListUNESCOIDs="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_UNESCO"

  local correlationListSourceLanguage="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_SOURCE_LANG"
  local correlationListTargetLanguage="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_TARGET_LANG"

  local correlationListKBRSOURCEIDs="$integrationName/correlation/$SUFFIX_CORRELATION_TRL_UNESCO"

  local correlationTurtle="$integrationName/correlation/rdf/$SUFFIX_CORRELATION_TRL_LD"

  export RML_SOURCE_CORRELATION_TRL="$correlationList"
  export RML_SOURCE_CORRELATION_TRL_ISBN10="$correlationListISBN10"
  export RML_SOURCE_CORRELATION_TRL_ISBN13="$correlationListISBN13"
  export RML_SOURCE_CORRELATION_TRL_KBR="$correlationListKBRIDs"
  export RML_SOURCE_CORRELATION_TRL_BNF="$correlationListBNFIDs"
  export RML_SOURCE_CORRELATION_TRL_KB="$correlationListKBIDs"
  export RML_SOURCE_CORRELATION_TRL_UNESCO="$correlationListUNESCOIDs"
  export RML_SOURCE_CORRELATION_TRL_SOURCE_LANG="$correlationListSourceLanguage"
  export RML_SOURCE_CORRELATION_TRL_TARGET_LANG="$correlationListTargetLanguage"
 
  echo "Map translations correlation data"
  . map.sh ../data-sources/correlation/correlation-translations.yml $correlationTurtle

  echo "Map extracted data about originals"
  mkdir -p "$integrationName/correlation/originals/rdf/mixed-lang"
  mapKBRBookInformationAndContributions $integrationName/correlation "originals" "mixed-lang"

}

# -----------------------------------------------------------------------------
function loadContributorCorrelationList {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"
  local correlationTurtle="$integrationName/correlation/rdf/$SUFFIX_CORRELATION_LD"

  echo "Load persons correlation list"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_INT_CONT" \
    "$correlationTurtle"
}
  
# -----------------------------------------------------------------------------
function loadTranslationCorrelationList {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"
  local correlationTurtle="$integrationName/correlation/rdf/$SUFFIX_CORRELATION_TRL_LD"
  local originalsTurtle="$integrationName/correlation/originals/rdf/mixed-lang"

  echo "Load translations correlation list"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_INT_TRL" \
    "$correlationTurtle"

  echo "Load extracted data about originals"
  loadKBRBookInformationAndContributions "$integrationName/correlation" "originals" "$TRIPLE_STORE_GRAPH_KBR_ORIG_TRL" "$TRIPLE_STORE_GRAPH_KBR_ORIG_LA" "mixed-lang"
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
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$linkedAuthoritiesNamedGraph"

  # also delete the original information, we will add limited original information
  # but this also means, that original information from a full original dump needs to be
  # added afterwards. Dependency is first KBR then original info, thus the latter should not delete any content
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KBR_ORIG_TRL"

  # load general book data
  loadKBRBookInformationAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph" "$linkedAuthoritiesNamedGraph" "fr-nl"
  loadKBRBookInformationAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph" "$linkedAuthoritiesNamedGraph" "nl-fr"

  # load translation specific RDF
  loadKBRTranslationsAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph" "fr-nl"
  loadKBRTranslationsAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph" "nl-fr"

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

  # uncommented because if we delete the original graph, we also delete partial original information from the regular KBR export
  # i.e. the schema:translationOf links to dummy source entities that encode the language of the original
  #deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$translationsNamedGraph"

  # only load book information, no translation-specific triples
  loadKBRBookInformationAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph" "$linkedAuthoritiesNamedGraph" "fr-nl"
  loadKBRBookInformationAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph" "$linkedAuthoritiesNamedGraph" "nl-fr"
}

# -----------------------------------------------------------------------------
function loadOriginalLinksKBR {
  local integrationName=$1
  local dataSourceName=$2

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"
  local kbrOriginalLinksTurtleFRNL="$integrationName/$dataSourceName/rdf/fr-nl/$SUFFIX_KBR_ORIGINAL_LINKING_LD"
  local kbrOriginalLinksTurtleNLFR="$integrationName/$dataSourceName/rdf/nl-fr/$SUFFIX_KBR_ORIGINAL_LINKING_LD"

  echo "Load KBR links to identified originals ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_KBR_TRL" \
    "$kbrOriginalLinksTurtleFRNL" "$kbrOriginalLinksTurtleNLFR"
}

# -----------------------------------------------------------------------------
function loadKBRTranslationsAndContributions {
  local integrationName=$1
  local dataSourceName=$2
  local translationsNamedGraph=$3
  local language=$4

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local kbrTranslations="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_TRL_LD"
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
  local language=$5

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local kbrBookInformationAndContributions="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_BOOK_LD"
  local kbrIdentifiedAuthorities="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_NEWAUT_LD"
  local kbrTranslationsBB="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_TRL_BB_LD"
  local kbrTranslationsPubCountries="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_TRL_PUB_COUNTRY_LD"
  local kbrTranslationsPubPlaces="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_TRL_PUB_PLACE_LD"
  local kbrTranslationsISBNTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_TRL_ISBN_LD"

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"


  echo "Load KBR book information and contributions, BB assignments, countries, places, ISBN10/ISBN13 - $language ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$translationsNamedGraph" \
    "$kbrBookInformationAndContributions" "$kbrTranslationsBB" "$kbrTranslationsPubCountries" "$kbrTranslationsPubPlaces" "$kbrTranslationsISBNTurtle"

  # upload newly identified authorities to the linked authorities named graph
  echo "Load newly identified KBR linked authorities $language ..."
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

  local kbrOrgMatchesTurtleFRNL="$integrationName/kbr/rdf/$SUFFIX_KBR_PBL_MULTIPLE_MATCHES_FR_NL_LD"
  local kbrOrgMatchesTurtleNLFR="$integrationName/kbr/rdf/$SUFFIX_KBR_PBL_MULTIPLE_MATCHES_NL_FR_LD"

  local kbrPersonsNamesTurtleFRNL="$integrationName/kbr/rdf/$SUFFIX_KBR_PERSONS_NAMES_FR_NL_LD"
  local kbrPersonsNamesTurtleNLFR="$integrationName/kbr/rdf/$SUFFIX_KBR_PERSONS_NAMES_NL_FR_LD"
  local kbrBelgianPersonsNamesTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_PERSONS_NAMES_BELGIANS_LD"

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  # upload newly identified authorities to the linked authorities named graph
  echo "Load newly identified KBR linked authorities ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$linkedAuthoritiesNamedGraph" \
    "$kbrPersonsFRNL" "$kbrPersonsNLFR" "$kbrOrgsFRNL" "$kbrOrgsNLFR" "$kbrPlaces" \
    "$kbrPersonsIdentifiersTurtleFRNL" "$kbrPersonsIdentifiersTurtleNLFR" "$kbrOrgsIdentifiersTurtleFRNL" \
    "$kbrOrgsIdentifiersTurtleNLFR" "$kbrBelgians" "$kbrBelgiansIdentifiersTurtle" \
    "$kbrPersonsNamesTurtleFRNL" "$kbrPersonsNamesTurtleNLFR" "$kbrBelgianPersonsNamesTurtle"

  echo "Load possible KBR publisher matches ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph $TRIPLE_STORE_GRAPH_KBR_PBL_MATCHES \
    "$kbrOrgMatchesTurtleFRNL" "$kbrOrgMatchesTurtleNLFR"

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
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KB_TRL"

  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KB_LA"

  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KB_TRL_ORIG"


  echo "Load KB translations and contributions ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_KB_TRL" "$kbTranslationsAndContributions"

  echo "Load KB (limited) original information ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_KB_TRL_ORIG" "$kbOriginalsTurtle"

  echo "Load KB linked authorities ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_KB_LA" "$kbLinkedAuthorities"

  echo "Load KB publisher data FR-NL ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph $TRIPLE_STORE_GRAPH_KB_PBL "$kbPublishersFRNL"

  echo "Load KB publisher data NL-FR ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph $TRIPLE_STORE_GRAPH_KB_PBL "$kbPublishersNLFR"

  echo "Link KB translations to publisher authority records ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_KB_TRL_PBL"

  echo "Create dcterms:identifier properties for KB publishers ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_KB_PBL_IDENTIFIERS"

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

  local bnfRameauClassifications="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_RAMEAU"


  local bnfLimitedOriginalInformationTurtle="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_ORIG_LD"
  local bnfLimitedOriginalInformationLinksTurtle="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_ORIG_LINKS_LD"

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  echo "Load BNF translations FR-NL ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_TRL_FR_NL" "$bnfTranslationsFRNL"

  echo "Load BNF translations NL-FR ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_TRL_NL_FR" "$bnfTranslationsNLFR"

  echo "Load BnF contributors persons and organizations ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_CONT" "$bnfContributorData" "$bnfContributorDataOrgs"

  echo "Load BnF publication-rameau links ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_RDF_XML" --named-graph "$TRIPLE_STORE_GRAPH_BNF_TRL_RAMEAU_LINKS" "$bnfRameauClassifications"

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

  echo "Load BnF limited originals into separate named graph ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_BNF_TRL_ORIG" "$bnfLimitedOriginalInformationTurtle"

  echo "Load BnF original links into the single BnF named graph ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_BNF_TRL" "$bnfLimitedOriginalInformationLinksTurtle"


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
    "$CREATE_QUERY_BNF_ISNI" "$CREATE_QUERY_BNF_VIAF" "$CREATE_QUERY_BNF_WIKIDATA" "$CREATE_QUERY_BNF_GENDER" \
    "$CREATE_QUERY_BNF_MANIFESTATIONS_BIBFRAME"

}

# -----------------------------------------------------------------------------
function loadUnesco {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_UNESCO"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_UNESCO_ORIG"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_UNESCO_LA"

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  local translationTurtle="$integrationName/unesco/rdf/$SUFFIX_UNESCO_TRANSLATIONS_LD"
  local translationOriginalTurtle="$integrationName/unesco/rdf/$SUFFIX_UNESCO_TRANSLATIONS_LIMITED_ORIGINAL_LD"
  local isbnTurtle="$integrationName/unesco/rdf/$SUFFIX_UNESCO_ISBN_LD"
  local authorityTurtle="$integrationName/unesco/rdf/$SUFFIX_UNESCO_AUTHORITIES_LD"

  echo "Load Unesco Index Translationum translation data (translations, contributions and ISBN relationships)"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph $TRIPLE_STORE_GRAPH_UNESCO \
    "$translationTurtle" "$isbnTurtle"

  echo "Load Unesco Index Translationum original information"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph $TRIPLE_STORE_GRAPH_UNESCO_ORIG \
    "$translationOriginalTurtle"

  echo "Load Unesco authority records"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph $TRIPLE_STORE_GRAPH_UNESCO_LA \
    "$authorityTurtle"
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
function getKBRRecords {
  local inputFile=$1
  local idColumn=$2
  local outputFile=$3

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  python $SCRIPT_GET_KBR_RECORDS -i "$inputFile" -o "$outputFile" --identifier-column "$idColumn" -b "150" -u "$ENV_KBR_API_Z3950"
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
  python -m $MODULE_NORMALIZE_HEADERS -i $input -o $output -m $headerConversionTable -d ';'
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
    integrate $3
    query $3
    postprocess $3

  elif [ "$1" = "tliqp" ];
  then
    transform $2 $3
    load $2 $3
    integrate $3
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

  elif [ "$1" = "c" ];
  then
    clustering $3

  else
    echo "uknown command, please use different combinations of extract (e) transform (t) load (l) query (q) and postprocess (p): 'etl', 'etlq', 'etlqp', 'e', 'et', 't', 'l', 'tl', 'q' etc"
    exit 1
  fi
fi
