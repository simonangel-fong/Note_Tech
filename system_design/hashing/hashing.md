# System Design - Consistent hashing

[Back](../system_design.md)

- [System Design - Consistent hashing](#system-design---consistent-hashing)
  - [Consistent hashing](#consistent-hashing)

---

## Consistent hashing

- rehashing problem
  - hashing: works well when the **size** of the server pool is **fixed**, and the data **distribution is even**.
  - redistributed if one server offline
    - causes a storm of cache misses: connect to the wrong servers to fetch data
- Consistent hashing
  - when a hash table is re-sized, only k/n keys need to be remapped on average

- benefits
  - **Minimized keys are redistributed** when servers are added or removed.
  - It is **easy to scale horizontally** because data are more evenly distributed.
  - Mitigate **hotspot key problem**. Excessive access to a specific shard could cause server overload. Imagine data for Katy Perry, Justin Bieber, and Lady Gaga all end up on the same shard. Consistent hashing helps to mitigate the problem by distributing the data more evenly.
