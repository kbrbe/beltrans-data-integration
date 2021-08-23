# Data sources

This directory provides information about the different data sources.
For each data source we provide an overview, detailled information are listed in the README of the respective data source directory.

## KBR (Belgium)
The Royal Library of Belgium.

* **source**: Library Management System (LMS) Syracuse
* **URL**: https://catalog.kbr.be/


## BnF (France)
The national library of France.

* **source**:
* **URL**: https://data.bnf.fr/

The import of all author information (`58,390,749 triples` from both skos and foaf dump)
from an `7.5 GB` n-triples dump
* took *54 minutes* on a local Blazegraph instance in a VM on a laptop with SSD and less than 4 GB of RAM
* took *3.3 hours* on a Blazegraph instance on a server given 2 GB of RAM


## KB (Netherlands)
The Royal Library of the Netherlands.

* **source**:
* **URL**:

There are several dumps which cover different datasets, an overview of all dumps is available here: https://data.bibliotheken.nl/files/

The import of all author information (`48,702,577 triples`)
from the `3.4 GB` XML dump of NTA took *3.8 hours* on a Blazegraph instance on a server given 2GB of RAM.

## Wikidata - Belgians

This data source is the result of a Wikidata query and a manual enrichment with identifiers from KBR.
