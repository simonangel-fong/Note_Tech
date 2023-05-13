# AWS - RDS

[Back](../index.md)

- [AWS - RDS](#aws---rds)
  - [Relational Databases](#relational-databases)
  - [Relational Database Service (RDS)](#relational-database-service-rds)
    - [Aurora - Performance, PostgreSQL and MySQL, not free](#aurora---performance-postgresql-and-mysql-not-free)
    - [ElastiCache - In-memory](#elasticache---in-memory)
    - [RDS Deployments](#rds-deployments)
      - [Read Replicas](#read-replicas)
      - [Multi-AZ](#multi-az)
      - [Multi-Region (Read Replicas)](#multi-region-read-replicas)

---

## Relational Databases

- Looks just like Excel **spreadsheets**, with **links** between them!
- Can use the **SQL** language to perform queries / lookups

---

## Relational Database Service (RDS)

- `Relational Database Service (RDS)`

  - a relational database service that supports multiple SQL engines. Relational is synonymous with `SQL` and `Online Transactional Processing (OLTP)`.

  - Supported SQL Engine

- It allows you to create databases in the cloud that are managed by AWS

  - Postgres
  - MySQL
  - MariaDB
  - Oracle
  - Microsoft SQL Server
  - **Aurora (AWS Proprietary database)**

- Advantage over using RDS versus deploying DB on EC2

  - RDS is a managed service:
    - Automated **provisioning**, OS **patching**
    - Continuous **backups** and **restore** to specific timestamp (Point in Time Restore)!
    - **Monitoring** dashboards
    - Read replicas for improved read **performance**
    - **Multi AZ** setup for DR (Disaster Recovery)
    - Maintenance windows for **upgrades**
    - **Scaling** capability (vertical and horizontal)
    - **Storage** backed by EBS (gp2 or io1)
  - BUT you **can’t SSH** into your instances

- `RDS on VMware`
  - allow to deploy RDS supported engines to an on-premise data-center.
  - For users who want databases managed by RDS on **user's own datacenter**.

---

### Aurora - Performance, PostgreSQL and MySQL, not free

- `Aurora`

  - an “AWS-**implementation” of PostgreSQL / MySQL**
  - PostgreSQL and MySQL are both supported as Aurora DB
  - For users who want a relational database for Postgres or MySQL.

- Aurora is “AWS cloud optimized” and claims 5x **performance** improvement over MySQL on RDS, over 3x the performance of Postgres on RDS
- Aurora storage automatically grows in increments of 10GB, up to 128 TB
- Aurora **costs more** than RDS (20% more) – but is more efficient
- **Not in the free tier**

- `Aurora Severless`

  - the serverless on-demand version of Aurora.
  - For users who want most of the benefits of Aurora but can trade to have cold-starts or don't have lots of traffic demand.

---

### ElastiCache - In-memory

- The same way RDS is to get managed **Relational Databases**…
- ElastiCache is to get managed Redis or Memcached
- Caches are **in-memory** databases with high **performance**, low latency
- Helps reduce load off databases **for read intensive workloads**
- AWS takes care of OS maintenance / patching, optimizations, setup, configuration, monitoring, failure recovery and backups

---

### RDS Deployments

#### Read Replicas

- Scale the **read** workload of your DB
- Can create up to **15** Read Replicas
- Data is **only written to the main** DB
- main purpose is **scalability**

#### Multi-AZ

- Failover in case of AZ **outage** (high availability)
- Data is **only read/written to the main** database
- Can **only have 1 other AZ** as failover
- main purpose is high **availability**

#### Multi-Region (Read Replicas)

- Disaster recovery in case of **region issue**
- Local performance for **global reads**
- Replication **cost**
- main purpose is **disaster recovery** and **local performance**.

---

[TOP](#aws---rds)
