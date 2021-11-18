#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import xml.etree.ElementTree as ET
import json
import itertools
import csv
from optparse import OptionParser
import utils

NS_MARCSLIM = 'http://www.loc.gov/MARC21/slim'

# -----------------------------------------------------------------------------
def countDatafields(df, countDict):
  """This function counts differnt types of datafields and stores the result in 'countDict'."""
  if(df.tag == ET.QName(NS_MARCSLIM, 'datafield')):
    tagName = df.attrib['tag']
    if tagName in countDict:
      countDict[tagName]['number'] += 1
    else:
      countDict[tagName] = {'number': 1}

# -----------------------------------------------------------------------------
def countUniqueDatafields(fields, countDict):
   """This function takes a set of fields (thus unique) and adds 1 to the related-counter in countDict."""
   for f in fields:
     if 'unique' in countDict[f]:
       countDict[f]['unique'] += 1
     else:
       countDict[f]['unique'] = 1

# -----------------------------------------------------------------------------
def calculatePercentages(countDict):
  """This function counts percentages for each datafield based on 'totalRecords' and stores it in 'percentage' per field."""
  total = countDict['totalRecords']
  for df in countDict:
    # only count percentages for MARC datafields (they all are numbers)
    if df.isdigit():
      countDict[df]['percentage'] = round((countDict[df]['unique']/total)*100, 4)


# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format and generates statistics about used fields."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing MARC slim XML records')
  parser.add_option('-o', '--output-file', action='store', help='The file in which statistics about the input is stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  stats = {}
  uniqueISNINumbers = set()
  for event, elem in ET.iterparse(options.input_file, events=('start', 'end')):

    #
    # The parser finished reading one MARC SLIM record, get information and then discard the record
    #
    if  event == 'end' and elem.tag == 'responseRecord':
      utils.count(stats, 'responseRecord')

      for datafield in elem:
        if datafield.tag == 'ISNIAssigned':
          utils.count(stats, 'ISNIAssigned')
          for subfield in datafield:
            if subfield.tag == 'dataConfidence':
              utils.countStat(stats, 'assignedConfidence', subfield.text)
            elif subfield.tag == 'isniUnformatted':
              utils.count(stats, 'unformattedISNINumbers')
              uniqueISNINumbers.add(subfield.text)
        elif datafield.tag == 'ISNINotAssigned':
          utils.count(stats, 'ISNINotAssigned')

        #
        # check for subfields which are the same for ISNIAssigned and ISNINotAssigned
        #
        for subfield in datafield:
          if subfield.tag == 'ISNIMetadata':
            for metadataField in subfield:
              if metadataField.tag == 'identity':
                for identityField in metadataField:
                  utils.count(stats, identityField.tag)
                  if identityField.tag == 'personOrFiction':
                    for personInfo in identityField:
                      if personInfo.tag == 'personalName':
                        forename = ''
                        surname = ''
                        for nameInfo in personInfo:
                          if nameInfo.tag == 'forename':
                            forename = nameInfo.text
                          if nameInfo.tag == 'surename':
                            surname = nameInfo.text
                          if nameInfo.tag == 'languageOfName':
                            utils.count(stats, 'name-language-' + nameInfo.text)
                        #print(f'{surname}, {forename}')
                      if personInfo.tag == 'additionalInformation':
                        for info in personInfo:
                          nationalityCounter = 0
                          associatedCountriesCounter = 0
                          genderCounter = 0
                          if info.tag == 'nationality':
                            nationalityCounter += 1
                            utils.count(stats, 'person-nationality-' + info.text)
                          if info.tag == 'gender':
                            genderCounter += 1
                            utils.count(stats, 'person-gender-' + info.text)
                          if info.tag == 'countriesAssociated':
                            for countryInfo in info:
                              if countryInfo.tag == 'countryCode':
                                associatedCountriesCounter += 1
                                utils.count(stats, 'person-associated-' + countryInfo.text)
                        utils.countStat(stats, 'multipleNationalities', nationalityCounter)
                        utils.countStat(stats, 'multipleAssociatedCountries', associatedCountriesCounter)
                        utils.countStat(stats, 'multipleGenders', genderCounter)
                  if identityField.tag == 'organisation':
                    pass
                

      elem.clear()

  print(f'unique unformatted ISNI numbers {len(uniqueISNINumbers)}')
  for key,val in sorted(stats.items()):
    if isinstance(val, dict):
      minVal = val['min']
      maxVal = val['max']
      avgVal = val['avg']
      numVal = val['number']
      print(key)
      print(f'\tmin {minVal}, max {maxVal}, avg {avgVal}, amount {numVal}')
    else:
      print(key)
      print("\t" + str(val))
  #
  # Calculate percentages
  #
  #calculatePercentages(stats)
  #with open(options.output_file, 'w') as outFile:
  #  fields=['field', 'number', 'unique', 'percentage']
  #  outputWriter = csv.DictWriter(outFile, fieldnames=fields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  #  outputWriter.writeheader()

  #  for key,val in sorted(stats.items()):
  #    if(key.isdigit()):
  #      row = {'field': key}
  #      row.update(val)
  #      outputWriter.writerow(row)


main()
