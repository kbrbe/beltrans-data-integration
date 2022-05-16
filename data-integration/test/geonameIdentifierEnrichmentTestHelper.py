import pandas as pd
import utils

class GeonameIdentifierEnrichmentTestHelper:

  # ---------------------------------------------------------------------------
  def __init__(self, data):
    self.df = pd.DataFrame(data)

  # ---------------------------------------------------------------------------
  def getTargetIdentifierCountry(self, identifier):
    return utils.getDfCellValue(self.df, "targetIdentifier", identifier, "targetCountryOfPublication")

  # ---------------------------------------------------------------------------
  def getTargetIdentifierLocation(self, identifier):
    return utils.getDfCellValue(self.df, "targetIdentifier", identifier, "targetPlaceOfPublication")

# ---------------------------------------------------------------------------
  def getTargetIdentifierPlaceOfPublicationIdentifier(self, identifier):
    return utils.getDfCellValue(self.df, "targetIdentifier", identifier, "targetPlaceOfPublicationIdentifier")

  # ---------------------------------------------------------------------------
  def getTargetIdentifierPlaceOfPublicationIdentifiers(self, identifier):
    """Get an array of found identifiers (useful if there are more than one row with given identifier)."""
    return utils.getDfValues(self.df, "targetIdentifier", identifier, "targetPlaceOfPublicationIdentifier")

  # ---------------------------------------------------------------------------
  def placeOfPublicationIdentifierExistsforTargetIdentifier(self, placeIdentifier, kbrIdentifier):
    """Returns True if a relationship between kbrIdentifier and placeIdentifier exists.
    >>> data = GeonameIdentifierEnrichmentTestHelper([
    ... {"targetIdentifier": "1", "targetPlaceOfPublicationIdentifier": "111"},
    ... {"targetIdentifier": "1", "targetPlaceOfPublicationIdentifier": "222"},
    ... {"targetIdentifier": "2", "targetPlaceOfPublicationIdentifier": "333"}])
    >>> data.placeOfPublicationIdentifierExistsforTargetIdentifier("111", "1")
    True
    >>> data.placeOfPublicationIdentifierExistsforTargetIdentifier("222", "1")
    True
    >>> data.placeOfPublicationIdentifierExistsforTargetIdentifier("111", "2")
    False
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      values = utils.getDfValues(self.df, "targetIdentifier", kbrIdentifier, "targetPlaceOfPublicationIdentifier")
      if placeIdentifier in values:
        return True
      else:
        return False
    except:
      return False

  # ---------------------------------------------------------------------------
  def placeOfPublicationLongitudeExistsforTargetIdentifier(self, longitude, kbrIdentifier):
    """Returns True if a relationship between kbrIdentifier and longitude exists.
    >>> data = GeonameIdentifierEnrichmentTestHelper([
    ... {"targetIdentifier": "1", "targetPlaceOfPublicationLongitude": "111"},
    ... {"targetIdentifier": "1", "targetPlaceOfPublicationLongitude": "222"},
    ... {"targetIdentifier": "2", "targetPlaceOfPublicationLongitude": "333"}])
    >>> data.placeOfPublicationLongitudeExistsforTargetIdentifier("111", "1")
    True
    >>> data.placeOfPublicationLongitudeExistsforTargetIdentifier("222", "1")
    True
    >>> data.placeOfPublicationLongitudeExistsforTargetIdentifier("111", "2")
    False
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      values = utils.getDfValues(self.df, "targetIdentifier", kbrIdentifier, "targetPlaceOfPublicationLongitude")
      if longitude in values:
        return True
      else:
        return False
    except:
      return False

  # ---------------------------------------------------------------------------
  def placeOfPublicationLatitudeExistsforTargetIdentifier(self, latitude, kbrIdentifier):
    """Returns True if a relationship between kbrIdentifier and latitude exists.
    >>> data = GeonameIdentifierEnrichmentTestHelper([
    ... {"targetIdentifier": "1", "targetPlaceOfPublicationLatitude": "111"},
    ... {"targetIdentifier": "1", "targetPlaceOfPublicationLatitude": "222"},
    ... {"targetIdentifier": "2", "targetPlaceOfPublicationLatitude": "333"}])
    >>> data.placeOfPublicationLatitudeExistsforTargetIdentifier("111", "1")
    True
    >>> data.placeOfPublicationLatitudeExistsforTargetIdentifier("222", "1")
    True
    >>> data.placeOfPublicationLatitudeExistsforTargetIdentifier("111", "2")
    False
    """
    # reuse the getCellValue function so also some checks are performed
    try:
      values = utils.getDfValues(self.df, "targetIdentifier", kbrIdentifier, "targetPlaceOfPublicationLatitude")
      if latitude in values:
        return True
      else:
        return False
    except:
      return False

# ---------------------------------------------------------------------------
  def getTargetIdentifierPlaceOfPublicationLatitude(self, identifier):
    return utils.getDfCellValue(self.df, "targetIdentifier", identifier, "targetPlaceOfPublicationLatitude")

  # ---------------------------------------------------------------------------
  def getTargetIdentifierPlaceOfPublicationLatitudes(self, identifier):
    """Get an array of found latitudes (useful if there are more than one row with given identifier)."""
    return utils.getDfValues(self.df, "targetIdentifier", identifier, "targetPlaceOfPublicationLatitude")

# ---------------------------------------------------------------------------
  def getTargetIdentifierPlaceOfPublicationLongitude(self, identifier):
    return utils.getDfCellValue(self.df, "targetIdentifier", identifier, "targetPlaceOfPublicationLongitude")

  # ---------------------------------------------------------------------------
  def getTargetIdentifierPlaceOfPublicationLongitudes(self, identifier):
    """Get an array of found longitudes (useful if there are more than one row with given identifier)."""
    return utils.getDfValues(self.df, "targetIdentifier", identifier, "targetPlaceOfPublicationLongitude")

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
