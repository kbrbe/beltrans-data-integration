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
def subtitleStopwordRemoval(s):
  """This function removes words from the stopword list from the given string

  >>> normalizedTitle = getNormalizedString('Mijn boek : roman')
  >>> subtitleStopwordRemoval(normalizedTitle)
  'mijn boek'

  >>> normalizedTitle = getNormalizedString('Mijn boek : [roman]')
  >>> subtitleStopwordRemoval(normalizedTitle)
  'mijn boek'

  """
  stopwords = ['roman', '[roman]','verhalen', 'poemes', '[poemes]']

  filteredString = s
  for sw in stopwords:
    if s.endswith(sw):
      filteredString = filteredString.replace(sw, '')
  return filteredString.strip()

# -----------------------------------------------------------------------------
def getNormalizedString(s):
  """This function returns a normalized copy of the given string.

  >>> getNormalizedString("HeLlO")
  'hello'
  >>> getNormalizedString("judaïsme, islam, christianisme, ET sectes apparentées")
  'judaisme islam christianisme et sectes apparentees'
  >>> getNormalizedString("chamanisme, de l’Antiquité…)")
  'chamanisme de lantiquite)'

  >>> getNormalizedString("Abe Ce De ?")
  'abe ce de'
  >>> getNormalizedString("Abe Ce De !")
  'abe ce de'
  >>> getNormalizedString("Abe Ce De :")
  'abe ce de'

  >>> getNormalizedString("les soins palliatifs : éthique et témoignage")
  'les soins palliatifs ethique et temoignage'

  >>> getNormalizedString("978-2-87386-027-1")
  '978-2-87386-027-1'

  >>> getNormalizedString("A. W. Bruna & zoon")
  'a. w. bruna & zoon'
  >>> getNormalizedString("A.W. Bruna & Zoon")
  'a.w. bruna & zoon'

  """
  charReplacements = {
    ',': '',
    '?': '',
    '!': '',
    ':': '',
    ';': ''
  }

  # by the way: only after asci normalization the UTF character for ... becomes ...
  asciiNormalized = ud.normalize('NFKD', s).encode('ASCII', 'ignore').lower().strip().decode("utf-8")

  normalized = ''.join([charReplacements.get(char, char) for char in asciiNormalized])
  noDots = normalized.replace('...', '')
  # remove double whitespaces using trick from stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string
  return " ".join(noDots.split())
  


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
def overlappingValues(values):
  """This function returns true if a value of one array element is also part of another array element.
  >>> data = ['Jan Janssen', 'Janssen, Jan', 'John Doe']
  >>> overlappingValues(data)
  True
  >>> data1 = ['John Doe', 'Alice', 'Bob', 'Pascal Renard, ']
  >>> overlappingValues(data1)
  False

  The function returns False if an empty array is given
  >>> overlappingValues([])
  False
  """
  lookup = {}
  for value in values:
    parts = value.replace(',', ' ').split(' ')
    for p in parts:
      namePart = getNormalizedString(p).strip()
      if namePart != '':
        if namePart in lookup:
          lookup[namePart] = True
        else:
          lookup[namePart] = False

  if True in lookup.values():
    return True
  else:
    return False

# -----------------------------------------------------------------------------
def getUniqueName(dictionary, columns, delimiter=' '):
  """This function returns the string normalized value of the given column or columns.

  It works with a single column
  >>> getUniqueName({'myCol': 'HElLo'}, ['myCol'])
  'hello'

  Or if multiple columns are given
  >>> getUniqueName({'myCol1': 'HElLo', 'myCol2': 'woRLd'}, ['myCol1', 'myCol2'])
  'hello world'
  """
  values = [ dictionary.get(key).strip() for key in columns ]
  valueString = delimiter.join(values)
  return getNormalizedString(valueString)



# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
