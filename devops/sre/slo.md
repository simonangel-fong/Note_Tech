# SLO

[Back](./index.md)

---

# SLO

- all the services should have the definition of service level indicators (SLIs), objectives(SLOs), and agreements(SLAs)
- they are quantitative and measurable targets that are agreed upon with stakeholders and service customers to set clear expectations for system behavior.

---

- SLI
  - **measuable metrics** used to assess the performance and reliability of a service.
  - e.g., request latency, error rate, system throughput, request 3XX, request 500, uptime.

- SLO
  - an **internal** target **values** or range of **values** for a service level that is measurred by an SLI.
  - used to caculate error budget
  - SRE focus on meeting the SLO requirements

- SLA
  - the **contract** with users that includes **consequences** of meeting or missing the SLOs they contain
  - not for SRE, but more for business and product decisions.

- Measurable metrics
  - used to calculate SLO
  - e.g., 95% of all measured values are 150ms or less.

- standardize indicators
  - recommended to standardize on common definitions for SLIs.
  - Aggregations intervals: AVG over 1 min
  - Measurements are made: every 10s
  - which request are included: HTTP GETs from X monitoring jobs