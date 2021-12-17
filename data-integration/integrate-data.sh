#!/bin/bash

SCRIPT_CLEAN_TRANSLATIONS="../data-sources/kbr/clean-marc-slim.py"
SCRIPT_CLEAN_AGENTS="../data-sources/kbr/pre-process-kbr-authors.py"
SCRIPT_TRANSFORM_TRANSLATIONS="../data-sources/kbr/marc-to-csv.py"
SCRIPT_NORMALIZE_HEADERS="../data-sources/kbr/replace-headers.py"
SCRIPT_EXTRACT_IDENTIFIED_AUTHORITIES="../data-sources/kbr/get-identified-authorities.sh"

KBR_CSV_HEADER_CONVERSION="../data-sources/kbr/author-headers.csv"

#
# Input filenames
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

# MASTER DATA

INPUT_MASTER_MARC_ROLES="../data-sources/master-data/marc-roles.csv"
INPUT_MASTER_MARC_BINDING_TYPES="../data-sources/master-data/binding-types.csv"
INPUT_MASTER_THES_EN="../data-sources/master-data/thesaurus-belgian-bibliography-en-hierarchy.csv"
INPUT_MASTER_THES_NL="../data-sources/master-data/thesaurus-belgian-bibliography-nl-hierarchy.csv"
INPUT_MASTER_THES_FR="../data-sources/master-data/thesaurus-belgian-bibliography-fr-hierarchy.csv"

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
SUFFIX_KBR_TRL_FR_CLEANED="fr-translations-cleaned.xml"
SUFFIX_KBR_TRL_FR_WORKS="fr-translations-works.csv"
SUFFIX_KBR_TRL_FR_CONT="fr-translations-contributors.csv"
SUFFIX_KBR_TRL_FR_NEWAUT="fr-translations-identified-authorities.csv"

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

# DATA SOURCE - MASTER DATA
#
SUFFIX_MASTER_MARC_ROLES="marc-roles.csv"
SUFFIX_MASTER_BINDING_TYPES="binding-types.csv"
SUFFIX_MASTER_THES_EN="thesaurus-belgian-bibliography-en-hierarchy.csv"
SUFFIX_MASTER_THES_NL="thesaurus-belgian-bibliography-nl-hierarchy.csv"
SUFFIX_MASTER_THES_FR="thesaurus-belgian-bibliography-fr-hierarchy.csv"

#
# LINKED DATA - KBR TRANSLATIONS
#
SUFFIX_KBR_TRL_LD="translations-and-contributions.ttl"
SUFFIX_KBR_NEWAUT_LD="translations-identified-authorities.ttl"

#
# LINKED DATA - KBR LINKED AUTHORITIES
#
SUFFIX_KBR_LA_LD="linked-authorities.ttl"

#
# LINKED DATA - MASTER DATA
#
SUFFIX_MASTER_LD="master-data.ttl"

# -----------------------------------------------------------------------------
function extract {

  local dataSource=$1
  local integrationFolderName=$2

  if [ -d "$integrationFolderName" ];
  then
    echo "the specified integration folder already exists, please provide the name of a new folder"
    exit 1
  fi

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
}

# -----------------------------------------------------------------------------
function query {
  echo"todo: query sparql endpoint"
}

# -----------------------------------------------------------------------------
function postprocess {
  echo "todo: postproces query result of sparql endpoint"
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
  
  source ../data-sources/py-etl-env/bin/activate

  echo "Clean Dutch translations ..."
  cleanTranslations "$kbrDutchTranslations" "$kbrDutchTranslationsCleaned"

  echo "Clean French translations ..."
  cleanTranslations "$kbrFrenchTranslations" "$kbrFrenchTranslationsCleaned"

  echo "Extract CSV from Dutch translations XML..."
  extractCSVFromXMLTranslations "$kbrDutchTranslationsCleaned" "$kbrDutchTranslationsCSVWorks" "$kbrDutchTranslationsCSVCont"

  echo "Extract CSV from French translations XML..."
  extractCSVFromXMLTranslations "$kbrFrenchTranslationsCleaned" "$kbrFrenchTranslationsCSVWorks" "$kbrFrenchTranslationsCSVCont"

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
function mapKBRTranslationsAndContributions {

  local integrationName=$1

  kbrTranslationsTurtle="$integrationName/kbr/rdf/$SUFFIX_KBR_TRL_LD"
  kbrTranslationsIdentifiedAuthorities="$integrationName/kbr/rdf/$SUFFIX_KBR_NEWAUT_LD"

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
    query
    postprocess
  elif [ "$1" = "qp" ];
  then
    query
    postprocess

  elif [ "$1" = "q" ];
  then
    query

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
    echo "uknown command, please use different combinations of extract (e) transform (t) and load (l): 'etl', 'e', 'et', 't', 'l', 'tl'"
    exit 1
  fi
fi
