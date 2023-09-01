#
# (c) 2023 Sven Lieber
# KBR Brussels
#

import csv
import argparse
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from tools import utils

# -----------------------------------------------------------------------------
def main(inputFilename, outputFilename, idColumnName, keyColumnName, delimiter):
  """This script performs the hierarchical clustering algorithm sklearn.cluster.AgglomerativeClustering
     on the input based on common descriptive keys."""

  with open(inputFilename, 'r') as inFile, \
       open(outputFilename, 'w') as outFile:

    inputReader = csv.DictReader(inFile, delimiter=delimiter)
    utils.checkIfColumnsExist(inputReader.fieldnames, [idColumnName, keyColumnName])

    elementIDs = set()
    descriptiveKeys = {}

    # Populate the two data structures above with values from the input file
    readElements(inputReader, elementIDs, descriptiveKeys)

    # compute a N:N distance matrix
    distanceMatrix = computeDistanceMatrix(elementIDs, descriptiveKeys)

    # Perform hierarchical clustering
    clusterLabels = performClustering(distanceMatrix)

    # write cluster assignment to the output file
    outputWriter = csv.DictWriter(fOut, fieldnames=['elementID', 'clusterID'])

    for elementIndex, clusterID in enumerate(clusterLabels):
      outputWriter.writerow({'elementID': elementIDs[elementIndex], 'clusterID': clusterID})

    print("finished")

# -----------------------------------------------------------------------------
def readElements(inputReader, elementIDs, descriptiveKeys):

  for row in inputReader:
    eID = row[idColumnName]
    key = row[keyColumnName]

    if eID != '' and key != '':
      elementIDs.add(eID)
      if eID in descriptiveKeys:
        descriptiveKeys[eID].add(key)
      else:
        descriptiveKeys[eID] = set([key])

  elementIDs = sorted(elementIDs)


# -----------------------------------------------------------------------------
def computeDistanceMatrix(elementIDs, descriptiveKeys):
  """Compute distance matrix based on common descriptive keys"""
  distanceMatrix = np.zeros((len(elementIDs), len(elementIDs)))
  for i, element1 in enumerate(elementIDs):
      for j, element2 in enumerate(elementIDs):
          commonKeys = descriptiveKeys[element1].intersection(descriptiveKeys[element2])

          # Negative distance for common keys
          distanceMatrix[i, j] = -len(commonKeys)

  return distanceMatrix


# -----------------------------------------------------------------------------
def performClustering(distanceMatrix):

  model = AgglomerativeClustering(n_clusters=None, affinity='precomputed', linkage='single', distance_threshold=0)

  # get a list where each index corresponds to an element in elementIDs
  # e.g. [0,2,0,1] the first element is in cluster 0, the second in cluster 2, the third in cluster 0 and the 4th in cluster 1
  return model.fit_predict(distance_matrix)


# -----------------------------------------------------------------------------
def parseArguments():

  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input-file', action='store', required=True, help="The CSV file with columns for elements and descriptive keys, one row is one element and descriptive key relationship")
  parser.add_argument('-o', '--output-file', action='store', required=True, help='The name of the output CSV file containing two columns: elementID and clusterID')
  parser.add_argument('--id-column', action='store', required=True, help='The name of the column with element identifiers')
  parser.add_argument('--key-column', action='store', required=True, help="The name of the column that contains a descriptive key")
  parser.add_argument('--delimiter', action='store', default=',', help="Optional delimiter of the input/output CSV, default is ','")
  options = parser.parse_args()

  return options

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  (options) = parseArguments()
  main(options.input_file, options.output_file, options.id_column, options.key_column, options.delimiter)
 
