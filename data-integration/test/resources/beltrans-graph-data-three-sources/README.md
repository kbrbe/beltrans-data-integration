
## Integrated data

| Book URI      | Author URI                                    | Illustrator URI        | Scenarist URI          | In corpus? | 
|---------------|-----------------------------------------------|------------------------|------------------------|------------|
| `btid:book1`  | `btid:contributor1BE  `                       | `-`                    |                        | Yes        |
| `btid:book2`  | `btid:contributor2BE`, `btid:contributor3FR`  | `-`                    |                        | Yes        |
| `btid:book3`  | `-`                                           | `btid:contributor4BE`  | `-`                    | Yes        |
| `btid:book4`  | `-`                                           | `-`                    | `btid:contributor5BE`  | Yes        |
| `btid:book5`  | `-`                                           | `-`                    | `btid:contributor6FR`  | No         |
| `btid:book6`  | `-`                                           | `btid:contributor7FR`  | `btid:contributor8FR`  | No         |
| `btid:book7`  | `-`                                           | `btid:contributor9BE`  | `btid:contributor10FR` | Yes        |
| `btid:book8`  | `btid:contributor11BE`                        | `btid:contributor11BE` | `-`                    | Yes        |

## Correspondence between integrated manifestations and sources

| Manifestation URI      | KBR URI            | BnF URI            | KB URI           |
|------------------------|--------------------|--------------------|------------------|
| `btid:book1`           | `btid:kbrBook1`    |                    |                  |
| `btid:book2`           | `-`                | `btid:bnfBook2`    | `btid:kbBook2`  |
| `btid:book3`           | `btid:kbrBook3`    |                    |                  |
| `btid:book4`           |                    |                    |                  |
| `btid:book5`           |                    | `btid:bnfBook5`    |                  |
| `btid:book6`           |                    | `btid:bnfBook6`    |                  |
| `btid:book7`           | `btid:kbrBook7`    | `btid:bnfBook7`    |                  |
| `btid:book8`           | `btid:kbrBook8`    |                    | `btid:kbrBook8`  |

## Correspondence between integrated contributors and sources

| Contributor URI        | KBR URI            | BnF URI            | KB URI           |
|------------------------|--------------------|--------------------|------------------|
| `btid:contributor1BE`  | `btid:kbrCont1BE`  | `btid:bnfCont1`    | `-`              |
| `btid:contributor2BE`  | `btid:kbrCont2`    | `-`                | `btid:kbCont2BE` |
| `btid:contributor3FR`  | `-`                | `btid:bnfCont3FR`  | `btid:kbCont3`   |
| `btid:contributor4BE`  | `btid:kbrCont4BE`  | `-`                | `-`              |
| `btid:contributor5BE`  | `-`                | `btid:bnfCont5FR`  | `btid:kbCont5BE` |
| `btid:contributor6FR`  | `-`                | `btid:bnfCont6FR`  | `btid:kbCont6FR` |
| `btid:contributor7FR`  | `-`                | `btid:bnfCont7FR`  | `-`              |
| `btid:contributor8FR`  | `-`                | `btid:bnfCont8FR`  | `-`              |
| `btid:contributor9BE`  | `btid:kbrCont9BE`  | `-`                | `-`              |
| `btid:contributor10FR` | `btid:kbrCont10FR` | `btid:bnfCont10FR` | `-`              |
| `btid:contributor11BE` | `btid:kbrCont11BE` | `btid:bnfCont11BE` | `btid:kbCont11`  |

The queried test corpus should contain **6** books.

