
# We use the result of a name matching between BELTRANS records that only have a unesco identifier
# and BELTRANS records that have other identifiers but no unesco identifiers yet
# The following command uses those matches to add the unesco identifier to the other BELTRANS record that already contains other identifiers
python -m tools.csv.update_column \
  --csv-1 data-sources/correlation/2023-06-28_person-contributors-correlation-list-processed.csv \
  --csv-2 data-integration/2023-08-07_matching-scores/clear-matches-token_sort_ratio-90.csv \
  --column-to-be-updated unescoIDs \
  --column-with-new-values contributorUnescoID \
  --id-column-1 contributorID \
  --id-column-2 candidatesID \
  --output-csv data-sources/correlation/2023-08-07_person-contributors-correlation-list-with-duplicates.csv \
  --info-column '2023-08-07_unesco-enrichment' \
  --log-column-2 'contributorBELTRANSID' \
  --mode 'append'

# The input of the previous command contains all BELTRANS person records.
# We added the unesco identifier from one BELTRANS record to another,
# but actually we should also delete the BELTRANS record that only contained the unesco identifier.
# After all, there is now another more enriched record with many third-part identifiers now including also unesco
# The previous command added the BELTRANS record identifier of the now obsolete authority
# in the column 'contributorBELTRANSID' (by using the "log-column-2" argument)
# We will delete rows with those identifiers

python -m tools.csv.delete_rows \
  --csv-1 data-sources/correlation/2023-08-07_person-contributors-correlation-list-with-duplicates.csv \
  --csv-2 data-sources/correlation/2023-08-07_person-contributors-correlation-list-with-duplicates.csv \
  --id-column-1 contributorID \
  --id-column-2 log-contributorBELTRANSID \
  --output-csv data-sources/correlation/2023-08-07_person-contributors-correlation-list.csv


