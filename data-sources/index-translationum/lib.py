import lxml.html 

# -----------------------------------------------------------------------------
def getStructuredRecord(htmlElement, encounteredFields):
  """
  >>> html1 = '<html><body><table class="restable"><tr><td class="res1">1/2</td><td class="res2"><span class="sn_year">2022</span>[<span class="sn_orig_lang">Dutch</span>]</td></tr><tr><td class="res1">2/2</td><td class="res2"><span class="sn_year">2020</span><span class="sn_pub"><span class="publisher">PBL</span></span></td></tr></table></body></html>'
  >>> foundFields = set()
  >>> getStructuredRecord(html1, foundFields)
  [{'id': '1/2', 'sn_year': '2022', 'sn_orig_lang': 'Dutch'}, {'id': '2/2', 'sn_year': '2020', 'publisher': 'PBL'}]
  >>> sorted(foundFields)
  ['publisher', 'sn_orig_lang', 'sn_year']
  """ 
  doc = lxml.html.fromstring(htmlElement)

  records = []
  rows = doc.findall('body/table[@class="restable"]/tr', {})
  for row in rows:
    record = {}
    rowID = row.find('td[@class="res1"]').text
    record['id'] = rowID
    fields = row.findall('td[@class="res2"]/span')
    for field in fields:
      fieldName = field.attrib['class']

      if fieldName == 'sn_pub':
        publisherData = field.findall('span')
        for publisherField in publisherData:
          publisherFieldName = publisherField.attrib['class']
          record[publisherFieldName] = publisherField.text
          encounteredFields.add(publisherFieldName)
      else:
        record[fieldName] = field.text
        encounteredFields.add(fieldName)
    records.append(record)
  return records

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
