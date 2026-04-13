# AWS - API Gateway

[Back](../index.md)

- [AWS - API Gateway](#aws---api-gateway)
  - [API Gateway](#api-gateway)
  - [API Types](#api-types)
  - [API Endpoint Types](#api-endpoint-types)
    - [Edge-Optimized Endpoints](#edge-optimized-endpoints)
    - [Regional Endpoints](#regional-endpoints)
    - [Private Endpoints](#private-endpoints)
  - [Resources](#resources)
    - [Methods](#methods)
    - [Integration Type](#integration-type)
      - [Lambda Proxy Integration](#lambda-proxy-integration)
      - [HTTP Proxy Integration](#http-proxy-integration)
      - [AWS Service Integration](#aws-service-integration)
      - [Lambda Custom (Non-Proxy) Integration](#lambda-custom-non-proxy-integration)
      - [HTTP Custom (Non-Proxy) Integration](#http-custom-non-proxy-integration)
  - [Deployment](#deployment)
    - [Deployment Strategies](#deployment-strategies)
  - [Stage](#stage)
    - [Stage Settings \& Features](#stage-settings--features)
  - [Usage Plans](#usage-plans)
  - [Authentication and Authorization](#authentication-and-authorization)
  - [Prvate API](#prvate-api)

---

## API Gateway

- `API Gateway`:
  - an AWS service for creating, publishing, maintaining, monitoring, and securing **REST, HTTP, and WebSocket APIs** at any scale.

---

## API Types

- `HTTP API`
  - Build **low-latency and cost-effective REST APIs** with built-in features such as OIDC and OAuth2, and native CORS support.
- `WebSocket API`
  - Build a WebSocket API using **persistent connections** for **real-time use cases** such as chat applications or dashboards.
- `REST API`
  - Develop a REST API where you gain **complete control** over the request and response along with **API management capabilities**.
- `REST API (Private)`
  - Create a REST API that is **only accessible from within a VPC**

---

- `REST API` vs `HTTP API`
  - `REST APIs` support **more features** than HTTP APIs, while `HTTP APIs` are designed with **minimal features** and offered at a **lower price**.
- Choose `REST APIs` if you need features such as `API keys`, **per-client throttling**, **request validation**, **AWS WAF integration**, or **private API endpoints**.
  - Choose `HTTP APIs` if you don't need the features included with REST APIs.

---

## API Endpoint Types

- `endpoint type`
  - determines **where the API is physically hosted** and how **traffic is routed** to it.

- Types:
  - `edge-optimized`, `regional`, or `private`, depending on where the majority of **API traffic originates from**.

| Feature              | Edge-Optimized               | Regional                        | Private                    |
| -------------------- | ---------------------------- | ------------------------------- | -------------------------- |
| Publicly Accessible? | Yes                          | Yes                             | No                         |
| Uses CloudFront?     | Yes (AWS-managed)            | No                              | No                         |
| Primary Use Case     | Global public users          | Local region users / Custom CDN | Internal VPC microservices |
| Default Type?        | Yes (for REST APIs)          | No                              | No                         |
| Network Path         | Public → Edge → AWS Backbone | Public → AWS Region             | VPC internal only          |

---

### Edge-Optimized Endpoints

- `Edge-Optimized Endpoints`
  - **default**
  - AWS automatically **creates and manages** a `CloudFront` distribution in front of API.
- How it works:
  - Requests -> nearest `CloudFront` `Point of Presence (PoP)` -> over the optimized `AWS private network` -> **API’s home region**.
- Best for:
  - Geographically distributed users (e.g., a global mobile app).
  -
- **Key Advantage**:
  - Reduced **connection latency** for the **initial TLS handshake** because the client connects to a nearby edge location rather than a distant AWS region.

---

### Regional Endpoints

- `Regional Endpoints`
  - intended for **clients located in the same AWS Region** where the API is deployed.

- **How it works**:
  - Requests -> directly regional `API Gateway` without going through `CloudFront`.

- **Best for:**
  - Reducing latency for **internal AWS callers** (e.g., `EC2` instances or `Lambda` functions **in the same region**).
  - When you want to **manage your own `CloudFront` distribution** or **use a different CDN** (like `Akamai` or `Cloudflare`) to have more control over caching and WAF.
  - If your users are **all in one specific geographic area** near the region, this often performs **better than** `Edge-Optimized` because it avoids the extra hop through the managed CloudFront layer.

---

### Private Endpoints

- `Private Endpoints`
  - **not** accessible from the **public internet** at all.
  - strictly for internal traffic.

- **How it works**:
  - They are accessed via `Interface VPC Endpoints` (`AWS PrivateLink`).
  - Traffic stays **entirely within the AWS network** and never traverses the public internet.

- **Best for:**
  - Internal **microservices**.
  - Secure backend communication **between VPCs**.
  - Applications with strict **compliance** or **security** requirements that forbid public exposure.

- **Configuration**:
  - You must use an API Gateway resource policy to allow specific VPCs or VPC Endpoints to access the API.

---

## Resources

- `REST` architecture treats **every content** as a `resource`.
- These resources can be :
  - Text Files,
  - Html Pages,
  - Images,
  - Videos,
  - or Business Data.

---

### Methods

| Method   | Description                                          |
| -------- | ---------------------------------------------------- |
| `GET`    | **Retrieve** information about the REST API resource |
| `POST`   | **Create** a REST API resource                       |
| `PUT`    | **Update** a REST API resource                       |
| `DELETE` | **Delete** a REST API resource or related component  |

---

### Integration Type

#### Lambda Proxy Integration

- the most popular and **simplest way to connect** to a `Lambda function`.
- **How it works**:
  - API Gateway **passes the entire "raw"** `HTTP request` (headers, query strings, body, and context) to the `Lambda function` as a **single JSON object (the event)**.
- **Response**:
  - The `Lambda function` must return a specific **JSON format** containing the `statusCode`, `headers`, and body.
- **Best for**:
  - Rapid development where you want your code to handle all the routing and logic.

---

#### HTTP Proxy Integration

- Similar to the `Lambda proxy`, but for any publicly accessible `HTTP endpoint`
  - e.g., an EC2 instance, an Application Load Balancer, or even a third-party API.

- **How it works**:
  - API Gateway passes the **entire request** through to the **backend URL without modification**.
- **Best for**:
  - Creating a "wrapper" around an existing legacy API or a microservice to add features like `API Keys` or `Throttling`.

---

#### AWS Service Integration

- allows to **connect API directly** to over 100 `AWS services` without writing a Lambda function in between.
- **How it works**:
  - **map** the **incoming request parameters** to the **action parameters** of an AWS service.
  - e.g., a `POST` request can put a message directly into an `SQS queue` or start a `Step Functions` state machine.
- **Best for**:
  - Improving performance and **reducing costs** by removing unnecessary "glue" code.

---

#### Lambda Custom (Non-Proxy) Integration

- Unlike the proxy version, this **gives full control** over the **data flow** using `Mapping Templates`.
- **How it works**:
  - use `Velocity Template Language (VTL)` to **transform the incoming request** into a specific **format** that your Lambda expects.
  - can define how the `Lambda`'s **output** is transformed back into an HTTP response.
- **Best for**:
  - Legacy code where the `Lambda function` **expects a very specific input** that doesn't match a standard HTTP request.

---

#### HTTP Custom (Non-Proxy) Integration

- Similar to the Lambda Custom integration, but for **HTTP backends**.
- **How it works**:
  - You use `VTL` to **map and transform headers, query parameters, and the payload** before it reaches your backend server.
- **Best for**:
  - Sanitizing or restructuring data before it hits a backend that you cannot easily modify.

---

## Deployment

- `Deployment`
  - a **snapshot** of API configuration.
  - When you make changes to `resources` (like adding a new /users path) or `methods` (changing a GET to a POST), those changes are "saved" but not live until you create a deployment.

- **Immutable Snapshots**:
  - Once a deployment is **created**, that specific version of the configuration cannot be changed.
  - If you update the API, you must create a new deployment.

- **Rollbacks**:
  - Because deployments are snapshots, you can easily "roll back" a stage to a previous deployment if a new update causes issues.

---

### Deployment Strategies

- two main ways to **roll out changes** to stages:
  - `Standard Deployment`
    - simply point `Stage` to a new `Deployment ID`.
    - The change is **near-instant** for all users hitting that stage URL.

  - `Canary Deployments`
    - To minimize risk, you can enable a `Canary` on a `specific stage`.
    - **Traffic Shifting**:
      - You send a small **percentage of traffic** (e.g., 10%) to the new deployment while the rest stays on the old one.
    - **Validation**:
      - You monitor logs and metrics for the canary traffic.
        - If everything looks **good**, you "promote" the canary to full production.
        - If it **fails**, you delete the canary without affecting 90% of your users.

---

## Stage

- `Stage`
  - a **logical reference** to a `deployment`.
  - It provides the **"path" to access your API** and defines its lifecycle state (e.g., dev, test, prod).

- **The URL Structure**:
  - Each stage creates a unique URL: `https://{api-id}.execute-api.{region}.amazonaws.com/{stage-name}/`

- **Stage Variables**:
  - can define **environment-specific variables** here (like a DB endpoint or a Lambda function alias).
  - This allows the same API configuration to point to a "test" database in the dev stage and a "production" database in the prod stage.

---

### Stage Settings & Features

- "operational" configuration for API Stage:
  - **CloudWatch Settings**:
    - Enable detailed logging, set the logging level (INFO, ERROR), and toggle "Data Tracing" to see the full request/response body.
  - **Throttling**:
    - Set "**Rate**" (`requests per second`) and **"Burst" limits** at the stage level to **protect backend from being overwhelmed**.
  - **Caching**:
    - enable an `API cache` for a stage to **reduce the number of calls** made to your integration (like Lambda or RDS), improving **latency** and reducing **costs**.

---

## Usage Plans

- `Usage Plans`
  - use to control who can access the API, how much they can access it, and at what speed.

- **Core Components**
  - `API Stages`:
    - associate the **plan** with specific **stages** (e.g., prod or v1) of one or more APIs.
  - `API Keys`:
    - These are **alphanumeric strings** distributed to customers.
    - The Usage Plan identifies the client **based on** the `key` they provide in the `x-api-key` header.
  - `Throttling` and `Quotas`:
    - These define the "speed limit" and "total volume" allowed for those keys.

- **Use Case**:
  - Differentiate between Basic and Premium Customers

---

| Feature      | Throttling                               | Quota                                              |
| ------------ | ---------------------------------------- | -------------------------------------------------- |
| Primary Goal | Protect backend stability                | Enforce business/billing limits                    |
| Metrics      | Requests per second (RPS)                | Total requests per period                          |
| Error Code   | `429` Too Many Requests                  | `429` Too Many Requests                            |
| Reset Logic  | Refills continuously (millisecond level) | Resets at the start of the period (day/week/month) |

- `Throttling`
  - Speed Limit
  - protects your backend from sudden spikes in traffic.
  - It uses a Token Bucket Algorithm.
    - `Rate`: The **average number** of `requests per second (RPS)` allowed over a long period.
    - `Burst`: The **maximum number** of concurrent requests the API can handle at a single moment (the "bucket size").
  - e.g., If your Rate is 100 but your Burst is 150, a user can send 150 requests in one millisecond, but they will then be limited to 100 per second until the bucket refills.

- `Quotas`
  - Data Cap
  - used for business logic, such as **subscription tiers** (e.g., "Free tier gets 1,000 calls per month").
    - `Limit`: The **total number** of requests allowed in a given time period.
    - `Period`: Day, Week, or Month.
  - e.g., Once a user hits 5,000 requests in a month, API Gateway will return a 429 Too Many Requests error until the next month begins

---

## Authentication and Authorization

- `IAM`
  - Authentication: `IAM role`
  - Authorization: `IAM policy`
  - Use case:
    - Enable API requests come from internal AWS services
    - Cross Account Access

- `Cognito`
  - Authentication: `Cognit User Pool`
  - Authorization: `API Gateway Methods`
  - Use case:
    - Enable external users for apps

- `Lambda Authorizer`
  - Authentication: External
  - Authorization: `Lambda Function`
  - Use Case:
    - Use Third Party Identity Provider, e.g., OAuth 2.0

---

## Prvate API

- `Private API`
  - an endpoint that is **not** accessible from the **public internet**.
  - designed to be **accessible only from within** `Amazon VPC` (`Virtual Private Cloud`) or from **on-premises networks** connected to your VPC via `Direct Connect` or `VPN`.

- **How it Works**:
  - Private APIs rely on `Interface VPC Endpoints` powered by `AWS PrivateLink`.
    - **VPC Endpoint**:
      - create an **interface endpoint** for API Gateway (`com.amazonaws.region.execute-api`) inside the VPC.
      - This places an `Elastic Network Interface (ENI)` with a private IP address into your subnets.
    - **Traffic Flow**:
      - a client (like an EC2 instance or a Lambda function) calls the API -> `AWS private network` -> `VPC endpoint` -> `API Gateway`

- **Methods to call a private API**

| Method                | URL Structure                                                           | Description                                                                            |
| --------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Private DNS**       | `https://{api-id}.execute-api.{region}.amazonaws.com/{stage}`           | "Standard URL works inside the VPC if ""Private DNS"" is enabled on the VPC Endpoint." |
| **Route 53 Alias**    | `https://api.yourdomain.com`                                            | create a custom domain name that aliases to the VPC endpoint.                          |
| **Endpoint-Specific** | `https://{api-id}-{vpce-id}.execute-api.{region}.amazonaws.com/{stage}` | Useful if need to target a specific VPC endpoint directly.                             |
