import pandas as pd

class DataprofileTestHelper:

  # ---------------------------------------------------------------------------
  def __init__(self, data):
    self.df = pd.DataFrame(data)
    print(self.df)

  # ---------------------------------------------------------------------------
  def numberRows(self):
    """Returns the number of rows of the provided CSV.
    >>> data = DataprofileTestHelper([{"id": 1, "name": "john"},{"id": 2, "name": "jane"}])
    >>> data.numberRows()
    2
    """
    return len(self.df.index)

  # ---------------------------------------------------------------------------
  def kbrTargetIdentifierExists(self, identifier):
    """Returns True if a KBR manifestation with the given ID exists.
    >>> data = DataprofileTestHelper([{"targetTextKBRIdentifier": 1, "name": "john"},{"targetTextKBRIdentifier": 2, "name": "jane"}])
    >>> data.kbrTargetIdentifierExists(2)
    True
    >>> data.kbrTargetIdentifierExists(4)
    False
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      value = self._getCellValue("targetTextKBRIdentifier", identifier, "targetTextKBRIdentifier")
      if value == identifier:
        return True
      else:
        return False
    except:
      return False


  # ---------------------------------------------------------------------------
  def bnfTargetIdentifierExists(self, identifier):
    """Returns True if a BnF manifestation with the given ID exists.
    >>> data = DataprofileTestHelper([{"targetTextBnFIdentifier": 1, "name": "john"}, {"targetTextBnFIdentifier": 2, "name": "jane"}, {"targetTextKBRIdentifier": 3, "name": "test", "targetTextBnFIdentifier": ""}, {"targetTextKBRIdentifier": 4}, {"targetTextBnFIdentifier": "BnF book 22"}])
    >>> data.bnfTargetIdentifierExists(2)
    True
    >>> data.bnfTargetIdentifierExists(4)
    False
    >>> data.bnfTargetIdentifierExists("BnF book 22")
    True
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      value = self._getCellValue("targetTextBnFIdentifier", identifier, "targetTextBnFIdentifier")
      if value == identifier:
        return True
      else:
        return False
    except:
      return False

  # ---------------------------------------------------------------------------
  def kbrAndBnFIdentifierOnSameRow(self, kbrIdentifier, bnfIdentifier):
    """Returns True if a KBR manifestation with the given KBR ID exists on the same row as a BnF manifestation with the given BnF ID.
    >>> data = DataprofileTestHelper([{"targetTextKBRIdentifier": "KBR book 4", "name": "john", "targetTextBnFIdentifier": "BnF book 4"},{"targetTextKBRIdentifier": 2, "name": "jane"}])

    Returns True if a row is found where both identifiers are present
    >>> data.kbrAndBnFIdentifierOnSameRow("KBR book 4", "BnF book 4")
    True

    If there is no row, for example with KBRID 1 and BnFID 2, then False is returned
    >>> data.kbrAndBnFIdentifierOnSameRow("KBR book 4",2)
    False

    If  there is even no row with the given KBR identifier found a ValueError is raised
    >>> data.kbrAndBnFIdentifierOnSameRow(11,22)
    Traceback (most recent call last):
     ...
    ValueError: No row with ID "11" in column "targetTextKBRIdentifier" found!

    >>> data2 = DataprofileTestHelper([{"targetTextKBRIdentifier": 1, "name": "john", "targetTextBnFIdentifier": ""},{"targetTextKBRIdentifier": 2, "targetTextBnFIdentifier": 2, "name": "jane"}])

    If there is no BnF identifier (empty value) then False is returned
    >>> data2.kbrAndBnFIdentifierOnSameRow(1,1)
    False
    >>> data2.kbrAndBnFIdentifierOnSameRow(1,2)
    False
    >>> data2.kbrAndBnFIdentifierOnSameRow(2,2)
    True

    >>> data3 = DataprofileTestHelper([{"targetTextKBRIdentifier": 1, "name": "john", "targetTextBnFIdentifier": "", "name": ""},{"targetTextKBRIdentifier": 2, "targetTextBnFIdentifier": "2", "name": "jane"}, {"targetTextKBRIdentifier": 2, "targetTextBnFIdentifier": 2}])

    If a KBR identifier is found more than once an error is raised
    >>> data3.kbrAndBnFIdentifierOnSameRow(2,2)
    Traceback (most recent call last):
     ...
    ValueError: More than one row with ID "2" in column "targetTextKBRIdentifier" found!
    """
    value = self._getCellValue('targetTextKBRIdentifier', kbrIdentifier, 'targetTextBnFIdentifier')
    if value == bnfIdentifier:
      return True
    else:
      return False

  # ---------------------------------------------------------------------------
  def kbrTargetIdentifierHasAuthor(self, identifier, authorString):
    """Returns True if a manifestation with the given ID contains the given author string.
    >>> data = DataprofileTestHelper([{"targetTextKBRIdentifier": 1, "name": "john", "authorIdentifier": "sven (12, 34)"},{"targetTextKBRIdentifier": 2, "name": "jane"}])
    >>> data.kbrTargetIdentifierHasAuthor(1, "sven (12, 34)")
    True
    >>> data.kbrTargetIdentifierHasAuthor(1, "sven")
    False
    """
    selection = self._getCellValue('targetTextKBRIdentifier', identifier, 'authorIdentifier')
    return (selection == authorString)

  # ---------------------------------------------------------------------------
  def _getCellValue(self, idColName, idColValue, colName):
    """Returns the value of a specific cell or raises errors in case the row isn't found or more than one value is found.
    >>> data = DataprofileTestHelper([{"myID": 1, "name": "john", "myCol": "sven (12, 34)"},{"myID": 2, "name": "jane"}])
    >>> data._getCellValue("myID", 1, "myCol")
    'sven (12, 34)'
    >>> data._getCellValue("myID", 11, "myCol")
    Traceback (most recent call last):
     ...
    ValueError: No row with ID "11" in column "myID" found!
    >>> data._getCellValue("myIDColumnWhichDoesNotExist", 11, "myCol")
    Traceback (most recent call last):
     ...
    KeyError: 'ID column "myIDColumnWhichDoesNotExist" does not exist!'
    >>> data._getCellValue("myID", 1, "myColWhichDoesNotExist")
    Traceback (most recent call last):
     ...
    KeyError: 'Value column "myColWhichDoesNotExist" does not exist!'
    >>> data2 = DataprofileTestHelper([{"myID": 1, "name": "john", "myCol": "sven (12, 34)"},{"myID": 1, "name": "jane"}])
    >>> data2._getCellValue("myID", 1, "myCol")
    Traceback (most recent call last):
     ...
    ValueError: More than one row with ID "1" in column "myID" found!
    >>> data3 = DataprofileTestHelper([{"targetTextKBRIdentifier": 1, "name": "john", "targetTextBnFIdentifier": "", "name": ""},{"targetTextKBRIdentifier": 2, "name": "jane"}, {"targetTextBnFIdentifier": "2", "name": "jane"}])
    >>> data3._getCellValue("targetTextKBRIdentifier", 2, "targetTextBnFIdentifier")
    Traceback (most recent call last):
     ...
    KeyError: 'No value found in column "targetTextKBRIdentifier"'
    """
    if idColName not in self.df:
      raise KeyError(f'ID column "{idColName}" does not exist!')
    if colName not in self.df:
      raise KeyError(f'Value column "{colName}" does not exist!')
    
    selection = (self.df.loc[self.df[idColName] == idColValue, colName])

    if selection.size > 1:
      raise ValueError(f'More than one row with ID "{idColValue}" in column "{idColName}" found!')
    elif selection.size == 1:
      if selection.isna().all():
        raise KeyError(f'No value found in column "{idColName}"')
      else:
        return selection.item()
      return selection
    else:
      raise ValueError(f'No row with ID "{idColValue}" in column "{idColName}" found!')
 
    
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
