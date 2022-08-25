from string import Template

# -----------------------------------------------------------------------------
class ContributorUpdateQuery():
  """With this query builder class, one can generate a SPARQL UPDATE query to update a person or organization
  of a target graph with certain properties from a source graph and a schema:sameAs link back to the person/organization
  of the source graph.

  The properties added to the target graph are identifiers described using the BIBFRAME ontology,
  i.e. instances of bf:Identifier or bf:Isni to which is linked via bf:identifiedBy.
  The update will always add the nationality from the source graph as well as add a schema:sameAs link from target to source.
  On the one hand it can be configured which identifier is used to identify a match between source and target graph
  and on the other hand, it can be configured which other identifiers from the source will be added to the target.

  For example, the following call will generate a SPARQL UPDATE query which tries to make a link between
  source and target graph using the ISNI identifier and will add VIAF and Wikidata identifiers to the target.

  qb = ContributorUpdateQuery("KBR", "http://kbr-data", "http://integrated-data", "ISNI", ["VIAF", "Wikidata"])
  """

  # ---------------------------------------------------------------------------
  def __init__(self, source, sourceGraph: str, targetGraph: str, identifierName: str, identifiersToAdd: list,
               nationalityProperty='schema:nationality', personClass='schema:Person',
               organizationClass='schema:Organization'):
    """

    Parameters
    ----------
    source :str
        The name of the data source which will be used for comments, for example "KBR"
    sourceGraph : str
        The name of the source graph without brackets, e.g. http://kbr-linked-authorities
    targetGraph : str
        The name of the target graph without brackets, e.g. http://beltrans-contributors
    identifierName : str
        The name of the identifier used to link a source to a target record, e.g. ISNI or VIAF
    identifiersToAdd : list
        The names of other identifiers which will be added from source to target if a match was found.
        On the one hand, this name is used to refer to the name of the identifier (rdfs:label) according to BIBFRAME
        and on the other hand to build variable names in the SPARQL query.
    nationalityProperty : str
        The RDF property used to fetch nationality information from the source graph, the default is schema:nationality
    personClass : str
        The RDF class used to identify a person record in the source graph, the default is schema:Person
    organizationClass : str
        The RDF class used to identify an organization record in the source graph, the default is schema:Organization
    """
    self.source = source
    self.sourceGraph = sourceGraph
    self.targetGraph = targetGraph
    self.identifierName = identifierName
    self.identifiersToAdd = identifiersToAdd
    self.nationalityProperty = nationalityProperty
    self.personClass = personClass
    self.organizationClass = organizationClass

    self.baseURL = "http://kbr.be/id/data/"

  # ---------------------------------------------------------------------------
  def _buildQuery(self):

    insertBeginPattern = Template("""
    graph <$targetGraph> {
      ?contributorURI schema:nationality ?contributorNationality ;
                      schema:sameAs ?localContributorURI .

    """)

    query = "INSERT { "

    query += insertBeginPattern.substitute(targetGraph=self.targetGraph)


    # bf:identifiedBy links, e.g. bf:identifiedBy ?viafEntityURI
    for identifier in self.identifiersToAdd:
      query += self._getINSERTIdentifiedByTriplePattern(identifier)

    # definition of identifiers, e.g. ?viafEntityURI a bf:Identifier
    for identifier in self.identifiersToAdd:
      query += self._getINSERTTriplePattern(identifier, self.source, self.identifierName)

    query += "} "  # end of graph block
    query += "} "  # end of INSERT block

    query += "WHERE { "

    query += self._getFilterSourceQuadPattern(self.sourceGraph, self.personClass, self.organizationClass)
    query += self._getSourceNationalityQuadPattern(self.sourceGraph, self.nationalityProperty)
    query += self._getFilterExistsQuadPattern(self.sourceGraph, self.targetGraph, self.identifierName)

    for identifier in self.identifiersToAdd:
      query += self._getIdentifierQuadPattern(self.identifierName, self.sourceGraph, optional=True)

    query += ' }'
    return query

  # ---------------------------------------------------------------------------
  def _getINSERTIdentifiedByTriplePattern(self, identifier):
    pattern = Template("""?contributorURI bf:identifiedBy ?${identifier}EntityURI .
    """)
    return pattern.substitute(identifier=identifier)

  # ---------------------------------------------------------------------------
  def _getFilterSourceQuadPattern(self, sourceGraph, personClass, organizationClass):
    pattern = Template("""
    graph <$sourceGraph> { ?localContributorURI a ?contributorType . }
    FILTER( ?contributorType IN ($personClass, $organizationClass) ) 
    
    """)
    return pattern.substitute(sourceGraph=sourceGraph, personClass=personClass, organizationClass=organizationClass)

  # ---------------------------------------------------------------------------
  def _getSourceNationalityQuadPattern(self, sourceGraph, nationalityProperty):
    pattern = Template("""
    OPTIONAL { graph <$sourceGraph> { ?localContributorURI $nationalityProperty ?contributorNationality . } }

    """)
    return pattern.substitute(sourceGraph=sourceGraph, nationalityProperty=nationalityProperty)

  # ---------------------------------------------------------------------------
  def _getFilterExistsQuadPattern(self, sourceGraph, targetGraph, identifier):
    """This function returns triple patterns for the WHERE clause used for the update functionality,
       i.e. only if the filter returns true the update will be performed.
       
    """

    identifierType = ' a bf:Isni ; ' if identifier == 'ISNI' or identifier == 'isni' else ' a bf:Identifier ; rdfs:label "$identifier" ; '

    pattern = Template("""
    graph <$sourceGraph> {
      ?localContributorURI bf:identifiedBy ?${identifier}Entity .

      ?${identifier}Entity """ + identifierType +
    """
                            rdf:value ?${identifier}Local .
    }

    OPTIONAL {
      graph <$targetGraph> {
        ?contributorURI bf:identifiedBy ?${identifier}Entity .
        ?${identifier}Entity """ + identifierType +
    """
                             rdf:value ?${identifier}Local .
      }
    }

    FILTER EXISTS {
      graph <$targetGraph> {
        ?contributorURI bf:identifiedBy ?${identifier}Entity .
        ?${identifier}Entity """ + identifierType +
    """
                             rdf:value ?${identifier}Local .
      }
    }
    """)
    return pattern.substitute(sourceGraph=sourceGraph, targetGraph=targetGraph, identifier=identifier)


  # ---------------------------------------------------------------------------
  def _getIdentifierQuadPattern(self, identifier, namedGraph, optional=False):
    """This function returns possibly optional quad patterns for the WHERE clause,
       for example if a particular identifier such as VIAF or Wikidata should be queried too.
    """

    identifierType = ' a bf:Isni ; ' if identifier == 'ISNI' or identifier == 'isni' else ' a bf:Identifier ; rdfs:label "$identifier" ; '

    pattern = Template("""
      graph <$graph> {
        ?localContributorURI bf:identifiedBy ?${identifier}Entity .

        ${identifier}Entity """ + identifierType + 
     """
                             rdf:value ?${identifier} .
      }
      BIND(iri(concat("${baseURL}identifier_${identifier}_", ?${identifier})) as ?${identifier}EntityURI)
    """)
    queryPart = pattern.substitute(identifier=identifier,
                              graph=namedGraph,
                              baseURL=self.baseURL)
    if optional:
      return 'OPTIONAL { ' + queryPart + ' } '
    else:
      return queryPart


  # ---------------------------------------------------------------------------
  def _getINSERTTriplePattern(self, identifier, source, linkingIdentifier):
    """"""

    identifierType = ' a bf:Isni ; ' if identifier == 'ISNI' or identifier == 'isni' else ' a bf:Identifier ; rdfs:label "$identifier" ; '

    pattern = Template("""
    ?${identifier}EntityURI """ + identifierType +
    """
        rdfs:comment "Created from $source via $linkingIdentifier" ;
        rdfs:value ?${identifier} .

    """
    )
    return pattern.substitute(identifier=identifier, source=source, linkingIdentifier=linkingIdentifier)

  # ---------------------------------------------------------------------------
  def getQueryString(self):
    return self._buildQuery()
