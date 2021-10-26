from datetime import datetime

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
if __name__ == "__main__":
  import doctest
  doctest.testmod()
