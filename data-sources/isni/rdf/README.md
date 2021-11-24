# ISNI RDF

ISNI dumps can be downloaded in RDF/XML and JSON-LD from the ISNI website: https://isni.org/page/linked-data/

* person dump in RDF/XML is 867MB compressed, and 18GB uncompressed

The RDF/XML dump can be filtered in a streaming fashion such that we only end up with relevant data.
However, there is no nationality in the person data on which we could filter.

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
