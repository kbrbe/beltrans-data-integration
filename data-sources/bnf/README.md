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
