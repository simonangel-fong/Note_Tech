# AWS Networking - Flow Logs

[Back](../index.md)

- [AWS Networking - Flow Logs](#aws-networking---flow-logs)
  - [VPC Flow Logs](#vpc-flow-logs)
    - [Syntax](#syntax)
    - [Troubleshoot SG \& NACL issues](#troubleshoot-sg--nacl-issues)
    - [Architectures](#architectures)
    - [Hands-on](#hands-on)

---

## VPC Flow Logs

![flow_log_diagram](./pic/flow_log_diagram.png)

- Capture **information about IP traffic** going into your interfaces:

  - **VPC** Flow Logs
  - **Subnet** Flow Logs
  - **Elastic Network Interface (ENI)** Flow Logs

- Helps to **monitor & troubleshoot** connectivity issues
- Flow logs data can go to `S3`, `CloudWatch Logs`, and `Kinesis Data Firehose`
- Captures network information from **AWS managed interfaces** too:

  - ELB, RDS, ElastiCache, Redshift, WorkSpaces, NATGW, Transit Gateway…

- Sample:
  - How can you capture information about IP traffic inside your VPCs?
    - Enable VPC Flow Logs
    - Traffic Mirroring is copying.

---

### Syntax

![flow_log_syntax](./pic/flow_log_syntax.png)

- `srcaddr` & `dstaddr` – help identify problematic **IP**
- `srcport` & `dstport` – help identity problematic **ports**
- `Action` – success or failure of the **request** due to Security Group / NACL
- Can be used for analytics on **usage patterns**, or **malicious behavior**
- **Query** VPC flow logs using `Athena` on `S3` or `CloudWatch Logs Insights`
- Flow Logs examples: https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs- records-examples.html

---

### Troubleshoot SG & NACL issues

- Look at the `ACTION` field

- Incoming Requests
  - Inbound `REJECT` => `NACL` or `SG`
  - Inbound `ACCEPT`, Outbound `REJECT` => `NACL` (stateless, sg=stateful)

![flow_log_incoming_requests](./pic/flow_log_incoming_requests.png)

- Outgoing Requests
  - Outbound `REJECT` => `NACL` or `SG`
  - Outbound `ACCEPT`, Inbound `REJECT` => `NACL`(stateless, sg=stateful)

![flow_log_outgoing_requests](./pic/flow_log_outgoing_requests.png)

---

### Architectures

- Top-10:
  - CloudWatch + Contributor

![flow_log_architecture_cloudWatch_contributor](./pic/flow_log_architecture_cloudWatch_contributor.png)

- Alarm + SNS

![flow_log_architecture_cloudWatch_sns](./pic/flow_log_architecture_cloudWatch_sns.png)

- Analysis

![flow_log_architecture_s3_athena](./pic/flow_log_architecture_s3_athena.png)

---

### Hands-on

- Create flow log: s3

![hands-on](./pic/flow_log_handson01.png)

![hands-on](./pic/flow_log_handson02.png)

![hands-on](./pic/flow_log_handson03.png)

![hands-on](./pic/flow_log_handson11.png)

![hands-on](./pic/flow_log_handson12.png)

---

- Analyze using Athena with S3

- Create a bucket for athena

![hands-on](./pic/flow_log_handson14.png)

- Specify the location of Athena's query result

![hands-on](./pic/flow_log_handson15.png)

![hands-on](./pic/flow_log_handson16.png)

- Create Athena table for flow log

  - ref: https://docs.aws.amazon.com/athena/latest/ug/vpc-flow-logs.html
  - Modify location

- Location of URI in the S3 where flow log is stored.

![hands-on](./pic/flow_log_handson17.png)

- Create table

![hands-on](./pic/flow_log_handson18.png)

- Alter table for dates

- URI to replace

![hands-on](./pic/flow_log_handson19.png)

- Alter table

![hands-on](./pic/flow_log_handson20.png)

- Query

![hands-on](./pic/flow_log_handson21.png)

![hands-on](./pic/flow_log_handson22.png)

---

- Create a new role

![hands-on](./pic/flow_log_handson05.png)

![hands-on](./pic/flow_log_handson06.png)

![hands-on](./pic/flow_log_handson07.png)

![hands-on](./pic/flow_log_handson08.png)

- Create a log group in CW

![hands-on](./pic/flow_log_handson09.png)

- Create flow log: cw

![hands-on](./pic/flow_log_handson04.png)

![hands-on](./pic/flow_log_handson10.png)

- In CW logs

![hands-on](./pic/flow_log_handson13.png)

---

[TOP](#aws-networking---flow-logs)
