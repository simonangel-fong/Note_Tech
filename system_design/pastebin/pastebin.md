# System Design - URL shortening service

[Back](../system_design.md)

- [System Design - URL shortening service](#system-design---url-shortening-service)
  - [Pastebin](#pastebin)
  - [Steps](#steps)
    - [Step 1 - Requirements](#step-1---requirements)
    - [Step 2 - API](#step-2---api)
    - [Step 3 - Data Model](#step-3---data-model)
    - [Step 4 - High level](#step-4---high-level)
    - [Step 5 - Detailed design](#step-5---detailed-design)

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

- Estimation
  - assume a 5:1 ratio between read and write.
  - assume 5 million reads per day
  - assume each paste on average 10KB.
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

- `POST /api/v1/paste`
- header: api_token
- param:
  - paste_data
  - alias optional
  - expire optional
- return
  - uuid
  - 200
- `GET /api/v1/uuid`
  - header: api_token
  - return
    - pasted_data
    - 200

---

### Step 3 - Data Model

- pasted data tb

| col        | data_type | DESC         |
| ---------- | --------- | ------------ |
| uuid       | int       | unique id    |
| paste_data | varchar2  | pasted data  |
| u_url      | varchar2  | unique data  |
| user_id    | int       | user id      |
| expire     | timestamp | expired time |

- user tb

| col     | data_type | DESC       |
| ------- | --------- | ---------- |
| user_id | int       | user id    |
| email   | varchar2  | user email |

- SQL
- master-replicas: availability / reliability
- shard: open

---

### Step 4 - High level

client -> web server -> database

- Evaluate: create paste
- Evaluate: get paste

---

### Step 5 - Detailed design

- High availability
  - LB
    - between client and app server
    - between app server and db

- UUID generation; unguessable
  - Key generation service(KGS): hash function
  - master-standby: spof

- Database
  - master-replicas
  - data partition
    - **hashing function** will **randomly distribute** URLs into different partitions

- Flowchart
  - write: client -> LB -> web server -> KGS(get UUID) -> LB -> DB
  - read: client -> LB -> web server -> LB -> DB

- expired:
  - backend clean up

- Telemetory & Analytics:
  - aggregate: user location; common user

- Seurity:
  - api key: authen
