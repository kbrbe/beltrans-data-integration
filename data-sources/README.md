# Data sources

This directory provides information about the different data sources.

## KBR (Belgium)
The Royal Library of Belgium.

* **source**: Library Management System (LMS) Syracuse
* **URL**: https://catalog.kbr.be/


## BnF (France)
The national library of France.

* **source**:
* **URL**: https://data.bnf.fr/

The import of all author information (`58,390,749 triples` from both skos and foaf dump)
from an `7.5 GB` dump
into a Blazegraph instance running on a local VM with less than 4 GB RAM took *54 minutes*.

## KB (Netherlands)
The Royal Library of the Netherlands.

* **source**:
* **URL**:

There are several dumps which cover different datasets, an overview of all dumps is available here: https://data.bibliotheken.nl/files/

### Personen uit de Nederlandse Thesaurus van Auteursnamen (NTA)

**This dump provides limited information, however, also a link to OAI-PMH where more information is available**.
The most recent version of this dump is `3.4 GB` (gzipped `226 MB`) and contains RDF triples in RDF/XML.
The dump contains descriptions of authors as `schema:Person` with IRIs such as `http://data.bibliotheken.nl/id/thes/p157733416`.
When browsing to one of these IRIs, one is forwarded to the metadata entity of the resource, in this example `http://data.bibliotheken.nl/doc/thes/p157733416`.

* The name is not separated into given and family name in RDF
* There is no information about nationality
* There is a link to an OAI-PMH XML record containing MARC (in which the name is separted in given and family name)
* Sometimes there are ISNI numbers at the person using `schema:sameAs`
* Sometimes there is no information about ISNI numbers
* ISNI numbers in the OAI-PMH record are either in tag `003B` (code `a` is the number and code `2` says `isni`) or in tag `024`, ind `1` (code `a` is the number and code `2` says `isni`)
* The OAI-PMH record contains a `skos:Concept` for an author which may link to a VIAF record via `skos:exactMatch`

### DBNLA

The most recent version of this dump is `101 MB` (gzipped `14 MB`) and contains RDF triples in turtle.

The dump is concatened from different dumps, e.g. initially not all namespaces are defined, some namespaces are defined in other places of the file.
Besides usual namespaces such as `schema` or `rdfs` the following namespaces are used:

* `@prefix ns1:  <http://data.bibliotheken.nl/id/dbnla/> .`
* `@prefix ns2:  <http://data.bibliotheken.nl/id/dbnla/> .`
* `@prefix ns5:  <http://data.bibliotheken.nl/doc/dbnla/> .`
* `@prefix ns7:  <http://data.bibliotheken.nl/id/dataset/> .`

The dump contains instances of `schema:Person`, `schema:WebPage` and `schema:Dataset` with the following relationships

* `rdfs:label` (based on some string pattern like `familyName`,`givenName`(`birth year`-`death year`) whereas birth year and death year might be empty or be written as `18de eeuw`)
* `schema:name`
* `schema:alternateName`
* `schema:givenName`
* `schema:gender` (with objects either `schema:Male` or `schema:Female`)
* `schema:birthPlace`
* `schema:deathPlace`
* `schema:birthDate`
* `schema:deathDate`
* `schema:hasOccupation` (with objects being literals in Dutch but not language tagged)
* `schema:identifier`
* `schema:mainEntityOfPage` (`ns2` resources linking to blank nodes)
* `schema:mainEntity` (blank nodes linking to `ns2` resources)
* `owl:sameAs` (blank nodes linking to `ns5` resources)
* `schema:dateModified`
* `schema:isPartOf` (blank nodes linking to `ns7`resources)
* `schema:license`
* `schema:url` (`ns1` resources to web urls of dbnl.org, e.g. https://www.dbnl.org/auteurs/auteur.php?id=mohk001)

### NBT

The most recent version of this dump is `2.3 GB` (gzipped `247 MB`) and contains RDF triples in turtle.

According to [this](https://data.bibliotheken.nl/files/hulptekst_data.bibliotheken.nl.pdf) explanation provided by KB,
when using a SPARQL `group by` and `count` on authors in the NBT dataset the result concerns manifestations according to LRM.
