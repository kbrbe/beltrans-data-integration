#
# (c) 2023 Sven Lieber
# KBR Brussels
#

import csv
import argparse
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from concurrent.futures import ThreadPoolExecutor
from tools import utils
import time

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
    # A sorted list of element identifiers is returned based on the given elementIDs set
    elementIDs = readElements(inputReader, elementIDs, descriptiveKeys, idColumnName, keyColumnName)

    # compute a N:N distance matrix
    distanceMatrix = computeDistanceMatrixParallel(elementIDs, descriptiveKeys)

    # Perform hierarchical clustering
    clusterLabels = performClustering(distanceMatrix)
    exit(1)

    # write cluster assignment to the output file
    outputWriter = csv.DictWriter(outFile, fieldnames=['elementID', 'clusterID'])
    outputWriter.writeheader()

    for elementIndex, clusterID in enumerate(clusterLabels):
      outputWriter.writerow({'elementID': elementIDs[elementIndex], 'clusterID': clusterID})

    print("finished")

# -----------------------------------------------------------------------------
def readElements(inputReader, elementIDs, descriptiveKeys, idColumnName, keyColumnName):

  for row in inputReader:
    eID = row[idColumnName]
    key = row[keyColumnName]

    if eID != '' and key != '':
      elementIDs.add(eID)
      if eID in descriptiveKeys:
        descriptiveKeys[eID].add(key)
      else:
        descriptiveKeys[eID] = set([key])

  return sorted(elementIDs)


# -----------------------------------------------------------------------------
def computeDistanceMatrix(elementIDs, descriptiveKeys):
  """Compute distance matrix based on common descriptive keys"""

  start_time = time.time()
  distanceMatrix = np.zeros((len(elementIDs), len(elementIDs)), dtype=np.float16)
  for i, element1 in enumerate(elementIDs):
      for j, element2 in enumerate(elementIDs):
          commonKeys = descriptiveKeys[element1].intersection(descriptiveKeys[element2])

          # Negative distance for common keys
          distanceMatrix[i, j] = -len(commonKeys)

  end_time = time.time()
  diffTime = time.strftime('%H:%M:%S', time.gmtime(end_time - start_time))
  print(f'distanceMatrix computed in {diffTime}')
  return distanceMatrix

# -----------------------------------------------------------------------------
def computeDistanceMatrixParallel(elementIDs, descriptiveKeys):
    start_time = time.time()
    # Create a distance matrix initialized with zeros
    num_elements = len(elementIDs)
    distanceMatrix = np.zeros((num_elements, num_elements))

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Compute distances in parallel
        futures = []
        for i in range(num_elements):
            for j in range(i, num_elements):
                element1 = elementIDs[i]
                element2 = elementIDs[j]
                common_keys = -len(descriptiveKeys[element1].intersection(descriptiveKeys[element2]))
                futures.append(common_keys)

        # Fill in the distance matrix using the results
        idx = 0
        for i in range(num_elements):
            for j in range(i, num_elements):
                distanceMatrix[i, j] = futures[idx]
                distanceMatrix[j, i] = distanceMatrix[i, j]  # Distance matrix is symmetric
                idx += 1

    end_time = time.time()
    diffTime = time.strftime('%H:%M:%S', time.gmtime(end_time - start_time))
    print(f'distanceMatrix computed in {diffTime}')

    return distanceMatrix



# -----------------------------------------------------------------------------
def performClustering(distanceMatrix):

  start_time = time.time()
  model = AgglomerativeClustering(n_clusters=None, affinity='precomputed', linkage='single', distance_threshold=0)

  # get a list where each index corresponds to an element in elementIDs
  # e.g. [0,2,0,1] the first element is in cluster 0, the second in cluster 2, the third in cluster 0 and the 4th in cluster 1
  clusterLabels = model.fit_predict(distanceMatrix)
  end_time = time.time()
  diffTime = time.strftime('%H:%M:%S', time.gmtime(end_time - start_time))
  print(f'clustering performed in {diffTime}')

  return clusterLabels


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
 
