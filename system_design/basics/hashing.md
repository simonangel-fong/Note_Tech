# System Design - Consistent hashing

[Back](../system_design.md)

- [System Design - Consistent hashing](#system-design---consistent-hashing)
  - [Consistent Hashing](#consistent-hashing)

---

## Consistent Hashing

- `Distributed Hash Table (DHT)` is one of the fundamental components used in distributed scalable systems.
- Hash Tables need
  - a **key**,
  - a **value**,
  - and a **hash function** where hash function maps the key to a location where the value is stored.

  ```
  index = hash_function(key)
  ```

- rehashing problem
  - hashing: works well when the **size** of the server pool is **fixed**, and the data **distribution is even**.
  - redistributed if one server offline
    - causes a storm of cache misses: connect to the wrong servers to fetch data

---

- `Consistent hashing`
  - a very useful strategy for distributed caching system and DHTs.
  - allows to distribute data across a cluster in such a way that will **minimize reorganization** when nodes are added or removed.
- when the hash table is **resized** (e.g. a new cache host is added to the system), only `k/n` keys need to be remapped
  - where `k` is the total number of keys and `n` is the total number of servers.

- benefits
  - **Minimized keys are redistributed** when servers are added or removed.
  - It is **easy to scale horizontally** because data are more evenly distributed.
  - Mitigate **hotspot key problem**. Excessive access to a specific shard could cause server overload. Imagine data for Katy Perry, Justin Bieber, and Lady Gaga all end up on the same shard. Consistent hashing helps to mitigate the problem by distributing the data more evenly.
