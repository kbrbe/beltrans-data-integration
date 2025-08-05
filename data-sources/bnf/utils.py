import re
from stdnum import isbn
from stdnum import exceptions

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
def preprocessISBNString(inputISBN):
  """This function normalizes a given string to return numbers only.

  >>> preprocessISBNString('978-90-8558-138-3 test')
  '9789085581383'
  >>> preprocessISBNString('9789085581383 test test')
  '9789085581383'
  >>> preprocessISBNString('9031411515')
  '9031411515'
  >>> preprocessISBNString('9791032305690')
  '9791032305690'
  >>> preprocessISBNString('978 90 448 3374')
  '978904483374'
  >>> preprocessISBNString('90 223 1348 4 (Manteau)')
  '9022313484'
  >>> preprocessISBNString('90 223 1348 4 (Manteau 123)')
  '9022313484'
  >>> preprocessISBNString('978-90-303-6744-4 (dl. 1)')
  '9789030367444'
  >>> preprocessISBNString('979-10-235-1393-613')
  '9791023513936'
  >>> preprocessISBNString('90-295-3453-2 (Deel 1)')
  '9029534532'
  >>> preprocessISBNString('I am not a ISBN number')
  ''
  >>> preprocessISBNString('')
  ''
  """

  inputISBNNorm = re.sub(r'[^0-9X]', '', inputISBN)

  if len(inputISBNNorm) == 0:
    return ''
  elif len(inputISBNNorm) == 10:
    return inputISBNNorm
  elif len(inputISBNNorm) == 13:
    if inputISBNNorm.startswith('978') or inputISBNNorm.startswith('979'):
      return inputISBNNorm
    else:
      # it is a wrong ISBN number which happens to have 13 digits
      # Best shot: it probably is a 10 digit ISBN and there were other numbers as part of text
      return inputISBNNorm[:10]
  else:
    if len(inputISBNNorm) > 13:
      return inputISBNNorm[:13]
    elif len(inputISBNNorm) < 13 and len(inputISBNNorm) > 10:
      if inputISBNNorm.startswith('978') or inputISBNNorm.startswith('979'):
        # it is actually a wrong ISBN 13 number, nevertheless return all of it
        return inputISBNNorm
      else:
        # maybe number parts of the text got added by accident to a valid 10 digit ISBN
        return inputISBNNorm[:10]
    else:
      return inputISBNNorm



# -----------------------------------------------------------------------------
def getNormalizedISBN10(inputISBN):
  """This function normalizes an ISBN number.

  >>> getNormalizedISBN10('978-90-8558-138-3')
  '90-8558-138-9'
  >>> getNormalizedISBN10('978-90-8558-138-3 test')
  '90-8558-138-9'
  >>> getNormalizedISBN10('9789085581383')
  '90-8558-138-9'
  >>> getNormalizedISBN10('9031411515')
  '90-314-1151-5'
  >>> getNormalizedISBN10('9791032305690')
  ''
  >>> getNormalizedISBN10('')
  ''
  >>> getNormalizedISBN10('979-10-235-1393-613')
  ''
  >>> getNormalizedISBN10('978-10-235-1393-613')
  Traceback (most recent call last):
   ...
  stdnum.exceptions.InvalidFormat: Not a valid ISBN13.
  """

  inputISBNNorm = preprocessISBNString(inputISBN)

  if inputISBNNorm:
    isbn10 = None
    try:
      isbn10 = isbn.format(isbn.to_isbn10(inputISBNNorm))
      return isbn10
    except exceptions.InvalidComponent:
      # Probably an ISBN number with 979 prefix for which no ISBN10 can be created
      if inputISBNNorm.startswith('979'):
        return ''
      else:
        raise
  else:
    return ''

# -----------------------------------------------------------------------------
def getNormalizedISBN13(inputISBN):
  """This function normalizes an ISBN number.

  >>> getNormalizedISBN13('978-90-8558-138-3')
  '978-90-8558-138-3'
  >>> getNormalizedISBN13('978-90-8558-138-3 test')
  '978-90-8558-138-3'
  >>> getNormalizedISBN13('9789085581383')
  '978-90-8558-138-3'
  >>> getNormalizedISBN13('9031411515')
  '978-90-314-1151-1'
  >>> getNormalizedISBN13('')
  ''
  """

  inputISBNNorm = preprocessISBNString(inputISBN)

  if inputISBNNorm:
    isbn13 = None
    try:
      isbn13 = isbn.format(isbn.to_isbn13(inputISBNNorm))
      return isbn13
    except exceptions.InvalidFormat:
      print(f'Error in ISBN 13 conversion for "{inputISBN}"')
      raise
  else:
    return ''



# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
