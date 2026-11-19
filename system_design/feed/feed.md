# System Design - News Feed System

[Back](../system_design.md)

- [System Design - News Feed System](#system-design---news-feed-system)
  - [News Feed System](#news-feed-system)
  - [Step 1 - requirements](#step-1---requirements)
    - [Estimation](#estimation)
  - [Step 2 - API design](#step-2---api-design)
  - [Step 3 - Data model](#step-3---data-model)
  - [Step 4 - High level](#step-4---high-level)
  - [Step 5 - details](#step-5---details)
    - [Reliability \& HA](#reliability--ha)
    - [Performance](#performance)
    - [Security](#security)
    - [Specific issue](#specific-issue)
    - [Diagram](#diagram)
  - [Step 6 - wrap up](#step-6---wrap-up)
  - [Reference](#reference)
  - [Step 1 - Understand the problem and establish design scope](#step-1---understand-the-problem-and-establish-design-scope)
  - [Step 2 - Propose high-level design and get buy-in](#step-2---propose-high-level-design-and-get-buy-in)
    - [Newsfeed APIs](#newsfeed-apis)
    - [feed publishing flow](#feed-publishing-flow)
    - [Newsfeed building](#newsfeed-building)
  - [Step 3 - Design deep dive](#step-3---design-deep-dive)
    - [Feed publishing deep dive](#feed-publishing-deep-dive)
    - [Newsfeed retrieval deep dive](#newsfeed-retrieval-deep-dive)
  - [Step 4 - Wrap up](#step-4---wrap-up)

---

## News Feed System

- `news feed`
  - a **constantly updating digital stream** of headlines, articles, posts, and real-time updates displayed on a web page or mobile app screen.

- Similar questions commonly asked are:
  - design Facebook news feed
  - Instagram feed
  - Twitter timeline, etc.

---

## Step 1 - requirements

**Functional requirements:**

1. Newsfeed will be generated based on the posts from the people, pages, and groups that a user **follows**.
2. A user may have many friends and follow a large number of pages/groups.
3. Feeds may contain images, videos, or just text.
4. Our service should support appending new posts as they arrive to the newsfeed for all active users.

**Non-functional requirements:**

1. Our system should be able to generate any user’s newsfeed in **real-time** - maximum latency seen by the end user would be 2s.
2. A post shouldn’t take more than 5s to make it to a user’s feed assuming a new newsfeed request comes in.

---

### Estimation

- **Assume:**
  - average friends per user: 300
  - average pages follwed per user: 200
  - DAU: 300M
  - avg fetch per day per user: 5
  - avg size per post: 1KB
- **Performance**:
  - read/query: 300M \* 5 / 24 / 3600 = 17.4K rps
- **Bandwidth**:
  - read/query: 17.4K rps \* 1KB = 18M/s

---

## Step 2 - API design

Feature: get feed

- `GET /api/v1/feed`
- header: api_token

---

## Step 3 - Data model

- user tb(SQL)

| field   | datatype | desc       |
| ------- | -------- | ---------- |
| user_id | int      | user id    |
| email   | varchar  | user email |

- post tb(NoSQL - kv)

| field      | datatype  | DESC               |
| ---------- | --------- | ------------------ |
| post_id    | int       | post id            |
| content    | varchar   | post content       |
| created_at | timestamp | post creation time |

- follow tb(NoSQL Graph)

| field     | datatype | DESC           |
| --------- | -------- | -------------- |
| user_id   | int      | user id        |
| follow_id | int      | follow user id |

- feed tb(NoSQL document)

| field        | datatype  | desc                  |
| ------------ | --------- | --------------------- |
| user_id      | int       | user id               |
| feed_content | json      | post list             |
| last_update  | timestamp | last update timestamp |

---

## Step 4 - High level

```
client -> app server -> database
```

---

## Step 5 - details

### Reliability & HA

- Issue: app servers == SPOF
  - Solution: **app server scaling + LB**
    - LB health check app server
    - route traffic only to healthy server
- Issue: DB server == SPOF
  - Solution: **primary-standby**
    - if master fails, standby -> master

### Performance

- Issue: app server handle high volume request
  - Solution: **horizontal scaling**

- Issue: DB handle high rps
  - Solution: **master-replicas**
    - master=wriet; replicas=read; replication: master->relicas

- Issue: DB high volume of data
  - Solution: **partitioning**
    - sharding data to multiple servers

- Issue: request hit DB
  - Solution: **Cache**
    - cache data in memory

### Security

- Issue: unauthorized request
  - Solution: **Authentication**
    - use api_token in header

- Issue: abusive user
  - Solution: **rate limiter**
    - throttle request

### Specific issue

- Issue: Sort post in feed
  - Solution: **Snowflake algorithm**
    - timestemp_region_serverSequence

- Issue: push or pull mode
  - Solution: **hybrid**
    - push mode: generate feed when post publish
    - pull mode: generate feed when user pull feed
    - hybrid:
      - active user: push
      - inactive user: pull

- Issues: Feed update time consuming(celebrity)
  - Solution: **MQ decouple**
    - fanout server to decouple feed update per user
    - feed worker handle specific feed generations

### Diagram

![feed](./img/feed.drawio.png)

---

## Step 6 - wrap up

- features
- no-functions
- open issue
- road map

---

## Reference

## Step 1 - Understand the problem and establish design scope

- Q:
  - Is this a mobile app? Or a web app? Or both?
  - What are the important features?
    - A user can publish a post and see her friends’ posts on the news feed page.
  - Is the news feed sorted by reverse chronological order or any particular order such as topic scores? For instance, posts from your close friends have higher scores.
    - assume the feed is sorted by reverse chronological order.
  - How many friends can a user have?
    - 5000
  - What is the traffic volume?
    - 10 million DAU
  - Can feed contain images, videos, or just text?

---

## Step 2 - Propose high-level design and get buy-in

- The design is divided into two flows: feed publishing and news feed building

### Newsfeed APIs

- Feed publishing API: publish a post
  - `POST /v1/me/feed`
  - param:
    - content
    - api token
- Newsfeed retrieval API: retrieve news feed
  - `GET /v1/me/feed`
  - param:
    - api token

### feed publishing flow

![feed_publish](./img/feed_publish.png)

- Web servers: web servers redirect traffic to different internal services.
- **Post service**: **persist** post in the database and cache
- **Fanout service**: push **new content** to friends’ news feed. Newsfeed data is stored in the **cache** for fast retrieval.
- **Notification service**: **inform** friends that new content is available and send out push notifications.

---

### Newsfeed building

![feed_build](./img/feed_build.png)

- **Web servers**: web servers **route** requests to newsfeed service.
- **Newsfeed service**: news feed service **fetches** news feed from the cache.
- **Newsfeed cache**: store **news** feed IDs needed to render the news feed.

---

## Step 3 - Design deep dive

### Feed publishing deep dive

![feed_publish_deep](./img/feed_publish_deep.png)

- **Web servers**: authentication and rate-limiting
- **Fanout service**: the process of delivering a post to all friends.
  - 1. Fetch friend IDs from the graph database.
  - 2. Get friends info from the user cache.
  - 3. Send friends list and new post ID to the **message queue**.
  - 4. Fanout workers fetch data from the message queue and store news feed data in the news feed cache.
  - 5. Store <post_id, user_id > in news feed cache.

---

- Fanout models:
  - push model: fanout on write
    - news feed is pre-computed **during write time**.
    - A new post is delivered to friends’ cache **immediately after it is published**.
    - pro:
      - Fetching news feed is fast
    - con:
      - generating news feeds for all of them are slow and time consuming.
      - For inactive users or those rarely log in, pre-computing news feeds waste computing resources.

  - pull model: fanout on read
    - generated during read time
    - Recent posts are pulled when a user loads her home page.
    - pro:
      - not waste computing resources on inactive users
    - Cons:
      - Fetching the news feed is slow
  - hybrid approach
    - push model for the majority of userss

---

### Newsfeed retrieval deep dive

![feed_build_deep](./img/feed_build_deep.png)

1. A user sends a request to **retrieve** her news feed. The request looks like this: /v1/me/feed
2. The load balancer redistributes requests to web servers.
3. Web servers call the news feed service to fetch news feeds.
4. **News feed service** gets a list post IDs from the news feed cache.
5. A user’s news feed is more than just a list of feed IDs. It contains username, profile picture, post content, post image, etc.
   - Thus, the news feed service **fetches the complete user and post objects** from caches (user cache and post cache) to construct the fully hydrated news feed.
6. The fully hydrated news feed is returned in JSON format back to the client for rendering.

---

## Step 4 - Wrap up

- high-level talking points
  - Scaling the database:
    - Vertical scaling vs Horizontal scaling
    - SQL vs NoSQL
    - Master-slave replication
    - Read replicas
    - Consistency models
    - Database sharding
  - Keep web tier stateless
  - Cache data as much as you can
  - Support multiple data centers
  - Lose couple components with message queues
  - Monitor key metrics.
    - For instance, QPS during peak hours and latency while users refreshing their news feed are interesting to monitor.
