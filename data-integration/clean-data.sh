

cd ../data-sources/kbr
# todo: activate python env
# todo: use variables (initialize with .env)

#
# TRANSLATIONS
# XML -> XML clean -> CSV -> TURTLE (kbr-translations.ttl)
# <http://kbr-syracuse>
#

# clean dates and some other string values in the MARC SLIM XML records
python clean-marc-slim.py -i translations/2021-11-29_1970-2020_FR-NL_9280records.xml -o translations/2021-11-29_1970-2020_FR-NL_9280records-cleaned.xml
python clean-marc-slim.py -i translations/2021-11-29_1970-2020_NL-FR_3687records.xml -o translations/2021-11-29_1970-2020_NL-FR_3687records-cleaned.xml 

# Create CSV files from the XML files for easier mapping
python marc-to-csv.py -i translations/2021-11-29_1970-2020_FR-NL_9280records-cleaned.xml -w translations/2021-11-29_FR-NL_works.csv -c translations/2021-11-29_FR-NL_contributors.csv
python marc-to-csv.py -i translations/2021-11-29_1970-2020_NL-FR_3687records-cleaned.xml -w translations/2021-11-29_NL-FR_works.csv -c translations/2021-11-29_NL-FR_contributors.csv


#
# AUTHORITIES - KBR Belgians
# CSV > CSV clean -> TURTLE (kbr-belgians.ttl)
# <http://kbr-belgians>
#
python replace-headers.py -i agents/2021-11-29-ExportSyracuse_ANAT-belg_24822records.csv -o agents/2021-11-29-kbr-belgians.csv -m author-headers.csv -d ';'
python pre-process-kbr-authors.py -i agents/2021-11-29-kbr-belgians.csv -o agents/2021-11-29-kbr-belgians-cleaned.csv -d ';'


#
# AUTHORITIES - Linked
# CSV -> CSV convert -> CSV clean -> TURTLE (kbr-linked-authorities.ttl)
# <http://kbr-linked-authorities>
#

# convert Syracuse CSV headers containing special characters based on conversion table

# convert csv headers
python replace-headers.py -i agents/KBR_1970-2020_FR-NL_AUT-lies_APEP_8384records-all-fields.csv -o agents/2021-11-29_FR-NL_persons.csv -m author-headers.csv -d ';'
python replace-headers.py -i agents/KBR_1970-2020_NL-FR_AUT-lies_APEP_3769records-all-fields.csv -o agents/2021-11-29_NL-FR_persons.csv -d ';' -m author-headers.csv

python replace-headers.py -i agents/KBR_1970-2020_FR-NL_AUT-lies_AORG_702records-all-fields.csv -d ';' -o agents/2021-11-29_FR-NL_orgs.csv -m author-headers.csv 
python replace-headers.py -i agents/KBR_1970-2020_NL-FR_AUT-lies_AORG_711records-all-fields.csv -o agents/2021-11-29_NL-FR_orgs.csv -d ';' -m author-headers.csv

# clean authority data
python pre-process-kbr-authors.py -i agents/2021-11-29_FR-NL_orgs.csv -o agents/2021-11-29_FR-NL_orgs-cleaned.csv -d ';'
python pre-process-kbr-authors.py -i agents/2021-11-29_FR-NL_persons.csv -o agents/2021-11-29_FR-NL_persons-cleaned.csv -d ';'

python pre-process-kbr-authors.py -i agents/2021-11-29_NL-FR_orgs.csv -o agents/2021-11-29_NL-FR_orgs-cleaned.csv -d ';'
python pre-process-kbr-authors.py -i agents/2021-11-29_NL-FR_persons.csv -o agents/2021-11-29_NL-FR_persons-cleaned.csv -d ';'
