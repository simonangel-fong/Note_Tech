# Cypher - Create Nodes

[Back](../index.md)

- [Cypher - Create Nodes](#cypher---create-nodes)
  - [Create Nodes](#create-nodes)

---

## Create Nodes

| Syntax                                            | Description                               |
| ------------------------------------------------- | ----------------------------------------- |
| `CREATE (node_name);`                             | Create a Single Node                      |
| `CREATE (node1),(node2),(noden);`                 | Create multiple nodese                    |
| `CREATE (node:label)`                             | Create a node with a label                |
| `CREATE (node:label1:label2:labeln)`              | Create multiple labels with a single node |
| `CREATE (node:label { key1: value, key2: value})` | Create Node with Properties               |
| `CREATE (Node:Label{properties}) RETURN Node`     | return the newly created node             |

- `label`
  - used to classify the nodes using labels.
- semicolon `;`:
  - optional.
- the curly braces `{ }`:
  - specify properties separated.

---

```cypher
CREATE(single);  // single is the name of the node
MATCH (n)
RETURN n

CREATE (primary_node), ( secondary_node);

CREATE (Kalam:scientist)
CREATE (Kalam:person:president:scientist)

CREATE (Ajeet:Developer{name: "Ajeet Kumar", YOB: 1989, POB: "Mau"})

CREATE (Sonoo:trainer{name: "Sonoo Jaiswal", YOB: 1987, POB: "Faizabad"}) RETURN Sonoo
```

---

[TOP](#cypher---create-nodes)
