# Data Integration

This directory contains scripts to integrate the different data sources using RDF.
Data from different sources are preprocessed and transformed to RDF. The RDF representation is then queried with SPARQL to create CSV files.


## Integration using our bash script

The currently custom made bash script performs Extract Transform and Load (ETL) steps involving preprocessing with Python and RDF generation with RML.

```
bash integrate-data.sh
```


## Link book translations of different sources via ISBN

```
python interlink-named-graph-data.py -u http://your-sparql-endpoint.org/sparql --create-queries manifestations-create-queries.csv --update-queries manifestations-update-queries.csv

CREATE data from Create KBR manifestations
	Processing file sparql-queries/add-manifestations-kbr.sparql
	Create KBR manifestations: 159075 changes in 111391ms
Update cycle 0/2
	Processing file sparql-queries/update-manifestations-bnf-isbn10.sparql
	Update data from BnF via ISBN10: 603 changes in 3688ms
	Processing file sparql-queries/update-manifestations-bnf-isbn13.sparql
	Update data from BnF via ISBN13: 1022 changes in 5848ms
	Processing file sparql-queries/update-manifestations-kb-isbn10.sparql
	Update data from KB via ISBN10: 9468 changes in 5113ms
	Processing file sparql-queries/update-manifestations-kb-isbn13.sparql
	Update data from KB via ISBN13: 16 changes in 2070ms
Update cycle 1/2
	Processing file sparql-queries/update-manifestations-bnf-isbn10.sparql
	Update data from BnF via ISBN10: 0 changes in 119ms
	Processing file sparql-queries/update-manifestations-bnf-isbn13.sparql
	Update data from BnF via ISBN13: 0 changes in 128ms
	Processing file sparql-queries/update-manifestations-kb-isbn10.sparql
	Update data from KB via ISBN10: 0 changes in 1866ms
	Processing file sparql-queries/update-manifestations-kb-isbn13.sparql
	Update data from KB via ISBN13: 0 changes in 1686ms
CREATE authorities from Create BnF manifestations
	Processing file sparql-queries/add-manifestations-bnf.sparql
	Create BnF manifestations: 3441 changes in 2798ms
Update cycle 0/2
	Processing file sparql-queries/update-manifestations-bnf-isbn10.sparql
	Update data from BnF via ISBN10: 0 changes in 101ms
	Processing file sparql-queries/update-manifestations-bnf-isbn13.sparql
	Update data from BnF via ISBN13: 1 changes in 215ms
	Processing file sparql-queries/update-manifestations-kb-isbn10.sparql
	Update data from KB via ISBN10: 126 changes in 2205ms
	Processing file sparql-queries/update-manifestations-kb-isbn13.sparql
	Update data from KB via ISBN13: 7 changes in 1735ms
Update cycle 1/2
	Processing file sparql-queries/update-manifestations-bnf-isbn10.sparql
	Update data from BnF via ISBN10: 0 changes in 102ms
	Processing file sparql-queries/update-manifestations-bnf-isbn13.sparql
	Update data from BnF via ISBN13: 0 changes in 110ms
	Processing file sparql-queries/update-manifestations-kb-isbn10.sparql
	Update data from KB via ISBN10: 0 changes in 1660ms
	Processing file sparql-queries/update-manifestations-kb-isbn13.sparql
	Update data from KB via ISBN13: 0 changes in 1669ms
CREATE authorities from Create KB manifestations
	Processing file sparql-queries/add-manifestations-kb.sparql
	Create KB manifestations: 124949 changes in 27885ms
Update cycle 0/2
	Processing file sparql-queries/update-manifestations-bnf-isbn10.sparql
	Update data from BnF via ISBN10: 2 changes in 170ms
	Processing file sparql-queries/update-manifestations-bnf-isbn13.sparql
	Update data from BnF via ISBN13: 0 changes in 116ms
	Processing file sparql-queries/update-manifestations-kb-isbn10.sparql
	Update data from KB via ISBN10: 1527 changes in 4435ms
	Processing file sparql-queries/update-manifestations-kb-isbn13.sparql
	Update data from KB via ISBN13: 3 changes in 2501ms
Update cycle 1/2
	Processing file sparql-queries/update-manifestations-bnf-isbn10.sparql
	Update data from BnF via ISBN10: 0 changes in 103ms
	Processing file sparql-queries/update-manifestations-bnf-isbn13.sparql
	Update data from BnF via ISBN13: 0 changes in 110ms
	Processing file sparql-queries/update-manifestations-kb-isbn10.sparql
	Update data from KB via ISBN10: 0 changes in 2577ms
	Processing file sparql-queries/update-manifestations-kb-isbn13.sparql
	Update data from KB via ISBN13: 0 changes in 2560ms
```
