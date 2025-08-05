from stdnum import isbn, exceptions
import re

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



