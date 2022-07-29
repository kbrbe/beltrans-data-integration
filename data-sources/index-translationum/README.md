# Index Translationum

This is an online database of translations offering a search interface.
With our BELTRANS criteria the search looks as follows:

  * NL-FR: https://www.unesco.org/xtrans/bsresult.aspx?lg=0&sl=nld&l=fra&from=1970&to=2020&fr=0
  * FR-NL: https://www.unesco.org/xtrans/bsresult.aspx?lg=0&sl=fra&l=nld&from=1970&to=2020&fr=0

* The resulting HTML page mentions the number of search results and shows 10 records per page
* The resulting HTML search result pages contain the structure of the data in an HTML table and the fields in `<span>` tags with class names such as `<span class="sb_year">` for publication year or `<span class="sn_target_title">` for the title of the translation
* The field `sn_pub` with information about the publishing is further divided into `place`, `publisher` and `sn_country`
* The field `sn_isbn` contains a single string with possibly multiple ISBN, e.g. `(ISBN: 2930367105, 9077213058, 9077213074)`, in case there are several ISBNs, the whole content within the parentheses is repeated again, it will have the same `span` element class `sn_isbn` but is thus displayed twice, e.g. `(ISBN: 2930367105, 9077213058, 9077213074) (ISBN: 2930367105, 9077213058, 9077213074)`

Our data processing is as follows: we first extract the data from the search results and then we resolve 1:N relationships between translations and ISBN identifiers to get normalized data.

## Step 1: data extraction

Our extraction script gets the data page by page, controlled via the URL parameter `fr` (where 0 is the first page with 10 results, 10 the second page, 20 the third page and so on).
We create a CSV with the field names as provided in the `span` tags. For ISBN identifiers we compute both the ISBN10 and ISBN13 variant, this implicitely includes a validity check of the ISBN identifiers.

The content was extracted using the script `get-content.py`.

### NL-FR extraction

Following the web interface, there are `3,349` results, we use this information to configure our script

```
time python get-content.py -u https://www.unesco.org/xtrans/bsresult.aspx -m 3349 -r 10 -o beltrans_NL-FR_index-translationum_3349.csv -w 0 --params lg=0 sl=nld l=fra from=1970 to=2020
 82%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▋                             | 275/335 [13:21<02:56,  2.94s/it]
Invalid ISBN "2-93004-02-11-3" in record 2747/3349
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 335/335 [16:13<00:00,  2.91s/it]

real	16m13,538s
user	0m1,258s
sys	0m0,077s

```

An erroneous ISBN was reported for one book.
We googled "ISBN" and the title, i.e. *ISBN Le mythe de la bonne guerre : les Etats-Unis et la Deuxième Guerre mondiale*
and got the following ISBN13 identifiers as sarch result.
We used the ISBN converter <https://www.isbn.org/ISBN_converter> to manually compute the ISBN10 version.


| found ISBN13  | converted ISBN10 |
|---------------|------------------|
| 9782805920042 | 2-8059-2004-X |
| 9782930402116 | 2-930402-11-3 |
| 9788879812276 | 88-7981-227-0 |

The invalid ISBN `2-93004-02-11-3` very likely refers to the second one (with a missing 0).
We inserted the corrected data manually.

### FR-NL extraction

Following the web interface, there are `11,899` results, we use this information to configure our script

```
time python get-content.py -u https://www.unesco.org/xtrans/bsresult.aspx -m 11899 -r 10 -o beltrans_FR-NL_index-translationum_11899.csv -w 0 --params lg=0 sl=fra l=nld from=1970 to=2020
 65%|█████████████████████████████████████████████████████████████████████████████████████████████████████████▋                                                         | 772/1190 [45:52<24:16,  3.48s/it]
Invalid ISBN "PRG" in record 7713/11899
 72%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▎                                             | 856/1190 [50:26<19:40,  3.54s/it]
Invalid ISBN "GEO GU90-209-2597-0" in record 8552/11899
 96%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏      | 1139/1190 [1:06:13<03:16,  3.86s/it]
Invalid ISBN "PHL" in record 11389/11899
Invalid ISBN "REL" in record 11389/11899
Invalid ISBN "PHL" in record 11389/11899
Invalid ISBN "REL" in record 11389/11899
Invalid ISBN "PHL" in record 11389/11899
Invalid ISBN "REL" in record 11389/11899
Invalid ISBN "PHL" in record 11389/11899
Invalid ISBN "REL" in record 11389/11899
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1190/1190 [1:09:00<00:00,  3.48s/it]

real	69m0,586s
user	0m4,982s
sys	0m0,325s
```

The found wrong values are also visible in the web interface and likely are the result of a data quality issue at the source.


## Step 2: data normalization

A search result may contain several ISBN10 or ISBN13 identifiers which are stored as semicolon-separated list in the respective `isbn10` or `isbn13` column.

We want to normalize the data and create separate CSV files with 1:1 relationships between books and ISBN identifier.
Therefore we use the existing script `extract-and-normalize-separated-strings.py` of KBR data source directory.

Extraction of ISBN10/ISBN13 relationships for NL-FR translations:

```
python extract-and-normalize-separated-strings.py -i ../index-translationum/beltrans_NL-FR_index-translationum_3349.csv -o beltrans_NL-FR_index-translationum_isbn10.csv --input-id-column-name "id" --input-value-column-name "isbn10" --output-id-column-name "id" --output-value-column-name "isbn10"
Finished without errors

python extract-and-normalize-separated-strings.py -i ../index-translationum/beltrans_NL-FR_index-translationum_3349.csv -o beltrans_NL-FR_index-translationum_isbn13.csv --input-id-column-name "id" --input-value-column-name "isbn13" --output-id-column-name "id" --output-value-column-name "isbn13"
Finished without errors
```

Extraction of ISBN10/ISBN13 relationships for FR-NL translations:

```
python extract-and-normalize-separated-strings.py -i ../index-translationum/beltrans_FR-NL_index-translationum_11899.csv -o beltrans_FR-NL_index-translationum_isbn10.csv --input-id-column-name "id" --input-value-column-name "isbn10" --output-id-column-name "id" --output-value-column-name "isbn10"
Finished without errors

python extract-and-normalize-separated-strings.py -i ../index-translationum/beltrans_FR-NL_index-translationum_11899.csv -o beltrans_FR-NL_index-translationum_isbn13.csv --input-id-column-name "id" --input-value-column-name "isbn13" --output-id-column-name "id" --output-value-column-name "isbn13"
Finished without errors
```
