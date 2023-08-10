from thefuzz import fuzz
import utils_string

# -----------------------------------------------------------------------------
class MatchingLookup():


  # ----------------------------------------------------------------------------
  def __init__(self):

    self.namesByID = {}
    self.titlesByID = {}
    self.idsByName = {}
    self.titlesByName = {}
    self.namesByTitle = {}
    self.idsByTitles = {}

  # ----------------------------------------------------------------------------
  def _addValues(self, theSet, identifier, values):
    """A very generic function that adds values to a given lookup data structure under the single given identifier."""
    if identifier in theSet:
      if type(values) is list:
        theSet[identifier].update(values)
      else:
        theSet[identifier].add(values)
    else:
      if type(values) is list:
        theSet[identifier] = set(values)
      else:
        theSet[identifier] = set([values])

  # --------------------------------------------------------------------------
  def _add(self, var, ids, values):
    """A very generic function that adds values to a given lookup data structure."""
    if type(ids) is list:
      for i in ids:
        self._addValues(var, i, values)
    else:
      self._addValues(var, ids, values)

  # --------------------------------------------------------------------------
  def addLookupRecord(self, identifier, names, titles):

    normalizedNames = []
    for name in names:
      normalizedNames.append(utils_string.getNormalizedString(name))

    normalizedTitles = []
    for title in titles:
      normalizedTitles.append(utils_string.getNormalizedString(title))

    # make it possible to quickly lookup names by person identifier
    self._add(self.namesByID, identifier, normalizedNames)

    # make it possible to quickly lookup titles by person identifier
    self._add(self.titlesByID, identifier, normalizedTitles)

    # make it possible to quickly lookup person identifiers by name
    self._add(self.idsByName, normalizedNames, identifier)

    # make it possible to quickly lookup titles by name
    self._add(self.titlesByName, normalizedNames, normalizedTitles)

    # make it possible to quickly lookup names by titles
    self._add(self.namesByTitle, normalizedTitles, normalizedNames)

    # make it possible to quickly lookup person identifiers by titles
    self._add(self.idsByTitles, normalizedTitles, identifier)

  # --------------------------------------------------------------------------
  def nameMatch(self, name, algorithm, similarityThreshold):
    """
    """
    possibleAlgorithms = ['ratio', 'partial_ratio', 'token_sort_ratio', 'token_set_ratio']

    if algorithm not in possibleAlgorithms:
      raise Exception(f'Invalid string comparison algorithm "{simAlgorithmNames}", expected one of {possibleAlgorithms}')

    normalizedName = utils_string.getNormalizedString(name)
    candidates = set()
    for storedName in self.titlesByName.keys():
      matchingFunction = getattr(fuzz, algorithm)
      result = matchingFunction(normalizedName, storedName)
      if result >= similarityThreshold:
        candidates.update(self.idsByName[storedName])

    # if the set is empty, the list will be empty
    # a calling function can check if the result is true (list has values) or false (list has no values)
    return list(candidates)




  # --------------------------------------------------------------------------
  def linkedTitlesMatch(self, personID, titles, algorithm, similarityThreshold, minTitleMatches):
    """This function checks how many of the given titles match with the titles of the given person identifier."""

    if personID not in self.titlesByID:
      raise Exception(f'No titles stored for person with ID "{personID}"')

    matchingTitles = set()
    for title in titles:
      normalizedTitle = utils_string.getNormalizedString(title)
      storedTitles = self.titlesByID[personID]
      for storedTitle in storedTitles:
#        print(f'compare "{normalizedTitle}" with "{storedTitle}"')
        matchingFunction = getattr(fuzz, algorithm)
        result = matchingFunction(normalizedTitle, storedTitle)
#        print(f'result is {result} (bigger than {similarityThreshold}?')
        if result >= similarityThreshold:
#          print(f'yes! bigger')
          matchingTitles.add(storedTitle)
          # one of the given titles only need to match against one of the stored ones, thus we can stop comparing
          # important is how many of the given titles match with AT LEAST one (outer loop)
          break

    if len(matchingTitles) <= minTitleMatches:
      return list(matchingTitles)
    else:
      return None

  # --------------------------------------------------------------------------
  def getNamesByID(self, personIdentifier):
    if personIdentifier in self.namesByID:
      return self.namesByID[personIdentifier]
    else:
      raise Exception(f'No names stored for person identifier "{personIdentifier}"')


# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
