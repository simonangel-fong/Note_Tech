# Prometheus - Data Collection

[Back](../index.md)

- [Prometheus - Data Collection](#prometheus---data-collection)
  - [Data Collection](#data-collection)

---

## Data Collection

- **Scaping** method

  - Common method used by `Prometheus`
  - Applications install `exporter`, from which `Prometheus` pulls the metrics.

- **Push** method

  - `Prometheus` uses `push gateway` to collect metrics from the application.
  - Limitation of push method
    - requires application source code to implement the push method
    - unscalable

- `push gateway`
  - a component of `Prometheus`
  - acts as temporary storage, to which application send the metric and from which Prometheus can scrape metric.
  - allows applications to use push method.
  - Prometheus is always a pull time series database.

---
