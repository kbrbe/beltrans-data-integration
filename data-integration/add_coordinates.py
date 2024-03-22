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
import utils_geo
import utils_string

def createMapping(filename):

    mapping = {}
    # Input file example: "Brussel = Bruxelles,Belgium,2800866,4.34878,50.85045"
    with open(filename, 'r', encoding='utf-8') as inFile:
        inputReader = csv.reader(inFile, delimiter=',')

        # skip header
        next(inputReader)

        for row in inputReader:
            mapping[row[0]] = [row[1], row[2], row[3], row[4], row[5]]
    return mapping

def main():
    """This script selects geoname identifeirs and longitude/latidude coordindates
    based on the place name (for Belgium, France & The Netherlands)"""
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('-i', '--input-file', action='store', help='The input file as CSV')
    parser.add_option('--input-id-column', action='store', help='The name of the column with the row identifier')
    parser.add_option('-p', '--column-with-places', action='store', help='The name of the column that contains the place names')
    parser.add_option('-m', '--mapping_file', action='store', help='An optional CSV file with a mapping between place names and correct identifier/longitude/latitude combination')
    parser.add_option('-g', '--geonames-folder', action='store', help='The filepath to the the geonames (insert the "/" at the end) folder. In this folder the geonames files for the three countries must be named "BE.txt", "FR.txt" and "NL.txt"')
    parser.add_option('-o', '--output-file', action='store', help='The output as TSV')
    parser.add_option('--column-place', action='store', help='The name of the output column for the place name')
    parser.add_option('--column-country', action='store', help='The name of the output column for the country name')
    parser.add_option('--column-identifier', action='store', help='The name of the output column for the geonames identifier')
    parser.add_option('--column-longitude', action='store', help='The name of the output column for the longitude coordinate')
    parser.add_option('--column-latitude', action='store', help='The name of the output column for the latitude coordinate')
    (options, args) = parser.parse_args()

    if( ( not options.geonames_folder) or (not options.input_file) or (not options.column_with_places) or (not options.geonames_folder) or (not options.output_file) or (not options.column_place) or (not options.column_country) or (not options.column_identifier) or (not options.column_longitude) or (not options.column_latitude) or (not options.input_id_column) ):
      parser.print_help()
      exit(1) 

    beContent = pd.read_csv(options.geonames_folder + "BE.txt", delimiter='\t', header=None)
    be = utils_geo.extract_geonames(beContent)
    frContent = pd.read_csv(options.geonames_folder + "FR.txt", delimiter='\t', header=None)
    fr = utils_geo.extract_geonames(frContent)
    nlContent = pd.read_csv(options.geonames_folder + "NL.txt", delimiter='\t', header=None)
    nl = utils_geo.extract_geonames(nlContent)

    mapping = {}
    if options.mapping_file:
        mapping = createMapping(options.mapping_file)

    with open(options.input_file, 'r', encoding='utf-8') as inFile, \
         open(options.output_file, 'w', encoding='utf-8') as outFile:

        inputReader = csv.DictReader(inFile, delimiter=',')

        # prepare slightly different output headers to include derived data
        outputHeaders = [options.input_id_column, options.column_place, options.column_country,
                         options.column_identifier, options.column_longitude, options.column_latitude]
        outputWriter = csv.DictWriter(outFile, fieldnames=outputHeaders, delimiter=',')
        outputWriter.writeheader()

        locationDelimiter = ';'
        numRows = 0
        numLocations = 0
        for row in inputReader:
            numRows += 1
            location = row[options.column_with_places]
            locationListNorm = utils_string.normalizeDelimiters(location, delimiter=locationDelimiter)

            # create a set of locations, even if it just has one entry
            locations = locationListNorm.split(locationDelimiter) if locationDelimiter in locationListNorm else [locationListNorm]

            alreadySeenLocations = set()
            for l in locations:
                numLocations += 1
                # The location might be in brackets, e.g. "(Brussels)" or "[Brussels]"
                noBrackets = utils_string.extractStringFromBrackets(l)
                # The location may contain also a country, e.g. "Gent (Belgium)"
                onlyLocation = utils_geo.extractLocationFromLocationCountryString(noBrackets)
                # The location needs to be normalized with respect to special characters
                lNorm = utils_string.getNormalizedString(onlyLocation)
                lNorm = lNorm.strip()

                # it could be the same location exists twice in a string, e.g. "Paris. - [Paris]"
                if lNorm in alreadySeenLocations:
                    break
                else:
                    alreadySeenLocations.add(lNorm)

                locationMainSpelling = ''
                locationIdentifier = ''
                locationLongitude = ''
                locationLatitude = ''
                locationCountry = ''
                # ElseIf because some places exist in several countries, but we want to prioritize Belgium
                # E.g. Hasselt exists in Belgium and in the Netherlands
                if lNorm == '':
                  if options.column_country in row:
                    # Don't overwrite existing values if nothing was found https://github.com/kbrbe/beltrans-data-integration/issues/252
                    locationCountry = row[options.column_country]
                elif lNorm in be:
                    locationMainSpelling = utils_geo.getGeoNamesMainSpellingFromDataFrame(beContent, be[lNorm])
                    locationCountry = 'Belgium'
                    locationIdentifier = be[lNorm]
                    locationLongitude = utils_geo.getGeoNamesLongitude(beContent, be[lNorm])
                    locationLatitude = utils_geo.getGeoNamesLatitude(beContent, be[lNorm])
                elif lNorm in fr:
                    if 'montreal' in lNorm and 'Montréal' in noBrackets:
                      locationMainSpelling = 'Montréal'
                      locationCountry = 'Canada'
                      locationIdentifier = '6077243'
                      locationLongitude = '-73.58781'
                      locationLatitude = '45.50884'
                    else:
                      locationMainSpelling = utils_geo.getGeoNamesMainSpellingFromDataFrame(frContent, fr[lNorm])
                      locationCountry = 'France'
                      locationIdentifier = fr[lNorm]
                      locationLongitude = utils_geo.getGeoNamesLongitude(frContent, fr[lNorm])
                      locationLatitude = utils_geo.getGeoNamesLatitude(frContent, fr[lNorm])
                elif lNorm in nl:
                    locationMainSpelling = utils_geo.getGeoNamesMainSpellingFromDataFrame(nlContent, nl[lNorm])
                    locationCountry = 'Netherlands'
                    locationIdentifier = nl[lNorm]
                    locationLongitude = utils_geo.getGeoNamesLongitude(nlContent, nl[lNorm])
                    locationLatitude = utils_geo.getGeoNamesLatitude(nlContent, nl[lNorm])
                else:
                    # if not found in the BE/Fr/NL geonames dump check if a manual mapping was provided
                    if onlyLocation in mapping:
                        locationMainSpelling = mapping[onlyLocation][0]
                        locationCountry = mapping[onlyLocation][1]
                        locationIdentifier = mapping[onlyLocation][2]
                        locationLongitude = mapping[onlyLocation][3]
                        locationLatitude = mapping[onlyLocation][4]
                    else:
                        # use the filtered one we got from the input (e.g. without country in brackets)
                        locationMainSpelling = onlyLocation

                #outputRow = row.copy()
                outputRow = {}
                outputRow[options.input_id_column] = row[options.input_id_column]
                outputRow[options.column_place] = locationMainSpelling
                outputRow[options.column_country] = locationCountry
                outputRow[options.column_identifier] = locationIdentifier
                outputRow[options.column_longitude] = locationLongitude
                outputRow[options.column_latitude] = locationLatitude

                outputWriter.writerow(outputRow)
        print(f'processed {numRows} rows and {numLocations} locations')


if __name__ == '__main__':
  main()

