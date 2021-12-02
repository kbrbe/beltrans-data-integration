# Data Integration

This directory contains scripts to integrate the different data sources using RDF. We currently integrate the following data sources:

* Translations export from the library management system of KBR
  * `2021-11-29_NL-FR_works.csv`
  * `2021-11-29_FR-NL_works.csv`
* Authorities (contributors) export from the library management system of KBR
  * `2021-11-29_NL-FR_contributors.csv`
  * `2021-11-29_FR-NL_contributors.csv`
* ISNI records from OCLC's SRU API
  * `2021-11-25-isni-authorities-belgian.csv`
* ISNI RDF/XML dump from OCLC
  * `2021-11-28-belgians-isni.rdf`

We describe how we provide an interface to query the RDF generated from those sources with SPARQL.

## Cleaning data



## Generating RDF

Different scripts and mapping files exist to create RDF from these different data sources (see `data-sources` directory).
With rml.io, each non-RDF source can be mapped to RDF files in any valid RDF serialization *or* be sent to a SPARQL endpoint when also specifying a "logical-target".

## Providing access

In order to use the data we have to provide access to the RDF data. We do this by setting up a SPARQL endpoint.
In this section we describe three alternative ways to do this.

## Alternative 1: Import data to an existing SPARQL endpoint

In this solution, we import RDF sources directly to an endpoint and use the SPARQL endpoint as "logical target" for the rml.io mapping of non-RDF data.

## Alternative 2: Setting up a SPARQL endpoint on files

In this solution, we generate RDF files for all non-RDF sources and then provide a SPARQL endpoint over all available RDF files.
We use Comunica to set up a SPARQL endpoint over our data using [this guide](https://comunica.dev/docs/query/getting_started/setup_endpoint/#3--sparql-endpoint-over-multiple-sources)

Install comunica if needed using `npm install @comunica/actor-init-sparql-file` and then create the SPARQL endpoint using:

```
comunica-sparql-file \
  2021-11-29_NL-FR_works.ttl \
  2021-11-29_FR-NL_contributors.ttl \
  2021-11-29_NL-FR_works.ttl \
  2021-11-29_FR-NL_contributors.ttl \
```


## Alternative 3: SPARQL endpoint over HDT file

This solution is similar to the previous one, but instead of creating a SPARQL endpoint over several files, all files are first merged into a single compressed and indexed HDT file.
This aims to make the access quicker.
