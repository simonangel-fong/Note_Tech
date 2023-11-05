# AWS - Amazon Athena

[Back](../index.md)

- [AWS - Amazon Athena](#aws---amazon-athena)
  - [Amazon Athena](#amazon-athena)
    - [Performance Improvement](#performance-improvement)
    - [Federated Query](#federated-query)
  - [Hands-on](#hands-on)

---

## Amazon Athena

- `Amazon Athena`

  - Serverless **query service to analyze data** stored in Amazon `S3`

- Uses standard `SQL` language to query the files (built on `Presto`)
- Supports `CSV`, `JSON`, `ORC`, `Avro`, and `Parquet`
- Pricing: **$5.00 per TB** of data scanned
- Commonly used with `Amazon Quicksight` for reporting/dashboards

- **Use cases**:

  - Business intelligence
  - analytics
  - reporting
  - analyze & query VPC Flow **Logs**,
  - ELB **Logs**,
  - CloudTrail **trails**, etc...

- Exam Tip: analyze data in `S3` using serverless `SQL`, use `Athena`

![athena_s3_quicksight_diagram](./pic/athena_s3_quicksight_diagram.png)

---

### Performance Improvement

- Use **columnar data** for cost-savings (**less scan**)

  - `Apache Parquet` or `ORC` is recommended
  - Huge performance improvement
  - Use `Glue` to **convert** your data to `Parquet` or `ORC`

- **Compress data** for smaller retrievals (bzip2, gzip, lz4, snappy, zlip, zstd…)
- **Partition datasets** in S3 for easy querying on virtual columns

```txt
s3://yourBucket/pathToTable
/<PARTITION_COLUMN_NAME>=<VALUE>
/<PARTITION_COLUMN_NAME>=<VALUE>
/<PARTITION_COLUMN_NAME>=<VALUE>
/etc…
```

- Example: `s3://athena-examples/flight/parquet/year=1991/month=1/day=1/`
- Use **larger files (> 128 MB)** to minimize overhead

---

### Federated Query

- `Federated Query`
  - Allows you to **run SQL queries across data** stored in relational, non-relational, object, and custom **data sources** (**AWS** or **on-premises**)
- Uses `Data Source Connectors` that run on `AWS Lambda` to run `Federated Queries` (e.g., CloudWatch Logs, DynamoDB, RDS, …)
- **Store** the results back in Amazon `S3`

![athena_federated_query_diagram](./pic/athena_federated_query_diagram.png)

---

## Hands-on

- Create s3 bucket for athena result

![athena_handson01](./pic/athena_handson01.png)

- Set result location

![athena_handson02](./pic/athena_handson02.png)

- Create DB

![athena_handson02](./pic/athena_handson03.png)

- Create table

![athena_handson02](./pic/athena_handson04.png)

- Query

![athena_handson02](./pic/athena_handson05.png)

---

[Top](#aws---amazon-athena)
