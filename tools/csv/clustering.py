#
# (c) 2023 Sven Lieber
# KBR Brussels
#

import csv
import argparse
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from scipy import sparse
from concurrent.futures import ProcessPoolExecutor
from tools import utils
import uuid
import time

# -----------------------------------------------------------------------------
def main(inputFilename, outputFilename, idColumnName, keyColumnName, delimiter, chunkSize):
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

    # clusterDistanceMatrixParallel(outFile, elementIDs, descriptiveKeys, chunkSize)
    #clusterIterative(elementIDs, descriptiveKeys, outFile)
    clusterInvertedIndex(elementIDs, descriptiveKeys, outFile)

    print("finished")

# -----------------------------------------------------------------------------
def getClusterKeys(elementIDs, descriptiveKeys):
  allKeys = set()
  for element in elementIDs:
    if element in descriptiveKeys:
      allKeys.update(descriptiveKeys[element])
  return allKeys


# -----------------------------------------------------------------------------
def addElementsToCluster(elements, clusterID, clusters, elementToCluster):
  clusters[clusterID].update(elements)
  for element in elements:
    elementToCluster[element] = clusterID

# -----------------------------------------------------------------------------
def clusterInvertedIndex(elementIDs, descriptiveKeys, outFile):

  start_time_index = time.time()
  keysToElements = {}
  for elementID, dKeys in descriptiveKeys.items():
    for dKey in dKeys:
      if dKey in keysToElements:
        keysToElements[dKey].add(elementID)
      else:
        keysToElements[dKey] = set([elementID])

  end_time_index = time.time()
  diffTimeIndex = time.strftime('%H:%M:%S', time.gmtime(end_time_index - start_time_index))
  print(f'Inverted index computed in {diffTimeIndex}')

  start_time_clustering = time.time()
  clusters = {}
  elementToCluster = {}

  for dKey, elementIDs in keysToElements.items():
    existingClusters = set()
    elementsInNoCluster = set()

    for element in elementIDs:
      if element in elementToCluster:
        existingClusters.add(elementToCluster[element])
      else:
        # those have to be added to a cluster
        elementsInNoCluster.add(element)

    if len(existingClusters) == 1:
      # sets have unique members: one or more of the elements are in the same cluster
      if len(elementsInNoCluster) > 0:
        # some of the elements are not yet in the cluster
        clusterID = existingClusters.pop()
        addElementsToCluster(elementsInNoCluster, clusterID, clusters, elementToCluster)
    else:
      newClusterID = str(uuid.uuid4())

      if len(existingClusters) == 0:
        # no existing clusters found, create a new one
        clusters[newClusterID] = elementIDs
        for element in elementIDs:
          elementToCluster[element] = newClusterID

        if len(elementsInNoCluster) > 0:
          addElementsToCluster(elementsInNoCluster, newClusterID, clusters, elementToCluster)

      elif len(existingClusters) > 1:
        # the members are in more than one cluster, so those clusters should be merged
        # 1. get elements of all identified clusters
        combinedElements = set()
        for cluster in existingClusters:
          combinedElements.update(clusters[cluster])
        # 2. remove old clusters
        [clusters.pop(clusterID) for clusterID in existingClusters]
        # 3. add new merged cluster
        clusters[newClusterID] = combinedElements
        # 4. update elementToCluster (overwrite if exists, otherwise create)
        for element in combinedElements:
          elementToCluster[element] = newClusterID

        # 5. now that the new cluster is created we can add eventually clusterless elements
        if len(elementsInNoCluster) > 0:
          addElementsToCluster(elementsInNoCluster, newClusterID, clusters, elementToCluster)

  end_time_clustering = time.time()
  diffTimeClustering = time.strftime('%H:%M:%S', time.gmtime(end_time_clustering - start_time_clustering))
  print(f'Clusters computed in {diffTimeClustering}')

  # write cluster assignment to the output file
  outputWriter = csv.DictWriter(outFile, fieldnames=['elementID', 'clusterID'])
  outputWriter.writeheader()

  for clusterID, memberIDSet in clusters.items():
    for memberID in memberIDSet:
      outputWriter.writerow({'elementID': memberID, 'clusterID': clusterID})
 

# -----------------------------------------------------------------------------
def clusterIterative(elementIDs, descriptiveKeys, outFile):
  initialClusters = {}

  start_time_initial_clusters = time.time()
  for identifier, keys in descriptiveKeys.items():
    clusterID = str(uuid.uuid4())
    initialClusters[clusterID] = set([identifier])

  end_time_initial_clusters = time.time()
  diffTimeInitialClusters = time.strftime('%H:%M:%S', time.gmtime(end_time_initial_clusters - start_time_initial_clusters))
  print(f'Initial clusters computed in {diffTimeInitialClusters}')

  clusterKeys = {}
  start_time_cluster_keys = time.time()
  for identifier, elementIDs in initialClusters.items():
    clusterKeys[identifier] = getClusterKeys(elementIDs, descriptiveKeys)

  end_time_cluster_keys = time.time()
  diffTimeClusterKeys = time.strftime('%H:%M:%S', time.gmtime(end_time_cluster_keys - start_time_cluster_keys))
  print(f'Initial cluster keys lookup data structure computed in {diffTimeClusterKeys}')

  currentClusters = initialClusters
  merged = True

  start_time_clustering = time.time()
  while merged:
    merged = False

    newClusters = {}
    newClusterKeys = {}
    clustersToRemove = []
    for clusterA in currentClusters:
      for clusterB in currentClusters:
        if clusterA != clusterB:
          clusterAKeys = clusterKeys[clusterA]
          clusterBKeys = clusterKeys[clusterB]
          commonKeys = clusterAKeys.intersection(clusterBKeys)
          if commonKeys:
            merged = True
            newClusterID = str(uuid.uuid4())
            newClusters[newClusterID] = currentClusters[clusterA].union(currentClusters[clusterB])
            newClusterKeys[newClusterID] = clusterAKeys.union(clusterBKeys)
            clustersToRemove.append(clusterA)
            clustersToRemove.append(clusterB)
            break
      if merged:
        break

    if merged:
      [currentClusters.pop(key) for key in clustersToRemove] 
      [clusterKeys.pop(key) for key in clustersToRemove]
      currentClusters.update(newClusters)
      clusterKeys.update(newClusterKeys)

  end_time_clustering = time.time()
  diffTimeClustering = time.strftime('%H:%M:%S', time.gmtime(end_time_clustering - start_time_clustering))
  print(f'Initial clusters computed in {diffTimeClustering}')

  # write cluster assignment to the output file
  outputWriter = csv.DictWriter(outFile, fieldnames=['elementID', 'clusterID'])
  outputWriter.writeheader()

  for clusterID, memberIDSet in currentClusters.items():
    for memberID in memberIDSet:
      outputWriter.writerow({'elementID': memberID, 'clusterID': clusterID})


# -----------------------------------------------------------------------------
def clusterDistanceMatrixParallel():

  # compute a N:N distance matrix
  distanceMatrix = computeDistanceMatrixParallel(elementIDs, descriptiveKeys, chunkSize)

  # Perform hierarchical clustering
  clusterLabels = performClustering(distanceMatrix)
  exit(1)

  # write cluster assignment to the output file
  outputWriter = csv.DictWriter(outFile, fieldnames=['elementID', 'clusterID'])
  outputWriter.writeheader()

  for elementIndex, clusterID in enumerate(clusterLabels):
    outputWriter.writerow({'elementID': elementIDs[elementIndex], 'clusterID': clusterID})

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
def computeDistanceMatrixParallel(elementIDs, descriptiveKeys, chunk_size):

    numWorkers = 20
    print(f'Parallel distance matrix computation in chunks of {chunk_size} with {numWorkers} workers')
    start_time = time.time()

    # Create a distance matrix initialized with zeros
    num_elements = len(elementIDs)
    #distance_matrix = np.zeros((num_elements, num_elements), dtype=np.float16)
    distance_matrix = sparse.csr_matrix((num_elements, num_elements), dtype=np.float32)

    # Use ThreadPoolExecutor for parallel processing
    with ProcessPoolExecutor(max_workers=numWorkers) as executor:
        # Compute distances in parallel for chunks of data
        for start_idx in range(0, num_elements, chunk_size):
            chunk_results = []
            chunk_elements = elementIDs[start_idx:start_idx + chunk_size]
            future = executor.submit(compute_distance_chunk, chunk_elements, elementIDs, descriptiveKeys)
            chunk_results.append(future)

           # Fill in the distance matrix using the results for this chunk
            for chunk_idx, result in enumerate(chunk_results):
                distances = result.result()
                for i, distance_row in enumerate(distances):
                    row_idx = start_idx + i
                    distance_matrix[row_idx] = distance_row

    end_time = time.time()
    diffTime = time.strftime('%H:%M:%S', time.gmtime(end_time - start_time))
    print(f'distanceMatrix computed in {diffTime}')

    return distance_matrix



# -----------------------------------------------------------------------------
def compute_distance_chunk(chunk_elements, elementIDs, descriptiveKeys):
    """
    Compute distances between elements in a chunk and all other element IDs using descriptive keys.

    Args:
        chunk_elements (list): List of elements in the chunk.
        elementIDs (list): List of all element IDs.
        descriptiveKeys (dict): Dictionary mapping element IDs to their descriptive keys.

    Returns:
        list: A 2D list where each element represents the negative number of common keys between two elements.

    Example:
    >>> elementIDs = ['A', 'B', 'C', 'D']
    >>> descriptiveKeys = {
    ...     'A': {'key1', 'key2'},
    ...     'B': {'key2', 'key3'},
    ...     'C': {'key4'},
    ...     'D': {'key3'}
    ... }
    >>> chunk_elements = ['A', 'B']
    >>> compute_distance_chunk(chunk_elements, elementIDs, descriptiveKeys)
    [[0, -1, 0, -1], [-1, 0, -1, 0]]

    """
    distances = []
    for element1 in chunk_elements:
        distance_row = []
        for element2 in elementIDs:
            common_keys = descriptiveKeys[element1].intersection(descriptiveKeys[element2])
            distance_row.append(-len(common_keys))
        distances.append(distance_row)
    return distances


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
  parser.add_argument('--chunk-size', action='store', default=500, type=int, help="Optional chunk size for parallelization of distance matrix calculation")
  options = parser.parse_args()

  return options

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  (options) = parseArguments()
  main(options.input_file, options.output_file, options.id_column, options.key_column, options.delimiter, options.chunk_size)
 
