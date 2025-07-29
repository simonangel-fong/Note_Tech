# Prometheus - Data Model

[Back](../index.md)

- [Prometheus - Data Model](#prometheus---data-model)
  - [Data Model](#data-model)
    - [Metric names](#metric-names)
    - [Metric labels](#metric-labels)

---

## Data Model

- Prometheus stores data as `time series`
  - streams of **timestamped values** belonging to the same `metric` and the same set of `labeled` dimensions
- Every `time series` is **uniquely identified** by its `metric` name and optional **key-value pairs** called `labels`.

---

### Metric names

- `Metric names`
  - **SHOULD** specify the **general feature** of a system that is measured
    - e.g., `http_requests_total` - the total number of HTTP requests received
  - **MAY** use any UTF-8 characters.
  - **SHOULD** match the regex `[a-zA-Z_:][a-zA-Z0-9_:]*` for the best experience and compatibility
  - Colons (':') are **reserved** for user-defined recording rules. They **SHOULD NOT** be used by exporters or direct instrumentation.

---

### Metric labels

- `Labels`
  - capture **different instances** of the **same** `metric name`. 

- **Label names**
  - **MAY** use any UTF-8 characters.
  - beginning with `__` (two underscores) **MUST be reserved** for **internal** Prometheus use.
  - **SHOULD match** the regex `[a-zA-Z_][a-zA-Z0-9_]*` for the best experience and compatibility
- **Label values**
  - **MAY contain** any UTF-8 characters.
  - an empty label value are considered **equivalent** to labels that **do not exist.**
  - 

```promql
<metric_name> {key=value, key=value, ...}

auth_api_hit {count=1,time_taken=800}
api_http_requests_total{method="POST", handler="/messages"}

<!-- Names with UTF-8 characters outside the recommended set must be quoted, -->
{"<metric name>", <label name>="<label value>", ...}

<!-- internal metric -->
{__name__="<metric name>", <label name>="<label value>", ...}
```

---
