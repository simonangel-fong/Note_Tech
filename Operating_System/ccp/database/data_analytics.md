# AWS - Data Analytics

[Back](../index.md)

- [AWS - Data Analytics](#aws---data-analytics)
  - [Data Warehouse](#data-warehouse)
    - [Redshift - analytics, data warehousing, BI](#redshift---analytics-data-warehousing-bi)
  - [Other Database](#other-database)
    - [Neptune - Graph, Latency](#neptune---graph-latency)
    - [Quantum Ledger Database (QLDB) - Financial regulation, Immutable, Centralization](#quantum-ledger-database-qldb---financial-regulation-immutable-centralization)
    - [Managed Blockchain - Decentralization](#managed-blockchain---decentralization)
  - [Data Analytics](#data-analytics)
    - [Elastic MapReduce (EMR) - Hadoop, Big Data](#elastic-mapreduce-emr---hadoop-big-data)
    - [Amazon Athena - S3, Serverless](#amazon-athena---s3-serverless)
    - [Amazon QuickSight - Serverless, BI](#amazon-quicksight---serverless-bi)
  - [Supportive Tools](#supportive-tools)
    - [AWS Glue - serverless, ETL](#aws-glue---serverless-etl)
    - [Glue Data Catalog](#glue-data-catalog)
    - [Database Migration Service (DMS)](#database-migration-service-dms)

---

## Data Warehouse

- `Data Warehouse`

  - A relational datastore designed for **analytic workload**s, which is generally **column**-oriented data-store.
  - Companies will have terabytes and millions of rows of data, and they need a fast way to be able to produce **analytics reports**.

- Data warehouses generally perform aggregation.

  - aggregation is grouping data. eg.total or average.
  - Data warehouses are optimized around columns since they need to quickly aggregate column data.

- Data warehouses are generally designed to be HOT

  - HOT means they can return **queries very fast** even though they have vast amounts of data.

- Data warehouse are infrequently accessed meaning they are **not intended for real-time** reporting but once or twice a day or once a week to generate business and user reports.

- Data warehouse needs to consume data from a relational database on a regular basis.

---

### Redshift - analytics, data warehousing, BI

- Redshift is based on **PostgreSQL**, but it’s **not** used for **OLTP**
- It’s **OLAP** – **online analytical processing** (**analytics** and **data** **warehousing**)
- Load data once every hour, not every second
- 10x better **performance** than other data warehouses, scale to PBs of data
- Columnar storage of data (**instead of row based**)
- **Massively Parallel Query Execution (MPP**), highly available
- Pay as you go based on the instances provisioned
- Has a **SQL** interface for performing the queries
- **BI** tools such as AWS Quicksight or Tableau integrate with it

---

## Other Database

### Neptune - Graph, Latency

- A popular **graph dataset** would be a social network

  - Users have friends
  - Posts have comments
  - Comments have likes from users
  - Users share and like posts…

- Highly available across **3 AZ**, with up to **15 read replicas**
- Build and run applications working with highly connected
  datasets–optimized for these complex and hard queries

- Can store up to billions of relations and query the graph with
  milliseconds **latency**

- Highly available with replications across multiple AZs
- Great for
  - knowledge graphs (Wikipedia),
  - fraud detection,
  - recommendation engines,
  - social networking

---

### Quantum Ledger Database (QLDB) - Financial regulation, Immutable, Centralization

- A `ledger` is a book **recording financial transactions**
- Fully Managed, Serverless, High available, Replication across **3 AZ**
- Used to review history of all the changes made to your application data over time
- **Immutable** system: **no entry can be removed or modified**, **cryptographically** verifiable
- 2-3x better **performance** than common ledger blockchain frameworks, manipulate data using SQL
- Difference with Amazon Managed Blockchain: **no decentralization** component, in accordance with **financial regulation** rules

---

### Managed Blockchain - Decentralization

- Blockchain makes it possible to build applications where **multiple parties** can execute transactions **without** the need for a trusted, **central** authority.
- Amazon Managed Blockchain is a managed service to:
  - Join public blockchain networks
  - Or create your own scalable private network
- Compatible with the frameworks **Hyperledger Fabric** & **Ethereum**

---

## Data Analytics

### Elastic MapReduce (EMR) - Hadoop, Big Data

- `Elastic MapReduce (EMR)`
  - EMR helps creating **Hadoop clusters (Big Data)** to analyze and process vast amount of data
- The clusters can be made of **hundreds of EC2 instances**
- Also supports **Apache Spark, HBase, Presto, Flink…**
- EMR takes care of all the provisioning and configuration
- Auto-scaling and integrated with Spot instances
- Use cases:
  - data processing,
  - machine learning,
  - web indexing,
  - big data…

---

### Amazon Athena - S3, Serverless

- **Serverless** query service to analyze data stored in Amazon S3
- Uses standard **SQL** language to query the files
- Supports CSV, JSON, ORC, Avro, and Parquet (built on Presto)
- Pricing: **$5.00 per TB **of data scanned
- Use compressed or **columnar** data for cost-savings (less scan)
- Use cases:
  - Business intelligence / analytics / reporting,
  - analyze & query VPC Flow Logs,
  - ELB Logs,
  - CloudTrail trails, etc...
- Exam Tip: analyze data in **S3** using **serverless SQL**, use Athena

---

### Amazon QuickSight - Serverless, BI

- Serverless machine learning-powered **business intelligence service** to create interactive dashboards
- Fast, automatically scalable, embeddable, with per-session pricing
- Use cases:
  - Business **analytics**
  - Building **visualizations**
  - Perform ad-hoc **analysis**
  - Get **business insights** using data
- Integrated with RDS, Aurora, Athena, Redshift, S3…

---

## Supportive Tools

### AWS Glue - serverless, ETL

- Managed **extract, transform, and load (ETL)** service
- Useful to **prepare and transform data for analytics**
- Fully **serverless** service

---

### Glue Data Catalog

- catalog of **datasets**
- can be used by Athena, Redshift, EMR

---

### Database Migration Service (DMS)

- Quickly and securely **migrate databases to AWS**, resilient, self healing
- The source database remains available during the migration
- Supports:
  - `Homogeneous migrations`: ex Oracle to Oracle
  - `Heterogeneous migrations`: ex Microsoft SQL Server to Aurora

---

[TOP](#aws---data-analytics)
