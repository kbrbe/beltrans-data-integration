# KBR

* The Royal Library of Belgium (KBR)
* **source**: Library Management System (LMS) Syracuse
* **URL**: https://catalog.kbr.be/


* Syracuse export of 8435 translations from French to Dutch: `ExportSyracuse_Document_20211019_FR-NL.xml`

## Extracting contributors from MARC XML data

Within a MARC XML record of a translation the person contributors are in MARC field 700 and organizational contributors (such as publishers) in field 710.
In both cases the KBR ID of the contributor is in field "\*" and the name in field "a"

The script `get-contributors.py` can be used to extract the contributors whereas for each specified role a new CSV is generated following a provided name pattern.
For example, I want the contributors authors (MARC code `aut`), translators (MARC code `trl`), publishers (MARC code `pbl`) and illustrators (MARC code `ill`).

The following command will create the four files

* `2021-10-27-dut-aut.csv`
* `2021-10-27-dut-trl.csv`
* `2021-10-27-dut-pbl.csv`
* `2021-10-27-dut-ill.csv`

```bash
python get-contributors.py --input cleaned.xml --pattern 2021-10-27-dut --role pbl --role trl --role ill --role aut
```

if we are only interested in role statistics the following command can be used

```bash
python get-contributors.py --input cleaned.xml --stats
```
