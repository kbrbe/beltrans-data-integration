import unicodedata as ud
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
    found = re.search('^\((.*)\)', value)
  elif value.startswith('['):
    found = re.search('\[(.*)\]', value)
  else:
    return value

  if found:
    return found.group(1)
  else:
    return ''

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
