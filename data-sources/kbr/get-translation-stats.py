#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import xml.etree.ElementTree as ET
import json
import itertools
import utils
import csv
from optparse import OptionParser

NS_MARCSLIM = 'http://www.loc.gov/MARC21/slim'
ALL_NS = {'': NS_MARCSLIM}

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
def countPublicationDates(df, countDict):
  """This function counts the number of records per publication date based on the MARC field 264 $c."""

  if(df.tag == ET.QName(NS_MARCSLIM, 'datafield')):
    tagNumber = df.attrib['tag']
    if(tagNumber == '264'):
      date = ''

      #
      # iterate over subfields to find the actual date in MARC subfield $c
      #
      for sf in df.iter():
        if(sf.tag == ET.QName(NS_MARCSLIM, 'subfield')):
          code = sf.attrib['code']
          if(code == 'c'):
            date = sf.text

      if(date != ''):
        if date in countDict:
          countDict[date] += 1
        else:
          countDict[date] = 1
      else:
        if 'NO_DATE' in countDict:
          countDict['NO_DATE'] += 1
        else:
          countDict['NO_DATE'] = 1
 

# -----------------------------------------------------------------------------
def countTitleVariants(df, countDict):
  """This function counts the type of a variant title and the language based on MARC field 246 $g (language) $i (type)."""

  if(df.tag == ET.QName(NS_MARCSLIM, 'datafield')):
    tagNumber = df.attrib['tag']
    if(tagNumber == '246'):
      variantType = ''
      variantLanguage = 'NOT_FOUND'

      #
      # iterate over subfields to find the type ($i) and language ($g)
      #
      for sf in df.iter():
        if(sf.tag == ET.QName(NS_MARCSLIM, 'subfield')):
          code = sf.attrib['code']
          if(code == 'g'):
            variantLanguage = sf.text
          if(code == 'i'):
            variantType = sf.text

      if(variantType != ''):
        if variantType in countDict:
          if variantLanguage in countDict[variantType]:
            countDict[variantType][variantLanguage] += 1
          else:
            countDict[variantType][variantLanguage] = 1
        else:
          countDict[variantType] = {variantLanguage: 1}
      else:
        if 'NO_VARIANT_TYPE' in countDict:
          countDict['NO_VARIANT_TYPE'] += 1
        else:
          countDict['NO_VARIANT_TYPE'] = 1
      
# -----------------------------------------------------------------------------
def countBindingTypes(elem, countDict, valuesDict):
  """This function counts the different variants of binding types in MARC field 020$q."""

  kbrID = utils.getElementValue(elem.find('./controlfield[@tag="001"]', ALL_NS))
  bindingType = utils.getElementValue(elem.find('./datafield[@tag="020"]/subfield[@code="q"]', ALL_NS))
  utils.count(countDict, bindingType, kbrID, valuesDict)

# -----------------------------------------------------------------------------
def countMediumTypes(elem, countDict, valuesDict):
  """This function counts the different variants of medium types in MARC field 245$h."""

  kbrID = utils.getElementValue(elem.find('./controlfield[@tag="001"]', ALL_NS))
  mediumType = utils.getElementValue(elem.find('./datafield[@tag="245"]/subfield[@code="h"]', ALL_NS))
  utils.count(countDict, mediumType, kbrID, valuesDict)

# -----------------------------------------------------------------------------
def printStatsLog(stats, valueLog, field, fieldName):
  """This function prints stats of the key 'field' in 'stats' in a certain format for further processing."""

  for key,val in stats[field].items():
    # we are only interested in non-standard values, e.g. single letter codes such as 'b' or 'd' are not of interest
    if len(key) > 1:
      if val < 5:
        # print the associated logged KBR identifiers
        identifiers = valueLog[key]
        print(f'{fieldName} ({field}) records having the value "{key}": {identifiers}')
        print()
      else:
        print(f'### {fieldName} ({field}) records with the value "{val}" ###')
        print(f'IDENT="', end='')
        print(f'" AND IDENT="'.join(valueLog[key]), end='')
        print('"')
        print()


# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format and generates statistics about used fields."""

  parser = OptionParser(usage="usage: %prog [options]")
  # commented out because there is no auto completion for bash for options (but for arguments), we anyway only have one parameter
  #parser.add_option('-i', '--input-file', action='store', help='The input file containing MARC slim XML records')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( len(args) != 1 ):
    parser.print_help()
    exit(1)

  inputFile = args[0]
  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  stats = {'totalRecords': 0, 'date': {}, 'translation': {}, 'binding-types': {}, 'medium-types': {} }
  valueLog = {}

  for event, elem in ET.iterparse(inputFile, events=('start', 'end')):
    if  event == 'start' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):
      stats['totalRecords'] += 1

    #
    # The parser finished reading one MARC SLIM record, get information and then discard the record
    #
    if  event == 'end' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):
      foundFields = set()

      countBindingTypes(elem, stats['binding-types'], valueLog)
      countMediumTypes(elem, stats['medium-types'], valueLog)

      for datafield in elem:
        #print(datafield.tag, datafield.attrib, datafield.text)
        countTitleVariants(datafield, stats['translation'])
        countPublicationDates(datafield, stats['date'])
        #countDatafields(datafield, stats)
        if datafield.tag == ET.QName(NS_MARCSLIM, 'datafield'):
          foundFields.add(datafield.attrib['tag'])
      #countUniqueDatafields(foundFields, stats)
      elem.clear()

  print(json.dumps(stats['totalRecords'], indent=4))
  print(json.dumps(stats['date'], indent=4))
  print(json.dumps(stats['translation'], indent=4))

  printStatsLog(stats, valueLog, 'binding-types', 'Q020')
  printStatsLog(stats, valueLog, 'medium-types', 'KBRM')

main()
