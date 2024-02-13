#!/bin/bash

# Make the locally developed python package accessible via python -m 
cd ..
export PYTHONPATH=$(pwd)
cd -

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

MODULE_NORMALIZED_LOOKUP="tools.csv.normalized_lookup"

LOOKUP_FILE_BB_EN="../data-sources/master-data/bb-en.csv"

SCRIPT_GET_KBR_RECORDS="../data-sources/kbr/get-kbr-records.py"

MODULE_COMPLETE_SEQUENCE_NUMBERS="tools.csv.complete_sequence_numbers"

MODULE_CSV_SET_DIFFERENCE="tools.csv.difference"

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

MODULE_FETCH_KBR_DATA="tools.xml.query_kbr"
MODULE_EXTRACT_KBR_CONTRIBUTOR_LINKS="tools.xml.extract_linked_authorities"

MODULE_NORMALIZE_1_N_COLUMNS="tools.csv.normalize_1_n_relationship"

# the following script is an older deprecated version of the script above
SCRIPT_EXTRACT_COLUMN="../data-sources/bnf/extractColumn.py" 

MODULE_FILTER_RDF_XML_SUBJECTS="tools.xml.filter-subjects-xml" 

SCRIPT_UNION_IDS="../data-sources/bnf/union.py"

SCRIPT_PARSE_UNESCO_HTML="../data-sources/unesco/parse-content.py"
MODULE_EXTRACT_UNIQUE_UNESCO_CONTRIBUTORS="tools.csv.count_unique_values"
MODULE_GROUP_BY="tools.csv.group_by"
MODULE_EXTRACT_STRING_FROM_COLUMN="tools.csv.extract_string_from_column"

SCRIPT_UPLOAD_DATA="../utils/upload-data.sh"
SCRIPT_DELETE_NAMED_GRAPH="../utils/delete-named-graph.sh"
SCRIPT_QUERY_DATA="../utils/query-data.sh"
SCRIPT_POSTPROCESS_QUERY_RESULT="post-process-integration-result.py"
SCRIPT_POSTPROCESS_AGG_QUERY_RESULT="post-process-manifestations.py"
SCRIPT_POSTPROCESS_QUERY_CONT_RESULT="post-process-contributors.py"
SCRIPT_POSTPROCESS_DERIVE_COUNTRIES="add_country.py"
SCRIPT_POSTPROCESS_GET_GEONAME_PLACE_OF_PUBLICATION="add_coordinates.py"
MODULE_POSTPROCESS_SORT_COLUMN_VALUES="tools.csv.sort_values_in_columns"
SCRIPT_POSTPROCESS_LOCATIONS="post-process-locations.py"
SCRIPT_POSTPROCESS_DATES="post-process-dates.py"


BNF_FILTER_CONFIG_CONTRIBUTORS="../data-sources/bnf/filter-config-beltrans-contributor-nationality.csv"
BNF_CSV_HEADER_CONVERSION="../data-sources/bnf/export-headers-mapping.csv"
KBR_CSV_HEADER_CONVERSION="../data-sources/kbr/author-headers.csv"

# 2023-12-04: when working with the difference script to obtain not-already-fetched KBR identifiers
KBR_CONTRIBUTOR_HEADER_CONVERSION="../data-sources/kbr/contributor-header-mapping.csv"

# #############################################################################
#
# INPUT FILENAMES
#

INPUT_EXISTING_CLUSTER_KEYS="corpus-versions/2023-12-07/integration/clustering/descriptive-keys-no-uri.csv"

# KBR - translations
INPUT_KBR_TRL_NL="../data-sources/kbr/translations/KBR_1970-2020_NL-FR_2024-02-08.xml"
INPUT_KBR_TRL_FR="../data-sources/kbr/translations/KBR_1970-2020_FR-NL_2024-02-08.xml"

INPUT_KBR_TRL_ORIG_NL_FR="../data-sources/kbr/translations/originals/BELTRANS_NL-FR_NL-gelinkte-documenten.xml"
INPUT_KBR_TRL_ORIG_FR_NL="../data-sources/kbr/translations/originals/BELTRANS_FR-NL_FR-gelinkte-documenten.xml"

INPUT_KBR_ORGS_LOOKUP="../data-sources/kbr/agents/aorg.csv"

INPUT_KBR_APEP="../data-sources/kbr/agents/ExportSyracuse_Autoriteit_2023-10-21_APEP.xml"
INPUT_KBR_AORG="../data-sources/kbr/agents/ExportSyracuse_Autoriteit_2023-10-23_AORG.xml"

# KBR - linked authorities
INPUT_KBR_LA_PERSON_NL="../data-sources/kbr/agents/KBR_1970-2020_NL-FR_persons_2024-02-08.xml"
INPUT_KBR_LA_ORG_NL="../data-sources/kbr/agents/KBR_1970-2020_NL-FR_orgs_2024-02-08.xml"
INPUT_KBR_LA_PERSON_FR="../data-sources/kbr/agents/KBR_1970-2020_FR-NL_persons_2024-02-08.xml"
INPUT_KBR_LA_ORG_FR="../data-sources/kbr/agents/KBR_1970-2020_FR-NL_orgs_2024-02-08.xml"

INPUT_KBR_LA_PLACES_VLG="../data-sources/kbr/agents/publisher-places-VLG.csv"
INPUT_KBR_LA_PLACES_WAL="../data-sources/kbr/agents/publisher-places-WAL.csv"
INPUT_KBR_LA_PLACES_BRU="../data-sources/kbr/agents/publisher-places-BRU.csv"

INPUT_KBR_PBL_REPLACE_LIST="../data-sources/kbr/agents/publisher-name-mapping.csv"

# KBR - Belgians
#INPUT_KBR_BELGIANS="../data-sources/kbr/agents/ExportSyracuse_ANAT-Belg_2023-11-08.xml"
INPUT_KBR_BELGIANS="../data-sources/kbr/agents/ANAT-belg_2024-02-08.xml"

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

INPUT_CORRELATION_PERSON="../data-sources/correlation/2024-02-05_person_contributors-correlation-list.csv"
INPUT_CORRELATION_ORG="../data-sources/correlation/2024-02-05_org_contributors-correlation-list.csv"
INPUT_CORRELATION_TRANSLATIONS="../data-sources/correlation/2024-02-05_translations_correlation-list.csv"
INPUT_CORRELATION_REMOVAL="../data-sources/correlation/2024-02-05_translations_removal-list.csv"


# #############################################################################

#
# CONFIGURATION
#
#

#TRIPLE_STORE_GRAPH_INT_TRL="http://beltrans-manifestations"
#TRIPLE_STORE_GRAPH_INT_CONT="http://beltrans-contributors"

TRIPLE_STORE_GRAPH_INT_TRL="http://beltrans-manifestations"
TRIPLE_STORE_GRAPH_INT_CONT="http://beltrans-contributors"
TRIPLE_STORE_GRAPH_WORKS="http://beltrans-works"
TRIPLE_STORE_GRAPH_INT_ORIG="http://beltrans-originals"
TRIPLE_STORE_GRAPH_INT_REMOVAL="http://beltrans-removal"
TRIPLE_STORE_GRAPH_INT_GEO="http://beltrans-geo"

TRIPLE_STORE_GRAPH_KBR_TRL="http://kbr-syracuse"
TRIPLE_STORE_GRAPH_KBR_LA="http://kbr-linked-authorities"
TRIPLE_STORE_GRAPH_KBR_BELGIANS="http://kbr-belgians"

# Named graphs for KBR original data that is fetched based on translations
TRIPLE_STORE_GRAPH_KBR_TRL_ORIG="http://kbr-originals"
TRIPLE_STORE_GRAPH_KBR_ORIG_LA="http://kbr-originals-linked-authorities"

# Named graphs for possibly outdated KBR data used for comparisons
TRIPLE_STORE_GRAPH_KBR_ORIG_MATCH_TRL="http://kbr-originals-matching"
TRIPLE_STORE_GRAPH_KBR_ORIG_MATCH_LA="http://kbr-originals-matching-linked-authorities"

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

CREATE_QUERY_BB="sparql-queries/add-bb-genres.sparql"
CREATE_QUERY_KBR_IDENTIFIED_ORIGINAL_LINKS="sparql-queries/add-kbr-identified-original-links.sparql"
DELETE_QUERY_KBR_WRONG_ORIGINAL_LINKS="sparql-queries/delete-kbr-wrong-original-links.sparql"
DELETE_QUERY_KBR_UNUSED_ORIGINALS="sparql-queries/delete-kbr-not-referenced-originals.sparql"
DELETE_QUERY_KBR_REDUNDANT_ORIGINALS="sparql-queries/delete-kbr-redundant-originals.sparql"

DELETE_QUERY_BNF_ISBN="sparql-queries/delete-bnf-isbn.sparql"
DELETE_QUERY_BNF_ISBN10_WITHOUT_HYPHEN="sparql-queries/delete-bnf-isbn10-without-hyphen.sparql"
DELETE_QUERY_BNF_ISBN13_WITHOUT_HYPHEN="sparql-queries/delete-bnf-isbn13-without-hyphen.sparql"
DELETE_QUERY_DUPLICATE_MANIFESTATIONS="sparql-queries/delete-duplicate-manifestations.sparql"

DELETE_QUERY_BELTRANS_DUPLICATE_ROLE="sparql-queries/delete-beltrans-duplicate-generic-role.sparql"
DELETE_QUERY_BELTRANS_REMOVAL_LIST="sparql-queries/delete-removal-list-translations.sparql"

TRANSFORM_QUERY_BNF_TRL_NL_FR="sparql-queries/transform-bnf-data-nl-fr.sparql"
TRANSFORM_QUERY_BNF_TRL_FR_NL="sparql-queries/transform-bnf-data-fr-nl.sparql"
CREATE_QUERY_BNF_IDENTIFIER_CONT="sparql-queries/create-bnf-contributors-identifier.sparql"
CREATE_QUERY_BNF_IDENTIFIER_MANIFESTATIONS="sparql-queries/create-bnf-manifestation-identifier.sparql"
CREATE_QUERY_BNF_ISNI="sparql-queries/create-bnf-isni.sparql"
CREATE_QUERY_BNF_VIAF="sparql-queries/create-bnf-viaf.sparql"
CREATE_QUERY_BNF_WIKIDATA="sparql-queries/create-bnf-wikidata.sparql"
CREATE_QUERY_BNF_GENDER="sparql-queries/create-bnf-contributors-gender.sparql"
CREATE_QUERY_BNF_ORIGINALS="sparql-queries/create-bnf-originals.sparql"
CREATE_QUERY_BNF_MANIFESTATIONS_BIBFRAME="sparql-queries/create-bnf-bibframe-identifiers.sparql"

CREATE_QUERY_KB_TRL_PBL="sparql-queries/link-kb-translations-to-publishers.sparql"
CREATE_QUERY_KB_PBL_IDENTIFIERS="sparql-queries/create-kb-org-identifier.sparql"

CREATE_QUERY_BELTRANS_ORIGINALS="sparql-queries/create-beltrans-originals.sparql"

CREATE_QUERY_BIBFRAME_TITLES="sparql-queries/create-bibframe-titles.sparql"
CREATE_QUERY_SCHEMA_TITLES="sparql-queries/derive-single-title-from-bibframe-titles.sparql"

ANNOTATE_QUERY_BELTRANS_CORPUS="sparql-queries/annotate-beltrans-corpus.sparql"
ANNOTATE_QUERY_KBR_ORIGINALS_CONTRIBUTOR_OVERLAP="sparql-queries/annotate-found-originals-contributor-overlap.sparql"

CREATE_QUERY_CORRELATION_DATA="sparql-queries/add-contributors-local-data.sparql"

LINK_QUERY_CONTRIBUTORS="integration_queries/link-beltrans-manifestations-contributors.sparql"
LINK_QUERY_CONTRIBUTORS_ORIG="integration_queries/link-beltrans-original-manifestations-contributors.sparql"

DATA_PROFILE_QUERY_FILE_CLUSTER_OLDEST_MANIFESTATIONS="sparql-queries/get-oldest-cluster-manifestation.sparql"

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
DATA_PROFILE_CONTRIBUTIONS_QUERY_FILE="sparql-queries/get-contributions.sparql"

GET_GEO_TEXT_INFO_QUERY_FILE="sparql-queries/get-text-location-info-per-data-source.sparql"
GET_GEO_DATA_QUERY_FILE="sparql-queries/get-manifestations-geo-data.sparql"

GET_DATE_TEXT_INFO_PUB_QUERY_FILE="sparql-queries/get-text-date-info-publications-per-data-source.sparql"
GET_DATE_TEXT_INFO_CONT_QUERY_FILE="sparql-queries/get-text-date-info-contributors-per-data-source.sparql"



POSTPROCESS_SPARQL_QUERY_TRL="sparql-queries/integrated-data-postprocessing.sparql"

SUFFIX_DATA_PROFILE_POSTPROCESS_TRL="postprocessing-input.csv"

SUFFIX_DATA_PROFILE_OLDEST_MANIFESTATIONS="cluster-oldest-manifestations.csv"

SUFFIX_DATA_PROFILE_CONT_PERSONS_ALL_DATA_FILE="contributors-persons-all-info.csv"
SUFFIX_DATA_PROFILE_CONT_PERSONS_ALL_DATA_FILE_SORTED="contributors-persons-all-info-sorted.csv"
SUFFIX_DATA_PROFILE_CONT_PERSONS_FILE="contributors-persons.csv"
SUFFIX_DATA_PROFILE_CONT_ALL_PERSONS="all-persons.csv"
SUFFIX_DATA_PROFILE_CONT_ALL_ORGS="all-orgs.csv"
SUFFIX_DATA_PROFILE_CONT_ORGS_FILE="contributors-orgs.csv"
SUFFIX_DATA_PROFILE_CONT_ORGS_FILE_PROCESSED="contributors-orgs-processed.csv"
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
SUFFIX_DATA_PROFILE_CONTRIBUTIONS="manifestation-contributions.csv"

SUFFIX_EXISTING_CLUSTER_ASSIGNMENTS="cluster-assignments-from-correlation-list.csv"

SUFFIX_PLACE_OF_PUBLICATION_GEONAMES_TARGET="place-of-publications-geonames-target.csv"
SUFFIX_PLACE_OF_PUBLICATION_GEONAMES_SOURCE="place-of-publications-geonames-source.csv"
SUFFIX_UNKNOWN_GEONAMES_MAPPING="missing-geonames-mapping.csv"

SUFFIX_GEO_TEXT="geo-text-information.csv"
SUFFIX_GEO_TEXT_COMBINED="geo-text-information-combined.csv"
SUFFIX_GEO_TEXT_COMBINED_ENRICHED="geo-text-information-combined-enriched.csv"
SUFFIX_GEO_DATA="geo-data.csv"
SUFFIX_GEO_BELTRANS_MANIFESTATIONS="manifestations-geo.csv"
SUFFIX_GEO_DATA_LD="geo-data.ttl"

SUFFIX_DATE_PUBLICATIONS_TEXT="date-publications-text-information.csv"
SUFFIX_DATE_CONTRIBUTORS_TEXT="date-contributors-text-information.csv"
SUFFIX_DATE_DATA_PUB="date-data-publications.csv"
SUFFIX_DATE_DATA_CONT="date-data-contributors.csv"
SUFFIX_DATE_DATA_PUB_LD="date-data-publications.ttl"
SUFFIX_DATE_DATA_CONT_LD="date-data-contributors.ttl"

#
# Filenames used within an integration directory 
# (will be produced by the extraction phase
# such that the transform phase can pick it up)
#
# DATA SOURCE - KBR TRANSLATIONS
#
KBR_CONT_FILTER_FILE_PERSON="../data-sources/kbr/person-filter.csv"
KBR_CONT_FILTER_FILE_ORG="../data-sources/kbr/org-filter.csv"
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

SUFFIX_KBR_TRL_CONT_APEP="linked-persons.csv"
SUFFIX_KBR_TRL_CONT_AORG="linked-orgs.csv"

SUFFIX_KBR_PBL_NO_MATCHES="publishers-no-matches.csv"
SUFFIX_KBR_PBL_MULTIPLE_MATCHES="publishers-multiple-matches.csv"

SUFFIX_KBR_LIST_FETCHED_CONTRIBUTORS="already-fetched-contributors.csv"

SUFFIX_KBR_TRL_ISBN10="isbn10.csv"
SUFFIX_KBR_TRL_ISBN13="isbn13.csv"

SUFFIX_KBR_LA_PLACES_VLG="publisher-places-VLG.csv"
SUFFIX_KBR_LA_PLACES_WAL="publisher-places-WAL.csv"
SUFFIX_KBR_LA_PLACES_BRU="publisher-places-BRU.csv"

# DATA SOURCE - KBR LINKED AUTHORITIES
#
SUFFIX_KBR_LA_PERSONS_CLEANED="translations-linked-authorities-persons-cleaned.csv"
SUFFIX_KBR_LA_ORGS_CLEANED="translations-linked-authorities-orgs-cleaned.csv"

SUFFIX_KBR_LA_PERSONS_NL_NORM="nl-translations-linked-authorities-persons-norm.csv"
SUFFIX_KBR_LA_ORGS_NL_NORM="nl-translations-linked-authorities-orgs-norm.csv"
SUFFIX_KBR_LA_PERSONS_FR_NORM="fr-translations-linked-authorities-persons-norm.csv"
SUFFIX_KBR_LA_ORGS_FR_NORM="fr-translations-linked-authorities-orgs-norm.csv"

SUFFIX_KBR_LA_PERSONS_NAT="translations-linked-authorities-nationalities.csv"
SUFFIX_KBR_LA_PERSONS_NAMES="translations-linked-authorities-names.csv"
SUFFIX_KBR_LA_PERSONS_NAMES_COMPLETE="translations-linked-authorities-names-complete.csv"

SUFFIX_KBR_LA_PERSONS_IDENTIFIERS="translations-linked-authorities-identifiers-persons.csv"
SUFFIX_KBR_LA_ORGS_IDENTIFIERS="translations-linked-authorities-identifiers-orgs.csv"

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
SUFFIX_KBR_SIMILARITY_MULTIPLE_MATCHES_NL_FR="similarity-multiple-matches.csv"

SUFFIX_KBR_ORIGINAL_MATCHES_XML="fetched-originals.xml"

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
SUFFIX_KB_TRL_FR_NL_ORIG="kb-original-titles-fr-nl.csv"
SUFFIX_KB_TRL_NL_FR_ORIG="kb-original-titles-nl-fr.csv"

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
SUFFIX_CORRELATION_NATIONALITY="correlation-persons-nationality.csv"

SUFFIX_CORRELATION_TRL="correlation-translation-entities"
SUFFIX_CORRELATION_TRL_ISBN10="correlation-trl-isbn10.csv"
SUFFIX_CORRELATION_TRL_ISBN13="correlation-trl-isbn13.csv"
SUFFIX_CORRELATION_TRL_KBR="correlation-trl-kbr-id.csv"
SUFFIX_CORRELATION_TRL_BNF="correlation-trl-bnf-id.csv"
SUFFIX_CORRELATION_TRL_KB="correlation-trl-kb-id.csv"
SUFFIX_CORRELATION_TRL_UNESCO="correlation-trl-unesco-id.csv"
SUFFIX_CORRELATION_TRL_KBR_ORIGINAL_XML="correlation-original-kbr.xml"
SUFFIX_CORRELATION_TRL_KBR_TRL_XML="correlation-translation-kbr.xml"
SUFFIX_CORRELATION_TRL_SOURCE_LANG="correlation-trl-source-lang.csv"
SUFFIX_CORRELATION_TRL_TARGET_LANG="correlation-trl-target-lang.csv"
SUFFIX_CORRELATION_TRL_TARGET_BB_NAMES="correlation-trl-target-bb-names.csv"
SUFFIX_CORRELATION_TRL_TARGET_BB_CODES="correlation-trl-target-bb-codes.csv"

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
SUFFIX_KBR_PERSONS_LD="persons.ttl"
SUFFIX_KBR_ORGS_LD="organizations.ttl"
SUFFIX_KBR_PLACES_LD="places.ttl"
SUFFIX_KBR_BELGIANS_LD="belgians.ttl"
SUFFIX_KBR_PERSONS_IDENTIFIERS_LD="persons-identifiers.ttl"
SUFFIX_KBR_ORGS_IDENTIFIERS_LD="orgs-identifiers.ttl"
SUFFIX_KBR_BELGIANS_IDENTIFIERS_LD="belgians-identifiers.ttl"

SUFFIX_KBR_PERSONS_NAMES_LD="persons-names.ttl"

SUFFIX_KBR_PBL_MULTIPLE_MATCHES_LD="orgs-multiple-matches.ttl"

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
SUFFIX_CORRELATION_LD="correlation-contributor-entities.ttl"

SUFFIX_CORRELATION_TRL_LD="correlation-translation-entities.ttl"

# -----------------------------------------------------------------------------
function fetch {

  local dataSource=$1
  local integrationFolderName=$2

  if [ "$dataSource" = "kbr" ];
  then
    fetchKBR $integrationFolderName
  fi

}

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
  elif [ "$dataSource" = "contributor-correlation" ];
  then
    extractContributorPersonCorrelationList "$integrationFolderName"
    extractContributorOrgCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "person-correlation" ];
  then
    extractContributorPersonCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "org-correlation" ];
  then
    extractContributorOrgCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "translation-correlation" ];
  then
    extractTranslationCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "translation-removal" ];
  then
    extractTranslationRemovalList "$integrationFolderName"
  elif [ "$dataSource" = "geo" ];
  then
    extractGeoInformation "$integrationFolderName"
  elif [ "$dataSource" = "date" ];
  then
    extractDateInformation "$integrationFolderName"
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
  elif [ "$dataSource" = "contributor-correlation" ];
  then 
    transformContributorPersonCorrelationList "$integrationFolderName"
    transformContributorOrgCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "person-correlation" ];
  then 
    transformContributorPersonCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "org-correlation" ];
  then 
    transformContributorOrgCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "translation-correlation" ];
  then
    transformTranslationCorrelationList "$integrationFolderName"
  elif [ "$dataSource" = "translation-removal" ];
  then
    transformTranslationRemovalList "$integrationFolderName"
  elif [ "$dataSource" = "geo" ];
  then
    transformGeoInformation "$integrationFolderName"
  elif [ "$dataSource" = "date" ];
  then
    transformDateInformation "$integrationFolderName"
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
  elif [ "$dataSource" = "translation-removal" ];
  then
    loadTranslationRemovalList "$integrationFolderName"
  elif [ "$dataSource" = "geo" ];
  then
    loadGeoInformation "$integrationFolderName"
  elif [ "$dataSource" = "date" ];
  then
    loadDateInformation "$integrationFolderName"
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
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_INT_TRL"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_INT_CONT"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_INT_ORIG"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_INT_REMOVAL"

  echo ""
  echo "Create title/subtitles according to the BIBFRAME ontology for records which do not yet have those"
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_BIBFRAME_TITLES"

  #
  # schema:name properties have to exist as they are required in the triple pattern for the data integration
  #
  echo ""
  echo "Create schema:name properties based on BIBFRAME titles/subtitles for records which do not yet have schema:name"
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_SCHEMA_TITLES"

  #
  # CREATE CORRELATION LIST ENTRIES BEFORE THE AUTOMATIC INTEGRATION
  #
  # Contributors
  #
  echo ""
  echo "Create BELTRANS person contributors based on correlation list"
  extractContributorPersonCorrelationList "$integrationName"
  transformContributorPersonCorrelationList "$integrationName"
  loadContributorPersonCorrelationList "$integrationName"

  echo ""
  echo "Create BELTRANS org contributors based on correlation list"
  extractContributorOrgCorrelationList "$integrationName"
  transformContributorOrgCorrelationList "$integrationName"
  loadContributorOrgCorrelationList "$integrationName"

  # Translations
  #
  echo ""
  echo "Create BELTRANS translations based on correlation list"
  extractTranslationCorrelationList "$integrationName"
  transformTranslationCorrelationList "$integrationName"
  loadTranslationCorrelationList "$integrationName"

  # Translations removal
  #
  echo ""
  echo "Create BELTRANS removal list based on correlation list"
  extractTranslationRemovalList "$integrationName"
  transformTranslationRemovalList "$integrationName"
  loadTranslationRemovalList "$integrationName"



  #
  # AUTOMATIC INTEGRATION
  # 
  echo ""
  echo "Automatically integrate manifestations ..."
  python $SCRIPT_INTERLINK_DATA -u "$integrationNamespace" --query-type "manifestations" --target-graph "$TRIPLE_STORE_GRAPH_INT_TRL" \
    --create-queries $createManifestationsQueries --update-queries $updateManifestationsQueries --number-updates 2 --query-log-dir $queryLogDir

  echo ""
  echo "Automatically integrate contributors ..."
  python $SCRIPT_INTERLINK_DATA -u "$integrationNamespace" --query-type "contributors" --target-graph "$TRIPLE_STORE_GRAPH_INT_CONT" \
    --create-queries $createContributorsQueries --update-queries $updateContributorsQueries --number-updates 3 --query-log-dir $queryLogDir

  # 2023-05-04 perform updates which did not finish due to a network interruption
#  python interlink_updates.py -u "$integrationNamespace" --query-type "contributors" --target-graph "$TRIPLE_STORE_GRAPH_INT_CONT" \
#    --update-queries $updateContributorsQueries --number-updates 3 --query-log-dir $queryLogDir

  # 2023-05-04 perform remaining INSERT/UPDATE operations with a modified creation config (excluding already integrated sources)
#  python $SCRIPT_INTERLINK_DATA -u "$integrationNamespace" --query-type "contributors" --target-graph "$TRIPLE_STORE_GRAPH_INT_CONT" \
#    --create-queries "2023-05-04_config-integration-contributors-create.csv" --update-queries $updateContributorsQueries --number-updates 3 --query-log-dir $queryLogDir

  echo ""
  echo "Delete translations from the manually curated removal list"
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$DELETE_QUERY_BELTRANS_REMOVAL_LIST"

  echo ""
  echo "Establish links between integrated manifestations and contributors (authors, translators, illustrators, scenarists, publishing directors, and publishers) ..."
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$LINK_QUERY_CONTRIBUTORS"

  echo ""
  echo "Delete duplicate more generic schema:author role if we have a more specific role"
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$DELETE_QUERY_BELTRANS_DUPLICATE_ROLE"

  echo ""
  echo "Create BELTRANS original manifestation records"
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_BELTRANS_ORIGINALS"

  echo ""
  echo "Establish links between integrated originals and contributors ..."
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$LINK_QUERY_CONTRIBUTORS_ORIG"

  echo ""
  echo "Perform Clustering ..."
  # 2023-12-15: this works, but EXISTING_CLUSTER_KEYS is element->key and not cluster->id
  #existingClusterAssignments="$integrationName/integration/clustering/$SUFFIX_EXISTING_CLUSTER_ASSIGNMENTS"
  #python -m tools.csv.extract_columns "$INPUT_CORRELATION_TRANSLATIONS" -o "$existingClusterAssignments" -c "targetIdentifier" -c "workClusterIdentifier" --output-column "elementID" --output-column "clusterID"
  #clustering "$integrationName" "$existingClusterAssignments" "$INPUT_EXISTING_CLUSTER_KEYS"
  clustering "$integrationName"

  echo ""
  echo "Annotate manifestations relevant for BELTRANS based on nationality ..."
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$ANNOTATE_QUERY_BELTRANS_CORPUS"

  echo ""
  echo "Create title/subtitles according to the BIBFRAME ontology (now also for integrated BELTRANS manifestations)"
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_BIBFRAME_TITLES"

  echo ""
  echo "Add BB genre classification to integrated records ..."
  python upload_data.py -u "$integrationNamespace" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_BB"

  echo ""
  echo "Create integrated geo information"
  extractGeoInformation "$integrationName"
  transformGeoInformation "$integrationName"
  loadGeoInformation "$integrationName"

  echo ""
  echo "Create integrated dates information"
  extractDateInformation "$integrationName"
  transformDateInformation "$integrationName"
  loadDateInformation "$integrationName"



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
function extractDateInformation {

  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  mkdir -p "$integrationName/dates"

  local outputFileDateTextPub="$integrationName/dates/$SUFFIX_DATE_PUBLICATIONS_TEXT"
  local outputFileDateTextCont="$integrationName/dates/$SUFFIX_DATE_CONTRIBUTORS_TEXT"
  local datesDataPub="$integrationName/dates/$SUFFIX_DATE_DATA_PUB"
  local datesDataCont="$integrationName/dates/$SUFFIX_DATE_DATA_CONT"

  echo ""
  echo "Integrate date information"
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$GET_DATE_TEXT_INFO_PUB_QUERY_FILE" "$ENV_SPARQL_ENDPOINT" "$outputFileDateTextPub"
  #queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$GET_DATE_TEXT_INFO_CONT_QUERY_FILE" "$ENV_SPARQL_ENDPOINT" "$outputFileDateTextCont"

  echo ""
  echo "Merge date values ..."
  time python $SCRIPT_POSTPROCESS_DATES \
    -i "$outputFileDateTextPub" \
    -d "dateOfPublication" \
    --id-column "manifestationID" \
    -o $datesDataPub


}

# -----------------------------------------------------------------------------
function extractGeoInformation {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  mkdir -p "$integrationName/geo"
  local unknownGeonamesMapping="$SUFFIX_UNKNOWN_GEONAMES_MAPPING"
  local outputFileGeoText="$integrationName/geo/$SUFFIX_GEO_TEXT"
  local combinedGeoText="$integrationName/geo/$SUFFIX_GEO_TEXT_COMBINED"
  local combinedGeoTextEnriched="$integrationName/geo/$SUFFIX_GEO_TEXT_COMBINED_ENRICHED"
  local geoData="$integrationName/geo/$SUFFIX_GEO_DATA"

  echo ""
  echo "Enrich geo information and create RDF descriptions of it"
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$GET_GEO_TEXT_INFO_QUERY_FILE" "$ENV_SPARQL_ENDPOINT" "$outputFileGeoText"

  echo ""
  echo "Combine location information from different data sources"
  python $SCRIPT_POSTPROCESS_LOCATIONS -i "$outputFileGeoText" -o "$combinedGeoText"

  echo "Derive missing country names from place names - KBR targetPlace ..."
  time python $SCRIPT_POSTPROCESS_DERIVE_COUNTRIES -i $combinedGeoText -o $combinedGeoTextEnriched \
    -g geonames/ -c "countryOfPublication" -p "placeOfPublication"

  echo "Create geonames relationships for place of publications ..."
  time python $SCRIPT_POSTPROCESS_GET_GEONAME_PLACE_OF_PUBLICATION \
    -i $combinedGeoTextEnriched -m $unknownGeonamesMapping -g geonames/ -p placeOfPublication \
    --input-id-column "manifestationID" \
    --column-place "placeOfPublication" \
    --column-country "countryOfPublication" \
    --column-identifier "placeGeonamesIdentifier" \
    --column-longitude "longitude" \
    --column-latitude "latitude" \
    -o $geoData

}

# -----------------------------------------------------------------------------
function transformDateInformation {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local datesDataPub="$integrationName/dates/$SUFFIX_DATE_DATA_PUB"
  #local datesDataCont="$integrationName/dates/$SUFFIX_DATE_DATA_CONT"

  local dateDataTurtle="$integrationName/dates/rdf/$SUFFIX_DATE_DATA_PUB_LD"

  mkdir -p "$integrationName/dates/rdf"

  export RML_SOURCE_DATE_PUB="$integrationName/dates/$SUFFIX_DATE_DATA_PUB"
  export RML_SOURCE_DATE_CONT="$integrationName/dates/$SUFFIX_DATE_DATA_CONT"

  echo ""
  echo "TRANSFORM dates data"
  . map.sh dates-data.yml $dateDataTurtle
}

# -----------------------------------------------------------------------------
function transformGeoInformation {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local geoDataTurtle="$integrationName/geo/rdf/$SUFFIX_GEO_DATA_LD"
  mkdir -p "$integrationName/geo/rdf"

  export RML_SOURCE_GEO="$integrationName/geo/$SUFFIX_GEO_DATA"

  echo ""
  echo "TRANSFORM geo data"
  . map.sh geo-data.yml $geoDataTurtle
}

# -----------------------------------------------------------------------------
function loadDateInformation {

  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"
  local dateDataTurtle="$integrationName/dates/rdf/$SUFFIX_DATE_DATA_PUB_LD"

  echo ""
  echo "LOAD dates data"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_INT_TRL" \
    "$dateDataTurtle"

}

# -----------------------------------------------------------------------------
function loadGeoInformation {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"
  local geoDataTurtle="$integrationName/geo/rdf/$SUFFIX_GEO_DATA_LD"

  echo ""
  echo "LOAD geo data"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_INT_GEO" \
    "$geoDataTurtle"

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
  outputFileContributions="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONTRIBUTIONS"
  outputFileKBCode="$integrationName/csv/$SUFFIX_DATA_PROFILE_KBCODE"
  outputFileGeo="$integrationName/csv/$SUFFIX_GEO_BELTRANS_MANIFESTATIONS"
  outputFileOldestManifestations="$integrationName/csv/$SUFFIX_DATA_PROFILE_OLDEST_MANIFESTATIONS"

  echo ""
  echo "Creating the dataprofile CSV file ..."
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$queryFileAgg" "$ENV_SPARQL_ENDPOINT" "$outputFileAgg"

  echo ""
  echo "Creating the contributor persons CSV file ..."
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$queryFileContPersons" "$ENV_SPARQL_ENDPOINT" "$outputFileContPersonsAllData"

  echo ""
  echo "Creating the contributor orgs CSV file ..."
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$queryFileContOrgs" "$ENV_SPARQL_ENDPOINT" "$outputFileContOrgs"

  echo ""
  echo "Creating list linking manifestations to contributors"
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$DATA_PROFILE_CONTRIBUTIONS_QUERY_FILE" "$ENV_SPARQL_ENDPOINT" "$outputFileContributions"

  echo ""
  echo "Creating the geo information CSV"
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$GET_GEO_DATA_QUERY_FILE" "$ENV_SPARQL_ENDPOINT" "$outputFileGeo"

  echo ""
  echo "Creating the oldest manifestations per cluster information CSV"
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$DATA_PROFILE_QUERY_FILE_CLUSTER_OLDEST_MANIFESTATIONS" "$ENV_SPARQL_ENDPOINT" "$outputFileOldestManifestations"

  echo ""
  echo "Creating KBCode list"
  queryDataBlazegraph "$TRIPLE_STORE_NAMESPACE" "$queryFileKBCode" "$ENV_SPARQL_ENDPOINT" "$outputFileKBCode"

}

# -----------------------------------------------------------------------------
function postprocess {
  local integrationName=$1

  integratedAllData="$integrationName/csv/$SUFFIX_DATA_PROFILE_FILE_ALL"
  integratedData="$integrationName/csv/$SUFFIX_DATA_PROFILE_FILE_PROCESSED"
  integratedDataEnriched="$integrationName/csv/$SUFFIX_DATA_PROFILE_FILE_ENRICHED"
  integratedDataEnrichedSorted="$integrationName/csv/$SUFFIX_DATA_PROFILE_FILE_ENRICHED_SORTED"

  placeOfPublicationsGeonamesTarget="$integrationName/csv/$SUFFIX_PLACE_OF_PUBLICATION_GEONAMES_TARGET"
  placeOfPublicationsGeonamesSource="$integrationName/csv/$SUFFIX_PLACE_OF_PUBLICATION_GEONAMES_SOURCE"
  unknownGeonamesMapping="$SUFFIX_UNKNOWN_GEONAMES_MAPPING"

  contributorsPersonsAllData="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_PERSONS_ALL_DATA_FILE"
  contributorsPersonsAllDataSorted="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_PERSONS_ALL_DATA_FILE_SORTED"
  contributorsPersons="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_PERSONS_FILE"
  allPersons="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_ALL_PERSONS"
  tmp1="$integrationName/csv/kbr-enriched-not-yet-bnf-and-kb.csv"
  tmp2="$integrationName/csv/kbr-and-bnf-enriched-not-yet-kb.csv"

  contributorsOrgsAllData="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_ORGS_FILE"
  contributorsOrgs="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_ORGS_FILE_PROCESSED"
  manifestationContributions="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONTRIBUTIONS"
  allOrgs="$integrationName/csv/$SUFFIX_DATA_PROFILE_CONT_ALL_ORGS"

  outputFileGeo="$integrationName/csv/$SUFFIX_GEO_BELTRANS_MANIFESTATIONS"
  kbCodeHierarchy="$integrationName/csv/$SUFFIX_DATA_PROFILE_KBCODE"

  excelData="$integrationName/$SUFFIX_DATA_PROFILE_EXCEL_DATA"

  source ./py-integration-env/bin/activate


  # 2023-11-14: these steps are executed combined in the extractGeoInformation function executed at the end of the integration
  #echo "Derive missing country names from place names - KBR targetPlace ..."
  #time python $SCRIPT_POSTPROCESS_DERIVE_COUNTRIES -i $integratedAllData -o $tmp1 -g geonames/ -c targetCountryOfPublicationKBR -p targetPlaceOfPublicationKBR

  #echo "Derive missing country names from place names - BnF ..."
  #time python $SCRIPT_POSTPROCESS_DERIVE_COUNTRIES -i $tmp1 -o $tmp2 -g geonames/ -c targetCountryOfPublicationBnF -p targetPlaceOfPublicationBnF

  #echo "Derive missing country names from place names - KB ..."
  #time python $SCRIPT_POSTPROCESS_DERIVE_COUNTRIES -i $tmp2 -o $integratedData -g geonames/ -c targetCountryOfPublicationKB -p targetPlaceOfPublicationKB

  #echo "Create geonames relationships for place of publications (targetPlace)..."
  #time python $SCRIPT_POSTPROCESS_GET_GEONAME_PLACE_OF_PUBLICATION \
  #  -i $integratedDataEnriched -m $unknownGeonamesMapping -g geonames/ -p targetPlaceOfPublication -o $placeOfPublicationsGeonamesTarget

  echo "Postprocess manifestation data ..."
  time python $SCRIPT_POSTPROCESS_AGG_QUERY_RESULT -i $integratedAllData -o $integratedDataEnriched -c $manifestationContributions
  
  echo "Sort certain columns in the contributors CSV"
  time python -m $MODULE_POSTPROCESS_SORT_COLUMN_VALUES -i $contributorsPersonsAllData -o $contributorsPersonsAllDataSorted \
       -c "nationalities" -c "gender"

  echo "Postprocess contributor data - persons ..."
  time python $SCRIPT_POSTPROCESS_QUERY_CONT_RESULT -c $contributorsPersonsAllDataSorted -m $integratedDataEnriched -o $contributorsPersons -t "persons"

  echo "Postprocess contributor data - orgs ..."
  time python $SCRIPT_POSTPROCESS_QUERY_CONT_RESULT -c $contributorsOrgsAllData -m $integratedDataEnriched -o $contributorsOrgs -t "orgs"

  echo "Postprocess contributor data -persons (keep non-contributors)..."
  time python $SCRIPT_POSTPROCESS_QUERY_CONT_RESULT -c $contributorsPersonsAllDataSorted -m $integratedDataEnriched -o $allPersons --keep-non-contributors -t "persons"

  echo "Postprocess contributor data - orgs (keep non-contributors)..."
  time python $SCRIPT_POSTPROCESS_QUERY_CONT_RESULT -c $contributorsOrgsAllData -m $integratedDataEnriched -o $allOrgs --keep-non-contributors -t "orgs"

  echo "Sort certain columns in the manifestation CSV"
  time python -m $MODULE_POSTPROCESS_SORT_COLUMN_VALUES -i $integratedDataEnriched -o $integratedDataEnrichedSorted \
       -c "sourceLanguage" -c "targetLanguage" -c "targetPlaceOfPublication" -c "targetCountryOfPublication"

  oldestManifestations="$integrationName/csv/$SUFFIX_DATA_PROFILE_OLDEST_MANIFESTATIONS"

  echo "Create Excel sheet for data ..."
  time python $SCRIPT_CSV_TO_EXCEL $integratedDataEnrichedSorted $oldestManifestations $contributorsPersons $contributorsOrgs $outputFileGeo $allPersons $allOrgs $kbCodeHierarchy -s "translations" -s "clusters" -s "person contributors" -s "org contributors" -s "geonames" -s "all persons" -s "all orgs" -s "KBCode" -o $excelData

}

# -----------------------------------------------------------------------------
function clustering {
  local integrationName=$1
  local existingClusters=$2
  local existingClusterKeys=$3

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
    --id-column "mID" \
    --column "keyPart1" \
    --column "keyPart2"

  local existingClusters=$2
  local existingClusterKeys=$3

  if [ -z $existingClusters ] || [ -z $existingClusterKeys ];
  then
    
    # perform the clustering from scratch
    #
    echo "CLUSTERING - Perform the clustering (from scratch)"
    python -m work_set_clustering.clustering \
      -i $clusterInput \
      -o $clusters \
      --id-column "elementID" \
      --key-column "descriptiveKey"

  else
    # perform the clustering with existing clusters
    #
    echo "CLUSTERING - Perform the clustering (update existing clusters)"
    python -m work_set_clustering.clustering \
      -i $clusterInput \
      -o $clusters \
      --id-column "elementID" \
      --key-column "descriptiveKey" \
      --existing-clusters "$existingClusters" \
      --existing-clusters-keys "$existingClusterKeys"

  fi

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
function fetchKBR {
  local integrationName=$1

  echo ""
  echo "FETCH - Download KBR data"
  fetchKBRTranslations "$1"
  fetchKBRLinkedAuthorities
}

# -----------------------------------------------------------------------------
function fetchKBRTranslations {
  local integrationName=$1

  local queryFRNL="H041=('*fre*','*frm*','*fro*') AND LAND='*dut*' AND ANPA=('*1970*', '*1971*', '*1972*', '*1973*', '*1974*', '*1975*', '*1976*', '*1977*', '*1978*', '*1979*', '*1980*', '*1981*', '*1982*', '*1983*', '*1984*', '*1985*', '*1986*', '*1987*', '*1988*', '*1989*', '*1990*', '*1991*', '*1992*', '*1993*', '*1994*', '*1995*', '*1996*', '*1997*', '*1998*', '*1999*', '*2000*', '*2001*', '*2002*', '*2003*', '*2004*', '*2005*', '*2006*', '*2007*', '*2008*', '*2009*', '*2010*', '*2011*', '*2012*', '*2013*', '*2014*', '*2015*', '*2016*', '*2017*', '*2018*', '*2019*', '*2020*') NOT TYPN=('COLL','CCOL')"

  local queryNLFR="H041=('*dut*','*dum*') AND LAND='*fre*' AND ANPA=('*1970*', '*1971*', '*1972*', '*1973*', '*1974*', '*1975*', '*1976*', '*1977*', '*1978*', '*1979*', '*1980*', '*1981*', '*1982*', '*1983*', '*1984*', '*1985*', '*1986*', '*1987*', '*1988*', '*1989*', '*1990*', '*1991*', '*1992*', '*1993*', '*1994*', '*1995*', '*1996*', '*1997*', '*1998*', '*1999*', '*2000*', '*2001*', '*2002*', '*2003*', '*2004*', '*2005*', '*2006*', '*2007*', '*2008*', '*2009*', '*2010*', '*2011*', '*2012*', '*2013*', '*2014*', '*2015*', '*2016*', '*2017*', '*2018*', '*2019*', '*2020*') NOT TYPN=('COLL','CCOL')"

  local date=`date +"%Y-%m-%d"`
  local dataFRNL="../data-sources/kbr/translations/KBR_1970-2020_FR-NL_$date.xml"
  local dataNLFR="../data-sources/kbr/translations/KBR_1970-2020_NL-FR_$date.xml"
  
  echo ""
  echo "FETCH - Download KBR translations FR-NL"
  fetchKBRData "$queryFRNL" "$dataFRNL"

  echo ""
  echo "FETCH - Download KBR translations NL-FR"
  fetchKBRData "$queryNLFR" "$dataNLFR"
}

# -----------------------------------------------------------------------------
function fetchKBRLinkedAuthorities {
  local integrationName=$1

  local date=`date +"%Y-%m-%d"`
  local dataFRNL="../data-sources/kbr/translations/KBR_1970-2020_FR-NL_$date.xml"
  local dataNLFR="../data-sources/kbr/translations/KBR_1970-2020_NL-FR_$date.xml"

  local personsFRNLXML="../data-sources/kbr/agents/KBR_1970-2020_FR-NL_persons_$date.xml"
  local personsNLFRXML="../data-sources/kbr/agents/KBR_1970-2020_NL-FR_persons_$date.xml"

  local orgsFRNLXML="../data-sources/kbr/agents/KBR_1970-2020_FR-NL_orgs_$date.xml"
  local orgsNLFRXML="../data-sources/kbr/agents/KBR_1970-2020_NL-FR_orgs_$date.xml"

  local belgiansXML="../data-sources/kbr/agents/ANAT-belg_$date.xml"

  local personsFRNLIdentifiers="../data-sources/kbr/agents/KBR_1970-2020_FR-NL_persons_$date.csv"
  local personsNLFRIdentifiers="../data-sources/kbr/agents/KBR_1970-2020_NL-FR_persons_$date.csv"

  local orgsFRNLIdentifiers="../data-sources/kbr/agents/KBR_1970-2020_FR-NL_orgs_$date.csv"
  local orgsNLFRIdentifiers="../data-sources/kbr/agents/KBR_1970-2020_NL-FR_orgs_$date.csv"

  checkFile $dataFRNL
  checkFile $dataNLFR

  echo ""
  echo "FETCH - Extract KBR translations FR-NL linked authorities"
  python -m $MODULE_EXTRACT_KBR_CONTRIBUTOR_LINKS -i $dataFRNL --output-persons $personsFRNLIdentifiers --output-orgs $orgsFRNLIdentifiers

  echo ""
  echo "FETCH - Extract KBR translations NL-FR linked authorities"
  python -m $MODULE_EXTRACT_KBR_CONTRIBUTOR_LINKS -i $dataNLFR --output-persons $personsNLFRIdentifiers --output-orgs $orgsNLFRIdentifiers

  echo ""
  echo "FETCH - Download KBR translations FR-NL linked authorities - person"
  getKBRAutRecords $personsFRNLIdentifiers "contributorID" $personsFRNLXML 

  echo ""
  echo "FETCH - Download KBR translations FR-NL linked authorities - orgs"
  getKBRAutRecords $orgsFRNLIdentifiers "contributorID" $orgsFRNLXML 

  echo ""
  echo "FETCH - Download KBR translations NL-FR linked authorities - persons"
  getKBRAutRecords $personsNLFRIdentifiers "contributorID" $personsNLFRXML 

  echo ""
  echo "FETCH - Download KBR translations NL-FR linked authorities - orgs"
  getKBRAutRecords $orgsNLFRIdentifiers "contributorID" $orgsNLFRXML 

  echo ""
  echo "FETCH - Download KBR Belgians"
  queryBelgians="ANAT='*belg*'"
  fetchKBRAuthorityData "$queryBelgians" "$belgiansXML"
  
}

# -----------------------------------------------------------------------------
# 2023-12-04: deprecated, replacement with live data getKBRAutRecords
function fetchKBRLinkedAuthoritiesPersonsFromDump {
  local inputFile=$1
  local inputFileIDColumnIndex=$2
  local outputFilePersons=$3

  echo ""
  echo "EXTRACT PERSON RECORDS (APEP)"
  python -m $MODULE_FILTER_RDF_XML_SUBJECTS \
    -i $INPUT_KBR_APEP \
    -f $inputFile \
    -o $outputFilePersons \
    --filter-column-index $inputFileIDColumnIndex \
    --subject-tag "marc:record" \
    --input-format "MARCXML"

}

# -----------------------------------------------------------------------------
# 2023-12-04: deprecated, replacement with live data getKBRAutRecords
function fetchKBRLinkedAuthoritiesOrgsFromDump {
  local inputFile=$1
  local inputFileIDColumnIndex=$2
  local outputFileOrgs=$3

  echo ""
  echo "EXTRACT ORG RECORDS (AORG)"
  python -m $MODULE_FILTER_RDF_XML_SUBJECTS \
    -i $INPUT_KBR_AORG \
    -f $inputFile \
    -o $outputFileOrgs \
    --filter-column-index $inputFileIDColumnIndex \
    --subject-tag "marc:record" \
    --input-format "MARCXML"

}



# -----------------------------------------------------------------------------
function extractKBR {

  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # create the folders to place the extracted translations and agents
  mkdir -p $integrationName/kbr/book-data-and-contributions/fr-nl
  mkdir -p $integrationName/kbr/book-data-and-contributions/nl-fr
  mkdir -p $integrationName/kbr/book-data-and-contributions/linked-originals
  mkdir -p $integrationName/kbr/agents/linked-originals
  mkdir -p $integrationName/kbr/agents/belgians
  mkdir -p $integrationName/kbr/agents/fr-nl
  mkdir -p $integrationName/kbr/agents/nl-fr

  local alreadyFetchedContributors="$integrationName/kbr/$SUFFIX_KBR_LIST_FETCHED_CONTRIBUTORS"

  echo ""
  echo "EXTRACTION - Extract and clean KBR translations data FR-NL"
  extractKBRTranslationsAndContributions "$integrationName" "kbr" "$INPUT_KBR_TRL_FR" "fr-nl"

  echo ""
  echo "EXTRACTION - Extract and clean KBR translations data NL-FR"
  extractKBRTranslationsAndContributions "$integrationName" "kbr" "$INPUT_KBR_TRL_NL" "nl-fr"

  echo ""
  echo "EXTRACTION - Extract and clean KBR linked authorities data"
  extractKBRPersons "$integrationName" "kbr" "$INPUT_KBR_LA_PERSON_NL" "nl-fr" "$alreadyFetchedContributors"
  extractKBRPersons "$integrationName" "kbr" "$INPUT_KBR_LA_PERSON_FR" "fr-nl" "$alreadyFetchedContributors"
  extractKBRPersons "$integrationName" "kbr" "$INPUT_KBR_BELGIANS" "belgians" "$alreadyFetchedContributors"

  extractKBROrgs "$integrationName" "kbr" "$INPUT_KBR_LA_ORG_FR" "fr-nl" "$alreadyFetchedContributors"
  extractKBROrgs "$integrationName" "kbr" "$INPUT_KBR_LA_ORG_NL" "nl-fr" "$alreadyFetchedContributors"

  echo ""
  echo "EXTRACTION - Extract and clean KBR linked originals data"
  kbrTranslationsCSVFRNL="$integrationName/kbr/book-data-and-contributions/fr-nl/$SUFFIX_KBR_TRL_WORKS"
  kbrTranslationsCSVNLFR="$integrationName/kbr/book-data-and-contributions/nl-fr/$SUFFIX_KBR_TRL_WORKS"
  kbrLinkedOriginalsXML="$integrationName/kbr/book-data-and-contributions/linked-originals/fetched-originals.xml"
  python $SCRIPT_GET_KBR_RECORDS -o "$kbrLinkedOriginalsXML" \
    --identifier-column "sourceKBRID" \
    -b "150" \
    -u "$ENV_KBR_API_Z3950" \
    "$kbrTranslationsCSVFRNL" "$kbrTranslationsCSVNLFR"
  extractKBRTranslationsAndContributions "$integrationName" "kbr" "$kbrLinkedOriginalsXML" "linked-originals"

  echo ""
  echo "EXTRACTION - Extract and clean KBR linked originals linked authorities data"
  kbrOriginalsFetchedPersonsXML="$integrationName/kbr/agents/linked-originals/fetched-apep.xml"
  kbrOriginalsFetchedOrgsXML="$integrationName/kbr/agents/linked-originals/fetched-aorg.xml"
  kbrOriginalsCSVContDedup="$integrationName/kbr/book-data-and-contributions/linked-originals/$SUFFIX_KBR_TRL_CONT_DEDUP"
  kbrOriginalsPersonContributorIDList="$integrationName/kbr/book-data-and-contributions/linked-originals/$SUFFIX_KBR_TRL_CONT_APEP"
  kbrOriginalsOrgContributorIDList="$integrationName/kbr/book-data-and-contributions/linked-originals/$SUFFIX_KBR_TRL_CONT_AORG"

  # Use filters to extract different types of authorities from the same contribution CSV file
  #
  python -m $MODULE_EXTRACT_COLUMNS -o "$kbrOriginalsPersonContributorIDList" -c "contributorID" "$kbrOriginalsCSVContDedup" --filter-file $KBR_CONT_FILTER_FILE_PERSON
  python -m $MODULE_EXTRACT_COLUMNS -o "$kbrOriginalsOrgContributorIDList" -c "contributorID" "$kbrOriginalsCSVContDedup" --filter-file $KBR_CONT_FILTER_FILE_ORG

  echo ""
  echo "Fetch KBR originals - persons"
  getKBRAutRecords "$kbrOriginalsPersonContributorIDList" "contributorID" "$kbrOriginalsFetchedPersonsXML" "$alreadyFetchedContributors"
  echo ""
  echo "Extract CSV data from fetched linked original authorities - persons"
  extractKBRPersons "$integrationName" "kbr" "$kbrOriginalsFetchedPersonsXML" "linked-originals" "$alreadyFetchedContributors"

  echo ""
  echo "Fetch KBR originals - persons"
  getKBRAutRecords "$kbrOriginalsOrgContributorIDList" "contributorID" "$kbrOriginalsFetchedOrgsXML" "$alreadyFetchedContributors"
  echo ""
  echo "Extract CSV data from fetched linked original authorities - orgs"
  extractKBROrgs "$integrationName" "kbr" "$kbrOriginalsFetchedOrgsXML" "linked-originals" "$alreadyFetchedContributors"

  echo ""
  echo "Extract KBR places"
  extractKBRPlaces

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

  kbOriginalTitlesFRNL="$integrationName/kb/translations/$SUFFIX_KB_TRL_FR_NL_ORIG"
  kbOriginalTitlesNLFR="$integrationName/kb/translations/$SUFFIX_KB_TRL_NL_FR_ORIG"

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

  echo "EXTRACTION - Extract KB original title from original title statement - FR-NL"
  python -m $MODULE_EXTRACT_STRING_FROM_COLUMN -i "$kbTranslationsFRNL" --id-column "manifestationID" --column "sourceTitle" -s ". -" -p "before" -o $kbOriginalTitlesFRNL

  echo "EXTRACTION - Extract KB original title from original title statement - NL-FR"
  python -m $MODULE_EXTRACT_STRING_FROM_COLUMN -i "$kbTranslationsNLFR" --id-column "manifestationID" --column "sourceTitle" -s ". -" -p "before" -o $kbOriginalTitlesNLFR

  echo "EXTRACTION - Extract publisher names from publications NL-FR"
  python -m $MODULE_EXTRACT_COLUMNS -o "$kbTranslationsPublishersNLFR" -c "publisherName" "$kbTranslationsNLFR"

  echo "EXTRACTION - Extract publisher names from publications FR-NL"
  python -m $MODULE_EXTRACT_COLUMNS -o "$kbTranslationsPublishersFRNL" -c "publisherName" "$kbTranslationsFRNL"

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

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

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

  echo ""
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

  echo ""
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

  echo ""
  echo "EXTRACTION - fetch live version of original records"
  mkdir -p "$integrationName/$dataSourceName/book-data-and-contributions/mixed-lang/"
  mkdir -p "$integrationName/$dataSourceName/agents/mixed-lang/"
  mkdir -p "$integrationName/$dataSourceName/mixed-lang/"
  local kbrOriginalsFetchedXML="$integrationName/$dataSourceName/mixed-lang/$SUFFIX_KBR_ORIGINAL_MATCHES_XML"
  # call the script directly instead of using the getKBRRecords function
  # because we want to give more than one input file (titleMatches and similarityMatches and both FR-NL and NL-FR)
  python $SCRIPT_GET_KBR_RECORDS -o "$kbrOriginalsFetchedXML" --identifier-column "candidatesIDs" \
    -b "150" -u "$ENV_KBR_API_Z3950" \
    "$titleMatchesFRNL" "$similarityMatchesFRNL" "$titleMatchesNLFR" "$similarityMatchesNLFR"

  extractKBRTranslationsAndContributions "$integrationName" "$dataSourceName" "$kbrOriginalsFetchedXML" "mixed-lang"

  echo ""
  echo "EXTRACTION - Extract and clean KBR translations linked authorities data"

  linkedContributors="$integrationName/$dataSourceName/book-data-and-contributions/mixed-lang/$SUFFIX_KBR_TRL_CONT_DEDUP"
  fetchedPersonsXML="$integrationName/$dataSourceName/agents/fetched-apep.xml"
  fetchedOrgsXML="$integrationName/$dataSourceName/agents/fetched-aorg.xml"
  getKBRAutRecords "$linkedContributors" "contributorID" "$fetchedPersonsXML"
  getKBRAutRecords "$linkedContributors" "contributorID" "$fetchedOrgsXML"

  extractKBRPersons "$integrationName" "$dataSourceName" "$fetchedPersonsXML" "mixed-lang"
  extractKBROrgs "$integrationName" "$dataSourceName" "$fetchedOrgsXML" "mixed-lang"



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
  mkdir -p $integrationName/kbr/rdf/belgians
  mkdir -p $integrationName/kbr/rdf/linked-originals

  echo ""
  echo "TRANSFORMATION - Map KBR book data and contributions to RDF - fr-nl"
  mapKBRBookInformationAndContributions $integrationName "kbr" "fr-nl"

  echo ""
  echo "TRANSFORMATION - Map KBR book data and contributions to RDF - nl-fr"
  mapKBRBookInformationAndContributions $integrationName "kbr" "nl-fr"

  echo ""
  echo "TRANSFORMATION - Map KBR book data and contributions to RDF - linked-originals"
  mapKBRBookInformationAndContributions $integrationName "kbr" "linked-originals"


  echo ""
  echo "TRANSFORMATION - Map KBR translation data to RDF - FR-NL"
  mapKBRTranslationsAndContributions $integrationName "kbr" "fr-nl"

  echo ""
  echo "TRANSFORMATION - Map KBR translation data to RDF - NL-FR"
  mapKBRTranslationsAndContributions $integrationName "kbr" "nl-fr"

  echo ""
  echo "TRANSFORMATION - Map KBR (limited) original information to RDF (FR-NL and NL-FR)"
  mapKBRTranslationLimitedOriginals $integrationName "kbr"


  echo ""
  echo "TRANSFORMATION - Map KBR linked person authorities data to RDF"
  mapKBRLinkedPersonAuthorities $integrationName "kbr" "fr-nl"
  mapKBRLinkedPersonAuthorities $integrationName "kbr" "nl-fr"
  mapKBRLinkedPersonAuthorities $integrationName "kbr" "belgians"
  mapKBRLinkedPersonAuthorities $integrationName "kbr" "linked-originals"

  echo ""
  echo "TRANSFORMATION - Map KBR linked org authorities data to RDF"
  mapKBRLinkedOrgAuthorities $integrationName "kbr" "fr-nl"
  mapKBRLinkedOrgAuthorities $integrationName "kbr" "nl-fr"
  mapKBRLinkedOrgAuthorities $integrationName "kbr" "linked-originals"

  echo ""
  echo "TRANSFORMATION - Map KBR places"
  local kbrPlacesTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_PLACES_LD"
  mapKBRPlaces "$integrationName" "$kbrPlacesTurtle"

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
  mkdir -p "$integrationName/$dataSourceName/rdf/mixed-lang"

  originalLinksTurtleFRNL="$integrationName/$dataSourceName/rdf/fr-nl/$SUFFIX_KBR_ORIGINAL_LINKING_LD"
  originalLinksTurtleNLFR="$integrationName/$dataSourceName/rdf/nl-fr/$SUFFIX_KBR_ORIGINAL_LINKING_LD"

  # map the translations

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_TITLE_MATCHES="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_TITLE_MATCHES_NL_FR"
  export RML_SOURCE_TITLE_DUPLICATES_MATCHES="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_TITLE_DUPLICATES_MATCHES_NL_FR"
  export RML_SOURCE_SIMILARITY_MATCHES="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_SIMILARITY_MATCHES_NL_FR"
  export RML_SOURCE_SIMILARITY_DUPLICATES_MATCHES="$integrationName/$dataSourceName/nl-fr/$SUFFIX_KBR_SIMILARITY_DUPLICATES_MATCHES_NL_FR"

  # 2) execute the mapping
  echo ""
  echo "Map KBR original linking NL-FR ..."
  . map.sh ../data-sources/kbr/kbr-original-linking.yml $originalLinksTurtleFRNL

  export RML_SOURCE_TITLE_MATCHES="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_TITLE_MATCHES_FR_NL"
  export RML_SOURCE_TITLE_DUPLICATES_MATCHES="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_TITLE_DUPLICATES_MATCHES_FR_NL"
  export RML_SOURCE_SIMILARITY_MATCHES="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_SIMILARITY_MATCHES_FR_NL"
  export RML_SOURCE_SIMILARITY_DUPLICATES_MATCHES="$integrationName/$dataSourceName/fr-nl/$SUFFIX_KBR_SIMILARITY_DUPLICATES_MATCHES_FR_NL"

  # 2) execute the mapping
  echo ""
  echo "Map KBR original linking FR-NL ..."
  . map.sh ../data-sources/kbr/kbr-original-linking.yml $originalLinksTurtleNLFR

  echo ""
  echo "Map extracted data about fetched KBR originals"
  mapKBRBookInformationAndContributions "$integrationName/" "$dataSourceName" "mixed-lang"

  echo ""
  echo "Map extracted data about linked authorities from fetched KBR originals"
  # those two functions already append the subfolder "kbr"
  mapKBRLinkedPersonAuthorities "$integrationName" "$dataSourceName" "mixed-lang"
  mapKBRLinkedOrgAuthorities "$integrationName" "$dataSourceName" "mixed-lang"

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

  export RML_SOURCE_KB_TRL_FR_NL_ORIG="$integrationName/kb/translations/$SUFFIX_KB_TRL_FR_NL_ORIG"
  export RML_SOURCE_KB_TRL_NL_FR_ORIG="$integrationName/kb/translations/$SUFFIX_KB_TRL_NL_FR_ORIG"

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
function extractKBRPersons {

  local integrationName=$1
  local dataSourceName=$2
  local kbrPersons=$3
  local language=$4
  local alreadyFetchedContributors=$5

  kbrPersonsCSV="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_PERSONS_CLEANED"
  kbrPersonsNationalities="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_PERSONS_NAT"
  kbrPersonsISNIs="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_PERSONS_IDENTIFIERS"
  kbrPersonsNames="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_PERSONS_NAMES"
  kbrPersonsNamesComplete="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_PERSONS_NAMES_COMPLETE"

  source py-integration-env/bin/activate

  echo ""
  echo "Extract person authorities - $language ..."
  python $SCRIPT_EXTRACT_AGENTS_PERSONS \
    -i $kbrPersons \
    -o $kbrPersonsCSV \
    -n $kbrPersonsNationalities \
    --names-csv $kbrPersonsNames \
    --identifier-csv $kbrPersonsISNIs

  echo ""
  echo "Complete author names sequence numbers - $language ..."
  python -m $MODULE_COMPLETE_SEQUENCE_NUMBERS \
    -i $kbrPersonsNames \
    -o $kbrPersonsNamesComplete \
    --identifier-column "authorityID" \
    --sequence-number-column "sequence_number"

  if [ ! -z $alreadyFetchedContributors ];
  then
    numberExtractedPersons=`wc -l $kbrPersonsCSV`
    # we extracted more KBR identifiers and therefore have to update the list of already fetched contributors
    # the reason we do this in the extraction phase and not after fetching with getKBRAutRecords
    # is that we initially start with an export and do not necessarilly call the fetch function,
    # but we still want that the initially extracted authorities are note fetched again
    echo ""
    echo "Append $numberExtractedPersons person identifiers to already fetched list (number including header)"
    appendValuesToCSV "$kbrPersonsCSV" "authorityID" "$alreadyFetchedContributors"
  fi

}

# -----------------------------------------------------------------------------
function extractKBROrgs {

  local integrationName=$1
  local dataSourceName=$2
  local kbrOrgs=$3
  local language=$4
  local alreadyFetchedContributors=$5

  kbrOrgsCSV="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_ORGS_CLEANED"
  kbrOrgsISNIs="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_ORGS_IDENTIFIERS"

  source py-integration-env/bin/activate

  echo ""
  echo "Extract authorities $language - Organizations ..."
  if [ -f $kbrOrgs ];
  then
    python $SCRIPT_EXTRACT_AGENTS_ORGS -i $kbrOrgs -o $kbrOrgsCSV --identifier-csv $kbrOrgsISNIs

    if [ ! -z $alreadyFetchedContributors ];
    then
      numberExtractedOrgs=`wc -l $kbrOrgsCSV`
      # we extracted more KBR identifiers and therefore have to update the list of already fetched contributors
      # the reason we do this in the extraction phase and not after fetching with getKBRAutRecords
      # is that we initially start with an export and do not necessarilly call the fetch function,
      # but we still want that the initially extracted authorities are note fetched again
      echo ""
      echo "Append $numberExtractedOrgs org identifiers to already fetched list (number including header)"
      appendValuesToCSV "$kbrOrgsCSV" "authorityID" "$alreadyFetchedContributors"
    fi
  else
    echo ""
    echo "Org input file does not exist, no org XML file to extract from!"
  fi



}

# -----------------------------------------------------------------------------
function extractKBRPlaces {

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
  echo ""
  echo "Map KBR book information and contributions - $language ..."
  . map.sh ../data-sources/kbr/kbr-book-data.yml $kbrBookDataTurtle


  # map newly identified publishers

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_CONT_IDENTIFIED="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_NEWAUT"

  # 2) execute the mapping
  echo ""
  echo "Map KBR newly identified contributors - $language ..."
  . map.sh ../data-sources/kbr/kbr-identified-authorities.yml $kbrBookDataIdentifiedAuthorities

  # map belgian bibliography assignments

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_BB="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_BB"
  
  # 2) execute the mapping
  echo ""
  echo "Map KBR BB assignments - $language ..."
  . map.sh ../data-sources/kbr/kbr-belgian-bibliography.yml $kbrBookDataBBTurtle

  # map publication countries

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_PUB_COUNTRIES="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_PUB_COUNTRY"

  # 2) execute the mapping
  echo ""
  echo "Map KBR publication countries relationships - $language ..."
  . map.sh ../data-sources/kbr/kbr-publication-countries.yml $kbrBookDataPubCountriesTurtle

  # map publication places

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_PUB_PLACES="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_PUB_PLACE"

  # 2) execute the mapping
  echo ""
  echo "Map KBR publication places relationships - $language ..."
  . map.sh ../data-sources/kbr/kbr-publication-places.yml $kbrBookDataPubPlacesTurtle


  # map ISBN10/ISBN13

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_ISBN10="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_ISBN10"
  export RML_SOURCE_KBR_ISBN13="$integrationName/$dataSourceName/book-data-and-contributions/$language/$SUFFIX_KBR_TRL_ISBN13"

  # 2) execute the mapping
  echo ""
  echo "Map KBR ISBN10/ISBN13 relationships ..."
  . map.sh ../data-sources/kbr/kbr-isbn.yml $kbrBookDataISBNTurtle
  

}

# -----------------------------------------------------------------------------
function mapKBRTranslationLimitedOriginals {
  local integrationName=$1
  local dataSourceName=$2
  local language=$3

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
function mapKBRLinkedPersonAuthorities {

  local integrationName=$1
  local dataSourceName=$2
  local language=$3

  # input
  local kbrPersons="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_PERSONS_CLEANED"
  local kbrPersonsNat="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_PERSONS_NAT"
  local kbrPersonsISNI="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_PERSONS_IDENTIFIERS"
  local kbrPersonsNames="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_PERSONS_NAMES_COMPLETE"
 
  # output
  local kbrPersonsTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_PERSONS_LD"
  local kbrPersonsIdentifiersTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_PERSONS_IDENTIFIERS_LD"
  local kbrPersonsNamesTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_PERSONS_NAMES_LD"

  # 2) execute the mapping
  mapKBRPersons "$kbrPersons" "$kbrPersonsNat" "$kbrPersonsTurtle"
  mapKBRNames "$kbrPersonsNames" "$kbrPersonsNamesTurtle"
  mapKBRLinkedIdentifiers "$kbrPersonsISNI" "$kbrPersonsIdentifiersTurtle"

}

# -----------------------------------------------------------------------------
function mapKBRLinkedOrgAuthorities {

  local integrationName=$1
  local dataSourceName=$2
  local language=$3

  # input
  local kbrOrgsISNI="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_ORGS_IDENTIFIERS"
  local kbrOrgs="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_LA_ORGS_CLEANED"
  local kbrOrgMatches="$integrationName/$dataSourceName/agents/$language/$SUFFIX_KBR_PBL_MULTIPLE_MATCHES"

  # output
  local kbrOrgsTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_ORGS_LD"
  local kbrOrgMatchesTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_PBL_MULTIPLE_MATCHES_LD"
  local kbrOrgsIdentifiersTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_ORGS_IDENTIFIERS_LD"

  # 2) execute the mapping
  mapKBROrgs "$kbrOrgs" "$kbrOrgsTurtle"
  mapKBROrgMatches "$kbrOrgMatches" "$kbrOrgMatchesTurtle"
  mapKBRLinkedIdentifiers "$kbrOrgsISNI" "$kbrOrgsIdentifiersTurtle"

}

# -----------------------------------------------------------------------------
function mapKBRPersons {
  local sourceFile=$1
  local sourceFileNat=$2
  local outputTurtle=$3

  export RML_SOURCE_KBR_PERSONS="$sourceFile"
  export RML_SOURCE_KBR_PERSONS_NAT="$sourceFileNat"

  echo ""
  echo "Map KBR Persons - $sourceFile"
  . map.sh ../data-sources/kbr/kbr-persons.yml $outputTurtle
}

# -----------------------------------------------------------------------------
function mapKBROrgs {
  local sourceFile=$1
  local outputTurtle=$2

  export RML_SOURCE_KBR_LINKED_AUTHORITIES_ORGS="$sourceFile"

  echo "" 
  echo "Map KBR Orgs - $sourceFile"
  . map.sh ../data-sources/kbr/kbr-linked-authorities-orgs.yml $outputTurtle

}

# -----------------------------------------------------------------------------
function mapKBROrgMatches {
  local sourceFile=$1
  local outputTurtle=$2
 
  export RML_SOURCE_KBR_MULTIPLE_ORG_MATCHES="$sourceFile"

  if [ -f "$sourceFile" ];
  then
    echo ""
    echo "Map KBR Orgs possible matches - $sourceFile"
    . map.sh ../data-sources/kbr/kbr-org-matches.yml $outputTurtle
  else
    echo ""
    echo "No KBR Orgs possible matches to map! - $sourceFile"
  fi
}

# -----------------------------------------------------------------------------
function mapKBRNames {
  local sourceFile=$1
  local outputTurtle=$2

  export RML_SOURCE_KBR_NAMES="$sourceFile"

  echo ""
  echo "Map KBR Names - $sourceFile"
  . map.sh ../data-sources/kbr/kbr-pseudonym-names.yml $outputTurtle
}

# -----------------------------------------------------------------------------
function mapKBRLinkedIdentifiers {
  local sourceFile=$1
  local outputTurtle=$2

  export RML_SOURCE_KBR_LINKED_AUTHORITIES="$sourceFile"

  if [ -f "$sourceFile" ];
  then
    echo ""
    echo "Map KBR linked identifiers  - $sourceFile"
    . map.sh ../data-sources/kbr/kbr-linked-identifiers.yml $outputTurtle
  else
    echo ""
    echo "No KBR linked identifiers to map! - $sourceFile"
  fi

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
function extractContributorPersonCorrelationList {
  local integrationName=$1

  folderName="$integrationName/correlation/contributor-persons"
  mkdir -p "$folderName"

  local correlationList="$INPUT_CORRELATION_PERSON"
  local correlationListKBRIDs="$folderName/$SUFFIX_CORRELATION_KBR"
  local correlationListBnFIDs="$folderName/$SUFFIX_CORRELATION_BNF"
  local correlationListNTAIDs="$folderName/$SUFFIX_CORRELATION_NTA"
  local correlationListUnescoIDs="$folderName/$SUFFIX_CORRELATION_UNESCO"
  local correlationListISNIIDs="$folderName/$SUFFIX_CORRELATION_ISNI"

  local correlationListUnescoLongIDs="$folderName/$SUFFIX_CORRELATION_UNESCO_LONG"
  local correlationListVIAFIDs="$folderName/$SUFFIX_CORRELATION_VIAF"
  local correlationListWikidataIDs="$folderName/$SUFFIX_CORRELATION_WIKIDATA"
  local correlationListPseudonymOfIDs="$folderName/$SUFFIX_CORRELATION_PSEUDONYM"
  local correlationListRealNameOfIDs="$folderName/$SUFFIX_CORRELATION_REAL_NAME"

  local correlationListNationalityCountryCodes="$folderName/$SUFFIX_CORRELATION_NATIONALITY"

  echo "Extract 1:n relationships of different persons correlation list columns from '$correlationList'"
  cp $correlationList $folderName
  extractSeparatedColumn $correlationList $correlationListKBRIDs "contributorID" "kbrIDs" "id" "KBR"
  extractSeparatedColumn $correlationList $correlationListBnFIDs "contributorID" "bnfIDs" "id" "BnF"
  extractSeparatedColumn $correlationList $correlationListNTAIDs "contributorID" "ntaIDs" "id" "NTA"
  extractSeparatedColumn $correlationList $correlationListVIAFIDs "contributorID" "viafIDs" "id" "VIAF"
  extractSeparatedColumn $correlationList $correlationListWikidataIDs "contributorID" "wikidataIDs" "id" "wikidata"
  extractSeparatedColumn $correlationList $correlationListUnescoIDs "contributorID" "unescoIDs" "id" "unesco"
  extractSeparatedColumn $correlationList $correlationListISNIIDs "contributorID" "isniIDs" "id" "ISNI"
  extractSeparatedColumn $correlationList $correlationListNationalityCountryCodes "contributorID" "nationalityCountryCodes" "id" "countryCode"

  echo ""
  echo "EXTRACTION - Fetch, extract and clean KBR contributor person correlation list"
  # the extractKBRPersons function will add the subfolder kbr/agents/$language (=mixed-lang)
  mkdir -p "$folderName/kbr/agents/mixed-lang"
  kbrOriginalsFetchedPersonsXML="$folderName/kbr/fetched-apep.xml"

  getKBRAutRecords "$correlationListKBRIDs" "KBR" "$kbrOriginalsFetchedPersonsXML"
  extractKBRPersons "$folderName" "kbr" "$kbrOriginalsFetchedPersonsXML" "mixed-lang"
}

# -----------------------------------------------------------------------------
function extractContributorOrgCorrelationList {
  local integrationName=$1

  folderName="$integrationName/correlation/contributor-orgs"
  mkdir -p "$folderName"

  local correlationList="$INPUT_CORRELATION_ORG"
  local correlationListKBRIDs="$folderName/$SUFFIX_CORRELATION_KBR"
  local correlationListBnFIDs="$folderName/$SUFFIX_CORRELATION_BNF"
  local correlationListNTAIDs="$folderName/$SUFFIX_CORRELATION_NTA"
  local correlationListUnescoIDs="$folderName/$SUFFIX_CORRELATION_UNESCO"
  local correlationListISNIIDs="$folderName/$SUFFIX_CORRELATION_ISNI"
  local correlationListVIAFIDs="$folderName/$SUFFIX_CORRELATION_VIAF"
  local correlationListWikidataIDs="$folderName/$SUFFIX_CORRELATION_WIKIDATA"

  echo "Extract 1:n relationships of different persons correlation list columns from '$correlationList'"
  cp $correlationList $folderName
  extractSeparatedColumn $correlationList $correlationListKBRIDs "contributorID" "kbrIDs" "id" "KBR"
  extractSeparatedColumn $correlationList $correlationListBnFIDs "contributorID" "bnfIDs" "id" "BnF"
  extractSeparatedColumn $correlationList $correlationListNTAIDs "contributorID" "ntaIDs" "id" "NTA"
  extractSeparatedColumn $correlationList $correlationListVIAFIDs "contributorID" "viafIDs" "id" "VIAF"
  extractSeparatedColumn $correlationList $correlationListWikidataIDs "contributorID" "wikidataIDs" "id" "wikidata"
  extractSeparatedColumn $correlationList $correlationListUnescoIDs "contributorID" "unescoIDs" "id" "unesco"
  extractSeparatedColumn $correlationList $correlationListISNIIDs "contributorID" "isniIDs" "id" "ISNI"

  echo ""
  echo "EXTRACTION - Fetch, extract and clean KBR contributor organization correlation list"
  # the extractKBROrgs function will add the subfolder kbr/agents/$language (=mixed-lang)
  mkdir -p "$folderName/kbr/agents/mixed-lang"
  kbrOriginalsFetchedOrgsXML="$folderName/kbr/fetched-aorg.xml"

  getKBRAutRecords "$correlationListKBRIDs" "KBR" "$kbrOriginalsFetchedOrgsXML"
  extractKBROrgs "$folderName" "kbr" "$kbrOriginalsFetchedOrgsXML" "mixed-lang"

}

# -----------------------------------------------------------------------------
function extractTranslationCorrelationList {
  local integrationName=$1

  local folderName="$integrationName/correlation/translations"
  mkdir -p "$folderName"

  local correlationList="$INPUT_CORRELATION_TRANSLATIONS"
  local correlationListISBN10="$folderName/$SUFFIX_CORRELATION_TRL_ISBN10"
  local correlationListISBN13="$folderName/$SUFFIX_CORRELATION_TRL_ISBN13"

  local correlationListKBRIDs="$folderName/$SUFFIX_CORRELATION_TRL_KBR"
  local correlationListBNFIDs="$folderName/$SUFFIX_CORRELATION_TRL_BNF"
  local correlationListKBIDs="$folderName/$SUFFIX_CORRELATION_TRL_KB"
  local correlationListUNESCOIDs="$folderName/$SUFFIX_CORRELATION_TRL_UNESCO"

  local correlationListSourceLanguage="$folderName/$SUFFIX_CORRELATION_TRL_SOURCE_LANG"
  local correlationListTargetLanguage="$folderName/$SUFFIX_CORRELATION_TRL_TARGET_LANG"

  local correlationListTargetBBNames="$folderName/$SUFFIX_CORRELATION_TRL_TARGET_BB_NAMES"
  local correlationListTargetBBCodes="$folderName/$SUFFIX_CORRELATION_TRL_TARGET_BB_CODES"

  local correlationListKBRSOURCEIDs="$folderName/$SUFFIX_CORRELATION_TRL_UNESCO"
  
  echo "Extract 1:n relationships of different translation correlation list columns from '$correlationList'"
  cp $correlationList "$folderName"
  extractSeparatedColumn $correlationList $correlationListISBN10 "targetIdentifier" "targetISBN10" "id" "isbn10"
  extractSeparatedColumn $correlationList $correlationListISBN13 "targetIdentifier" "targetISBN13" "id" "isbn13"
  extractSeparatedColumn $correlationList $correlationListKBRIDs "targetIdentifier" "targetKBRIdentifier" "id" "KBR"
  extractSeparatedColumn $correlationList $correlationListBNFIDs "targetIdentifier" "targetBnFIdentifier" "id" "BnF"
  extractSeparatedColumn $correlationList $correlationListKBIDs "targetIdentifier" "targetKBIdentifier" "id" "KB"
  extractSeparatedColumn $correlationList $correlationListUNESCOIDs "targetIdentifier" "targetUnescoIdentifier" "id" "unesco"
  extractSeparatedColumn $correlationList $correlationListSourceLanguage "targetIdentifier" "sourceLanguage" "id" "sourceLanguage"
  extractSeparatedColumn $correlationList $correlationListTargetLanguage "targetIdentifier" "targetLanguage" "id" "targetLanguage"


  # 2023-12-15: we currently have LEXICON codes instead the name of genres
  # if there will be names again, the extra step below to lookup codes is important
  #extractSeparatedColumn $correlationList $correlationListTargetBBCodes "targetIdentifier" "targetThesaurusBB" "id" "targetThesaurusBB"
  extractSeparatedColumn $correlationList $correlationListTargetBBNames "targetIdentifier" "targetThesaurusBB" "id" "targetThesaurusBB"

  python -m $MODULE_NORMALIZED_LOOKUP \
    --input-file $correlationListTargetBBNames \
    --lookup-file $LOOKUP_FILE_BB_EN \
    --output-file $correlationListTargetBBCodes \
    --lookup-key-column "name" \
    --lookup-value-column "id" \
    --input-key-column "targetThesaurusBB" \
    --input-id-column "id" \
    --output-value-column "targetThesaurusBB" \
    --input-delimiter "," \
    --lookup-delimiter ";"

  echo ""
  echo "Fetch and extract KBR translations"
  mkdir -p "$integrationName/correlation/translations/kbr/book-data-and-contributions/mixed-lang"
  mkdir -p "$integrationName/correlation/translations/kbr/agents/mixed-lang"
  local correlationListKBRTranslationXML="$integrationName/correlation/translations/kbr/$SUFFIX_CORRELATION_TRL_KBR_TRL_XML"
  getKBRRecords $correlationList "targetKBRIdentifier" $correlationListKBRTranslationXML 

  extractKBRTranslationsAndContributions "$integrationName/correlation/translations" "kbr" "$correlationListKBRTranslationXML" "mixed-lang"

  echo ""
  echo "EXTRACTION - Extract and clean KBR translations linked authorities data"
  kbrTranslationsFetchedPersonsXML="$integrationName/correlation/translations/kbr/agents/fetched-apep.xml"
  kbrTranslationsFetchedOrgsXML="$integrationName/correlation/translations/kbr/agents/fetched-aorg.xml"
  # This CSV file will be created by the extractKBRTranslationsAndContributions function above
  kbrTranslationsCSVContDedup="$integrationName/correlation/translations/kbr/book-data-and-contributions/mixed-lang/$SUFFIX_KBR_TRL_CONT_DEDUP"

  getKBRAutRecords "$kbrTranslationsCSVContDedup" "contributorID" "$kbrTranslationsFetchedPersonsXML"
  getKBRAutRecords "$kbrTranslationsCSVContDedup" "contributorID" "$kbrTranslationsFetchedOrgsXML"

  extractKBRPersons "$integrationName/correlation/translations" "kbr" "$kbrTranslationsFetchedPersonsXML" "mixed-lang"
  extractKBROrgs "$integrationName/correlation/translations" "kbr" "$kbrTranslationsFetchedOrgsXML" "mixed-lang"


  echo ""
  echo "Fetch and extract KBR originals"
  mkdir -p "$integrationName/correlation/originals/kbr/book-data-and-contributions/mixed-lang"
  mkdir -p "$integrationName/correlation/originals/kbr/agents/mixed-lang"
  local correlationListKBROriginalXML="$integrationName/correlation/originals/kbr/$SUFFIX_CORRELATION_TRL_KBR_ORIGINAL_XML"
  getKBRRecords $correlationList "sourceKBRIdentifier" $correlationListKBROriginalXML 

  extractKBRTranslationsAndContributions "$integrationName/correlation/originals" "kbr" "$correlationListKBROriginalXML" "mixed-lang"


  echo ""
  echo "EXTRACTION - Extract and clean KBR originals linked authorities data"
  kbrOriginalsFetchedPersonsXML="$integrationName/correlation/originals/kbr/agents/mixed-lang/fetched-apep.xml"
  kbrOriginalsFetchedOrgsXML="$integrationName/correlation/originals/kbr/agents/mixed-lang/fetched-aorg.xml"
  # This CSV file will be created by the extractKBRTranslationsAndContributions function above
  kbrOriginalsCSVContDedup="$integrationName/correlation/originals/kbr/book-data-and-contributions/mixed-lang/$SUFFIX_KBR_TRL_CONT_DEDUP"

  getKBRAutRecords "$kbrOriginalsCSVContDedup" "contributorID" "$kbrOriginalsFetchedPersonsXML"
  getKBRAutRecords "$kbrOriginalsCSVContDedup" "contributorID" "$kbrOriginalsFetchedOrgsXML"

  extractKBRPersons "$integrationName/correlation/originals" "kbr" "$kbrOriginalsFetchedPersonsXML" "mixed-lang"
  extractKBROrgs "$integrationName/correlation/originals" "kbr" "$kbrOriginalsFetchedOrgsXML" "mixed-lang"
 
}

# -----------------------------------------------------------------------------
function extractTranslationRemovalList {
  local integrationName=$1

  local folderName="$integrationName/correlation/removal"
  mkdir -p "$folderName"

  local correlationList="$INPUT_CORRELATION_REMOVAL"
  local correlationListISBN10="$folderName/$SUFFIX_CORRELATION_TRL_ISBN10"
  local correlationListISBN13="$folderName/$SUFFIX_CORRELATION_TRL_ISBN13"

  local correlationListKBRIDs="$folderName/$SUFFIX_CORRELATION_TRL_KBR"
  local correlationListBNFIDs="$folderName/$SUFFIX_CORRELATION_TRL_BNF"
  local correlationListKBIDs="$folderName/$SUFFIX_CORRELATION_TRL_KB"
  local correlationListUNESCOIDs="$folderName/$SUFFIX_CORRELATION_TRL_UNESCO"

  local correlationListSourceLanguage="$folderName/$SUFFIX_CORRELATION_TRL_SOURCE_LANG"
  local correlationListTargetLanguage="$folderName/$SUFFIX_CORRELATION_TRL_TARGET_LANG"

  local correlationListKBRSOURCEIDs="$folderName/$SUFFIX_CORRELATION_TRL_UNESCO"
  
  echo "Extract 1:n relationships of different translation correlation list columns from '$correlationList'"
  cp $correlationList "$folderName"
  extractSeparatedColumn $correlationList $correlationListISBN10 "targetIdentifier" "targetISBN10" "id" "isbn10"
  extractSeparatedColumn $correlationList $correlationListISBN13 "targetIdentifier" "targetISBN13" "id" "isbn13"
  extractSeparatedColumn $correlationList $correlationListKBRIDs "targetIdentifier" "targetKBRIdentifier" "id" "KBR"
  extractSeparatedColumn $correlationList $correlationListBNFIDs "targetIdentifier" "targetBnFIdentifier" "id" "BnF"
  extractSeparatedColumn $correlationList $correlationListKBIDs "targetIdentifier" "targetKBIdentifier" "id" "KB"
  extractSeparatedColumn $correlationList $correlationListUNESCOIDs "targetIdentifier" "targetUnescoIdentifier" "id" "unesco"
  extractSeparatedColumn $correlationList $correlationListSourceLanguage "targetIdentifier" "sourceLanguage" "id" "sourceLanguage"
  extractSeparatedColumn $correlationList $correlationListTargetLanguage "targetIdentifier" "targetLanguage" "id" "targetLanguage"

}




# -----------------------------------------------------------------------------
function transformContributorPersonCorrelationList {
  local integrationName=$1

  folderName="$integrationName/correlation/contributor-persons"
  mkdir -p "$folderName/rdf"

  local correlationList="$INPUT_CORRELATION_PERSON"
  local correlationListKBRIDs="$folderName/$SUFFIX_CORRELATION_KBR"
  local correlationListBnFIDs="$folderName/$SUFFIX_CORRELATION_BNF"
  local correlationListNTAIDs="$folderName/$SUFFIX_CORRELATION_NTA"
  local correlationListUnescoIDs="$folderName/$SUFFIX_CORRELATION_UNESCO"
  local correlationListISNIIDs="$folderName/$SUFFIX_CORRELATION_ISNI"

  local correlationListNationalityCountryCodes="$folderName/$SUFFIX_CORRELATION_NATIONALITY"

  #local correlationListUnescoLongIDs="$folderName/$SUFFIX_CORRELATION_UNESCO_LONG"
  local correlationListVIAFIDs="$folderName/$SUFFIX_CORRELATION_VIAF"
  local correlationListWikidataIDs="$folderName/$SUFFIX_CORRELATION_WIKIDATA"


  local correlationTurtle="$folderName/rdf/$SUFFIX_CORRELATION_LD"


  export RML_SOURCE_CORRELATION_CONTRIBUTORS="$correlationList"
  export RML_SOURCE_CORRELATION_KBR="$correlationListKBRIDs"
  export RML_SOURCE_CORRELATION_BNF="$correlationListBnFIDs"
  export RML_SOURCE_CORRELATION_NTA="$correlationListNTAIDs"
  export RML_SOURCE_CORRELATION_UNESCO="$correlationListUnescoIDs"
  export RML_SOURCE_CORRELATION_ISNI="$correlationListISNIIDs"
  export RML_SOURCE_CORRELATION_NATIONALITY="$correlationListNationalityCountryCodes"

  export RML_SOURCE_CORRELATION_VIAF="$correlationListVIAFIDs"
  export RML_SOURCE_CORRELATION_WIKIDATA="$correlationListWikidataIDs"

  echo ""
  echo "Map persons correlation data"
  . map.sh ../data-sources/correlation/correlation-contributors-persons.yml $correlationTurtle

  echo ""
  echo "Map fetched KBR contributor data - persons"
  mkdir -p "$folderName/kbr/rdf/mixed-lang"
  mapKBRLinkedPersonAuthorities "$folderName" "kbr" "mixed-lang"

}


# -----------------------------------------------------------------------------
function transformContributorOrgCorrelationList {
  local integrationName=$1

  folderName="$integrationName/correlation/contributor-orgs"
  mkdir -p "$folderName/rdf"

  local correlationList="$INPUT_CORRELATION_ORG"
  local correlationListKBRIDs="$folderName/$SUFFIX_CORRELATION_KBR"
  local correlationListBnFIDs="$folderName/$SUFFIX_CORRELATION_BNF"
  local correlationListNTAIDs="$folderName/$SUFFIX_CORRELATION_NTA"
  local correlationListUnescoIDs="$folderName/$SUFFIX_CORRELATION_UNESCO"
  local correlationListISNIIDs="$folderName/$SUFFIX_CORRELATION_ISNI"

  local correlationListVIAFIDs="$folderName/$SUFFIX_CORRELATION_VIAF"
  local correlationListWikidataIDs="$folderName/$SUFFIX_CORRELATION_WIKIDATA"

  local correlationTurtle="$folderName/rdf/$SUFFIX_CORRELATION_LD"


  export RML_SOURCE_CORRELATION_CONTRIBUTORS="$correlationList"
  export RML_SOURCE_CORRELATION_KBR="$correlationListKBRIDs"
  export RML_SOURCE_CORRELATION_BNF="$correlationListBnFIDs"
  export RML_SOURCE_CORRELATION_NTA="$correlationListNTAIDs"
  export RML_SOURCE_CORRELATION_UNESCO="$correlationListUnescoIDs"
  export RML_SOURCE_CORRELATION_ISNI="$correlationListISNIIDs"

  export RML_SOURCE_CORRELATION_VIAF="$correlationListVIAFIDs"
  export RML_SOURCE_CORRELATION_WIKIDATA="$correlationListWikidataIDs"

  echo ""
  echo "Map orgs correlation data"
  . map.sh ../data-sources/correlation/correlation-contributors-orgs.yml $correlationTurtle

  echo ""
  echo "Map fetched KBR contributor data - orgs"
  mkdir -p "$folderName/kbr/rdf/mixed-lang"
  mapKBRLinkedOrgAuthorities "$folderName" "kbr" "mixed-lang"

}



# -----------------------------------------------------------------------------
function transformTranslationCorrelationList {
  local integrationName=$1

  folderName="$integrationName/correlation/translations"
  mkdir -p "$integrationName/correlation/translations/rdf"
  
  local correlationList="$INPUT_CORRELATION_TRANSLATIONS"
  local correlationListISBN10="$folderName/$SUFFIX_CORRELATION_TRL_ISBN10"
  local correlationListISBN13="$folderName/$SUFFIX_CORRELATION_TRL_ISBN13"

  local correlationListKBRIDs="$folderName/$SUFFIX_CORRELATION_TRL_KBR"
  local correlationListBNFIDs="$folderName/$SUFFIX_CORRELATION_TRL_BNF"
  local correlationListKBIDs="$folderName/$SUFFIX_CORRELATION_TRL_KB"
  local correlationListUNESCOIDs="$folderName/$SUFFIX_CORRELATION_TRL_UNESCO"

  local correlationListSourceLanguage="$folderName/$SUFFIX_CORRELATION_TRL_SOURCE_LANG"
  local correlationListTargetLanguage="$folderName/$SUFFIX_CORRELATION_TRL_TARGET_LANG"

  local correlationListKBRSOURCEIDs="$folderName/$SUFFIX_CORRELATION_TRL_UNESCO"
  local correlationListTargetBBCodes="$folderName/$SUFFIX_CORRELATION_TRL_TARGET_BB_CODES"

  local correlationTurtle="$integrationName/correlation/translations/rdf/$SUFFIX_CORRELATION_TRL_LD"

  export RML_SOURCE_CORRELATION_TRL="$correlationList"
  export RML_SOURCE_CORRELATION_TRL_ISBN10="$correlationListISBN10"
  export RML_SOURCE_CORRELATION_TRL_ISBN13="$correlationListISBN13"
  export RML_SOURCE_CORRELATION_TRL_KBR="$correlationListKBRIDs"
  export RML_SOURCE_CORRELATION_TRL_BNF="$correlationListBNFIDs"
  export RML_SOURCE_CORRELATION_TRL_KB="$correlationListKBIDs"
  export RML_SOURCE_CORRELATION_TRL_UNESCO="$correlationListUNESCOIDs"
  export RML_SOURCE_CORRELATION_TRL_SOURCE_LANG="$correlationListSourceLanguage"
  export RML_SOURCE_CORRELATION_TRL_TARGET_LANG="$correlationListTargetLanguage"
  export RML_SOURCE_CORRELATION_TRL_TARGET_BB="$correlationListTargetBBCodes"
 
  echo ""
  echo "Map translations correlation data"
  . map.sh ../data-sources/correlation/correlation-translations.yml $correlationTurtle

  echo ""
  echo "Map extracted data about KBR translations from correlation list"
  mkdir -p "$integrationName/correlation/translations/kbr/rdf/mixed-lang"
  mapKBRBookInformationAndContributions "$integrationName/correlation" "translations/kbr" "mixed-lang"

  # those two functions already append the subfolder "kbr"
  mapKBRLinkedPersonAuthorities "$integrationName/correlation/translations" "kbr" "mixed-lang"
  mapKBRLinkedOrgAuthorities "$integrationName/correlation/translations" "kbr" "mixed-lang"

  echo ""
  echo "Map extracted data about originals"
  mkdir -p "$integrationName/correlation/originals/kbr/rdf/mixed-lang"
  mapKBRBookInformationAndContributions "$integrationName/correlation" "originals/kbr" "mixed-lang"

  # those two functions already append the subfolder "kbr"
  mapKBRLinkedPersonAuthorities "$integrationName/correlation/originals" "kbr" "mixed-lang"
  mapKBRLinkedOrgAuthorities "$integrationName/correlation/originals" "kbr" "mixed-lang"

}

# -----------------------------------------------------------------------------
function transformTranslationRemovalList {
  local integrationName=$1

  folderName="$integrationName/correlation/removal"
  mkdir -p "$integrationName/correlation/removal/rdf"
  
  local correlationList="$INPUT_CORRELATION_REMOVAL"
  local correlationListISBN10="$folderName/$SUFFIX_CORRELATION_TRL_ISBN10"
  local correlationListISBN13="$folderName/$SUFFIX_CORRELATION_TRL_ISBN13"

  local correlationListKBRIDs="$folderName/$SUFFIX_CORRELATION_TRL_KBR"
  local correlationListBNFIDs="$folderName/$SUFFIX_CORRELATION_TRL_BNF"
  local correlationListKBIDs="$folderName/$SUFFIX_CORRELATION_TRL_KB"
  local correlationListUNESCOIDs="$folderName/$SUFFIX_CORRELATION_TRL_UNESCO"

  local correlationListSourceLanguage="$folderName/$SUFFIX_CORRELATION_TRL_SOURCE_LANG"
  local correlationListTargetLanguage="$folderName/$SUFFIX_CORRELATION_TRL_TARGET_LANG"

  local correlationListKBRSOURCEIDs="$folderName/$SUFFIX_CORRELATION_TRL_UNESCO"

  local correlationTurtle="$integrationName/correlation/removal/rdf/$SUFFIX_CORRELATION_TRL_LD"

  export RML_SOURCE_CORRELATION_TRL="$correlationList"
  export RML_SOURCE_CORRELATION_TRL_ISBN10="$correlationListISBN10"
  export RML_SOURCE_CORRELATION_TRL_ISBN13="$correlationListISBN13"
  export RML_SOURCE_CORRELATION_TRL_KBR="$correlationListKBRIDs"
  export RML_SOURCE_CORRELATION_TRL_BNF="$correlationListBNFIDs"
  export RML_SOURCE_CORRELATION_TRL_KB="$correlationListKBIDs"
  export RML_SOURCE_CORRELATION_TRL_UNESCO="$correlationListUNESCOIDs"
  export RML_SOURCE_CORRELATION_TRL_SOURCE_LANG="$correlationListSourceLanguage"
  export RML_SOURCE_CORRELATION_TRL_TARGET_LANG="$correlationListTargetLanguage"
 
  echo ""
  echo "Map translations correlation data"
  . map.sh ../data-sources/correlation/correlation-translations-removal.yml $correlationTurtle

}



# -----------------------------------------------------------------------------
function loadContributorPersonCorrelationList {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"
  local correlationTurtle="$integrationName/correlation/contributor-persons/rdf/$SUFFIX_CORRELATION_LD"

  echo ""
  echo "Load persons correlation list"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_INT_CONT" \
    "$correlationTurtle"

  echo ""
  echo "Load fetched correlation KBR person contributors"
  loadKBRLinkedPersonAuthorities "$integrationName" "correlation/contributor-persons/kbr" "mixed-lang" "$linkedAuthoritiesNamedGraph"

}

# -----------------------------------------------------------------------------
function loadContributorOrgCorrelationList {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"
  local correlationTurtle="$integrationName/correlation/contributor-orgs/rdf/$SUFFIX_CORRELATION_LD"

  echo ""
  echo "Load org correlation list"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_INT_CONT" \
    "$correlationTurtle"

  echo ""
  echo "Load fetched correlation KBR org contributors"
  loadKBRLinkedOrgAuthorities "$integrationName" "correlation/contributor-orgs/kbr" "mixed-lang" "$linkedAuthoritiesNamedGraph"

}
  
# -----------------------------------------------------------------------------
function loadTranslationCorrelationList {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"
  local correlationTurtle="$integrationName/correlation/translations/rdf/$SUFFIX_CORRELATION_TRL_LD"
  local originalsTurtle="$integrationName/correlation/originals/rdf/mixed-lang"

  echo "Load translations correlation list"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_INT_TRL" \
    "$correlationTurtle"

  echo "Load extracted data about correlation list KBR translations"
  loadKBRBookInformationAndContributions "$integrationName/correlation" "translations/kbr" "$TRIPLE_STORE_GRAPH_KBR_TRL" "$TRIPLE_STORE_GRAPH_KBR_LA" "mixed-lang"

  loadKBRLinkedPersonAuthorities "$integrationName/correlation" "translations/kbr" "mixed-lang" "$TRIPLE_STORE_GRAPH_KBR_LA"
  loadKBRLinkedOrgAuthorities "$integrationName/correlation" "translations/kbr" "mixed-lang" "$TRIPLE_STORE_GRAPH_KBR_LA"

  echo "Load extracted data about originals"
  loadKBRBookInformationAndContributions "$integrationName/correlation" "originals/kbr" "$TRIPLE_STORE_GRAPH_KBR_TRL_ORIG" "$TRIPLE_STORE_GRAPH_KBR_LA" "mixed-lang"

  loadKBRLinkedPersonAuthorities "$integrationName/correlation" "originals/kbr" "mixed-lang" "$TRIPLE_STORE_GRAPH_KBR_LA"
  loadKBRLinkedOrgAuthorities "$integrationName/correlation" "originals/kbr" "mixed-lang" "$TRIPLE_STORE_GRAPH_KBR_LA"

}

# -----------------------------------------------------------------------------
function loadTranslationRemovalList {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"
  local correlationTurtle="$integrationName/correlation/removal/rdf/$SUFFIX_CORRELATION_TRL_LD"

  echo "Load translations correlation removal list"
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_INT_REMOVAL" \
    "$correlationTurtle"

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
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KBR_TRL_ORIG"

  # load general book data
  loadKBRBookInformationAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph" "$linkedAuthoritiesNamedGraph" "fr-nl"
  loadKBRBookInformationAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph" "$linkedAuthoritiesNamedGraph" "nl-fr"
  loadKBRBookInformationAndContributions "$integrationName" "$dataSourceName" "$TRIPLE_STORE_GRAPH_KBR_TRL_ORIG" "$linkedAuthoritiesNamedGraph" "linked-originals"

  # load translation specific RDF
  loadKBRTranslationsAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph" "fr-nl"
  loadKBRTranslationsAndContributions "$integrationName" "$dataSourceName" "$translationsNamedGraph" "nl-fr"

  # there is only a single file containing limited information about both FR-NL and NL-FR
  loadKBRLimitedOriginalInfo "$integrationName" "$dataSourceName" "$TRIPLE_STORE_GRAPH_KBR_TRL_ORIG"

  loadKBRLinkedPersonAuthorities "$integrationName" "$dataSourceName" "fr-nl" "$linkedAuthoritiesNamedGraph"
  loadKBRLinkedPersonAuthorities "$integrationName" "$dataSourceName" "nl-fr" "$linkedAuthoritiesNamedGraph"
  loadKBRLinkedPersonAuthorities "$integrationName" "$dataSourceName" "belgians" "$linkedAuthoritiesNamedGraph"
  loadKBRLinkedPersonAuthorities "$integrationName" "$dataSourceName" "linked-originals" "$linkedAuthoritiesNamedGraph"

  loadKBRLinkedOrgAuthorities "$integrationName" "$dataSourceName" "fr-nl" "$linkedAuthoritiesNamedGraph"
  loadKBRLinkedOrgAuthorities "$integrationName" "$dataSourceName" "nl-fr" "$linkedAuthoritiesNamedGraph"
  loadKBRLinkedOrgAuthorities "$integrationName" "$dataSourceName" "linked-originals" "$linkedAuthoritiesNamedGraph"

  loadKBRPlaces "$integrationName" "$linkedAuthoritiesNamedGraph"
}

# -----------------------------------------------------------------------------
function loadKBROriginals {
  local integrationName=$1

  local dataSourceName="kbr-originals"

  local translationsNamedGraph="$TRIPLE_STORE_GRAPH_KBR_ORIG_MATCH_TRL"
  local linkedAuthoritiesNamedGraph="$TRIPLE_STORE_GRAPH_KBR_ORIG_MATCH_LA"

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # 2023-10-31: activated it again, because now we use a separate named graph for these special dumps
  #
  # before 2023-10-31: uncommented because if we delete the original graph, we also delete partial original information from the regular KBR export
  # i.e. the schema:translationOf links to dummy source entities that encode the language of the original
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$translationsNamedGraph"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$linkedAuthoritiesNamedGraph"

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

  # todo: maybe add this to another named graph, 
  # and only "promote" links to the actual KBR graph after they survived a test based on overlapping contributors with SPARQL
  echo ""
  echo "Load KBR links to identified originals ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$TRIPLE_STORE_GRAPH_KBR_TRL" \
    "$kbrOriginalLinksTurtleFRNL" "$kbrOriginalLinksTurtleNLFR"

  echo ""
  echo "Load fetched KBR originals from identified links ..."
  loadKBRBookInformationAndContributions "$integrationName" "$dataSourceName" "$TRIPLE_STORE_GRAPH_KBR_TRL_ORIG" "$TRIPLE_STORE_GRAPH_KBR_LA" "mixed-lang"

  echo ""
  echo "Load fetched authorities linked to KBR originals from identified links ..."
  loadKBRLinkedPersonAuthorities "$integrationName" "$dataSourceName" "mixed-lang" "$TRIPLE_STORE_GRAPH_KBR_LA"
  loadKBRLinkedOrgAuthorities "$integrationName" "$dataSourceName" "mixed-lang" "$TRIPLE_STORE_GRAPH_KBR_LA"

  echo ""
  echo "Annotate identified originals with overlapping contributors ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" "$ANNOTATE_QUERY_KBR_ORIGINALS_CONTRIBUTOR_OVERLAP"

  echo ""
  echo "Delete links to originals which are not verified by overlapping contributors ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" "$DELETE_QUERY_KBR_WRONG_ORIGINAL_LINKS"

  echo ""
  echo "Add links between translations and originals that not only match with title, but also have overlapping contributors ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" "$CREATE_QUERY_KBR_IDENTIFIED_ORIGINAL_LINKS"

  echo ""
  echo "Delete wrongly identified originals that are no longer linked to any translation ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" "$DELETE_QUERY_KBR_WRONG_ORIGINAL_LINKS"

  echo ""
  echo "Delete redundant limited originals (after identifying and adding link to a real original) ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_SPARQL_UPDATE" "$DELETE_QUERY_KBR_REDUNDANT_ORIGINALS"
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

  echo ""
  echo "Load KBR (limited) original information ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$originalsNamedGraph" \
    "$kbrLimitedOriginalsTurtle"
}

# -----------------------------------------------------------------------------
function loadKBRLinkedPersonAuthorities {
  local integrationName=$1
  local dataSourceName=$2
  local language=$3
  local linkedAuthoritiesNamedGraph=$4

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local kbrPersons="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_PERSONS_LD"
  local kbrPersonsIdentifiersTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_PERSONS_IDENTIFIERS_LD"
  local kbrPersonsNamesTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_PERSONS_NAMES_LD"

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  # upload newly identified authorities to the linked authorities named graph
  echo ""
  echo "Load person authorities - $language ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$linkedAuthoritiesNamedGraph" \
    "$kbrPersons" "$kbrPersonsIdentifiersTurtle" "$kbrPersonsNamesTurtle"
}

# -----------------------------------------------------------------------------
function loadKBRLinkedOrgAuthorities {
  local integrationName=$1
  local dataSourceName=$2
  local language=$3
  local linkedAuthoritiesNamedGraph=$4

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  local kbrOrgs="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_ORGS_LD"
  local kbrOrgsIdentifiersTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_ORGS_IDENTIFIERS_LD"
  local kbrOrgMatchesTurtle="$integrationName/$dataSourceName/rdf/$language/$SUFFIX_KBR_PBL_MULTIPLE_MATCHES_LD"

  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  # upload newly identified authorities to the linked authorities named graph
  echo ""
  echo "Load org authorities - $language ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$linkedAuthoritiesNamedGraph" \
    "$kbrOrgs"

  if [ -f "$kbrOrgsIdentifiersTurtle" ];
  then
    echo ""
    echo "Load org authorities identifiers - $language ..."
    python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$linkedAuthoritiesNamedGraph" "$kbrOrgsIdentifiersTurtle"
  fi
  

  if [ -f "$kbrOrgMatchesTurtle" ];
  then
    echo "Load possible KBR publisher matches ..."
    python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph $TRIPLE_STORE_GRAPH_KBR_PBL_MATCHES \
      "$kbrOrgMatchesTurtle"
  fi

}


# -----------------------------------------------------------------------------
function loadKBRPlaces {
  local integrationName=$1
  local linkedAuthoritiesNamedGraph=$2

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)
  local kbrPlaces="$integrationName/kbr/rdf/$SUFFIX_KBR_PLACES_LD"
  local uploadURL="$ENV_SPARQL_ENDPOINT/namespace/$TRIPLE_STORE_NAMESPACE/sparql"

  echo "Load KBR places ..."
  python upload_data.py -u "$uploadURL" --content-type "$FORMAT_TURTLE" --named-graph "$linkedAuthoritiesNamedGraph" "$kbrPlaces"
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

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_BNF_TRL_ORIG>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_TRL_ORIG"

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
    "$CREATE_QUERY_BNF_MANIFESTATIONS_BIBFRAME" "$CREATE_QUERY_BNF_ORIGINALS"

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
function fetchKBRData {
  local query=$1
  local outputFile=$2

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  echo python -m $MODULE_FETCH_KBR_DATA -u "$ENV_KBR_API_Z3950" -q "$query" -o "$outputFile" -b 500
  python -m $MODULE_FETCH_KBR_DATA -u "$ENV_KBR_API_Z3950" -q "$query" -o "$outputFile" -b 500
}

# -----------------------------------------------------------------------------
function fetchKBRAuthorityData {
  local query=$1
  local outputFile=$2

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  echo python -m $MODULE_FETCH_KBR_DATA -u "$ENV_KBR_API_Z3950_AUT" -q "$query" -o "$outputFile" -b 500
  python -m $MODULE_FETCH_KBR_DATA -u "$ENV_KBR_API_Z3950_AUT" -q "$query" -o "$outputFile" -b 500
}



# -----------------------------------------------------------------------------
function getKBRRecords {
  local inputFile=$1
  local idColumn=$2
  local outputFile=$3

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)
  python $SCRIPT_GET_KBR_RECORDS -o "$outputFile" --identifier-column "$idColumn" -b "150" -u "$ENV_KBR_API_Z3950" "$inputFile"
}

# -----------------------------------------------------------------------------
function getKBRAutRecords {
  local inputFile=$1
  local idColumn=$2
  local outputFile=$3
  local alreadyFetchedContributors=$4

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  if [ -z $alreadyFetchedContributors ];
  then
    echo ""
    echo "Fetch KBR authority data"
    python $SCRIPT_GET_KBR_RECORDS -o "$outputFile" --identifier-column "$idColumn" -b "150" -u "$ENV_KBR_API_Z3950_AUT" "$inputFile"

  else
    local currentTime=`date +"%Y-%m-%d_%H-%M-%S"`
    local inputFileFolder=$(dirname $inputFile)
    local notYetFetched="$inputFileFolder/diff-authorities-to-fetch-$currentTime.csv"

    python -m $MODULE_CSV_SET_DIFFERENCE -o $notYetFetched --minus-rest --column "$idColumn" --column "authorityID" --output-column "authorityID" "$inputFile" "$alreadyFetchedContributors"
    local numberRows=`wc -l $inputFile`
    local numberRowsDiff=`wc -l $notYetFetched`

    echo ""
    echo "Fetch KBR authority data (records we do not have already: $numberRowsDiff from $numberRowsDiff)"
    python $SCRIPT_GET_KBR_RECORDS -o "$outputFile" --identifier-column "authorityID" -b "150" -u "$ENV_KBR_API_Z3950_AUT" "$notYetFetched"

  fi

}

# -----------------------------------------------------------------------------
function appendValuesToCSV {
  local inputFile=$1
  local inputFileIDColumn=$2
  local outputFile=$3

  echo ""
  echo "Store extracted and thus already fetched identifiers"
  # using extract columns, but with append mode
  if [ $inputFileIDColumn != "authorityID" ];
  then
    local currentTime=`date +"%Y-%m-%d_%H-%M-%S"`
    local tempOutput="/tmp/append-values-$currentTime.csv"
    python -m $MODULE_NORMALIZE_HEADERS -i $inputFile --delimiter ',' --header-mapping-file $KBR_CONTRIBUTOR_HEADER_CONVERSION -o $tempOutput
    python -m $MODULE_EXTRACT_COLUMNS -o "$outputFile" --column "$inputFileIDColumn" --append "$tempOutput" 
  else
    python -m $MODULE_EXTRACT_COLUMNS -o "$outputFile" --column "$inputFileIDColumn" --append "$inputFile" 
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
  if [ "$1" = "fetliqp" ];
  then
    fetch $2 $3
    extract $2 $3
    transform $2 $3
    load $2 $3
    integrate $3
    query $3
    postprocess $3

  elif [ "$1" = "etliqp" ];
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

  elif [ "$1" = "f" ];
  then
    fetch $2 $3

  elif [ "$1" = "fetl" ];
  then
    fetch $2 $3
    extract $2 $3
    transform $2 $3
    load $2 $3

  elif [ "$1" = "fe" ];
  then
    fetch $2 $3
    extract $2 $3

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
