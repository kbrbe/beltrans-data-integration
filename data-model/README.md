# Data model

This data model has the aim to enable data stewardship on bibliographic data from heterogeneous data sources.

## Explanations

In this document we develop requirements in the form of user stories which are rendered the following:

> :smiley: *I am a user story from the perspective of the public*

> :computer: *I am a user story from the perspective of a data steward*

> :books: *I am a user story from the perspective of a researcher*

Our data model is represented using the Resource Description Framework (RDF)
and for the different components of the model (and the data) we use the following namespaces.

```
# BELTRANS data model (concepts and properties)
btm: <http://data.kbr.be/beltrans/model#> .

# BELTRANS data model shapes (constraints on the data)
bts: <http://data.kbr.be/beltrans/shapes#> .

# BELTRANS data regarding real world things
btd: <http://data.kbr.be/id/data/> .

# BELTRANS data regarding metadata entities
btmd: <http://data.kbr.be/about/data/>
```

## High level goals

The aim of this data model is to represent books, their translations as well as involved parties such as authors, publishers, etc within a RDF Knowledge Graph (Linked Data).
Therefore we have to consider the following high-level objectives:

* Translations are different *expressions* of some *creative work* (similar to how the original work is only *one possible* expression of a *creative work*)
* *Things*, such as authors or creative works, are different to their descriptions and thus both should be represented by different URIs
* Different Linked Data vocabularies may be used to express our conceptual model
* Constraints on data may be expressed on source data, e.g. to verify their completeness with respect to the constraints, or on the already integrated data

In the following we elaborate on the data model.

## Metadata entities

Following Linked Data best practices a thing or person is different to their descriptions.
Such a model is also applied at KB and BnF.

At **KB**, a *thing* has `id` in its namespace
and metadata entities about things have `doc` in their namespaces.
For example `<http://data.bibliotheken.nl/id/nbt/w1234567>` for a thing,
more concretely an instance of `schema:CreativeWork` and `schema:Book`,
and `<http://data.bibliotheken.nl/doc/nbt/w1234567>` for the metadata entity of this book,
more concretely an instance of `schema:WebPage` and `schema:Dataset`.

At **BnF** a *thing*'s URI is reused for the metadata entity
but without the trailing `#about` (an HTML anchor).
For example `<http://data.bnf.fr/ark:/12148/cb11927594h>` for a person,
more concretely an instance of `foaf:Person`,
and `<http://data.bnf.fr/ark:/12148/cb11927594h#about> for the metadata entity of this person,
more concretely an instance of `skos:Concept`.

The tool [trifid](https://github.com/zazuko/trifid) which provides a basic UI to browse resources seems to have issues with the notation of BnF.
The HTML anchor `#about` which is part of the IRI of a thing is not recognized
as part of the IRI in trifid but just as HTML anchor.
Thus, instead of the metadata entity trifid always shows the related *thing*
(the other URI without `#about`) assuming there is a `#about` section in the HTML page.

> :computer: *As a data steward, I want to represent information about things different from things.*

## Authors

Authors usually have a given name and a family name and might be uniquely identified by an International Standard Name Identifier (ISNI).
Besides an actual author, any expression may have several other collaborators involved
such as translators or illustrators.
For the BELTRANS project the nationality of authors is important
as we only consider Belgian authors.

According to a LRM to schema.org mapping performed by the Royal Library of the Netherlands (KB),
the *LRM Agent* concept is not fully compatible with a `schema:Agent`,
because *LRM agents* are non-fictive persons who are alive or have lived.
Different personas (or pseudonyms of authors) are represented as different instances of `schema:Person`,
which are linked together with `schema:sameAs`.


> :books: *As a researcher, I want to get all information related to an author.*

## Translations

According to the LRM to schema.org mapping the property `schema:translationOfWork` can be used between two expressions.
