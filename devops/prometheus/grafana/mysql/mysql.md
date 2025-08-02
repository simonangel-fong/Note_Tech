# Prometheus - Grafana Data Source: MySQL

[Back](../../index.md)

- [Prometheus - Grafana Data Source: MySQL](#prometheus---grafana-data-source-mysql)
  - [Data Source: MySQL](#data-source-mysql)

---

## Data Source: MySQL

- Use Grafana to visualize time series data in MySQL.

- Query must return 3 mandatory columns:
  - `metric`: the metric name
  - `value`: the metric value
  - `time_sec`: the unix time stamp, can use `unix_timestamp` function

---

- 1. Create mysql data source with credential
  - create a read-only user for grafana
- 2. Create Dashboard
- 3. Query:

```sql
SELECT
    unix_timestamp(s.SalesDateTime) AS time_sec
    , p.ProductName AS metric
    , Sum(s.Amount) AS value
FROM Products AS p
JOIN Sales AS s
ON p.ProductID = s.ProductID
GROUP BY p.ProductName, s.SalesDataTime
HAVING $__timeFilter(s.SalesDataTime)       -- filter timerange dynamically.
;
```
