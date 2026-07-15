# BELTRANS data integration


This repository contains code for the data integration of the [BELTRANS](https://www.kbr.be/en/projects/beltrans/) project which studies Intra-Belgian translation flows between French and Dutch in the period 1970-2020.
Data from different heterogenous data sources is integrated to create a FAIR corpus, this includes XML files from different sources but also existing large RDF dumps.

Preprocessing scripts for the different data sources are stored in the respective data-source folder. This mainly includes Python scripts but also [RML](https://rml.io) mapping documents.
The data integration is currently controlled by a bash script in the data-integration folder.

![BELTRANS data integration overview](https://user-images.githubusercontent.com/3501171/204752537-d58fb277-9f3a-4ab8-934c-e5faee94802b.png)

## Data availability

The integrated data is available in different formats on Zenodo [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20668316.svg)](https://doi.org/10.5281/zenodo.20668316),
and the corpus will soon be available via a SAMPO-UI.

During the project we have stored the RDF data in seperate named-graphs to indicate the provenance of the data,
e.g. data from KBR in the graph `http://kbr-syracuse`. The following queries can be used to retrieve RDF representations of the data
If _+ provenance_ is indicated, this means that the previously mentioned data source graphs, including RDF of bibliographic/authority data of KBR, BnF, KB and Unesco Index Translationum are exported as well.

* All integrated data flattened (all in a single named-graph): [get-flattened-data](data-integration/sparql-queries/get-flattened-data.sparql)
* All integrated data + provenance flattened (all in a single named-graph): [get-flattened-data-with-provenance](data-integration/sparql-queries/get-flattened-data-with-provenance.sparql)
* Due to limitations of the SPARQL 1.1 standard, it is not possible to CONSTRUCT a named-graph from a named-graph in the WHERE clause (https://github.com/w3c-cg/sparql-dev/issues/31).
   * ~~All integrated data: [get-data](data-integration/sparql-queries/get-data-with-provenance.sparql)~~
   * ~~All integrated data + provenance: [get-data-with-provenance](data-integration/sparql-queries/get-data-with-provenance.sparql)~~


