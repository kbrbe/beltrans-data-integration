# Test resources

Synthetic data used by our integration tests to provide a test environment.
 
## beltrans-graph-data-three-sources

Data to populate named-graphs for the following sources (bib + aut)

* KBR data 
* BnF data
* KB data 
* integrated data
* sameAs links between integrated data and the other sources 

## country-enrichment

Data to test the country enrichment script.
Containing minimal dumps of geonames for BE, NL and FR for lookup as well as a CSV file with different combinations of place/country assignments for translations which should be enriched.

## duplicate-integrated-manifestations

Data to popuate named-graphs for the following sources (bib + auth)

* KB data
* integrated data

A script to remove duplicates after integrating is tested.

## geoname-identifier-enrichment

Data to test enrichment with geoname identifiers.
Containing minimal dumps of geonames for BE, NL and FR for lookup as well as a CSV file with different combinations of place/country assignments for translations which should be enriched.

## data-integration-sparql

Data to test the integration of data from different named graphs via identifiers into a new integrated named graph.

* Bibliographic data from KBR, BnF and KB via ISBN into the named graph `<http://beltrans-manifestations>`
* Authority data from KBR, BnF and KB via ISNI/VIAF/Wikidata/KBR/BnF/KB identifier into the named graph `<http://beltrans-contributors>`

## source-graph-data-two-sources

Data to test ?


