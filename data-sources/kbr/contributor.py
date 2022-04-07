from abc import ABC, abstractmethod

# -----------------------------------------------------------------------------
class Contributor(ABC):

  def __init__(self, identifier, name, roles, roleDelimiter=';'):
    self.identifier = identifier
    self.name = name
    self.setRoles(roles, roleDelimiter)

  @classmethod
  def fromTuple(cls, cTuple):
    """Instead of initializing an instance with parameters, a tuple can be given."""
    return cls(cTuple[0], cTuple[1], cTuple[2])

  @abstractmethod
  def setRoles(self, roles, roleDelimiter):
    pass

  def getIdentifier(self):
    return self.identifier

  def getName(self):
    return self.name

  def getRoles(self):
    """Returns the roles as array, if there is only one role an array with one element is returned.
    >>> c1 = PersonContributor('1', 'sven', 'aut;trl')
    >>> c1.getRoles()
    ['aut', 'trl']
    >>> c2 = PersonContributor('1', 'sven', 'aut')
    >>> c2.getRoles()
    ['aut']

    >>> c3 = PersonContributor('1', 'sven', 'aut,ill', roleDelimiter=',')
    >>> c3.getRoles()
    ['aut', 'ill']

    >>> c4 = PersonContributor('1', 'sven', '', roleDelimiter=',')
    >>> c4.getRoles()
    ['aut']

    >>> c5 = OrganizationalContributor('1', 'sven', '', roleDelimiter=',')
    >>> c5.getRoles()
    ['pbl']

    >>> c6 = PersonContributor.fromTuple(('1', 'sven', 'ill'))
    >>> c6.getRoles()
    ['ill']
    """
    return self.roles


# -----------------------------------------------------------------------------
class PersonContributor(Contributor):

  def setRoles(self, roles, roleDelimiter): 
    # if no role is set it is an author (confirmed with KBRs cataloguing agency)
    if roles == '':
      self.roles = ['aut']
    else:
      self.roles = roles.split(roleDelimiter)

# -----------------------------------------------------------------------------
class OrganizationalContributor(Contributor):

  def __init__(self, identifier, name, roles, roleDelimiter=';'):
    self.uncertainRole = False
    super().__init__(identifier, name, roles, roleDelimiter)

  def setRoles(self, roles, roleDelimiter): 
    # if no role is set it is most likely a publisher 
    if roles == '':
      self.roles = ['pbl']
      self.uncertainRole = True
    else:
      self.roles = roles.split(roleDelimiter)

  def roleUncertain(self):
    """If the given role was empty this method will return true, because it is most likely a publisher, not necessarily.
    >>> c1 = OrganizationalContributor('1', 'sven', 'pbl')
    >>> c1.roleUncertain()
    False
    >>> c2 = OrganizationalContributor('1', 'sven', '')
    >>> c2.roleUncertain()
    True
    """
    return self.uncertainRole


# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
