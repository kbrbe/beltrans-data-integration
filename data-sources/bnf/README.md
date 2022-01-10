# BnF

The National Library of France (BnF) provides information via a SPARQL endpoint or RDF dumps.

* **source**:
* **URL**: https://data.bnf.fr/

The import of all author information (`58,390,749 triples` from both skos and foaf dump)
from an `7.5 GB` n-triples dump
* took *54 minutes* on a local Blazegraph instance in a VM on a laptop with SSD and less than 4 GB of RAM
* took *3.3 hours* on a Blazegraph instance on a server given 2 GB of RAM

## Belgian authors

We assume the property `http://rdfvoab.info/ElementsGr2/countryAssociatedWithThePerson` refers to the nationality of a person.

# Edition data dump


Data about expressions and manifestations is scattered throughout `62611` XML files (`39 GB`), in the following a simple text search for the ID of one manifestation.

```xml
#
# a few lines of one of the input files (it is not one coherent manifestation record but just a few definition triples)
#
 <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb39862770t#about">
    <rdf:type rdf:resource="http://rdvocab.info/uri/schema/FRBRentitiesRDA/Manifestation"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb398622399#about">
    <rdf:type rdf:resource="http://rdvocab.info/uri/schema/FRBRentitiesRDA/Manifestation"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb39863098h#about">
    <rdf:type rdf:resource="http://rdvocab.info/uri/schema/FRBRentitiesRDA/Manifestation"/>
  </rdf:Description>
```

We want to do a quick text search in all files for a specific ID, but there are too many files so we get an error.

```bash
#
# grep will give an error message because there are too many input files
#
grep -rnw "12148/cb398622399" *.xml
-bash: /usr/bin/grep: Argument list too long
```

The following command can be used instead.

The following shows in which files information about the searched manifestation are stored (or links to the manifestation).
This makes a "quick filtering" on different attributes while streaming impossible, because if we read a manifestation ID we do not now if it fulfills our filter criteria (e.g. the publication year might be the very last line in the last file, thus for every ID we have to remember it and thus our memory would get full quickly).

```bash
#
# this find command lets grep search in one file at a time
#
find . -type f -exec grep -rnw "12148/cb398622399" {} +

./databnf_editions__manif_036066.xml:2993:  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb398622399#about">
./databnf_editions__manif_036067.xml:12919:  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb398622399#about">
./databnf_editions__manif_036067.xml:12924:    <rdam:P30139 rdf:resource="http://data.bnf.fr/ark:/12148/cb398622399#Expression"/>
./databnf_editions__manif_036067.xml:12936:    <rdarelationships:expressionManifested rdf:resource="http://data.bnf.fr/ark:/12148/cb398622399#Expression"/>
./databnf_editions__manif_036067.xml:12937:    <rdfs:seeAlso rdf:resource="https://catalogue.bnf.fr/ark:/12148/cb398622399"/>
./databnf_editions__expr_036068.xml:1196:  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb398622399#Expression">
./databnf_editions__expr_036069.xml:1631:  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb398622399#Expression">
./databnf_editions__expr_036069.xml:1633:    <owl:sameAs rdf:resource="http://data.bnf.fr/ark:/12148/cb398622399#frbr:Expression"/>
./databnf_editions__expr_036070.xml:769:  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb398622399">
./databnf_editions__expr_036070.xml:771:    <foaf:focus rdf:resource="http://data.bnf.fr/ark:/12148/cb398622399#about"/>
```
