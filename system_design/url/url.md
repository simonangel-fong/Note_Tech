# System Design - URL shortening service

[Back](../system_design.md)

- [System Design - URL shortening service](#system-design---url-shortening-service)
  - [URL shortening servic](#url-shortening-servic)
  - [Steps](#steps)
    - [Step 1 - Requirements](#step-1---requirements)
      - [Estimation](#estimation)
    - [Step 2 - API Design](#step-2---api-design)
    - [Step 3 - Data Model](#step-3---data-model)
    - [Step 4 - High-level design](#step-4---high-level-design)
    - [Step 5 - Detailed design](#step-5---detailed-design)
      - [Performance](#performance)
      - [Reliability and availability](#reliability-and-availability)
      - [Security](#security)
      - [Specific issues](#specific-issues)
      - [Flowchart](#flowchart)
    - [Step 6 - Wrap up](#step-6---wrap-up)

---

## URL shortening servic

- `URL shortening`
  - create shorter aliases, named short links, for long URLs.
  - Users are redirected to the original URL when they hit these short links.

- benefit
  - save a lot of space when displayed, printed, messaged, or tweeted.
  - optimize links across devices, tracking individual links to analyze audience and campaign performance, and hiding affiliated original URLs.

---

## Steps

### Step 1 - Requirements

- Q:
  - Can you give an example of how a URL shortener work?
  - What is the traffic volume?
  - How long is the shortened URL?
  - What characters are allowed in the shortened URL?
  - Can shortened URLs be deleted or updated?

---

- **Functional Requirements**:
  1. Given a URL, our service should generate a shorter and unique alias of it. This is called a short link.
  2. When users access a short link, our service should redirect them to the original link.
  3. Users should optionally be able to pick a custom short link for their URL.
  4. Links will expire after a standard default timespan. Users should be able to specify the expiration time.

- **Non-Functional Requirements:**
  1. The system should be **highly available**. This is required because, if our service is down, all the URL redirections will start failing.
  2. URL redirection should happen in real-time with **minimal latency**.
  3. Shortened links should not be guessable (not predictable).

- **Extended Requirements:**
  1. Analytics; e.g., how many times a redirection happened?
  2. Our service should also be accessible through REST APIs by other services.

---

#### Estimation

- **Assumption**
  - read/write ratio: 100:1
  - **new** URL shortenings per month: 500M
  - size per url: 500 bytes
- Traffic
  - **read/redirection** : 100 \* 500M => 50B per month
  - **qps write**: 500M / (30 days \* 24 hours \* 3600 seconds) = ~200 URLs/s
  - **qps read**: 100 \* 200 URLs/s = 20K/s
- **Storage**:
  - total urls in 5 years: 500 million \* 5 years \* 12 months = 30 billion
  - size in 5 years: 30 billion \* 500 bytes = 15 TB
- **Bandwidth**
  - **write/incoming**: 200 \* 500 bytes = 100 KB/s
  - **read/outgoing**: 20K \* 500 bytes = ~10 MB/s
- **Memory**(if cache)
  - **read request per day**: 20K \* 3600 seconds \* 24 hours = ~1.7 billion
  - **assumed 20% are hot url** to be cached: 0.2 \* 1.7 billion \* 500 bytes = ~170GB

---

### Step 2 - API Design

- Feature: Create short link
  - `POST /api/v1/url`
  - header: `api-token`
  - param (body):
    - `destination_url`
    - `custom_alias` (optional)
    - `expires_at` (optional, defaults to the standard expiration)
  - return:
    - `201 Created` with `short_url`
    - `409 Conflict` if the custom alias is taken

---

- Feature: Follow short link
  - `GET /{short_code}`
  - header: none required for public links
  - param (path): `short_code` (e.g., `aB3x7` in `GET /aB3x7`)
  - return:
    - `302 Found` with the destination URL in the `Location` header
    - `404 Not Found` if the link is unknown, expired, or revoked

---

- Feature: Revoke short link (if in scope)
  - `DELETE /api/v1/url/{short_code}`
  - header: `api-token` (link owner only)
  - param (path): `short_code`
  - return: `204 No Content`

---

### Step 3 - Data Model

**Short link mapping**

| Field             | Data type | Description                                       |
| ----------------- | --------- | ------------------------------------------------- |
| `short_code`      | String    | Unique key, generated or chosen as a custom alias |
| `destination_url` | String    | URL returned in the redirect                      |
| `expires_at`      | Timestamp | Time when the link stops working                  |
| `revoked_at`      | Timestamp | Set only when the owner revokes the link          |

**User links (if owner-only revocation is in scope)**

| Field        | Data type | Description                             |
| ------------ | --------- | --------------------------------------- |
| `short_code` | String    | Unique key referencing the link mapping |
| `user_id`    | String    | User who owns the link                  |

- NoSQL key-value
  - ~15 TB raw over 5 years; partitioning is challenge for SQL

---

### Step 4 - High-level design

client -> app server -> database

---

### Step 5 - Detailed design

#### Performance

- Estimated average load: ~20K redirects/s and ~200 creates/s.
- Issue: repeated **database reads** for popular links
  - Solution: **Redis caching**
    - Cache hot mappings by `short_code`.
    - A high-memory Redis node can hold ~170 GB of raw cache data plus overhead.
    - Eviction policy: least recently used (LRU).

---

#### Reliability and availability

- Issue: app server **scaling and failure**
  - Solution: **Load balancing**
    - Route requests to healthy app servers across availability zones.
    - App servers use the Redis and database service endpoints.
- Issue: **database failure**
  - Solution: **Primary–standby failover**
    - Replicate data to a standby in another availability zone.
    - Promote the standby if the primary fails.
- Issue: data growth to ~15 TB raw over 5 years
  - Solution: **Sharding**
    - Partition mappings by `short_code`.

---

#### Security

- Issue: unauthorized link management
  - Solution: **Token authentication and ownership checks**
    - Require `api-token` for creation and revocation. Verify ownership on revoke.
    - Public redirects are anonymous.
- Issue: abusive traffic
  - Solution: **Rate limiting**
    - Limit link creation and repeated requests for invalid codes.

---

#### Specific issues

- Issue: short-code collisions and predictability
  - Solution: **Key generation service (KGS)**
    - Pre-generate secure random Base62 codes in batches.
    - Reserve each generated code atomically. Insert the mapping only if `short_code` is unused, including when a user requests a custom alias.
    - Use a standby KGS with access to the same durable reservation state.
    - Seven characters give `62^7 ≈ 3.5T` possible codes. Choose the length based on the number of active links and the risk of guessing one.
- Issue: expired links
  - Solution: **Expiration checks and scheduled cleanup**
    - Check `expires_at` during redirects and cap cache TTL at expiration.
    - Remove expired records with a scheduled job.
    - Evict cached mappings on revocation if that feature is in scope.

---

#### Flowchart

- Create short link

```text
Client -> LB -> App server(authentication+rate limiter) -> KGS(get short code) -> LB -> DB(insert)
```

---

- Get full link

```text
Client -> LB -> App server(authentication + rate limtier) -> Cache
    -> if hit -> return
    -> if miss -> LB -> DB -> cache -> return
```

![Redirect path through the load balancer, cache, and database](./img/url_diagram.png)

---

### Step 6 - Wrap up

- feature
  - functional
  - non-functional
- resolved vs open-end
- road map
