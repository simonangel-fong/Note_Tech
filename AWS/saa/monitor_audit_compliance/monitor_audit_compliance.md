# AWS - Monitor, Audit, Compliance

[Back](../index.md)

- [AWS - Monitor, Audit, Compliance](#aws---monitor-audit-compliance)
  - [CloudWatch vs CloudTrail vs Config](#cloudwatch-vs-cloudtrail-vs-config)
    - [Use Case: For an Elastic Load Balancer](#use-case-for-an-elastic-load-balancer)

---

## CloudWatch vs CloudTrail vs Config

- `CloudWatch`

  - Performance **monitoring** (metrics, CPU, network, etc…) & **dashboards**
  - **Events** & **Alerting**
  - **Log** Aggregation & Analysis

- `CloudTrail`

  - **Record API calls** made within your Account by everyone
  - Can define **trails** for specific resources
  - **Global** Service

- `Config`
  - **Record** configuration **changes**
  - **Evaluate** resources against **compliance rules**
  - Get **timeline** of changes and compliance

---

### Use Case: For an Elastic Load Balancer

- `CloudWatch`:
  - **Monitoring** Incoming connections **metric**
  - **Visualize** error codes as % over time
  - Make a **dashboard** to get an idea of your load balancer performance
- `Config`:

  - Track security group **rules** for the Load Balancer
  - Track configuration **changes** for the Load Balancer
  - Ensure an **SSL certificate** is always assigned to the Load Balancer (compliance)

- `CloudTrail`:
  - Track who made any **changes** to the Load Balancer with API calls

---

[TOP](#aws---monitor-audit-compliance)
