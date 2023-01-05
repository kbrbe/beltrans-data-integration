import lxml.html 
import utils_isbn
import re

# -----------------------------------------------------------------------------
def getStructuredRecord(htmlElement, encounteredFields):
  """
  >>> html1 = '<html><body><table class="restable"><tr><td class="res1">1/2</td><td class="res2"><span class="sn_isbn">"(ISBN: 2930367105, 9077213058, 9077213074)"</span><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]</td></tr><tr><td class="res1">2/2</td><td class="res2"><span class="sn_year">2020</span><span class="sn_pub"><span class="publisher">PBL</span></span></td></tr></table></body></html>'
  >>> foundFields = set()
  >>> getStructuredRecord(html1, foundFields)
  [{'id': '1-2', 'isbn10': '2-930367-10-5;90-77213-05-8;90-77213-07-4', 'isbn13': '978-2-930367-10-1;978-90-77213-05-6;978-90-77213-07-0', 'sn_year': '2022', 'sn_orig_lang': 'Dutch'}, {'id': '2-2', 'sn_year': '2020', 'publisher': 'PBL'}]
  >>> sorted(foundFields)
  ['isbn10', 'isbn13', 'publisher', 'sn_orig_lang', 'sn_year']
  """ 
  doc = lxml.html.fromstring(htmlElement)

  records = []
  rows = doc.findall('body/table[@class="restable"]/tr', {})
  for row in rows:
    record = {}
    rowID = row.find('td[@class="res1"]').text
    record['id'] = rowID.replace('/', '-')
    fields = row.findall('td[@class="res2"]/span')
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
      else:
        record[fieldName] = field.text
        encounteredFields.add(fieldName)
    records.append(record)
  return records

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
