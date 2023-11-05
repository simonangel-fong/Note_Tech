# AWS - Amazon EMR

[Back](../index.md)

- [AWS - Amazon EMR](#aws---amazon-emr)
  - [Amazon EMR](#amazon-emr)
    - [Node types \& purchasing](#node-types--purchasing)

---

## Amazon EMR

- `EMR` stands for “`Elastic MapReduce`”

  - helps creating `Hadoop clusters (Big Data)` to **analyze** and **process** vast amount of data
  - EMR comes bundled with `Apache Spark`, `HBase`, `Presto`, `Flink…`

- Feature

  - The **clusters** can be made of hundreds of `EC2 instances`
  - EMR **takes care of all** the provisioning and configuration
  - Auto-scaling and integrated with `Spot instances`

- **Use cases**:
  - data **processing**,
  - **machine learning**,
  - web **indexing**,
  - **big data**…

---

### Node types & purchasing

- Node Types:

  - `Master Node`:

    - **Manage** the cluster, coordinate, manage health – must be long running

  - `Core Node`:

    - **Run** tasks and **store** data – must be long running

  - `Task Node (optional)`:
    - Just to **run** tasks – usually Spot instance

- **Purchasing options**: Instance Types

  - **On-demand**:
    - reliable, predictable, won’t be **terminated**
  - **Reserved (min 1 year)**:
    - cost **savings** (EMR will automatically use if available)
    - best for Master node and Core node.
  - **Spot Instances**:
    - cheaper, can be **terminated**, **less reliable**
    - best for Task node

- Types of cluster for deployment:
  - Can have **long-running** cluster, or **transient (temporary**) cluster

---

[TOP](#aws---amazon-emr)
