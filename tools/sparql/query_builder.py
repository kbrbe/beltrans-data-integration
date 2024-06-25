from string import Template
from abc import ABC
from datetime import datetime

class Query(ABC):

    BASE_URL = 'http://kbr.be/id/data/'
    VAR_IDENTIFIER_UPDATE_COMMENT = "?identifierComment"
    VAR_IDENTIFIER_TYPE_LABEL = "?typeLabel"

    # ---------------------------------------------------------------------------
    @classmethod
    def normalizeVarName(cls, identifierName):
        return identifierName.replace('-', '')

    # ---------------------------------------------------------------------------
    @classmethod
    def getIdentifierVarName(cls, identifierName):
        identifierName = Query.normalizeVarName(identifierName)
        return f'?identifier{identifierName}'

    # ---------------------------------------------------------------------------
    @classmethod
    def _getSimpleTriplePattern(cls, subject, predicate, object, graph=None, optional=False, newline=False):
        """This function builds a triple pattern.

        It can be a simple subject predicate object triple
        >>> Query._getSimpleTriplePattern('?person', 'a', 'schema:Person')
        '?person a schema:Person .\\n        '

        It can be an optional subject predicate object triple
        >>> Query._getSimpleTriplePattern('?person', 'a', 'schema:Person', optional=True)
        'OPTIONAL { ?person a schema:Person .\\n         }'

        It can be a quad
        >>> Query._getSimpleTriplePattern('?person', 'a', 'schema:Person', graph='http://my-graph')
        'graph <http://my-graph> { ?person a schema:Person .\\n         }'

        And it can be an optional quad
        >>> Query._getSimpleTriplePattern('?person', 'a', 'schema:Person', graph='http://my-graph', optional=True)
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
    @classmethod
    def _getINSERTIdentifierDeclarationTriplePattern(cls, identifier, source, graph=None):
        """"""

        #identifierType = ' a bf:Isni ; ' if identifier == 'ISNI' or identifier == 'isni' else ' a bf:Identifier ; rdfs:label "$identifier" ; '
        identifierType = ' a bf:Isni ; rdfs:label "ISNI" ; ' if identifier == 'ISNI' or identifier == 'isni' else ' a bf:Identifier ; rdfs:label "$identifierLabel" ; '

        identifierLabel = identifier
        identifier = cls.normalizeVarName(identifier)

        pattern = Template("""
    ?${identifier}EntityURI """ + identifierType +
                           """
                               rdfs:comment $commentTextVariable ;
                               rdf:value ?${identifier} .
                       
                           """
                           )
        queryPart = pattern.substitute(identifier=identifier,
                                       identifierLabel=identifierLabel,
                                       source=source,
                                       commentTextVariable=cls.VAR_IDENTIFIER_UPDATE_COMMENT)
        if graph != None:
            queryPart = f'graph <{graph}> ' + '{ ' + queryPart + """ }
                         """

        return queryPart

    # ---------------------------------------------------------------------------
    @classmethod
    def _getUpdateCommentBindText(cls, commentText):
        pattern = Template("""  
    BIND( "$commentText" as $updateCommentVariable)
    """)
        return pattern.substitute(updateCommentVariable=cls.VAR_IDENTIFIER_UPDATE_COMMENT,
                                  commentText=commentText)

    # ---------------------------------------------------------------------------
    @classmethod
    def _getUpdateCommentBindConcat(cls, commentText, additionalTextVariable):
        pattern = Template("""  
    BIND( CONCAT("$commentText", $additionalTextVariable) as $updateCommentVariable)
    """)
        return pattern.substitute(updateCommentVariable=cls.VAR_IDENTIFIER_UPDATE_COMMENT,
                                  commentText=commentText,
                                  additionalTextVariable=additionalTextVariable)




    # ---------------------------------------------------------------------------
    @classmethod
    def _getIdentifierStringPatternBIBFRAME(cls, identifier, subjectURIVariable, baseURL=None, graph=None, optional=False):
        identifierType = ' a bf:Isni ; rdfs:label "$identifier" ; ' if identifier == 'ISNI' or identifier == 'isni' else ' a bf:Identifier ; rdfs:label "$identifierLabel" ; '

        # We cannot give Query.BASE_URL or cls.BASE_URL as default in the parameter list
        # That's why we do it here
        baseURL = baseURL if baseURL != None else cls.BASE_URL

        identifierLabel = identifier
        identifier = cls.normalizeVarName(identifier)

        queryPart = """
            $subjectURIVariable bf:identifiedBy ?${identifier}Entity .
    
            ?${identifier}Entity""" + identifierType + \
            """
                                               rdf:value ?${identifier} . 
        """

        if graph != None:
            queryPart = f'graph <{graph}> ' + '{ ' + queryPart + """ } """

        if optional:
            queryPart = 'OPTIONAL { ' + queryPart + ' } ' + """
            """

        pattern = Template(queryPart + """
        BIND(iri(concat("${baseURL}identifier_${identifier}_", ?${identifier})) as ?${identifier}EntityURI)
        """)
        queryPart = pattern.substitute(subjectURIVariable=subjectURIVariable, identifier=identifier, identifierLabel=identifierLabel, graph=graph, baseURL=baseURL)
        return queryPart

    # ---------------------------------------------------------------------------
    @classmethod
    def _getGenericIdentifierQuadPattern(cls, sourceGraph, localURIVariable, targetURIVariable, targetGraph):
        """This function returns triple patterns for the WHERE clause used for the update functionality."""

        pattern = Template("""
        graph <$sourceGraph> {
          $localURIVariable bf:identifiedBy ?localIdentifierEntity .
    
          ?localIdentifierEntity a ?type ;
                                 rdfs:label ?typeLabel ;
                                 rdf:value ?identifierLocal .
        }

        graph <$targetGraph> {
          $targetURIVariable bf:identifiedBy ?identifierTargetEntity .

          ?identifierTargetEntity a ?type ;
                                  rdfs:label ?typeLabel ;
                                  rdf:value ?identifierLocal .
        }
        """)

        return pattern.substitute(sourceGraph=sourceGraph, localURIVariable=localURIVariable, targetURIVariable=targetURIVariable, targetGraph=targetGraph)

    # ---------------------------------------------------------------------------
    @classmethod
    def _getCorrelationListFilter(self, targetGraph, localURIVariable, targetURIVariable):

          pattern = Template("""
          OPTIONAL { graph <$targetGraph> { ?activity a btm:CorrelationActivity ; prov:used ${localURIVariable} . } }
          OPTIONAL { graph <$targetGraph> { ?activity a btm:CorrelationActivity ; prov:generated ${targetURIVariable} . } }
          FILTER( !bound(?activity) ) 
        """)
          return pattern.substitute(targetGraph=targetGraph, localURIVariable=localURIVariable, targetURIVariable=targetURIVariable)




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
PREFIX fabio: <http://purl.org/spar/fabio/> 
PREFIX frbr: <http://rdvocab.info/uri/schema/FRBRentitiesRDA/>
PREFIX rda-wemi: <http://rdvocab.info/RDARelationshipsWEMI/>
PREFIX marcrel: <http://id.loc.gov/vocabulary/relators/>
PREFIX rdagroup1elements: <http://rdvocab.info/Elements/>
PREFIX rdagroup2elements: <http://rdvocab.info/ElementsGr2/>
"""

    # ---------------------------------------------------------------------------
    def getQueryString(self):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        provenanceString = f'# generated at {date_time} by class {type(self)}'
        return provenanceString + "\n\n" + Query._getPrefixList() + "\n\n" + self._buildQuery()

# ---------------------------------------------------------------------------
class DeadLinkQuery(Query):

    # ---------------------------------------------------------------------------
    def __init__(self, sourceGraph, targetGraph, entityTargetType, entitySourceType, identifierName):
        self.sourceGraph = sourceGraph
        self.targetGraph = targetGraph
        self.entityTargetType = entityTargetType
        self.entitySourceType = entitySourceType
        self.identifierName = identifierName

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        pattern = Template("""

    SELECT ?targetIdentifier ("$identifierName" AS ?localIdentifierName) ?localIdentifier
    WHERE {
      graph <$targetGraph> { 
        ?manifestation a $entityTargetType ;
                       dcterms:identifier ?targetIdentifier ;
                       bf:identifiedBy ?identifierEntity .
        
        ?identifierEntity a bf:Identifier ;
                          rdfs:label "$identifierName" ;
                          rdf:value ?localIdentifier .
      } 
      
      OPTIONAL { 
        graph <$targetGraph> { ?manifestation schema:sameAs ?localURI . } 
        graph <$sourceGraph> { ?localURI a $entitySourceType . } 
      }

      FILTER(!bound(?localURI))

    }


        """)

        return pattern.substitute(sourceGraph=self.sourceGraph, targetGraph=self.targetGraph,
                                  entityTargetType=self.entityTargetType, entitySourceType=self.entitySourceType,
                                  identifierName=self.identifierName)

# ---------------------------------------------------------------------------
class DuplicateIdentifierQuery(Query):

    # ---------------------------------------------------------------------------
    def __init__(self, contributorNamedGraph, manifestationNamedGraph, entityType, identifierName):
        self.contributorNamedGraph = contributorNamedGraph
        self.manifestationNamedGraph = manifestationNamedGraph
        self.identifierName = identifierName
        self.entityType = entityType

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        if self.identifierName == 'isni' or self.identifierName == 'ISNI':
            identifierClass = 'bf:Isni'
            identifierLabelTriple = ''
        else:
            identifierClass = 'bf:Identifier'
            identifierLabelTriple = f'rdfs:label "{self.identifierName}" ;'
       
        pattern = Template("""
  SELECT DISTINCT ?person (group_concat(distinct ?identifier;SEPARATOR=';') AS ?duplicateIdentifiers)
  WHERE {

    #
    # first order the identifiers to ensure reproducible aggregated strings
    #
    {
      SELECT DISTINCT ?person ?identifier
      WHERE {
        graph <$contributorNamedGraph> {
        ?person a $entityType ;
                bf:identifiedBy ?identifierEntity .

        ?identifierEntity a $identifierClass ;
                          $identifierLabelTriple
                          rdf:value ?identifier .
        } 

    #
    # the person needs to be linked to a translation of the BELTRANS corpus
    #
    {
      SELECT DISTINCT ?person
      WHERE {
        graph <$manifestationNamedGraph> {
          ?manifestation schema:isPartOf btid:beltransCorpus ;
                         schema:author|schema:translator|marcrel:ill|marcrel:sce|marcrel:pbd ?person .
        }
      }
    }
  }
  ORDER BY ASC(?person) ASC(?identifier)
  }

}
GROUP BY ?person
HAVING (COUNT(?identifier) > 1)
ORDER BY ASC(?person)
       """)
        return pattern.substitute(contributorNamedGraph=self.contributorNamedGraph, entityType=self.entityType,
                                  identifierClass=identifierClass, identifierLabelTriple=identifierLabelTriple,
                                  manifestationNamedGraph=self.manifestationNamedGraph)



class ContributorQuery(Query, ABC):
    VAR_CONTRIBUTOR_URI = "?contributorURI"
    VAR_CONTRIBUTOR_NATIONALITY = "?contributorNationality"
    VAR_CONTRIBUTOR_GENDER = "?contributorGender"
    VAR_CONTRIBUTOR_LOCAL_URI = "?localContributorURI"
    VAR_CONTRIBUTOR_FAMILY_NAME = "?familyName"
    VAR_CONTRIBUTOR_GIVEN_NAME = "?givenName"
    VAR_CONTRIBUTOR_LABEL = "?contributorLabel"
    VAR_CONTRIBUTOR_UUID = "?uuid"
    VAR_COUNTRY_ENTITY = "?countryEntityURI"
    VAR_COUNTRY = "?country"



    # ---------------------------------------------------------------------------
    def _getINSERTIdentifiedByTriplePattern(self, identifier):
        identifier = Query.normalizeVarName(identifier)
        return Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'bf:identifiedBy',
                                                        f'?{identifier}EntityURI',
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTNationalityTriplePattern(self):
        return Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'schema:nationality',
                                                        ContributorQuery.VAR_CONTRIBUTOR_NATIONALITY,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTGenderTriplePattern(self):
        return Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'schema:gender',
                                                        ContributorQuery.VAR_CONTRIBUTOR_GENDER,
                                                        newline=True)


    # ---------------------------------------------------------------------------
    def _getINSERTCountryTriplePattern(self):

        pattern = Template("""
        $countryEntityVar a schema:PostalAddress ;
                  rdfs:comment "Created from $source data" ;
                  schema:addressCountry $countryVar .
        """)
        declarationPattern = pattern.substitute(countryEntityVar=ContributorQuery.VAR_COUNTRY_ENTITY, source=self.source,
                           countryVar=ContributorQuery.VAR_COUNTRY)

        linkPattern = Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'schema:location',
                                                        ContributorQuery.VAR_COUNTRY_ENTITY,
                                                        newline=True)

        return linkPattern + declarationPattern


    # ---------------------------------------------------------------------------
    def _getINSERTSameAsTriplePattern(self):
        return Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'schema:sameAs',
                                                        ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTIdentifierTriplePattern(self):
        return Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'dcterms:identifier',
                                                        ContributorQuery.VAR_CONTRIBUTOR_UUID,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTFamilyNameTriplePattern(self):
        return Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'schema:familyName',
                                                        ContributorQuery.VAR_CONTRIBUTOR_FAMILY_NAME,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTGivenNameTriplePattern(self):
        return Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'schema:givenName',
                                                        ContributorQuery.VAR_CONTRIBUTOR_GIVEN_NAME,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTContributorLabelTriplePattern(self):
        return Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'rdfs:label',
                                                        ContributorQuery.VAR_CONTRIBUTOR_LABEL,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    def _getINSERTContributorCommentTriplePattern(self, comment):
        return Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                        'rdfs:comment',
                                                        f'"{comment}"',
                                                        newline=True)

     # ---------------------------------------------------------------------------
    def _getSourceNationalityQuadPattern(self, sourceGraph, nationalityProperty, optional=False):
        pattern = Template("""
    graph <$sourceGraph> { ?localContributorURI $nationalityProperty ?contributorNationality . }

    """)
        queryPart = pattern.substitute(sourceGraph=sourceGraph, nationalityProperty=nationalityProperty)

        if optional:
            return 'OPTIONAL { ' + queryPart + ' } '
        else:
            return queryPart

    # ---------------------------------------------------------------------------
    def _getSourceGenderQuadPattern(self, sourceGraph, genderProperty, optional=False):
        pattern = Template("""
    graph <$sourceGraph> { ?localContributorURI $genderProperty ?contributorGender . }

    """)
        queryPart = pattern.substitute(sourceGraph=sourceGraph, genderProperty=genderProperty)

        if optional:
            return 'OPTIONAL { ' + queryPart + ' } '
        else:
            return queryPart


    # ---------------------------------------------------------------------------
    def _getSourceCountryQuadPattern(self, sourceGraph, optional=False):
        pattern = Template("""
    graph <$sourceGraph> { ?localContributorURI $countryProperty $countryVar . }

    """)
        queryPart = pattern.substitute(sourceGraph=sourceGraph, countryProperty=self.countryProperty,
                                       countryVar=ContributorQuery.VAR_COUNTRY)

        bindPart = f'BIND(iri(concat("{self.baseURL}address_", {ContributorQuery.VAR_CONTRIBUTOR_UUID})) as {ContributorQuery.VAR_COUNTRY_ENTITY})'
        if optional:
            return 'OPTIONAL { ' + queryPart + ' } ' + bindPart + ' '
        else:
            return queryPart + bindPart + ' '

    # ---------------------------------------------------------------------------
    @classmethod
    def _getIdentifierStringPatternDCTERMS(cls, identifier, subjectURIVariable, baseURL=None, graph=None):
        queryPart = "$subjectURIVariable dcterms:identifier ?${identifier} ."

        # We cannot give Query.BASE_URL or cls.BASE_URL as default in the parameter list
        # That's why we do it here
        baseURL = baseURL if baseURL != None else cls.BASE_URL
        if graph != None:
            queryPart = f'graph <{graph}> ' + '{ ' + queryPart + """ } """
            
        pattern = Template(queryPart + """
        BIND(iri(concat("${baseURL}identifier_${identifier}_", ?${identifier})) as ?${identifier}EntityURI)
        """)
        return pattern.substitute(subjectURIVariable=subjectURIVariable, identifier=identifier, baseURL=baseURL)

    # ---------------------------------------------------------------------------
    def _getIdentifierQuadPattern(self, identifier, namedGraph, optional=False):
        """This function returns possibly optional quad patterns for the WHERE clause,
           for example if a particular identifier such as VIAF or Wikidata should be queried too.
        """

        if identifier == self.source:
            queryPart = ContributorQuery._getIdentifierStringPatternDCTERMS(identifier,
                                                                            subjectURIVariable=ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI,
                                                                            graph=namedGraph)
        else:
            queryPart = Query._getIdentifierStringPatternBIBFRAME(identifier,
                                                                  subjectURIVariable=ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI,
                                                                  graph=namedGraph)
        if optional:
            return 'OPTIONAL { ' + queryPart + ' } '
        else:
            return queryPart


class ManifestationQuery(Query, ABC):
    VAR_MANIFESTATION_URI = '?manifestationURI'
    VAR_MANIFESTATION_UUID = '?uuid'
    VAR_MANIFESTATION_LABEL = '?manifestationLabel'
    VAR_MANIFESTATION_TITLE = '?manifestationTitle'
    VAR_MANIFESTATION_TARGET_LANG = '?targetLang'
    VAR_MANIFESTATION_SOURCE_LANG = '?sourceLang'
    VAR_MANIFESTATION_LOCAL_URI = '?localManifestationURI'
    VAR_MANIFESTATION_ISBN10 = '?isbn10'
    VAR_MANIFESTATION_ISBN13 = '?isbn13'


    # ---------------------------------------------------------------------------
    def _getINSERTIdentifiedByTriplePattern(self, identifier, graph=None, optional=False):
        identifier = Query.normalizeVarName(identifier)
        return Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_URI,
                                                        'bf:identifiedBy',
                                                        f'?{identifier}EntityURI',
                                                        graph=graph,
                                                        optional=optional,
                                                        newline=True)

    # ---------------------------------------------------------------------------
    @classmethod
    def _getUUIDAndLabelCreationAndBind(cls):
        pattern = Template("""

        BIND( STRUUID() as $uuidVariable)
        BIND( IRI( CONCAT( "$baseURL", $uuidVariable ) ) as $URIVariable)
        BIND( CONCAT( "BELTRANS manifestation ", $uuidVariable ) as $labelVariable)
        """)
        return pattern.substitute(baseURL=Query.BASE_URL, uuidVariable=ManifestationQuery.VAR_MANIFESTATION_UUID,
                                  URIVariable=ManifestationQuery.VAR_MANIFESTATION_URI,
                                  labelVariable=ManifestationQuery.VAR_MANIFESTATION_LABEL)

    # ---------------------------------------------------------------------------
    def _getIdentifierQuadPattern(self, identifier, namedGraph, optional=False):
        """This function returns possibly optional quad patterns for the WHERE clause,
           for example if a particular identifier such as VIAF or Wikidata should be queried too.
        """

        queryPart = Query._getIdentifierStringPatternBIBFRAME(identifier,
                                                              subjectURIVariable=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                                              graph=namedGraph)
        if optional:
            return 'OPTIONAL { ' + queryPart + ' } '
        else:
            return queryPart

class IdentifiersDescriptiveKeysQuery(ManifestationQuery):

    # -----------------------------------------------------------------------------
    def __init__(self, sourceGraph: str, targetGraph: str,
                 identifiersToAdd: list,
                 entitySourceClass: str):
        """

        Parameters
        ----------
        sourceGraph : str
            The name of the source graph without brackets, e.g. http://kb-manifestations
        targetGraph : str
            The name of the target graph without brackets, e.g. http://beltrans-manifestations
        identifiersToAdd : list
            The names of other identifiers which will be added from source to target if a match was found.
            On the one hand, this name is used to refer to the name of the identifier (rdfs:label) according to BIBFRAME
            and on the other hand to build variable names in the SPARQL query.
        entitySourceClass : str
            The RDF class used to identify a  record in the source graph,
            e.g. schema:CreativeWork or schema:Book
        """
        self.sourceGraph = sourceGraph
        self.targetGraph = targetGraph
        self.identifiersToAdd = identifiersToAdd
        self.entitySourceClass = entitySourceClass

        print(f'Constructor received identifiersToAdd: {identifiersToAdd}')

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        query = "SELECT ?entityID ?identifierName ?identifierValue WHERE { "
        for property, object in [('a', self.entitySourceClass),
                                 ('dcterms:identifier', '?entityID')]:
            query += Query._getSimpleTriplePattern('?entity',
                                                  property,
                                                  object,
                                                  graph=self.sourceGraph,
                                                  optional=False,
                                                  newline=True)

        query += self._getSubquery(self.identifiersToAdd)

        query += "} \n"  # end of query WHERE clause

        return query

    # ---------------------------------------------------------------------------
    def _getSubquery(self, identifiersToAdd):

        identifierTypes = 'bf:Identifier, bf:Isni'
        identifierNames = ','.join(f'"{id}"' for id in identifiersToAdd)
        pattern = Template("""
        {
          graph <${namedGraph}> { 
            ?entity bf:identifiedBy ?identifierEntityURI .

            ?identifierEntityURI a ?identifierType ;
                                    rdfs:label ?identifierName ;
                                    rdf:value ?identifierValue .
          }
          FILTER( ?identifierType IN (${identifierTypes}) )
          FILTER( ?identifierName IN (${identifierNames}) )

        FILTER NOT EXISTS {
          graph <${targetGraph}> {
        
            ?anyIntegratedRecordURI schema:sameAs ?entity .
            ?anyCorrelationActivity a btm:CorrelationActivity ;
                                    prov:generated ?anyIntegratedRecordURI .
          }
      }


        }
        """)

        return pattern.substitute(namedGraph=self.sourceGraph,identifierNames=identifierNames, identifierTypes=identifierTypes,targetGraph=self.targetGraph)

class ClustersDescriptiveKeysQuery(ManifestationQuery):

    # -----------------------------------------------------------------------------
    def __init__(self, targetGraph: str, memberIdentifiers: list, keyIdentifiers: list,
                 entitySourceClass: str):
        """

        Parameters
        ----------
        targetGraph : str
            The name of the target graph without brackets, e.g. http://beltrans-manifestations
        memberIdentifiers : list
            The names of identifiers of cluster members
            This name is used to refer to the name of the identifier (rdfs:label) according to BIBFRAME
        keyIdentifiers : list
            The names of identifiers that cluster members have in common
            This name is used to refer to the name of the identifier (rdfs:label) according to BIBFRAME
        entitySourceClass : str
            The RDF class used to identify a  record in the source graph,
            e.g. schema:CreativeWork or schema:Book
        """
        self.targetGraph = targetGraph
        self.memberIdentifiers = memberIdentifiers
        self.keyIdentifiers = keyIdentifiers
        self.entitySourceClass = entitySourceClass


    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        pattern = Template("""
    SELECT DISTINCT ?memberName ?memberIdentifier ?keyIdentifierName ?keyIdentifier
    WHERE {
      graph <${namedGraph}> {
      ?cluster a ${entityClass} ;
               bf:identifiedBy ?memberIdentifierEntity ;
               bf:identifiedBy ?keyIdentifierEntity .
    
      ?memberIdentifierEntity rdfs:label ?memberName ;
                              rdf:value ?memberIdentifier .
    
      ?keyIdentifierEntity rdfs:label ?keyIdentifierName ;
                           rdf:value ?keyIdentifier .
      }
      FILTER( ?memberName IN ( ${memberNameListString} ) )
      FILTER( ?keyIdentifierName IN ( ${keyIdentifiersNameListString} ) )
   }""")
        memberListString = ','.join(f'"{id}"' for id in self.memberIdentifiers)
        keyIdentifiersListString = ','.join(f'"{id}"' for id in self.keyIdentifiers)

        query = pattern.substitute(namedGraph=self.targetGraph, entityClass=self.entitySourceClass,memberNameListString=memberListString,keyIdentifiersNameListString=keyIdentifiersListString)


        return query


class ClustersDescriptiveKeysSameAsQuery(ManifestationQuery):

    # -----------------------------------------------------------------------------
    def __init__(self, targetGraph: str, sourceGraph: str, linkProperty: str, memberIdentifiers: list, sourceType: str, targetType: str):
        """

        Parameters
        ----------
        targetGraph : str
            The name of the target graph without brackets, e.g. http://beltrans-manifestations
        memberIdentifiers : list
            The names of identifiers of cluster members
            This name is used to refer to the name of the identifier (rdfs:label) according to BIBFRAME
        keyIdentifiers : list
            The names of identifiers that cluster members have in common
            This name is used to refer to the name of the identifier (rdfs:label) according to BIBFRAME
        entitySourceClass : str
            The RDF class used to identify a  record in the source graph,
            e.g. schema:CreativeWork or schema:Book
        """
        self.targetGraph = targetGraph
        self.sourceGraph = sourceGraph
        self.targetType = targetType
        self.sourceType = sourceType
        self.linkProperty = linkProperty
        self.memberIdentifiers = memberIdentifiers


    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        pattern = Template("""
    INSERT {
      graph <${targetGraph}> {
        ?cluster bf:identifiedBy ?keyEntityURI .

        ?keyEntityURI a ?entityType ;
                      rdfs:label ?memberName ;
                      rdf:value ?memberIdentifier .
      }
    }
    WHERE {

      graph <${targetGraph}> {
        ?cluster a ${targetType} ;
                 ${linkProperty} ?memberURI .
      }

      graph <${sourceGraph}> {
        ?memberURI a ${sourceType} ;
                 bf:identifiedBy ?memberIdentifierEntity .
    
        ?memberIdentifierEntity a ?entityType ;
                                rdfs:label ?memberName ;
                                rdf:value ?memberIdentifier .
    
      }
      FILTER( ?memberName IN ( ${memberNameListString} ) )
      OPTIONAL {
        graph <${targetGraph}> {
          ?anyCorrelationActivity a btm:CorrelationActivity ;
                                  prov:generated ?cluster . 
        }
      }
      FILTER( !bound(?anyCorrelationActivity) )
      BIND( IRI( CONCAT( "${baseURL}_", ?memberName, "_", ?memberIdentifier ) ) as ?keyEntityURI)


   }""")
        memberListString = ','.join(f'"{id}"' for id in self.memberIdentifiers)

        query = pattern.substitute(targetGraph=self.targetGraph, sourceGraph=self.sourceGraph, targetType=self.targetType, sourceType=self.sourceType, baseURL=Query.BASE_URL,memberNameListString=memberListString, linkProperty=self.linkProperty)

        return query 


class PropertyUpdateSimpleQuery(ManifestationQuery):

    # -----------------------------------------------------------------------------
    def __init__(self, targetGraph: str, sourceGraph: str, property: str, linkProperty: str, targetType: str, sourceType: str):
        """

        Parameters
        ----------
        targetGraph : str
            The name of the target graph without brackets, e.g. http://beltrans-manifestations
        """
        self.targetGraph = targetGraph
        self.sourceGraph = sourceGraph
        self.property = property
        self.linkProperty = linkProperty
        self.targetType = targetType
        self.sourceType = sourceType

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        pattern = Template("""
    INSERT {
      graph <${targetGraph}> {
        ?entity ${property} ?propertyValue .
      }
    }
    WHERE {
      graph <${targetGraph}> {
        ?entity a ${targetType} ;
                ${linkProperty} ?sourceURI .
      }

      graph <${sourceGraph}> {
        ?sourceURI a ${sourceType} ;
                   ${property} ?propertyValue .
      }
      FILTER NOT EXISTS {
        graph <${targetGraph}> {
          ?entity ${property} ?someValue .
        }
      }
   }""")

        query = pattern.substitute(targetGraph=self.targetGraph, sourceGraph=self.sourceGraph, property=self.property, linkProperty=self.linkProperty, targetType=self.targetType, sourceType=self.sourceType)

        return query


class PropertyUpdateComplexMappingQuery(ManifestationQuery):

    # -----------------------------------------------------------------------------
    def __init__(self, targetGraph: str, sourceGraph: str, targetProperty: str, sourceProperty: str, sourcePropertyGraph: str, sourceGraphLinkProperty: str, linkProperty: str, targetType: str, sourceType: str):
        """

        Parameters
        ----------
        targetGraph : str
            The name of the target graph without brackets, e.g. http://beltrans-manifestations
        """
        self.targetGraph = targetGraph
        self.sourceGraph = sourceGraph
        self.targetProperty = targetProperty
        self.sourceProperty = sourceProperty
        self.linkProperty = linkProperty
        self.sourcePropertyGraph = sourcePropertyGraph
        self.sourceGraphLinkProperty = sourceGraphLinkProperty
        self.targetType = targetType
        self.sourceType = sourceType

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        pattern = Template("""
    INSERT {
      graph <${targetGraph}> {
        ?entity ${targetProperty} ?propertyValue .
      }
    }
    WHERE {
      graph <${targetGraph}> {
        ?entity a ${targetType} ;
                ${linkProperty} ?sourceURI .
      }

      graph <${sourceGraph}> {
        ?sourceURI a ${sourceType} ;
                   ${sourceGraphLinkProperty} ?originalURI .
      }

      graph <${sourcePropertyGraph}> {
        ?originalURI ${sourceProperty} ?propertyValue .
      }
      FILTER NOT EXISTS {
        graph <${targetGraph}> {
          ?entity ${targetProperty} ?someValue .
        }
      }
   }""")

        query = pattern.substitute(targetGraph=self.targetGraph, sourceGraph=self.sourceGraph, targetProperty=self.targetProperty, linkProperty=self.linkProperty, sourceProperty=self.sourceProperty, sourcePropertyGraph=self.sourcePropertyGraph, sourceGraphLinkProperty=self.sourceGraphLinkProperty, targetType=self.targetType, sourceType=self.sourceType)

        return query

class PropertyUpdateSimpleMappingQuery(ManifestationQuery):

    # -----------------------------------------------------------------------------
    def __init__(self, targetGraph: str, sourceGraph: str, targetProperty: str, sourceProperty: str, linkProperty: str, targetType: str, sourceType: str):
        """

        Parameters
        ----------
        targetGraph : str
            The name of the target graph without brackets, e.g. http://beltrans-manifestations
        """
        self.targetGraph = targetGraph
        self.sourceGraph = sourceGraph
        self.targetProperty = targetProperty
        self.sourceProperty = sourceProperty
        self.linkProperty = linkProperty
        self.targetType = targetType
        self.sourceType = sourceType

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        pattern = Template("""
    INSERT {
      graph <${targetGraph}> {
        ?entity ${targetProperty} ?propertyValue .
      }
    }
    WHERE {
      graph <${targetGraph}> {
        ?entity a ${targetType} ;
                ${linkProperty} ?sourceURI .
      }

      graph <${sourceGraph}> {
        ?sourceURI a ${sourceType} ;
                   ${sourceProperty} ?propertyValue .
      }

      FILTER NOT EXISTS {
        graph <${targetGraph}> {
          ?entity ${targetProperty} ?someValue .
        }
      }
   }""")

        query = pattern.substitute(targetGraph=self.targetGraph, sourceGraph=self.sourceGraph, targetProperty=self.targetProperty, linkProperty=self.linkProperty, sourceProperty=self.sourceProperty, targetType=self.targetType, sourceType=self.sourceType)

        return query

class PropertyUpdatePropertyPathQuery(ManifestationQuery):

    # -----------------------------------------------------------------------------
    def __init__(self, targetGraph: str, sourceGraph: str, targetProperty: list, linkProperty: str, targetPropertyEntityUUID: str, targetPropertyEntityPrefix: str, targetPropertyEntityType: str, targetType: str, sourceType: str):
        """

        Parameters
        ----------
        targetGraph : str
            The name of the target graph without brackets, e.g. http://beltrans-manifestations
        """
        self.targetGraph = targetGraph
        self.sourceGraph = sourceGraph
        self.targetProperty = targetProperty
        self.linkProperty = linkProperty
        self.targetPropertyEntityUUID=targetPropertyEntityUUID
        self.targetPropertyEntityPrefix=targetPropertyEntityPrefix
        self.targetPropertyEntityType=targetPropertyEntityType
        self.targetType = targetType
        self.sourceType = sourceType

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        pattern = Template("""
    INSERT {
      graph <${targetGraph}> {
        ?entity ${targetPropertyFirst} ?propertyEntityURI .

        ?propertyEntityURI a ${propertyEntityType} ;
                           ${targetPropertySecond} ?propertyValue .
      }
    }
    WHERE {
      graph <${targetGraph}> {
        ?entity a ${targetType} ;
                ${targetPropertyEntityUUID} ?entityUUID ;
                ${linkProperty} ?sourceURI .
      }

      graph <${sourceGraph}> {
        ?sourceURI a ${sourceType} ;
                   ${sourcePropertyPath} ?propertyValue .
      }

      BIND( IRI( CONCAT( "${baseURL}", ?entityUUID ) ) as ?propertyEntityURI)
      FILTER NOT EXISTS {
        graph <${targetGraph}> {
          ?entity ${sourcePropertyPath} ?someValue .
        }
      }
   }""")

        targetPropertyPath = '/'.join(self.targetProperty)
        query = pattern.substitute(
                  baseURL=Query.BASE_URL + self.targetPropertyEntityPrefix,
                  targetGraph=self.targetGraph, 
                  sourceGraph=self.sourceGraph, 
                  targetPropertyFirst=self.targetProperty[0],
                  targetPropertySecond=self.targetProperty[1],
                  targetPropertyEntityUUID=self.targetPropertyEntityUUID,
                  linkProperty=self.linkProperty,
                  propertyEntityType=self.targetPropertyEntityType,
                  sourcePropertyPath=targetPropertyPath,
                  targetType=self.targetType, 
                  sourceType=self.sourceType)

        return query


class ManifestationCreateQueryIdentifiers(ManifestationQuery):

    # -----------------------------------------------------------------------------
    def __init__(self, source, sourceGraph: str, targetGraph: str, originalsGraph: str,
                 identifiersToAdd: list,
                 entitySourceClass, entityTargetClass,
                 titleProperty='schema:name'):
        """

        Parameters
        ----------
        source : str
            The name of the data source. It will be used for comments.
        sourceGraph : str
            The name of the source graph without brackets, e.g. http://kb-manifestations
        targetGraph : str
            The name of the target graph without brackets, e.g. http://beltrans-manifestations
        originalsGraph : str
            The name of the graph with information about the translation's original, e.g. http://kb-originals
        identifiersToAdd : list
            The names of other identifiers which will be added from source to target if a match was found.
            On the one hand, this name is used to refer to the name of the identifier (rdfs:label) according to BIBFRAME
            and on the other hand to build variable names in the SPARQL query.
        entitySourceClass : str
            The RDF class used to identify a  record in the source graph,
            e.g. schema:CreativeWork or schema:Book
        entityTargetClass : str
            The RDF class used to specify the type of a newly created entity in the target graph
        titleProperty : str
            The RDF property used to fetch a name label in the source graph, the default is rdfs:label
        """
        self.source = source
        self.sourceGraph = sourceGraph
        self.targetGraph = targetGraph
        self.originalsGraph = originalsGraph
        self.identifiersToAdd = identifiersToAdd
        self.entitySourceClass = entitySourceClass
        self.entityTargetClass = entityTargetClass
        self.titleProperty = titleProperty

        print(f'Constructor received identifiersToAdd: {identifiersToAdd}')

    # ---------------------------------------------------------------------------
    def _getFilterSourceQuadPattern(self):
#        pattern = Template("""
#
#       FILTER NOT EXISTS {
#         graph <$targetGraph> {
#           ?entity a $entityType ;
#                   schema:sameAs $localContributorURI .
#         }
#       }
#       """)

        pattern = Template("""
        OPTIONAL { graph <$targetGraph> { ?entity schema:sameAs $localContributorURI . } }
        FILTER(!bound(?entity))
        """)
        return pattern.substitute(targetGraph=self.targetGraph, entityType=self.entityTargetClass,
                                  localContributorURI=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI)

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        query = "INSERT { "
        for property, object in [('a', self.entityTargetClass),
                                 ('dcterms:identifier', ManifestationQuery.VAR_MANIFESTATION_UUID),
                                 ('rdfs:label', ManifestationQuery.VAR_MANIFESTATION_LABEL),
                                 ('schema:name', ManifestationQuery.VAR_MANIFESTATION_TITLE),
                                 ('schema:inLanguage', ManifestationQuery.VAR_MANIFESTATION_TARGET_LANG),
                                 ('btm:sourceLanguage', ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG),
                                 ('schema:sameAs', ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI),
                                 ('bibo:isbn10', ManifestationQuery.VAR_MANIFESTATION_ISBN10),
                                 ('bibo:isbn13', ManifestationQuery.VAR_MANIFESTATION_ISBN13),
                                 ('rdfs:comment', f'"Created from {self.source} data"')]:
            query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_URI,
                                                  property,
                                                  object,
                                                  graph=self.targetGraph,
                                                  optional=False,
                                                  newline=True)

        query += """
          graph <""" + self.targetGraph + """> {
        """
        # bf:identifiedBy links, e.g. bf:identifiedBy ?viafEntityURI
        for identifier in self.identifiersToAdd:
            if identifier != '':
                query += self._getINSERTIdentifiedByTriplePattern(identifier)

        # definition of identifiers, e.g. ?viafEntityURI a bf:Identifier
        for identifier in self.identifiersToAdd:
            query += Query._getINSERTIdentifierDeclarationTriplePattern(identifier, self.source)



        query += "} \n" # end of graph block for identifiers
        query += "} \n"  # end of INSERT block

        query += "WHERE { "


        for property, object, optional in [('a', self.entitySourceClass, False),
                                           (self.titleProperty, ManifestationQuery.VAR_MANIFESTATION_TITLE, False),
                                           ('schema:inLanguage', ManifestationQuery.VAR_MANIFESTATION_TARGET_LANG, True),
                                           ('bibo:isbn10', ManifestationQuery.VAR_MANIFESTATION_ISBN10, True),
                                           ('bibo:isbn13', ManifestationQuery.VAR_MANIFESTATION_ISBN13, True)]:
            query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                                  property,
                                                  object,
                                                  graph=self.sourceGraph,
                                                  optional=optional,
                                                  newline=True)

        query += Query._getUpdateCommentBindText(f'Created from {self.source} data')

        for identifier in self.identifiersToAdd:
            if identifier != '':
                query += self._getIdentifierQuadPattern(identifier, self.sourceGraph, optional=True)



        if self.source == 'BnF' or self.source == 'bnf':
            pattern = Template("""OPTIONAL { graph <$sourceGraph> { $localURIVar btm:sourceLanguage $sourceLangVar . } }
            """)
            query += pattern.substitute(sourceGraph=self.sourceGraph, localURIVar=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                        sourceLangVar=ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG)
        else:
            pattern = Template("""OPTIONAL { graph <$sourceGraph> { $localURIVar schema:translationOfWork ?originalURI . }
                                        graph <$originalsGraph> { ?originalURI schema:inLanguage $sourceLangVar . } }
                          """)

            query += pattern.substitute(sourceGraph=self.sourceGraph, localURIVar=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                    originalsGraph=self.originalsGraph, sourceLangVar=ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG)

        query += pattern.substitute(sourceGraph=self.sourceGraph, localURIVar=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                    originalsGraph=self.originalsGraph, sourceLangVar=ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG)

        query += ManifestationQuery._getUUIDAndLabelCreationAndBind()


        query += self._getFilterSourceQuadPattern()

        query += ' }'
        return query



class ManifestationCreateQuery(ManifestationQuery):

    # -----------------------------------------------------------------------------
    def __init__(self, source, sourceGraph: str, targetGraph: str, originalsGraph: str,
                 entitySourceClass, entityTargetClass,
                 titleProperty='schema:name'):
        """

        Parameters
        ----------
        source : str
            The name of the data source. It will be used for comments.
        sourceGraph : str
            The name of the source graph without brackets, e.g. http://kb-manifestations
        targetGraph : str
            The name of the target graph without brackets, e.g. http://beltrans-manifestations
        originalsGraph : str
            The name of the graph with information about the translation's original, e.g. http://kb-originals
        entitySourceClass : str
            The RDF class used to identify a  record in the source graph,
            e.g. schema:CreativeWork or schema:Book
        entityTargetClass : str
            The RDF class used to specify the type of a newly created entity in the target graph
        titleProperty : str
            The RDF property used to fetch a name label in the source graph, the default is rdfs:label
        """
        self.source = source
        self.sourceGraph = sourceGraph
        self.targetGraph = targetGraph
        self.originalsGraph = originalsGraph
        self.entitySourceClass = entitySourceClass
        self.entityTargetClass = entityTargetClass
        self.titleProperty = titleProperty

    # ---------------------------------------------------------------------------
    def _getFilterSourceQuadPattern(self):
#        pattern = Template("""
#
#       FILTER NOT EXISTS {
#         graph <$targetGraph> {
#           ?entity a $entityType ;
#                   schema:sameAs $localContributorURI .
#         }
#       }
#       """)

        pattern = Template("""
        OPTIONAL { graph <$targetGraph> { ?entity schema:sameAs $localContributorURI . } }
        FILTER(!bound(?entity))
        """)
        return pattern.substitute(targetGraph=self.targetGraph, entityType=self.entityTargetClass,
                                  localContributorURI=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI)

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        query = "INSERT { "
        for property, object in [('a', self.entityTargetClass),
                                 ('dcterms:identifier', ManifestationQuery.VAR_MANIFESTATION_UUID),
                                 ('rdfs:label', ManifestationQuery.VAR_MANIFESTATION_LABEL),
                                 ('schema:name', ManifestationQuery.VAR_MANIFESTATION_TITLE),
                                 ('schema:inLanguage', ManifestationQuery.VAR_MANIFESTATION_TARGET_LANG),
                                 ('btm:sourceLanguage', ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG),
                                 ('schema:sameAs', ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI),
                                 ('bibo:isbn10', ManifestationQuery.VAR_MANIFESTATION_ISBN10),
                                 ('bibo:isbn13', ManifestationQuery.VAR_MANIFESTATION_ISBN13),
                                 ('rdfs:comment', f'"Created from {self.source} data"')]:
            query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_URI,
                                                  property,
                                                  object,
                                                  graph=self.targetGraph,
                                                  optional=False,
                                                  newline=True)



        query += "} \n"  # end of INSERT block

        query += "WHERE { "


        for property, object, optional in [('a', self.entitySourceClass, False),
                                           (self.titleProperty, ManifestationQuery.VAR_MANIFESTATION_TITLE, False),
                                           ('schema:inLanguage', ManifestationQuery.VAR_MANIFESTATION_TARGET_LANG, True),
                                           ('bibo:isbn10', ManifestationQuery.VAR_MANIFESTATION_ISBN10, True),
                                           ('bibo:isbn13', ManifestationQuery.VAR_MANIFESTATION_ISBN13, True)]:
            query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                                  property,
                                                  object,
                                                  graph=self.sourceGraph,
                                                  optional=optional,
                                                  newline=True)


        if self.source == 'BnF' or self.source == 'bnf':
            pattern = Template("""OPTIONAL { graph <$sourceGraph> { $localURIVar btm:sourceLanguage $sourceLangVar . } }
            """)
            query += pattern.substitute(sourceGraph=self.sourceGraph, localURIVar=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                        sourceLangVar=ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG)
        else:
            pattern = Template("""OPTIONAL { graph <$sourceGraph> { $localURIVar schema:translationOfWork ?originalURI . }
                                        graph <$originalsGraph> { ?originalURI schema:inLanguage $sourceLangVar . } }
                          """)

            query += pattern.substitute(sourceGraph=self.sourceGraph, localURIVar=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                    originalsGraph=self.originalsGraph, sourceLangVar=ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG)

        query += pattern.substitute(sourceGraph=self.sourceGraph, localURIVar=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                    originalsGraph=self.originalsGraph, sourceLangVar=ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG)

        query += ManifestationQuery._getUUIDAndLabelCreationAndBind()


        query += self._getFilterSourceQuadPattern()

        query += ' }'
        return query


class ManifestationUpdateQuery(ManifestationQuery):

    # -----------------------------------------------------------------------------
    def __init__(self, source, sourceGraph: str, targetGraph: str, originalsGraph: str,
                 entitySourceClass, linkIdentifier: tuple, identifiersToAdd: list):
        """

        Parameters
        ----------
        source : str
            The name of the data source. It will be used for comments.
        sourceGraph : str
            The name of the source graph without brackets, e.g. http://kb-manifestations
        targetGraph : str
            The name of the target graph without brackets, e.g. http://beltrans-manifestations
        originalsGraph : str
            The name of the graph with information about the translation's original, e.g. http://kb-originals
        entitySourceClass : str
            The RDF class used to identify a  record in the source graph,
            e.g. schema:CreativeWork or schema:Book
        linkIdentifier : tuple
            A (property, name) tuple specifying the name of the identifier used to identify update records
            and the property to fetch the data from the source, e.g. ('bibo:isbn13', 'ISBN13')
        identifiersToAdd : list
            A list of (property, name) tuples specifying the name of identifiers and the property with which
            it can be extracted from the source, e.g. [('bibo:isbn10', 'ISBN10')]
        """
        self.source = source
        self.sourceGraph = sourceGraph
        self.targetGraph = targetGraph
        self.originalsGraph = originalsGraph
        self.entitySourceClass = entitySourceClass
        self.linkIdentifier = linkIdentifier
        self.identifiersToAdd = identifiersToAdd

    # ---------------------------------------------------------------------------
    def _getFilterSourceQuadPattern(self):
        pattern = Template("""
        
       OPTIONAL { graph <$targetGraph> { $entityVar $identifierProperty $identifierVariable . } }
       FILTER EXISTS {
         graph <$targetGraph> { $entityVar $identifierProperty $identifierVariable . }
       }
       """)
        return pattern.substitute(targetGraph=self.targetGraph,
                                  identifierProperty=self.linkIdentifier[0],
                                  identifierVariable=self.getLinkIdentifierVarName(),
                                  entityVar=ManifestationQuery.VAR_MANIFESTATION_URI)


    # ---------------------------------------------------------------------------
    def getLinkIdentifierVarName(self):
        return Query.getIdentifierVarName(self.linkIdentifier[1])

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        query = "INSERT { "
        for property, object in [('schema:inLanguage', ManifestationQuery.VAR_MANIFESTATION_TARGET_LANG),
                                 ('btm:sourceLanguage', ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG),
                                 ('schema:sameAs', ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI)]:

            query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_URI,
                                                  property,
                                                  object,
                                                  graph=self.targetGraph,
                                                  optional=False,
                                                  newline=True)

        # Insert other identifiers which are optionally fetched
        for identifierProperty, identifierName in self.identifiersToAdd:

            if identifierProperty != '':
                query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_URI,
                                                   identifierProperty,
                                                   Query.getIdentifierVarName(identifierName),
                                                   graph=self.targetGraph,
                                                   optional=False,
                                                   newline=True)
            else:
                query += self._getINSERTIdentifiedByTriplePattern(identifierName)

        # definition of identifiers, e.g. ?viafEntityURI a bf:Identifier
        for identifierProperty, identifierName in self.identifiersToAdd:

            if identifierProperty != '':
                query += Query._getINSERTIdentifierDeclarationTriplePattern(identifierName, self.source)





        query += "} \n"  # end of INSERT block

        query += "WHERE { "


        query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                              'a',
                                              self.entitySourceClass,
                                              graph=self.sourceGraph,
                                              optional=False,
                                              newline=True)

        query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                               self.linkIdentifier[0],
                                               Query.getIdentifierVarName(self.linkIdentifier[1]),
                                               graph=self.sourceGraph,
                                               optional=False,
                                               newline=True)

        query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                               'schema:inLanguage',
                                               ManifestationQuery.VAR_MANIFESTATION_TARGET_LANG,
                                               graph=self.sourceGraph,
                                               optional=True,
                                               newline=True)

        # Optionally fetch other identifiers
        for identifierProperty, identifierName in self.identifiersToAdd:

            if identifierProperty != '':
                query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                                       identifierProperty,
                                                       Query.getIdentifierVarName(identifierName),
                                                       graph=self.sourceGraph,
                                                       optional=True,
                                                       newline=True)
            else:
                query += self._getIdentifierQuadPattern(identifierName, self.sourceGraph, optional=True)

        if self.source == 'BnF' or self.source == 'bnf':
            pattern = Template("""OPTIONAL { graph <$sourceGraph> { $localURIVar btm:sourceLanguage $sourceLangVar . } }
            """)
            query += pattern.substitute(sourceGraph=self.sourceGraph, localURIVar=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                        sourceLangVar=ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG)
        else:
            pattern = Template("""OPTIONAL { graph <$sourceGraph> { $localURIVar schema:translationOfWork ?originalURI . }
                                        graph <$originalsGraph> { ?originalURI schema:inLanguage $sourceLangVar . } }
                          """)

            query += pattern.substitute(sourceGraph=self.sourceGraph, localURIVar=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                    originalsGraph=self.originalsGraph, sourceLangVar=ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG)

        query += self._getFilterSourceQuadPattern()

        query += ' }'
        return query


class ManifestationSingleUpdateQuery(ManifestationQuery):

    # -----------------------------------------------------------------------------
    def __init__(self, source, sourceGraph: str, targetGraph: str, originalsGraph: str,
                 entitySourceClass, identifiersToAdd: list, correlationListFilter=False):
        """

        Parameters
        ----------
        source : str
            The name of the data source. It will be used for comments.
        sourceGraph : str
            The name of the source graph without brackets, e.g. http://kb-manifestations
        targetGraph : str
            The name of the target graph without brackets, e.g. http://beltrans-manifestations
        originalsGraph : str
            The name of the graph with information about the translation's original, e.g. http://kb-originals
        entitySourceClass : str
            The RDF class used to identify a  record in the source graph,
            e.g. schema:CreativeWork or schema:Book
        identifiersToAdd : list
            A list of (property, name) tuples specifying the name of identifiers and the property with which
            it can be extracted from the source, e.g. [('bibo:isbn10', 'ISBN10')]
        correlationListFilter : boolean
            A boolean flag indicating if a matching should only be performed if the target was not generated based on a correlation list,
            the default is False
        """
        self.source = source
        self.sourceGraph = sourceGraph
        self.targetGraph = targetGraph
        self.originalsGraph = originalsGraph
        self.entitySourceClass = entitySourceClass
        self.identifiersToAdd = identifiersToAdd
        self.correlationListFilter = correlationListFilter


    # ---------------------------------------------------------------------------
    def _getFilterSourceQuadPattern(self):
        pattern = Template("""
        
       OPTIONAL { graph <$targetGraph> { $entityVar $identifierProperty $identifierVariable . } }
       FILTER EXISTS {
         graph <$targetGraph> { $entityVar $identifierProperty $identifierVariable . }
       }
       """)
        return pattern.substitute(targetGraph=self.targetGraph,
                                  identifierProperty=self.linkIdentifier[0],
                                  identifierVariable=self.getLinkIdentifierVarName(),
                                  entityVar=ManifestationQuery.VAR_MANIFESTATION_URI)



    # ---------------------------------------------------------------------------
    def getLinkIdentifierVarName(self):
        return self.getIdentifierVarName(self.linkIdentifier[1])

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        query = "INSERT { "
        for property, object in [('schema:inLanguage', ManifestationQuery.VAR_MANIFESTATION_TARGET_LANG),
                                 ('btm:sourceLanguage', ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG),
                                 ('schema:sameAs', ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI)]:

            query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_URI,
                                                  property,
                                                  object,
                                                  graph=self.targetGraph,
                                                  optional=False,
                                                  newline=True)

        # Insert other identifiers which are optionally fetched
        # they are taken based on the first element of the tuple ('bibo:isbn10', 'ISBN-10')
        for identifierProperty, identifierName in self.identifiersToAdd:

            if identifierProperty != '':
                # create a direct property based on the first tuple element
                query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_URI,
                                                       identifierProperty,
                                                       self.getIdentifierVarName(identifierName),
                                                       graph=self.targetGraph,
                                                       optional=False,
                                                       newline=True)
            else:
                query += self._getINSERTIdentifiedByTriplePattern(identifierName)

            # create a triple pattern according to the BIBFRAME ontology
            # thus based on the name (second part of the tuple)
            query += self._getINSERTIdentifiedByTriplePattern(identifierName,
                                                              graph=self.targetGraph)

            query += Query._getINSERTIdentifierDeclarationTriplePattern(identifierName, 
                                                              self.source,
                                                              graph=self.targetGraph)

        query += "} \n"  # end of INSERT block

        query += "WHERE { "


        query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                              'a',
                                              self.entitySourceClass,
                                              graph=self.sourceGraph,
                                              optional=False,
                                              newline=True)


        query += Query._getUpdateCommentBindConcat(f'Added from {self.source} via ', Query.VAR_IDENTIFIER_TYPE_LABEL)
#        query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
#                                               self.linkIdentifier[0],
#                                               self.getIdentifierVarName(self.linkIdentifier[1]),
#                                               graph=self.sourceGraph,
#                                               optional=False,
#                                               newline=True)

        query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                               'schema:inLanguage',
                                               ManifestationQuery.VAR_MANIFESTATION_TARGET_LANG,
                                               graph=self.sourceGraph,
                                               optional=True,
                                               newline=True)

        query += Query._getGenericIdentifierQuadPattern(self.sourceGraph,
                                                        ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                                        ManifestationQuery.VAR_MANIFESTATION_URI,
                                                        self.targetGraph)

        if self.correlationListFilter:
            query += Query._getCorrelationListFilter(self.targetGraph, ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI, ManifestationQuery.VAR_MANIFESTATION_URI)

        # Optionally fetch other identifiers
        for identifierProperty, identifierName in self.identifiersToAdd:

            if identifierProperty != '':
                query += Query._getIdentifierStringPatternBIBFRAME(identifierName,
                                                                   subjectURIVariable=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                                                   graph=self.sourceGraph,
                                                                   optional=True)

                query += Query._getSimpleTriplePattern(ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                                       identifierProperty,
                                                       self.getIdentifierVarName(identifierName),
                                                       graph=self.sourceGraph,
                                                       optional=True,
                                                       newline=True)

            else:
                query += self._getIdentifierQuadPattern(identifierName, self.sourceGraph, optional=True)

        if self.source == 'BnF' or self.source == 'bnf':
            pattern = Template("""OPTIONAL { graph <$sourceGraph> { $localURIVar btm:sourceLanguage $sourceLangVar . } }
            """)
            query += pattern.substitute(sourceGraph=self.sourceGraph, localURIVar=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                        sourceLangVar=ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG)
        else:
            pattern = Template("""OPTIONAL { graph <$sourceGraph> { $localURIVar schema:translationOfWork ?originalURI . }
                                        graph <$originalsGraph> { ?originalURI schema:inLanguage $sourceLangVar . } }
                          """)

            query += pattern.substitute(sourceGraph=self.sourceGraph, localURIVar=ManifestationQuery.VAR_MANIFESTATION_LOCAL_URI,
                                    originalsGraph=self.originalsGraph, sourceLangVar=ManifestationQuery.VAR_MANIFESTATION_SOURCE_LANG)

#        query += self._getFilterSourceQuadPattern()

        query += ' }'
        return query



# -----------------------------------------------------------------------------
class ContributorCreateQuery(ContributorQuery, ABC):
    """
    With this query builder class, one can generate a SPARQL UPDATE query to add a person or organization
    from a local data source graph to a target graph in case there is not yet an existing target graph record
    pointing to the local person or organization via a schema:sameAs link.
    """

    # ---------------------------------------------------------------------------
    def _getFilterSourceQuadPattern(self):
#        pattern = Template("""
#    
#    FILTER NOT EXISTS {
#      graph <$targetGraph> {
#        ?entity a $entityType ;
#                schema:sameAs $localContributorURI .
#      }
#    }
#    """)

        pattern = Template("""
        OPTIONAL { graph <$targetGraph> { ?entity schema:sameAs $localContributorURI . } }
        FILTER(!bound(?entity))
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

class PersonContributorCreateQuery(ContributorCreateQuery):
    """
     With this query builder class, one can generate a SPARQL UPDATE query to add a person
     from a local data source graph to a target graph in case there is not yet an existing target graph record
     pointing to the local person or organization via a schema:sameAs link.
     """

    # -----------------------------------------------------------------------------
    def __init__(self, source, sourceGraph: str, targetGraph: str, identifiersToAdd: list,
                 entitySourceClass, entityTargetClass,
                 nationalityProperty='schema:nationality', genderProperty='schema:gender', labelProperty='rdfs:label',
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
        genderProperty : str
            The RDF property used to fetch gender information from the source graph, the default is schema:gender
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
        self.genderProperty = genderProperty
        self.entitySourceClass = entitySourceClass
        self.entityTargetClass = entityTargetClass
        self.labelProperty = labelProperty
        self.familyNameProperty = familyNameProperty
        self.givenNameProperty = givenNameProperty

        self.baseURL = Query.BASE_URL

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        insertBeginPattern = Template("""
    graph <$targetGraph> {
    """)

        query = "INSERT { "

        query += insertBeginPattern.substitute(targetGraph=self.targetGraph)
        query += Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                          'a',
                                                          self.entityTargetClass,
                                                          newline=True)
        query += self._getINSERTNationalityTriplePattern()
        query += self._getINSERTGenderTriplePattern()
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
            query += Query._getINSERTIdentifierDeclarationTriplePattern(identifier, self.source)

        query += "} "  # end of graph block
        query += "} "  # end of INSERT block

        query += "WHERE { "

        query += Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI,
                                                          'a',
                                                          self.entitySourceClass,
                                                          graph=self.sourceGraph)
        for property, object in [(self.labelProperty, ContributorQuery.VAR_CONTRIBUTOR_LABEL),
                                 (self.familyNameProperty, ContributorQuery.VAR_CONTRIBUTOR_FAMILY_NAME),
                                 (self.givenNameProperty, ContributorQuery.VAR_CONTRIBUTOR_GIVEN_NAME),
                                 (self.nationalityProperty, ContributorQuery.VAR_CONTRIBUTOR_NATIONALITY),
                                 (self.genderProperty, ContributorQuery.VAR_CONTRIBUTOR_GENDER)]:
            query += Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI,
                                                  property,
                                                  object,
                                                  graph=self.sourceGraph,
                                                  optional=True)

        query += Query._getUpdateCommentBindText(f'Created from {self.source} data')
        query += self._getUUIDCreationAndBind()
        # query += self._getSourceNationalityQuadPattern(self.sourceGraph, self.nationalityProperty)
        # query += self._getFilterExistsQuadPattern(self.sourceGraph, self.targetGraph, self.identifierName)


        for identifier in self.identifiersToAdd:
            if identifier != '':
                query += self._getIdentifierQuadPattern(identifier, self.sourceGraph, optional=True)

        query += self._getFilterSourceQuadPattern()

        query += ' }'
        return query

class OrganizationContributorCreateQuery(ContributorCreateQuery):
    """
         With this query builder class, one can generate a SPARQL UPDATE query to add an organization
         from a local data source graph to a target graph in case there is not yet an existing target graph record
         pointing to the local person or organization via a schema:sameAs link.
         """

    # -----------------------------------------------------------------------------
    def __init__(self, source, sourceGraph: str, targetGraph: str, identifiersToAdd: list,
                 entitySourceClass, entityTargetClass,
                 countryProperty='schema:address/schema:addressCountry', labelProperty='skos:prefLabel'):
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
        countryProperty : str
            The RDF property used to fetch the country information from the source graph, the default is the property path schema:address/schema:addressCountry
        entitySourceClass : str
            The RDF class used to identify a  record in the source graph,
            e.g. schema:Person, foaf:Person, schema:Organization or foaf:Organization
        entityTargetClass : str
            The RDF class used to specify the type of a newly created entity in the target graph
        labelProperty : str
            The RDF property used to fetch a name label in the source graph, the default is skos:prefLabel
        """
        self.source = source
        self.sourceGraph = sourceGraph
        self.targetGraph = targetGraph
        self.identifiersToAdd = identifiersToAdd
        self.countryProperty = countryProperty
        self.entitySourceClass = entitySourceClass
        self.entityTargetClass = entityTargetClass
        self.labelProperty = labelProperty

        self.baseURL = "http://kbr.be/id/data/"


    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        insertBeginPattern = Template("""
    graph <$targetGraph> {
    """)

        query = "INSERT { "

        query += insertBeginPattern.substitute(targetGraph=self.targetGraph)
        query += Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_URI,
                                                          'a',
                                                          self.entityTargetClass,
                                                          newline=True)

        query += self._getINSERTIdentifierTriplePattern()
        query += self._getINSERTSameAsTriplePattern()
        query += self._getINSERTContributorLabelTriplePattern()
        query += self._getINSERTContributorCommentTriplePattern(comment=f'Created from {self.source} data')
        query += self._getINSERTCountryTriplePattern()

        # bf:identifiedBy links, e.g. bf:identifiedBy ?viafEntityURI
        for identifier in self.identifiersToAdd:
            if identifier != '':
                query += self._getINSERTIdentifiedByTriplePattern(identifier)

        # definition of identifiers, e.g. ?viafEntityURI a bf:Identifier
        for identifier in self.identifiersToAdd:
            query += Query._getINSERTIdentifierDeclarationTriplePattern(identifier, self.source)

        query += "} "  # end of graph block
        query += "} "  # end of INSERT block

        query += "WHERE { "

        query += Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI,
                                                          'a',
                                                          self.entitySourceClass,
                                                          graph=self.sourceGraph)
        for property, object in [(self.labelProperty, ContributorQuery.VAR_CONTRIBUTOR_LABEL)]:
            query += Query._getSimpleTriplePattern(ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI,
                                                  property,
                                                  object,
                                                  graph=self.sourceGraph,
                                                  optional=True)

        query += Query._getUpdateCommentBindText(f'Created from {self.source} data')
        query += self._getUUIDCreationAndBind()
        query += self._getSourceCountryQuadPattern(self.sourceGraph, optional=True)
        # query += self._getFilterExistsQuadPattern(self.sourceGraph, self.targetGraph, self.identifierName)


        for identifier in self.identifiersToAdd:
            if identifier != '':
                query += self._getIdentifierQuadPattern(identifier, self.sourceGraph, optional=True)

        query += self._getFilterSourceQuadPattern()

        query += ' }'
        return query

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
                 nationalityProperty='schema:nationality', genderProperty='schema:gender', personClass='schema:Person',
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
        genderProperty : str
            The RDF property used to fetch gender information from the source graph, the default is schema:gender
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
        self.genderProperty = genderProperty
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
        query += self._getINSERTGenderTriplePattern()
        query += self._getINSERTSameAsTriplePattern()

        # bf:identifiedBy links, e.g. bf:identifiedBy ?viafEntityURI
        for identifier in self.identifiersToAdd:
            query += self._getINSERTIdentifiedByTriplePattern(identifier)

        # definition of identifiers, e.g. ?viafEntityURI a bf:Identifier
        for identifier in self.identifiersToAdd:
            query += Query._getINSERTIdentifierDeclarationTriplePattern(identifier, self.source)

        query += "} "  # end of graph block
        query += "} "  # end of INSERT block

        query += "WHERE { "

        query += self._getFilterSourceQuadPattern(self.sourceGraph, self.personClass, self.organizationClass)
        query += self._getSourceNationalityQuadPattern(self.sourceGraph, self.nationalityProperty, optional=True)
        query += self._getSourceGenderQuadPattern(self.sourceGraph, self.genderProperty, optional=True)
        query += self._getFilterExistsQuadPattern(self.sourceGraph, self.targetGraph, self.identifierName)
        query += self._getFilterCorrelationNotExist(self.targetGraph)

        query += Query._getUpdateCommentBindConcat(f'Added from {self.source} via ', Query.VAR_IDENTIFIER_TYPE_LABEL)
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
        if identifier == self.source:
            queryPart = """
                graph <$sourceGraph> { ?localContributorURI dcterms:identifier ?${identifier}Local . }
                """
        else:

            queryPart = """
        graph <$sourceGraph> {
          ?localContributorURI bf:identifiedBy ?${identifier}Entity .
    
          ?${identifier}Entity """ + identifierType + """
                                  rdf:value ?${identifier}Local .
        }
        """

        pattern = Template(queryPart + """
    OPTIONAL {
      graph <$targetGraph> {
        ?contributorURI bf:identifiedBy ?${identifier}TargetEntity .
        ?${identifier}TargetEntity """ + identifierType + """
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

    # ---------------------------------------------------------------------------
    def _getFilterCorrelationNotExist(self, targetGraph):
        """This function returns triple patterns for the WHERE clause used for the update functionality,
           i.e. only if the filter returns false the update will be performed.

        """
        pattern = Template("""

    # We do not want to add our local identifiers to an integrated record
    # which was created by a correlation list
    #FILTER NOT EXISTS {
    #  graph <$targetGraph> {
    #    ?correlationActivity a btm:CorrelationActivity ;
    #                         prov:generated ?contributorURI .
    #  }
    #}

    # We also do not want to add our local identifiers to a regularly integrated record
    # if this local record belongs to an integrated record made from a correlation list
    FILTER NOT EXISTS {
      graph <http://beltrans-contributors> {
        
        ?anyIntegratedContributorURI schema:sameAs ?localContributorURI .
        ?anyCorrelationActivity a btm:CorrelationActivity ;
                                prov:generated ?anyIntegratedContributorURI .
      }
    }
   """)
        return pattern.substitute(targetGraph=targetGraph)



# -----------------------------------------------------------------------------
class ContributorSingleUpdateQuery(ContributorQuery):
    """
    With this query builder class, one can generate a SPARQL UPDATE query to update a person or organization
    of a target graph with certain properties from a source graph and a schema:sameAs link back to the person/organization
    of the source graph.

    The properties added to the target graph are identifiers described using the BIBFRAME ontology,
    i.e. instances of bf:Identifier or bf:Isni to which is linked via bf:identifiedBy.
    The update will always add the nationality from the source graph as well as add a schema:sameAs link from target to source.

    With instances of this class it cannot be configured which identifiers will be used to identify a match
    between source and target graph: all identifiers are taken into account via a generic triple pattern.
    However,it can be configured which identifiers from the source will be added to the target.

    For example, the following call will generate a SPARQL UPDATE query which tries to make a link between
    source and target graph using all available identifiers and will add VIAF and Wikidata identifiers to the target.

    qb = ContributorUpdateQuery("KBR", "http://kbr-data", "http://integrated-data", ["VIAF", "Wikidata"])
    """

    # ---------------------------------------------------------------------------
    def __init__(self, source, sourceGraph: str, targetGraph: str, identifiersToAdd: list,
                 nationalityProperty='schema:nationality', genderProperty='schema:gender', personClass='schema:Person',
                 organizationClass='schema:Organization', correlationListFilter=False):
        """

        Parameters
        ----------
        source : str
            The name of the data source which will be used for comments, for example "KBR"
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
        genderProperty : str
            The RDF property used to fetch gender information from the source graph, the default is schema:gender
        personClass : str
            The RDF class used to identify a person record in the source graph, the default is schema:Person
        organizationClass : str
            The RDF class used to identify an organization record in the source graph, the default is schema:Organization
        correlationListFilter : boolean
            A boolean flag indicating if a matching should only be performed if the target was not generated based on a correlation list,
            the default is False
        """
        self.source = source
        self.sourceGraph = sourceGraph
        self.targetGraph = targetGraph
        self.identifiersToAdd = identifiersToAdd
        self.nationalityProperty = nationalityProperty
        self.genderProperty = genderProperty
        self.personClass = personClass
        self.organizationClass = organizationClass
        self.correlationListFilter = correlationListFilter

        self.baseURL = "http://kbr.be/id/data/"

    # ---------------------------------------------------------------------------
    def _buildQuery(self):

        insertBeginPattern = Template("""
    graph <$targetGraph> {
    """)

        query = "INSERT { "

        query += insertBeginPattern.substitute(targetGraph=self.targetGraph)
        query += self._getINSERTNationalityTriplePattern()
        query += self._getINSERTGenderTriplePattern()
        query += self._getINSERTSameAsTriplePattern()

        # bf:identifiedBy links, e.g. bf:identifiedBy ?viafEntityURI
        for identifier in self.identifiersToAdd:
            query += self._getINSERTIdentifiedByTriplePattern(identifier)

        # definition of identifiers, e.g. ?viafEntityURI a bf:Identifier
        for identifier in self.identifiersToAdd:
            query += Query._getINSERTIdentifierDeclarationTriplePattern(identifier, self.source)

        query += "} "  # end of graph block
        query += "} "  # end of INSERT block

        query += "WHERE { "

        query += self._getFilterSourceQuadPattern(self.sourceGraph, self.personClass, self.organizationClass)

        #query += self._getGenericIdentifierQuadPattern(self.sourceGraph, self.targetGraph, self.correlationListFilter)
        query += Query._getGenericIdentifierQuadPattern(self.sourceGraph, ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI, ContributorQuery.VAR_CONTRIBUTOR_URI, self.targetGraph)
        if self.correlationListFilter:
            query += Query._getCorrelationListFilter(self.targetGraph, ContributorQuery.VAR_CONTRIBUTOR_LOCAL_URI, ContributorQuery.VAR_CONTRIBUTOR_URI)
        query += self._getSourceNationalityQuadPattern(self.sourceGraph, self.nationalityProperty, optional=True)
        query += self._getSourceGenderQuadPattern(self.sourceGraph, self.genderProperty, optional=True)

        query += Query._getUpdateCommentBindConcat(f'Added from {self.source} via ', Query.VAR_IDENTIFIER_TYPE_LABEL)
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
    def _getGenericIdentifierQuadPattern(self, sourceGraph, targetGraph, correlationListFilter=False):
        """This function returns triple patterns for the WHERE clause used for the update functionality."""

        queryPart = """
        graph <$sourceGraph> {
          ?localContributorURI bf:identifiedBy ?localIdentifierEntity .
    
          ?localIdentifierEntity a ?type ;
                                 rdfs:label ?typeLabel ;
                                 rdf:value ?identifierLocal .
        }

        graph <$targetGraph> {
          ?contributorURI bf:identifiedBy ?identifierTargetEntity .

          ?identifierTargetEntity a ?type ;
                                  rdfs:label ?typeLabel ;
                                  rdf:value ?identifierLocal .
        }
        """

        if correlationListFilter:
          queryPart += """
          OPTIONAL { graph <$targetGraph> { ?activity a btm:CorrelationActivity ; prov:used ?localContributorURI . } }
          OPTIONAL { graph <$targetGraph> { ?activity a btm:CorrelationActivity ; prov:generated ?contributorURI . } }
          FILTER( !bound(?activity) ) 
        """

        pattern = Template(queryPart)

        return pattern.substitute(sourceGraph=sourceGraph, targetGraph=targetGraph)




# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import doctest

    doctest.testmod()
