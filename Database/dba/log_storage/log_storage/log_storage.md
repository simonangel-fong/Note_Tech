# DBA - Logical Storage Structures

[Back](../../index.md)

- [DBA - Logical Storage Structures](#dba---logical-storage-structures)
  - [Logical Storage Structures](#logical-storage-structures)

---

## Logical Storage Structures

- Oracle Database **allocates** `logical space` for all data in the database.

- The **logical units** of database space allocation:

  - data blocks,
  - extents,
  - segments,
  - and tablespaces.

- At a **physical** level, the data is stored in `data files` on disk.
  - The data in the `data files` is stored **in operating system blocks**.

![logical_physical_diagram](./pic/logical_physical_diagram.png)

---

