# System Design - KV store

[Back](../system_design.md)

- [System Design - KV store](#system-design---kv-store)
  - [KV store](#kv-store)
  - [Understand the problem and establish design scope](#understand-the-problem-and-establish-design-scope)
    - [Single server key-value store](#single-server-key-value-store)

---

## KV store

asked to design a key-value store that supports the following
operations:

- put(key, value) // insert “value” associated with “key”
- get(key) // get “value” associated with “key”

---

## Understand the problem and establish design scope

- requirements
  - The size of a key-value pair is small: less than 10 KB.
  - Ability to store big data.
  - High availability: The system responds quickly, even during failures.
  - High scalability: The system can be scaled to support large data set.
  - Automatic scaling: The addition/deletion of servers should be automatic based on traffic.
  - Tunable consistency.
  - Low latency.

---

### Single server key-value store


