#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser



def main():
  """This script extracts the header of the input file and tries to replace each header based on the provided mapping file."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing CSV data')
  parser.add_option('-d', '--delimiter', action='store', help='The delimiter of the input file')
  parser.add_option('-o', '--output-file', action='store', help='The file in which content with new headers is stored')
  parser.add_option('-m', '--header-mapping-file', action='store', help='The CSV file containing a mapping from old to new headers')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) or (not options.header_mapping_file) or (not options.delimiter) ):
    parser.print_help()
    exit(1)

  #
  # Open input file with encoding 'utf-8-sig' (instead of 'utf-8') because the Syracuse export contains Byte Order marks (BOM)
  #
  with open(options.input_file, 'r', encoding="utf-8-sig") as inFile:
    inputReader = csv.reader(inFile, delimiter=options.delimiter)

    oldHeader = next(inputReader)
    oldHeaderLength = len(oldHeader)

    with open(options.header_mapping_file, 'r', encoding="utf-8") as hFile:
      mappingReader = csv.reader(hFile)

      #
      # get a dictionary where the old header name is the key and the new header name the value
      #
      mapping = {rows[0]:rows[1] for rows in mappingReader}

      notFound = list()
      replaced = 0

      #
      # iterate over the old header and if the mapping contains a new value, replace it
      #
      for i, val in enumerate(oldHeader):
        if( val in mapping):
          oldHeader[i] = mapping[val]
          replaced+=1
        else:
          notFound.append(val)

       # todo: write new header and content to output file 
      with open(options.output_file, 'w', encoding="utf-8") as outFile:
        outputWriter = csv.writer(outFile, delimiter=options.delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # write new header (which is the updated oldHeader)
        outputWriter.writerow(oldHeader)

        # write the content of the input file
        for row in inputReader:
          outputWriter.writerow(row)

      print("replaced " + str(replaced) + "/" + str(oldHeaderLength) + " headers!")
      if(replaced != oldHeaderLength):
        print("Finished with warnings: could not find the following fields in the mapping:")
        print(notFound)
      

main()
