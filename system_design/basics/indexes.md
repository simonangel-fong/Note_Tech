# System Design: Fundamental - Indexes

[Back](../system_design.md)

- [System Design: Fundamental - Indexes](#system-design-fundamental---indexes)
  - [Indexes](#indexes)

---

## Indexes

- `database indexing`
  - a data structure technique used to **speed up data retrieval operations** by **creating shortcuts** that let the database jump directly to requested records instead of scanning an entire table.

- Indexes impact on write performance
  - when adding rows or making updates to existing rows, **decrease the write performance**
    - not only have to **write the data**
    - but also have to **update the index**.
  - best practice:
    - **avoid** adding unnecessary indexes
    - indexes that are no longer used should be **removed**.

---
