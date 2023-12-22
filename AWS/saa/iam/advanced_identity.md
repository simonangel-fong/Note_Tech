# AWS - Organizations

[Back](../index.md)

- [AWS - Organizations](#aws---organizations)
  - [`AWS Organizations`](#aws-organizations)
    - [Organizational Units (OU) Example](#organizational-units-ou-example)
    - [Benefits](#benefits)
    - [Service Control Policies(常考)](#service-control-policies常考)
      - [SCP Hierarchy](#scp-hierarchy)
      - [SCP Strategies](#scp-strategies)
    - [Hands-on](#hands-on)

---

## `AWS Organizations`

- `AWS Organizations`

  - **Global** service
  - Allows to manage **multiple** AWS accounts

- Typs of Account

  - `management account`

    - The **main** account

  - `member accounts`
    - Other accounts
    - Member accounts can only be **part of one** organization

- `Consolidated Billing`

  - across all accounts
  - **single** payment method on the `management account`
  - Pricing **benefits** from **aggregated usage** (volume discount for EC2, S3…)
  - **Shared** `reserved instances` and `Savings Plans` **discounts** across accounts

- `API` is available to automate **AWS account creation**

![organ_diagram](./pic/organ_diagram.png)

---

### Organizational Units (OU) Example

![ou_example01](./pic/ou_example01.png)

![ou_example02](./pic/ou_example02.png)

![ou_example02](./pic/ou_example03.png)

---

### Benefits

- **Advantages**

  - **Admin**

    - Establish `Cross Account Roles` for **Admin purposes**

  - **Billing**

    - Use **tagging standards** for **billing** purposes

  - **Log**

    - Send `CloudWatch Logs` to **central logging account**

  - **Audit**

    - Enable `CloudTrail` on all accounts, send **logs** to **central `S3` account**

  - **Security**
    - **Multi Account** vs One Account **Multi VPC**(more separated, more security)
    - `SCP`

---

### Service Control Policies(常考)

- `Service Control Policies (SCP)`

  - the `IAM policies` applied to **OU** or **Accounts** to **restrict** `Users` and `Roles`
  - They do not apply to the `management account` (**full** admin power)
  - Must have an **explicit allow**
    - does **not allow anything** by default – like `IAM`

- Sample:
  - You have strong regulatory requirements to **only allow** fully internally audited AWS services in **production**. You still want to **allow** your teams to experiment in a **development environment** while services are being audited. How can you best set this up?
    - Create Organ and create Prod and Dev OU, apply SCP on Prod OU
  - You have 5 AWS Accounts that you manage using AWS Organizations. You want to **restrict access** to certain AWS services in each account. How should you do that?
    - Organ SCP

---

#### SCP Hierarchy

![scp_hierarchy_example01](./pic/scp_hierarchy_example01.png)

- 注意:

1. 以上**对 Management Account 的 DenyAthena 无效**, 因为 full admin power.
2. AccountA 有授权 Redshift, 但不能与上位法 OU SCP 冲突, 所以无效.

---

#### SCP Strategies

- Blocklist Strategy
  - AllowsAllActions + Deny Actions

![scp_blocklist_example](./pic/scp_blocklist_example.png)

- Allowlist Strategy
  - Allow actions

![scp_allowlist_example.png](./pic/scp_allowlist_example.png)

---

### Hands-on

- Create Organization

![organ_handson01](./pic/organ_handson01.png)

- Add account

![organ_handson01](./pic/organ_handson02.png)

![organ_handson01](./pic/organ_handson03.png)

- Create OU

![organ_handson01](./pic/organ_handson04.png)

![organ_handson01](./pic/organ_handson05.png)

![organ_handson01](./pic/organ_handson06.png)

![organ_handson01](./pic/organ_handson07.png)

![organ_handson01](./pic/organ_handson08.png)

- Create subOU

![organ_handson01](./pic/organ_handson09.png)

![organ_handson01](./pic/organ_handson10.png)

- Policies

![organ_handson01](./pic/organ_handson11.png)

- SCP

![organ_handson01](./pic/organ_handson12.png)

- By default, SCP has `FULLAWSAccess` policy.

![organ_handson01](./pic/organ_handson13.png)

- Create policy

![organ_handson01](./pic/organ_handson14.png)

![organ_handson01](./pic/organ_handson15.png)

![organ_handson01](./pic/organ_handson16.png)

- Policies hierarchy (subOU)

![organ_handson01](./pic/organ_handson16.png)

![organ_handson01](./pic/organ_handson17.png)

![organ_handson01](./pic/organ_handson18.png)

- Attach policy

![organ_handson01](./pic/organ_handson19.png)

![organ_handson01](./pic/organ_handson20.png)

![organ_handson01](./pic/organ_handson21.png)

---

[TOP](#aws---organizations)
