# system design interview

[Back](../README.md)

- [Interview](./interview/interview.md)
- [Example: scale from zero to millions of users](./scale/scale.md)
- [System Design Fundamental](./basics/basics.md)
  - [Load Balancing](./basics/lb.md)
  - [Caching](./basics/caching.md)
  - [Data Partitioning](./basics/partition.md)
  - [Indexes](./basics/indexes.md)
  - [Proxies](./basics/proxies.md)
  - [SQL vs. NoSQL](./basics/sql_nosql.md)
  - [Communication protocols](./basics/protocols.md)
  - [Consistent hashing](./basics/hashing.md)

---

- Features
  - [Design rate limiter](./rate_limiter/rate_limiter.md)
  - [Design key-value store](./kv/kv.md)
  - [Design a unique ID generator ](./uid/uid.md)

---

- Products
  - [Design url shortener](./url/url.md)
  - [Design Pastebin](./pastebin/pastebin.md)
  - [Design Cloud file storage](./drive/drive.md)
  - [Design Instagram](./instagram/instagram.md)
  - [Design chat system](./chat/chat.md)
  - [Design Twitter](./twitter/twitter.md)

---

- [Design a web crawler](./crawler/crawler.md)
- [Design a notification system](./notification/notification.md)
- [Design a news feed system](./feed/feed.md)
- [Design a search autocomplete](./autocomplete/autocomplete.md)
- [Design a youtube](./youtube/youtube.md)

---

## CAP Theorem

- `CAP (Consistency, Availability, Partition Tolerance) theorem`
  - it is **impossible** for a distributed system to simultaneously provide **more than two** of these three guarantees: `consistency`, `availability`, and `partition tolerance`.

- `Consistency`:
  - **all** clients see the **same data** at the **same time** no matter which node they connect to

- `Availability`:
  - **any** client which requests data **gets a response** even if some of the nodes are **down**.

- `Partition Tolerance`:
  - a `partition` indicates a communication break between two nodes.
  - the system **continues** to operate despite **network partitions**.

![cap](./img/cap.png)

---

## Quorum consensus

- `Quorum consensus`
  - a technique used in distributed systems to **maintain data consistency, availability, and fault tolerance** without requiring every single node to respond.
  - relies on a minimum number of participating nodes (a quorum) to agree on read and write operations.

- Definitions:
  - N = The number of **replicas**
  - W = A **write quorum** of size W.
    - For a **write operation** to be considered as successful, write operation must be acknowledged from W replicas.
  - R = A **read quorum** of size R.
    - For a **read operation** to be considered as successful, read operation must wait for responses from at least R replicas.

- **configuration of W, R and N is a typical tradeoff between latency and consistency.**
  - `W = 1` or `R = 1`,
    - an operation is **returned quickly** because a coordinator only needs to wait for a response from any of the replicas.
  - If `W` or `R > 1`,
    - the system offers better **consistency**; however, the query will be **slower** because the coordinator must wait for the response from the **slowest replica**.

  - If `W + R > N`,
    - **strong consistency** is guaranteed because there must be **at least one overlapping** node that has the latest data to ensure consistency.

- How to configure N, W, and R to fit our use cases? Here are some of the possible setups:
  - If `R = 1` and `W = N`, the system is optimized for a **fast read**.
  - If `W = 1` and `R = N`, the system is optimized for **fast write**.
  - If `W + R > N`, **strong consistency** is guaranteed (Usually N = 3, W = R = 2).
  - If `W + R <= N`, strong consistency is **not guaranteed**.

---

- example

![quorum_consensus_write](./img/quorum_consensus_write.png)

- A coordinator acts as a proxy between the client and the nodes.
- N = 3
  - data is replicated at s0, s1, and s2.
- W = 1
  - the coordinator must receive at least one acknowledgment before the write operation is considered as successful.
  - if we get an acknowledgment from s1, we no longer need to wait for acknowledgements from s0 and s2.

---

## Consistency models

- Consistency models
  - defines the degree of data consistency

- `Strong consistency`:
  - any **read operation** returns a value corresponding to the result of the **most updated write data item**.
  - A client never sees out-of-date data.
  - by forcing a replica **not to accept new** reads/writes **until** every replica has **agreed on current write**.
  - no highly available system
    - block new operations
- `Weak consistency`:
  - subsequent read operations may **not see the most updated value**.
- `Eventual consistency`:
  - this is a specific form of weak consistency.
  - Given enough **time**, all updates are propagated, and **all** replicas are **consistent**.
  - e.g., Dynamo and Cassandra
