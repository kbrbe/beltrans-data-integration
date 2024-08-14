
date="2024-08-06"


# input files
translationsInput="../data-sources/correlation/$date""_translations_correlation-list.xlsx"
personsInput="../data-sources/correlation/$date""_person-contributors-correlation-list.xlsx"
orgsInput="../data-sources/correlation/$date""_org-contributors-correlation-list.xlsx"

# output files
translationsCSV="../data-sources/correlation/$date""_translations_correlation-list.csv"
removalCSV="../data-sources/correlation/$date""_translations_removal-list.csv"
personsCSV="../data-sources/correlation/$date""_person_contributors-correlation-list.csv"
orgsCSV="../data-sources/correlation/$date""_org_contributors-correlation-list.csv"

echo "Extract persons ..."
python -m tools.csv.excel_to_csv $personsCSV -i $personsInput -s "all persons"

echo "Extract orgs ..."
python -m tools.csv.excel_to_csv $orgsCSV -i $orgsInput -s "all orgs"

echo "Extract translations and removal ..."
python -m tools.csv.excel_to_csv $translationsCSV $removalCSV -i $translationsInput -s "Create minimal records" -s "remove"

