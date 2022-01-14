# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This repository contains code to create a data corpus, instead of following [Semantic Versioning](https://semver.org/spec/v2.0.0.html) we use the date of a corpus release as version number, because in fact we implicitly version the corpus.
Every version of the corpus may contain breaking changes, thus a semantic versioning with minor and patch would not be very effective.

## [2021-12-13] - 2021-12-23

This version contains fixes and improvements based on received corpus feedback.
It corresponds to the milestone https://github.com/SvenLieber/beltrans-data/milestone/2.

### Added

- Add the Belgian Bibliiography classification to translations, this includes a multilingual RDF representation of the Belgian Bibliography as a SKOS taxonomy (#33, #50)
- If a publication is in fact a multilingual work instead of a "regular" translation, we now indicate this explicitly (#31, #49)
- Missing publication-related information about binding types and editions were added to our RDF representation using schema.org (#36, #38, #50)
- The creation of the corpus is now automized using a bash script (#46)
- In addition to a large CSV containing columns for publication-related but also contributor-related data, we also provide a CSV in normalized form. Several authors, publishers etc of a publication are aggregated in their respective columns and one line corresponds to a single publication (#53)
- For each KBR translation in our corpus, we create a RDF resource for the source publication to which we append the source language (#55)
- Some basic statistics about the corpus such as number of Dutch/French translations per publisher or per country are automatically provided via a SPARQL query for each new version of the corpus (#52)

### Changed

- We assumed a publisher role for organizations linked in MARC field 710 to a publication even if the 'publisher role' was not explicitly specified. We indicate uncertainty in RDF in case there was no role specified (#37, #50)
- Part of a KBR publication URI was the word `work`, however, this is confusing in a library setting, thus it was renamed to `manifestation` (#43)
- Different columns in the CSV version of the corpus simply contained URIs, the RDF contains now human-readable labels and the labels are shown instead the URI (#40)
- Instead of having separate columns for birth/death dates from different sources in the CSV version of the corpus, we now post-process the query result and provide the most complete birth/death date, i.e. either from ISNI or from KBR. This also helps us in identifying wrong dates (#41)
- Instead of showing the KBR URI of a publication in the CSV version of the corpus, we simply show the numerical identifier (#54)

### Fixed

- Instead of an authority linked to a publication, a publisher might be indicated only textual and thus was missing in our corpus. Also textual publisher information was taken into account when linking publications to publishers in RDF (#34, #35)
- In case several "countries of publication" exist in the KBR source data, we also create links for *all* of them and not just the first (#51)

## [2021-11-29] - 2021-11-29

This is a first version of the corpus created by the code of this repository.
The main data source are exports of the library management system from KBR. Additionally, data from ISNI are used (a XML dump containing among others gender information and a Linked Data dump containing dates and Wikidata links).
This version corresponds to the milestone https://github.com/SvenLieber/beltrans-data/milestone/1.

### Added

- Create Linked Data from KBR data
  - RML mappings to create RDF for translations exported from KBRs library management system (#12)
  - RML mappings to create RDF linking translations and their contributors with various roles (#18)
  - Get updated data from KBR authorities (#16)
  - Add data of publisher location (#26)
- Create Linked Data from ISNI
  - CSV preprocessing and RML mappings to get relevant data from ISNI XML dump (#14)
  - Filter the massive amount of ISNI Linked Data (18GB) to obtain birth and death dates of authorities as well as Wikidata links (#13, #25)
  - Import ISNI RDF data to our triple store (#15)
- Create the corpus by querying all integrated data sources
  - Make data queryable via SPARQL endpoint (#23)
  - A SPARQL query to obtain the data (#22)

[2021-11-29]: https://github.com/SvenLieber/beltrans-data/releases/tag/2021-11-29
[2021-12-23]: https://github.com/SvenLieber/beltrans-data/compare/2021-11-29...2021-12-23

