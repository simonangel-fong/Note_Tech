# System Design: Fundamental - Caching

[Back](../system_design.md)

- [System Design: Fundamental - Caching](#system-design-fundamental---caching)
  - [Caching](#caching)
    - [Application server cache](#application-server-cache)
    - [Content Distribution Network (CDN)](#content-distribution-network-cdn)
    - [Cache Invalidation](#cache-invalidation)
    - [Cache eviction policies](#cache-eviction-policies)

---

## Caching

- `locality of reference principle`
  - recently requested data is likely to be requested again.

- `cache`
  - like **short-term memory**
  - has a **limited** amount of space, but is typically **faster** than the original data source and contains the **most recently accessed items**.

---

### Application server cache

- Placing a cache directly on a request layer node
  - Each time a request is made to the service, the node will quickly **return local cached data if it exists**.
  - If it is **not** in the cache, the requesting node will **query the data from disk or memory**.

- if the load balancer **randomly distributes** requests across the nodes
  - global caches and distributed caches

---

### Content Distribution Network (CDN)

- a kind of **cache** serving large amounts of **static media**.

---

### Cache Invalidation

- inconsistency: fail to keep cache coherent with the source of truth (e.g., database).
- solved: cache invalidation

- three main schemes
  - `Write-through cache`
    - data is written into the `cache` and the scorresponding `database` **at the same time**.
    - benefits:
      - complete **data consistency** between the cache and the storage
      - **minimizes the risk of data loss** in case of a crash, power failure, or other system sdisruptions.
    - drawbacks:
      - **higher latency** for write operations.

  - `Write-around cache`:
    - data is written **directly to permanent storage**, **bypassing** the `cache`.
    - benefits:
      - reduce the cache being flooded with write operations
    - drawbacks:
      - create a “cache miss” and must be read from slower back-end storage
      - experience higher latency.
  - `Write-back cache`:
    - data is **written to cache alone** and completion is immediately confirmed to the client
    - benefits:
      - **low latency** and **high throughput** for write-intensive applications
    - drawbacks:
      - risk of data loss in case of a crash

---

### Cache eviction policies

- `First In First Out (FIFO)`:
  - The cache evicts the first block **accessed first** without any regard to how often or how many times it was accessed before.
- `Last In First Out (LIFO)`:
  - The cache evicts the block accessed **most recently first** without any regard to how often or how many times it was accessed before.
- `Least Recently Used (LRU)`: Discards the **least recently** used items first.
- `Most Recently Used (MRU)`: Discards, in contrast to LRU, the **most recently** used items first.
- `Least Frequently Used (LFU)`: Counts how often an item is needed. Those that are used least often are discarded first.
- `Random Replacement (RR)`: Randomly selects a candidate item and discards it to make space when necessary.

---
