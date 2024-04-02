# Cypher - Select Data with MATCH

[Back](../index.md)

- [Cypher - Select Data with MATCH](#cypher---select-data-with-match)
  - [Fetch all Nodes](#fetch-all-nodes)
  - [Relationships](#relationships)
    - [Chain Relationships](#chain-relationships)
    - [Node has not relationship](#node-has-not-relationship)
  - [WHERE Clause](#where-clause)
  - [Return Clause](#return-clause)
  - [Order By Clause](#order-by-clause)
  - [LIMIT Clause](#limit-clause)
  - [SKIP Clause](#skip-clause)
  - [WITH Clause](#with-clause)

---

## Fetch all Nodes

```cypher
MATCH (n) RETURN n
```

---

## Relationships

### Chain Relationships

```cypher
MATCH p=(:Service)-[:CAN_WRITE_TO|CAN_READ_FROM*5]->(:Service)
RETURN p


MATCH
p=(e:Employee)<-[:REPORTS_TO*]-(sub:Employee)
WHERE
sub.firstName = 'Robert'
RETURN
p
```

---

### Node has not relationship

```cypher
MATCH
(e:Employee)
WHERE
NOT (e)-[:REPORTS_TO]->()
RETURN
e.firstName as bigBoss
```



---

## WHERE Clause

```cypher
CREATE (a:Actors { Name : "Sonu Nigam" })

MATCH (a:Actors)
WHERE a.Name = "Sonu Nigam"
RETURN a

// with Multiple Conditions
MATCH (stu:Student)
WHERE stu.name = 'Abc' AND stu.name = 'Xyz'
RETURN stu
```

---

## Return Clause

- Syntax

```cypher
// Return a single Node
Create (node:label {properties})
RETURN node

// Return Multiple Nodes
Create (node1:label {properties})
Create (node2:label {properties})
Create (node N:label {properties})
RETURN node1, node2.... node N

// Return Relationships
CREATE (node1)-[Relationship:Relationship_type]->(node2)
RETURN Relationship

// Return Properties
Match (node:label {properties:values})
Return node.property

// Return All Elements
Match m = (n {name: "India", result: "Winners"})-[r]-(x)
RETURN *

```

---

## Order By Clause

```cypher
MATCH (n)
RETURN n.property1, n.property2 . . . . . . . .
ORDER BY n.property

// Order Nodes by Multiple Properties
MATCH (n)
RETURN n
ORDER BY n.property_1, n.property_2


// Order Nodes in Descending Order
MATCH (n)
RETURN n
ORDER BY n.property DESC
```

---

## LIMIT Clause

```cypher
MATCH (n)
RETURN n
ORDER BY n.name
LIMIT i

// LIMIT with Expression
MATCH (n)
RETURN n.name, n.Marks
ORDER BY n.Marks DESC
LIMIT toInt(3 * rand())+ 1
```

---

## SKIP Clause

```cypher
// skipping the first 3 nodes.
MATCH (n)
RETURN n.name, n.Marks
ORDER BY n.Marks DESC
SKIP 3

// with Expression
MATCH (n)
RETURN n.name, n.Marks
ORDER BY n.Marks DESC
SKIP toInt (2*rand())+ 1

```

---

## WITH Clause

```cypher
MATCH (n)
WITH n
ORDER BY n.property
RETURN collect(n.property)

MATCH (n)
WITH n
ORDER BY n.name DESC LIMIT 3
RETURN collect(n.name)
```

---

[TOP](#cypher---select-data-with-match)
