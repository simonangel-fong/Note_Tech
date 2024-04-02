# Cypher - Merge Command

[Back](../index.md)

- [Cypher - Merge Command](#cypher---merge-command)
  - [Merge Command](#merge-command)
  - [OnCreate and OnMatch](#oncreate-and-onmatch)
  - [Merge a Relationship](#merge-a-relationship)

---

## Merge Command

- `MERGE` command

  - a combination of `CREATE` and `MATCH` command.
  - used to **search** for a given pattern in the graph.
    - If it exists in the graph then it will return the result.
    - Otherwise, it creates a new node/relationship and returns the results.

| Syntax                                                    | Desc                         |
| --------------------------------------------------------- | ---------------------------- |
| `MERGE (node:label)`                                      | Merge a node with label      |
| `MERGE (node:label {key1:value, key2:value, key3:value})` | Merge a Node with Properties |

---

- Example

```cypher
CREATE (sachin:player{name: "Sachin Tendulkar", YOB: 1968, POB: "Mumbai"})
CREATE (Ind:Country {name: "India"})
CREATE (sachin)-[r:BATSMAN_OF]->(Ind)


// ======== Merge a Node with a Label =========
MERGE (Sehwag:player) RETURN Sehwag
// (:player {POB: "Mumbai",name: "Sachin Tendulkar",YOB: 1968})
// return only one node "Sachin Tendulkar"

// ======== Merge a Node with Properties ========
MERGE (CT:Tornament{name: "ICC Champions Trophy"})
RETURN CT, labels(CT)
// (:Tornament {name: "ICC Champions Trophy"})│["Tornament"]
// will create new node and return


MERGE (Sehwag:player {name: "Virendra Sehwag", YOB: 1978, POB: "Najafgarh"})
RETURN Sehwag
// (:player {POB: "Najafgarh",name: "Virendra Sehwag",YOB: 1978})


```

---

## OnCreate and OnMatch

- used to indicate whether the node is created or matched. Whenever, we execute a merge query, a node is either matched or created.

- Syntax

```cypher
MERGE (node:label {properties . . . . . . . . . . .})
ON CREATE SET property.isCreated ="true"
ON MATCH SET property.isFound ="true"
```

- Example

```cypher
MERGE (Sehwag:player {name: "Virendra Sehwag", YOB: 1978, POB: "Najafgarh"})
ON CREATE SET Sehwag.isCreated = "true"
ON MATCH SET Sehwag.isFound = "true"
RETURN Sehwag
// (:player {isFound: "true",POB: "Najafgarh",name: "Virendra Sehwag",YOB: 1978})
```

---

## Merge a Relationship

```cypher
MATCH (a:Country), (b:Tournament)
   WHERE a.name = "India" AND b.name = "ICC Champions Trophy"
   MERGE (a)-[r:WINNERS_OF]->(b)
RETURN a, b
```

---

[TOP](#cypher---merge-command)
