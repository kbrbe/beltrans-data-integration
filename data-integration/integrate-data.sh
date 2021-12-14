#!/bin/bash

SCRIPT_CLEAN_TRANSLATIONS="../data-sources/kbr/clean-marc-slim.py"
SCRIPT_CLEAN_AGENTS="../data-sources/kbr/pre-process-kbr-authors.py"
SCRIPT_TRANSFORM_TRANSLATIONS="../data-sources/kbr/marc-to-csv.py"
SCRIPT_NORMALIZE_HEADERS="../data-sources/kbr/replace-headers.py"

# -----------------------------------------------------------------------------
function main {

  integrationName=$1

  mkdir -p $integrationName/kbr/translations
  mkdir -p $integrationName/kbr/agents

  source ../data-sources/py-etl-env/bin/activate

  # get environment variables
  export $(cat .env | sed 's/#.*//g' | xargs)


  kbrDutchTranslations="../data-sources/kbr/translations/ExportSyracuse_20211213_NL-FR_1970-2020_3866records.xml"
  kbrFrenchTranslations="../data-sources/kbr/translations/ExportSyracuse_20211213_FR-NL_1970-2020_9239records.xml"
  mapKBRTranslationsAndContributions $kbrDutchTranslations $kbrFrenchTranslations

  #mapKBRLinkedAuthorities


}

# -----------------------------------------------------------------------------
function mapKBRLinkedAuthorities {

  kbrDutchLinkedOrgs="../data-sources/kbr/agents/KBR_1970-2020_NL-FR_AUT-lies_AORG_xxrecords-all-fields.csv"
  kbrDutchLinkedPersons="../data-sources/kbr/agents/KBR_1970-2020_NL-FR_AUT-lies_APEP_xxrecords-all-fields.csv"
  kbrFrenchLinkedOrgs="../data-sources/kbr/agents/KBR_1970-2020_FR-NL_AUT-lies_AORG_xxrecords-all-fields.csv"
  kbrFrenchLinkedPersons="../data-sources/kbr/agents/KBR_1970-2020_FR-NL_AUT-lies_APEP_xxrecords-all-fields.csv"
}

# -----------------------------------------------------------------------------
function mapKBRTranslationsAndContributions {

  #
  # KBR TRANSLATIONS
  # XML -> XML clean -> CSV -> TURTLE (kbr-translations.ttl)
  # mapping: kbr-translations.yml
  # named graph: <http://kbr-syracuse>
  #
  kbrDutchTranslations=$1
  kbrFrenchTranslations=$1

  # document which input was used
  printf "Used input\n* $kbrDutchTranslations\n* $kbrFrenchTranslations" > $integrationName/README.md

  # output files
  kbrDutchTranslationsCleaned="$integrationName/kbr/translations/nl-translations-cleaned.xml"
  kbrFrenchTranslationsCleaned="$integrationName/kbr/translations/fr-translations-cleaned.xml"
  kbrDutchTranslationsCSVWorks="$integrationName/kbr/translations/nl-translations-works.csv"
  kbrFrenchTranslationsCSVWorks="$integrationName/kbr/translations/fr-translations-works.csv"
  kbrDutchTranslationsCSVCont="$integrationName/kbr/translations/nl-translations-contributors.csv"
  kbrFrenchTranslationsCSVCont="$integrationName/kbr/translations/fr-translations-contributors.csv"
  
  kbrTranslationsTurtle="$integrationName/kbr/translations-and-contributions.ttl"

  echo "Clean Dutch translations ..."
  cleanTranslations $kbrDutchTranslations $kbrDutchTranslationsCleaned

  echo "Clean French translations ..."
  cleanTranslations $kbrFrenchTranslations $kbrFrenchTranslationsCleaned

  echo "Transform Dutch translations ..."
  transformXMLTranslations $kbrDutchTranslationsCleaned $kbrDutchTranslationsCSVWorks $kbrDutchTranslationsCSVCont

  echo "Transform French translations ..."
  transformXMLTranslations $kbrFrenchTranslationsCleaned $kbrFrenchTranslationsCSVWorks $kbrFrenchTranslationsCSVCont

  # map the translations

  # 1) specify the input for the mapping (env variables taken into account by the YARRRML mapping)
  export RML_SOURCE_WORKS_FR=$kbrFrenchTranslationsCSVWorks
  export RML_SOURCE_WORKS_NL=$kbrDutchTranslationsCSVWorks
  export RML_SOURCE_CONT_FR=$kbrFrenchTranslationsCSVCont
  export RML_SOURCE_CONT_NL=$kbrDutchTranslationsCSVCont

  # 2) execute the mapping
  . map.sh ../data-sources/kbr/kbr-translations.yml $kbrTranslationsTurtle



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
function transformXMLTranslations {
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

if [ "$#" -ne 1 ];
then
  echo "use 'bash integrate-data.sh <integration folder name>"
  exit 1
else
  echo "Using '$1'"
  if [ -d "$1" ];
  then
    echo "the specified integration folder already exists, please provide the name of a new folder"
    exit 1
  else
    echo "main '$1'"
    main "$1"
  fi
fi
