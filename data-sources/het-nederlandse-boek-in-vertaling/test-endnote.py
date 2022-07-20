from litter_getter import ris

importer = ris.RisImporter('2013_digitaal/NL-boek-in-vertaling_2013_FR.txt')
refs = importer.references

refs[0].keys()


