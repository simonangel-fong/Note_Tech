# Prometheus - Data Model

[Back](../index.md)

- [Prometheus - Data Model](#prometheus---data-model)
  - [Data Model](#data-model)

---

## Data Model

- Prometheus stores data as time series
- Each time series is identified by metric name and labels
- Label
  - optional
  - key and value pair

```txt
<metric_name> {key=value, key=value, ...}

auth_api_hit {count=1,time_taken=800}
```

---
