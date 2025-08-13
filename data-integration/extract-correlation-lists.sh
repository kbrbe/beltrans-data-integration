
date="2025-07-17"


# input files
translationsInput="/data/beltrans/data-sources/correlation/$date""_translations_correlation-list.xlsx"
personsInput="/data/beltrans/data-sources/correlation/$date""_person-contributors-correlation-list.xlsx"
orgsInput="/data/beltrans/data-sources/correlation/$date""_org-contributors-correlation-list.xlsx"

# output files
translationsCSV="/data/beltrans/data-sources/correlation/$date""_translations_correlation-list.csv"
removalCSV="/data/beltrans/data-sources/correlation/$date""_translations_removal-list.csv"
personsCSV="/data/beltrans/data-sources/correlation/$date""_person_contributors-correlation-list.csv"
orgsCSV="/data/beltrans/data-sources/correlation/$date""_org_contributors-correlation-list.csv"

echo "Extract persons ..."
python -m tools.csv.excel_to_csv $personsCSV -i $personsInput -s "all persons"

echo "Extract orgs ..."
python -m tools.csv.excel_to_csv $orgsCSV -i $orgsInput -s "all orgs"

echo "Extract translations and removal ..."
python -m tools.csv.excel_to_csv $translationsCSV $removalCSV -i $translationsInput -s "Create minimal records" -s "remove"

