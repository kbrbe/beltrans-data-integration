# Master data

This directory contains smaller datasets such as thesauri or other reference data the different data sources may link to.
Concretely we have

## MARC relator codes

* A mapping from MARC relator codes to their human readable name in English (`marc-roles.csv`)

## Belgian Bibliography

* The belgian bibliography in different languages
  * English names: `thesaurus-belgian-bibliography-en.csv`
  * French names: `thesaurus-belgian-bibliography-fr.csv`
  * Dutch names: `thesaurus-belgian-bibliography-nl.csv`

The thesauri files were created by applying character encoding on received files:

```bash
# both with UTF-8 and ISO-8859 only a few but never all characters were decoded successfully
# based on a preview via LibreOffice the files seemed to have WINDOWS-1252 character encoding
iconv -f WINDOWS-1252 -t UTF-8 ~/Downloads/THESAURUS1-2021-12-02T20_09_00_EN.csv > thesaurus-belgian-bibliography-en.csv 
iconv -f WINDOWS-1252 -t UTF-8 ~/Downloads/THESAURUS1-2021-12-02T20_07_49_FR.csv > thesaurus-belgian-bibliography-fr.csv 
iconv -f WINDOWS-1252 -t UTF-8 ~/Downloads/THESAURUS1-2021-12-02T20_08_39_NL.csv > thesaurus-belgian-bibliography-nl.csv 
```

For easier processing during Knowledge Graph generation we converted these files to a more machine-friendly format.

```bash
python convert-thesaurus.py -i thesaurus-belgian-bibliography-en.csv -o thesaurus-belgian-bibliography-en-hierarchy.csv
python convert-thesaurus.py -i thesaurus-belgian-bibliography-nl.csv -o thesaurus-belgian-bibliography-nl-hierarchy.csv
python convert-thesaurus.py -i thesaurus-belgian-bibliography-fr.csv -o thesaurus-belgian-bibliography-fr-hierarchy.csv
``
