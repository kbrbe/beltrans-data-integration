from string import Template

from jinja2.nodes import Concat


class ContributorQuery():
    VAR_CONTRIBUTOR_URI = "?contributorURI"
    VAR_CONTRIBUTOR_NATIONALITY = "?contributorNationality"
    VAR_CONTRIBUTOR_LOCAL_URI = "?localContributorURI"
    VAR_CONTRIBUTOR_FAMILY_NAME = "?familyName"
    VAR_CONTRIBUTOR_GIVEN_NAME = "?givenName"
    VAR_CONTRIBUTOR_LABEL = "?contributorLabel"
    VAR_CONTRIBUTOR_UUID = "?uuid"

    # ---------------------------------------------------------------------------
    @classmethod
    def _getSimpleTriplePattern(cls, subject, predicate, object, graph=None, optional=False, newline=False):
        """This function builds a triple pattern.

        It can be a simple subject predicate object triple
        >>> ContributorQuery._getSimpleTriplePattern('?person', 'a', 'schema:Person')
        '?person a schema:Person .\\n        '

        It can be an optional subject predicate object triple
        >>> ContributorQuery._getSimpleTriplePattern('?person', 'a', 'schema:Person', optional=True)
        'OPTIONAL { ?person a schema:Person .\\n         }'

        It can be a quad
        >>> ContributorQuery._getSimpleTriplePattern('?person', 'a', 'schema:Person', graph='http://my-graph')
        'graph <http://my-graph> { ?person a schema:Person .\\n         }'

        And it can be an optional quad
        >>> ContributorQuery._getSimpleTriplePattern('?person', 'a', 'schema:Person', graph='http://my-graph', optional=True)
        'OPTIONAL { graph <http://my-graph> { ?person a schema:Person .\\n         } }'
        """
        pattern = Template(""" ${subject} ${predicate} ${object} . """)
        queryPart = pattern.substitute(subject=subject, predicate=predicate, object=object)
        if graph != None:
            queryPart = f'graph <{graph}> ' + '{ ' + queryPart + """ } """

        if optional:
            queryPart = """
      OPTIONAL { """ + queryPart + """ } """

        if newline:
            return queryPart + """
      """
        else:
            return queryPart

    # ---------------------------------------------------------------------------
    def _getINSERTIdentifiedByTriplePattern(self, identifier):
        return ContributorQuery._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'bf:identifiedBy',
                                                        f'?{identifier}EntityURI',
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTNationalityTriplePattern(self):
        return ContributorQuery._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'schema:nationality',
                                                        ContributorQuery.VAR_CONTRIBUTOR_NATIONALITY,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTSameAsTriplePattern(self):
        return ContributorQuery._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'schema:sameAs',
                                                        ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTIdentifierTriplePattern(self):
        return ContributorQuery._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'dcterms:identifier',
                                                        ContributorQuery.VAR_CONTRIBUTOR_UUID,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTFamilyNameTriplePattern(self):
        return ContributorQuery._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'schema:familyName',
                                                        ContributorQuery.VAR_CONTRIBUTOR_FAMILY_NAME,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTGivenNameTriplePattern(self):
        return ContributorQuery._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'schema:givenName',
                                                        ContributorQuery.VAR_CONTRIBUTOR_GIVEN_NAME,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTContributorLabelTriplePattern(self):
        return ContributorQuery._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'rdfs:label',
                                                        ContributorQuery.VAR_CONTRIBUTOR_LABEL,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTContributorCommentTriplePattern(self, comment):
        return ContributorQuery._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'rdfs:comment',
                                                        f'"{comment}"',
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTIdentifierDeclarationTriplePattern(self, identifier, source, additionalCommentText):
        """"""

        identifierType = ' a bf:Isni ; ' if identifier == 'ISNI' or identifier == 'isni' else ' a bf:Identifier ; rdfs:label "$identifier" ; '

        pattern = Template("""
    ?${identifier}EntityURI """ + identifierType +
                           """
                               rdfs:comment "$additionalCommentText" ;
                               rdf:value ?${identifier} .
                       
                           """
                           )
        return pattern.substitute(identifier=identifier, source=source, additionalCommentText=additionalCommentText)

    # ---------------------------------------------------------------------------
    def _getSourceNationalityQuadPattern(self, sourceGraph, nationalityProperty, optional=False):
        pattern = Template("""
    OPTIONAL { graph <$sourceGraph> { ?localContributorURI $nationalityProperty ?contributorNationality . } }

    """)
        queryPart = pattern.substitute(sourceGraph=sourceGraph, nationalityProperty=nationalityProperty)

        if optional:
            return 'OPTIONAL { ' + queryPart + ' } '
        else:
            return queryPart

    # ---------------------------------------------------------------------------
    @classmethod
    def _getIdentifierStringPatternBIBFRAME(cls, identifier):
        identifierType = ' a bf:Isni ; ' if identifier == 'ISNI' or identifier == 'isni' else ' a bf:Identifier ; rdfs:label "$identifier" ; '

        pattern = """
        graph <$graph> {
            $localContributorURIVariable bf:identifiedBy ?${identifier}Entity .
    
            ?${identifier}Entity""" + identifierType + \
            """
                                               rdf:value ?${identifier} .
        }
        BIND(iri(concat("${baseURL}identifier_${identifier}_", ?${identifier})) as ?${identifier}EntityURI)
        
        """
        return pattern

    # ---------------------------------------------------------------------------
    @classmethod
    def _getIdentifierStringPatternDCTERMS(cls):
        pattern = """
        graph <$graph> { $localContributorURIVariable dcterms:identifier ?${identifier}Entity . }
        BIND(iri(concat("${baseURL}identifier_${identifier}_", ?${identifier})) as ?${identifier}EntityURI)
        """
        return pattern

    # ---------------------------------------------------------------------------
    def _getIdentifierQuadPattern(self, identifier, namedGraph, optional=False):
        """This function returns possibly optional quad patterns for the WHERE clause,
           for example if a particular identifier such as VIAF or Wikidata should be queried too.
        """

        if identifier == self.source:
            pattern = Template(ContributorQuery._getIdentifierStringPatternDCTERMS())
        else:
            pattern = Template(ContributorQuery._getIdentifierStringPatternBIBFRAME(identifier))
        queryPart = pattern.substitute(identifier=identifier,
                                       graph=namedGraph,
                                       baseURL=self.baseURL,
                                       localContributorURIVariable=ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI)
        if optional:
            return 'OPTIONAL { ' + queryPart + ' } '
        else:
            return queryPart

    @classmethod
    def _getPrefixList(cls):
        return """prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix prov: <http://www.w3.org/ns/prov#>
prefix dc: <http://purl.org/dc/elements/1.1/>
prefix dcterms: <http://purl.org/dc/terms/>
prefix schema: <http://schema.org/>
prefix lang: <http://id.loc.gov/vocabulary/languages/>
prefix bibo: <http://purl.org/ontology/bibo/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX btm: <http://kbr.be/ns/beltrans/model#>
PREFIX btid: <http://kbr.be/id/data/> 
PREFIX bf: <http://id.loc.gov/ontologies/bibframe/>
PREFIX btisni: <http://kbr.be/isni/>
PREFIX mads: <http://www.loc.gov/mads/rdf/v1#>
PREFIX up: <http://users.ugent.be/~tdenies/up/>
PREFIX bnf-onto: <http://data.bnf.fr/ontology/bnf-onto/>
PREFIX frbr: <http://rdvocab.info/uri/schema/FRBRentitiesRDA/>
PREFIX rda-wemi: <http://rdvocab.info/RDARelationshipsWEMI/>
PREFIX marcrel: <http://id.loc.gov/vocabulary/relators/>
PREFIX rdagroup1elements: <http://rdvocab.info/Elements/>
PREFIX rdagroup2elements: <http://rdvocab.info/ElementsGr2/>
"""

    # ---------------------------------------------------------------------------
    def getQueryString(self):
        return ContributorQuery._getPrefixList() + "\n\n" + self._buildQuery()


# -----------------------------------------------------------------------------
class ContributorCreateQuery(ContributorQuery):
    """
    With this query builder class, one can generate a SPARQL UPDATE query to add a person or organization
    from a local data source graph to a target graph in case there is not yet an existing target graph record
    pointing to the local person or organization via a schema:sameAs link.
    """

    # -----------------------------------------------------------------------------
    def __init__(self, source, sourceGraph: str, targetGraph: str, identifiersToAdd: list,
                 entitySourceClass, entityTargetClass,
                 nationalityProperty='schema:nationality', labelProperty='rdfs:label',
                 familyNameProperty='schema:familyName', givenNameProperty='schema:givenName'):
        """

        Parameters
        ----------
        source : str
            The name of the data source. It will be used for comments.
        sourceGraph : str
            The name of the source graph without brackets, e.g. http://kbr-linked-authorities
        targetGraph : str
            The name of the target graph without brackets, e.g. http://beltrans-contributors
        identifiersToAdd : list
            The names of other identifiers which will be added from source to target if a match was found.
            On the one hand, this name is used to refer to the name of the identifier (rdfs:label) according to BIBFRAME
            and on the other hand to build variable names in the SPARQL query.
        nationalityProperty : str
            The RDF property used to fetch nationality information from the source graph, the default is schema:nationality
        entitySourceClass : str
            The RDF class used to identify a  record in the source graph,
            e.g. schema:Person, foaf:Person, schema:Organization or foaf:Organization
        entityTargetClass : str
            The RDF class used to specify the type of a newly created entity in the target graph
        labelProperty : str
            The RDF property used to fetch a name label in the source graph, the default is rdfs:label
        familyNameProperty : str
            The RDF property used to fetch a family name in the source graph, the default is schema:familyName
        givenNameProperty : str
            The RDF property used to fetch a given name in the source graph, the default is schema:givenName
        """
        self.source = source
        self.sourceGraph = sourceGraph
        self.targetGraph = targetGraph
        self.identifiersToAdd = identifiersToAdd
        self.nationalityProperty = nationalityProperty
        self.entitySourceClass = entitySourceClass
        self.entityTargetClass = entityTargetClass
        self.labelProperty = labelProperty
        self.familyNameProperty = familyNameProperty
        self.givenNameProperty = givenNameProperty

        self.baseURL = "http://kbr.be/id/data/"

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        insertBeginPattern = Template("""
    graph <$targetGraph> {
    """)

        query = "INSERT { "

        query += insertBeginPattern.substitute(targetGraph=self.targetGraph)
        query += ContributorQuery._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                          'a',
                                                          self.entityTargetClass,
                                                          newline=True)
        query += self._getINSERTNationalityTriplePattern()
        query += self._getINSERTIdentifierTriplePattern()
        query += self._getINSERTSameAsTriplePattern()
        query += self._getINSERTContributorLabelTriplePattern()
        query += self._getINSERTFamilyNameTriplePattern()
        query += self._getINSERTGivenNameTriplePattern()
        query += self._getINSERTContributorCommentTriplePattern(comment=f'Created from {self.source} data')

        # bf:identifiedBy links, e.g. bf:identifiedBy ?viafEntityURI
        for identifier in self.identifiersToAdd:
            if identifier != '':
                query += self._getINSERTIdentifiedByTriplePattern(identifier)

        # definition of identifiers, e.g. ?viafEntityURI a bf:Identifier
        for identifier in self.identifiersToAdd:
            query += self._getINSERTIdentifierDeclarationTriplePattern(identifier, self.source, f'Created from $source data')

        query += "} "  # end of graph block
        query += "} "  # end of INSERT block

        query += "WHERE { "

        query += ContributorQuery._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI,
                                                          'a',
                                                          self.entitySourceClass,
                                                          graph=self.sourceGraph)
        for property, object in [(self.labelProperty, ContributorQuery.VAR_CONTRIBUTOR_LABEL),
                                 (self.familyNameProperty, ContributorQuery.VAR_CONTRIBUTOR_FAMILY_NAME),
                                 (self.givenNameProperty, ContributorQuery.VAR_CONTRIBUTOR_GIVEN_NAME),
                                 (self.nationalityProperty, ContributorQuery.VAR_CONTRIBUTOR_NATIONALITY)]:
            query += self._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI,
                                                  property,
                                                  object,
                                                  graph=self.sourceGraph,
                                                  optional=True)

        query += self._getUUIDCreationAndBind()
        # query += self._getSourceNationalityQuadPattern(self.sourceGraph, self.nationalityProperty)
        # query += self._getFilterExistsQuadPattern(self.sourceGraph, self.targetGraph, self.identifierName)


        for identifier in self.identifiersToAdd:
            if identifier != '':
                query += self._getIdentifierQuadPattern(identifier, self.sourceGraph, optional=True)

        query += self._getFilterSourceQuadPattern()

        query += ' }'
        return query

    # ---------------------------------------------------------------------------
    def _getFilterSourceQuadPattern(self):
        pattern = Template("""
    
    FILTER NOT EXISTS {
      graph <$targetGraph> {
        ?entity a $entityType ;
                schema:sameAs $localContributorURI .
      }
    }
    """)
        return pattern.substitute(targetGraph=self.targetGraph, entityType=self.entityTargetClass,
                                  localContributorURI=ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI)

    # ---------------------------------------------------------------------------
    def _getUUIDCreationAndBind(self):
        pattern = Template("""
      
    BIND( STRUUID() as $uuidVariable)
    BIND( IRI( CONCAT( "$baseURL", $uuidVariable ) ) as $contributorURIVariable)
    """)
        return pattern.substitute(baseURL=self.baseURL, uuidVariable=ContributorQuery.VAR_CONTRIBUTOR_UUID,
                                  contributorURIVariable=ContributorQuery.VAR_CONTRIBUTOR_URI)


# -----------------------------------------------------------------------------
class ContributorUpdateQuery(ContributorQuery):
    """
    With this query builder class, one can generate a SPARQL UPDATE query to update a person or organization
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
        source : str
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
    """)

        query = "INSERT { "

        query += insertBeginPattern.substitute(targetGraph=self.targetGraph)
        query += self._getINSERTNationalityTriplePattern()
        query += self._getINSERTSameAsTriplePattern()

        # bf:identifiedBy links, e.g. bf:identifiedBy ?viafEntityURI
        for identifier in self.identifiersToAdd:
            query += self._getINSERTIdentifiedByTriplePattern(identifier)

        # definition of identifiers, e.g. ?viafEntityURI a bf:Identifier
        for identifier in self.identifiersToAdd:
            query += self._getINSERTIdentifierDeclarationTriplePattern(identifier, self.source,
                                                                       f'Added from $source via {self.identifierName}')

        query += "} "  # end of graph block
        query += "} "  # end of INSERT block

        query += "WHERE { "

        query += self._getFilterSourceQuadPattern(self.sourceGraph, self.personClass, self.organizationClass)
        query += self._getSourceNationalityQuadPattern(self.sourceGraph, self.nationalityProperty)
        query += self._getFilterExistsQuadPattern(self.sourceGraph, self.targetGraph, self.identifierName)

        for identifier in self.identifiersToAdd:
            query += self._getIdentifierQuadPattern(identifier, self.sourceGraph, optional=True)

        query += ' }'
        return query

    # ---------------------------------------------------------------------------
    def _getFilterSourceQuadPattern(self, sourceGraph, personClass, organizationClass):
        pattern = Template("""
    graph <$sourceGraph> { ?localContributorURI a ?contributorType . }
    FILTER( ?contributorType IN ($personClass, $organizationClass) ) 
    
    """)
        return pattern.substitute(sourceGraph=sourceGraph, personClass=personClass, organizationClass=organizationClass)

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
                               ?contributorURI bf:identifiedBy ?${identifier}TargetEntity .
                               ?${identifier}TargetEntity """ + identifierType +
                           """
                                                    rdf:value ?${identifier}Local .
                             }
                           }
                       
                           FILTER EXISTS {
                             graph <$targetGraph> {
                               ?contributorURI bf:identifiedBy ?${identifier}TargetEntity .
                               ?${identifier}TargetEntity """ + identifierType +
                           """
                                                    rdf:value ?${identifier}Local .
                             }
                           }
                           """)
        return pattern.substitute(sourceGraph=sourceGraph, targetGraph=targetGraph, identifier=identifier)


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import doctest

    doctest.testmod()
