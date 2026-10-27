# System Design - BACK-OF-THE-ENVELOPE ESTIMATION

[Back](../system_design.md)

- [System Design - BACK-OF-THE-ENVELOPE ESTIMATION](#system-design---back-of-the-envelope-estimation)
  - [Power of two](#power-of-two)
  - [Latency](#latency)
  - [Availability numbers](#availability-numbers)
  - [Estimate example](#estimate-example)

---

## Power of two

- A `byte` is a sequence of 8 `bits`.
- An **ASCII character** uses one `byte` of memory (`8 bits`)

| Power | Approximate value | Full name  | Short name |
| ----- | ----------------- | ---------- | ---------- |
| 10    | 1 Thousand        | 1 Kilobyte | 1 KB       |
| 20    | 1 Million         | 1 Megabyte | 1 MB       |
| 30    | 1 Billion         | 1 Gigabyte | 1 GB       |
| 40    | 1 Trillion        | 1 Terabyte | 1 TB       |
| 50    | 1 Quardillion     | 1 Petabyte | 1 PB       |

---

## Latency

- `Memory` is fast but the `disk` is slow.
- Avoid disk seeks if possible.
- Simple **compression** algorithms are fast.
- **Compress data before sending** it over the internet if possible.
- Data centers are usually in **different regions**, and it takes time to send data between them.

---

## Availability numbers

- service level agreement (SLA)
  - agreement between the service provider and customer
  - Amazon, Google, and Microsoft set their SLAs at **99.9%**

- `90% (1 Nine)`: Allows up to 36.5 days of downtime per year.
- `99% (2 Nines)`: Allows up to 3.65 days (87.6 hours) of downtime per year.
- `99.9% (3 Nines)`: Allows up to 8.76 hours of downtime per year.
- `99.99% (4 Nines)`: Allows up to 52.56 minutes of downtime per year.
- `99.999% (5 Nines)`: Allows up to 5.26 minutes of downtime per year.
- `99.9999% (6 Nines)`: Allows up to 31.5 seconds of downtime per year.

---

## Estimate example

Assumptions:

- 300 million monthly active users.
- 50% of users use Twitter daily.
- Users post 2 tweets per day on average.
- 10% of tweets contain media.
- Data is stored for 5 years.

Estimations:

- Query per second (QPS) estimate:
  - Daily active users (DAU) = 300 million \* 50% = 150 million
  - Tweets QPS = 150 million \* 2 tweets / 24 hour / 3600 seconds = ~3500
  - Peek QPS = 2 \* QPS = ~7000
    > multiplier: commonly peak QPS = 2x QPS

- Media storage Estimate:
  - Average tweet size:
    - tweet_id 64 bytes
    - text 140 bytes
    - media 1 MB
  - Media storage per day: 150 million \* 2 \* 10% \* 1 MB = 30 TB
  - 5-year media storage: 30 TB \* 365 \* 5 = ~55 PB
