# AWS - Lambda

[Back](../index.md)

- [AWS - Lambda](#aws---lambda)
  - [Lambda](#lambda)
    - [Core Features](#core-features)
    - [Pricing Model](#pricing-model)
  - [Invocation Types](#invocation-types)

---

## Lambda

- `AWS Lambda`
  - a **serverless, event-driven compute service** that runs code **without provisioning or managing servers**.
  - It is the core of "`Functions-as-a-Service`" (`FaaS`) on AWS, designed to execute logic only when triggered by a specific event.

- **Limits**
  - **Timeout**: A single execution cannot exceed 15 minutes.
  - **Ephemeral Storage**: You get between 512 MB and 10 GB of temporary /tmp space.
  - **Payload Size**: Requests and responses are limited to 6 MB for synchronous calls.

- **Comparison Table: EC2 vs. ECS vs. EKS vs. Lambda**

| Feature             | EC2 (Virtual Machines)                       | ECS (Docker / AWS Native)     | EKS (Managed Kubernetes)  | Lambda (Serverless)                |
| ------------------- | -------------------------------------------- | ----------------------------- | ------------------------- | ---------------------------------- |
| Abstraction Level   | Infrastructure as a Service (IaaS)           | Container as a Service (CaaS) | Managed Kubernetes (K8s)  | Function as a Service (FaaS)       |
| Management Overhead | OS patching and scaling                      | manage the containers.        | Requires K8s expertise    | Zero server management             |
| Scaling             | Slow(Minutes to spin up)                     | Fast(Seconds to start)        | Fast(Seconds)             | Instant(Millisecond scaling)       |
| Cost Model          | hourly/second                                | resources (vCPU/RAM)          | cluster + nodes/resources | per request+execution duration     |
| Max Runtime         | Unlimited.                                   | Unlimited.                    | Unlimited.                | 15 Minutes.                        |
| Best For            | Legacy apps, custom OS, high-performance HPC | Microservices                 | Complex microservices     | Event-driven/Unpredictable demand. |

---

### Core Features

- **Serverless Execution**:
  - don't manage the underlying OS, patching, or scaling.
  - AWS **handles the entire compute lifecycle**.
- **Event-Driven Model**:
  - Functions are **triggered automatically** by over 200 AWS services (e.g., an S3 file upload, a DynamoDB update, or an API Gateway request).
- **Instant Scaling**:
  - Lambda **scales** precisely with the size of the workload, from zero to thousands of concurrent executions in seconds.
- **Flexible Runtimes**:
  - Natively supports Python, Node.js, Java, Go, C#, Ruby, and PowerShell.
  - can also bring custom runtimes or package the code as a `Docker container image` (up to 10 GB).
- **Security & Isolation**:
  - Every function **runs in a dedicated Firecracker micro-VM**, providing **hardware-level isolation** between different functions and accounts.
- **Performance Optimization**:
  - `SnapStart`: Dramatically reduces "cold start" times (initialization latency) for Java, Python, and .NET.
  - **Provisioned Concurrency**:
    - **Keeps** a specified number of functions **"warm"** and ready to respond instantly for latency-critical apps.
  - **Graviton2 Support**: Allows you to run functions on **ARM-based processors** for up to 34% better price-performance.

---

### Pricing Model

- Lambda follows a `pay-as-you-go model` where you only pay for what you use.

| Component | Description                                                                                                      |
| --------- | ---------------------------------------------------------------------------------------------------------------- |
| Requests  | $0.20 per 1 million requests (after the 1M free monthly requests).                                               |
| Duration  | Charged based on the time it takes for your code to execute (billed per 1ms) and the amount of memory allocated. |
| Memory    | You can allocate between 128 MB and 10 GB. CPU power scales proportionally with memory.                          |

---

## Invocation Types

| Invocation Type      | Model            | Example Service        | Behavior                                                   |
| -------------------- | ---------------- | ---------------------- | ---------------------------------------------------------- |
| Synchronous          | Request/Response | API Gateway, ALB       | Caller waits for the function to finish.                   |
| Asynchronous         | Event            | S3, SNS, EventBridge   | the event in an internal queue and returns a 202 Accepted. |
| Event Source Mapping | Polling          | SQS, Kinesis, DynamoDB | Lambda service polls, batches, and pushes to function.     |
