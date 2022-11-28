SCRIPT="detectors/identify_conflicting_dates.py"
CORPUS_DIR="../data-integration/corpus-versions/2022-11-28"

python $SCRIPT -i $CORPUS_DIR/csv/contributors-persons-all-info.csv -o data/int1-conflicting-birth-dates.csv --date-column birthDateKBR --date-column birthDateBnF --date-column birthDateNTA --date-column birthDateISNI --output-column contributorID --output-column name --output-column isniIDs --output-column viafIDs --output-column wikidataIDs

python $SCRIPT -i $CORPUS_DIR/csv/contributors-persons-all-info.csv -o data/int2-conflicting-death-dates.csv --date-column deathDateKBR --date-column deathDateBnF --date-column deathDateNTA --date-column deathDateISNI --output-column contributorID --output-column name --output-column isniIDs --output-column viafIDs --output-column wikidataIDs

python $SCRIPT -i $CORPUS_DIR/csv/integrated-data.csv -o data/int3-conflicting-publication-dates.csv --date-column targetYearOfPublicationKBR --date-column targetYearOfPublicationBnF --date-column targetYearOfPublicationKB --output-column targetIdentifier --output-column targetKBRIdentifier --output-column targetBnFIdentifier --output-column targetKBIdentifier --output-column targetKBRTitle --output-column targetBnFTitle --output-column targetKBTitle
