# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 18:01:31 2022

@author: FabrizioPascucci
"""

from optparse import OptionParser
import pandas as pd
import re
import glob
import unicodedata as ud
import utils

def main():
    """This script fills out missing countries based on the place name (for Belgium, France & The Netherlands)"""
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('-i', '--input-file', action='store', help='The input file as TSV')
    parser.add_option('-c', '--column-with-country-names', action='store', help='The name of the column that contains the countries')
    parser.add_option('-p', '--column-with-places', action='store', help='The name of the column that contains the place names')
    parser.add_option('-g', '--geonames-folder', action='store', help='The filepath to the the geonames (insert the "/" at the end) folder. In this folder the geonames files for the three countries must be named "BE.txt", "FR.txt" and "NL.txt"')
    parser.add_option('-o', '--output-file', action='store', help='The output as TSV')
    (options, args) = parser.parse_args()

    if( ( not options.geonames_folder) or (not options.input_file) or (not options.column_with_country_names) or (not options.column_with_places) or (not options.geonames_folder) or (not options.output_file) ):
      parser.print_help()
      exit(1) 

    beContent = pd.read_csv(options.geonames_folder + "BE.txt", delimiter='\t', header=None)
    be = utils.extract_geonames(beContent)
    frContent = pd.read_csv(options.geonames_folder + "FR.txt", delimiter='\t', header=None)
    fr = utils.extract_geonames(frContent)
    nlContent = pd.read_csv(options.geonames_folder + "NL.txt", delimiter='\t', header=None)
    nl = utils.extract_geonames(nlContent)

#    df = pd.read_csv(options.input_file, delimiter='\t', encoding= 'ISO-8859-1')
    df = pd.read_csv(options.input_file, delimiter=',', encoding= 'utf-8')
    df['country1'] = df[options.column_with_places].str.extract('\((.*?)\)', expand=True)
    df = df.fillna('')

    df.loc[df[options.column_with_country_names] == '', options.column_with_country_names] = df['country1']

    df = df.drop('country1', 1)

    places = utils.extract_places_tsv(df, options.column_with_places, options.column_with_country_names)

    countries_new = []
    for place in places:
        country = place[1]
        if country == '':
            if " ; " in place[0]:
                cities = place[0].split(" ; ")
                countries = []
                for city in cities:
                    if city.strip() in be:
                        countries.append("Belgium")
                    elif city.strip() in fr:
                         countries.append("France")
                    elif city.strip() in nl:
                        countries.append("Netherlands")
                    else:
                        countries.append("")
                new_country = ' ; '.join(countries)
                countries_new.append(new_country)
            else:
                city = place[0]
                if city.strip() in be:
                    countries_new.append("Belgium")
                elif city.strip() in fr:
                    countries_new.append("France")
                elif city.strip() in nl:
                    countries_new.append("Netherlands")
                else:
                    countries_new.append("")
        else:
            new_country = country
            countries_new.append(new_country)

    places_clean = []
    for x in places:
        places_clean.append(x[0])

    df[str(options.column_with_country_names)] = countries_new
    #df.drop(options.column_with_places, 1)
    #df[str(options.column_with_places)] = places_clean
    #df.to_csv(options.output_file, sep="\t", index=False, encoding = "ISO-8859-1")
    df.to_csv(options.output_file, sep=",", index=False, encoding = "utf-8")

main()

