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
def getDataprofileRecordFromMARCXML(elem, fieldMapping):
  """This function iterates over the MARC XML record given in 'elem' and creates a dictionary based on MARC fields and the provided 'fieldMapping'.

  >>> getDataprofileRecordFromMARCXML('', {})
  {'hello': 'world'}
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
if __name__ == "__main__":
  import doctest
  doctest.testmod()
