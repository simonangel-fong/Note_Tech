# System Design - URL shortening service

[Back](../system_design.md)

- [System Design - URL shortening service](#system-design---url-shortening-service)
  - [Pastebin](#pastebin)
  - [Steps](#steps)
    - [Step 1 - Requirements](#step-1---requirements)
      - [Estimation](#estimation)
    - [Step 2 - API](#step-2---api)
    - [Step 3 - Data Model](#step-3---data-model)
    - [Step 4 - High level](#step-4---high-level)
    - [Step 5 - Detailed design](#step-5---detailed-design)
      - [Performance](#performance)
      - [Reliability and availability](#reliability-and-availability)
      - [Security](#security)
      - [Specific issues](#specific-issues)
      - [Flowchart](#flowchart)
    - [Step 6 - Wrap up](#step-6---wrap-up)

---

## Pastebin

- `Pastebin`
  - services enable users to store **plain text or images** over the network (typically the Internet) and generate **unique URLs** to access the uploaded data.
  - users would just need to **pass the URL** to let other users see it.

## Steps

### Step 1 - Requirements

- **Functional Requirements:**
  1. Users should be able to **upload or “paste” their data** and get a **unique URL** to access it.
  2. Users will only be able to **upload text**.
  3. Data and links will **expire** after a specific timespan automatically; users should also be able to **specify expiration time**.
  4. Users should optionally be able to pick a custom **alias** for their paste.

- **Non-Functional Requirements:**
  1. The system should be highly **reliable**, any data uploaded should not be lost.
  2. The system should be highly **available**. This is required because if our service is down, users will not be able to access their Pastes.
  3. Users should be able to access their Pastes in real-time with **minimum latency**.
  4. Paste links should not be **guessable** (not predictable).

- **Extended Requirements:**
  1. **Analytics**, e.g., how many times a paste was accessed?
  2. Our service should also be accessible through **REST APIs** by other services.

- Constrain
  - the amount of text user can paste at a time: < 10MB
  - limits on custom URLs: impose a size limit on custom URLs

---

#### Estimation

- **Assumption**
  - read/write: 5:1
  - read per day: 5M
  - average paste size: 10KB
- **Traffic estimates**
  - write: 1M / (24 hours \* 3600 seconds) ~= 12 pastes/sec
  - read: 5M / (24 hours \* 3600 seconds) ~= 58 reads/sec
- **uuid / unique url**
  - 5 year: 1M \* 365 days \* 5 years ~= 1.8 B
  - uuid/url length = 6: (26+26+10) ^ 6 ~= 56B > 1.8B
- **Storage estimates**
  - pasted data per day: 1M \* 10KB => 10 GB/day
  - pasted data 5 year: 10 GB/day \* 365 days \* 5 years => 18TB
  - uuid/url 5 year: 1 byte \* 1.8 B ~= 11GB
- **Bandwidth estimates**
  - write: 12 pastes/sec \* average 10KB = 120 KB/s
  - read: 58 reads/sec \* average 10KB = 580 KB/s
- **Memory estimates**
  - cache these 20% pastes: 0.2 \* 5M \* 10KB ~= 10 GB

---

### Step 2 - API

- Feature: Create paste
  - `POST /api/v1/paste`
  - header: `api-token`
  - param (body):
    - `paste_data` (plain text, under 10 MB)
    - `custom_alias` (optional label appended to the generated public ID)
    - `expires_at` (optional, defaults to the standard expiration)
  - return:
    - `201 Created` with `paste_url` (e.g., `https://paste.example/aB3x7Q/hello`)
    - `413 Content Too Large` if the paste reaches or exceeds the size limit

---

- Feature: Read paste
  - `GET /{paste_code}` or `GET /{paste_code}/{custom_alias}`
  - header: none required for shared links
  - param (path):
    - `paste_code` (generated public ID)
    - `custom_alias` (included if set on the paste)
  - return:
    - `200 OK` with the paste content as `text/plain`
    - `404 Not Found` if the paste is unknown or expired, or the URL alias differs from the saved value

---

### Step 3 - Data Model

**Paste**

| Field          | Data type | Description                                                 |
| -------------- | --------- | ----------------------------------------------------------- |
| `paste_code`   | VARCHAR   | Generated, immutable public ID (case-sensitive primary key) |
| `custom_alias` | VARCHAR   | Optional URL label, reusable across pastes                  |
| `object_key`   | VARCHAR   | Key of the text object in object storage                    |
| `user_id`      | BIGINT    | Creator ID (foreign key to `User.user_id`)                  |
| `expires_at`   | TIMESTAMP | Time when the paste expires                                 |

**User**

| Field     | Data type | Description        |
| --------- | --------- | ------------------ |
| `user_id` | BIGINT    | Primary key        |
| `email`   | VARCHAR   | User email address |

- **SQL for metadata**
  - Look up paste metadata by `paste_code`.
  - Enforce the paste creator relationship with the `user_id` foreign key.
- **Object storage for paste text**
  - ~18 TB of raw text over five years. Store the text as objects so content storage can grow independently of SQL.

---

### Step 4 - High level

client -> app server -> storage

- **SQL** stores paste metadata and user records.
- **Object storage** stores the paste text.

---

### Step 5 - Detailed design

#### Performance

- Issue: repeated reads of popular pastes
  - Solution: **Cache-aside (if needed)**
    - Cache hot paste text, alias, and expiry together by `paste_code` if repeated reads become a bottleneck.
    - Cap cache TTL at `expires_at`.
    - Default cache 24 hr

---

#### Reliability and availability

- Issue: app server failure
  - Solution: **Load balancing**
    - Route requests to healthy app servers across availability zones.
- Issue: SQL failure
  - Solution: **Primary–standby failover**
    - Replicate metadata across availability zones and promote the standby if the primary fails.
- Issue: growth of SQL metadata
  - Solution: **Partitioning (if needed)**
    - Partition the Paste table by `paste_code` when metadata volume warrants it.

---

#### Security

- Issue: unauthorized creation or direct access to stored text
  - Solution: **API token and private object storage**
    - Require `api-token` to create a paste. The app serves anonymous reads through the share URL and accesses the private bucket.
- Issue: abusive traffic
  - Solution: **Rate limiting**
    - Limit paste creation and repeated requests for invalid codes.

---

#### Specific issues

- Issue: paste-code **collisions** and guessing
  - Solution: **Key generation service (KGS)**
    - Generate secure random `paste_code` values. Choose the length based on guessing risk and the number of active pastes.
    - Enforce uniqueness with the SQL primary key. Retry collisions with a new code. Keep a standby KGS for failover.
- Issue: create succeeds in one store(DB) and fails in the other(storage)
  - Solution: **Publish after both writes**
    - Upload text under a unique `object_key`, then insert SQL metadata. Return `201` after both writes succeed.
    - Reuse the uploaded object on a code collision. Clean up objects from failed creates after confirming no metadata references them.
- Issue: expired pastes
  - Solution: **Expiration checks and scheduled cleanup**
    - Check `expires_at` before serving text. Delete expired objects, then remove their metadata.

---

#### Flowchart

- Create paste

```text
Client -> LB -> App server (validate token and size) -> KGS (get paste_code) -> Object storage (write text) -> SQL (insert metadata) -> 201 Created with paste_url
```

---

- Read paste

![pastebin](./pastebin.drawio.png)

```text
Client -> LB -> App server -> Cache (look up paste_code, if enabled)
    -> if hit -> check cached alias and expiry -> 200 OK (text/plain) if valid, otherwise 404
    -> if miss or disabled -> SQL (look up metadata by paste_code)
        -> if unknown, expired, or alias mismatch -> 404 Not Found
        -> if active -> Object storage (read by object_key) -> Cache (if enabled) -> 200 OK (text/plain)
```

---

### Step 6 - Wrap up

- feature
  - functional
  - non-functional
- resolved vs open-end
- road map
