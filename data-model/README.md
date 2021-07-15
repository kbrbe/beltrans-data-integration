# Data model

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
For example `<http://data.bnf.fr/ark:/12148/cb11927594h#about>` for a person,
more concretely an instance of `foaf:Person`,
and `<http://data.bnf.fr/ark:/12148/cb11927594h> for the metadata entity of this person,
more concretely an instance of `skos:Concept`.

The tool [trifid](https://github.com/zazuko/trifid) which provides a basic UI to browse resources seems to have issues with the BnF notation.
The HTML anchor `#about` which is part of the IRI of a thing is not recognized
as part of the IRI in trifid but just as HTML anchor.
Thus trifid shows the related metadata entity.

## Authors

According to a LRM to schema.org mapping performed by the Royal Library of the Netherlands (KB),
the *LRM Agent* concept is not fully compatible with a `schema:Agent`,
because *LRM agents* are non-fictive persons who are alive or have lived.
Different personas (or pseudonyms of authors) are represented as different instances of `schema:Person`,
which are linked together with `schema:sameAs`.


## Translations

According to the LRM to schema.org mapping the property `schema:translationOfWork` can be used between two expressions.
