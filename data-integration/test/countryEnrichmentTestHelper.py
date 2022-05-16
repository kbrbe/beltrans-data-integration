import pandas as pd
import utils

class CountryEnrichmentTestHelper:

  # ---------------------------------------------------------------------------
  def __init__(self, data):
    self.df = pd.DataFrame(data)

  # ---------------------------------------------------------------------------
  def kbrIdentifierHasCountry(self, identifier, country):
    """
    >>> data = CountryEnrichmentTestHelper([{"targetIdentifier": "1", "targetCountryOfPublication": "Belgium"},{"targetIdentifier": "2", "targetCountryOfPublication": "Germany"}, {"targetIdentifier": "3", "targetCountryOfPublication": ""}])
    >>> data.kbrIdentifierHasCountry("1", "Belgium")
    True
    >>> data.kbrIdentifierHasCountry("2", "Germany")
    True
    >>> data.kbrIdentifierHasCountry("1", "France")
    False
    >>> data.kbrIdentifierHasCountry("3", "")
    True
    """
    foundCountry = utils.getDfCellValue(self.df, "targetIdentifier", identifier, "targetCountryOfPublication")

  # ---------------------------------------------------------------------------
  def getKBRIdentifierCountry(self, identifier):
    return utils.getDfCellValue(self.df, "targetIdentifier", identifier, "targetCountryOfPublication")

  # ---------------------------------------------------------------------------
  def getKBRIdentifierLocation(self, identifier):
    return utils.getDfCellValue(self.df, "targetIdentifier", identifier, "targetPlaceOfPublication")
