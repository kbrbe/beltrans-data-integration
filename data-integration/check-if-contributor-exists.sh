correlationListDate="2025-02-10"
contributorFile="extracted-contributors_$correlationListDate"".csv" \
diffFile="missing-contributors_$correlationListDate"".csv"
personFile="../data-sources/correlation/2025-02-10_person_contributors-correlation-list.csv"
orgFile="../data-sources/correlation/2025-02-10_org_contributors-correlation-list.csv"
allLookupFile="beltrans-persons-and-orgs_$correlationListDate"".csv"

python -m tools.csv.extract_contributor_identifier_from_column \
  -i "../data-sources/correlation/$correlationListDate""_translations_correlation-list.csv" \
  -o "$contributorFile" \
  --id-column "targetIdentifier" \
  -c "authorIdentifiers" \
  -c "translatorIdentifiers" \
  -c "illustratorIdentifiers" \
  -c "scenaristIdentifiers" \
  -c "publishingDirectorIdentifiers" \
  -c "targetPublisherIdentifiers" \
  -c "sourcePublisherIdentifiers" \
  --output-column-name "contributorID"

# lookup in combination of all-persons and all-orgs
python -m tools.csv.stack_csv_files \
  -c "contributorID" \
  -o "$allLookupFile" \
  "$personFile" "$orgFile"

python -m tools.csv.difference \
  --minus-last \
  -c "contributorID" \
  -o "$diffFile" \
  --output-column "missingContributorID" \
  "$contributorFile" "$allLookupFile"


