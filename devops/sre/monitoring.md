# monitoring

[Back](./index.md)

---

## Monitoring

- Collecting, aggregation, and displaying quantitative data
- white-box monitoring:
  - based on metrics exposed by the internals of the system, including logs
- black-box monitoring:
  - run testing externally to see behavior as a user would see it.
- Dashboard
  - a summary of a service core metrics.
- Alert
  - the notification intended to be read by a human or automation

---

## 4 Golden signals

- latency: the time it takes to serve a request
- traffic: a measure of how much demand is being placed on the system
- Errors: the rate of requests that fail, e.g., 5XX, 2XX but wrong content
- Saturation: How close to full the service is
  - memory, disk, CPU, I/O, networkbandwidth

---

## effective runbooks

- runbooks/playbooks:
  - comprehensive and well-documented set of instructions and procedures for managing, troubleshooting, and resolving incidents and operational tasks.
