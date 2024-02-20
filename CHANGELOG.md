# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This repository contains code to create a data corpus, instead of following [Semantic Versioning](https://semver.org/spec/v2.0.0.html) we use the date of a corpus release as version number, because in fact we implicitly version the corpus.
Every version of the corpus may contain breaking changes, thus a semantic versioning with minor and patch would not be very effective.


* Years of publication are not only created in a postprocessing step, but are also added to our RDF Knowledge Graph

## [20240208] - 2024-02-08
## [20231215] - 2023-12-15

## [20231114] - 2023-11-14

## [20231009] - 2023-10-09

Added

* Using a translation correlation list in addition to our previously used person contributor correlation list (+ integration test) ([#190](https://github.com/kbrbe/beltrans-data-integration/issues/190))
* Cluster our manifestations to the work level by using a Python implementation of the OCLC Work-Set algorithm ([#193](https://github.com/kbrbe/beltrans-data-integration/issues/193)), also improved the generation of clustering input data based on experiments with our data ([#197](https://github.com/kbrbe/beltrans-data-integration/issues/197)). This script was outsourced to a different repo https://github.com/kbrbe/work-set-clustering (DOI: [10.5281/zenodo.10011416](https://zenodo.org/doi/10.5281/zenodo.10011416))
* Enrich our data via the central ISNI database via a script that we outsourced to a different repo https://github.com/kbrbe/enrich-authority-csv. Statistics of the enrichment are available in a [Jupyter notebook](https://github.com/kbrbe/beltrans-data-integration/blob/main/data-integration/Enriching.ipynb) ([#188](https://github.com/kbrbe/beltrans-data-integration/issues/188)), PR [#189](https://github.com/kbrbe/beltrans-data-integration/pull/189)
* Smaller helper scripts as part of PR [#189](https://github.com/kbrbe/beltrans-data-integration/pull/189) such as finding the difference between two CSV files ([d904bc](https://github.com/kbrbe/beltrans-data-integration/commit/d904bc26084ba8e9f3aea37f939a0be92533e151)) or using different matching algorithms to identify name matches ([a0fd9d](https://github.com/kbrbe/beltrans-data-integration/pull/189/commits/a0fd9d3a5dbbeea89c16a3aecea46bf3225befaf))
* Mapping the most common source and target languages from the correlation list ([1365bf](https://github.com/kbrbe/beltrans-data-integration/commit/1365bf9604cf07f729179bd2e6b2f1b0a346467e))

Changed

* Provide a single sourceTitle column instead source title column per data source ([#195](https://github.com/kbrbe/beltrans-data-integration/issues/195))
* Displaying years of publication correctly, i.e. prefer the value of the manually curated correlation list above found data ([#201](https://github.com/kbrbe/beltrans-data-integration/issues/201))

## [20230630] - 2023-06-30

The biggest changes in this version are the addition of pseudonym and alternate name information as well as a generic SPARQL update query for the data integration.

Added

* Pseudonyms and alternate names in RDF ([#183](https://github.com/kbrbe/beltrans-data-integration/issues/183)), PR [#186](https://github.com/kbrbe/beltrans-data-integration/pull/186)
* Deduplicate collective pseudonyms (need human curation) ([#185](https://github.com/kbrbe/beltrans-data-integration/issues/185))
* Birth and death date is taken from person correlation list ([83ddc5](https://github.com/kbrbe/beltrans-data-integration/commit/83ddc55beb75d89c07edf6fad16e53ec7f1e40b6))
* Script to fetch bibliographic KBR records via Z39.50 API ([187](https://github.com/kbrbe/beltrans-data-integration/issues/187))
* Functionality to compute the BnF control character ([#99](https://github.com/kbrbe/beltrans-data-integration/issues/99))

Changed

* Use a generic UPDATE query with `bf:identifiedBy` and FILTER to increase integration performance, see also `..SingleUpdateQuery` classes in query\_builder ([#179](https://github.com/kbrbe/beltrans-data-integration/issues/179)), PR [#182](https://github.com/kbrbe/beltrans-data-integration/pull/182)

Fixed

* SPARQL Update query to generate `dcterms:identifier` properties for BnF manifestations ([#180](https://github.com/kbrbe/beltrans-data-integration/issues/180))
* Correlation list filter SPARQL query ([1107df](https://github.com/kbrbe/beltrans-data-integration/commit/1107df32253a6a5735b0eaff33ecfe4a5aae8736))
* Missing relevant nationality query works again ([169f32](https://github.com/kbrbe/beltrans-data-integration/commit/169f32b57080ea8c369938c569b63d0cc25513d5))

## [20230203] - 2023-02-03

The biggest changes in this version was the addition of a big 4th data source (Unesco Index Translationum) in the data integration pipeline and a feature which allows to specify a correlation list of person contributors excluded from the automatic data integration based on identifiers.

### Added

The following new data or features were added (Unesco, person correlation list, KB organizations, BnF source titles, BnF Rameau classifications)

* We added Unesco Index Translationum as a 4th big data source to the data integration pipeline ([168](https://github.com/kbrbe/beltrans-data-integration/issues/168)), that also included semi-automatic matching between person authorities based on translations ([174](https://github.com/kbrbe/beltrans-data-integration/issues/174) with the `identify_duplicate_contributors.py` script described below)
* Use a manually curated person correlation list whose records are excluded from the automatic data integration via identifiers to avoid a wrong integration due to wrong identifiers in data sources ([176](https://github.com/kbrbe/beltrans-data-integration/issues/176))
* ETL organizations from KB based on provided RDF/XML dumps ([152](https://github.com/kbrbe/beltrans-data-integration/issues/152))
* Not only ETL BnF translations, but also information about originals ([129](https://github.com/kbrbe/beltrans-data-integration/issues/129), [163](https://github.com/kbrbe/beltrans-data-integration/pull/163))
* ETL Rameau classifications of BnF translations and display them in the dataprofile CSV ([171](https://github.com/kbrbe/beltrans-data-integration/pull/171))
* Publisher names in book records that have multiple matches with a KBR organization dump are ETL'ed and added to the `http://kbr-publisher-matches` named graph with a `btm:matchCandidate` property. Based on that, a list with possible candidates is easily created with SPARQL ([158](https://github.com/kbrbe/beltrans-data-integration/issues/158))


The following scripts were added to perform certain subtasks

* To support the integration of contributors without identifiers in common, we added the `identify_duplicate_contributors.py` script that identifies occurrences of translation contributors that have a similar name ([144](https://github.com/kbrbe/beltrans-data-integration/issues/144), relevant is also the fix of [146](https://github.com/kbrbe/beltrans-data-integration/issues/146) for the integration *with* identifier)
* Documentation about a script to match organizations from two different data sources, for example KBR and KB ([c40cd46](https://github.com/kbrbe/beltrans-data-integration/commit/c40cd46959cf0393df5d574c98e720ea382e9e6e)) integrated publishers will also be shown in a name-id version, e.g. "PublisherA (kbr1, kb1337)" ([153](https://github.com/kbrbe/beltrans-data-integration/issues/153))
* Added a script to normalize 1:n relationships with the initial usecase of multiline BnF unimarc CSV files ([336582](https://github.com/kbrbe/beltrans-data-integration/commit/336582c823fc9da6f4da281b031613118faaedd2))
* Added a script to find overlapping content in two CSV Files ([aabaf23](https://github.com/kbrbe/beltrans-data-integration/commit/aabaf23302ebf2553a00d51db4fefa66307a5338))
* Added a reusable `checkIfColumnExists` function to check if a CSV file contains given columns ([139406](https://github.com/kbrbe/beltrans-data-integration/commit/1394060a257330dca3910927aac185246d777c9d))
* Added an `activate.sh` bash script to quickly activate the Python environment (incl. setting Python path correctly for the `tools` module)

The following miscellaneous features were added to fix issues

* Show gender information in the person authority list that also includes gender information from BnF ([160](https://github.com/kbrbe/beltrans-data-integration/issues/160))
* SPARQL queries to identify instances of previously defined data quality metrics ([milestone 5](https://github.com/kbrbe/beltrans-data-integration/milestone/5))

### Changed

Changes in the dataprofile CSV

* Display a publisher as a combination of name and identifiers in the dataprofile CSV similar to person contributors ([2d1aa6](https://github.com/kbrbe/beltrans-data-integration/commit/2d1aa614bf882fd209976a140c956ef630d64987))
* Titles and subtitles of books are now stored separately based on the BIBFRAME ontology ([169](https://github.com/kbrbe/beltrans-data-integration/issues/169), when possible based on already splitted/structured data source data, otherwise automatically based on a title splitting) and a single Title/Subtitle is shown in the dataprofile CSV ([170](https://github.com/kbrbe/beltrans-data-integration/issues/170))
* Columns containing several delimited values are now sorted in a postprocessing step to ease working with pivot tables ([162](https://github.com/kbrbe/beltrans-data-integration/issues/162))
* Write dataprofile Excel cell values explicitly as string, e.g. to avoid cutting of leading zeros in ISNI identifiers ([467a1d](https://github.com/kbrbe/beltrans-data-integration/commit/467a1de2c3b954cbf5e9aa46df3def394edebbef))

Other noteworthy changes

* Explicitly annotate translations that fulfill the BELTRANS criteria (`schema:isPartOf btid:beltransCorpus`), helpful among others to query quality indicators for a Librarian-In-The-Loop only for a relevant subset ([156](https://github.com/kbrbe/beltrans-data-integration/issues/156))
* The script `tools.xml.get-subjects`, used to identify and extract subject URIs in RDF/XML based on filter criteria, can now be configured with the type of resource (e.g. `schema:Organization`  instead of `RDF:Description` [df1973d](https://github.com/kbrbe/beltrans-data-integration/commit/df1973d237cd7d577d0f913aec5dd58829046d93))
* Automatically generated SPARQL queries for the data integration are now saved in files to ease debugging afterwards ([164](https://github.com/kbrbe/beltrans-data-integration/issues/164))

### Fixed

* Fixed a bug in the SPARQL queries of the contributor integration and added a test to test and verify it ([146](https://github.com/kbrbe/beltrans-data-integration/issues/146))
* Improved the integration from the ISNI-SRU dumps, persons from the ISNI dump now properly link to KBR persons (added missing triple pattern in RML mapping[164](https://github.com/kbrbe/beltrans-data-integration/issues/164)) and to KB persons (added missing prefix `p` to KB identifier [166](https://github.com/kbrbe/beltrans-data-integration/issues/166))
* Fixed missing KB publisher names ([53a133](https://github.com/kbrbe/beltrans-data-integration/commit/53a133e583844e18ed3f6897cc2d5be573bc612c))

## [20220912] - 2022-09-12

In this version we mainly fixed some bugs and filled some gaps in the data.

### Added

* We started to integrate genre classifications from KB ([106](https://github.com/kbrbe/beltrans-data-integration/issues/106))
* We started to use an Export of Belgians from the KBR catalogue to fill missing KBR identifier gaps in the contributor list of the corpus Excel file

### Changed

* All information about originals is now stored in dedicated named graphs (even if it is minimal information extracted from the translation records) (this prevents incorrect data due to inconsistently updated data and required that we restructure RML mapping rules [134](https://github.com/kbrbe/beltrans-data-integration/issues/134)) 
* Our data integration relies on several SPARQL queries per data source, instead of having hard-coded queries we generate the queries now based on a configuration file ([130](https://github.com/kbrbe/beltrans-data-integration/issues/130))

### Fixed

* Retrieving more ISNI identifiers from KBR exports because we properly handle newline characters ([46730da](https://github.com/kbrbe/beltrans-data-integration/commit/46730dacf0ba66e5d1ae1d060e742c8d41724dc6))
* Fixed integration from Wikidata list based on ISNI: due to wrong configuration ISNI was not taken into account ([d987018](https://github.com/kbrbe/beltrans-data-integration/commit/d98701848869da94fcc7b028e442ac8dabdced23))

## [20220811] - 2022-08-11

Besides our main data sources, we also started to use correlation lists of contributor identifiers as data source and started to visualize contributor statistics across corpus versions.
We started to systematically identify the KBR identifier of originals.
Furthermore, we used federated Wikidata queries and more extraction from BnF dumps to fill gaps related to ISNI identifiers and nationality information.

### Added

* We also visualize corpus statistics with respect to contributors ([126](https://github.com/kbrbe/beltrans-data-integration/issues/126))
* We added a list of contributors with identifiers from Wikidata as a new data source, it also contains manually curated links to KBR contributors. Thus we also had to adapt the RDF generation and integration SPARQL queries to represent library identifiers using the Bibframe ontology, like we already did for ISNI/VIAF/Wikidata identifiers ([805dfd](https://github.com/kbrbe/beltrans-data-integration/commit/805dfd10d85a09568b51f9caf5132bc429aac21b))
* We added federated Wikidata queries to fill ISNI and nationality gaps as well as a subsequent script to lookup missing (authority) data in BnF dumps ([83](https://github.com/kbrbe/beltrans-data-integration/issues/83))
* Based on a different KBR export and source title information in translations, we started to systematically identify KBR identifiers of originals ([129](https://github.com/kbrbe/beltrans-data-integration/issues/129))

### Changed

* So far only translations from authors with Belgian nationality were considered for the corpus, now we also consider translations from organizational authors with associated country Belgium ([127](https://github.com/kbrbe/beltrans-data-integration/issues/127))
* With some changes in our infrastructure we also started to use Python script to send SPARQL queries instead of using bash scripts and curl
* We refactored the large integration `utils.py` file into several more thematic utils files ([117](https://github.com/kbrbe/beltrans-data-integration/issues/117#issuecomment-1185624839))


## [20220624] - 2022-06-24

Starting from this version we have a processing step to add geoname identifiers, we provide more source titles, provide translation-related statistics in the contributor list and in general provide statistics to visualize changes in the corpus.
Furthermore we simplified the corpus Excel sheet by merging several columns from different data sources and provide several bug fixes.

We tried clustering based on manifestation editions: reprints have different local identifiers ([119](https://github.com/kbrbe/beltrans-data-integration/issues/119)), but this lead to unwanted side-effects resulting in data loss which why we do not perform this clustering anymore ([b9f8821](https://github.com/kbrbe/beltrans-data-integration/commit/b9f8821518e1b307406315dca993d07350fbcc88))

### Added

- We started to visualize the statistics representing the changes in the corpus between versions ([120](https://github.com/kbrbe/beltrans-data-integration/issues/120))
- We started to collect statistics about the overlap between different combinations of KBR, BnF and KB identifiers ([125](https://github.com/kbrbe/beltrans-data-integration/issues/125))
- Besides the enrichment of country names (see fixed) we also provide an enrichment with geonames identifier ([112](https://github.com/kbrbe/beltrans-data-integration/issues/112), [104](https://github.com/kbrbe/beltrans-data-integration/issues/105))
- We identified more original titles: for KBR we also check the value of the MARC field `246$a` to extract the original title of a translation ([111](https://github.com/kbrbe/beltrans-data-integration/issues/111))
- Source titles from KB data are now also available in the corpus ([118](https://github.com/kbrbe/beltrans-data-integration/issues/118))
- The contributor list in the corpus Excel sheet now shows some basic statistics about how many works someone authored, illustrated, ... ([115](https://github.com/kbrbe/beltrans-data-integration/issues/115))


### Changed

- Instead of having a single *year of publication* and *placeOfPublication* column for each source, we perform a postprocessing to merge the columns of the respective sources (and indicate inconsistencies) ([107](https://github.com/kbrbe/beltrans-data-integration/issues/105), [110](https://github.com/kbrbe/beltrans-data-integration/issues/109))
- The corpus Excel file contains now "tables" instead of only showing CSV, which already includes the possibility to filter ([113](https://github.com/kbrbe/beltrans-data-integration/issues/113))
- The corpus Excel file contains now seperate sheets for person and organization contributors ([109](https://github.com/kbrbe/beltrans-data-integration/issues/109))

### Fixed

- For BnF and KB no publisher name information existed because of a mistake in a SPARQL query (BnF) and a missing RML mapping for KB. This was fixed with the commits [603d517](https://github.com/kbrbe/beltrans-data-integration/commit/603d51786c897e9d01355267014c15a652510815), [cd0c6e6](https://github.com/kbrbe/beltrans-data-integration/commit/cd0c6e61f72aa95b809a7d7e02d6436f284e75ad) and was added to the dataprofile query 
- Information about publishing directors are now not only extracted but also used (see [this](https://github.com/kbrbe/beltrans-data-integration/commit/3cf508454209dd68ebc915bbec95c4a3c7970612) commit)
- The enrichment of country names based on locations was improved, unit tests were added ([104](https://github.com/kbrbe/beltrans-data-integration/issues/104))
- KBR identifiers are treated as string identifiers instead of float numbers ([108](https://github.com/kbrbe/beltrans-data-integration/issues/108))
- Column values starting with `=` are no longer interpreted as formula in the corpus Excel sheet ([113](https://github.com/kbrbe/beltrans-data-integration/issues/113))
- Uncleaned ISBN10 and ISBN13 from KBR were mapped, but this was fixed ([121](https://github.com/kbrbe/beltrans-data-integration/issues/121), [123](https://github.com/kbrbe/beltrans-data-integration/issues/123))
- We improved the contributors postprocessing runtime from several minutes to less than a second ([122](https://github.com/kbrbe/beltrans-data-integration/issues/122))
- Fetching more KBR ISNI identifiers by looking also for `ISNI` instead of only `isni` (see [this](https://github.com/kbrbe/beltrans-data-integration/commit/fdac9d52b885a5f74a8a1ebd648f2496a6169330) commit)

## [20220425] - 2022-04-25

This version includes also data from KB as well as fixes and improvements based on received corpus feedback.
It corresponds to the milestone https://github.com/kbrbe/beltrans-data-integration/milestone/4.

### Added

- Besides KBR and BnF, we now also use data extracted from The Royal Library of the Netherlands (KB) via SPARQL and their public SPARQL endpoint ([#84](https://github.com/kbrbe/beltrans-data-integration/issues/84), [#2](https://github.com/kbrbe/beltrans-data-integration/issues/2), [#84](https://github.com/kbrbe/beltrans-data-integration/issues/84), [#102](https://github.com/kbrbe/beltrans-data-integration/issues/102))
- We adapted the way of integrating data, instead of a very complex SPARQL query per data source and Python postprocessing to merge the results, we implemented a workflow in which we create URIs for own manifestations and own contributors in separated named graphs. These graphs we populate with `schema:sameAs` links in several update-cycles such that we have integrated records which we then query with a single SPARQL query ([89](https://github.com/kbrbe/beltrans-data-integration/issues/89))
- Besides author, illustrator and scenarist, we now take also the role *publishing director* into account for the Belgian nationality filter ([#93](https://github.com/kbrbe/beltrans-data-integration/issues/93))
- The contributor lists now shows integrated information, e.g. an author and related identifiers from different data sources ([#79](https://github.com/kbrbe/beltrans-data-integration/issues/79))
- We represent ISNI identifiers for BnF data now using the BIBFRAME vocabulary (`bf:identifiedBy -> bf:Isni`) as we already do for the other data sources ([#68](https://github.com/kbrbe/beltrans-data-integration/issues/68))
- For BnF data we use the `dcterms:identifier` property to link to the identifier as found in the data.bnf.fr link ([#92](https://github.com/kbrbe/beltrans-data-integration/issues/92) which may differ from the identifier represented in the RDF from BnF [#99](https://github.com/kbrbe/beltrans-data-integration/issues/99))
- We added integration tests to verify that our dataprofile SPARQL query and postprocessing fetches all data correctly, therefore we added test data and Python tests ([#85](https://github.com/kbrbe/beltrans-data-integration/issues/85), [#97](https://github.com/kbrbe/beltrans-data-integration/issues/97))
- Contribution relationships within KBR data are now additionally expressed using direct properties (as for BnF data), for example `ex:myBook marcrel:ill ex:illustrator1`. Before we only had these relationships expressed using W3C PROV qualified Associations which was more difficult to query ([#86](https://github.com/kbrbe/beltrans-data-integration/issues/86))
- The country of publication was missing for several translations, a script from [Fabrizio Pascucci](https://be.linkedin.com/in/fabrizio-pascucci-bb950616a) was added to derive the country from the mentioned place of publication ([#101](https://github.com/kbrbe/beltrans-data-integration/issues/101))

### Changed

- We show the string normalized name of publishers ([#81](https://github.com/kbrbe/beltrans-data-integration/issues/81))
- Instead of having two scripts to extract a semicolon-separated list of BelgianBibliography entries and country of publications, we added a generalized script (see [this commit](https://github.com/kbrbe/beltrans-data-integration/commit/f02499271062f8d998fb60886cc117f39ac641b4))
- We explicitly add the source language for BnF records (before this only happened implicitly via the dataprofile SPARQL query) ([#100](https://github.com/kbrbe/beltrans-data-integration/issues/100))
- The column names of the dataprofile CSV were simplified, e.g. `targetCountryOfPublication` instead of `targetTextCountryOfPublication` ([#78](https://github.com/kbrbe/beltrans-data-integration/issues/78))

### Fixed

- We normalize ISBN10/ISBN13 identifiers from BnF to increase matches with other sources (use of hyphens) ([#95](https://github.com/kbrbe/beltrans-data-integration/issues/95), [#103](https://github.com/kbrbe/beltrans-data-integration/issues/103))
- The KBR catalogue may indicate more than one role per publisher, only the first was mapped to RDF, now all are mapped ([#87](https://github.com/kbrbe/beltrans-data-integration/issues/87))
- The KBR catalogue may indicate more than one place of publication, only the first was mapped to RDF, now all are mapped ([#88](https://github.com/kbrbe/beltrans-data-integration/issues/88))
- The KBR catalogue may indicate more than one ISBN10/ISBN13 identifier, for example for co-editions, but only the first was mapped to RDF, now all are mapped ([#73](https://github.com/kbrbe/beltrans-data-integration/issues/73))
- The global lookup check to replace self-created publisher IDs with found IDs was improved and can be controlled by a CSV file  (see [this commit](https://github.com/kbrbe/beltrans-data-integration/commit/f7916602f1597e77f56179ba26ba135d2bf118da))
- We fixed an issue in the linking to self-created publisher URIs ([#82](https://github.com/kbrbe/beltrans-data-integration/issues/82))
- VIAF and Wikidata identifiers of BnF authorities were missing in our RDF, it is added now (see [this commit](https://github.com/kbrbe/beltrans-data-integration/commit/678c4c3f06b4f7bcbed9f0849d4a3ebac1ba250e))
- We did not correctly indicate VIAF identifiers extracted from the ISNI SRU API, we changed the extraction method to fix it ([#98](https://github.com/kbrbe/beltrans-data-integration/issues/98))

## [20220217] - 2022-02-17

This version includes also data from BnF as well as fixes and improvements based on received corpus feedback.
It corresponds to the milestone https://github.com/kbrbe/beltrans-data-integration/milestone/3.

### Added

- We added translations from BnF to our corpus, thus there is a new column *targetTextBnFIdentifier*. Via ISBN identifiers links between KBR and BnF manifestations were established. ([#30](https://github.com/kbrbe/beltrans-data-integration/issues/30), [#63](https://github.com/kbrbe/beltrans-data-integration/issues/63))
- Based on available links from the KBR catalog, we added information about the original of a translation ([#29](https://github.com/kbrbe/beltrans-data-integration/issues/29))
- We added new columns to the CSV corpus file with the name and ID of the collection, in case a translation is part of a collection [#45](https://github.com/kbrbe/beltrans-data-integration/issues/45)
- Previous corpus versioned missed the field of the language of the original, this is now added ([#60](https://github.com/kbrbe/beltrans-data-integration/issues/60))

### Changed

- ISBN numbers are now represented in normalized form (all with hyphen) which also helped in establishing links between KBR and BnF records ([#17](https://github.com/kbrbe/beltrans-data-integration/issues/17), [#67](https://github.com/kbrbe/beltrans-data-integration/issues/67))
- The corpus now contains two Excel files which are automatically generated, one for data one for statistics. Initially we only created CSV files which had to be imported to Excel manually by also selecting the used characterset. ([#56](https://github.com/kbrbe/beltrans-data-integration/issues/56))
- In the Excel sheet containing one translation per row we refer now to the name and ID of a contributor instead of only the ID to increase readability. For example `Sven Lieber (1234); John Doe (567)` ([#74](https://github.com/kbrbe/beltrans-data-integration/issues/74))
- Statistics of the corpus describe now both KBR and BnF records ([#72](https://github.com/kbrbe/beltrans-data-integration/issues/72))
- Contributors listed in a separate Excel sheet now contain besides KBR also BnF records ([#76](https://github.com/kbrbe/beltrans-data-integration/issues/76))
- Internally we use now a MARCXML export of KBR for authorities instead of CSV, therefore we have access to more structured data ([#48](https://github.com/kbrbe/beltrans-data-integration/issues/48))

### Fixed

- We also use author information from the MARC field `100` of a manifestation. Initially we only extracted contributors from `700` fields, therefore several relationships between authors and manifestations were missing ([#71](https://github.com/kbrbe/beltrans-data-integration/issues/71), [#57](https://github.com/kbrbe/beltrans-data-integration/issues/57), [#58](https://github.com/kbrbe/beltrans-data-integration/issues/58))
- The list of contributors is now complete, a wrong SPARQL query resulted in the issue that only contributors where shown which were also translators ([#70](https://github.com/kbrbe/beltrans-data-integration/issues/70))
- We use now less self-created publisher IDs and refer to existing publisher records as much as possible. Publishers in KBR records are represented both in text fields and as linked authorities, when there was no linked authority in the record we created our own identifier. However a global check afterwards was needed to check if the publisher name is found in all KBR authority records ([#62](https://github.com/kbrbe/beltrans-data-integration/issues/62))

## [20211213] - 2021-12-23

This version contains fixes and improvements based on received corpus feedback.
It corresponds to the milestone https://github.com/SvenLieber/beltrans-data/milestone/2.

### Added

- Add the Belgian Bibliiography classification to translations, this includes a multilingual RDF representation of the Belgian Bibliography as a SKOS taxonomy ([#33](https://github.com/SvenLieber/beltrans-data/issues/33), [#50](https://github.com/SvenLieber/beltrans-data/issues/50))
- If a publication is in fact a multilingual work instead of a "regular" translation, we now indicate this explicitly ([#31](https://github.com/SvenLieber/beltrans-data/issues/31), [#49](https://github.com/SvenLieber/beltrans-data/issues/49))
- Missing publication-related information about binding types and editions were added to our RDF representation using schema.org ([#36](https://github.com/SvenLieber/beltrans-data/issues/36), [#38](https://github.com/SvenLieber/beltrans-data/issues/38), [#50](https://github.com/SvenLieber/beltrans-data/issues/50))
- The creation of the corpus is now automized using a bash script ([#46](https://github.com/SvenLieber/beltrans-data/issues/46))
- In addition to a large CSV containing columns for publication-related but also contributor-related data, we also provide a CSV in normalized form. Several authors, publishers etc of a publication are aggregated in their respective columns and one line corresponds to a single publication ([#53](https://github.com/SvenLieber/beltrans-data/issues/53))
- For each KBR translation in our corpus, we create a RDF resource for the source publication to which we append the source language ([#55](https://github.com/SvenLieber/beltrans-data/issues/55))
- Some basic statistics about the corpus such as number of Dutch/French translations per publisher or per country are automatically provided via a SPARQL query for each new version of the corpus ([#52](https://github.com/SvenLieber/beltrans-data/issues/52))

### Changed

- We assumed a publisher role for organizations linked in MARC field 710 to a publication even if the 'publisher role' was not explicitly specified. We indicate uncertainty in RDF in case there was no role specified ([#37](https://github.com/SvenLieber/beltrans-data/issues/37), [#50](https://github.com/SvenLieber/beltrans-data/issues/50))
- Part of a KBR publication URI was the word `work`, however, this is confusing in a library setting, thus it was renamed to `manifestation` ([#43](https://github.com/SvenLieber/beltrans-data/issues/43))
- Different columns in the CSV version of the corpus simply contained URIs, the RDF contains now human-readable labels and the labels are shown instead the URI ([#40](https://github.com/SvenLieber/beltrans-data/issues/40))
- Instead of having separate columns for birth/death dates from different sources in the CSV version of the corpus, we now post-process the query result and provide the most complete birth/death date, i.e. either from ISNI or from KBR. This also helps us in identifying wrong dates ([#41](https://github.com/SvenLieber/beltrans-data/issues/41))
- Instead of showing the KBR URI of a publication in the CSV version of the corpus, we simply show the numerical identifier ([#54](https://github.com/SvenLieber/beltrans-data/issues/54))

### Fixed

- Instead of an authority linked to a publication, a publisher might be indicated only textual and thus was missing in our corpus. Also textual publisher information was taken into account when linking publications to publishers in RDF ([#34](https://github.com/SvenLieber/beltrans-data/issues/34), [#35](https://github.com/SvenLieber/beltrans-data/issues/35))
- In case several "countries of publication" exist in the KBR source data, we also create links for *all* of them and not just the first ([#51](https://github.com/SvenLieber/beltrans-data/issues/51))

## [20211129] - 2021-11-29

This is a first version of the corpus created by the code of this repository.
The main data source are exports of the library management system from KBR. Additionally, data from ISNI are used (a XML dump containing among others gender information and a Linked Data dump containing dates and Wikidata links).
This version corresponds to the milestone https://github.com/SvenLieber/beltrans-data/milestone/1.

### Added

- Create Linked Data from KBR data
  - RML mappings to create RDF for translations exported from KBRs library management system ([#12](https://github.com/SvenLieber/beltrans-data/issues/12))
  - RML mappings to create RDF linking translations and their contributors with various roles ([#18](https://github.com/SvenLieber/beltrans-data/issues/18))
  - Get updated data from KBR authorities ([#16](https://github.com/SvenLieber/beltrans-data/issues/16))
  - Add data of publisher location ([#26](https://github.com/SvenLieber/beltrans-data/issues/26))
- Create Linked Data from ISNI
  - CSV preprocessing and RML mappings to get relevant data from ISNI XML dump ([#14](https://github.com/SvenLieber/beltrans-data/issues/14))
  - Filter the massive amount of ISNI Linked Data (18GB) to obtain birth and death dates of authorities as well as Wikidata links ([#13](https://github.com/SvenLieber/beltrans-data/issues/13), [#25](https://github.com/SvenLieber/beltrans-data/issues/25))
  - Import ISNI RDF data to our triple store ([#15](https://github.com/SvenLieber/beltrans-data/issues/15))
- Create the corpus by querying all integrated data sources
  - Make data queryable via SPARQL endpoint ([#23](https://github.com/SvenLieber/beltrans-data/issues/23))
  - A SPARQL query to obtain the data ([#22](https://github.com/SvenLieber/beltrans-data/issues/22))

[20211129]: https://github.com/kbrbe/beltrans-data-integration/releases/tag/2021-11-29
[20211223]: https://github.com/kbrbe/beltrans-data-integration/compare/2021-11-29...2021-12-23
[20220217]: https://github.com/kbrbe/beltrans-data-integration/compare/2021-12-23...2022-02-17
[20220425]: https://github.com/kbrbe/beltrans-data-integration/compare/2022-02-17...2022-04-25
[20220624]: https://github.com/kbrbe/beltrans-data-integration/compare/2022-04-25...2022-06-24
[20220811]: https://github.com/kbrbe/beltrans-data-integration/compare/2022-06-24...2022-08-11
[20220912]: https://github.com/kbrbe/beltrans-data-integration/compare/2022-08-11...2022-09-12
[20230203]: https://github.com/kbrbe/beltrans-data-integration/compare/2022-09-12...2023-02-03
[20230630]: https://github.com/kbrbe/beltrans-data-integration/compare/2023-02-03...2023-06-30
