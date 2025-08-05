import unicodedata as ud
from itertools import combinations
import re

def normalizeDelimiters(value, delimiter=';'):
  """This function replaces other found delimiters with the given.
  >>> normalizeDelimiters('Leuven. - Paris')
  'Leuven;Paris'
  >>> normalizeDelimiters('Leuven - Paris')
  'Leuven;Paris'
  >>> normalizeDelimiters('Brussels')
  'Brussels'
  >>> normalizeDelimiters('Sint-Martens-Latem. - Paris')
  'Sint-Martens-Latem;Paris'
  """
  return value.replace('. - ', delimiter).replace(' - ', delimiter)


# -----------------------------------------------------------------------------
def getNormalizedString(s):
  """This function returns a normalized copy of the given string.

  >>> getNormalizedString("HeLlO")
  'hello'
  >>> getNormalizedString("judaïsme, islam, christianisme, ET sectes apparentées")
  'judaisme islam christianisme et sectes apparentees'
  >>> getNormalizedString("chamanisme, de l’Antiquité…)")
  'chamanisme de lantiquite...)'

  >>> getNormalizedString("Abe Ce De ?")
  'abe ce de'
  >>> getNormalizedString("Abe Ce De !")
  'abe ce de'
  >>> getNormalizedString("Abe Ce De :")
  'abe ce de'

  >>> getNormalizedString("A. W. Bruna & zoon")
  'a. w. bruna & zoon'
  >>> getNormalizedString("A.W. Bruna & Zoon")
  'a.w. bruna & zoon'

  """
  noComma = s.replace(',', '')
  noQuestionMark = noComma.replace('?', '')
  noExclamationMark = noQuestionMark.replace('!', '')
  noColon = noExclamationMark.replace(':', '')
  return ud.normalize('NFKD', noColon).encode('ASCII', 'ignore').lower().strip().decode("utf-8")


# -----------------------------------------------------------------------------
def extractStringFromBrackets(value):
  """This function extracts a string in different brackets.
  >>> extractStringFromBrackets('[Brussels]')
  'Brussels'
  >>> extractStringFromBrackets('(Ghent)')
  'Ghent'
  >>> extractStringFromBrackets('Gent')
  'Gent'
  >>> extractStringFromBrackets('')
  ''

  Nothing should be extracted when threre is content before the brackets
  >>> extractStringFromBrackets('Gent (Belgium)')
  'Gent (Belgium)'
  """
  found = None
  if value.startswith('('):
    found = re.search(r'^\((.*)\)', value)
  elif value.startswith('['):
    found = re.search(r'\[(.*)\]', value)
  else:
    return value

  if found:
    return found.group(1)
  else:
    return ''

# -----------------------------------------------------------------------------
def overlappingValues(values):
  """This function returns true if a value of one array element is also part of another array element.
  >>> overlappingValues(['Jan Janssen', 'Janssen, Jan', 'John Doe'])
  True
  >>> data1 = ['John Doe', 'Alice', 'Bob', 'Pascal Renard, ']
  >>> overlappingValues(data1)
  False

  The function returns False if an empty array is given
  >>> overlappingValues([])
  False

  An overlap in the same string should NOT be taken into account
  >>> overlappingValues(['John, John', 'Alice Alice', 'Bob Bobsen'])
  False
  """
  lookup = []

  # first create a lookup list per string
  for value in values:
    lookupValues = set()
    parts = value.replace(',', ' ').split(' ')
    for p in parts:
      namePart = getNormalizedString(p).strip()
      if namePart != '':
        lookupValues.add(namePart)
    lookup.append(lookupValues)

  if len(lookup) == 0:
    return False

  # we have now a list of sets, e.g. [{'jan', 'janssen'}, {'janssen'}, {'doe'}]
  # now compare values across the different lookup lists
  for i in combinations(lookup, 2):
    if i[0].intersection(i[1]):
      return True

  return False

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
