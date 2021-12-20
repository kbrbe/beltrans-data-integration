
def mostCompleteDate(dates):
  """This function returns the most complete date from the given array, if there is a mismatch both are returned.

  """

  # TODO: change to actually compare the dates
  if len(dates) > 0:
    return dates[0]
  else:
    return ''

# -----------------------------------------------------------------------------
def selectDate(row, role, dateType, sources):
  """This function chooses the most complete date for the given role and row, possible dateTypes are 'Birth' and 'Death'.

  Select the most complete date betwen the sources
  >>> row = {'authorBirthDateKBR': '1988-04-25', 'authorBirthDateISNI': '1988'}
  >>> selectDate(row, 'author', 'Birth', ['KBR', 'ISNI'])
  >>> row['authorBirthDate'] == '1988-04-25'
  True

  >>> row = {'authorBirthDateKBR': '', 'authorBirthDateISNI': '1988'}
  >>> selectDate(row, 'author', 'Birth', ['KBR', 'ISNI'])
  >>> row['authorBirthDate'] == '1988'
  True

  Keep it empty if none of the sources provide a date
  >>> row = {'authorBirthDateKBR': '', 'authorBirthDateISNI': ''}
  >>> selectDate(row, 'author', 'Birth', ['KBR', 'ISNI'])
  >>> row['authorBirthDate'] == ''
  True

  It also works for other roles than author
  >>> row = {'translatorBirthDateKBR': '1988-04-25', 'translatorBirthDateISNI': '1988'}
  >>> selectDate(row, 'translator', 'Birth', ['KBR', 'ISNI'])
  >>> row['translatorBirthDate'] == '1988-04-25'
  True

  >>> row = {'illustratorBirthDateKBR': '1988-04-25', 'illustratorBirthDateISNI': '1988'}
  >>> selectDate(row, 'illustrator', 'Birth', ['KBR', 'ISNI'])
  >>> row['illustratorBirthDate'] == '1988-04-25'
  True

  >>> row = {'scenaristBirthDateKBR': '1988-04-25', 'scenaristBirthDateISNI': '1988'}
  >>> selectDate(row, 'scenarist', 'Birth', ['KBR', 'ISNI'])
  >>> row['scenaristBirthDate'] == '1988-04-25'
  True

  Log an error if a mismatch was found and keep both in the output
  >>> row = {'authorBirthDateKBR': '1988-04-25', 'authorBirthDateISNI': '1989'}
  >>> selectDate(row, 'author', 'Birth', ['KBR', 'ISNI'])
  >>> row['authorBirthDate'] == '1988-04-25 or 1989'
  True

  The same works also for death dates
  >>> row = {'authorDeathDateKBR': '1988-04-25', 'authorDeathDateISNI': '1988'}
  >>> selectDate(row, 'author', 'Death', ['KBR', 'ISNI'])
  >>> row['authorDeathDate'] == '1988-04-25'
  True
  """

  # extract all possible birth dates
  dates = []
  for s in sources:
    colName = f'{role}{dateType}Date{s}'
    dates.append(row[colName])

  outputColName = f'{role}{dateType}Date'

  # set the selected value
  row[outputColName] = mostCompleteDate(dates)

  # remove the initial sources
  for s in sources:
    colName = f'{role}{dateType}Date{s}'
    row.pop(colName)
  

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
