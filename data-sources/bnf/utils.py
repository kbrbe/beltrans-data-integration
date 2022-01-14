
# -----------------------------------------------------------------------------
def count(stats, counter):
  """ This function simply adds to the given counter or creates it if not yet existing in 'stats'.

  >>> stats = {}
  >>> count(stats, 'myCounter')
  >>> stats['myCounter']
  1
  """
  if counter in stats:
    stats[counter] += 1
  else:
    stats[counter] = 1

# -----------------------------------------------------------------------------
def countStat(stats, counter, value):
  """ This function logs the value 'value' in the dictionary 'stats' under the key 'counter'. Additionally min, max and number are stored.

  An empty stats dictionary is filled.
  >>> stats = {}
  >>> countStat(stats, 'myCounter', 1)
  >>> stats['myCounter']
  {'min': 1.0, 'max': 1.0, 'avg': 1.0, 'number': 1, 'values': [1.0]}

  Stats are correctly computed and added for already existing counters.
  >>> stats =  { 'myCounter': {'min': 1.0, 'max': 3.0, 'avg': 2, 'number': 3, 'values': [1.0, 2.0, 3.0]}}
  >>> countStat(stats, 'myCounter', 7)
  >>> stats['myCounter']
  {'min': 1.0, 'max': 7.0, 'avg': 3.25, 'number': 4, 'values': [1.0, 2.0, 3.0, 7.0]}
  """
  value = float(value)
  if counter in stats:
    stats[counter]['values'].append(value)
    stats[counter]['number'] += 1
    stats[counter]['min'] = min(stats[counter]['min'], value)
    stats[counter]['max'] = max(stats[counter]['max'], value)
    stats[counter]['avg'] = sum(stats[counter]['values'])/len(stats[counter]['values'])
  else:
    stats[counter] = {'min': value, 'max': value, 'avg': value, 'number': 1, 'values': [value]}


# -----------------------------------------------------------------------------
def getElementValue(elem, sep=';'):
  """This function returns the value of the element if it is not None, otherwise an empty string.

  The function returns the 'text' value if there is one
  >>> class Test: text = 'hello'
  >>> obj = Test()
  >>> getElementValue(obj)
  'hello'

  It returns nothing if there is no text value
  >>> class Test: pass
  >>> obj = Test()
  >>> getElementValue(obj)
  ''

  And the function returns a semicolon separated list in case the argument is a list of objects with a 'text' attribute
  >>> class Test: text = 'hello'
  >>> obj1 = Test()
  >>> obj2 = Test()
  >>> getElementValue([obj1,obj2])
  'hello;hello'
  """
  if elem is not None:
    if isinstance(elem, list):
      valueList = list()
      for e in elem:
        if hasattr(e, 'text'):
          valueList.append(e.text)
      return ';'.join(valueList)
    else:
      if hasattr(elem, 'text'):
        return elem.text
  
  return ''

# -----------------------------------------------------------------------------
def extractBnFIdentifier(uri):
  """This function extracts the numerical identifier of a BnF URI.
  >>> extractBnFIdentifier("http://data.bnf.fr/ark:/12148/cb39863687h#Expression")
  'cb39863687h'

  >>> extractBnFIdentifier("http://data.bnf.fr/ark:/12148/cb39863687h#about")
  'cb39863687h'

  >>> extractBnFIdentifier("http://data.bnf.fr/ark:/12148/cb39863687h")
  'cb39863687h'

  >>> extractBnFIdentifier("cb39863687h")
  'cb39863687h'

  >>> extractBnFIdentifier("http://catalogue.bnf.fr/ark:/12148/cb41449389q | ISBN 9782092523636 | ")
  'cb41449389q'
  """
  uriPart = uri.split(' ')[0]
  lastPart = uriPart.split('/')[-1]
  return lastPart.split('#')[0]

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
