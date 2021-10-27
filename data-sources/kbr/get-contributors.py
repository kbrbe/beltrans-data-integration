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
def main():
  """This script reads an XML file in MARC slim format and generates statistics about used fields."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing MARC slim XML records')
  parser.add_option('-p', '--pattern', action='store', help='The pattern for the name of the output files, e.g. "2021-10-export" which could result in files such as "2021-10-export-pbl.csv" for publishers')
  parser.add_option('-r', '--roles', action='append', help='A list of possible roles for which output files should be generated, see list of MARC roles. Possible values are "pbl" for publisher or "trl" for translator')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.pattern) or (not options.roles) ):
    parser.print_help()
    exit(1)

  #
  # Set the default namespace for the collection (and thus also for all child records)
  #
  ET.register_namespace('', 'http://www.loc.gov/MARC21/slim')

  stats = {}
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
      recordID = ''
      date = ''
      contributors = list()
      for datafield in elem:

        #
        # get the ID of the bibliographic record
        #
        if(datafield.tag == ET.QName(NS_MARCSLIM, 'controlfield') and datafield.attrib['tag'] == '001'):
          recordID = datafield.text

        #
        # get the date so we can later filter on the date
        #
        if(datafield.tag == ET.QName(NS_MARCSLIM, 'datafield') and datafield.attrib['tag'] == '264'):

          #
          # iterate over subfields to find the actual date in MARC subfield $c, stop looking in subfields when found
          #
          for sf in datafield.iter():
            if(sf.tag == ET.QName(NS_MARCSLIM, 'subfield') and sf.attrib['code'] == 'c' and sf.text is not None):
              date = sf.text
              break


        #
        # Get the contributor, their name and their role
        #
        if(datafield.tag == ET.QName(NS_MARCSLIM, 'datafield') and ( datafield.attrib['tag'] == '700' or datafield.attrib['tag'] == '710') ):
          contributor = 'NO_IDENTIFIER'
          role = 'NO_ROLE'
          for sf in datafield.iter():
            if(sf.tag == ET.QName(NS_MARCSLIM, 'subfield')):
              code = sf.attrib['code']
              if(code == '*'):
                contributorID = sf.text
              if(code == 'a'):
                contributorName = sf.text
              if(code == '4'):
                role = sf.text
          contributors.append((contributorID, contributorName, role))
      #
      # We are done iterating over all datafields, store the data we collected
      #
      if(date != '' and date.startswith(('197', '198', '199', '200', '201', '2020')) ):
        for (cID, cN, r) in contributors:
          if(r in stats):
            if(recordID in stats[r]):
              stats[r][recordID].append((cID, cN))
            else:
              stats[r][recordID] = [(cID, cN)]
          else:
            stats[r] = {recordID: [(cID, cN)]}


      elem.clear()

  #print(json.dumps(stats, indent=4))
  print("Found roles: ")
  print(stats.keys())

  #
  # Create CSV files for some of the selected roles
  #
  for role in options.roles:
    if role in stats.keys():
      outputFilename = options.pattern + '-' + role + ".csv"
      with open(outputFilename, 'w', encoding='utf-8') as outFile:
        writer = csv.writer(outFile, delimiter=',')
        writer.writerow(['role', 'bibID', 'contributorID', 'contributorName'])
        for bibID in stats[role]:
          for contributor in stats[role][bibID]:
            writer.writerow([role, bibID, contributor[0], contributor[1]])
      print("Created file '" + outputFilename + "' for role '" + role + "'")
    else:
      print("Skipping '" + role + "', no contributors found with that role!")

main()
