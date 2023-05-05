# AWS - Database

[Back](../index.md)

- [AWS - Database](#aws---database)
  - [Database](#database)
  - [Data Warehouse](#data-warehouse)
  - [A Key/Value Store](#a-keyvalue-store)
  - [Document Store](#document-store)

---

## Database

- `Database`

  - a data-store that stores semi-structed and structured data.
  - is more complex data stotes because it requires using formal design and modeling techniques.

- Categorized as either:

  - `Relational databases`

    - structured data that strongly represents tabular data (table, rows and columns).
    - Row-oriented or Columnar-oriented

  - Non-relational databases
    - Semi-structured that may or may not distantly resemble tabular data.

- Databases have a rich set of functionality:
  - specialized language to query (retrieve data)
  - specialized modeling strategies to optimize retrieval for difference use cases.
  - more fine tune control over the transformation of the data into useful data structures or reports.

---

## Data Warehouse

- `Data Warehouse`

  - A relational datastore designed for analytic workloads, which is generally column-oriented data-store.
  - Companies will have terabytes and millions of rows of data, and they need a fast way to be able to produce analytics reports.

- Data warehouses generally perform aggregation.

  - aggregation is grouping data. eg.total or average.
  - Data warehouses are optimized around columns since they need to quickly aggregate column data.

- Data warehouses are generally designed to be HOT

  - HOT means they can return queries very fast even though they have vast amounts of data.

- Data warehouse are infrequently accessed meaning they are not intended for real=time reporting but once or twice a day or once a week to generate business and user reports.

- Data warehouse needs to consume data from a relational database on a regular basis.

---

## A Key/Value Store

- A key-value database is a type of non-relational databse (NoSQL) that uses a simple key-value method to store data.

  - Key values stores are dumb and fast.
  - generally lack feactures like:
    - relationships
    - indexes
    - Aggregation

![key-value](./pic/database_key_value.png)

---

## Document Store

- `Document Store`
  - a NOSQL database that stores documents as its primary data structure.
  - A document could be an XML but commonly is JSON or JSON-Like
  - Document stores are sub-class of Key/Value stores.

![document store](./pic/database_document_store.png)

---

[TOP](#aws---database)
