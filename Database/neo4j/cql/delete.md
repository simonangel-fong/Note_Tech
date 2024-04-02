# Cypher - Delete Command

[Back](../index.md)

- [Cypher - Delete Command](#cypher---delete-command)
  - [Delete a Node](#delete-a-node)
  - [Delete a Relationship](#delete-a-relationship)
  - [DELETE all Nodes and Relationships](#delete-all-nodes-and-relationships)
  - [Delete All Database](#delete-all-database)

---

## Delete a Node

```cypher
// Delete a Node
MATCH (Kohli:person {Name: "Virat Kohli"})
DELETE Kohli

// Delete Multiple Nodes
MATCH (a:Student {Name: "Chris Grey"}), (b:Employee {Name: "Mark Twin"})
DELETE a,b
```

---

## Delete a Relationship

```cypher
// Delete a Relationship
MATCH (Raul)-[r:PLAYER_OF]->(It)
DELETE r

// delete a node and all relationships related to that node
MATCH (Kohli:player{name: "Virat Kohli"})
DETACH DELETE Kohli
```

---

## DELETE all Nodes and Relationships

```cypher
// Delete All Nodes
MATCH (n) DELETE n
// The above statement cannot delete nodes if they have any relationships.
// In other words, you must delete any relationships before you delete the node itself.

// Detach and delete all nodes
MATCH (Kohli:player{name: "Virat Kohli"})
DETACH DELETE Kohli
```

---

## Delete All Database

```cypher
// delete all database
DETACH DELETE;
```

---

[TOP](#cypher---delete-command)
