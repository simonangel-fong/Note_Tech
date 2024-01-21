# DBA - Memory: SGA

[Back](../../index.md)

- [DBA - Memory: SGA](#dba---memory-sga)
  - [Database Buffer Cache](#database-buffer-cache)
    - [Buffer Writes](#buffer-writes)

---

## Database Buffer Cache

- `database buffer cache` / `buffer cache`

  - the memory area that **stores copies of data blocks** read from data files.

- `buffer`

  - a **main memory address** in which the buffer manager **temporarily caches a currently or recently used data block**.
  - All users **share access** to the buffer cache.

- Purpose
  - **Optimize** physical **I/O**
    - update data block -> store in `redo log buffer` -> write to `online redo log` -> `DBW` lazy write to data file. 不是马上写入,而是先缓存, 再由 DBW 写入.
    - 常考: when a transaction committed, the data will not be writen directly to the data file.
      - Transaction happens in the memory, the buffer cache.
  - ## **Keep frequently** accessed blocks in the buffer cache and **write infrequently** accessed blocks to disk

---

### Buffer Writes

- `database writer (DBW) process` **periodically** writes cold, dirty buffers to disk.

- DBW writes buffers to disk when:
  - Dirty buffer threshold, cannot find clean buffers for reading new blocks into the database buffer cache.
  - free buffer for some operations is needed
  - shutdown (normal, transactional, immediate)
    - if shutdown abort, the dirty buffer will not be writen to data files.
  - change the status for tbsp (e.g., read-onlye)
  - during a checkpoint.

---

[TOP](#dba---memory-sga)
