"""
@author: Fabrizio Pascucci
"""

import pandas as pd
import re
from optparse import OptionParser
import unicodedata as ud

def getNormalizedString(s):
    noComma = s.replace(',', '')
    noQuestionMark = noComma.replace('?', '')
    noExclamationMark = noQuestionMark.replace('!', '')
    noColon = noExclamationMark.replace(':', '')
    return ud.normalize('NFKD', noColon).encode('ASCII', 'ignore').lower().strip().decode("utf-8")

def extract_geonames(filename):
    geo_ids = {}
    g = pd.read_csv(filename, delimiter='\t', header=None)
    messy_column = dict(zip(g[3], g[0]))
    for key, value in messy_column.items():
        if isinstance(key, str):
            new_keys = key.split(",")
            for new_key in new_keys:
                geo_ids[new_key] = value

    geo_ids.update(dict(zip(g[1], g[0])))
    geo_ids.update(dict(zip(g[2], g[0])))

    geo_ids_normalized = {}

    for key, value in geo_ids.items():
        key_normalized = getNormalizedString(key)
        geo_ids_normalized[key_normalized] = value

    return geo_ids_normalized

def extract_places(df, columnname_places, columnname_countries):
    places = df[columnname_places].replace(to_replace=r'\[|\]|(\(.*?\))', value='', regex=True)
    countries = df[columnname_countries]
    places = list(places)
    countries = list(countries)

    places_clean = []
    for place in places:
        if type(place) is not float:
            place = getNormalizedString(place)
            if ". - " in place:
                place = place.replace(". - ", " ; ")
            elif " - " in place:
                place = place.replace(" - ", " ; ")
            places_clean.append(place.strip())
        else:
            places_clean.append("")

    place_country = list(zip(places_clean, countries))

    return place_country

def get_coordinates(geonames):
    coordinates = {}
    filenames = []
    filenames.append(geonames + "BE.txt")
    filenames.append(geonames + "FR.txt")
    filenames.append(geonames + "NL.txt")
    for filename in filenames:
        df = pd.read_csv(filename, delimiter = '\t', header=None)
        country = df[8].tolist()
        geonamesid = df[0].tolist()
        latitudes = df[4].tolist()
        longitudes = df[5].tolist()
        place = df[1].tolist()
        placecountrylatlong = list(zip(place, country, latitudes, longitudes))
        coordinates.update(dict(zip(geonamesid, placecountrylatlong)))
    return coordinates

def main():
    """This script fills out missing countries based on the place name (for Belgium, France & The Netherlands)"""
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('-i', '--input-file', action='store', help='The input file as CSV')
    parser.add_option('-c', '--column-with-country-names', action='store', help='The name of the column that contains the countries')
    parser.add_option('-p', '--column-with-places', action='store', help='The name of the column that contains the place names')
    parser.add_option('-g', '--geonames-folder', action='store', help='The filepath to the the geonames (insert the "/" at the end) folder. In this folder the geonames files for the three countries must be named "BE.txt", "FR.txt" and "NL.txt"')
    parser.add_option('-o', '--output-file', action='store', help='The output as TSV')
    (options, args) = parser.parse_args()

    if( ( not options.geonames_folder) or (not options.input_file) or (not options.column_with_country_names) or (not options.column_with_places) or (not options.geonames_folder) or (not options.output_file) ):
      parser.print_help()
      exit(1)

    be = extract_geonames(options.geonames_folder +"BE.txt")
    fr = extract_geonames(options.geonames_folder +"FR.txt")
    nl = extract_geonames(options.geonames_folder +"NL.txt")

    df = pd.read_csv(options.input_file, delimiter=',', encoding= 'utf-8')
    df = df.fillna('')

    places = extract_places(df, options.column_with_places, options.column_with_country_names)

    ids = []
    wrong_country = []
    for place in places:
        city = place[0]
        country = place[1]
        if ";" in city or ";" in country:
            ids.append("")
            wrong_country.append("")
        elif "Bel" in country and city in be:
            ids.append(be[city])
            wrong_country.append("")
        elif country == "France" and city in fr:
            ids.append(fr[city])
            wrong_country.append("")
        elif country == "Netherlands" and city in nl:
            ids.append(nl[city])
            wrong_country.append("")
        elif city in be:
            ids.append(be[city])
            wrong_country.append("yes")
        elif city in fr:
            ids.append(fr[city])
            wrong_country.append("yes")
        elif city in nl:
            ids.append(nl[city])
            wrong_country.append("yes")
        else:
            ids.append("")
            wrong_country.append("")

    d = get_coordinates(options.geonames_folder)

    geonames_place = []
    geonames_country = []
    geonames_lat = []
    geonames_long = []

    for id in ids:
        if id in d:
            geonames_place.append((d[id])[0])
            geonames_country.append((d[id])[1])
            geonames_lat.append((d[id])[2])
            geonames_long.append((d[id])[3])
        else:
            geonames_place.append("")
            geonames_country.append("")
            geonames_lat.append("")
            geonames_long.append("")

    df['targetPlaceOfPublicationIdentifier'] = ids
    df['wrong_country'] = wrong_country
    df['geonames_place'] = geonames_place
    df['geonames_country'] = geonames_country
    df['targetPlaceOfPublicationLatitude'] = geonames_lat
    df['targetPlaceOfPublicationLongitude'] = geonames_long

    df.to_csv(options.output_file, sep=",", index=False, encoding="utf-8")


main()

# python add_coordinates.py -i input.txt -c targetTextCountryOfPublication -p targetTextPlaceOfPublication -g geonames/ -o output.txt
