import pandas as pd
import utils

class DataprofileTestHelper:

  # ---------------------------------------------------------------------------
  def __init__(self, data):
    self.df = pd.DataFrame(data)
    #print(self.df)
    #print(self.df[['targetIdentifier', 'authorIdentifiers', 'illustratorIdentifiers', 'scenaristIdentifiers']])

  # ---------------------------------------------------------------------------
  def numberRows(self):
    """Returns the number of rows of the provided CSV.
    >>> data = DataprofileTestHelper([{"id": 1, "name": "john"},{"id": 2, "name": "jane"}])
    >>> data.numberRows()
    2
    """
    return len(self.df.index)

  # ---------------------------------------------------------------------------
  def targetIdentifierExists(self, identifier):
    """Returns True if a manifestation with the given ID exists.
    >>> data = DataprofileTestHelper([{"targetIdentifier": 1, "name": "john"},{"targetIdentifier": 2, "name": "jane"}])
    >>> data.targetIdentifierExists(2)
    True
    >>> data.targetIdentifierExists(4)
    False
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      value = utils.getDfCellValue(self.df, "targetIdentifier", identifier, "targetIdentifier")
      if value == identifier:
        return True
      else:
        return False
    except:
      return False



  # ---------------------------------------------------------------------------
  def kbrTargetIdentifierExists(self, identifier):
    """Returns True if a KBR manifestation with the given ID exists.
    >>> data = DataprofileTestHelper([{"targetKBRIdentifier": 1, "name": "john"},{"targetKBRIdentifier": 2, "name": "jane"}])
    >>> data.kbrTargetIdentifierExists(2)
    True
    >>> data.kbrTargetIdentifierExists(4)
    False
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      value = utils.getDfCellValue(self.df, "targetKBRIdentifier", identifier, "targetKBRIdentifier")
      if value == identifier:
        return True
      else:
        return False
    except:
      return False


  # ---------------------------------------------------------------------------
  def bnfTargetIdentifierExists(self, identifier):
    """Returns True if a BnF manifestation with the given ID exists.
    >>> data = DataprofileTestHelper([{"targetBnFIdentifier": 1, "name": "john"}, {"targetBnFIdentifier": 2, "name": "jane"}, {"targetKBRIdentifier": 3, "name": "test", "targetBnFIdentifier": ""}, {"targetKBRIdentifier": 4}, {"targetBnFIdentifier": "BnF book 22"}])
    >>> data.bnfTargetIdentifierExists(2)
    True
    >>> data.bnfTargetIdentifierExists(4)
    False
    >>> data.bnfTargetIdentifierExists("BnF book 22")
    True
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      value = utils.getDfCellValue(self.df, "targetBnFIdentifier", identifier, "targetBnFIdentifier")
      if value == identifier:
        return True
      else:
        return False
    except:
      return False

  # ---------------------------------------------------------------------------
  def kbTargetIdentifierExists(self, identifier):
    """Returns True if a KB manifestation with the given ID exists.
    >>> data = DataprofileTestHelper([{"targetKBIdentifier": 1, "name": "john"}, {"targetKBIdentifier": 2, "name": "jane"}, {"targetKBRIdentifier": 3, "name": "test", "targetKBIdentifier": ""}, {"targetKBRIdentifier": 4}, {"targetKBIdentifier": "KB book 22"}])
    >>> data.kbTargetIdentifierExists(2)
    True
    >>> data.kbTargetIdentifierExists(4)
    False
    >>> data.kbTargetIdentifierExists("KB book 22")
    True
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      value = utils.getDfCellValue(self.df, "targetKBIdentifier", identifier, "targetKBIdentifier")
      if value == identifier:
        return True
      else:
        return False
    except:
      return False


  # ---------------------------------------------------------------------------
  def identifiersOnSameRow(self, identifierTuple, otherIdentifierTuples):
    """Returns True if a contributor record (one row) contains all the given identifiers.
    The given tuples represent column name and column value, e.g. ('kbrID', '1') the column kbrID and identifier 1.
    The identifierTuple is the starting point and then the function recursively checks that the row found
    via the identifierTuple contains also the data specified by the otherIdentifierTuples.

    >>> data = DataprofileTestHelper([{'kbrIDs': 'kbr1', 'bnfIDs': 'bnf1', 'ntaIDs': 'nta1'},{'kbrIDs': '2'},{'bnfIDs': '3'}])
    >>> data.identifiersOnSameRow(('kbrIDs','kbr1'), [('bnfIDs','bnf1'), ('ntaIDs','nta1')])
    True

    >>> data.identifiersOnSameRow(('kbrIDs','kbr2'), [('bnfIDs','bnf1'), ('ntaIDs','nta1')])
    Traceback (most recent call last):
     ...
    ValueError: No row with ID "kbr2" in column "kbrIDs" found!

    >>> data2 = DataprofileTestHelper([{'kbrIDs': 'kbr1', 'bnfIDs': 'bnf1'},{'kbrIDs': 'kbr1', 'bnfIDs': 'bnf2'}])
    >>> data2.identifiersOnSameRow(('kbrIDs','kbr1'), [('bnfIDs','bnf1')])
    Traceback (most recent call last):
     ...
    ValueError: More than one row with ID "kbr1" in column "kbrIDs" found!
    """
    colName, identifier = identifierTuple
    if len(otherIdentifierTuples) > 0:
      colName2, identifier2 = otherIdentifierTuples.pop(0)
      colName2Value = utils.getDfCellValue(self.df, colName, identifier, colName2)
      if colName2Value == identifier2:
        # There was a match between given value and found value, if there is more to check do a recursive call
        # otherwise we are happy because we found a match and return True
        if len(otherIdentifierTuples) > 0:
          return self.identifiersOnSameRow((colName2, identifier2), otherIdentifierTuples)
        else:
          return True     
      else:
        # if at some point in the recursive calls one identifier is not as expected we return False
        return False
    

  # ---------------------------------------------------------------------------
  def kbrAndBnFIdentifierOnSameRow(self, kbrIdentifier, bnfIdentifier):
    """Returns True if a KBR manifestation with the given KBR ID exists on the same row as a BnF manifestation with the given BnF ID.
    >>> data = DataprofileTestHelper([{"targetKBRIdentifier": "KBR book 4", "name": "john", "targetBnFIdentifier": "BnF book 4"},{"targetKBRIdentifier": 2, "name": "jane"}])

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
    ValueError: No row with ID "11" in column "targetKBRIdentifier" found!

    >>> data2 = DataprofileTestHelper([{"targetKBRIdentifier": 1, "name": "john", "targetBnFIdentifier": ""},{"targetKBRIdentifier": 2, "targetBnFIdentifier": 2, "name": "jane"}])

    If there is no BnF identifier (empty value) then False is returned
    >>> data2.kbrAndBnFIdentifierOnSameRow(1,1)
    False
    >>> data2.kbrAndBnFIdentifierOnSameRow(1,2)
    False
    >>> data2.kbrAndBnFIdentifierOnSameRow(2,2)
    True

    >>> data3 = DataprofileTestHelper([{"targetKBRIdentifier": 1, "name": "john", "targetBnFIdentifier": "", "name": ""},{"targetKBRIdentifier": 2, "targetBnFIdentifier": "2", "name": "jane"}, {"targetKBRIdentifier": 2, "targetBnFIdentifier": 2}])

    If a KBR identifier is found more than once an error is raised
    >>> data3.kbrAndBnFIdentifierOnSameRow(2,2)
    Traceback (most recent call last):
     ...
    ValueError: More than one row with ID "2" in column "targetKBRIdentifier" found!
    """
    value = utils.getDfCellValue(self.df, 'targetKBRIdentifier', kbrIdentifier, 'targetBnFIdentifier')
    if value == bnfIdentifier:
      return True
    else:
      return False

  # ---------------------------------------------------------------------------
  def kbrAndKBIdentifierOnSameRow(self, kbrIdentifier, kbIdentifier):
    """Returns True if a KBR manifestation with the given KBR ID exists on the same row as a KB manifestation with the given BnF ID.
    >>> data = DataprofileTestHelper([{"targetKBRIdentifier": "KBR book 4", "name": "john", "targetKBIdentifier": "KB book 4"},{"targetKBRIdentifier": 2, "name": "jane"}])

    Returns True if a row is found where both identifiers are present
    >>> data.kbrAndKBIdentifierOnSameRow("KBR book 4", "KB book 4")
    True

    If there is no row, for example with KBRID 1 and KBID 2, then False is returned
    >>> data.kbrAndKBIdentifierOnSameRow("KBR book 4",2)
    False

    If  there is even no row with the given KBR identifier found a ValueError is raised
    >>> data.kbrAndKBIdentifierOnSameRow(11,22)
    Traceback (most recent call last):
     ...
    ValueError: No row with ID "11" in column "targetKBRIdentifier" found!

    >>> data2 = DataprofileTestHelper([{"targetKBRIdentifier": 1, "name": "john", "targetKBIdentifier": ""},{"targetKBRIdentifier": 2, "targetKBIdentifier": 2, "name": "jane"}])

    If there is no KB identifier (empty value) then False is returned
    >>> data2.kbrAndKBIdentifierOnSameRow(1,1)
    False
    >>> data2.kbrAndKBIdentifierOnSameRow(1,2)
    False
    >>> data2.kbrAndKBIdentifierOnSameRow(2,2)
    True

    >>> data3 = DataprofileTestHelper([{"targetKBRIdentifier": 1, "name": "john", "targetKBIdentifier": "", "name": ""},{"targetKBRIdentifier": 2, "targetKBIdentifier": "2", "name": "jane"}, {"targetKBRIdentifier": 2, "targetKBIdentifier": 2}])

    If a KBR identifier is found more than once an error is raised
    >>> data3.kbrAndKBIdentifierOnSameRow(2,2)
    Traceback (most recent call last):
     ...
    ValueError: More than one row with ID "2" in column "targetKBRIdentifier" found!
    """
    value = utils.getDfCellValue(self.df, 'targetKBRIdentifier', kbrIdentifier, 'targetKBIdentifier')
    if value == kbIdentifier:
      return True
    else:
      return False

  # ---------------------------------------------------------------------------
  def kbAndBnFIdentifierOnSameRow(self, kbIdentifier, bnfIdentifier):
    """Returns True if a KB manifestation with the given KB ID exists on the same row as a BnF manifestation with the given BnF ID.
    >>> data = DataprofileTestHelper([{"targetKBIdentifier": "KB book 4", "name": "john", "targetBnFIdentifier": "BnF book 4"},{"targetKBIdentifier": 2, "name": "jane"}])

    Returns True if a row is found where both identifiers are present
    >>> data.kbAndBnFIdentifierOnSameRow("KB book 4", "BnF book 4")
    True

    If there is no row, for example with KBID 1 and BnFID 2, then False is returned
    >>> data.kbAndBnFIdentifierOnSameRow("KB book 4",2)
    False

    If  there is even no row with the given KB identifier found a ValueError is raised
    >>> data.kbAndBnFIdentifierOnSameRow(11,22)
    Traceback (most recent call last):
     ...
    ValueError: No row with ID "11" in column "targetKBIdentifier" found!

    >>> data2 = DataprofileTestHelper([{"targetKBIdentifier": 1, "name": "john", "targetBnFIdentifier": ""},{"targetKBIdentifier": 2, "targetBnFIdentifier": 2, "name": "jane"}])

    If there is no BnF identifier (empty value) then False is returned
    >>> data2.kbAndBnFIdentifierOnSameRow(1,1)
    False
    >>> data2.kbAndBnFIdentifierOnSameRow(1,2)
    False
    >>> data2.kbAndBnFIdentifierOnSameRow(2,2)
    True

    >>> data3 = DataprofileTestHelper([{"targetKBIdentifier": 1, "name": "john", "targetBnFIdentifier": "", "name": ""},{"targetKBIdentifier": 2, "targetBnFIdentifier": "2", "name": "jane"}, {"targetKBIdentifier": 2, "targetBnFIdentifier": 2}])

    If a KB identifier is found more than once an error is raised
    >>> data3.kbAndBnFIdentifierOnSameRow(2,2)
    Traceback (most recent call last):
     ...
    ValueError: More than one row with ID "2" in column "targetKBIdentifier" found!
    """
    value = utils.getDfCellValue(self.df, 'targetKBIdentifier', kbIdentifier, 'targetBnFIdentifier')
    if value == bnfIdentifier:
      return True
    else:
      return False




  # ---------------------------------------------------------------------------
  def targetIdentifierContainsAuthorString(self, identifier, authorString):
    """Returns True if a manifestation with the given ID contains the given author string.
    >>> data = DataprofileTestHelper([{"targetIdentifier": 1, "name": "myBook", "authorIdentifiers": "sven (12, 34)"},{"targetIdentifier": 2, "name": "otherBook"}])
    >>> data.targetIdentifierContainsAuthorString(1, "sven (12, 34)")
    True
    >>> data.targetIdentifierContainsAuthorString(1, "john")
    False
    >>> data.targetIdentifierContainsAuthorString(1, "12")
    True
    """
    selection = utils.getDfCellValue(self.df, 'targetIdentifier', identifier, 'authorIdentifiers')
    return (authorString in selection)

  # ---------------------------------------------------------------------------
  def targetIdentifierContainsIllustratorString(self, identifier, illustratorString):
    """Returns True if a manifestation with the given ID contains the given illustrator string.
    >>> data = DataprofileTestHelper([{"targetIdentifier": 1, "name": "myBook", "illustratorIdentifiers": "sven (12, 34)"},{"targetIdentifier": 2, "name": "otherBook"}])
    >>> data.targetIdentifierContainsIllustratorString(1, "sven (12, 34)")
    True
    >>> data.targetIdentifierContainsIllustratorString(1, "john")
    False
    >>> data.targetIdentifierContainsIllustratorString(1, "12")
    True
    """
    selection = utils.getDfCellValue(self.df, 'targetIdentifier', identifier, 'illustratorIdentifiers')
    return (illustratorString in selection)

  # ---------------------------------------------------------------------------
  def targetIdentifierContainsScenaristString(self, identifier, scenaristString):
    """Returns True if a manifestation with the given ID contains the given scenarist string.
    >>> data = DataprofileTestHelper([{"targetIdentifier": 1, "name": "myBook", "scenaristIdentifiers": "sven (12, 34)"},{"targetIdentifier": 2, "name": "otherBook"}])
    >>> data.targetIdentifierContainsScenaristString(1, "sven (12, 34)")
    True
    >>> data.targetIdentifierContainsScenaristString(1, "john")
    False
    >>> data.targetIdentifierContainsScenaristString(1, "12")
    True
    """
    selection = utils.getDfCellValue(self.df, 'targetIdentifier', identifier, 'scenaristIdentifiers')
    return (scenaristString in selection)

  # ---------------------------------------------------------------------------
  def targetIdentifierContainsKBIdentifierString(self, identifier, kbIdentifierString):
    """Returns True if a manifestation with the given ID contains the given KBIdentifier string.
    >>> data = DataprofileTestHelper([{"targetIdentifier": 1, "name": "myBook", "targetKBIdentifier": "sven (12, 34)"},{"targetIdentifier": 2, "name": "otherBook"}])
    >>> data.targetIdentifierContainsKBIdentifierString(1, "sven (12, 34)")
    True
    >>> data.targetIdentifierContainsKBIdentifierString(1, "john")
    False
    >>> data.targetIdentifierContainsKBIdentifierString(1, "12")
    True
    """
    selection = utils.getDfCellValue(self.df, 'targetIdentifier', identifier, 'targetKBIdentifier')
    return (kbIdentifierString in selection)



# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
