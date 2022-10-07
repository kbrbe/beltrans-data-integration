# Organization overlap

In contrast to person contributors who often have identifiers like ISNI or Wikidata in common, organizational contributors from different sources often have no identifiers in common.
Therefore we create a correlation list based on existing organization data we have and string matching. A human checks the created matches and the finalized correlation list can be treated as another data source.


## String matching

Currently we mainly have authority identifiers for organizations from KBR and KB.
Thus the following steps will query all names and identifiers from KBR and compares the names with all names and identifiers from KB.

First we get the input for the comparison with the following two SPARQL queries.

```bash
cd ../../data-integration
source py-integration-env/bin/activate

python query_data.py -u <SPARQL ENDPOINT URL> -q sparql-queries/get-organizations-kbr.sparql -o ../data-sources/org-overlap/kbr-organizations.csv

python query_data.py -u <SPARQL ENDPOINT URL> -q sparql-queries/get-organizations-nta.sparql -o ../data-sources/org-overlap/nta-organizations.csv

```

Please note: the organization names from NTA often contain a city in brackets, to increase the number of possible matches these should be removed.
Alternatively line 74 can be changed from `nameNormalized = utils_string.getNormalizedString(name)` to `nameNormalized = utils_string.getNormalizedString(name.split('(')[0])`.

Afterwards we use the script `match_records.py` to find the overlap.

```bash
python match_records.py --file1 kbr-organizations.csv --file2 nta-organizations.csv --match-column1 name --match-column2 name --output-column1 kbrID --output-column1 isniID --output-column2 ntaID --output-column2 isniID --file1-label KBR --file2-label NTA -o overlap.csv

```
