# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 18:01:31 2022

@author: Fabrizio Pascucci
@author: Sven Lieber
"""
import csv
from optparse import OptionParser
import pandas as pd
import re
import glob
import unicodedata as ud
import utils_geo
import utils_string

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
    be = utils_geo.extract_geonames(beContent)
    frContent = pd.read_csv(options.geonames_folder + "FR.txt", delimiter='\t', header=None)
    fr = utils_geo.extract_geonames(frContent)
    nlContent = pd.read_csv(options.geonames_folder + "NL.txt", delimiter='\t', header=None)
    nl = utils_geo.extract_geonames(nlContent)

    with open(options.input_file, 'r', encoding='utf-8') as inFile, \
         open(options.output_file, 'w', encoding='utf-8') as outFile:

        inputReader = csv.DictReader(inFile, delimiter=',')
        outputWriter = csv.DictWriter(outFile, fieldnames=inputReader.fieldnames, delimiter=',')
        outputWriter.writeheader()

        locationDelimiter = ';'
        for row in inputReader:
            location = row[options.column_with_places]
            locationListNorm = utils_string.normalizeDelimiters(location, delimiter=locationDelimiter)

            # create a list of locations, even if it just has one entry
            locations = locationListNorm.split(locationDelimiter) if locationDelimiter in locationListNorm else [locationListNorm]

            # we use a filter because otherwise an empty string becomes an array with one empty country
            existingCountries = list(filter(None, row[options.column_with_country_names].split(';')))
            foundCountries = set()

            # For the end result we also need the non-normalized main spelling of the location
            locationsMainSpelling = set()

            for l in locations:

                # The location might be in brackets, e.g. "(Brussels)" or "[Brussels]"
                noBrackets = utils_string.extractStringFromBrackets(l)
                # The location may contain also a country, e.g. "Gent (Belgium)"
                onlyLocation = utils_geo.extractLocationFromLocationCountryString(noBrackets)
                # The location needs to be normalized with respect to special characters
                lNorm = utils_string.getNormalizedString(onlyLocation)
                lNorm = lNorm.replace(' etc.', '')
                lNorm = lNorm.replace('[etc.]', '')
                lNorm = lNorm.strip()

                # ElseIf because some places exist in several countries, but we want to prioritize Belgium
                # E.g. Hasselt exists in Belgium and in the Netherlands
                if lNorm == '':
                    pass
                elif lNorm in be:
                    foundCountries.add('Belgium')
                    locationsMainSpelling.add(utils_geo.getGeoNamesMainSpellingFromDataFrame(beContent, be[lNorm]))
                elif lNorm in fr:
                    if 'montreal' in lNorm and 'Québec' in noBrackets:
                      foundCountries.add('Canada')
                      locationsMainSpelling.add('Montréal')
                    elif 'lausanne' in lNorm:
                      foundCountries.add('Switzerland')
                      locationsMainSpelling.add('Lausanne')
                    elif 'cologne' in lNorm:
                      foundCountries.add('Germany')
                      locationsMainSpelling.add('Cologne')
                    else:
                      foundCountries.add('France')
                      locationsMainSpelling.add(utils_geo.getGeoNamesMainSpellingFromDataFrame(frContent, fr[lNorm]))
                elif lNorm in nl:
                    foundCountries.add('Netherlands')
                    locationsMainSpelling.add(utils_geo.getGeoNamesMainSpellingFromDataFrame(nlContent, nl[lNorm]))
                else:
                    usedSpelling = onlyLocation.replace(' etc.', '').replace('[etc.]', '').strip()
                    locationsMainSpelling.add(usedSpelling)

            for foundC in foundCountries:
                if foundC not in existingCountries:
                    existingCountries.append(foundC)

            existingCountries.sort()
            newLocationsString = ';'.join(sorted(locationsMainSpelling))
            newCountriesString = ';'.join(existingCountries)
            row[options.column_with_places] = newLocationsString
            row[options.column_with_country_names] = newCountriesString
            outputWriter.writerow(row)


if __name__ == '__main__':
  main()

