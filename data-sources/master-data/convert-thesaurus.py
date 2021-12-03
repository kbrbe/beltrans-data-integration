#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser


# -----------------------------------------------------------------------------
def writeResult(writer, rowID, name, parent):
  writer.writerow([rowID, name.strip(), parent])

def main():
  """This script converts a thesaurus CSV where each level is specified in another column to a more machine-friendly format."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing CSV data')
  parser.add_option('-o', '--output-file', action='store', help='The file in which content with new headers is stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  with open(options.input_file, 'r', encoding="latin_1") as inFile, \
       open(options.output_file, 'w', encoding="latin_1") as outFile:

    inputReader = csv.DictReader(inFile, delimiter=';')
    outputWriter = csv.writer(outFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    outputWriter.writerow(['id', 'name', 'parentID'])
    parents = list()
    lastLevel = 1
    for row in inputReader:
      # the first 10 columns refer to the different thesaurus levels, DictReader gives us the column names in the original order
      # iterate over these first 10 columns determine the value and parent
      numNameColumns = 10
      currentCol = 1
      rowID = row['Identifiant']
      for (col, val) in row.items():
        if(currentCol == numNameColumns):
          break
        if val != '':
          currentLevel = currentCol
          if len(parents) == 0:
            writeResult(outputWriter, rowID, val, '')
            parents.append(rowID)
            lastLevel = currentLevel
          else:
            if currentLevel > lastLevel:
              # we are now one hierarchy level lower
              writeResult(outputWriter, rowID, val, parents[-1])
              # now we are a possible new parent
              parents.append(rowID)
              lastLevel = currentLevel
            elif currentLevel == lastLevel:
              # we are still on the same hierarchy level
              # following records might be our children,
              # thus remove our neighboor and set ourselves as parent
              parents.pop()
              writeResult(outputWriter, rowID, val, parents[-1])
              parents.append(rowID)
              lastLevel = currentLevel
            else:
              # we are one or more hierarchy levels up again
              # remove the current element because it is not a parent for anyone
              parents.pop()
              # we might be several hierarchy levels higher,
              # thus also remove other parents, e.g. we were in level 4, but now we are in a hierarchy for 1, thus remove 4-1 = 3
              levelDiff = lastLevel - currentLevel
              for i in range(levelDiff):
                parents.pop()
              lastLevel = currentLevel
              if len(parents) > 0:
                writeResult(outputWriter, rowID, val, parents[-1])
              else:
                # we are again at a new root
                writeResult(outputWriter, rowID, val, '')
              parents.append(rowID)
              
         
        currentCol += 1


main()
