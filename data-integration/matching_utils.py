import pandas as pd

def findMatches(row, lookupObject, stats, simAlgorithmNames='ratio', simThresholdNames=0.9, simAlgorithmTitles='ratio', simThresholdTitles=0.9, minTitleMatches=1, valueDelimiter=';'):
  """This function gets one row containing information about a person.
     Based on available columns and the provided lookup object possible matches are searched

     This function assumes a lookupObject with methods nameMatch and
  """

  
  possibleAlgorithms = ['ratio', 'partial_ratio', 'token_sort_ratio', 'token_set_ratio']
  nameMatchFunction = None
  titleMatchFunction = None
  if simAlgorithmNames not in possibleAlgorithms or simAlgorithmTitles not in possibleAlgorithms:
    raise Exception(f'Invalid string comparison algorithm, retrieved simAlgorithmNames={simAlgorithmNames} and simAlgorithmTitles={simAlgorithmTitles}, expected {possibleAlgorithms}')

  contributorName = row['contributorName']

  alternateNames = row['alternateNames'].split(valueDelimiter) if 'alternateNames' in row and row['alternateNames'] != '' else []
  titles = row['titles'].split(valueDelimiter)

  # reduce the search space: look for similar names
  names = [contributorName] + alternateNames
  nameCandidateIDs = set()
  for name in names:
#    print(f'checking "{name}"')
    foundCandidateIDs = lookupObject.nameMatch(name, simAlgorithmNames, simThresholdNames)
#    print(f'found "{foundCandidateIDs}"')
    if foundCandidateIDs:
      if type(foundCandidateIDs) is list:
        nameCandidateIDs.update(foundCandidateIDs)
      else:
        nameCandidateIDs.add(foundCandidateIDs)

  possibleCandidateIDs = set()
  possibleCandidateNames = set()
  discardedCandidateIDs = set()
  discardedCandidateNames = set()

#  print(nameCandidateIDs)
  if not nameCandidateIDs:
    stats['no-name-candidates'] += 1
  else:
    # one or more matching candidates found
    if len(nameCandidateIDs) == 1:
      stats['one-name-candidate'] += 1
    else:
      stats['more-than-one-name-candidate'] += 1
    stats['number-name-candidates'].append(len(nameCandidateIDs))

    # one or more matching candidate(s)
    # thus perform an additional check based on common published book titles
    for cID in nameCandidateIDs:
      matchingTitles = lookupObject.linkedTitlesMatch(cID, titles, simAlgorithmTitles, simThresholdTitles, minTitleMatches)
#      print(matchingTitles)
      if matchingTitles:
        # if matching titles were returned, cID is a possible match
        possibleCandidateIDs.add(cID)
        possibleCandidateNames.update(lookupObject.getNamesByID(cID))
      else:
        # if no matching titles were returned, cID can be discarded
        discardedCandidateIDs.add(cID)
        discardedCandidateNames.update(lookupObject.getNamesByID(cID))
  
  if possibleCandidateIDs:
    if len(possibleCandidateIDs) == 1:
      stats['one-authority-match-via-title'] += 1
    else:
      stats['more-than-one-authority-match-via-title'] += 1

  possibleCandidateIDsString = valueDelimiter.join(possibleCandidateIDs) if possibleCandidateIDs else ''
  possibleCandidateNamesString = valueDelimiter.join(possibleCandidateNames) if possibleCandidateNames else ''
  discardedCandidateIDString = valueDelimiter.join(discardedCandidateIDs) if discardedCandidateIDs else ''
  discardedCandidateNamesString = valueDelimiter.join(discardedCandidateNames) if discardedCandidateNames else ''
  # return a tuple of size 4 of candidate identifiers and names as well as discarded identifiers and names
  # those can be used to populate four pandas dataframe columns when this function is called in an df.apply context
  return pd.Series([possibleCandidateIDsString,possibleCandidateNamesString,discardedCandidateIDString,discardedCandidateNamesString])    
