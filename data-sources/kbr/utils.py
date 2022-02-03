from datetime import datetime
import xml.etree.ElementTree as ET
import unicodedata as ud
import enchant
import re
from stdnum import isbn
from stdnum import exceptions

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
def count(stats, counter, val=None, valueDict=None):
  """ This function simply adds to the given counter or creates it if not yet existing in 'stats'
      If the optional 'val' argument is given, the val is also logged in a set.

  >>> stats = {}
  >>> count(stats, 'myCounter')
  >>> stats['myCounter']
  1
  """
  if counter in stats:
    stats[counter] += 1
  else:
    stats[counter] = 1

  if val is not None:
      if counter in valueDict:
        valueDict[counter].add(val) 
      else:
        valueDict[counter] = set([val])



# -----------------------------------------------------------------------------
def compareStrings(s1, s2):
  """This function normalizes both strings and compares them. It returns true if it matches, false if not.

  >>> compareStrings("HeLlO", "Hello")
  True
  >>> compareStrings("judaïsme, islam, christianisme, ET sectes apparentées", "judaisme, islam, christianisme, et sectes apparentees")
  True
  >>> compareStrings("chamanisme, de l’Antiquité…)", "chamanisme, de lAntiquite...)")
  True
  """

  nS1 = getNormalizedString(s1)
  nS2 = getNormalizedString(s2)

  if(nS1 == nS2):
    return True
  else:
    return False

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
  """
  noComma = s.replace(',', '')
  noQuestionMark = noComma.replace('?', '')
  noExclamationMark = noQuestionMark.replace('!', '')
  noColon = noExclamationMark.replace(':', '')
  return ud.normalize('NFKD', noColon).encode('ASCII', 'ignore').lower().strip().decode("utf-8")


# -----------------------------------------------------------------------------
def smallLevenshteinInList(str1, wordList):
  """This function checks the levensthein distance of str1 to each of the words
     in the given wordList. As soon as one word has a very little distance,
     consider it a match and return True.

  >>> smallLevenshteinInList('balon', ['ballon', 'media'])
  True
  """

  retVal = False

  for word in wordList:
    lsDist = enchant.utils.levenshtein(str1, word)
    if(lsDist == 1):
      retVal = True

  return retVal

# -----------------------------------------------------------------------------
def smallLevenshteinBetweenLists(wordList1, wordList2):
  """This function checks the levenshtein distances between the two word lists.
  It considers a match if the words of the smaller list all match with distance 0 or 1 with
  a word of the longer list.

  >>> smallLevenshteinBetweenLists(['bauwens', 'noella'], ['noella', 'bauwens'])
  True
  >>> smallLevenshteinBetweenLists(['one', 'two', 'three'], ['three', 'two', 'one'])
  True
  >>> smallLevenshteinBetweenLists(['one', 'two', 'three'], ['two', 'one', 'three'])
  True
  >>> smallLevenshteinBetweenLists(['one', 'two', 'three', 'four', 'five'], ['two', 'one', 'three'])
  True
  >>> smallLevenshteinBetweenLists(['one', 'two', 'thrae', 'foor', 'five'], ['two', 'one', 'three'])
  True
  >>> smallLevenshteinBetweenLists(['one', 'two', 'one', 'thrae', 'foor', 'two', 'five'], ['two', 'one', 'three'])
  True

  >>> smallLevenshteinBetweenLists(['five', 'six', 'seven'], ['two', 'one', 'three'])
  False
  >>> smallLevenshteinBetweenLists(['five', 'six', 'seven', 'eight', 'nine'], ['two', 'one', 'three'])
  False
  """

  #
  # check which list is smaller
  # so we know for how many 0 or 1 levenshtein numbers we have to look
  #smallerListLen = min(len(wordList1), len(wordList2))

  #distances = list()
  #for w1 in wordList1:
  #  for w2 in wordList2:
  #    distances.append(enchant.utils.levenshtein(w1, w2))

  #smallDistanceCounter = 0
  #for d in distances:
  #  if d < 2:
  #    smallDistanceCounter += 1

  #
  # If the items of the smaller list occured one or more times in the longer list (with slight variation)
  # we consider it a match
  #if(smallDistanceCounter >= smallerListLen):
  #  return True
  #else:
  #  return False

  smallerList = None
  biggerList = None


  (smallerList, biggerList) = getSmallerAndBiggerElement(wordList1, wordList2)

  for w1 in smallerList:
    similarMatchFound = False
    for w2 in biggerList:
      # at least one of the shorter list's words is not part of the larger list
      if enchant.utils.levenshtein(w1,w2) < 2:
        similarMatchFound = True
    if not similarMatchFound:
      return False
  
  return True

# -----------------------------------------------------------------------------
def getSmallerAndBiggerElement(element1, element2):
  """Returning a tuple of smaller and bigger element, if the same length the first is listed first.
  >>> getSmallerAndBiggerElement([1,2], [3,4])
  ([1, 2], [3, 4])

  >>> getSmallerAndBiggerElement([1,2,3], [3,4])
  ([3, 4], [1, 2, 3])

  >>> getSmallerAndBiggerElement([1,2], [3,4,5])
  ([1, 2], [3, 4, 5])
  """
  smallerList = None
  biggerList = None
  if len(element1) == len(element2):
    smallerList = element1
    biggerList = element2
  elif len(element1) > len(element2):
    smallerList = element2
    biggerList = element1
  else:
    smallerList = element1
    biggerList = element2

  return (smallerList, biggerList)

# -----------------------------------------------------------------------------
def smallLevenshteinDistance(stats, str1, str2):
  """This function checks both strings with respect to their levenshtein distance, checking also substrings.

  >>> smallLevenshteinDistance({}, 'koninklijke bibliotheek albert i', 'koninklijke bibliotheek van belgie')
  True
  >>> smallLevenshteinDistance({}, 'athenaeum-polak & van gennep', 'athenaeum  polak & van gennep')
  True
  >>> smallLevenshteinDistance({}, 'publieboek : baart', 'publiboek')
  True
  >>> smallLevenshteinDistance({}, 'blake en mortimer', 'blake & mortimer')
  True
  >>> smallLevenshteinDistance({}, 'nomonkeybooks', 'no monkey business')
  False
  """

  retVal = False

  #
  # check which string is longer
  # needed to compare levenshtein distance relative to string length
  #
  longerNameLength = max([len(str1), len(str2)])
  halfLongerNameLength = longerNameLength/2
  
  distance = enchant.utils.levenshtein(str1, str2)
 
  if(longerNameLength > 1 and distance == 1):
    #
    # the levenshtein distance is very small,
    # very likely it was just a typo or there is a special character like a hyphen
    #
    retVal = True
    count(stats, 'levenshtein-distance-match-just-1')
  elif(distance < (longerNameLength/4)):
    #
    # the levenshtein distance is relatively low (less than a quarter of the length of the string)
    #
    retVal = True
    count(stats, 'levenshtein-distance-match-less-than-a-quarter')
  #
  # Checking for a too big difference turned out to be to strict
  # "Sven Lieber" and "Lieber, Sven" would have too much of a difference already
  # thus going to the else condition where the words are checked separately
  #
  #elif(distance > halfLongerNameLength ):
    #
    # The distance is quite big
    #
    #count(stats, 'levenshtein-distance-no-match-too-big')
    #retVal = False
    #print("definitely no match, distance too long")
  else:
    #
    # The levenshtein distance is not too small but also not too big
    # check the distance for different words
    #
    strList1 = str1.split()
    strList2 = str2.split()

    if(len(strList1) == 1 and len(strList2) > 1):
      #
      # We only have to check if a misspelled version of the single word first string
      # matches with one of the words of the second string
      #
      if(smallLevenshteinInList(str1, strList2)):
        count(stats, 'levenshtein-distance-match-word1-in-list2')
        retVal = True
    elif(len(strList2) == 1 and len(strList1) > 1):
      #
      # We only have to check if a misspelled version of the single word second string
      # matches with one of the words of the first string
      #
      if(smallLevenshteinInList(str2, strList1)):
        count(stats, 'levenshtein-distance-match-word2-in-list1')
        retVal = True
    elif(len(strList1) == 1 and len(strList2) == 1):
      # both are just one word and the levenshtein distance was already too big
      retVal = False
    else:
      # both names consist of many words
      if(smallLevenshteinBetweenLists(strList1, strList2)):
        count(stats, 'levenshtein-distance-match-words-in-lists')
        retVal = True

  return retVal

# -----------------------------------------------------------------------------
def smallLevenshteinDistanceImproved(stats, str1, str2):
  """This function checks both strings with respect to their levenshtein distance, checking also substrings.

  >>> smallLevenshteinDistance({}, 'koninklijke bibliotheek albert i', 'koninklijke bibliotheek van belgie')
  True
  >>> smallLevenshteinDistance({}, 'athenaeum-polak & van gennep', 'athenaeum  polak & van gennep')
  True
  >>> smallLevenshteinDistance({}, 'publieboek : baart', 'publiboek')
  True
  >>> smallLevenshteinDistance({}, 'blake en mortimer', 'blake & mortimer')
  True
  >>> smallLevenshteinDistance({}, 'nomonkeybooks', 'no monkey business')
  False
  """

  retVal = False

  #
  # check which string is longer
  # needed to compare levenshtein distance relative to string length
  #
  longerNameLength = max([len(str1), len(str2)])
  halfLongerNameLength = longerNameLength/2
  
  distance = enchant.utils.levenshtein(str1, str2)
 
  if(longerNameLength > 1 and distance == 1):
    #
    # the levenshtein distance is very small,
    # very likely it was just a typo or there is a special character like a hyphen
    #
    retVal = True
    count(stats, 'levenshtein-distance-match-just-1')
  elif(distance < (longerNameLength/4)):
    #
    # the levenshtein distance is relatively low (less than a quarter of the length of the string)
    #
    retVal = True
    count(stats, 'levenshtein-distance-match-less-than-a-quarter')
  #
  # Checking for a too big difference turned out to be to strict
  # "Sven Lieber" and "Lieber, Sven" would have too much of a difference already
  # thus going to the else condition where the words are checked separately
  #
  #elif(distance > halfLongerNameLength ):
    #
    # The distance is quite big
    #
    #count(stats, 'levenshtein-distance-no-match-too-big')
    #retVal = False
    #print("definitely no match, distance too long")
  else:
    #
    # The levenshtein distance is not too small but also not too big
    # check the distance for different words
    #
    strList1 = str1.split()
    strList2 = str2.split()

    maxLenDiff = 2
    lenDiff = abs(len(strList1)-len(strList2))

    if(lenDiff >= maxLenDiff):
      return False
    elif(lenDiff < maxLenDiff and len(strList1) == 1 and len(strList2) > 1):
      # even though maxLen is not exceeded, one of the lists has just 1 element
      return False
    elif(lenDiff < maxLenDiff and len(strList2) == 1 and len(strList1) > 1):
      # even though maxLen is not exceeded, one of the lists has just 1 element
      return False
    elif(len(strList1) == 1 and len(strList2) > 1):
      #
      # We only have to check if a misspelled version of the single word first string
      # matches with one of the words of the second string
      # If the second is a large list of words we likely get a mismatch, thus make the max=3
      #
      if(smallLevenshteinInList(str1, strList2)):
        count(stats, 'levenshtein-distance-match-word1-in-list2')
        retVal = True
    elif(len(strList2) == 1 and len(strList1) > 1):
      #
      # We only have to check if a misspelled version of the single word second string
      # matches with one of the words of the first string
      #
      if(smallLevenshteinInList(str2, strList1)):
        count(stats, 'levenshtein-distance-match-word2-in-list1')
        retVal = True
    elif(len(strList1) == 1 and len(strList2) == 1):
      # both are just one word and the levenshtein distance was already too big
      retVal = False
    else:
      # both names consist of many words
      if(smallLevenshteinBetweenLists(strList1, strList2)):
        count(stats, 'levenshtein-distance-match-words-in-lists')
        retVal = True

  return retVal



# -----------------------------------------------------------------------------
def createURIString(valueString, delimiter, vocab):
  """This function takes a delimiter separted string of values and returns a string
     in which every of these values is prefixed with the specified vocab URI.

  >>> createURIString('nl;fr;de', ';', 'http://id.loc.gov/vocabulary/languages/')
  'http://id.loc.gov/vocabulary/languages/nl;http://id.loc.gov/vocabulary/languages/fr;http://id.loc.gov/vocabulary/languages/de'

  An empty input string results in an empty output string
  >>> createURIString('', ';', 'http://id.loc.gov/vocabulary/languages/')
  ''

  Only a delimiter results in an empty string
  >>> createURIString(';', ';', 'http://id.loc.gov/vocabulary/languages/')
  ''

  """

  uris = []
  urisString = ""
  values = valueString.split(delimiter)
  if len(values) > 1: 
    for v in values:
      if len(v) > 0:
        uris.append(vocab + v) 
    urisString = ';'.join(uris)
  elif len(values) == 1:
    if len(values[0]) > 0:
      urisString = vocab + valueString
  else:
    urisString = ''

  return urisString

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

  inputISBNNorm = re.sub('\D', '', inputISBN)

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
