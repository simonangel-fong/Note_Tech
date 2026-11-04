# System Design: Fundamental - Data Partitioning

[Back](../system_design.md)

- [System Design: Fundamental - Data Partitioning](#system-design-fundamental---data-partitioning)
  - [Sharding or Data Partitioning](#sharding-or-data-partitioning)
    - [Partitioning Methods](#partitioning-methods)
    - [Partitioning Criteria](#partitioning-criteria)
    - [Common Problems of Sharding](#common-problems-of-sharding)

---

## Sharding or Data Partitioning

- `Data partitioning` / `sharding`
  - a technique to **break up** a big database (DB) **into many smaller parts**
  - the process of **splitting up a DB/table** across **multiple machines** to improve the manageability, performance, availability, and load balancing of an application.
    - make it **cheaper and more feasible** to scale horizontally by adding more machines

### Partitioning Methods

- 3 most popular schemes used to break up an application database

- **Horizontal partitioning**
  - put **different rows** into different tables.
    - e.g., break ZIP code into > 100000 and < 10000
  - drawback:
    - could lead to **unbalanced servers** as assuming that data is **evenly distributed**
    - e.g., down town vs suburb

- **Vertical Partitioning**
  - divide data to store **tables** related to a **specific feature** in their own server.
    - e.g., break data based on users, photos, people they follow, etc
  - drawback:
    - may be necessary to further partition a feature specific DB
    - e.g., need further patirtion photo db

- **Directory Based Partitioning**
  - create a **lookup service** which knows the current partitioning scheme and abstracts it away from the DB access code.

---

### Partitioning Criteria

- **Key or Hash-based partitioning**
  - apply a hash function to some key attributes of the entity
    - e.g., have 100 DB servers; hash ID/100
  - drawback:
    - **adding** new servers means changing the hash function which would require **redistribution** of data

- **List partitioning**
  - each partition is assigned a list of values
    - when insert a new record, the partition value also get insert
    - e.g., user data for Nordic countries; list: Iceland, Norway, Sweden, Finland, etc

- **Round-robin partitioning:**
  - a simple strategy that ensures **uniform data** distribution.
    - With `n` partitions, the `i` tuple is assigned to partition (i mod n).

- **Composite partitioning**:
  - **combine** any of the above partitioning schemes to devise a new scheme.
  - e.g., first applying a **list partitioning** scheme and then a **hash based partitioning**.
  - Consistent hashing could be considered a **composite of hash and list partitioning** where the hash reduces the key space to a size that can be listed.

---

### Common Problems of Sharding

- **Joins and Denormalization**
  - joins will **not be performance efficient**
    - data has to be **compiled from multiple servers**
  - workaround
    - denormalize the database
      - but risk of data inconsistency

- **Referential integrity**
  - data integrity constraints, e.g., foreign keys
  - workaround
    - enforce referential integrity in application code
    - regular SQL jobs to clean up dangling references.

- **Rebalancing**
  - change sharding scheme
    - e.g., data distribution is not uniform; ZIP code at downtown vs suburb
  - a lot of load on a shard
    - e.g., many requests for user photos

---
