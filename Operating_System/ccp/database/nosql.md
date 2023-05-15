# AWS - NoSQL

[Back](../index.md)

- [AWS - NoSQL](#aws---nosql)
  - [NoSQL Databases](#nosql-databases)
    - [A Key/Value Store](#a-keyvalue-store)
    - [Document Store](#document-store)
  - [NoSQL Database Services](#nosql-database-services)
    - [`DynamoDB` - Serverless, Low latency retrieval](#dynamodb---serverless-low-latency-retrieval)
      - [Global Tables - a low latency feature](#global-tables---a-low-latency-feature)
    - [`DynamoDB Accelerator(DAX)` - In-memory Cache](#dynamodb-acceleratordax---in-memory-cache)
    - [`DocumentDB` - MongoDB](#documentdb---mongodb)
  - [Others NoSQL](#others-nosql)
    - [`Amoazon Keyspaces` - Cassandra](#amoazon-keyspaces---cassandra)

---

## NoSQL Databases

- NoSQL = non-SQL = **non relational** databases
- NoSQL databases are purpose built for specific data models and have flexible schemas for building modern applications.
- **Benefits**:
  - Flexibility: easy to evolve data model
  - Scalability: designed to **scale-out** by using distributed clusters
  - High-performance: optimized for a specific data model
  - Highly functional: types optimized for the data model
- Examples: Key-value, document, graph, in-memory, search databases

- NoSQL data example: JSON
  - JSON = JavaScript Object Notation
  - **JSON is a common form** of data that fits into a NoSQL model
  - Data can be **nested**
  - **Fields can change** over time
  - Support for new types: arrays, etc…

---

### A Key/Value Store

- A key-value database is a type of non-relational databse (NoSQL) that uses a simple key-value method to store data.

  - Key values stores are dumb and fast.
  - generally lack feactures like:
    - relationships
    - indexes
    - Aggregation

![key-value](./pic/database_key_value.png)

---

### Document Store

- `Document Store`
  - a NOSQL database that stores documents as its primary data structure.
  - A document could be an XML but commonly is JSON or JSON-Like
  - Document stores are sub-class of Key/Value stores.

![document store](./pic/database_document_store.png)

---

## NoSQL Database Services

### `DynamoDB` - Serverless, Low latency retrieval

- `DynamoDB`

  - **NoSQL** database - not a relational database
  - DynamoDB is a **key/value** database
  - Single-digit millisecond latency – **low latency retrieval**
  - Scales to massive workloads, distributed **“serverless”** database

- Fully Managed Highly available with replication **across 3 AZ**
- Millions of requests per seconds, trillions of row, 100s of TB of storage
- **Fast** and consistent in performance
- Integrated with **IAM** for security, authorization and administration
- Low cost and auto **scaling** capabilities
- **Standard** & **Infrequent Access (IA)** Table Class
- Can Create table without a database

#### Global Tables - a low latency feature

- Make a DynamoDB table accessible with low latency in multiple-regions
- Active-Active replication (read/write to any AWS Region)

---

### `DynamoDB Accelerator(DAX)` - In-memory Cache

- Fully Managed **in-memory cache** for DynamoDB
- 10x **performance** improvement – single- digit millisecond latency to microseconds latency – when accessing your DynamoDB tables
- Secure, highly scalable & highly available
- **Difference with ElastiCache** at the CCP level:
  - **DAX** is only used for and is **integrated with DynamoDB**,
  - while **ElastiCache** can be used for **other databases**

---

### `DocumentDB` - MongoDB

- Aurora is an “AWS-implementation” of PostgreSQL / MySQL …
- DocumentDB is the same for **MongoDB (which is a NoSQL database)**
- MongoDB is **used to store, query, and index JSON data**
- Similar “deployment concepts” as Aurora
- Fully Managed, highly available with **replication across 3 AZ**
- DocumentDB storage **automatically grows** in increments of 10GB, up to 64 TB.
- Automatically scales to workloads with millions of requests per seconds

---

## Others NoSQL

### `Amoazon Keyspaces` - Cassandra

- `Cassandra`

  - an open-souce NoSQL key/value database.

- `Amoazon Keyspaces`

  - a fully managed Apache `Cassardra` database.
  - For users who want to use `Apache Cassandra`

---

[TOP](#aws---nosql)
