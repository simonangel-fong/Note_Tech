# Neo4j - GraphDB

[Back](../index.md)

- [Neo4j - GraphDB](#neo4j---graphdb)
  - [GraphDB](#graphdb)
    - [Labeled Property Graph Model](#labeled-property-graph-model)
  - [Pros and Cons](#pros-and-cons)
  - [Graph Database vs. RDBMS](#graph-database-vs-rdbms)
  - [GraphDB vs NoSQL Database](#graphdb-vs-nosql-database)

---

## GraphDB

- `graph`

  - a collection of vertices and edges
  - a set of nodes and the relationships that connect them

- Graph database

  - very useful now a day because in graph databases data exist **in the form of the relationship between different objects.**
  - The **relationship** between the data is more valuable than the data itself.
  - can be used with OLTP systems
    - provide features like transactional integrity and operational availability.

---

### Labeled Property Graph Model

- `Nodes`

  - represent **entities** and **complex types**
  - can contain `properties` (key-value pairs).
  - Each node can have different properties

- `Relationships`

  - Every relationship has a **name** and **direction**
  - Relationships can contain `properties`, which can further clarify the relationship
  - Must have a **start and end node**

- `Properties`

  - **Key value pairs** used for nodes and relationships
  - **Adds metadata** to your nodes and relationships
  - Entity attributes
  - Relationship qualities

- `Labels`
  - Used to **represent objects** in your domain (e.g. user, person, movie)
  - With labels, you can **group** nodes
  - Allows us to create **indexes** and **constraints** with groups of nodes

---

## Pros and Cons

- Pros:
  - Powerful data **model**, as general as RDBMS
  - Connected data locally **indexed**
  - Easy to **query**
- Cons
  - **Sharding** (lots of people working on this)
    - Scales UP reasonably well
  - Requires rewiring your **brain**

---

## Graph Database vs. RDBMS

| Graph Database                                       | RDBMS                                     |
| ---------------------------------------------------- | ----------------------------------------- |
| data is stored in **graphs**.                        | data is stored in **tables**.             |
| there are **nodes**                                  | there are **rows**                        |
| there are **properties** and their **values**.       | there are **columns** and **data**.       |
| the connected nodes are defined by **relationships** | **constraints** are used instead of that. |
| **traversal** is used instead of join.               | **join** is used instead of traversal.    |

- Vs `Relational databases`

  - `Relational databases` store highly structured data which have several records **storing the same type of data**
    - so they can be used to store structured data
    - they do not store the relationships between the data
  - `graph databases` store **relationships** and **connections** as first-class entities.

- **Join tables** => `relationships`
- **columns** => `relationship` **properties**

---

## GraphDB vs NoSQL Database

- `NoSQL databases`

  - store sets of **disconnected** aggregates, making it difficult to use them for connected data and graphs.
  - `Relational database`: It is represented in **tabular** form so it is best for calculating the income.
  - `Key-Value Store`: It is best for building a shopping cart.
  - `NoSQL databases`: It is stored as a **document** so, it is best for storing structured product information.
  - `GraphDB`: It follows a graph structure. It is best for describing how a user got **from point A to point B**.

- Types:
  - `Document Stores`
    - Binary Large Objects (BLOBs)
    - MongoDB
  - `Key-Value Stores`
    - no joins and aggregate functions
    - Amazon DynamoDB and Apache Cassandra
  - `Columnar Databases`
    - Every row can have its own schema
    - HBase
  - `Graph Databases`
    - vertices and edges.
    - Neo4j
