# AWS - Database

[Back](../index.md)

- [AWS - Database](#aws---database)
  - [Database](#database)
  - [Shared Responsibility on AWS Databases](#shared-responsibility-on-aws-databases)
  - [Databases \& Analytics Summary in AWS](#databases--analytics-summary-in-aws)

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

## Shared Responsibility on AWS Databases

- AWS offers use to manage different databases
- Benefits include:
  - Quick **Provisioning**, High Availability, Vertical and Horizontal Scaling
  - Automated **Backup** & Restore, Operations, Upgrades
  - Operating System **Patching** is handled by AWS
  - Monitoring, alerting
- Note: many databases technologies could be run on EC2, but you must
  handle yourself the **resiliency, backup, patching, high availability, fault tolerance, scaling**…

---

## Databases & Analytics Summary in AWS

- **Relational Databases - OLTP**:
  - `RDS` & `Aurora` (SQL)
  - Differences between Multi-AZ, Read Replicas, Multi-Region
  - In-memory Database: `ElastiCache`
- **NoSQL Key/Value Database**:
  - `DynamoDB` (serverless) & `DAX` (cache for DynamoDB)
  - `DocumentDB`: “Aurora for MongoDB” (JSON – NoSQL database)
- **Warehouse - OLAP**:
  - `Redshift`(SQL)
- **Big Data**
  - Hadoop Cluster: `EMR`
- **Data Analytics**
  - `Athena`: query data on **Amazon S3** (**serverless & SQL**)
  - `QuickSight`: **dashboards** on your data (serverless)
- **Ledger**
  - `Amazon QLDB`: Financial Transactions Ledger (immutable journal, cryptographically verifiable)
- **Decentralization**
  - `Amazon Managed Blockchain`: managed **Hyperledger Fabric** & **Ethereum** blockchains
- **ETL Tools**
  - `Glue`: Managed ETL (Extract Transform Load) and Data Catalog service (serverless)
- **Database Migration**:
  - `DMS`
- **Graph database**
  - `Neptune`

---

[TOP](#aws---database)
