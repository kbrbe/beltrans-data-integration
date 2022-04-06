
## Integration test of dataprofile queries

As part of our pipeline we query data from a RDF triple store to create CSV files.
To verify that the query and postprocessing of the results works correct we created test data
to cover border cases with respect to books and contributors from different sources and their links.

|  KBR book URI    | BnF book URI     | In corpus? | Belgian contributor? | ISBN10 | ISBN13 | book link     |
|------------------|------------------|------------|----------------------|--------|--------|---------------|
| `btid:kbrBook1`  | `-`              | Yes        | KBR                  | `-`    | `-`    | `-`           |
| `btid:kbrBook2`  | `-`              | No         | `-`                  | `-`    | `-`    | `-`           |
| `-`              | `btid:bnfBook1`  | Yes        | BnF                  | `-`    | `-`    | `-`           |
| `-`              | `btid:bnfBook2`  | No         | `-`                  | `-`    | `-`    | `-`           |
| `btid:kbrBook3`  | `-`              | Yes        | KBR                  | Yes    | `-`    | `-`           |
| `-`              | `btid:bnfBook3`  | Yes        | BnF                  | Yes    | `-`    | `-`           |
| `btid:kbrBook4`  | `btid:bnfBook4`  | Yes        | KBR,BnF              | Yes    | `-`    | ISBN10        |
| `btid:kbrBook5`  | `btid:bnfBook5`  | Yes        | KBR                  | Yes    | `-`    | ISBN10        |
| `btid:kbrBook6`  | `-`              | No         | `-`                  | Yes    | `-`    | `-`           |
| `-`              | `btid:bnfBook6`  | No         | `-`                  | Yes    | `-`    | `-`           |
| `btid:kbrBook7`  | `btid:bnfBook7`  | Yes        | BnF                  | Yes    | `-`    | `-`           |
| `btid:kbrBook8`  | `btid:bnfBook8`  | No         | `-`                  | Yes    | `-`    | ISBN10        |
| `btid:kbrBook9`  | `-`              | Yes        | KBR                  | `-`    | Yes    | `-`           |
| `-`              | `btid:bnfBook9`  | Yes        | BnF                  | `-`    | Yes    | `-`           |
| `btid:kbrBook10` | `btid:bnfBook10` | Yes        | KBR,BnF              | `-`    | Yes    | ISBN13        |
| `btid:kbrBook11` | `btid:bnfBook11` | Yes        | KBR                  | `-`    | Yes    | ISBN13        |
| `btid:kbrBook12` | `-`              | No         | `-`                  | `-`    | Yes    | `-`           |
| `-`              | `btid:bnfBook12` | No         | `-`                  | `-`    | Yes    | `-`           |
| `btid:kbrBook13` | `btid:bnfBook13` | Yes        | BnF                  | `-`    | Yes    | ISBN13        |
| `btid:kbrBook14` | `btid:bnfBook14` | No         | `-`                  | `-`    | Yes    | ISBN13        |
| `btid:kbrBook15` | `-`              | Yes        | KBR                  | Yes    | Yes    | `-`           |
| `-`              | `btid:bnfBook15` | Yes        | BnF                  | Yes    | Yes    | `-`           |
| `btid:kbrBook16` | `btid:bnfBook16` | Yes        | KBR,BnF              | Yes    | Yes    | ISBN10        |
| `btid:kbrBook17` | `btid:bnfBook17` | Yes        | KBR                  | Yes    | Yes    | ISBN10        |
| `btid:kbrBook18` | `-`              | No         | `-`                  | Yes    | Yes    | `-`           |
| `-`              | `btid:bnfBook18` | No         | `-`                  | Yes    | Yes    | `-`           |
| `btid:kbrBook19` | `btid:bnfBook19` | Yes        | BnF                  | Yes    | Yes    | ISBN10        |
| `btid:kbrBook20` | `btid:bnfBook20` | No         | `-`                  | Yes    | Yes    | ISBN10        |
| `btid:kbrBook21` | `btid:bnfBook21` | Yes        | KBR,BnF              | Yes    | Yes    | ISBN13        |
| `btid:kbrBook22` | `btid:bnfBook22` | Yes        | KBR                  | Yes    | Yes    | ISBN13        |
| `btid:kbrBook23` | `btid:bnfBook23` | Yes        | BnF                  | Yes    | Yes    | ISBN13        |
| `btid:kbrBook24` | `btid:bnfBook24` | No         | `-`                  | Yes    | Yes    | ISBN13        |
| `btid:kbrBook25` | `btid:bnfBook25` | Yes        | KBR,BnF              | Yes    | Yes    | ISBN10,ISBN13 |
| `btid:kbrBook26` | `btid:bnfBook26` | Yes        | KBR                  | Yes    | Yes    | ISBN10,ISBN13 |
| `btid:kbrBook27` | `btid:bnfBook27` | Yes        | BnF                  | Yes    | Yes    | ISBN10,ISBN13 |
| `btid:kbrBook28` | `btid:bnfBook28` | No         | `-`                  | Yes    | Yes    | ISBN10,ISBN13 |

The queried test corpus should contain **23** books.

## Detect quality issues

For the SPARQL query to return correct results the following assumptions must hold:

* No books with more than one ISBN10
* No books with more than one ISBN13

These constraints need to be expressed and checked on the data.

Other issues with respect to poor or erroneous data:

* Books with no contributors

