#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import xml.etree.ElementTree as ET
import json
import itertools
import csv
from optparse import OptionParser

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
def count(stats, counter):
  if counter in stats:
    stats[counter] += 1
  else:
    stats[counter] = 1

# -----------------------------------------------------------------------------
def countStat(stats, counter, value):
  if counter in stats:
    stats[counter]['values'].append(value)
    stats[counter]['number'] += 1
    stats[counter]['min'] = min(stats[counter]['min'], value)
    stats[counter]['max'] = max(stats[counter]['max'], value)
    stats[counter]['avg'] = sum(stats[counter]['values'])/len(stats[counter]['values'])
  else:
    stats[counter] = {'min': value, 'max': value, 'avg': value, 'number': value, 'values': [value]}

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
  stats = {'totalRecords': 0}
  for event, elem in ET.iterparse(options.input_file, events=('start', 'end')):
    if  event == 'start' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):
      stats['totalRecords'] += 1

    #
    # The parser finished reading one MARC SLIM record, get information and then discard the record
    #
    if  event == 'end' and elem.tag == 'responseRecord':
      count(stats, 'responseRecord')

      for datafield in elem:
        if datafield.tag == 'ISNIAssigned':
          count(stats, 'ISNIAssigned')
          for subfield in datafield:
            if subfield.tag == 'dataConfidence':
              countStat(stats, 'assignedConfidence', subfield.text)
        elif datafield.tag == 'ISNINotAssigned':
          count(stats, 'ISNINotAssigned')

        #
        # check for subfields which are the same for ISNIAssigned and ISNINotAssigned
        #
        for subfield in datafield:
          if subfield.tag == 'ISNIMetadata':
            for subsubfield in subfield:
              if subsubfield.tag == 'identity':
                pass

        #print(datafield.tag, datafield.attrib, datafield.text)
        countDatafields(datafield, stats)
        if datafield.tag == ET.QName(NS_MARCSLIM, 'datafield'):
          foundFields.add(datafield.attrib['tag'])
      countUniqueDatafields(foundFields, stats)
      elem.clear()

  #
  # Calculate percentages
  #
  calculatePercentages(stats)
  with open(options.output_file, 'w') as outFile:
    fields=['field', 'number', 'unique', 'percentage']
    outputWriter = csv.DictWriter(outFile, fieldnames=fields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    outputWriter.writeheader()

    for key,val in sorted(stats.items()):
      if(key.isdigit()):
        row = {'field': key}
        row.update(val)
        outputWriter.writerow(row)

main()
