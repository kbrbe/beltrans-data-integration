import pandas as pd
import utils

class GeonameIdentifierEnrichmentTestHelper:

  # ---------------------------------------------------------------------------
  def __init__(self, data):
    self.df = pd.DataFrame(data)
    print(self.df)

  # ---------------------------------------------------------------------------
  def getKBRIdentifierCountry(self, identifier):
    return utils.getDfCellValue(self.df, "targetKBRIdentifier", identifier, "targetCountryOfPublication")

  # ---------------------------------------------------------------------------
  def getKBRIdentifierLocation(self, identifier):
    return utils.getDfCellValue(self.df, "targetKBRIdentifier", identifier, "targetPlaceOfPublication")

# ---------------------------------------------------------------------------
  def getKBRIdentifierPlaceOfPublicationIdentifier(self, identifier):
    return utils.getDfCellValue(self.df, "targetKBRIdentifier", identifier, "targetPlaceOfPublicationIdentifier")

  # ---------------------------------------------------------------------------
  def getKBRIdentifierPlaceOfPublicationIdentifiers(self, identifier):
    """Get an array of found identifiers (useful if there are more than one row with given identifier)."""
    return utils.getDfValues(self.df, "targetKBRIdentifier", identifier, "targetPlaceOfPublicationIdentifier")

  # ---------------------------------------------------------------------------
  def placeOfPublicationIdentifierExistsforKBRIdentifier(self, placeIdentifier, kbrIdentifier):
    """Returns True if a relationship between kbrIdentifier and placeIdentifier exists.
    >>> data = GeonameIdentifierEnrichmentTestHelper([
    ... {"targetKBRIdentifier": "1", "targetPlaceOfPublicationIdentifier": "111"},
    ... {"targetKBRIdentifier": "1", "targetPlaceOfPublicationIdentifier": "222"},
    ... {"targetKBRIdentifier": "2", "targetPlaceOfPublicationIdentifier": "333"}])
    >>> data.placeOfPublicationIdentifierExistsforKBRIdentifier("111", "1")
    True
    >>> data.placeOfPublicationIdentifierExistsforKBRIdentifier("222", "1")
    True
    >>> data.placeOfPublicationIdentifierExistsforKBRIdentifier("111", "2")
    False
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      values = utils.getDfValues(self.df, "targetKBRIdentifier", kbrIdentifier, "targetPlaceOfPublicationIdentifier")
      if placeIdentifier in values:
        return True
      else:
        return False
    except:
      return False

  # ---------------------------------------------------------------------------
  def placeOfPublicationLongitudeExistsforKBRIdentifier(self, longitude, kbrIdentifier):
    """Returns True if a relationship between kbrIdentifier and longitude exists.
    >>> data = GeonameIdentifierEnrichmentTestHelper([
    ... {"targetKBRIdentifier": "1", "targetPlaceOfPublicationLongitude": "111"},
    ... {"targetKBRIdentifier": "1", "targetPlaceOfPublicationLongitude": "222"},
    ... {"targetKBRIdentifier": "2", "targetPlaceOfPublicationLongitude": "333"}])
    >>> data.placeOfPublicationLongitudeExistsforKBRIdentifier("111", "1")
    True
    >>> data.placeOfPublicationLongitudeExistsforKBRIdentifier("222", "1")
    True
    >>> data.placeOfPublicationLongitudeExistsforKBRIdentifier("111", "2")
    False
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      values = utils.getDfValues(self.df, "targetKBRIdentifier", kbrIdentifier, "targetPlaceOfPublicationLongitude")
      if longitude in values:
        return True
      else:
        return False
    except:
      return False

  # ---------------------------------------------------------------------------
  def placeOfPublicationLatitudeExistsforKBRIdentifier(self, latitude, kbrIdentifier):
    """Returns True if a relationship between kbrIdentifier and latitude exists.
    >>> data = GeonameIdentifierEnrichmentTestHelper([
    ... {"targetKBRIdentifier": "1", "targetPlaceOfPublicationLatitude": "111"},
    ... {"targetKBRIdentifier": "1", "targetPlaceOfPublicationLatitude": "222"},
    ... {"targetKBRIdentifier": "2", "targetPlaceOfPublicationLatitude": "333"}])
    >>> data.placeOfPublicationLatitudeExistsforKBRIdentifier("111", "1")
    True
    >>> data.placeOfPublicationLatitudeExistsforKBRIdentifier("222", "1")
    True
    >>> data.placeOfPublicationLatitudeExistsforKBRIdentifier("111", "2")
    False
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      values = utils.getDfValues(self.df, "targetKBRIdentifier", kbrIdentifier, "targetPlaceOfPublicationLatitude")
      if latitude in values:
        return True
      else:
        return False
    except:
      return False

# ---------------------------------------------------------------------------
  def getKBRIdentifierPlaceOfPublicationLatitude(self, identifier):
    return utils.getDfCellValue(self.df, "targetKBRIdentifier", identifier, "targetPlaceOfPublicationLatitude")

  # ---------------------------------------------------------------------------
  def getKBRIdentifierPlaceOfPublicationLatitudes(self, identifier):
    """Get an array of found latitudes (useful if there are more than one row with given identifier)."""
    return utils.getDfValues(self.df, "targetKBRIdentifier", identifier, "targetPlaceOfPublicationLatitude")

# ---------------------------------------------------------------------------
  def getKBRIdentifierPlaceOfPublicationLongitude(self, identifier):
    return utils.getDfCellValue(self.df, "targetKBRIdentifier", identifier, "targetPlaceOfPublicationLongitude")

  # ---------------------------------------------------------------------------
  def getKBRIdentifierPlaceOfPublicationLongitudes(self, identifier):
    """Get an array of found longitudes (useful if there are more than one row with given identifier)."""
    return utils.getDfValues(self.df, "targetKBRIdentifier", identifier, "targetPlaceOfPublicationLongitude")

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
