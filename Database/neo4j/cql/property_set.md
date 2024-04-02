# Cypher - Set Property

[Back](../index.md)

- [Cypher - Set Property](#cypher---set-property)
  - [Set a Label on a Node](#set-a-label-on-a-node)
  - [Set Property](#set-property)
  - [Remove a Property](#remove-a-property)

---

## Set a Label on a Node

- Syntax

```cypher
MATCH (n {properties . . . . . . . })
SET n :label
RETURN n
```

- Example: Single label

```cypher
CREATE (Ganguly {name: "Saurav Ganguly", YOB: 1968, POB: "Kolkata"})

MATCH (Ganguly {name: "Saurav Ganguly", YOB: 1968, POB: "Kolkata"})
SET Ganguly: player
RETURN Ganguly
```

- Example: Multiple label

```cypher
CREATE (Chetan {name: "Chetan Sharma", YOB: 1958, POB: "Delhi"})

MATCH (Chetan {name: "Chetan Sharma", YOB: 1958, POB: "Delhi"})
SET Chetan: player:person
RETURN Chetan
```

---

## Set Property

- Syntax

```cypher
// set
MATCH (node:label {properties})
SET node.property1 = value, node.property2 = value
RETURN node
```

- Example

```cypher
CREATE (Hardik:player{name: "Hardik Pandya", YOB: 1992, POB: "Gujrat"})

MATCH (Hardik:player{name: "Hardik Pandya", YOB: 1992, POB: "Gujrat"})
SET Hardik.hattrick = 666
RETURN Hardik

```

---

## Remove a Property

- Syntax

```cypher
MATCH (node:label {properties})
SET node.property = NULL
RETURN node
```

- Example

```cypher
Create (Dhoni:player {name: "Mahendra Singh Dhoni", YOB: 1978, POB: "Bihar"})

MATCH (Dhoni:player {name: "Mahendra Singh Dhoni", YOB: 1978, POB: "Bihar"})
SET Dhoni.POB = NULL
RETURN Dhoni
```

---

[TOP](#cypher---set-property)
