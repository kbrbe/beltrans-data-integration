#
# (c) 2022 Sven Lieber
# KBR Brussels
#
import csv
import utils
from tqdm import tqdm
from optparse import OptionParser

# -----------------------------------------------------------------------------
def readAndNormalizeNameColumns(reader):

  idColumn = 0
  isbnColumn = 1
  dateColumn = 2
  nameColumn = 3
  nameLookup = {}
  for row in reader:
    nameLookup[utils.getNormalizedString(row[nameColumn])] = (row[idColumn], row[isbnColumn], row[dateColumn], row[nameColumn])

  return nameLookup

# -----------------------------------------------------------------------------
def main():
  """This script reads two CSV files, extracts a name columns and uses an algorithm based on the levenshtein-distance to output possible matches."""

  parser = OptionParser(usage="usage: %prog [options]") 
  parser.add_option('-o', '--output-file', action='store', help='The name of the file to store the possible matches')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.output_file)):
    print("Output file needed!")
    parser.print_help()
    exit(1)
  if( len(args) > 2 ):
    print("Only two files can be compared")
    parser.print_help()
    exit(1) 
  if( len(args) < 2 ):
    print("Two files are needed such that a comparison can be made")
    parser.print_help()
    exit(1)

  with open(args[0], 'r') as f1In,\
       open(args[1], 'r') as f2In,\
       open(options.output_file, 'w') as fOut:

    #inputDelimiter = options.delimiter if options.delimiter else ','
    inputDelimiter = ','

    input1Reader = csv.reader(f1In, delimiter=inputDelimiter)
    input2Reader = csv.reader(f2In, delimiter=inputDelimiter)
    outputWriter = csv.writer(fOut, delimiter=',')

    # skip headers
    next(input1Reader)
    next(input2Reader)
    names1 = readAndNormalizeNameColumns(input1Reader)
    names2 = readAndNormalizeNameColumns(input2Reader)

    numberNames1 = len(names1.keys())
    numberNames2 = len(names2.keys())

    print(f'Successfully read {numberNames1} names from the first file and {numberNames2} names from the second file!')

    (smallerList, biggerList) = utils.getSmallerAndBiggerElement(names1, names2)

    stats = {}
    outputWriter.writerow(['matchType', 'id', 'isbn', 'date', 'matches'])
    for n1 in tqdm(smallerList.keys()):
      matchCandidates = []
      for n2 in biggerList.keys():
        if utils.smallLevenshteinDistanceImproved(stats, n1, n2):
          matchTuple = biggerList[n2]
          matchCandidates.append([matchTuple[0], matchTuple[1], matchTuple[2], matchTuple[3]])

      sourceTuple = smallerList[n1]
      if(len(matchCandidates) == 1):
        matchData = ';'.join(matchCandidates[0])
        outputWriter.writerow(['oneMatch', sourceTuple[0], sourceTuple[1], sourceTuple[2], sourceTuple[3], matchData])
      elif(len(matchCandidates) > 1):
        candidatesList = []
        for c in matchCandidates:
          candidatesList.append(';'.join(c))
        matchData = '\n'.join(candidatesList)
        outputWriter.writerow(['multipleMatches', sourceTuple[0], sourceTuple[1], sourceTuple[2], sourceTuple[3], matchData])

    print(stats)
main()
