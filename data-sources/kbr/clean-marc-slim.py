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
def cleanDate(df):
  """This function cleans the date in the MARC field 264 $c."""

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
              newDate = utils.parseYear(date, ['[%Y]', '(%Y)', '%Y', '%Y-', '%Y]', '%Y.', '%Y .', '%Y ;', '[%Y ?]', 'cop. %Y'])
              # replace if the detected years are from the 70s, 80s etc (this also includes values such as '197?' or '2014-2015')
              #if( newDate.startswith(('197', '198', '199', '200', '201', '2020')) ):
              sf.text = newDate
              if( any(s in newDate for s in ['s', 'd']) ):
                sf.text = ''
                
          

# -----------------------------------------------------------------------------
def cleanTitleVariants(df):
  """This function cleans the subfield type of title variant ($i) of MARC field 246."""

  if(df.tag == ET.QName(NS_MARCSLIM, 'datafield')):
    tagNumber = df.attrib['tag']
    if(tagNumber == '246'):
      variantType = ''
      variantLanguage = 'NOT_FOUND'

      #
      # iterate over subfields to find the type ($i)
      #
      for sf in df.iter():
        if(sf.tag == ET.QName(NS_MARCSLIM, 'subfield')):
          code = sf.attrib['code']
          if(code == 'i'):
            variantType = sf.text
            if( sf.text.startswith( ('original tit', 'Oorspronkel', 'Titre original', 'oorspronkelijk', 'titre original', 'Originele', 'originele', 'Ooors', 'Oorsp', 'Original') ) ):
              sf.text = "Titre original / oorspronkelijke titel"

# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format in a streaming fashion, performs some cleaning and creates a new output file with the cleaned records."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing MARC slim XML records')
  parser.add_option('-o', '--output-file', action='store', help='The file in which the cleaned data is stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  #
  # Set the default namespace for the collection (and thus also for all child records)
  #
  ET.register_namespace('', 'http://www.loc.gov/MARC21/slim')

  with open(options.output_file, 'wb') as outFile:

    outFile.write(b'<collection>')
    counter = 0
    #
    # Instead of loading everything to main memory, stream over the XML using iterparse
    #
    for event, elem in ET.iterparse(options.input_file, events=('start', 'end')):

      #
      # The parser finished reading one MARC SLIM record, get information and then discard the record
      #
      if  event == 'end' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):
        counter += 1
        for datafield in elem:
          cleanDate(datafield)
          cleanTitleVariants(datafield)

        outFile.write(ET.tostring(elem, encoding='utf-8'))
        elem.clear()
    outFile.write(b'</collection>')


main()
