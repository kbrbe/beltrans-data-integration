#!/bin/bash

SCRIPT_CLEAN_TRANSLATIONS="../data-sources/kbr/clean-marc-slim.py"
SCRIPT_CLEAN_AGENTS="../data-sources/kbr/pre-process-kbr-authors.py"
SCRIPT_TRANSFORM_TRANSLATIONS="../data-sources/kbr/marc-to-csv.py"
SCRIPT_NORMALIZE_HEADERS="../data-sources/kbr/replace-headers.py"
SCRIPT_EXTRACT_IDENTIFIED_AUTHORITIES="../data-sources/kbr/get-identified-authorities.sh"
SCRIPT_EXTRACT_BB="../data-sources/kbr/extract-belgian-bibliography.py"
SCRIPT_EXTRACT_PUB_COUNTRIES="../data-sources/kbr/extract-publication-countries.py"

SCRIPT_UPLOAD_DATA="../utils/upload-data.sh"
SCRIPT_DELETE_NAMED_GRAPH="../utils/delete-named-graph.sh"
SCRIPT_QUERY_DATA="../utils/query-data.sh"
SCRIPT_POSTPROCESS_QUERY_RESULT="post-process-integration-result.py"
SCRIPT_POSTPROCESS_QUERY_CONT_RESULT="post-process-contributors.py"

KBR_CSV_HEADER_CONVERSION="../data-sources/kbr/author-headers.csv"

# #############################################################################
#
# INPUT FILENAMES
#

# KBR - translations
INPUT_KBR_TRL_NL="../data-sources/kbr/translations/ExportSyracuse_20211213_NL-FR_1970-2020_3866records.xml"
INPUT_KBR_TRL_FR="../data-sources/kbr/translations/ExportSyracuse_20211213_FR-NL_1970-2020_9239records.xml"

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
TRIPLE_STORE_GRAPH_KBR_LA="http://kbr-linked-authorities"
TRIPLE_STORE_GRAPH_KBR_BELGIANS="http://kbr-belgians"
TRIPLE_STORE_GRAPH_MASTER="http://master-data"

# if it is a blazegraph triple store
TRIPLE_STORE_NAMESPACE="integration"

FORMAT_TURTLE="text/turtle"
FORMAT_NT="text/rdf+n3"

DATA_PROFILE_QUERY_FILE="dataprofile.sparql"
DATA_PROFILE_AGG_QUERY_FILE="dataprofile-aggregated.sparql"
DATA_PROFILE_CONT_QUERY_FILE="contributors.sparql"
SUFFIX_DATA_PROFILE_FILE="integrated-data.csv"
SUFFIX_DATA_PROFILE_CONT_FILE="integrated-data-contributors.csv"
SUFFIX_DATA_PROFILE_AGG_FILE="integrated-data-aggregated.csv"
SUFFIX_DATA_PROFILE_FILE_PROCESSED="integrated-data-processed.csv"
SUFFIX_DATA_PROFILE_CONT_FILE_PROCESSED="integrated-data-contributors-processed.csv"

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
SUFFIX_KBR_TRL_FR_CLEANED="fr-translations-cleaned.xml"
SUFFIX_KBR_TRL_FR_WORKS="fr-translations-works.csv"
SUFFIX_KBR_TRL_FR_CONT="fr-translations-contributors.csv"
SUFFIX_KBR_TRL_FR_NEWAUT="fr-translations-identified-authorities.csv"
SUFFIX_KBR_TRL_FR_BB="fr-translations-bb.csv"
SUFFIX_KBR_TRL_FR_PUB_COUNTRY="fr-translations-pub-country.csv"

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
  elif [ "$dataSource" = "all" ];
  then
    extractKBR $integrationFolderName
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
  elif [ "$dataSource" = "all" ];
  then
    transformKBR $integrationFolderName
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
  elif [ "$dataSource" = "all" ];
  then
    loadMasterData $integrationFolderName
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
  queryFileCont="$DATA_PROFILE_CONT_QUERY_FILE"

  outputFile="$integrationName/$SUFFIX_DATA_PROFILE_FILE"
  outputFileAgg="$integrationName/$SUFFIX_DATA_PROFILE_AGG_FILE"
  outputFileCont="$integrationName/$SUFFIX_DATA_PROFILE_CONT_FILE"

  echo "Creating the dataprofile CSV file ..."
  queryData "$TRIPLE_STORE_NAMESPACE" "$queryFile" "$ENV_SPARQL_ENDPOINT" "$outputFile"

  echo "Creating the dataprofile CSV file with aggregated values ..."
  queryData "$TRIPLE_STORE_NAMESPACE" "$queryFileAgg" "$ENV_SPARQL_ENDPOINT" "$outputFileAgg"

  echo "Creating the dataprofile CSV accompanying contributor file ..."
  queryData "$TRIPLE_STORE_NAMESPACE" "$queryFileCont" "$ENV_SPARQL_ENDPOINT" "$outputFileCont"
}

# -----------------------------------------------------------------------------
function postprocess {
  local integrationName=$1

  integratedData="$integrationName/$SUFFIX_DATA_PROFILE_FILE"
  processedData="$integrationName/$SUFFIX_DATA_PROFILE_FILE_PROCESSED"

  contributorData="$integrationName/$SUFFIX_DATA_PROFILE_CONT_FILE"
  processedContributors="$integrationName/$SUFFIX_DATA_PROFILE_CONT_FILE_PROCESSED"

  source ../data-sources/py-etl-env/bin/activate

  echo "Postprocess integrated data ..."
  postprocessIntegratedData $integratedData $processedData

  echo "Postprocess contributor data ..."
  postprocessContributorData $contributorData $processedContributors
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
  printf "Used input\n* $kbrDutchTranslations\n* $kbrFrenchTranslations" >> "$integrationName/kbr/README.md"

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
  
  source ../data-sources/py-etl-env/bin/activate

  echo "Clean Dutch translations ..."
  cleanTranslations "$kbrDutchTranslations" "$kbrDutchTranslationsCleaned"

  echo "Clean French translations ..."
  cleanTranslations "$kbrFrenchTranslations" "$kbrFrenchTranslationsCleaned"

  echo "Extract CSV from Dutch translations XML..."
  extractCSVFromXMLTranslations "$kbrDutchTranslationsCleaned" "$kbrDutchTranslationsCSVWorks" "$kbrDutchTranslationsCSVCont"

  echo "Extract CSV from French translations XML..."
  extractCSVFromXMLTranslations "$kbrFrenchTranslationsCleaned" "$kbrFrenchTranslationsCSVWorks" "$kbrFrenchTranslationsCSVCont"

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
  printf "Used input\n* $kbrNLPersons\n* $kbrNLOrgs\n* $kbrFRPersons\n*$kbrFROrgs" >> "$integrationName/kbr/README.md"

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
  printf "Used input\n* $kbrBelgians" >> "$integrationName/kbr/README.md"

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

  checkFile $inputXML
  python $SCRIPT_TRANSFORM_TRANSLATIONS -i $inputXML -w $outputCSVWorks -c $outputCSVContributors
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

  . $SCRIPT_QUERY_DATA "$namespace" "$queryFile" "$endpoint" "$outputFile"
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
  echo "use 'bash integrate-data.sh <command> <data source> <integration folder name>, whereas command is either 'extract', 'transform' or 'load'"
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
