import pandas as pd

class DataprofileTestHelper:

  # ---------------------------------------------------------------------------
  def __init__(self, data):
    self.df = pd.DataFrame(data)

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
    """Returns True if a manifestation with the given ID exists.
    >>> data = DataprofileTestHelper([{"targetTextKBRIdentifier": 1, "name": "john"},{"targetTextKBRIdentifier": 2, "name": "jane"}])
    >>> data.kbrTargetIdentifierExists(2)
    True
    >>> data.kbrTargetIdentifierExists(4)
    False
    """
    return (self.df['targetTextKBRIdentifier'] == identifier).any()

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
    >>> data2 = DataprofileTestHelper([{"myID": 1, "name": "john", "myCol": "sven (12, 34)"},{"myID": 1, "name": "jane"}])
    >>> data2._getCellValue("myID", 1, "myCol")
    Traceback (most recent call last):
     ...
    ValueError: More than one row with ID "1" in column "myID" found!
    """
    selection = (self.df.loc[self.df[idColName] == idColValue, colName])
    if selection.size > 1:
      raise ValueError(f'More than one row with ID "{idColValue}" in column "{idColName}" found!')
    elif selection.size == 1:
      return selection[0]
    else:
      raise ValueError(f'No row with ID "{idColValue}" in column "{idColName}" found!')
 
    
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
