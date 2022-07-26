# BnF

The National Library of France (BnF) provides information via a catalog, a SPARQL endpoint or RDF dumps.

* **source**: data dumps or catalog
* **URL**: https://data.bnf.fr/


## Integration process
We follow a 5-step process to integrate BELTRANS-relevant translations from BnF:

1. Obtain BnF IDs of persons with Belgian nationality (used to filter later)
2. Obtain BnF publication IDs of publications between 1970 and 2020 (used to filter later)\*
3. Obtain BnF publication IDs of publications with Belgian author, illustrator or scenarist
4. Obtain BnF publication IDs of French/Dutch, Dutch/French tanslations from an advanced search in the BnF catalog (used to filter later)
5. Obtain BELTRANS-relevant BnF publication data by filtering the BnF editions dump with IDs obtained in step 1-4

\*this filter can also be applied as part of the advanced catalog search of step 4

### 1. BnF IDs of Belgians

We assume the property `http://rdfvoab.info/ElementsGr2/countryAssociatedWithThePerson` refers to the nationality of a person.
Then we use the script `get-subjects.py` to filter the RDF/XML dump of person authors (`person-authors` folder containing the BnF contributions dump `5.1GB`)

* input: BnF person-authors dump `5.1GB`
* output: BnF Belgian person IDs `belgian-contributors.csv` `1.1MB`

```bash

# configuration to filter for Belgian nationality (filter-config-beltrans-contributor-nationality.csv)
"rdagroup2elements:countryAssociatedWithThePerson","=","http://id.loc.gov/vocabulary/countries/be"

# execution of the script with the config CSV (containing only one line see above)
time python get-subjects.py -i person-authors -o belgian-contributors.csv -f filter-config-beltrans-contributor-nationality.csv
202 XML files with 5425148 records read. 23075 records (23075 unique) matched filter criteria.

real    5m27.330s
user    4m34.378s
sys     0m3.564s
```

### 2. BnF IDs of publications 1970-2020

Please note that this step is not necessary if a date filter is already applied for translations in the BnF catalog (see step 5)

* input: BnF editions dump `39GB`
* output: BnF publication IDs published between 1970 and 2020 `pubs-1970-2020.csv` `275MB`

```bash
time python get-subjects.py -i editions -o pubs-1970-2020.csv -f filter-config-beltrans-time.csv
62610 XML files with 64321802 records read. 5863941 records (5863941 unique) matched filter criteria.

real    80m42.126s
user    40m25.168s
sys     0m35.828s
```

### 3. BnF IDs of publications with Belgian contributors

The directory `contributions` contains the BnF contributions dump, uncompressed size `6.2GB`.

* input
  * BnF contributions dump `6.2GB`
  * BnF Belgians `belgian-contributors.csv` (from step 1)
* output: BnF publication IDs of publications with Belgian author, illustrator or scenarist `belgian-contributors-pubs.csv` `5.3MB`

```bash
time python get-subjects.py -i contributions -o belgian-contributors-pubs.csv -p marcrel:aut -p marcrel:ill -p marcrel:sce -l belgian-contributors.csv
44 XML files with 12320353 records read. 102227 records (94945 unique) matched filter criteria.

real    9m5.043s
user    8m23.466s
sys     0m5.276s
```

### 4. BnF IDs of translations FR-NL and NL-FR

The advanced search of the BnF catalog is used to look for translations between Dutch and French and French and Dutch: https://catalogue.bnf.fr/recherche-avancee.do?pageRech=rav
The following search filters were applied (using an `AND` condition):

* *Par nature de document*, *type de document*: Texte imprimé et livre numérique 
* *Par langue*, *Langue du document*: français
* *Par langue*, *Langue de l'oeuvre originale*: néerlandais
* *Par date de publication*: de 1970 a 2020

This resulted in `3762` translations from Dutch to French. When switching the language of the document with language of the original we obtained `584` translations from French to Dutch.
These results were exported as CSV, afterwards the column with the URI was extracted for further processing.

### 5. BELTRANS-relevant translations

In this final step relevant BnF publication records are extracted from the editions dump by applying a filter using the publication IDs of the previous steps.
We are not only interested in the IDs of the publication but also data related to them.
Therefore, we have to extract other related information from the publication IDs in other dumps such as the "external links" dump or the "contributions" dump.

#### 5.1 NL-FR translations from editions

* input
  * BnF editions dump `39GB`
  * BnF publication IDs of Dutch to French translations from 1970 onwards `0.4MB`
  * BnF publication IDs of publications with Belgian authors, illustrators or scenarists `5.1MB`
output: RDF/XML data of BELTRANS-relevant publications, `bnf-translations-1970-belgian-nl-fr.xml` `4.6MB`

```bash
time python filter-subjects-xml.py -i editions -o bnf-translations-1970-belgian-nl-fr.xml -f belgian-contributors-pubs.csv -f bnf_nl-fr_translations.csv
Successfully read 94899 identifiers from 102227 records in given CSV file belgian-contributors-pubs.csv
Successfully read 3763 identifiers from 3763 records in given CSV file bnf_nl-fr_translations.csv
The intersection between the filters are 1177 unique identifiers
Start processing 62611 files
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 62611/62611 [1:07:08<00:00, 15.54it/s]
62610 XML files with 64321802 records read. 5885 records (1177 unique) matched filter criteria.


real    66m2.864s
user    29m45.683s
sys     0m30.882s
```

#### 5.2 FR-NL translations from editions

* input
  * BnF editions dump `39GB`
  * BnF publication IDs of French to Dutch translations from 1970 onwards `0.05MB`
  * BnF publication IDs of publications with Belgian authors, illustrators or scenarists `5.1MB`
output: RDF/XML data of BELTRANS-relevant publications, `bnf-translations-1970-belgian-nl-fr.xml` `0.3MB`

```bash

time python filter-subjects-xml.py -i editions -o bnf-translations-1970-belgian-fr-nl.xml -f belgian-contributors-pubs.csv -f BnF_FR-NL_vanaf1970_689notices_export-public-fullids.csv
Successfully read 94899 identifiers from 102227 records in given CSV file belgian-contributors-pubs.csv
Successfully read 689 identifiers from 948 records in given CSV file BnF_FR-NL_vanaf1970_689notices_export-public-fullids.csv
The intersection between the filters are 93 unique identifiers
Start processing 62611 files
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 62611/62611 [1:05:12<00:00, 16.00it/s]
62610 XML files with 64321802 records read. 465 records (93 unique) matched filter criteria.

real    65m13.167s
user    29m26.532s
sys     0m32.044s


```

#### 5.3 Related information 

todo: complete this paragraph based on what we already do in `integrate-data.sh`

## ISBN information

ISBN numbers are always represented using the `bnf-onto:isbn` property and either `bibo:isbn10` or `bibo:isbn13`. Thus, based on `bnf-onto:isbn` it is not clear what type of ISBN it is and one should use the more detailed `bibo:isbn10` or `bibo:isbn13` values.

## Publisher information

The BnF edition dumps denote relationships to publishers via an explicit `marcrel:pbl` property to a resource representing the publisher, but also as text.
The BnF edition dumps use the following elements to store information regarding the publishing as text

* `rdagroup1elements:publishersName` for the name of the publisher
* `rdam:P30088` (has place of publication) for the place of publication
* `dcterms:date` for the publising year

These information seem to be used to build the value of `dcterms:publisher` based on the following pattern: `publishing place : publisher name , publishing year`.

Sometimes not all values will be available which may result in `dcterms:publisher` values such as `[S.l.] : [s.n.] , 1971`

At least for the Belgian works of our corpus the publisher information is mainly given in text only.

## Information about edition data dump


Data about expressions and manifestations is scattered throughout `62611` XML files (`39 GB`), in the following a simple text search for the ID of one manifestation.

```xml
#
# a few lines of one of the input files (it is not one coherent manifestation record but just a few definition triples)
#
 <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb39862770t#about">
    <rdf:type rdf:resource="http://rdvocab.info/uri/schema/FRBRentitiesRDA/Manifestation"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb398622399#about">
    <rdf:type rdf:resource="http://rdvocab.info/uri/schema/FRBRentitiesRDA/Manifestation"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb39863098h#about">
    <rdf:type rdf:resource="http://rdvocab.info/uri/schema/FRBRentitiesRDA/Manifestation"/>
  </rdf:Description>
```

We want to do a quick text search in all files for a specific ID, but there are too many files so we get an error.

```bash
#
# grep will give an error message because there are too many input files
#
grep -rnw "12148/cb398622399" *.xml
-bash: /usr/bin/grep: Argument list too long
```

The following command can be used instead.

The following shows in which files information about the searched manifestation are stored (or links to the manifestation).
This makes a "quick filtering" on different attributes while streaming impossible, because if we read a manifestation ID we do not now if it fulfills our filter criteria (e.g. the publication year might be the very last line in the last file, thus for every ID we have to remember it and thus our memory would get full quickly).

```bash
#
# this find command lets grep search in one file at a time
#
find . -type f -exec grep -rnw "12148/cb398622399" {} +

./databnf_editions__manif_036066.xml:2993:  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb398622399#about">
./databnf_editions__manif_036067.xml:12919:  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb398622399#about">
./databnf_editions__manif_036067.xml:12924:    <rdam:P30139 rdf:resource="http://data.bnf.fr/ark:/12148/cb398622399#Expression"/>
./databnf_editions__manif_036067.xml:12936:    <rdarelationships:expressionManifested rdf:resource="http://data.bnf.fr/ark:/12148/cb398622399#Expression"/>
./databnf_editions__manif_036067.xml:12937:    <rdfs:seeAlso rdf:resource="https://catalogue.bnf.fr/ark:/12148/cb398622399"/>
./databnf_editions__expr_036068.xml:1196:  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb398622399#Expression">
./databnf_editions__expr_036069.xml:1631:  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb398622399#Expression">
./databnf_editions__expr_036069.xml:1633:    <owl:sameAs rdf:resource="http://data.bnf.fr/ark:/12148/cb398622399#frbr:Expression"/>
./databnf_editions__expr_036070.xml:769:  <rdf:Description rdf:about="http://data.bnf.fr/ark:/12148/cb398622399">
./databnf_editions__expr_036070.xml:771:    <foaf:focus rdf:resource="http://data.bnf.fr/ark:/12148/cb398622399#about"/>
```


## Alternative BnF data import

The import of all author information (`58,390,749 triples` from both skos and foaf dump)
from an `7.5 GB` n-triples dump
* took *54 minutes* on a local Blazegraph instance in a VM on a laptop with SSD and less than 4 GB of RAM
* took *3.3 hours* on a Blazegraph instance on a server given 2 GB of RAM


## Nationality enrichment via ISNI and BnF

From our SPARQL endpoint we queried all ISNI identifiers from person authorities with missing nationality information.
This resulted in 9,065 identifiers which were stored in the file `missing-nationality-isnis.csv`.

By using the following script and the previously generated list of ISNIs, we extracted the matching BnF identifiers from the `external` dump of BnF in 17 seconds.
This resulted in 5,593 found BnF identifiers.

```
time python get-subjects.py -i external-isni -o bnf-person-ids-with-isni.csv -f filter-config-persons-with-given-isni.csv

1 XML files with 1626891 records read. 5593 records (5593 unique) matched filter criteria.

real	0m17.474s
user	0m17.352s
sys	0m0.120s

```

In order to check which ones have a nationality information, we extracted the properties and values from the found BnF identifiers in 3 minutes.

```
time python filter-subjects-xml.py -i person-authors/ -o missing-nationality-information.xml -f bnf-person-ids-with-isni.csv

Successfully read 5593 identifiers from 5593 records in given CSV file bnf-person-ids-with-isni.csv
The intersection between the filters are 5593 unique identifiers
Opening output file missing-nationality-information.xml
Start processing 202 files
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 202/202 [02:58<00:00,  1.13it/s]
202 XML files with 5425148 records read. 11186 records (5593 unique) matched filter criteria.

real	2m58.212s
user	2m54.728s
sys	0m2.125s

```

To finally obtain a list of the found nationalities, we performed a SPARQL query which took 18 seconds (including parsing/loading the RDF/XML file generated in the last step).
This resulted in 5,34 found nationalities (one of them Belgian).

```
time python queryFiles.py -q ../../data-integration/sparql-queries/get-bnf-nationalities.sparql -o missing-isni-nationalities-from-bnf.csv missing-nationality-information.xml 

trying to parse missing-nationality-information.xml ...
Parsed input files!
Execute SPARQL query get-nationalities.sparql ...
successfully executed SPARQL query!

real	0m18.621s
user	0m18.489s
sys	0m0.132s

```
