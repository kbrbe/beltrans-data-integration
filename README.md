# BELTRANS data integration


This repository contains code for the data integration of the [BELTRANS](https://www.kbr.be/en/projects/beltrans/) project which studies Intra-Belgian translation flows between French and Dutch in the period 1970-2020.
Data from different heterogenous data sources is integrated to create a FAIR corpus, this includes XML files from different sources but also existing large RDF dumps.

Preprocessing scripts for the different data sources are stored in the respective data-source folder. This mainly includes Python scripts but also [RML](https://rml.io) mapping documents.
The data integration is currently controlled by a bash script in the data-integration folder.

![BELTRANS data integration overview](https://user-images.githubusercontent.com/3501171/153832514-e763ace1-de0f-4f96-b872-36c0864beae8.png)
