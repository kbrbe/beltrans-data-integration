import utils_string
from itertools import combinations

# -----------------------------------------------------------------------------
class ContributorLookup():

  # ---------------------------------------------------------------------------
  def __init__(self, integratedIdentifierDelimiter=':', localIdentifierDelimiter=','):
    self.contributors = {}
    self.possibleMatches = []
    self.correlations = []
    self.localIdentifierNames = set()

    self.integratedIdentifierDelimiter = integratedIdentifierDelimiter
    self.localIdentifierDelimiter = localIdentifierDelimiter

  # ---------------------------------------------------------------------------
  def addContributor(self, contributorString):
    """This method extracts contributor data from the given string.
    >>> c = ContributorLookup()
    >>> c.addContributor("Sven Lieber (int123: 123, cb123, p123)")
    'int123'
    >>> dict(sorted(c.getContributor('int123').items()))
    {'BnF': 'cb123', 'KBR': '123', 'NTA': 'p123', 'name': 'Sven Lieber'}
    """

    # split name from the list of identifiers
    # we use rpartition instead of split,
    # because the name might include a bracket too,
    # example: "Davidsfonds (Leuven) (1234: kbr123, bnf123)"
    nameIDParts = contributorString.rpartition('(')
    contributorName = nameIDParts[0].strip()

    # split the unique identifier from the local identifiers
    # nameIDParts[1] is the delimiter itself
    identifiersString = nameIDParts[2].split(')')[0]

    identifierParts = identifiersString.split(self.integratedIdentifierDelimiter)

    # get the unique identifier
    contributorID = identifierParts[0].strip()
    localIdentifiers = identifierParts[1]

    localIdentifierParts = localIdentifiers.split(self.localIdentifierDelimiter)

    # add the local identifiers if we have not yet seen this contributor
    if contributorID not in self.contributors:
      self.contributors[contributorID] = {'name': contributorName}

      for localIdentifier in localIdentifierParts:
        localIdentifier = localIdentifier.strip()
        if localIdentifier.startswith('cb'):
          self.localIdentifierNames.add('BnF')
          self.contributors[contributorID]['BnF'] = localIdentifier
        elif localIdentifier.startswith('p'):
          self.localIdentifierNames.add('NTA')
          self.contributors[contributorID]['NTA'] = localIdentifier
        elif localIdentifier.startswith('u'):
          self.localIdentifierNames.add('Unesco')
          self.contributors[contributorID]['Unesco'] = localIdentifier
        else:
          self.localIdentifierNames.add('KBR')
          self.contributors[contributorID]['KBR'] = localIdentifier

    return contributorID
    
  # ---------------------------------------------------------------------------
  def computePossibleMatches(self, contributorIdentifiers):
    """This method takes a list of contributor identifiers and returns a set with the contributor identifiers who share at least one normalized name component.
    >>> c = ContributorLookup()

    Add the first author with unique identifier int123 who has a KBR and a BnF identifier
    >>> c.addContributor("Sven Lieber (int123: 123, cb123)")
    'int123'

    Add a second author with unique identifier int456 who has a Unesco identifier
    >>> c.addContributor("Lieber, Sven (int456: u123)")
    'int456'

    Add more authors ...
    >>> c.addContributor("John Johnsson (int789: 789, cb789)")
    'int789'

    >>> c.addContributor("Lieber, S. (int10: p10)")
    'int10'

    The call to this method determines that all three Sven's might be the same
    >>> sorted(c.computePossibleMatches(['int123', 'int456', 'int789', 'int10']))
    ['int10', 'int123', 'int456']
    """ 

    # create a lookup list with the contributor ID as key
    # and a set of normalized name components as values
    lookup = {}
    for cID in contributorIdentifiers:
      lookupValues = set()
      if cID in self.contributors:
        parts = self.contributors[cID]['name'].replace(',', ' ' ).split(' ')
        for p in parts:
          namePart = utils_string.getNormalizedString(p).strip()
          if namePart != '':
            lookupValues.add(namePart)
        lookup[cID] = lookupValues

    # determine possible contributor overlap
    # by performing an intersection between the name components:
    # if at least one of the components overlap, add it to the result set
    possibleMatch = set()
    for i in combinations(lookup, 2):
      if set.intersection(lookup[i[0]], lookup[i[1]]):
        possibleMatch.add(i[0])
        possibleMatch.add(i[1])

    self.possibleMatches.append(possibleMatch)
    return possibleMatch

  # ---------------------------------------------------------------------------
  def computeCorrelations(self):
    """This method creates a list of unique sets with all found correlations by looping over possible matches.
    >>> c = ContributorLookup()

    Some sets are indirectly linked because they share an identifier.
    This function aims to link those sets and return the minimum set of correlations
    >>> c.possibleMatches = [{'123', '456'}, {'123', '789'}, {'456', '789'}, {'789', '10'}, {'111', '222'}, {'1', '3'}, {'3', '4'}]
    >>> c.computeCorrelations()
    >>> [sorted(s) for s in c.correlations]
    [['10', '123', '456', '789'], ['111', '222'], ['1', '3', '4']]
    """

    matchesDictionary = {}

    # create a dictionary with contributor identifiers as key
    # and all direct found matches as value represented as a set
    # (this set also contains the contributor ID of the key)
    # For example: {'123': {'456', '123', '789'}
    for possibleMatchSet in self.possibleMatches:
      for contID in possibleMatchSet:
        if contID in matchesDictionary:
          matchesDictionary[contID].update(possibleMatchSet)
        else:
          matchesDictionary[contID] = possibleMatchSet

    # create unique sets of contributor identifiers
    # which are also linked indirectly
    alreadyProcessed = set()
    for cID in matchesDictionary:

      # if the current ID was already processed as value of another cID
      # we do not need to process it again, it will already be part of the output
      if cID in alreadyProcessed:
        continue

      # fetch all matches of all the identifiers in the current set
      # the current cID is also part of its values, so no need to add it separately
      currentMatchSet = matchesDictionary[cID]
      relatedMatches = set()
      for matchID in currentMatchSet:
        alreadyProcessed.add(matchID)
        relatedMatches.add(matchID)

        # for each possibleMatch identifier, get its possible matches
        if matchID in matchesDictionary:
          otherMatchSet = matchesDictionary[matchID]
          alreadyProcessed.update(otherMatchSet)
          relatedMatches.update(otherMatchSet)

      self.correlations.append(relatedMatches)

  # ---------------------------------------------------------------------------
  def getCorrelationsLocalIdentifiers(self):
    """This method computes correlation based on possible matches and returns linked local identifiers.
    >>> c = ContributorLookup()

    Add the first author with unique identifier int123 who has a KBR and a BnF identifier
    >>> c.addContributor("Sven Lieber (int123: 123, cb123)")
    'int123'

    Add a second author with unique identifier int456 who has a Unesco identifier
    >>> c.addContributor("Lieber, Sven (int456: u123)")
    'int456'

    Add more authors ...
    >>> c.addContributor("John Johnsson (int789: 789, cb789)")
    'int789'

    >>> c.addContributor("Lieber, S. (int10: 123x, p10)")
    'int10'

    Imagine we have seen the following 4 authors for the same publication, check the overlap
    >>> sorted(c.computePossibleMatches(['int123', 'int456', 'int789', 'int10']))
    ['int10', 'int123', 'int456']

    Get the first item which is returned by this generator function
    >>> dict(sorted(next(c.getCorrelationsLocalIdentifiers()).items()))
    {'BnF': 'cb123', 'KBR': '123;123x', 'NTA': 'p10', 'Unesco': 'u123'}
    """

    # first compute correlations which will be stored in self.correlations
    self.computeCorrelations()

    for correlationSet in self.correlations:
      outputRow = {}
      localIdentifiers = {}
      for cID in correlationSet:
        if cID in self.contributors:
          currentLocalIdentifiers = self.contributors[cID]
          #currentLocalIdentifiers = {key: value for key, value in self.contributors[cID].items() if key != 'name'}

          # merge current local identifiers to the rest
          # we do not simply use the dictionary update method, 
          # because we do not want to overwrite possible already existing identifiers
          # but add others of the same type using a semicolon
          for l in currentLocalIdentifiers:
            if l in localIdentifiers:
              # create a sorted list of identifiers from this type
              # serialized as a semicolon-separated list
              currentValue = localIdentifiers[l]
              newValue = [currentValue] + currentLocalIdentifiers[l].split(';')
              localIdentifiers[l] = ';'.join(sorted(newValue))
            else:
              localIdentifiers[l] = currentLocalIdentifiers[l]
      yield localIdentifiers

  # ---------------------------------------------------------------------------
  def getContributor(self, contributorID):
    if contributorID in self.contributors:
      return self.contributors[contributorID]
    else:
      return None

  # ---------------------------------------------------------------------------
  def getLocalIdentifierNames(self):
    return list(self.localIdentifierNames)

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
