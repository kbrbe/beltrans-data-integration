# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This repository contains code to create a data corpus, instead of following [Semantic Versioning](https://semver.org/spec/v2.0.0.html) we use the date of a corpus release as version number, because in fact we implicitly version the corpus.
Every version of the corpus may contain breaking changes, thus a semantic versioning with minor and patch would not be very effective.

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

[20211129]: https://github.com/SvenLieber/beltrans-data/releases/tag/2021-11-29
[20211223]: https://github.com/SvenLieber/beltrans-data/compare/2021-11-29...2021-12-23
[20220217]: https://github.com/SvenLieber/beltrans-data/compare/2021-12-23...2022-02-17

