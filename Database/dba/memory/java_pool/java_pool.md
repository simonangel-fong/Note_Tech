# DBA - SGA: Java Pool

[Back](../../index.md)

- [DBA - SGA: Java Pool](#dba---sga-java-pool)
  - [Java Pool](#java-pool)

---

## Java Pool

- `Java pool`

  - an area of memory that **stores** all session-specific **Java code** and **data** within the `Java Virtual Machine (JVM)`.
  - includes Java objects that are migrated to the Java session space at end-of-call.

- For **dedicated** server connections,
  - the Java pool includes the **shared part** of each Java class, including methods and read-only memory such as code vectors, but not the per-session Java state of each session.
- For **shared** server,
  - the pool includes the **shared part** of each class and some `UGA` used for the state of each session. Each UGA grows and shrinks as necessary, but the total UGA size must fit in the Java pool space.

---

[TOP](#dba---sga-java-pool)
