# -*- coding: utf-8 -*-
"""
@author: Fabrizio Pascucci
@author: Sven Lieber
"""
import csv
from optparse import OptionParser
import pandas as pd
import re
import glob
import unicodedata as ud
import utils

def main():
    """This script selects geoname identifeirs and longitude/latidude coordindates
    based on the place name (for Belgium, France & The Netherlands)"""
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

    with open(options.input_file, 'r', encoding='utf-8') as inFile, \
         open(options.output_file, 'w', encoding='utf-8') as outFile:

        inputReader = csv.DictReader(inFile, delimiter=',')

        # prepare slightly different output headers to include derived data
        outputHeaders = inputReader.fieldnames.copy()
        placeOfPublicationIndex = outputHeaders.index('targetPlaceOfPublication')
        outputHeaders.insert(placeOfPublicationIndex+1, 'targetPlaceOfPublicationIdentifier')
        outputHeaders.insert(placeOfPublicationIndex+2, 'targetPlaceOfPublicationLongitude')
        outputHeaders.insert(placeOfPublicationIndex+3, 'targetPlaceOfPublicationLatitude')
        outputWriter = csv.DictWriter(outFile, fieldnames=outputHeaders, delimiter=',')
        outputWriter.writeheader()

        locationDelimiter = ';'
        numRows = 0
        numLocations = 0
        for row in inputReader:
            numRows += 1
            location = row[options.column_with_places]
            locationListNorm = utils.normalizeDelimiters(location, delimiter=locationDelimiter)

            # create a list of locations, even if it just has one entry
            locations = locationListNorm.split(locationDelimiter) if locationDelimiter in locationListNorm else [locationListNorm]

            for l in locations:
                numLocations += 1
                # The location might be in brackets, e.g. "(Brussels)" or "[Brussels]"
                noBrackets = utils.extractStringFromBrackets(l)
                # The location may contain also a country, e.g. "Gent (Belgium)"
                onlyLocation = utils.extractLocationFromLocationCountryString(noBrackets)
                # The location needs to be normalized with respect to special characters
                lNorm = utils.getNormalizedString(onlyLocation)
                lNorm = lNorm.strip()

                locationMainSpelling = ''
                locationIdentifier = ''
                locationLongitude = ''
                locationLatitude = ''
                locationCountry = ''
                # ElseIf because some places exist in several countries, but we want to prioritize Belgium
                # E.g. Hasselt exists in Belgium and in the Netherlands
                if lNorm == '':
                    pass
                elif lNorm in be:
                    locationMainSpelling = utils.getGeoNamesMainSpellingFromDataFrame(beContent, be[lNorm])
                    locationCountry = 'Belgium'
                    locationIdentifier = be[lNorm]
                    locationLongitude = utils.getGeoNamesLongitude(beContent, be[lNorm])
                    locationLatitude = utils.getGeoNamesLatitude(beContent, be[lNorm])
                elif lNorm in fr:
                    locationMainSpelling = utils.getGeoNamesMainSpellingFromDataFrame(frContent, fr[lNorm])
                    locationCountry = 'France'
                    locationIdentifier = fr[lNorm]
                    locationLongitude = utils.getGeoNamesLongitude(frContent, fr[lNorm])
                    locationLatitude = utils.getGeoNamesLatitude(frContent, fr[lNorm])
                elif lNorm in nl:
                    locationMainSpelling = utils.getGeoNamesMainSpellingFromDataFrame(nlContent, nl[lNorm])
                    locationCountry = 'Netherlands'
                    locationIdentifier = nl[lNorm]
                    locationLongitude = utils.getGeoNamesLongitude(nlContent, nl[lNorm])
                    locationLatitude = utils.getGeoNamesLatitude(nlContent, nl[lNorm])
                else:
                    # use the filtered one we got from the input (e.g. without country in brackets)
                    locationMainSpelling = onlyLocation

                outputRow = row.copy()
                outputRow['targetPlaceOfPublication'] = locationMainSpelling
                outputRow['targetCountryOfPublication'] = locationCountry
                outputRow['targetPlaceOfPublicationIdentifier'] = locationIdentifier
                outputRow['targetPlaceOfPublicationLongitude'] = locationLongitude
                outputRow['targetPlaceOfPublicationLatitude'] = locationLatitude

                outputWriter.writerow(outputRow)
        print(f'processed {numRows} rows and {numLocations} locations')


main()

