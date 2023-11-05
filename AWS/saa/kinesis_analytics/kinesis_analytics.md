# AWS - Kinesis Data Analytics

[Back](../index.md)

- [AWS - Kinesis Data Analytics](#aws---kinesis-data-analytics)
  - [Kinesis Data Analytics - Real-time Analytics](#kinesis-data-analytics---real-time-analytics)
    - [SQL application](#sql-application)
    - [`Amazon Managed Service` for Apache Flink](#amazon-managed-service-for-apache-flink)

---

## Kinesis Data Analytics - Real-time Analytics

- has 2 flavors
  - SQL application
  - `Amazon Managed Service` for Apache Flink

---

### SQL application

- `Kinesis Data Analytics(SQL application)`

  - **Real-time analytics** on `Kinesis Data Streams & Firehose` using `SQL`

- Features:

  - Add **reference data** from Amazon S3 to enrich streaming data
  - Fully managed, **no servers** to provision
  - Automatic **scaling**
  - Pay for **actual consumption rate**

- **Output**:

  - `Kinesis Data Streams`:
    - **create streams** out of the real-time **analytics queries**
  - `Kinesis Data Firehose`:
    - **send** analytics query results to **destinations**

- **Use cases**:
  - **Time-series** analytics
  - Real-time **dashboards**
  - Real-time **metrics**

![kinesis_data_analytics_sql_diagram](./pic/kinesis_data_analytics_sql_diagram.png)

---

### `Amazon Managed Service` for Apache Flink

- Usage:

  - Use `Flink` (Java, Scala or SQL) to process and **analyze streaming data**

- Run any `Apache Flink` application on a managed cluster on AWS

  - **provisioning** compute resources, **parallel computation**, automatic **scaling**
  - application **backups** (implemented as checkpoints and snapshots)
  - Use any `Apache Flink` **programming** features

- `Flink` does **not read** from `Firehose`
  - if need `Firehose`, use Kinesis Analytics for `SQL` instead

![kinesis_data_analytics_flink_diagram.png](./pic/kinesis_data_analytics_flink_diagram.png)

---

[TOP](#aws---kinesis-data-analytics)
