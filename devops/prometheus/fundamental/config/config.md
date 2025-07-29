# Prometheus - Configuration

[Back](../../index.md)

- [Prometheus - Configuration](#prometheus---configuration)
  - [Prometheus](#prometheus)
  - [Prometheus configuration](#prometheus-configuration)
  - [Start with Configuration File](#start-with-configuration-file)
  - [Common Metrics](#common-metrics)

---

## Prometheus

- `Prometheus`
  - a **monitoring platform** that **collects metrics** from monitored targets by **scraping** metrics `HTTP` endpoints on these targets.

---

## Prometheus configuration

- **Prometheus configuration** is `YAML`.
- Default: `prometheus.yml`

```yaml
# sample cf
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first.rules"
  # - "second.rules"

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["localhost:9090"]
```

- `global` block

  - controls the Prometheus server's **global configuration**.
  - options:
    - `scrape_interval`:
      - controls **how often** Prometheus will **scrape** targets.
      - default: every 15 seconds
      - can be overridden by individual targets.
    - `evaluation_interval`:
      - controls **how often** Prometheus will **evaluate** rules.
  - Prometheus uses rules to create new time series and to generate alerts.

- `rule_files` block

  - specifies the **location of any rules** that the Prometheus server to **load**.
  - Default: no rules.

- `scrape_configs` block
  - **controls what resources** Prometheus **monitors**.
  - Default: `prometheus` job
    - Prometheus exposes data about itself as an HTTP endpoint it can scrape and monitor its own health.
    - `http://localhost:9090/metrics`
      - target: `localhost`
      - port: `9090`
      - path: `/metrics`
  - Scrape job
    - target
    - port
    - expected path: `/metrics`

---

## Start with Configuration File

```sh
# To start Prometheus with our newly created configuration file
./prometheus --config.file=prometheus.yml
```

- Confirm: `http://localhost:9090`
- metrics endpoint: `http://localhost:9090/metrics`

---

## Common Metrics

| Metrics                                  | Description                                 |
| ---------------------------------------- | ------------------------------------------- |
| `promhttp_metric_handler_requests_total` | Total number of scrapes by HTTP status code |


```promql
# HELP promhttp_metric_handler_requests_total Total number of scrapes by HTTP status code.
# TYPE promhttp_metric_handler_requests_total counter
promhttp_metric_handler_requests_total{code="200"} 270
promhttp_metric_handler_requests_total{code="500"} 0
promhttp_metric_handler_requests_total{code="503"} 0
```
