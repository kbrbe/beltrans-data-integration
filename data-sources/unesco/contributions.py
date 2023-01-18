
# -----------------------------------------------------------------------------
class Contribution:

  def __init__(self):
    self.identifiers = dict()
    self.counter = 1

  def getShortIdentifier(self, longIdentifier):
    """Always returns a short identifier for the given longIdentifier.
    >>> c1 = Contribution()
    >>> c1.getShortIdentifier('sven123')
    1

    >>> c1.getShortIdentifier('anotherLongIdentifier')
    2

    >>> c1.getShortIdentifier('sven123')
    1
    """

    if longIdentifier in self.identifiers:
      return self.identifiers[longIdentifier]
    else:
      self.identifiers[longIdentifier] = self.counter
      self.counter += 1
      return self.identifiers[longIdentifier]

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
