#!/bin/bash

SCRIPT_CLEAN_TRANSLATIONS="../data-sources/kbr/clean-marc-slim.py"
SCRIPT_CLEAN_AGENTS="../data-sources/kbr/pre-process-kbr-authors.py"
SCRIPT_TRANSFORM_TRANSLATIONS="../data-sources/kbr/marc-to-csv.py"
SCRIPT_NORMALIZE_HEADERS="../data-sources/kbr/replace-headers.py"
SCRIPT_EXTRACT_IDENTIFIED_AUTHORITIES="../data-sources/kbr/get-identified-authorities.sh"

#
# Input filenames
#
# KBR
INPUT_KBR_TRL_NL="../data-sources/kbr/translations/ExportSyracuse_20211213_NL-FR_1970-2020_3866records.xml"
INPUT_KBR_TRL_FR="../data-sources/kbr/translations/ExportSyracuse_20211213_FR-NL_1970-2020_9239records.xml"


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

# DATA SOURCE - KBR LINKED AUTHORITIES
#
SUFFIX_KBR_LA_NL="nl-translations-identified-authorities.csv"
SUFFIX_KBR_LA_FR="fr-translations-identified-authorities.csv"

#
# LINKED DATA - KBR TRANSLATIONS
#
SUFFIX_KBR_TRL_LD="translations-and-contributions.ttl"
SUFFIX_KBR_NEWAUT_LD="translations-identified-authorities.ttl"

#
# LINKED DATA - KBR LINKED AUTHORITIES
#
SUFFIX_KBR_LA_LD="linked-authorities.ttl"


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
  elif [ "$dataSource" = "all" ];
  then
    extractKBR $integrationFolderName
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
  elif [ "$dataSource" = "all" ];
  then
    transformKBR $integrationFolderName
  fi
  
}

# -----------------------------------------------------------------------------
function load {

  local dataSource=$1
  local integrationFolderName=$2

  folderHasToExist $integrationFolderName
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

  echo "EXTRACTION - Extract and clean KBR data"
  extractKBRTranslationsAndContributions "$integrationName" "$INPUT_KBR_TRL_NL" "$INPUT_KBR_TRL_FR"

}

# -----------------------------------------------------------------------------
function transformKBR {

  local integrationName=$1

  # create the folder to place the transformed data
  mkdir -p $integrationName/kbr/rdf 

  echo "TRANSFORMATION - Map KBR data to RDF"
  mapKBRTranslationsAndContributions $integrationName
}

# -----------------------------------------------------------------------------
function mapKBRLinkedAuthorities {

  kbrDutchLinkedOrgs="../data-sources/kbr/agents/KBR_1970-2020_NL-FR_AUT-lies_AORG_xxrecords-all-fields.csv"
  kbrDutchLinkedPersons="../data-sources/kbr/agents/KBR_1970-2020_NL-FR_AUT-lies_APEP_xxrecords-all-fields.csv"
  kbrFrenchLinkedOrgs="../data-sources/kbr/agents/KBR_1970-2020_FR-NL_AUT-lies_AORG_xxrecords-all-fields.csv"
  kbrFrenchLinkedPersons="../data-sources/kbr/agents/KBR_1970-2020_FR-NL_AUT-lies_APEP_xxrecords-all-fields.csv"
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
  printf "Used input\n* $kbrDutchTranslations\n* $kbrFrenchTranslations" > "$integrationName/kbr/README.md"

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
  echo "Map translations and contributions ..."
  . map.sh ../data-sources/kbr/kbr-translations.yml $kbrTranslationsTurtle


  # map newly identified publishers

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_KBR_CONT_NL_IDENTIFIED="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_NL_NEWAUT"
  export RML_SOURCE_KBR_CONT_FR_IDENTIFIED="$integrationName/kbr/translations/$SUFFIX_KBR_TRL_FR_NEWAUT"

  # 2) execute the mapping
  echo "Map newly identified contributors ..."
  . map.sh ../data-sources/kbr/kbr-identified-authorities.yml $kbrTranslationsIdentifiedAuthorities


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
  if [ "$1" = "etl" ];
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
