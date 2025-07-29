# Prometheus - Observability

[Back](../../index.md)

- [Prometheus - Observability](#prometheus---observability)
  - [Architecture](#architecture)
  - [Monitoring](#monitoring)
    - [Method of Monitoring](#method-of-monitoring)
  - [Observability](#observability)

---

## Architecture

- `Monolithic Architecture`

  - feature
    - All services **in one** application
    - User Interface and business logic **in one** application
    - All services shared one database
  - Drawsback
    - To make a change, **entire** application was deployed.
    - Incremental improvement was **time consuming.**

- `Microservice Architecture`

  - Features:
    - Individual services
    - each service has its own storage
    - UI and services are separate.
  - Benefits
    - Changes can be deployed **without deploying** the entire software.
    - Development on sercies can be done simultaneously.

- DevOps view on the evolution fo application architecture

  - monolithic: waterfall methodology.
    - Requirement -> analysis -> design -> code -> test -> maintenance
  - microservices: continuous integration and delivery(CI/CD) method
    - plan -> code -> build -> test -> release -> deploy -> operate -> measure

- Impact of microservices and CI/CD to `observability`
  - many services to monitor.
  - intra-service communications can fail.
  - more valnerable to security threats.
  - more changes are deployed.

---

## Monitoring

- `Monitoring`

  - the **process of collecting and visuaizing** data about systems regularly, to view and track system's health.

- Key concerns

  - Is the service on?
    - car dashboard: engine rpm beyond zero
    - website: HTTP GET -> returns HTTP 200
  - Is the service functioning as expected?
    - car dashboard: speedometer
    - Website: python / database error
  - Is the service performing well?
    - car dashboard: warning/alert
    - Website: http reponse time 20ms. Throughput: 2000 request/second

- `Telemetry Data`

  - the data that is collected for monitoring, to discover where the problem might be.
  - used to measure a system's internal states by examining its outputs.

- Metrics used to measure the DevOps success
  - `Mean Time to Detection (MTTD)`
    - the amount of time, on average, between the **start of an issue** and when **teams become aware of it**.
  - `Mean Time to Resolve (MTTR)`
    - the average amount of time between **when an issure is detected**, and **when system are fixed and operating normally**.

---

### Method of Monitoring

| Layers                                         | Methods                      |
| ---------------------------------------------- | ---------------------------- |
| UI Layer (Website/Mobile)                      | `Core Web Vitals`            |
| Service Layer (Microservices)                  | `RED`, `Four Golden Signals` |
| Infrastructure Layer (Disk/memory/network/CPU) | `USE`, `Four Golden Signals` |

- `RED` Method (Request Oriented)

  - **Rate** (throughput): Request per second
  - **Duration**: Latency or Transaction Response Time
  - **Errors**: Failed requests, i.e., HTTP 500

- `USE` Method (Resource Oriented)

  - **Utilization**. i.e., CPU Usage%, Disk Space%
  - **Error**. i.e., Disk write error. Zero = Good
  - **Saturation**. i.e.,Network queue length. Zero = Good

- `Four Golden Signals` Method (`RED+S`)

  - **Traffic** (Throughput)
  - **Latency**
  - **Errors**
  - **Saturation** (Resources at 100 capacity)

- `Core Web Vitals` UI layer
  - Largest Contentful Paint (Perceived page load)
    - How long it takes for a user to feel that the page is loaded completely.
  - First Input Delay (Perceived responsiveness)
    - How long it takes for a text box, for example, to become available and user can use.
  - Cumulative Layout Shift (perceived stability)
    - essential in SEO

---

## Observability

- To use `monitoring`, we need to know what to monitor in advance.

  - Using monitoring only results in **Tool Sprawling**, using differen tools but not coherently.

- `Observability`

  - `Monitoring` is part of obervability
  - gathering actionable data in a way that gives a **holistic view** of the entire system, **telling where, when, and why an issue occurs**.

- Car example:

  - monitoring:
    - dashboard shows the metrics, i.e., speed, engine alert
  - observability:
    - a mechanic understands and fix the error by observing the data.

- Types of `Telemetry Data`: `MELT`

  - `Event`:
    - an action happened at a given time.
      - i.e., a transaction occurs at 9:32 am.
    - Common Event Streaming platform, `Kalfka`
  - `Metric`:
    - an aggregated value representing events in a period of time.
      - i.e., average 100 transaction made in a day
    - Used to compare the performance of the systems in a time.
  - `Log`:
    - a detailed representation of an event.
      - i.e., Customer, time, price, amount, location, payment.
  - `Trace`
    - Shows the interactions of microservices to fulfill a request.
      - i.e., interaction of credit card, POS, banking system, sale database.
    - used to identify the component of the system could fail.

- Methods of Collecting Metric
  - Push method:
    - Applications and Microservices **send the metric to an endpoints**, via TCP, UDP, or HTTP.
  - Scrape method:
    - Applications and Microservices **provid APIs** for the time series database, **to read** the metrics.
      - i.e., Prometheus scrapes metrics
