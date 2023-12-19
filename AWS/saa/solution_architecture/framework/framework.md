# AWS Well Architected Framework Whitepaper

[Back](../../index.md)

- [AWS Well Architected Framework Whitepaper](#aws-well-architected-framework-whitepaper)
  - [Well Architected Framework](#well-architected-framework)
    - [General Guiding Principles](#general-guiding-principles)
    - [6 Pillars(背, 知道名称即可)](#6-pillars背-知道名称即可)
  - [`AWS Well-Architected Tool`](#aws-well-architected-tool)

---

## Well Architected Framework

### General Guiding Principles

- ref:
  https://aws.amazon.com/architecture/well-architected

- Stop guessing your **capacity needs** (use asg)
- **Test** systems at **production scale**
- **Automate** to make architectural experimentation easier (cloudFormation)
- Allow for **evolutionary architectures**(serverful -> serverless)
  - Design based on **changing requirements**
- Drive architectures **using data** (storage and process)
- Improve through **game days** (try out)
  - **Simulate** applications for flash sale days

---

### 6 Pillars(背, 知道名称即可)

- 1. Operational Excellence
- 2. Security
- 3. Reliability
- 4. Performance Efficiency
- 5. Cost Optimization
- 6. Sustainability

- They are not something to balance, or trade-offs, they’re a **synergy(协同)**

---

## `AWS Well-Architected Tool`

- `AWS Well-Architected Tool`

  - Free tool to **review** your architectures against the 6 pillars Well-Architected Framework and **adopt** architectural best practices

- How does it work?
  - Select your **workload** and **answer** questions
  - **Review** your answers against the **6 pillars**
  - Obtain **advice**:
    - get videos and documentations,
    - generate a report,
    - see the results in a dashboard
- Let’s have a look: https://console.aws.amazon.com/wellarchitected

