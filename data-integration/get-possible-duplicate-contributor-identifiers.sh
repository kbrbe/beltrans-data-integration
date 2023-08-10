
contributorTypes=(author translator illustrator scenarist publishingDirector)

for i in "${contributorTypes[@]}"
do
  echo "check $i"
  python identify_duplicate_contributors.py -i corpus-versions/2022-09-27/csv/integrated-data-enriched.csv -o duplicate-"$i"s.csv --column "$i"Identifiers --output-column targetIdentifier --output-column targetKBRTitle --output-column targetKBRIdentifier
done
