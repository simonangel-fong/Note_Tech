# AWS - Control Tower

[Back](../index.md)

- [AWS - Control Tower](#aws---control-tower)
  - [`AWS Control Tower`](#aws-control-tower)
    - [`Guardrails`](#guardrails)

---

## `AWS Control Tower`

- Easy way to set up and govern a secure and compliant **multi-account AWS environment** based on best practices
- AWS Control Tower uses `AWS Organizations` to **create accounts**

- **Benefits**:
  - **Automate** the set up of your **environment** in a few clicks
  - **Automate** ongoing **policy management** using `guardrails`
  - **Detect** policy violations and **remediate** them
  - **Monitor** compliance through an **interactive dashboard**

---

### `Guardrails`

- Provides **ongoing governance** on all your AWS Accounts within your Control Tower **environment**

- Types of Guardrails
  - `Preventive Guardrail`
    - using `SCPs` (e.g., Restrict Regions across all your accounts)
  - `Detective Guardrail`
    - using `AWS Config` (e.g., identify untagged resources)

---

[TOP](#aws---control-tower)
