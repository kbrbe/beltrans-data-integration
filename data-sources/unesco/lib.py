import lxml.html 
import utils_isbn
import re

# -----------------------------------------------------------------------------
def parseContributor(row, nameClass, firstnameClass, qualifierClass):
  """This function parses information about contributors of a given type and returns a data structure with contributor information.

  It can find a person first author and a second non person author

  >>> html1 = '<tr><td class="res1">1/2</td><td class="res2"><span class="sn_auth_name">Lieber</span>, <span class="sn_auth_firstname">Sven</span>; <span class="sn_auth_name">Fake institution</span>, <span class="sn_auth_quality">Paris</span>: <span class="sn_isbn">"(ISBN: 2930367105, 9077213058, 9077213074)"</span><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]</td></tr>'
  >>> doc1 = lxml.html.fromstring(html1)
  >>> parseContributor(doc1, 'sn_auth_name', 'sn_auth_firstname', 'sn_auth_quality')
  [{'type': 'person', 'name': 'Lieber', 'firstname': 'Sven'}, {'type': 'org', 'name': 'Fake institution', 'place': 'Paris'}]

  It can also find both, if the person is missing a firstname (however, it can not be determined if the person is a person, hence it is 'unknown')

  >>> html2 = '<tr><td class="res1">1/2</td><td class="res2"><span class="sn_auth_name">Lieber</span>,; <span class="sn_auth_name">Fake institution</span>, <span class="sn_auth_quality">Paris</span>: <span class="sn_isbn">"(ISBN: 2930367105, 9077213058, 9077213074)"</span><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]</td></tr>'
  >>> doc2 = lxml.html.fromstring(html2)
  >>> parseContributor(doc2, 'sn_auth_name', 'sn_auth_firstname', 'sn_auth_quality')
  [{'type': 'unknown', 'name': 'Lieber'}, {'type': 'org', 'name': 'Fake institution', 'place': 'Paris'}]

  Similarly, it can also find both if the non person is missing the qualifier

  >>> html3 = '<tr><td class="res1">1/2</td><td class="res2"><span class="sn_auth_name">Lieber</span>, <span class="sn_auth_firstname">Sven</span>; <span class="sn_auth_name">Fake institution</span>, : <span class="sn_isbn">"(ISBN: 2930367105, 9077213058, 9077213074)"</span><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]</td></tr>'
  >>> doc3 = lxml.html.fromstring(html3)
  >>> parseContributor(doc3, 'sn_auth_name', 'sn_auth_firstname', 'sn_auth_quality')
  [{'type': 'person', 'name': 'Lieber', 'firstname': 'Sven'}, {'type': 'unknown', 'name': 'Fake institution'}]



  Vice versa, it can find a non person first author and a second person author

  >>> html4 = '<tr><td class="res1">1/2</td><td class="res2"><span class="sn_auth_name">Fake institution</span>, <span class="sn_auth_quality">Paris</span>; <span class="sn_auth_name">Lieber</span>, <span class="sn_auth_firstname">Sven</span>: <span class="sn_isbn">"(ISBN: 2930367105, 9077213058, 9077213074)"</span><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]</td></tr>'
  >>> doc4 = lxml.html.fromstring(html4)
  >>> parseContributor(doc4, 'sn_auth_name', 'sn_auth_firstname', 'sn_auth_quality')
  [{'type': 'org', 'name': 'Fake institution', 'place': 'Paris'}, {'type': 'person', 'name': 'Lieber', 'firstname': 'Sven'}]

  Also if the first non person author has missing attributes

  >>> html5 = '<tr><td class="res1">1/2</td><td class="res2"><span class="sn_auth_name">Fake institution</span>, ; <span class="sn_auth_name">Lieber</span>, <span class="sn_auth_firstname">Sven</span>: <span class="sn_isbn">"(ISBN: 2930367105, 9077213058, 9077213074)"</span><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]</td></tr>'
  >>> doc5 = lxml.html.fromstring(html5)
  >>> parseContributor(doc5, 'sn_auth_name', 'sn_auth_firstname', 'sn_auth_quality')
  [{'type': 'unknown', 'name': 'Fake institution'}, {'type': 'person', 'name': 'Lieber', 'firstname': 'Sven'}]

  Or the second person author has missing attributes

  >>> html6 = '<tr><td class="res1">1/2</td><td class="res2"><span class="sn_auth_name">Fake institution</span>, <span class="sn_auth_quality">Paris</span>; <span class="sn_auth_name">Lieber</span>, : <span class="sn_isbn">"(ISBN: 2930367105, 9077213058, 9077213074)"</span><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]</td></tr>'
  >>> doc6 = lxml.html.fromstring(html6)
  >>> parseContributor(doc6, 'sn_auth_name', 'sn_auth_firstname', 'sn_auth_quality')
  [{'type': 'org', 'name': 'Fake institution', 'place': 'Paris'}, {'type': 'unknown', 'name': 'Lieber'}]

  """
  allFields = row.findall('td[@class="res2"]/span', {})

  contributors = []
  currentContributor = {}
  lastClass = None

  for field in allFields:
    fieldName = field.attrib['class']

    if fieldName == nameClass:
      # it is the name of a contributor
      if lastClass == nameClass:
        # we just had a contributor name, so we are already parsing a new one
        # the last one seemed to only have a name and nothing else
        contributors.append(currentContributor.copy())
        currentContributor = {}
      # a new contributor
      currentContributor['type'] = 'unknown'
      currentContributor['name'] = field.text
      lastClass = fieldName
    elif fieldName == firstnameClass:
      # the first name of a previously found contributor: it is a person
      currentContributor['type'] = 'person'
      currentContributor['firstname'] = field.text
      contributors.append(currentContributor.copy())
      currentContributor = {}
      lastClass = fieldName
    elif fieldName == qualifierClass:
      # the qualifier of a previously found contributor: it is not a person
      currentContributor['type'] = 'org'
      currentContributor['place'] = field.text
      contributors.append(currentContributor.copy())
      currentContributor = {}
      lastClass = fieldName
    else:
      # it seems we are done with the current contributor
      lastClass = fieldName
      # save the partial contributor we may have (it is empty if we already saved it)
      if currentContributor:
        contributors.append(currentContributor.copy())
        currentContributor = {}
  
  return contributors


# -----------------------------------------------------------------------------
def serializeContributorsToString(contributors):
  """This function serializes a contributor dictionary to a string representation.
  >>> cont1 = [{'type': 'person', 'name': 'Lieber', 'firstname': 'Sven'}, {'type': 'org', 'name': 'Fake institution', 'place': 'Paris'}]
  >>> serializeContributorsToString(cont1)
  'type=person,name=Lieber,firstname=Sven;type=org,name=Fake institution,place=Paris'
  """
  contributorString = []
  for cont in contributors:
    contributorString.append(dictToString(cont, keySeparator=',', valueSeparator='='))
  return ';'.join(contributorString)


# -----------------------------------------------------------------------------
def getStructuredRecord(htmlElement, encounteredFields):
  """
  >>> html1 = '<html><body><table class="restable"><tr><td class="res1">1/2</td><td class="res2"><span class="sn_isbn">"(ISBN: 2930367105, 9077213058, 9077213074)"</span><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]</td></tr><tr><td class="res1">2/2</td><td class="res2"><span class="sn_year">2020</span><span class="sn_pub"><span class="publisher">PBL</span></span></td></tr></table></body></html>'
  >>> foundFields = set()
  >>> getStructuredRecord(html1, foundFields)
  [{'id': '1-2', 'isbn10': '2-930367-10-5;90-77213-05-8;90-77213-07-4', 'isbn13': '978-2-930367-10-1;978-90-77213-05-6;978-90-77213-07-0', 'sn_year': '2022', 'sn_orig_lang': 'Dutch'}, {'id': '2-2', 'sn_year': '2020', 'publisher': 'PBL'}]
  >>> sorted(foundFields)
  ['isbn10', 'isbn13', 'publisher', 'sn_orig_lang', 'sn_year']

  It should work if there is more than one author or translator

  >>> html2 = '<html><body><table class="restable"><tr><td class="res1">1/2</td><td class="res2"><span class="sn_auth_name">Bobsen</span>, <span class="sn_auth_firstname">Bob</span>: <span class="sn_isbn">"(ISBN: 2930367105, 9077213058, 9077213074)"</span><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]<span class="sn_transl_name">Lieber</span>, <span class="sn_transl_firstname">Sven</span>; <span class="sn_transl_name">Doe</span>, <span class="sn_transl_firstname">John</span></td></tr><tr><td class="res1">2/2</td><td class="res2"><span class="sn_auth_name">Jannssen</span>, <span class="sn_auth_firstname">Jan</span>: <span class="sn_year">2020</span><span class="sn_pub"><span class="publisher">PBL</span></span><span class="sn_transl_name">Alisson</span>, <span class="sn_transl_firstname">Alice</span></td></tr></table></body></html>'
  >>> foundFields2 = set()
  >>> getStructuredRecord(html2, foundFields2)
  [{'id': '1-2', 'authors': 'type=person,name=Bobsen,firstname=Bob', 'translators': 'type=person,name=Lieber,firstname=Sven;type=person,name=Doe,firstname=John', 'isbn10': '2-930367-10-5;90-77213-05-8;90-77213-07-4', 'isbn13': '978-2-930367-10-1;978-90-77213-05-6;978-90-77213-07-0', 'sn_year': '2022', 'sn_orig_lang': 'Dutch'}, {'id': '2-2', 'authors': 'type=person,name=Jannssen,firstname=Jan', 'translators': 'type=person,name=Alisson,firstname=Alice', 'sn_year': '2020', 'publisher': 'PBL'}]
  >>> sorted(foundFields2)
  ['authors', 'isbn10', 'isbn13', 'publisher', 'sn_orig_lang', 'sn_year', 'translators']

  A record with several authors, one with a single author, but both without translators.

  >>> html3 = '<html><body><table class="restable"><tr><td class="res1">1/2</td><td class="res2"><span class="sn_auth_name">Bobsen</span>, <span class="sn_auth_firstname">Bob</span>: <span class="sn_isbn">"(ISBN: 2930367105, 9077213058, 9077213074)"</span><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]</td></tr><tr><td class="res1">2/2</td><td class="res2"><span class="sn_auth_name">Jannssen</span>, <span class="sn_auth_firstname">Jan</span>; <span class="sn_auth_name">Alisson</span>, <span class="sn_auth_firstname">Alice</span>: <span class="sn_year">2020</span><span class="sn_pub"><span class="publisher">PBL</span></span></td></tr></table></body></html>'
  >>> foundFields3 = set()
  >>> getStructuredRecord(html3, foundFields3)
  [{'id': '1-2', 'authors': 'type=person,name=Bobsen,firstname=Bob', 'isbn10': '2-930367-10-5;90-77213-05-8;90-77213-07-4', 'isbn13': '978-2-930367-10-1;978-90-77213-05-6;978-90-77213-07-0', 'sn_year': '2022', 'sn_orig_lang': 'Dutch'}, {'id': '2-2', 'authors': 'type=person,name=Jannssen,firstname=Jan;type=person,name=Alisson,firstname=Alice', 'sn_year': '2020', 'publisher': 'PBL'}]
  >>> sorted(foundFields3)
  ['authors', 'isbn10', 'isbn13', 'publisher', 'sn_orig_lang', 'sn_year']

  Records with an organization instead of a person (no auth_firstname, but auth_quality)

  >>> html4 = '<html><body><table class="restable"><tr><td class="res1">1/2</td><td class="res2"><span class="sn_auth_name">Fake institution</span>, <span class="sn_auth_quality">Paris</span>: <span class="sn_isbn">"(ISBN: 2930367105, 9077213058, 9077213074)"</span><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]</td></tr><tr><td class="res1">2/2</td><td class="res2"><span class="sn_auth_name">Jannssen</span>, <span class="sn_auth_firstname">Jan</span>; <span class="sn_auth_name">Alisson</span>, <span class="sn_auth_firstname">Alice</span>: <span class="sn_year">2020</span><span class="sn_pub"><span class="publisher">PBL</span></span></td></tr></table></body></html>'
  >>> foundFields4 = set()
  >>> getStructuredRecord(html4, foundFields4)
  [{'id': '1-2', 'authors': 'type=org,name=Fake institution,place=Paris', 'isbn10': '2-930367-10-5;90-77213-05-8;90-77213-07-4', 'isbn13': '978-2-930367-10-1;978-90-77213-05-6;978-90-77213-07-0', 'sn_year': '2022', 'sn_orig_lang': 'Dutch'}, {'id': '2-2', 'authors': 'type=person,name=Jannssen,firstname=Jan;type=person,name=Alisson,firstname=Alice', 'sn_year': '2020', 'publisher': 'PBL'}]
  >>> sorted(foundFields4)
  ['authors', 'isbn10', 'isbn13', 'publisher', 'sn_orig_lang', 'sn_year']

  Records with multiple authors: first a person and then an organization

  >>> html5 = '<html><body><table class="restable"><tr><td class="res1">1/2</td><td class="res2"><span class="sn_auth_name">Lieber</span>, <span class="sn_auth_firstname">Sven</span>; <span class="sn_auth_name">Fake institution</span>, <span class="sn_auth_quality">Paris</span>: <span class="sn_isbn">"(ISBN: 2930367105, 9077213058, 9077213074)"</span><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]</td></tr><tr><td class="res1">2/2</td><td class="res2"><span class="sn_auth_name">Jannssen</span>, <span class="sn_auth_firstname">Jan</span>; <span class="sn_auth_name">Alisson</span>, <span class="sn_auth_firstname">Alice</span>: <span class="sn_year">2020</span><span class="sn_pub"><span class="publisher">PBL</span></span></td></tr></table></body></html>'
  >>> foundFields5 = set()
  >>> getStructuredRecord(html5, foundFields5)
  [{'id': '1-2', 'authors': 'type=person,name=Lieber,firstname=Sven;type=org,name=Fake institution,place=Paris', 'isbn10': '2-930367-10-5;90-77213-05-8;90-77213-07-4', 'isbn13': '978-2-930367-10-1;978-90-77213-05-6;978-90-77213-07-0', 'sn_year': '2022', 'sn_orig_lang': 'Dutch'}, {'id': '2-2', 'authors': 'type=person,name=Jannssen,firstname=Jan;type=person,name=Alisson,firstname=Alice', 'sn_year': '2020', 'publisher': 'PBL'}]
  >>> sorted(foundFields5)
  ['authors', 'isbn10', 'isbn13', 'publisher', 'sn_orig_lang', 'sn_year']



  """ 
  doc = lxml.html.fromstring(htmlElement)

  records = []
  rows = doc.findall('body/table[@class="restable"]/tr', {})
  for row in rows:
    record = {}
    rowID = row.find('td[@class="res1"]').text
    record['id'] = rowID.replace('/', '-')
    fields = row.findall('td[@class="res2"]/span')


    authors = parseContributor(row, 'sn_auth_name', 'sn_auth_firstname', 'sn_auth_quality')
    translators = parseContributor(row, 'sn_transl_name', 'sn_transl_firstname', 'sn_transl_quality')    

    if len(authors) > 0:
      encounteredFields.add('authors')
      record['authors'] = serializeContributorsToString(authors)

    if len(translators) > 0:
      encounteredFields.add('translators')
      record['translators'] = serializeContributorsToString(translators)

    # for all other fields
    for field in fields:
      fieldName = field.attrib['class']

      if fieldName == 'sn_pub':
        publisherData = field.findall('span')
        for publisherField in publisherData:
          publisherFieldName = publisherField.attrib['class']
          record[publisherFieldName] = publisherField.text
          encounteredFields.add(publisherFieldName)
      elif fieldName == 'sn_isbn':
        isbnIdentifiersString = re.findall('\(ISBN: (.*)\)', field.text)[0]
        isbnIdentifiers = isbnIdentifiersString.split(',')
        isbn10Set = set()
        isbn13Set = set()
        for isbn in isbnIdentifiers:
          isbn = isbn.strip()
          isbnUnformatted = isbn.replace('-','')
          if len(isbnUnformatted) == 10 or len(isbnUnformatted) == 13:
            isbn10Set.add(utils_isbn.getNormalizedISBN10(isbnUnformatted))
            isbn13Set.add(utils_isbn.getNormalizedISBN13(isbnUnformatted))
          else:
            print(f'Invalid ISBN "{isbn}" in record {rowID}')
        record['isbn10'] = ';'.join(sorted(isbn10Set))
        record['isbn13'] = ';'.join(sorted(isbn13Set))
        encounteredFields.add('isbn10')
        encounteredFields.add('isbn13')
      elif fieldName in ['sn_auth_name', 'sn_auth_firstname', 'sn_auth_quality', 'sn_transl_name', 'sn_transl_firstname', 'sn_transl_quality']:
        # we already handled authors and translators separately because there can be more than one, thus skip related fields
        pass
      else:
        record[fieldName] = field.text
        encounteredFields.add(fieldName)
    records.append(record)
  return records

# -----------------------------------------------------------------------------
def dictToString(dictionary, keySeparator='_', valueSeparator='-'):

  paramList = [f'{key}{valueSeparator}{value}' for (key,value) in dictionary.items()]
  return keySeparator.join(paramList)

# -----------------------------------------------------------------------------
def getOutputFolderName(params):
  """This function creates the name of the output folder, based on the provided search parameters.

  >>> getOutputFolderName({'lg': 0, 'sl': 'nld', 'l': 'fra', 'from': '1970', 'to': 2020})
  'lg-0_sl-nld_l-fra_from-1970_to-2020'
  """
  return dictToString(params, '_', '-')

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
