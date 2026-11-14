# System Design - YouTube

[Back](../system_design.md)

- [System Design - YouTube](#system-design---youtube)
  - [YouTube](#youtube)
  - [Step 1: Requirements](#step-1-requirements)
    - [Estimation](#estimation)
  - [Step 2: API design](#step-2-api-design)
  - [Step 3: Data model](#step-3-data-model)
  - [Step 4: High](#step-4-high)
  - [Step 5: details](#step-5-details)
    - [Reliability \& HA](#reliability--ha)
    - [Performance](#performance)
    - [Security](#security)
    - [Specific](#specific)
    - [FlowChart](#flowchart)
    - [Diagram](#diagram)
  - [Step 6: Wrap up](#step-6-wrap-up)
  - [Reference](#reference)
  - [Step 1 - Understand the problem and establish design scope](#step-1---understand-the-problem-and-establish-design-scope)
  - [Step 2 - Propose high-level design and get buy-in](#step-2---propose-high-level-design-and-get-buy-in)
    - [Video uploading flow](#video-uploading-flow)
    - [Video streaming flow](#video-streaming-flow)
    - [Step 3 - Design deep dive](#step-3---design-deep-dive)
    - [Video transcoding](#video-transcoding)
    - [Directed acyclic graph (DAG) model](#directed-acyclic-graph-dag-model)
    - [Video transcoding architecture](#video-transcoding-architecture)
  - [Step 4 - Wrap up](#step-4---wrap-up)

---

## YouTube

- video sharing platform
  - e.g., YouTube, Netflix, Hulu

---

## Step 1: Requirements

**Functional Requirements:**

1. Users should be able to **upload** videos.
2. Users should be able to **share** and view videos.
3. Users should be able to perform **searches** based on video **titles**.
4. Our services should be able to **record stats** of videos, e.g., likes/dislikes, total number of views, etc.
5. Users should be able to add and view **comments** on videos.

**Non-Functional Requirements:**

1. The system should be highly **reliable**, any video uploaded should not be lost.
2. The system should be highly **available**. **Consistency** can take a hit (in the interest of availability); if a user doesn’t see a video for a while, it should be fine.
3. Users should have a **real time** experience while watching videos and should not feel any lag.

**Not in scope:**
Video recommendations, most popular videos, channels, subscriptions, watch later, favorites, etc.

---

### Estimation

- **Assume**
  - total users: 1.5B
  - DAU: 800M
  - viewed per user per day: 5 videos
  - upload/view ratio: 1:200
- **Performance**:
  - read/view: 800M \* 5 videos / 3600 /24 = 46k rps
  - write/upload: 46k/s / 200 = 230 rps
- **Storage:**
  - 5 years storage: avg video size \* write rps \* 3600 \* 24 \* 365
- **Bandwidth:**

---

## Step 2: API design

- feature: upload
- `POST /api/v1/video`
- header: api_token
- param:
  - video_title
  - video_shownote
  - video_data

---

- feature: view
- `GET /api/v1/<video_id>`
- header: api_token optional
- param: video_id

---

- feature: search
- `GET /api/v1/q?title=<video_title>`
- header: api_token optional
- param: video_title

---

- feature: comment
- `POST /api/v1/comment/<video_id>`
- header: api_token
- param:
  - video_id
  - comment_data

---

- feature: like
- `POST /api/v1/like/<video_id>`
- header: api_token
- param:
  - video_id
  - like/dislike

---

- feature: stat metadata
- `POST /api/v1/stat/<video_id>`
- header: api_token optional
- param:
  - video_id
  - stat_data

---

## Step 3: Data model

- user table: SQL

| Field   | datatype | desc       |
| ------- | -------- | ---------- |
| user_id | int      | user id    |
| email   | varchar  | user email |

- video metadata: NoSQL

| Field       | datatype | desc                      |
| ----------- | -------- | ------------------------- |
| video_id    | int      | video id                  |
| length      | int      | length of video in second |
| title       | varchar  | video title               |
| storage_url | varchar  | video storage url/arn     |

- comment table: NoSQL kv

| Field      | datatype | desc            |
| ---------- | -------- | --------------- |
| comment_id | int      | comment id      |
| video_id   | int      | video id        |
| comment    | varchar  | comment content |

- stat table: NoSQL kv

| Field     | datatype | desc                                      |
| --------- | -------- | ----------------------------------------- |
| user_id   | int      | user id                                   |
| video_id  | int      | video id                                  |
| like      | int      | whether like video (check: like, dislike) |
| stat_data | int      |                                           |

---

## Step 4: High

```
client -> app server -> database
```

---

## Step 5: details

### Reliability & HA

- Issue: API server == SPOF
  - Solution: **LB**
    - LB health check app server
    - distribute traffic

- Issue: DB == SPOF
  - Solution: **Partitioning + master-standby**
    - **data shard**
    - **master-standby**:
      - if master fails, one replica promote to master

- Issue: video data loss
  - Solution: **Partitioning**
    - multiple replica storage

---

### Performance

- Issue: high volume rps
  - Solution: **horizontal scaling + master-replicas**
    - H scaling: handle high traffic
    - read replicas: make HA of read requests

- Issue: upload video takes time
  - Solution: **Separate download and upload workload**
    - download api: download request
    - upload api: upload request

- Issue: download video takes time
  - Solution: **Cache videos in CDN**
    - close to client

- Issue: request direct to DB
  - Solution: **memory Cache(redis)**
    - cache common data in memory
      - like/dislike
      - metadata (cache for 7 seven days)
      - comment (pagenation)
      - user
    - eviction police: `Least Recently Used (LRU)`

### Security

- Issue: anonymous user upload
  - Solution: **Authentication**
    - header: api_token

- Issue: abusive request
  - Solution: **rate limiter**
    - limit request in a period

### Specific

- Issue: unify video format
  - Solution: **formating process + MQ**
    - user upload video -> format video into unified schema -> storage (replication) -> add CDN
    - MQ decouple submition and processing

- Issue: preprocess
  - Solution: **DAG**
    - sequence + parallel

---

### FlowChart

- upload video

```
client -> LB -> API server -> preprocess server -> MQ -> storage -> video metadata DB -> update cache -> upload CDN
```

- view video

```
client -> LB -> API serer -> cache -> database -> CDN -> download video
```

- comment/stat

```
client -> LB -> API server -> cache -> database
```

---

### Diagram

![](./img/youtube.drawio.png)

---

## Step 6: Wrap up

- feature
  - functional
  - non-functional
- resolved vs open-end
- road map

---

## Reference

## Step 1 - Understand the problem and establish design scope

- Q:
  - What features are important?
    - Ability to upload a video and watch a video.
  - What clients do we need to support?
    - Mobile apps, web browsers, and smart TV
  - How many daily active users do we have?
    - 5 million
  - What is the average daily time spent on the product?
    - 30 minutes
  - Do we need to support international users?
    - Yes, a large percentage of users are international users.
  - What are the supported video resolutions?
    - The system accepts most of the video resolutions and formats.
  - Is encryption required?
    - Yes
  - Any file size requirement for videos?
    - Our platform focuses on small and medium-sized videos. The maximum allowed video size is 1GB.
  - Can we leverage some of the existing cloud infrastructures provided by Amazon, Google, or Microsoft?
    - That is a great question. Building everything from scratch is unrealistic for most companies, it is recommended to leverage some of the existing cloud services.

- features
  - Ability to **upload** videos **fast**
  - Smooth video **streaming**
  - Ability to change video **quality**
  - Low infrastructure **cost**
  - High availability, scalability, and reliability requirements
  - Clients supported: mobile apps, web browser, and smart TV

- estimation
  - Assume the product has **5 million** `daily active users (DAU)`.
  - Users watch **5 videos** per day.
  - **10%** of users upload 1 video per day.
  - Assume the average video size is **300 MB**.
  - Total daily storage space needed: 5 million \* 10% \* 300 MB = 150TB

- CDN cost.
  - When **cloud CDN** serves a video, you are charged for **data transferred** out of the CDN.
  - Let us use Amazon’s CDN CloudFront for cost estimation.
    - Assume 100% of traffic is served from the United States. The average cost per GB is $0.02.
  - For simplicity, we only calculate the cost of video streaming.
    - 5 million \* 5 videos \* 0.3GB \* $0.02 = $150,000 per day.

---

## Step 2 - Propose high-level design and get buy-in

![high_level](./img/high_level.png)

- streamed from the CDN
- API servers:
  - feed recommendation, generating video upload URL, updating metadata database and cache, user signup, etc.

- two flows:
  - Video uploading flow
  - Video streaming flow

---

### Video uploading flow

- Flow a: upload the actual video

![high_upload_flow](./img/high_upload_flow.png)

1. Videos are **uploaded** to the original storage.
2. `Transcoding servers` fetch videos from the original storage and **start transcoding**.
3. Once transcoding is complete, the following two steps are executed in parallel:
   3a. Transcoded videos are **sent** to `transcoded storage`.
   3a.1. Transcoded videos are **distributed** to `s`.
   3b. Transcoding completion **events** are queued in the `completion queue`.
   3b.1. `Completion handler` contains a bunch of workers that continuously **pull** event data from the queue.
   3b.1.a. and 3b.1.b. `Completion handler` updates the metadata database and cache when svideo transcoding is complete.
4. API servers **inform** the client that the video is successfully uploaded and is ready for streaming.

---

- Flow b: update the metadata

![high_update_metadata](./img/high_update_metadata.png)

---

### Video streaming flow

- streaming protocol
- To lower latency, Videos are streamed from CDN directly. The edge server closest to you will deliver the video.

![high_streaming](./img/high_streaming.png)

---

### Step 3 - Design deep dive

### Video transcoding

- Why
  - Many devices and browsers only support certain types of video formats. Thus, it is important to encode a video to different formats for compatibility reasons.
  - To ensure users watch high-quality videos while maintaining smooth playback, it is a good idea to deliver **higher resolution** video to users who have **high network bandwidth** and **lower resolution** video to users who have **low bandwidth**.
  - switching video quality automatically or manually based on network conditions is essential for smooth user experiencess

---

### Directed acyclic graph (DAG) model

![deep_dag](./img/deep_dag.png)

---

### Video transcoding architecture

![deep_transcoding](./img/deep_transcoding.png)

---

## Step 4 - Wrap up

- additional points
  - Scale the API tier: Because API servers are stateless, it is easy to scale API tier horizontally.
  - Scale the database: You can talk about database replication and sharding.
  - Video takedowns: Videos that violate copyrights, pornography, or other illegal acts shall be removed.
