from datetime import datetime
import xml.etree.ElementTree as ET

# -----------------------------------------------------------------------------
def parseYear(year, patterns):
  """"This function returns a string representing a year based on the input and a list of possible patterns.

  >>> parseYear('2021', ['%Y'])
  '2021'
  >>> parseYear('2021', ['(%Y)', '%Y'])
  '2021'
  >>> parseYear('(2021)', ['%Y', '(%Y)'])
  '2021'
  """

  parsedYear = None
  for p in patterns:

    try:
      tmp = datetime.strptime(year, p).date().year
      parsedYear = str(tmp)
      break
    except ValueError:
      pass

  if parsedYear == None:
    return year
  else:
    return parsedYear

# -----------------------------------------------------------------------------
def parseDate(date, patterns):
  """"This function returns a string representing a date based on the input and a list of possible patterns.

  >>> parseDate('2021', ['%Y'])
  '2021'
  >>> parseDate('2021', ['(%Y)', '%Y'])
  '2021'
  >>> parseDate('(2021)', ['%Y', '(%Y)'])
  '2021'

  A correct date string for a correct input.
  >>> parseDate('1988-04-25', ['%Y-%m-%d'])
  '1988-04-25'

  A correct date string for dates with slash.
  >>> parseDate('25/04/1988', ['%Y-%m-%d', '%Y/%m/%d', '%Y/%m/%d', '%d/%m/%Y'])
  '1988-04-25'

  An empty value if the pattern is not found.
  >>> parseDate('25/04/1988', ['%Y-%m-%d', '%Y/%m/%d'])
  ''

  A correct date string for dates without delimiter.
  >>> parseDate('19880425', ['%Y-%m-%d', '%Y%m%d'])
  '1988-04-25'

  Only year and month are invalid.
  >>> parseDate('1988-04', ['%Y%m', '%Y-%m'])
  ''
  >>> parseDate('198804', ['%Y-%m', '%Y%m'])
  ''

  Keep year if this is the only provided information.
  >>> parseDate('1988', ['%Y-%m-%d', '%Y'])
  '1988'

  Keep year if it is in round or square brackets or has a trailing dot.
  >>> parseDate('[1988]', ['%Y', '[%Y]'])
  '1988'
  >>> parseDate('(1988)', ['(%Y)'])
  '1988'
  >>> parseDate('1988.', ['%Y', '%Y.'])
  '1988'


  """

  parsedDate = None
  for p in patterns:

    try:
      # try if the value is a year
      tmp = datetime.strptime(date, p).date()
      if len(date) == 4:
        parsedDate = str(tmp.year)
      elif len(date) > 4 and len(date) <= 7:
        if any(ele in date for ele in ['(', '[', ')', ']', '.']):
          parsedDate = str(tmp.year)
        else:
          parsedDate = ''
      else:
        parsedDate = str(tmp)
      break
    except ValueError:
      pass

  if parsedDate == None:
    return ''
  else:
    return parsedDate




# -----------------------------------------------------------------------------
def getDataprofileRecordFromMARCXML(elem, fieldMapping):
  """This function iterates over the MARC XML record given in 'elem' and creates a dictionary based on MARC fields and the provided 'fieldMapping'.

  >>> getDataprofileRecordFromMARCXML('', {})
  """
  for df in elem:
    if(df.tag == EQ.QName(NS_MARCSLIM, 'controlfield')):
      pass
    if(df.tag == EQ.QName(NS_MARCSLIM, 'datafield')):
      tagNumber = df.attrib['tag']
      if(tagNumber == '020'):
        pass
      elif(tagNumber == '041'):
        pass
      elif(tagNumber == '044'):
        pass
      elif(tagNumber == '245'):
        pass
      elif(tagNumber == '250'):
        pass
      elif(tagNumber == '264'):
        pass
      elif(tagNumber == '300'):
        pass
      elif(tagNumber == '700'):
        pass
      elif(tagNumber == '710'):
        pass
      elif(tagNumber == '765'):
        pass
      elif(tagNumber == '773'):
        pass
      elif(tagNumber == '775'):
        pass
      elif(tagNumber == '911'):
        pass
      elif(tagNumber == '944'):
        pass


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
def extractNameComponents(value):
  """This function tries to extract a family name and a last name from the input and returns them as a tuple.

  >>> extractNameComponents('Lieber, Sven')
  ('Lieber', 'Sven')
  >>> extractNameComponents('van Gogh, Vincent')
  ('van Gogh', 'Vincent')

  Empty strings are returned if it did not work. If there is only one value, we assume the family name
  >>> extractNameComponents('')
  ('', '')
  >>> extractNameComponents('van Gogh')
  ('van Gogh', '')
  >>> extractNameComponents('Hermann')
  ('Hermann', '')
  """
  familyName = ''
  givenName = ''

  if value != '':
  
    components = value.split(',')
    if len(components) == 0:
      familyName = value
    elif len(components) == 1:
      familyName = components[0].strip()
    elif len(components) > 1:
      familyName = components[0].strip()
      givenName = components[1].strip()
 
  return (familyName, givenName) 


# -----------------------------------------------------------------------------
def extractIdentifier(rowID, value, pattern):
  """Extracts the digits of an identifier in column 'col' if it starts with 'pattern'.

  >>> extractIdentifier('1', 'ISNI 0000 0000 0000 1234', 'ISNI')
  '0000000000001234'
  >>> extractIdentifier('1', 'ISNI --', 'ISNI')
  ''
  >>> extractIdentifier('1', 'ISNI ?', 'ISNI')
  ''
  >>> extractIdentifier('1', 'VIAF --', 'VIAF')
  ''
  >>> extractIdentifier('1', '1234', 'ISNI')
  ''
  >>> extractIdentifier('1', 'VIAF 1234', 'VIAF')
  '1234'
  >>> extractIdentifier('1', '', 'ISNI')
  ''
  >>> extractIdentifier('1', 'ISNI 0000 0000 0000 1234 5678', 'ISNI')
  ''
  >>> extractIdentifier('1', 1234, 'ISNI')
  ''
  """

  identifier = ''

  if( isinstance(value, str) ):

    if(str.startswith(value, pattern) and not str.endswith(value, '-') and not '?' in value):
      # remove the prefix (e.g. VIAF or ISNI) and replace spaces (e.g. '0000 0000 1234')
      tmp = value.replace(pattern, '')
      #identifier = value.replace(pattern, '').replace(' ', '')
      identifier = tmp.replace(' ', '')

      if(pattern == 'ISNI' and len(identifier) == 32):
        print("Several ISNI numbers (?) for '" + rowID + ": '" + identifier + "'")
        identifier = identifier[0:16]

  if pattern == 'ISNI':
    if len(identifier) != 16:
      return ''
    else:
      return str(identifier)
  else:
    return str(identifier)



# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
