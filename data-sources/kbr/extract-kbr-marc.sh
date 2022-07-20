
SCRIPT_CLEAN_TRANSLATIONS="clean-marc-slim.py"
SCRIPT_TRANSFORM_TRANSLATIONS="marc-to-csv.py"
SCRIPT_CHANGE_PUBLISHER_NAME="change-publisher-name.py"
SCRIPT_DEDUPLICATE_KBR_PUBLISHERS="deduplicate-publishers.py"
SCRIPT_EXTRACT_SEPARATED_COL="extract-and-normalize-separated-strings.py"
SCRIPT_EXTRACT_IDENTIFIED_AUTHORITIES="get-identified-authorities.sh"

INPUT_KBR_PBL_REPLACE_LIST="agents/publisher-name-mapping.csv"
INPUT_KBR_ORGS_LOOKUP="agents/aorg.csv"

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
function extractCSVFromXMLTranslations {
  local inputXML=$1
  local outputCSVWorks=$2
  local outputCSVContributors=$3
  local outputCollectionLinks=$4

  checkFile $inputXML
  python $SCRIPT_TRANSFORM_TRANSLATIONS -i $inputXML -w $outputCSVWorks -c $outputCSVContributors -l $outputCollectionLinks
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
function extractIdentifiedAuthorities {
  local input=$1
  local output=$2

  checkFile $input
  . $SCRIPT_EXTRACT_IDENTIFIED_AUTHORITIES $input $output
}

# -----------------------------------------------------------------------------
function extractKBRMARC {

  local outputFolder=$1
  local inputFile=$2
  local namePattern=$3

  # DutchTranslations = NL-FR
  # FrenchTranslations = FR-NL

  #
  # Define file names based on input and file name patterns
  #
  inputFileCleaned="$outputFolder/$namePattern-cleaned.xml"
  inputFileCSVWorks="$outputFolder/$namePattern-works.csv"

  inputFileCSVCont="$outputFolder/$namePattern-contributions.csv"
  inputFileCSVContReplaced="$outputFolder/$namePattern-contributions-replaced.csv"
  inputFileCSVContDedup="$outputFolder/$namePattern-contributions-deduplicated.csv"

  inputFileIdentifiedAuthorities="$outputFolder/$namePattern-new-authorities.csv"

  inputFileCSVBB="$outputFolder/$namePattern-bb.csv"
  inputFilePubCountries="$outputFolder/$namePattern-pub-country.csv"
  inputFilePubPlaces="$outputFolder/$namePattern-pub-place.csv"
  inputFileCollectionLinks="$outputFolder/$namePattern-collection-links.csv"
  inputFileISBN10="$outputFolder/$namePattern-isbn10.csv"
  inputFileISBN13="$outputFolder/$namePattern-isbn13.csv"
  
  source py-kbr-etl-env/bin/activate

  echo "Clean translations $namePattern ..."
  cleanTranslations "$inputFile" "$inputFileCleaned"


  echo "Extract CSV from translations XML $namePattern ..."
  extractCSVFromXMLTranslations "$inputFileCleaned" "$inputFileCSVWorks" "$inputFileCSVCont" "$inputFileCollectionLinks"

  echo "Replace publisher names to support deduplication - $namePattern"
  python $SCRIPT_CHANGE_PUBLISHER_NAME -l $INPUT_KBR_PBL_REPLACE_LIST -i $inputFileCSVCont -o $inputFileCSVContReplaced


  echo "Deduplicate newly identified contributors - $namePattern"
  python $SCRIPT_DEDUPLICATE_KBR_PUBLISHERS -l $INPUT_KBR_ORGS_LOOKUP -i $inputFileCSVContReplaced -o $inputFileCSVContDedup


  echo "Extract BB assignments for translations $namePattern ..."
  extractBBEntries "$inputFileCSVWorks" "$inputFileCSVBB"


  echo "Extract publication countries from translations $namePattern ..."
  extractPubCountries "$inputFileCSVWorks" "$inputFilePubCountries"


  echo "Extract publication places from translations $namePattern..."
  extractPubPlaces "$inputFileCSVWorks" "$inputFilePubPlaces"


  echo "Extract (possibly multiple) ISBN10 identifiers per translation - $namePattern"
  extractISBN10 "$inputFileCSVWorks" "$inputFileISBN10"

  echo "Extract (possibly multiple) ISBN13 identifiers per translation - $namePattern"
  extractISBN13 "$inputFileCSVWorks" "$inputFileISBN13"


  echo "Extract newly identified contributors ..."
  extractIdentifiedAuthorities "$inputFileCSVContDedup" "$inputFileIdentifiedAuthorities"

}


extractKBRMARC "translations/originals/csv" "translations/originals/BELTRANS_FR-NL_FR-gelinkte-documenten.xml" "fr-nl_fr"
extractKBRMARC "translations/originals/csv" "translations/originals/BELTRANS_NL-FR_NL-gelinkte-documenten.xml" "nl-fr_nl"
