import pandas as pd
import utils

class DataprofileTestHelper:

  # ---------------------------------------------------------------------------
  def __init__(self, data):
    self.df = pd.DataFrame(data)
    print('DATA START')
    print(data)
    print('DATA END')
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
    >>> data = DataprofileTestHelper([{"targetTextKBRIdentifier": 1, "name": "john"},{"targetTextKBRIdentifier": 2, "name": "jane"}])
    >>> data.kbrTargetIdentifierExists(2)
    True
    >>> data.kbrTargetIdentifierExists(4)
    False
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      value = utils.getDfCellValue(self.df, "targetTextKBRIdentifier", identifier, "targetTextKBRIdentifier")
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
      value = utils.getDfCellValue(self.df, "targetTextBnFIdentifier", identifier, "targetTextBnFIdentifier")
      if value == identifier:
        return True
      else:
        return False
    except:
      return False

  # ---------------------------------------------------------------------------
  def kbTargetIdentifierExists(self, identifier):
    """Returns True if a KB manifestation with the given ID exists.
    >>> data = DataprofileTestHelper([{"targetTextKBIdentifier": 1, "name": "john"}, {"targetTextKBIdentifier": 2, "name": "jane"}, {"targetTextKBRIdentifier": 3, "name": "test", "targetTextKBIdentifier": ""}, {"targetTextKBRIdentifier": 4}, {"targetTextKBIdentifier": "KB book 22"}])
    >>> data.kbTargetIdentifierExists(2)
    True
    >>> data.kbTargetIdentifierExists(4)
    False
    >>> data.kbTargetIdentifierExists("KB book 22")
    True
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      value = utils.getDfCellValue(self.df, "targetTextKBIdentifier", identifier, "targetTextKBIdentifier")
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
    value = utils.getDfCellValue(self.df, 'targetTextKBRIdentifier', kbrIdentifier, 'targetTextBnFIdentifier')
    if value == bnfIdentifier:
      return True
    else:
      return False

  # ---------------------------------------------------------------------------
  def kbrAndKBIdentifierOnSameRow(self, kbrIdentifier, kbIdentifier):
    """Returns True if a KBR manifestation with the given KBR ID exists on the same row as a KB manifestation with the given BnF ID.
    >>> data = DataprofileTestHelper([{"targetTextKBRIdentifier": "KBR book 4", "name": "john", "targetTextKBIdentifier": "KB book 4"},{"targetTextKBRIdentifier": 2, "name": "jane"}])

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
    ValueError: No row with ID "11" in column "targetTextKBRIdentifier" found!

    >>> data2 = DataprofileTestHelper([{"targetTextKBRIdentifier": 1, "name": "john", "targetTextKBIdentifier": ""},{"targetTextKBRIdentifier": 2, "targetTextKBIdentifier": 2, "name": "jane"}])

    If there is no KB identifier (empty value) then False is returned
    >>> data2.kbrAndKBIdentifierOnSameRow(1,1)
    False
    >>> data2.kbrAndKBIdentifierOnSameRow(1,2)
    False
    >>> data2.kbrAndKBIdentifierOnSameRow(2,2)
    True

    >>> data3 = DataprofileTestHelper([{"targetTextKBRIdentifier": 1, "name": "john", "targetTextKBIdentifier": "", "name": ""},{"targetTextKBRIdentifier": 2, "targetTextKBIdentifier": "2", "name": "jane"}, {"targetTextKBRIdentifier": 2, "targetTextKBIdentifier": 2}])

    If a KBR identifier is found more than once an error is raised
    >>> data3.kbrAndKBIdentifierOnSameRow(2,2)
    Traceback (most recent call last):
     ...
    ValueError: More than one row with ID "2" in column "targetTextKBRIdentifier" found!
    """
    value = utils.getDfCellValue(self.df, 'targetTextKBRIdentifier', kbrIdentifier, 'targetTextKBIdentifier')
    if value == kbIdentifier:
      return True
    else:
      return False

  # ---------------------------------------------------------------------------
  def kbAndBnFIdentifierOnSameRow(self, kbIdentifier, bnfIdentifier):
    """Returns True if a KB manifestation with the given KB ID exists on the same row as a BnF manifestation with the given BnF ID.
    >>> data = DataprofileTestHelper([{"targetTextKBIdentifier": "KB book 4", "name": "john", "targetTextBnFIdentifier": "BnF book 4"},{"targetTextKBIdentifier": 2, "name": "jane"}])

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
    ValueError: No row with ID "11" in column "targetTextKBIdentifier" found!

    >>> data2 = DataprofileTestHelper([{"targetTextKBIdentifier": 1, "name": "john", "targetTextBnFIdentifier": ""},{"targetTextKBIdentifier": 2, "targetTextBnFIdentifier": 2, "name": "jane"}])

    If there is no BnF identifier (empty value) then False is returned
    >>> data2.kbAndBnFIdentifierOnSameRow(1,1)
    False
    >>> data2.kbAndBnFIdentifierOnSameRow(1,2)
    False
    >>> data2.kbAndBnFIdentifierOnSameRow(2,2)
    True

    >>> data3 = DataprofileTestHelper([{"targetTextKBIdentifier": 1, "name": "john", "targetTextBnFIdentifier": "", "name": ""},{"targetTextKBIdentifier": 2, "targetTextBnFIdentifier": "2", "name": "jane"}, {"targetTextKBIdentifier": 2, "targetTextBnFIdentifier": 2}])

    If a KB identifier is found more than once an error is raised
    >>> data3.kbAndBnFIdentifierOnSameRow(2,2)
    Traceback (most recent call last):
     ...
    ValueError: More than one row with ID "2" in column "targetTextKBIdentifier" found!
    """
    value = utils.getDfCellValue(self.df, 'targetTextKBIdentifier', kbIdentifier, 'targetTextBnFIdentifier')
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

 
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
