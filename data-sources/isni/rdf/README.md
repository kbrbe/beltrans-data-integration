# ISNI RDF

ISNI dumps can be downloaded in RDF/XML and JSON-LD from the ISNI website: https://isni.org/page/linked-data/

* person dump in RDF/XML is 867MB compressed, and 18GB uncompressed

The RDF/XML dump can be filtered in a streaming fashion such that we only end up with relevant data.
However, there is no nationality in the person data on which we could filter.


## Stats full file
There are 756,780 entries which have an `owl:sameAs` link to Wikidata entities.
This information was obtained using the following script:

```
time python get-isni-rdf-data.py -i rdf/ISNI_persons.rdf
results
http://www.wikidata.org/entity/ 756780

real    20m20.759s
user    17m23.134s
sys     0m17.654s
```

## Filter for Belgians

```
time python filter-isni-results.py -i rdf/ISNI_persons.rdf -f 2021-11-25-isni-authorities-belgian.csv -o rdf/2021-11-28-belgians-isni.rdf
Successfully read 27066 unique ISNI identifiers from 91909 records in given CSV file
27036 records from the input matched with the 27066 of the filter

real    23m1.837s
user    19m42.333s
sys     0m17.423s
```

## Stats Belgian file

```
time python get-isni-rdf-data.py -i rdf/2021-11-28-belgians-isni.rdf 
results
http://www.wikidata.org/entity/	9172

real	0m2.937s
user	0m2.533s
sys	0m0.036s
```
