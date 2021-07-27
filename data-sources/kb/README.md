# KB

The Royal Library of the Netherlands provides information via a SPARQL endpoint or RDF dumps.
There are several datasets which we briefly discuss in this section.

* **NTA**: Personen uit de Nederlandse Thesaurus van Auteursnamen
* **DBNLA**: Thesaurus Auteurs Digitale bibliotheek voor de Nederlandse letteren

### Personen uit de Nederlandse Thesaurus van Auteursnamen (NTA)

**This dump provides limited information, however, also a link to OAI-PMH where more information is available**.
The most recent version of this dump is `3.4 GB` (gzipped `226 MB`) and contains RDF triples in `RDF/XML`.
The dump contains descriptions of authors as `schema:Person` with IRIs such as `http://data.bibliotheken.nl/id/thes/p157733416`.
When browsing to one of these IRIs, one is forwarded to the metadata entity of the resource, in this example `http://data.bibliotheken.nl/doc/thes/p157733416`.

* There is a link to an OAI-PMH XML record containing MARC (in which the name is separted in given and family name)
* Sometimes there are ISNI numbers at the person using `schema:sameAs`
* Sometimes there is no information about ISNI numbers
* ISNI numbers in the OAI-PMH record are either in tag `003B` (code `a` is the number and code `2` says `isni`) or in tag `024`, ind `1` (code `a` is the number and code `2` says `isni`)
* The OAI-PMH record contains a `skos:Concept` for an author which may link to a VIAF record via `skos:exactMatch`
* Different values for `schema:birthDate` or `schema:deathDate`
  * The value might just be of type `xsd:gYear`
  * It might just be a string saying `ca. 1850`
* `schema:alternateName` might be used for the name in other languages, e.g. with Greek letters
* `schema:familyName` and `schema:givenName` are usually empty
  * However, they can get queried from a linked VIAF record via an XML API (appending `/rdf.xml` to the viaf URI)
  * But there might be several family or given names, e.g. for http://viaf.org/viaf/287159080/rdf.xml there are the family names `Halsa`, `Halasā`, `Halsā`, `Hulsā`

**Examples**

* Dijkstra
  * LOD View http://data.bibliotheken.nl/doc/thes/p157733416#lodCloud
  * OAI-PMH http://services.kb.nl/mdo/oai?verb=GetRecord&identifier=GGC-THES:AC:157733416&metadataPrefix=mdoall
* Egge
  * OAI-PMH http://services.kb.nl/mdo/oai?verb=GetRecord&identifier=GGC-THES:AC:072567813&metadataPrefix=mdoall

### DBNLA

* The most recent version of this dump is `101 MB` (gzipped `14 MB`) and contains RDF triples in turtle.
* The import via `url  -H "Content-Type: text/turtle" --upload-file data/kb/authors/dbnla/dbnla_20210208.ttl  -X POST http://localhost:8090/bigdata/namespace/kb-authors-dbnla/sparql` resulted in `<?xml version="1.0"?><data modified="2148204" milliseconds="83737"/>`

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

**Import errors**

```
blazegraph_1    | ERROR: LexiconConfiguration.java:738: "1431-02-29" is not a valid representation of an XML Gregorian Calendar value.: value=1431-02-29
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 26 for Month field.: value=1585-26-25
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 31 for Month field.: value=1794-31-30
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 21 for Month field.: value=1621-21-13
blazegraph_1    | ERROR: LexiconConfiguration.java:738: "1517-02-29" is not a valid representation of an XML Gregorian Calendar value.: value=1517-02-29
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 40 for Day field.: value=1935-06-40
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 24 for Month field.: value=1672-24-23
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 15 for Month field.: value=1761-15-14
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 29 for Month field.: value=1670-29-22
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 31 for Month field.: value=1778-31-30
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 32 for Day field.: value=1557-07-32
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 32 for Day field.: value=1981-04-32
blazegraph_1    | ERROR: LexiconConfiguration.java:738: "1722-02-29" is not a valid representation of an XML Gregorian Calendar value.: value=1722-02-29
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 18 for Month field.: value=1815-18-15
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 13 for Month field.: value=1628-13-08
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 29 for Month field.: value=1717-29-28
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 19 for Month field.: value=1780-19-10
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 27 for Month field.: value=1970-27-26
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 29 for Month field.: value=1681-29-22
blazegraph_1    | ERROR: LexiconConfiguration.java:738: "1799-02-29" is not a valid representation of an XML Gregorian Calendar value.: value=1799-02-29
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 31 for Month field.: value=1680-31-30
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 22 for Month field.: value=1734-22-21
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 20 for Month field.: value=1723-20-10
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 20 for Month field.: value=1798-20-19
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 31 for Month field.: value=1735-31-30
blazegraph_1    | ERROR: LexiconConfiguration.java:738: Invalid value 19 for Month field.: value=1992-19-18

```

### NBT

The most recent version of this dump is `2.3 GB` (gzipped `247 MB`) and contains RDF triples in turtle.

According to [this](https://data.bibliotheken.nl/files/hulptekst_data.bibliotheken.nl.pdf) explanation provided by KB,
when using a SPARQL `group by` and `count` on authors in the NBT dataset the result concerns manifestations according to LRM.

* The import via `url  -H "Content-Type: application/xml" --upload-file data/kb/authors/nta/ntaa_20210314.rdf  -X POST http://localhost:8090/bigdata/namespace/kb-authors-nta/sparql` resulted in `<?xml version="1.0"?><data modified="48702577" milliseconds="6383652"/>


## Belgian authors

We assume the property `http://rdfvoab.info/ElementsGr2/countryAssociatedWithThePerson` refers to the nationality of a person.

