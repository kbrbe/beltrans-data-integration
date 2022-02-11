# Data Integration

This directory contains scripts to integrate the different data sources using RDF.
Data from different sources are preprocessed and transformed to RDF. The RDF representation is then queried with SPARQL to create CSV files.


## Integration using our bash script

The currently custom made bash script performs Extract Transform and Load (ETL) steps involving preprocessing with Python and RDF generation with RML.

```
bash integrate-data.sh
```
