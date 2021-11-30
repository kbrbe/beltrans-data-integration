
bash delete-named-graph.sh integration http://wikibase-test-srv01.kbr.be/sparql http://isni-sru
bash upload-data.sh integration ../data-sources/isni/authorities-sru.ttl "application/x-turtle" http://wikibase-test-srv01.kbr.be/sparql http://isni-sru

bash upload-data.sh integration ../data-sources/isni/rdf/2021-11-28-belgians-isni.rdf "application/rdf+xml" http://wikibase-test-srv01.kbr.be/sparql http://isni-rdf

bash delete-named-graph.sh integration http://wikibase-test-srv01.kbr.be/sparql http://kbr-syracuse
bash upload-data.sh integration ../data-sources/kbr/kbr-translations.ttl "application/x-turtle" http://wikibase-test-srv01.kbr.be/sparql http://kbr-syracuse

bash delete-named-graph.sh integration http://wikibase-test-srv01.kbr.be/sparql http://kbr-belgians
bash upload-data.sh integration ../data-sources/kbr/kbr-belgians.ttl "application/x-turtle" http://wikibase-test-srv01.kbr.be/sparql http://kbr-belgians

bash delete-named-graph.sh integration http://wikibase-test-srv01.kbr.be/sparql http://kbr-linked-authorities
bash upload-data.sh integration ../data-sources/kbr/kbr-linked-authorities.ttl "application/x-turtle" http://wikibase-test-srv01.kbr.be/sparql http://kbr-linked-authorities
