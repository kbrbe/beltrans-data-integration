
## Integration test of dataprofile queries

As part of our pipeline we query data from a RDF triple store to create CSV files.
To verify that the query and postprocessing of the results works correct we created test data
to cover border cases with respect to books and contributors from different sources and their links.

* A KBR book with no ISBN information
  * One with a BE contributor (this should appear once in the output, `btid:kbrBookA_author_BE`)
  * One without BE contributors (this should NOT appear in the output, `btid:kbrBookA`)
* A KBR book with one ISBN10 (no match to other sources)
  * One with a BE contributor (this should appear once in the output, `btid:kbrBookB_illustrator_BE`)
  * One without BE contributors (this should NOT appear in the output, `btid:kbrBookB`)
* A KBR book with one ISBN10 (link to BnF)
  * One with a BE contributor, linked to BnF which also has a Belgian contributor (this should appear once in the output, `btid:kbrBookC_author_BE` linked `btid:bnfBookC_author_BE`)
  * One with a BE contributor, linked to Bnf, but the BnF version does not indicate a BE contributor (this should appear once in the output, `btid:kbrBookC_author_BE2` with linked `btid:bnfBookC_author_BE2`)
  * One without BE contributors (this should NOT appear in the output, `btid:kbrBookC`)
  * One without BE contributor, but linked to BnF which has a BE contributor (this should appear once in the output, `btid:kbrBookC_no_BE` and linked `btid:bnfBookC_author_BE3`)
* one KBR book with one ISBN13 (no match to other sources)
  * One with a BE contributor (this should appear once in the output, `btid:kbrBookD_author_BE`)
  * One without BE contributors (this should NOT appear in the output, `btid:kbrBookD`)
* one KBR book with one ISBN13 (link to BnF)
  * One with a BE contributor (this should appear once in the output, `btid:kbrBookE_scenarist_BE`, linked to `btid:bnfBookE_scenarist_BE`)
  * One with a BE contributor, linked to Bnf, but the BnF version does not indicate a BE contributor (this should appear once in the output, `btid:kbrBookE_scenarist_BE2` and linked `btid:bnfBookE_scenarist_BE2`)
  * One without BE contributors (this should NOT appear in the output, `btid:kbrBookE`)
  * One without BE contributor, but linked to BnF which has a BE contributor (this should appear once in the output, `btid:kbrBookE_no_BE` with linked `btid:bnfBookE_author_BE3`)
* one KBR book with ISBN10 and one ISBN 13 (no match to other sources)
  * One with a BE contributor (this should appear once in the output)
  * One without BE contributors (this should NOT appear in the output)
* one KBR book with ISBN10 and one ISBN13 (link to BnF via both)
  * One with a BE contributor (this should appear once in the output)
  * One without BE contributors (this should NOT appear in the output)

## Detect quality issues

For the SPARQL query to return correct results the following assumptions must hold:

* No books with more than one ISBN10
* No books with more than one ISBN13

These constraints need to be expressed and checked on the data.

Other issues with respect to poor or erroneous data:

* Books with no contributors

