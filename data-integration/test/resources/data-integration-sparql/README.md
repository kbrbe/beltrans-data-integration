# Data Integration SPARQL

This test data reflects the following cases.

## Bibliographic data matching based on ISBN10

* A manifestation, which should have matches via ISBN10 with a record from KBR, BnF and KB (`KBR-BnF-KB`)
* A manifestation, which should have matches via ISBN10 with a record from KBR and BnF (`KBR-BnF-00`)
* A manifestation, which should have matches via ISBN10 with a record from KBR and KB (`KBR-000-KB`)
* A manifestation, which should have matches via ISBN10 with a record from BnF and KB (`000-BnF-KB`)
* A manifestation with ISBN10 only found at KBR (`KBR-000-00`)
* A manifestation with ISBN10 only found at BnF (`000-BnF-00`)
* A manifestation with ISBN10 only found at KB (`000-000-KB`)

## Bibliographic data matching based on ISBN13

* A manifestation, which should have matches via ISBN13 with a record from KBR, BnF and KB (`KBR-BnF-KB`)
* A manifestation, which should have matches via ISBN13 with a record from KBR and BnF (`KBR-BnF-00`)
* A manifestation, which should have matches via ISBN13 with a record from KBR and KB (`KBR-000-KB`)
* A manifestation, which should have matches via ISBN13 with a record from BnF and KB (`000-BnF-KB`)
* A manifestation with ISBN13 only found at KBR (`KBR-000-00`)
* A manifestation with ISBN13 only found at BnF (`000-BnF-00`)
* A manifestation with ISBN13 only found at KB (`000-000-KB`)

## Authority data matching based on ISNI

* A person record, which should have matches via ISNI with a record from KBR, BnF and KB (`KBR-BnF-KB`)
* A person record, which should have matches via ISNI with a record from KBR and BnF (`KBR-BnF-00`)
* A person record, which should have matches via ISNI with a record from KBR and KB (`KBR-000-KB`)
* A person record, which should have matches via ISNI with a record from BnF and KB (`000-BnF-KB`)
* A person record with ISNI only found at KBR (`KBR-000-00`)
* A person record with ISNI only found at BnF (`000-BnF-00`)
* A person record with ISNI only found at KB (`000-000-KB`)

## Authority data matching based on VIAF

* A person record, which should have matches via VIAF with a record from KBR, BnF and KB (`KBR-BnF-KB`)
* A person record, which should have matches via VIAF with a record from KBR and BnF (`KBR-BnF-00`)
* A person record, which should have matches via VIAF with a record from KBR and KB (`KBR-000-KB`)
* A person record, which should have matches via VIAF with a record from BnF and KB (`000-BnF-KB`)
* A person record with VIAF only found at KBR (`KBR-000-00`)
* A person record with VIAF only found at BnF (`000-BnF-00`)
* A person record with VIAF only found at KB (`000-000-KB`)

## Authority data matching based on Wikidata

* A person record, which should have matches via Wikidata with a record from KBR, BnF and KB (`KBR-BnF-KB`)
* A person record, which should have matches via Wikidata with a record from KBR and BnF (`KBR-BnF-00`)
* A person record, which should have matches via Wikidata with a record from KBR and KB (`KBR-000-KB`)
* A person record, which should have matches via Wikidata with a record from BnF and KB (`000-BnF-KB`)
* A person record with Wikidata only found at KBR (`KBR-000-00`)
* A person record with Wikidata only found at BnF (`000-BnF-00`)
* A person record with Wikidata only found at KB (`000-000-KB`)

## Authority data matching from a correlation list based on library identifiers 

* A person record from a correlation list, which should create a match between a BnF and a KB record
* A person record from a correlation list, which should create a match between a KBR, BnF and a KB record
  * One of the sources (`kbrAuthorBE14`) contains a wrong VIAF identifier according to the source which would integrate with `bnfAuthorBE8`
  * Only if the correlation list is properly handled and data integration via identifiers excluded for the list members, there won't be a wrong link

