# System Design: Fundamental - SQL vs. NoSQL

[Back](../system_design.md)

- [System Design: Fundamental - SQL vs. NoSQL](#system-design-fundamental---sql-vs-nosql)
  - [SQL vs. NoSQL](#sql-vs-nosql)
    - [High level differences between SQL and NoSQL](#high-level-differences-between-sql-and-nosql)
    - [SQL VS. NoSQL - Which one to use?](#sql-vs-nosql---which-one-to-use)
  - [Redundancy and Replication](#redundancy-and-replication)

---

## SQL vs. NoSQL

- `Relational databases`
  - **structured** and have **predefined schemas**
  - store data in rows and columns
    - Each **row** contains all the **information about one entity**
    - each **column** contains all the separate **data points**.

- `Non-relational databases`
  - **unstructured**, **distributed**, and have a **dynamic schema**
  - **Key-Value Stores**
    - stored in an array of key-value pairs
    - e.g., Redis, Voldemort, and Dynamo.
  - **Document Databases**
    - stored in documents
    - documents are **grouped together in collections**.
    - Each document can have an **entirely different structure**.
    - e.g., CouchDB, MongoDB

  - **Wide-Column Databases**
    - in columnar databases we have **column families**, which are containers for rows.
    - e.g., Cassandra and HBase

  - **Graph Databases**
    - store data whose relations are best represented in a graph.
    - structures with nodes (entities), properties, and edges(lines)
    - e.g, Neo4J, InfiniteGraph

---

### High level differences between SQL and NoSQL

- **Storage**:
  - `SQL` stores data in **tables**;
  - `NoSQL` stores in key-value, document, graph, and columnar

- **Schema**
  - `SQL`: each record conforms to a **fixed** schema
  - `NoSQL`: schemas are **dynamic**.

- **Querying**:
  - `SQL databases` use `SQL`
  - `NoSQL` use `UnQL`

- **Scalability**
  - `SQL`:
    - **vertically scalable**
    - possible to scale a relational database **across multiple servers**
  - `NoSQL`: **horizontally** scalable

- **Reliability or `ACID` Compliancy (`Atomicity, Consistency, Isolation, Durability`)**:
  - `SQL`: ACID compliant
    - **Atomicity**: "all-or-nothing" operation.
    - **Consistency**: a transaction can only bring the database from one valid state to another
    - **Isolation**: concurrent transactions **run independently** without interfering with each other
    - **Durability**: once a transaction is committed, its changes are permanently saved
  - `NoSQL`: sacrifice ACID compliance for performance and scalability

---

### SQL VS. NoSQL - Which one to use?

- **Reasons to use SQL database**
  - when eed to ensure ACID compliance.
  - data is structured and unchanging.
- **Reasons to use NoSQL database**
  - Storing large volumes of data that often have **little to no structure**.
  - Making the most of **cloud computing and storage**.
  - Rapid development.

---

## Redundancy and Replication

- `Redundancy`
  - the **duplication of critical components** or functions of a system with the intention of **increasing the reliability** of the system
    - usually in the form of a **backup** or **fail-safe**, or to improve actual system performance.
  - benefits:
    - **removing** the `single points of failure`
    - **provides backups** if needed in a crisis.

- `Replication`
  - **sharing** information to **ensure consistency** between **redundant resources**, such as software or hardware components, to improve **reliability, faulttolerance, or accessibility**.
  - e.g., **Master-Replica Architecture** in database

---
