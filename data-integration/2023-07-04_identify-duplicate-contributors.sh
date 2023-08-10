
CORPUS_VERSION="2023-06-30"
INPUT="corpus-versions/$CORPUS_VERSION/csv/integrated-data-enriched.csv"
OUTPUT_PATH="corpus-versions/$CORPUS_VERSION"

declare -a roles=("author" "translator" "illustrator" "scenarist" "publishingDirector")

for r in "${roles[@]}"
do
  outputFile="$OUTPUT_PATH/correlations_$r.csv"
  columnName="$r""Identifiers"

  echo -n "Matching for role '$r': "
  python identify_duplicate_contributors.py \
    -i $INPUT \
    -o $outputFile \
    --column $columnName \
    --output-column targetIdentifier \
    --output-column targetKBRIdentifier \
    --output-column targetBnFIdentifier \
    --output-column targetKBIdentifier \
    --output-column targetUnescoIdentifier \
    --csv-delimiter ',' \
    --column-value-delimiter ';' \
    --new-column-value-delimiter ';'
done
