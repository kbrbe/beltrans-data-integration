
CORPUS_VERSION="2023-04-28"
UPDATE_DATE="2023-07-05"

CONTRIBUTIONS_CSV="/home/slieber/repos/kbr/beltrans-data/data-integration/corpus-versions/$CORPUS_VERSION/unesco/unesco-contributions.csv"
CURATED_CONTRIBUTORS="/home/slieber/repos/kbr/beltrans-data/data-sources/unesco/2023-07-04_unesco-unique-contributors.csv"
UPDATED_CONTRIBUTIONS="/home/slieber/repos/kbr/beltrans-data/data-integration/corpus-versions/$CORPUS_VERSION/unesco/$UPDATE_DATE""_updated-contributions-with-curated-types.csv"
INPUT_CSV_2="/home/slieber/repos/kbr/beltrans-data/data-integration/corpus-versions/$CORPUS_VERSION/unesco/unesco_translations.csv"
OUTPUT_CSV="/home/slieber/repos/kbr/beltrans-data/data-integration/corpus-versions/$CORPUS_VERSION/unesco/2023-07-05_merged-contributions.csv"

python -m tools.csv.update_column \
  --csv-1 $CONTRIBUTIONS_CSV \
  --csv-2 $CURATED_CONTRIBUTORS \
  --output-csv $UPDATED_CONTRIBUTIONS \
  --column-to-be-updated "type" \
  --column-with-new-values "type" \
  --id-column-1 "contributorID" \
  --id-column-2 "contributorID"
  

python data-sources/unesco/merge-contributions-and-book-info.py \
  --csv-1 $UPDATED_CONTRIBUTIONS \
  --csv-2 $INPUT_CSV_2 \
  --merge-column-left id \
  --merge-column-right id \
  --output-csv $OUTPUT_CSV
