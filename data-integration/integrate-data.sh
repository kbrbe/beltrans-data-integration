#!/bin/bash

SCRIPT_CLEAN_TRANSLATIONS="../data-sources/kbr/clean-marc-slim.py"
SCRIPT_CLEAN_AGENTS="../data-sources/kbr/pre-process-kbr-authors.py"
SCRIPT_TRANSFORM_TRANSLATIONS="../data-sources/kbr/marc-to-csv.py"
SCRIPT_NORMALIZE_HEADERS="../data-sources/kbr/replace-headers.py"
SCRIPT_EXTRACT_IDENTIFIED_AUTHORITIES="../data-sources/kbr/get-identified-authorities.sh"
SCRIPT_EXTRACT_BB="../data-sources/kbr/extract-belgian-bibliography.py"
SCRIPT_EXTRACT_PUB_COUNTRIES="../data-sources/kbr/extract-publication-countries.py"

SCRIPT_GET_RDF_XML_SUBJECTS="../data-sources/bnf/get-subjects.py"
SCRIPT_GET_RDF_XML_OBJECTS="../data-sources/bnf/get-objects.py"
SCRIPT_EXTRACT_COLUMN="../data-sources/bnf/extractColumn.py" 
SCRIPT_FILTER_RDF_XML_SUBJECTS="../data-sources/bnf/filter-subjects-xml.py" 
SCRIPT_UNION_IDS="../data-sources/bnf/union.py"

SCRIPT_UPLOAD_DATA="../utils/upload-data.sh"
SCRIPT_DELETE_NAMED_GRAPH="../utils/delete-named-graph.sh"
SCRIPT_QUERY_DATA="../utils/query-data.sh"
SCRIPT_POSTPROCESS_QUERY_RESULT="post-process-integration-result.py"
SCRIPT_POSTPROCESS_QUERY_CONT_RESULT="post-process-contributors.py"

BNF_FILTER_CONFIG_CONTRIBUTORS="../data-sources/bnf/filter-config-beltrans-contributor-nationality.csv"
KBR_CSV_HEADER_CONVERSION="../data-sources/kbr/author-headers.csv"

# #############################################################################
#
# INPUT FILENAMES
#

# KBR - translations
#INPUT_KBR_TRL_NL="../data-sources/kbr/translations/ExportSyracuse_20211213_NL-FR_1970-2020_3866records.xml"
#INPUT_KBR_TRL_FR="../data-sources/kbr/translations/ExportSyracuse_20211213_FR-NL_1970-2020_9239records.xml"
INPUT_KBR_TRL_NL="../data-sources/kbr/translations/KBR_1970-2020_NL-FR_4597records.xml"
INPUT_KBR_TRL_FR="../data-sources/kbr/translations/KBR_1970-2020_FR-NL_12962records.xml"

# KBR - linked authorities
INPUT_KBR_LA_PERSON_NL="../data-sources/kbr/agents/KBR_1970-2020_NL-FR_AUT-lies_APEP_3769records-all-fields.csv"
INPUT_KBR_LA_ORG_NL="../data-sources/kbr/agents/KBR_1970-2020_NL-FR_AUT-lies_AORG_711records-all-fields.csv"
INPUT_KBR_LA_PERSON_FR="../data-sources/kbr/agents/KBR_1970-2020_FR-NL_AUT-lies_APEP_8384records-all-fields.csv"
INPUT_KBR_LA_ORG_FR="../data-sources/kbr/agents/KBR_1970-2020_FR-NL_AUT-lies_AORG_702records-all-fields.csv"

INPUT_KBR_LA_PLACES_VLG="../data-sources/kbr/agents/publisher-places-VLG.csv"
INPUT_KBR_LA_PLACES_WAL="../data-sources/kbr/agents/publisher-places-WAL.csv"
INPUT_KBR_LA_PLACES_BRU="../data-sources/kbr/agents/publisher-places-BRU.csv"

# KBR - Belgians
INPUT_KBR_BELGIANS="../data-sources/kbr/agents/2021-11-29-kbr-belgians.csv"

# BNF
INPUT_BNF_PERSON_AUTHORS="../data-sources/bnf/person-authors"
INPUT_BNF_ORG_AUTHORS="../data-sources/bnf/org-authors"
INPUT_BNF_EDITIONS="../data-sources/bnf/editions"
INPUT_BNF_CONTRIBUTIONS="../data-sources/bnf/contributions"
INPUT_BNF_TRL_FR="../data-sources/bnf/BnF_FR-NL_1970-2020_584notices.csv"
INPUT_BNF_TRL_NL="../data-sources/bnf/BnF_NL-FR_1970-2020_3762notices.csv"
INPUT_BNF_CONT_ISNI="../data-sources/bnf/external/dump_extref-isni_exact_match.xml"
INPUT_BNF_CONT_VIAF="../data-sources/bnf/external/dump_extref-viaf_exact_match.xml"
INPUT_BNF_CONT_WIKIDATA="../data-sources/bnf/external/dump_extref-wikidata_exact_match.xml"

# MASTER DATA

INPUT_MASTER_MARC_ROLES="../data-sources/master-data/marc-roles.csv"
INPUT_MASTER_MARC_BINDING_TYPES="../data-sources/master-data/binding-types.csv"
INPUT_MASTER_COUNTRIES="../data-sources/master-data/countries.nt"
INPUT_MASTER_LANGUAGES="../data-sources/master-data/languages.nt"
INPUT_MASTER_GENDER="../data-sources/master-data/gender.ttl"
INPUT_MASTER_THES_EN="../data-sources/master-data/thesaurus-belgian-bibliography-en-hierarchy.csv"
INPUT_MASTER_THES_NL="../data-sources/master-data/thesaurus-belgian-bibliography-nl-hierarchy.csv"
INPUT_MASTER_THES_FR="../data-sources/master-data/thesaurus-belgian-bibliography-fr-hierarchy.csv"


# #############################################################################

#
# CONFIGURATION
#
#

TRIPLE_STORE_GRAPH_KBR_TRL="http://kbr-syracuse"
TRIPLE_STORE_GRAPH_BNF_TRL_FR="http://bnf-fr"
TRIPLE_STORE_GRAPH_BNF_TRL_NL="http://bnf-nl"
TRIPLE_STORE_GRAPH_BNF_TRL_CONT_LINKS="http://bnf-trl-contributor-links"
TRIPLE_STORE_GRAPH_BNF_CONT="http://bnf-contributors"
TRIPLE_STORE_GRAPH_BNF_CONT_ISNI="http://bnf-contributors-isni"
TRIPLE_STORE_GRAPH_BNF_CONT_VIAF="http://bnf-contributors-viaf"
TRIPLE_STORE_GRAPH_BNF_CONT_WIKIDATA="http://bnf-contributors-wikidata"
TRIPLE_STORE_GRAPH_KBR_LA="http://kbr-linked-authorities"
TRIPLE_STORE_GRAPH_KBR_BELGIANS="http://kbr-belgians"
TRIPLE_STORE_GRAPH_MASTER="http://master-data"

# if it is a blazegraph triple store
TRIPLE_STORE_NAMESPACE="integration"

FORMAT_RDF_XML="application/rdf+xml"
FORMAT_TURTLE="text/turtle"
FORMAT_NT="text/rdf+n3"

DATA_PROFILE_QUERY_FILE="dataprofile.sparql"
DATA_PROFILE_AGG_QUERY_FILE="dataprofile-aggregated.sparql"
DATA_PROFILE_CONT_BE_QUERY_FILE="contributors-belgian.sparql"
DATA_PROFILE_CONT_ALL_QUERY_FILE="contributors-all.sparql"
DATA_PROFILE_PUBS_PER_YEAR_QUERY_FILE="translations-per-year.sparql"
DATA_PROFILE_PUBS_PER_LOC_QUERY_FILE="translations-per-location.sparql"
DATA_PROFILE_PUBS_PER_COUNTRY_QUERY_FILE="translations-per-country.sparql"
DATA_PROFILE_PUBS_PER_PBL_QUERY_FILE="translations-per-publisher.sparql"

SUFFIX_DATA_PROFILE_FILE="integrated-data-not-filtered.csv"
SUFFIX_DATA_PROFILE_CONT_BE_FILE="integrated-data-contributors-belgian-not-filtered.csv"
SUFFIX_DATA_PROFILE_CONT_ALL_FILE="integrated-data-contributors-all-not-filtered.csv"
SUFFIX_DATA_PROFILE_AGG_FILE="integrated-data-aggregated.csv"
SUFFIX_DATA_PROFILE_PUBS_PER_YEAR_FILE="translations-per-year.csv"
SUFFIX_DATA_PROFILE_PUBS_PER_LOC_FILE="translations-per-location.csv"
SUFFIX_DATA_PROFILE_PUBS_PER_COUNTRY_FILE="translations-per-country.csv"
SUFFIX_DATA_PROFILE_PUBS_PER_PBL_FILE="translations-per-publisher.csv"

SUFFIX_DATA_PROFILE_FILE_PROCESSED="integrated-data.csv"
SUFFIX_DATA_PROFILE_CONT_BE_FILE_PROCESSED="integrated-data-contributors-belgian.csv"
SUFFIX_DATA_PROFILE_CONT_ALL_FILE_PROCESSED="integrated-data-contributors-all.csv"

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
SUFFIX_KBR_TRL_NL_NEWAUT="nl-translations-identified-authorities.csv"
SUFFIX_KBR_TRL_NL_BB="nl-translations-bb.csv"
SUFFIX_KBR_TRL_NL_PUB_COUNTRY="nl-translations-pub-country.csv"
SUFFIX_KBR_TRL_NL_COL_LINKS="nl-collection-links.csv"
SUFFIX_KBR_TRL_FR_CLEANED="fr-translations-cleaned.xml"
SUFFIX_KBR_TRL_FR_WORKS="fr-translations-works.csv"
SUFFIX_KBR_TRL_FR_CONT="fr-translations-contributors.csv"
SUFFIX_KBR_TRL_FR_NEWAUT="fr-translations-identified-authorities.csv"
SUFFIX_KBR_TRL_FR_BB="fr-translations-bb.csv"
SUFFIX_KBR_TRL_FR_PUB_COUNTRY="fr-translations-pub-country.csv"
SUFFIX_KBR_TRL_FR_COL_LINKS="fr-collection-links.csv"

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

# DATA SOURCE - KBR BELGIANS
#
SUFFIX_KBR_BELGIANS_CLEANED="belgians-cleaned.csv"
SUFFIX_KBR_BELGIANS_NORM="belgians-norm.csv"

# DATA SOURCE - BNF
#
SUFFIX_BNF_BELGIANS_IDS="bnf-belgian-contributor-ids.csv"
SUFFIX_BNF_BELGIAN_PUBS_IDS="bnf-belgian-contributor-publication-ids.csv"
SUFFIX_BNF_TRL_CONT_ORGS_IDS="bnf-translation-contributor-orgs-ids.csv"
SUFFIX_BNF_TRL_CONT_IDS="bnf-translation-contributor-persons-ids.csv"
SUFFIX_BNF_TRL_IDS_FR="bnf-translation-ids-fr-nl.csv"
SUFFIX_BNF_TRL_IDS_NL="bnf-translation-ids-nl-fr.csv"
SUFFIX_BNF_TRL_IDS="bnf-translation-ids.csv"
  
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

#
# LINKED DATA - KBR TRANSLATIONS
#
SUFFIX_KBR_TRL_LD="translations-and-contributions.ttl"
SUFFIX_KBR_NEWAUT_LD="translations-identified-authorities.ttl"
SUFFIX_KBR_TRL_BB_LD="translations-bb.ttl"
SUFFIX_KBR_TRL_PUB_COUNTRY_LD="translations-publication-countries.ttl"

#
# LINKED DATA - KBR LINKED AUTHORITIES
#
SUFFIX_KBR_LA_LD="linked-authorities.ttl"

#
# LINKED DATA - KBR BELGIANS
#
SUFFIX_KBR_BELGIANS_LD="belgians.ttl"

#
# LINKED DATA - BNF
#
SUFFIX_BNF_TRL_FR_LD="fr-translations.xml"
SUFFIX_BNF_TRL_NL_LD="nl-translations.xml"

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
  elif [ "$dataSource" = "master-data" ];
  then
    extractMasterData $integrationFolderName
  elif [ "$dataSource" = "bnf" ];
  then
    extractBnF $integrationFolderName
  elif [ "$dataSource" = "all" ];
  then
    extractKBR $integrationFolderName
    extractBnF $integrationFolderName
    extractMasterData $integrationFolderName
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
  elif [ "$dataSource" = "master-data" ];
  then
    transformMasterData $integrationFolderName
  elif [ "$dataSource" = "bnf" ];
  then
    transformBnF $integrationFolderName
  elif [ "$dataSource" = "all" ];
  then
    transformKBR $integrationFolderName
    transformBnF $integrationFolderName
    transformMasterData $integrationFolderName
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
  elif [ "$dataSource" = "master-data" ];
  then
    loadMasterData $integrationFolderName
  elif [ "$dataSource" = "bnf" ];
  then
    loadBnF $integrationFolderName
  elif [ "$dataSource" = "all" ];
  then
    loadMasterData $integrationFolderName
    loadBnF $integrationFolderName
    loadKBR $integrationFolderName
  fi

}

# -----------------------------------------------------------------------------
function query {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  queryFile="$DATA_PROFILE_QUERY_FILE"
  queryFileAgg="$DATA_PROFILE_AGG_QUERY_FILE"
  queryFileContBE="$DATA_PROFILE_CONT_BE_QUERY_FILE"
  queryFileContAll="$DATA_PROFILE_CONT_ALL_QUERY_FILE"
  queryFilePubsPerYear="$DATA_PROFILE_PUBS_PER_YEAR_QUERY_FILE"
  queryFilePubsPerCountry="$DATA_PROFILE_PUBS_PER_COUNTRY_QUERY_FILE"
  queryFilePubsPerLoc="$DATA_PROFILE_PUBS_PER_LOC_QUERY_FILE"
  queryFilePubsPerPbl="$DATA_PROFILE_PUBS_PER_PBL_QUERY_FILE"

  outputFile="$integrationName/$SUFFIX_DATA_PROFILE_FILE"
  outputFileAgg="$integrationName/$SUFFIX_DATA_PROFILE_AGG_FILE"
  outputFileContBE="$integrationName/$SUFFIX_DATA_PROFILE_CONT_BE_FILE"
  outputFileContAll="$integrationName/$SUFFIX_DATA_PROFILE_CONT_ALL_FILE"
  outputFilePubsPerYear="$integrationName/$SUFFIX_DATA_PROFILE_PUBS_PER_YEAR_FILE"
  outputFilePubsPerCountry="$integrationName/$SUFFIX_DATA_PROFILE_PUBS_PER_COUNTRY_FILE"
  outputFilePubsPerLoc="$integrationName/$SUFFIX_DATA_PROFILE_PUBS_PER_LOC_FILE"
  outputFilePubsPerPbl="$integrationName/$SUFFIX_DATA_PROFILE_PUBS_PER_PBL_FILE"

  echo "Creating the dataprofile CSV file ..."
  queryData "$TRIPLE_STORE_NAMESPACE" "$queryFile" "$ENV_SPARQL_ENDPOINT" "$outputFile"

  echo "Creating the dataprofile CSV file with aggregated values ..."
  queryData "$TRIPLE_STORE_NAMESPACE" "$queryFileAgg" "$ENV_SPARQL_ENDPOINT" "$outputFileAgg"

  echo "Creating the dataprofile CSV accompanying contributor file (Belgians) ..."
  queryData "$TRIPLE_STORE_NAMESPACE" "$queryFileContBE" "$ENV_SPARQL_ENDPOINT" "$outputFileContBE"

  echo "Creating the dataprofile CSV accompanying contributor file (all nationalities) ..."
  queryData "$TRIPLE_STORE_NAMESPACE" "$queryFileContAll" "$ENV_SPARQL_ENDPOINT" "$outputFileContAll"

  echo "Creating statistics about publications per language and year ..."
  queryData "$TRIPLE_STORE_NAMESPACE" "$queryFilePubsPerYear" "$ENV_SPARQL_ENDPOINT" "$outputFilePubsPerYear"

  echo "Creating statistics about publications per language and country ..."
  queryData "$TRIPLE_STORE_NAMESPACE" "$queryFilePubsPerCountry" "$ENV_SPARQL_ENDPOINT" "$outputFilePubsPerCountry"

  echo "Creating statistics about publications per language and location ..."
  queryData "$TRIPLE_STORE_NAMESPACE" "$queryFilePubsPerLoc" "$ENV_SPARQL_ENDPOINT" "$outputFilePubsPerLoc"

  echo "Creating statistics about publications per language and publisher ..."
  queryData "$TRIPLE_STORE_NAMESPACE" "$queryFilePubsPerPbl" "$ENV_SPARQL_ENDPOINT" "$outputFilePubsPerPbl"
}

# -----------------------------------------------------------------------------
function postprocess {
  local integrationName=$1

  integratedData="$integrationName/$SUFFIX_DATA_PROFILE_FILE"
  processedData="$integrationName/$SUFFIX_DATA_PROFILE_FILE_PROCESSED"

  contributorDataBE="$integrationName/$SUFFIX_DATA_PROFILE_CONT_BE_FILE"
  contributorDataAll="$integrationName/$SUFFIX_DATA_PROFILE_CONT_ALL_FILE"
  processedContributorsBE="$integrationName/$SUFFIX_DATA_PROFILE_CONT_BE_FILE_PROCESSED"
  processedContributorsAll="$integrationName/$SUFFIX_DATA_PROFILE_CONT_ALL_FILE_PROCESSED"

  source ../data-sources/py-etl-env/bin/activate

  echo "Postprocess integrated data ..."
  postprocessIntegratedData $integratedData $processedData

  echo "Postprocess contributor data (Belgians)..."
  postprocessContributorData $contributorDataBE $processedContributorsBE

  echo "Postprocess contributor data (all nationalities)..."
  postprocessContributorData $contributorDataAll $processedContributorsAll
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
  mkdir -p $integrationName/kbr/translations
  mkdir -p $integrationName/kbr/agents

  echo "EXTRACTION - Extract and clean KBR translations data"
  extractKBRTranslationsAndContributions "$integrationName" "$INPUT_KBR_TRL_NL" "$INPUT_KBR_TRL_FR"

  echo "EXTRACTION - Extract and clean KBR linked authorities data"
  extractKBRLinkedAuthorities "$integrationName" "$INPUT_KBR_LA_PERSON_NL" "$INPUT_KBR_LA_ORG_NL" "$INPUT_KBR_LA_PERSON_FR" "$INPUT_KBR_LA_ORG_FR"

  echo "EXTRACTION - Extract and clean KBR Belgians"
  extractKBRBelgians "$integrationName" "$INPUT_KBR_BELGIANS"
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
  bnfNLTranslations="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_IDS_NL"
  bnfFRTranslations="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_IDS_FR"
  bnfBelgianPublications="$integrationName/bnf/translations/$SUFFIX_BNF_BELGIAN_PUBS_IDS"
  bnfTranslationIDs="$integrationName/bnf/translations/$SUFFIX_BNF_TRL_IDS"

  bnfFRRelevantTranslationData="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_FR_LD"
  bnfNLRelevantTranslationData="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_NL_LD"
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
  extractBnFTranslations "$integrationName" "$INPUT_BNF_TRL_NL" "$bnfNLTranslations" 
  echo "EXTRACTION - Extract publication IDs of translations from BnF catalog export - FR-NL"
  extractBnFTranslations "$integrationName" "$INPUT_BNF_TRL_FR" "$bnfFRTranslations"


  # extract the actual data of translations with relevant Belgian contributors
  echo "EXTRACTION - Extract publication data about publications from BnF data - NL-FR"
  extractBnFRelevantPublicationData "$integrationName" "$INPUT_BNF_EDITIONS" "$bnfNLTranslations" "$bnfBelgianPublications" "$bnfNLRelevantTranslationData"
  echo "EXTRACTION - Extract publication data about publications from BnF data - NL-FR"
  extractBnFRelevantPublicationData "$integrationName" "$INPUT_BNF_EDITIONS" "$bnfFRTranslations" "$bnfBelgianPublications" "$bnfFRRelevantTranslationData"

  #
  # we also need related information of the identified publications from other data dumps
  #
  source ../data-sources/py-etl-env/bin/activate

  echo "EXTRACTION - Create list of both NL and FR BnF translation IDs"
  time python $SCRIPT_UNION_IDS $bnfNLTranslations $bnfFRTranslations -o $bnfTranslationIDs

  # extract contributor IDs of all translation contributors (also non-Belgian contributors)
  echo "EXTRACTION - Extract all BnF contributor IDs of BELTRANS translations (despite the nationality)"
  time python $SCRIPT_GET_RDF_XML_OBJECTS -i $INPUT_BNF_CONTRIBUTIONS -o $bnfPersonsBELTRANS -l $bnfTranslationIDs -p "dcterms:contributor"

  # extract contributor IDs of all translation contributors (orgs)
  echo "EXTRACTION - Extract all BnF contributor IDs of organizations"
  time python $SCRIPT_GET_RDF_XML_OBJECTS -i $INPUT_BNF_CONTRIBUTIONS -o $bnfOrgsBELTRANS -l $bnfTranslationIDs -p "marcrel:pbl"

  # extract the actual data of all BELTRANS translations contributors - persons
  echo "EXTRACTION - Extract BnF contributor data (persons)"
  time python $SCRIPT_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_PERSON_AUTHORS -o $bnfContributorDataPersons -f $bnfPersonsBELTRANS

  # extract the actual data of all BELTRANS translations contributors - orgs
  echo "EXTRACTION - Extract BnF contributor data (orgs)"
  time python $SCRIPT_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_ORG_AUTHORS -o $bnfContributorDataOrgs -f $bnfOrgsBELTRANS
  
  # extract the actual links between publications and contributors (not just looking up things) - ALL links are taken as the subject with all properties is extracted
  echo "EXTRACTION - Extract links between BELTRANS relevant BnF publications and BnF contributors"
  time python $SCRIPT_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONTRIBUTIONS -o $bnfContributionLinksData -f $bnfBelgianPublications -f $bnfTranslationIDs

  echo "EXTRACTION - Extract links between BnF contributors and ISNI"
  time python $SCRIPT_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_ISNI -o $bnfContributorIsniData -f $bnfPersonsBELTRANS

  echo "EXTRACTION - Extract links between BnF contributors and VIAF"
  time python $SCRIPT_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_VIAF -o $bnfContributorVIAFData -f $bnfPersonsBELTRANS

  echo "EXTRACTION - Extract links between BnF contributors and Wikidata"
  time python $SCRIPT_FILTER_RDF_XML_SUBJECTS -i $INPUT_BNF_CONT_WIKIDATA -o $bnfContributorWikidataData -f $bnfPersonsBELTRANS
}

# -----------------------------------------------------------------------------
function extractMasterData {

  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # create the folders to place the extracted translations and agents
  mkdir -p $integrationName/master-data

  echo "EXTRACTION - Nothing to extract from master data, copying files"
  cp "$INPUT_MASTER_MARC_ROLES" "$integrationName/master-data/$SUFFIX_MASTER_MARC_ROLES"
  cp "$INPUT_MASTER_MARC_BINDING_TYPES" "$integrationName/master-data/$SUFFIX_MASTER_BINDING_TYPES"
  cp "$INPUT_MASTER_COUNTRIES" "$integrationName/master-data/$SUFFIX_MASTER_COUNTRIES"
  cp "$INPUT_MASTER_LANGUAGES" "$integrationName/master-data/$SUFFIX_MASTER_LANGUAGES"
  cp "$INPUT_MASTER_GENDER" "$integrationName/master-data/$SUFFIX_MASTER_GENDER"
  cp "$INPUT_MASTER_THES_EN" "$integrationName/master-data/$SUFFIX_MASTER_THES_EN"
  cp "$INPUT_MASTER_THES_NL" "$integrationName/master-data/$SUFFIX_MASTER_THES_NL"
  cp "$INPUT_MASTER_THES_FR" "$integrationName/master-data/$SUFFIX_MASTER_THES_FR"

}

# -----------------------------------------------------------------------------
function transformKBR {

  local integrationName=$1

  # create the folder to place the transformed data
  mkdir -p $integrationName/kbr/rdf 

  echo "TRANSFORMATION - Map KBR translation data to RDF"
  mapKBRTranslationsAndContributions $integrationName

  echo "TRANSFORMATION - Map KBR linked authorities data to RDF"
  mapKBRLinkedAuthorities $integrationName

  echo "TRANSFORMATION - Map KBR Belgians data to RDF"
  mapKBRBelgians $integrationName
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
function extractKBRTranslationsAndContributions {

  #
  # KBR TRANSLATIONS
  # XML -> XML clean -> CSV -> TURTLE (kbr-translations.ttl)
  # mapping: kbr-translations.yml
  # named graph: <http://kbr-syracuse>
  #
  local integrationName=$1
  local kbrDutchTranslations=$2
  local kbrFrenchTranslations=$3


  # document which input was used
  printf "\nUsed input (KBR translations and contributors)\n* $kbrDutchTranslations\n* $kbrFrenchTranslations" >> "$integrationName/kbr/README.md"

  #
  # Define file names based on current integration directory and file name patterns
  #
  kbrDutchTranslationsCleaned="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_CLEANED"
  kbrFrenchTranslationsCleaned="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_CLEANED"

  kbrDutchTranslationsCSVWorks="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_WORKS"
  kbrFrenchTranslationsCSVWorks="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_WORKS"

  kbrDutchTranslationsCSVCont="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_CONT"
  kbrFrenchTranslationsCSVCont="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_CONT"

  kbrDutchTranslationsIdentifiedAuthorities="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_NEWAUT"
  kbrFrenchTranslationsIdentifiedAuthorities="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_NEWAUT"

  kbrDutchTranslationsCSVBB="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_BB"
  kbrFrenchTranslationsCSVBB="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_BB"

  kbrDutchTranslationsPubCountries="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_PUB_COUNTRY"
  kbrFrenchTranslationsPubCountries="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_PUB_COUNTRY"

  kbrDutchTranslationsCollectionLinks="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_COL_LINKS"
  kbrFrenchTranslationsCollectionLinks="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_COL_LINKS"
  
  source ../data-sources/py-etl-env/bin/activate

  echo "Clean Dutch translations ..."
  cleanTranslations "$kbrDutchTranslations" "$kbrDutchTranslationsCleaned"

  echo "Clean French translations ..."
  cleanTranslations "$kbrFrenchTranslations" "$kbrFrenchTranslationsCleaned"

  echo "Extract CSV from Dutch translations XML..."
  extractCSVFromXMLTranslations "$kbrDutchTranslationsCleaned" "$kbrDutchTranslationsCSVWorks" "$kbrDutchTranslationsCSVCont" "$kbrDutchTranslationsCollectionLinks"

  echo "Extract CSV from French translations XML..."
  extractCSVFromXMLTranslations "$kbrFrenchTranslationsCleaned" "$kbrFrenchTranslationsCSVWorks" "$kbrFrenchTranslationsCSVCont" "$kbrFrenchTranslationsCollectionLinks"

  echo "Extract BB assignments for Dutch translations ..."
  extractBBEntries "$kbrDutchTranslationsCSVWorks" "$kbrDutchTranslationsCSVBB"

  echo "Extract BB assignments for French translations ..."
  extractBBEntries "$kbrFrenchTranslationsCSVWorks" "$kbrFrenchTranslationsCSVBB"

  echo "Extract publication countries from Dutch translations ..."
  extractPubCountries "$kbrDutchTranslationsCSVWorks" "$kbrDutchTranslationsPubCountries"

  echo "Extract publication countries from French translations ..."
  extractPubCountries "$kbrFrenchTranslationsCSVWorks" "$kbrFrenchTranslationsPubCountries"

  echo "Extract newly identified contributors ..."
  extractIdentifiedAuthorities "$kbrDutchTranslationsCSVCont" "$kbrDutchTranslationsIdentifiedAuthorities"
  extractIdentifiedAuthorities "$kbrFrenchTranslationsCSVCont" "$kbrFrenchTranslationsIdentifiedAuthorities"

}

# -----------------------------------------------------------------------------
function extractKBRLinkedAuthorities {

  local integrationName=$1
  local kbrNLPersons=$2
  local kbrNLOrgs=$3
  local kbrFRPersons=$4
  local kbrFROrgs=$5

  # document which input was used
  printf "\nUsed input (KBR linked authorities) \n* $kbrNLPersons\n* $kbrNLOrgs\n* $kbrFRPersons\n* $kbrFROrgs" >> "$integrationName/kbr/README.md"

  #
  # Define file names based on current integration directory and file name patterns
  #
  kbrNLPersonsNorm="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_NL_NORM"
  kbrNLOrgsNorm="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_NL_NORM"
  kbrFRPersonsNorm="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_FR_NORM"
  kbrFROrgsNorm="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_FR_NORM"

  kbrNLPersonsCleaned="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_NL_CLEANED"
  kbrNLOrgsCleaned="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_NL_CLEANED"
  kbrFRPersonsCleaned="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_FR_CLEANED"
  kbrFROrgsCleaned="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_FR_CLEANED"

  source ../data-sources/py-etl-env/bin/activate

  echo "Clean authorities NL - Persons ..."
  normalizeCSVHeaders "$kbrNLPersons" "$kbrNLPersonsNorm" "$KBR_CSV_HEADER_CONVERSION"
  cleanAgents "$kbrNLPersonsNorm" "$kbrNLPersonsCleaned"

  echo "Clean authorities NL - Organizations ..."
  normalizeCSVHeaders "$kbrNLOrgs" "$kbrNLOrgsNorm" "$KBR_CSV_HEADER_CONVERSION"
  cleanAgents "$kbrNLOrgsNorm" "$kbrNLOrgsCleaned"

  echo "Clean authorities FR - Persons ..."
  normalizeCSVHeaders "$kbrFRPersons" "$kbrFRPersonsNorm" "$KBR_CSV_HEADER_CONVERSION"
  cleanAgents "$kbrFRPersonsNorm" "$kbrFRPersonsCleaned"

  echo "Clean authorities FR - Organizations ..."
  normalizeCSVHeaders "$kbrFROrgs" "$kbrFROrgsNorm" "$KBR_CSV_HEADER_CONVERSION"
  cleanAgents "$kbrFROrgsNorm" "$kbrFROrgsCleaned"

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

  source ../data-sources/py-etl-env/bin/activate

  echo "Clean Belgians ..."
  # currently this input has already normalized headers
  #normalizeCSVHeaders "$kbrBelgians" "$kbrBelgiansNorm" "$KBR_CSV_HEADER_CONVERSION"
  cleanAgents "$kbrBelgians" "$kbrBelgiansCleaned"
}

# -----------------------------------------------------------------------------
function extractBnFBelgianContributors {

  local integrationName=$1
  local bnfPersonAuthors=$2
  local bnfBelgianContributorIDs=$3

  # document which input was used
  printf "\nUsed input (BnF Belgian contributors)\n* $bnfPersonAuthors" >> "$integrationName/bnf/README.md"

  source ../data-sources/py-etl-env/bin/activate

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

  source ../data-sources/py-etl-env/bin/activate
  time python $SCRIPT_GET_RDF_XML_SUBJECTS -i $bnfEditionContributions -o $bnfBelgianPublicationIDs -p "marcrel:aut" -p "marcrel:ill" -p "marcrel:sce" -l $bnfBelgians
}

# -----------------------------------------------------------------------------
function extractBnFTranslations {
  local integrationName=$1
  local bnfTranslations=$2
  local bnfTranslationIDs=$3
 
  # document which input was used
  printf "\nUsed input (BnF translations used to extract relevant publication IDs)\n* $bnfTranslations\n" >> "$integrationName/bnf/README.md"

  source ../data-sources/py-etl-env/bin/activate
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

  source ../data-sources/py-etl-env/bin/activate
  time python $SCRIPT_FILTER_RDF_XML_SUBJECTS -i $bnfEditions  -o $bnfRelevantData -f $bnfTranslationIDs -f $bnfBelgianPubs
}

# -----------------------------------------------------------------------------
function mapKBRTranslationsAndContributions {

  local integrationName=$1

  kbrTranslationsTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_TRL_LD"
  kbrTranslationsIdentifiedAuthorities="$integrationName/kbr/rdf/$SUFFIX_KBR_NEWAUT_LD"
  kbrTranslationsBBTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_TRL_BB_LD"
  kbrTranslationsPubCountriesTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_TRL_PUB_COUNTRY_LD"

  # map the translations

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_WORKS_FR="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_WORKS"
  export RML_SOURCE_WORKS_NL="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_WORKS"
  export RML_SOURCE_CONT_FR="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_CONT"
  export RML_SOURCE_CONT_NL="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_CONT"
  export RML_SOURCE_COLLECTION_LINKS_FR="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_COL_LINKS"
  export RML_SOURCE_COLLECTION_LINKS_NL="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_COL_LINKS"

  # 2) execute the mapping
  echo "Map KBR translations and contributions ..."
  . map.sh ../data-sources/kbr/kbr-translations.yml $kbrTranslationsTurtle


  # map newly identified publishers

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_CONT_NL_IDENTIFIED="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_NEWAUT"
  export RML_SOURCE_KBR_CONT_FR_IDENTIFIED="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_NEWAUT"

  # 2) execute the mapping
  echo "Map KBR newly identified contributors ..."
  . map.sh ../data-sources/kbr/kbr-identified-authorities.yml $kbrTranslationsIdentifiedAuthorities

  # map belgian bibliography assignments

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_BB_NL="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_BB"
  export RML_SOURCE_KBR_BB_FR="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_BB"
  
  # 2) execute the mapping
  echo "Map KBR BB assignments ..."
  . map.sh ../data-sources/kbr/kbr-belgian-bibliography.yml $kbrTranslationsBBTurtle

  # map publication countries

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_PUB_COUNTRIES_NL="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_PUB_COUNTRY"
  export RML_SOURCE_KBR_PUB_COUNTRIES_FR="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_PUB_COUNTRY"

  # 2) execute the mapping
  echo "Map KBR publication countries ..."
  . map.sh ../data-sources/kbr/kbr-publication-countries.yml $kbrTranslationsPubCountriesTurtle

}

# -----------------------------------------------------------------------------
function mapKBRLinkedAuthorities {

  local integrationName=$1

  kbrLinkedAuthoritiesTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_LA_LD"

  # map the linked authorities

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_LINKED_AUTHORITIES_PERSONS_NL="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_NL_CLEANED"
  export RML_SOURCE_KBR_LINKED_AUTHORITIES_PERSONS_FR="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PERSONS_FR_CLEANED"
  export RML_SOURCE_KBR_LINKED_AUTHORITIES_ORGS_NL="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_NL_CLEANED"
  export RML_SOURCE_KBR_LINKED_AUTHORITIES_ORGS_FR="$integrationName/kbr/agents/$SUFFIX_KBR_LA_ORGS_FR_CLEANED"

  export RML_SOURCE_KBR_PUBLISHER_PLACES_FLANDERS="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PLACES_VLG"
  export RML_SOURCE_KBR_PUBLISHER_PLACES_WALLONIA="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PLACES_WAL"
  export RML_SOURCE_KBR_PUBLISHER_PLACES_BRUSSELS="$integrationName/kbr/agents/$SUFFIX_KBR_LA_PLACES_BRU"

  # 2) execute the mapping
  echo "Map KBR linked authorities ..."
  . map.sh ../data-sources/kbr/kbr-linked-authorities.yml $kbrLinkedAuthoritiesTurtle

}

# -----------------------------------------------------------------------------
function mapKBRBelgians {

  local integrationName=$1

  kbrBelgiansTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_BELGIANS_LD"

  # map the authorities

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_BELGIANS="$integrationName/kbr/agents/$SUFFIX_KBR_BELGIANS_CLEANED"

  # 2) execute the mapping
  echo "Map KBR Belgians ..."
  . map.sh ../data-sources/kbr/kbr-belgians.yml $kbrBelgiansTurtle
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

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # first delete content of the named graph in case it already exists
  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_KBR_TRL>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KBR_TRL"

  local kbrTranslationsAndContributions="$integrationName/kbr/rdf/$SUFFIX_KBR_TRL_LD"
  local kbrIdentifiedAuthorities="$integrationName/kbr/rdf/$SUFFIX_KBR_NEWAUT_LD"
  local kbrLinkedAuthorities="$integrationName/kbr/rdf/$SUFFIX_KBR_LA_LD"
  local kbrTranslationsBB="$integrationName/kbr/rdf/$SUFFIX_KBR_TRL_BB_LD"
  local kbrTranslationsPubCountries="$integrationName/kbr/rdf/$SUFFIX_KBR_TRL_PUB_COUNTRY_LD"
  local kbrBelgians="$integrationName/kbr/rdf/$SUFFIX_KBR_BELGIANS_LD"

  echo "Load KBR translations and contributions ..."
  uploadData "$TRIPLE_STORE_NAMESPACE"  "$kbrTranslationsAndContributions" "$FORMAT_TURTLE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KBR_TRL"

  echo "Load KBR BB assignments ..."
  uploadData "$TRIPLE_STORE_NAMESPACE"  "$kbrTranslationsBB" "$FORMAT_TURTLE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KBR_TRL"

  echo "Load KBR publication countries ..."
  uploadData "$TRIPLE_STORE_NAMESPACE"  "$kbrTranslationsPubCountries" "$FORMAT_TURTLE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KBR_TRL"

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_KBR_LA>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KBR_LA"
  
  # upload both linked authorities and newly identified authorities to the linked authorities named graph
  echo "Load KBR linked authorities ..."
  uploadData "$TRIPLE_STORE_NAMESPACE"  "$kbrLinkedAuthorities" "$FORMAT_TURTLE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KBR_LA"

  echo "Load KBR newly identified authorities ..."
  uploadData "$TRIPLE_STORE_NAMESPACE"  "$kbrIdentifiedAuthorities" "$FORMAT_TURTLE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KBR_LA"

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_KBR_BELGIANS>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KBR_BELGIANS"

  echo "Load KBR Belgians ..."
  uploadData "$TRIPLE_STORE_NAMESPACE"  "$kbrBelgians" "$FORMAT_TURTLE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_KBR_BELGIANS"

}

# -----------------------------------------------------------------------------
function loadBnF {
  local integrationName=$1

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)

  # first delete content of the named graph in case it already exists
  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_BNF_TRL_FR>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_TRL_FR"

  echo "Delete existing content in namespace <$TRIPLE_STORE_GRAPH_BNF_TRL_NL>"
  deleteNamedGraph "$TRIPLE_STORE_NAMESPACE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_TRL_NL"

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

  local bnfTranslationsFR="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_FR_LD"
  local bnfTranslationsNL="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_NL_LD"
  local bnfContributorData="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_LD"
  local bnfContributionLinksData="$integrationName/bnf/rdf/$SUFFIX_BNF_TRL_CONT_LINKS_LD"
  local bnfContributorIsniData="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_ISNI_LD"
  local bnfContributorVIAFData="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_VIAF_LD"
  local bnfContributorWikidataData="$integrationName/bnf/rdf/$SUFFIX_BNF_CONT_WIKIDATA_LD"

  echo "Load BNF translations FR-NL ..."
  uploadData "$TRIPLE_STORE_NAMESPACE" "$bnfTranslationsFR" "$FORMAT_RDF_XML" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_TRL_FR"

  echo "Load BNF translations NL-FR ..."
  uploadData "$TRIPLE_STORE_NAMESPACE" "$bnfTranslationsNL" "$FORMAT_RDF_XML" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_TRL_NL"

  echo "Load BnF contributors ..."
  uploadData "$TRIPLE_STORE_NAMESPACE" "$bnfContributorData" "$FORMAT_RDF_XML" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_CONT"

  echo "Load BnF publication-contributor links ..."
  uploadData "$TRIPLE_STORE_NAMESPACE" "$bnfContributionLinksData" "$FORMAT_RDF_XML" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_TRL_CONT_LINKS"

  echo "Load external links of BnF contributors - ISNI ..."
  uploadData "$TRIPLE_STORE_NAMESPACE" "$bnfContributorIsniData" "$FORMAT_RDF_XML" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_CONT_ISNI"

  echo "Load external links of BnF contributors - VIAF ..."
  uploadData "$TRIPLE_STORE_NAMESPACE" "$bnfContributorIsniData" "$FORMAT_RDF_XML" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_CONT_VIAF"

  echo "Load external links of BnF contributors - WIKIDATA ..."
  uploadData "$TRIPLE_STORE_NAMESPACE" "$bnfContributorIsniData" "$FORMAT_RDF_XML" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_BNF_CONT_WIKIDATA"

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

  echo "Load master data - mapped content"
  uploadData "$TRIPLE_STORE_NAMESPACE" "$masterDataTurtle" "$FORMAT_TURTLE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_MASTER"

  echo "Load master data - countries"
  uploadData "$TRIPLE_STORE_NAMESPACE" "$masterDataCountries" "$FORMAT_NT" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_MASTER"

  echo "Load master data - languages"
  uploadData "$TRIPLE_STORE_NAMESPACE" "$masterDataLanguages" "$FORMAT_NT" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_MASTER"

  echo "Load master data - gender"
  uploadData "$TRIPLE_STORE_NAMESPACE" "$masterDataGender" "$FORMAT_TURTLE" "$ENV_SPARQL_ENDPOINT" "$TRIPLE_STORE_GRAPH_MASTER"

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

  checkFile $input
  python $SCRIPT_EXTRACT_BB -i $input -o $output
}

# -----------------------------------------------------------------------------
function extractPubCountries {
  local input=$1
  local output=$2

  checkFile $input
  python $SCRIPT_EXTRACT_PUB_COUNTRIES -i $input -o $output
}

# -----------------------------------------------------------------------------
function getSubjects {
  local input=$1
  local config=$2
  local output=$3

  python $SCRIPT_GET_RDF_XML_SUBJECTS -i $input -o $output -f $config
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

  . $SCRIPT_UPLOAD_DATA "$namespace" "$fileToUpload" "$format" "$endpoint" "$namedGraph"
}

# -----------------------------------------------------------------------------
function deleteNamedGraph {
  local namespace=$1
  local endpoint=$2
  local namedGraph=$3

  . $SCRIPT_DELETE_NAMED_GRAPH "$namespace" "$endpoint" "$namedGraph"
}

# -----------------------------------------------------------------------------
function queryData {
  local namespace=$1
  local queryFile=$2
  local endpoint=$3
  local outputFile=$4

#  . $SCRIPT_QUERY_DATA "$namespace" "$queryFile" "$endpoint" "$outputFile"
  . $SCRIPT_QUERY_DATA "$endpoint/namespace/$namespace/sparql" "$queryFile" "$outputFile"
}

# -----------------------------------------------------------------------------
function postprocessIntegratedData {

  local input=$1
  local output=$2

  checkFile $input
  python $SCRIPT_POSTPROCESS_QUERY_RESULT -i "$input" -o "$output"

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
  echo "extract (e) transform (t) load (l) query (q) and postprocess (p): 'etl', 'etlq', 'etlqp', 'e', 'et', 't', 'l', 'tl', 'q' etc"
  exit 1
else
  if [ "$1" = "etlqp" ];
  then
    extract $2 $3
    transform $2 $3
    load $2 $3
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

  elif [ "$1" = "tl" ];
  then
    transform $2 $3
    load $3 $3

  else
    echo "uknown command, please use different combinations of extract (e) transform (t) load (l) query (q) and postprocess (p): 'etl', 'etlq', 'etlqp', 'e', 'et', 't', 'l', 'tl', 'q' etc"
    exit 1
  fi
fi
