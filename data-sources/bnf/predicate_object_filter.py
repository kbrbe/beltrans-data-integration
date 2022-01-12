from abc import ABC, abstractmethod

class PredicateObjectFilter(ABC):

  @abstractmethod
  def passFilter(value):
    pass

  @abstractmethod
  def getPredicates(value):
    pass

  @abstractmethod
  def getNumberPassed(value):
    pass

  @abstractmethod
  def getNumberChecked(value):
    pass
  
# ------------------------------------------------------------------------------
class PredicateObjectConfigFilter(PredicateObjectFilter):

  # ----------------------------------------------------------------------------
  def __init__(self, filterArray):

    self.filterCriteria = []
    self.numberChecked = 0
    self.numberPassed = 0

    for row in filterArray:
      if ';' in row[2]:
        self.filterCriteria.append((row[0], row[1], row[2].split(';')))
      else:
        self.filterCriteria.append((row[0], row[1], row[2]))

  # --------------------------------------------------------------------------
  def getPredicates(self):
    """
    >>> f = PredicateObjectConfigFilter([["schema:nationality","=","be"], ["ex:year","in","1970;1971"]])
    >>> f.getPredicates()
    ['schema:nationality', 'ex:year']
    """
    predicates = []
    for r in self.filterCriteria:
      predicates.append(r[0])
    return predicates

  # --------------------------------------------------------------------------
  def getNumberChecked(self):
    """
    >>> f = PredicateObjectConfigFilter([["schema:nationality","=","be"]])
    >>> f.passFilter("be")
    True
    >>> f.passFilter("de")
    False
    >>> f.getNumberChecked()
    2
    """
    return self.numberChecked

  # --------------------------------------------------------------------------
  def getNumberPassed(self):
    """
    >>> f = PredicateObjectConfigFilter([["schema:nationality","=","be"]])
    >>> f.passFilter("be")
    True
    >>> f.passFilter("de")
    False
    >>> f.getNumberPassed()
    1
    """
    return self.numberPassed

  # --------------------------------------------------------------------------
  def passFilter(self, value):
    """
    >>> f = PredicateObjectConfigFilter([["schema:nationality","=","be"]])
    >>> f.passFilter("be")
    True
    >>> f = PredicateObjectConfigFilter([["schema:nationality","=","be"]])
    >>> f.passFilter("de")
    False
    >>> f = PredicateObjectConfigFilter([["schema:copyrightYear",">","1970"]])
    >>> f.passFilter("1971")
    True
    >>> f = PredicateObjectConfigFilter([["schema:copyrightYear",">","1970"]])
    >>> f.passFilter("1969")
    False
    >>> f = PredicateObjectConfigFilter([["schema:copyrightYear","<","2020"]])
    >>> f.passFilter("2000")
    True
    >>> f = PredicateObjectConfigFilter([["schema:copyrightYear","<","2020"]])
    >>> f.passFilter("2021")
    False
    >>> f = PredicateObjectConfigFilter([["ex:year","in","1970;1971"]])
    >>> f.passFilter("1971")
    True
    >>> f = PredicateObjectConfigFilter([["ex:year","in","1970;1971"]])
    >>> f.passFilter("1972")
    False
    """

    filterPass = False
    self.numberChecked += 1

    for (predicate, operator, filterValue) in self.filterCriteria:

      # perform filter check
      if operator == '=':
        if value == filterValue:
          filterPass = True
      elif operator == 'in':
        if value in filterValue:
          filterPass = True
      elif operator == '>':
        if value > filterValue:
          filterPass = True
      elif operator == '<':
        if value < filterValue:
          filterPass = True
      else:
        print(f'Error: unknown operator {operator}')

    if filterPass:
      self.numberPassed += 1

    return filterPass



# ------------------------------------------------------------------------------
class PredicateObjectLookupFilter(PredicateObjectFilter):

  def passFilter(value):
    pass

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
