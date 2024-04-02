# Neo4j

[Back](../index.md)

- [Neo4j](#neo4j)
  - [Neo4j](#neo4j-1)
  - [Features](#features)
  - [Use Cases](#use-cases)
  - [CQL](#cql)
  - [Paths](#paths)

---

## Neo4j

- `Neo4j`

  - a NoSQL database.
  - It is highly scalable and schema-free.

- `Neo4j` is implemented in `Java` language and it can be accessed by other language using `Cypher Query Language (CQL)` through a transactional `HTTP` endpoint.

- Native both:
  - **processing** engine
  - underlying **storage**

---

- `Neo4j`
  - stores and displays **data** in the form of **graph**.
    - **data** is represented by `nodes` and `relationships` between those nodes.
  - best for storing data that has **many interconnecting relationships**
  - Neo4j is a "schema-optional" DBMS.
    - In Neo4j, the data is the structure.
  - In Neo4j, **no** need to set up **primary key/foreign key** constraints to predetermine which fields can have a relationship, and to which data.
    - You just have to define the relationships between the nodes you need.

---

## Features

- **Flexible Schema**:

  - Neo4j follows a **data model** called `graph model`.
    - The graph contains `nodes` and the nodes are **connected** to each other.
    - `Nodes` and `relationships` store data in **key-value pairs** known as `properties`.

- **ACID Property**:

  - Neo4j supports full ACID properties (, Consistency, Isolation and Durability).
    - `Atomicity`
      - each statement in a transaction is treated as a single unit.
      - **Either the entire** statement is executed, **or none** of it is executed.
      - This property **prevents** data loss and corruption from occurring if, for example, if your streaming data source **fails mid-stream**.
    - `Consistency`
      - ensures that transactions only **make changes** to tables **in predefined, predictable ways**.
      - Transactional consistency ensures that corruption or errors in your data do not create unintended consequences for the integrity of your table.
    - `Isolation`
      - when **multiple users** are reading and writing from the same table all at once, isolation of their transactions ensures that the **concurrent transactions don't interfere with or affect one another**.
      - Each request can occur as though they were **occurring one by one**, even though they're actually occurring simultaneously.
    - `Durability`
      - ensures that **changes** to your data made by successfully executed transactions **will be saved**, even in the event of system failure.

- **Scalability**:

  - Neo4j facilitates you to scale the database by **increasing the number of reads/writes**, and the **volume** without affecting the data integrity and the speed of query processing.

- **Reliability**:

  - Neo4j provides replication for data safety and reliability.

- **Real-time** data analysis:

  - Neo4j provides results based on real-time data.

- **No Join**:

  - Neo4j doesn't require complex Joins to retrieve connected/related data as it is very easy to retrieve its adjacent node or relationship details without Joins or Indexes because it is a graph database and all nodes are already connected.

- **Cypher Query Language**:
  Neo4j provides a powerful declarative query language called `Cypher Query language`.
  It is used to create and retrieve relations between data **without using the complex queries like Joins**.

- **Built-in Web applications**:

  - Neo4j also provides a built-in Neo4j browser web application which can be used to create and retrieve your graph data.

- **GraphDB**:
  - Neo4j follows Property `Graph Data Model`.

---

- General Features:
  - It supports `UNIQUE` constraints.
  - It uses Native graph storage with `Native GPE(Graph Processing Engine)`.
  - It supports exporting of query data to `JSON` and `XLS` format.
  - It provides `REST API` to be accessed by any Programming Language like Java, Spring, Scala etc.
  - It provides `Java Script` to be accessed by any UI MVC Framework like Node JS.
  - It supports two kinds of Java API:
    - `Cypher API`
    - `Native Java API` to develop Java applications.

---

## Use Cases

- Real Time **Recommendations**
- Master Data Management
- Fraud Detection
- Graph Based Search
- Network & IT-Operations
- Identity & Access Management

---

## CQL

- `Cypher Query Language`:

  - a query language for Neo4j.

- Features

  - a query language for Neo4j Graph Database.
  - Is a **declarative pattern-matching** language.
  - The syntax of CQL is same like SQL syntax.
  - Syntax of CQL is very simple and in **human readable** format.

- vs SQL
  - both have simple **commands to do database operations**.
  - Both support clauses like `WHERE`,` ORDER BY`, etc., to simplify complex queries.
  - Both supports some Relationship Functions and functions such as String, Aggregation.

---

## Paths

- `path`
  - one or more nodes with **connecting relationships**, typically retrieved as a query or traversal result

---

[TOP](#neo4j)
