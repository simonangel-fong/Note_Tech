# AWS - API Gateway

[Back](../../index.md)

- [AWS - API Gateway](#aws---api-gateway)
  - [`AWS API Gateway`](#aws-api-gateway)
    - [API Type](#api-type)
    - [Integrations High Level](#integrations-high-level)
    - [Endpoint Types](#endpoint-types)
    - [Security](#security)
  - [Use Case](#use-case)
    - [Building a Serverless API](#building-a-serverless-api)
    - [Kinesis Data Streams](#kinesis-data-streams)
  - [Hands-on](#hands-on)

---

## `AWS API Gateway`

- `AWS Lambda` + `API Gateway`: **No infrastructure to manage**

- Support for the `WebSocket Protocol`
- Handle API **versioning** (v1, v2…)
- Handle **different environments** (dev, test, prod…)
- Handle **security** (Authentication and Authorization)
- Create `API keys`, handle request **throttling**
- Swagger / Open API import to quickly define APIs
- **Transform** and **validate** requests and responses
- Generate SDK and API specifications
- **Cache** API responses

---

### API Type

- **HTTP API**

  - Build low-latency and cost-effective `REST APIs` with built-in features such as `OIDC` and `OAuth2`, and native `CORS` support

- **WebSocket API**

  - Build a WebSocket API using persistent connections for **real-time** use cases such as **chat applications** or **dashboards**.

- **REST API**

  - Develop a `REST API` where you gain **complete control** over the **request** and **response** along with API management capabilities.

- **REST API Private**
  - Create a `REST API` that is **only accessible from within a VPC**.

---

### Integrations High Level

- `Lambda Function`

  - Invoke Lambda function
  - **Easy** way to expose `REST API` backed by `AWS Lambda`

- **HTTP**

  - Expose `HTTP endpoints` in the backend
  - Example:
    - internal `HTTP API` **on premise**,
    - `Application Load Balancer`…
  - Why? Add rate limiting, caching, user authentications, API keys, etc…

- **AWS Service**
  - Expose any `AWS API` through the `API Gateway`
  - Example:
    - start an `AWS Step Function` workflow,
    - post a message to `SQS`
  - Why? Add authentication, deploy publicly, rate control…

---

### Endpoint Types

- **Edge-Optimized (default)**:

  - For **global** clients
  - Requests are **routed** through the `CloudFront Edge` locations (improves **latency**)
  - The `API Gateway` still **lives** in **only one region**

- **Regional**:

  - For clients within the **same region**
  - Could manually combine with `CloudFront` (more control over the caching strategies and the distribution)

- **Private**:
  - Can **only** be **accessed** from your `VPC` using an `interface VPC endpoint (ENI)`
  - Use a **resource policy** to define access


- Sample:
  - When you are using an Edge-Optimized API Gateway, your API Gateway lives in CloudFront Edge Locations across all AWS Regions.
    - An Edge-Optimized API Gateway is best for geographically **distributed clients**. API requests are **routed** to the nearest CloudFront Edge Location which improves latency. The API Gateway **still lives in one AWS Region.**

---

### Security

- **User Authentication** through

  - `IAM Roles` (useful for **internal applications**)
  - `Cognito` (identity for **external users** – example **mobile** users)
  - **Custom Authorizer** (your own logic)

- **Custom Domain Name HTTPS** security through integration with `AWS Certificate Manager (ACM)`

  - If using **Edge-Optimized** endpoint, then the **certificate** must be in `us-east-1`
  - If using **Regional** endpoint, the **certificate** must be in the `API Gateway` **region**
  - Must setup `CNAME` or `A-alias` record in `Route 53`

---

## Use Case

### Building a Serverless API

![gateway_example](./pic/gateway_example.png)

---

### Kinesis Data Streams

![gateway_example02.png](./pic/gateway_example02.png)

---

## Hands-on

- Create Lambda

![gateway_handson09](./pic/gateway_handson09.png)

- update code and deploy

![gateway_handson10](./pic/gateway_handson10.png)

```py
import json

def lambda_handler(event, context):
    body = "Hello from Lambda!"
    statusCode = 200
    return {
        "statusCode": statusCode,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json"
        }
    }
```

![gateway_handson11](./pic/gateway_handson11.png)

- API Type

![gateway_handson01](./pic/gateway_handson01.png)

![gateway_handson02](./pic/gateway_handson02.png)

![gateway_handson03](./pic/gateway_handson03.png)

- Endpoint Type

![gateway_handson05](./pic/gateway_handson05.png)

- Create API

![gateway_handson04](./pic/gateway_handson04.png)

![gateway_handson06](./pic/gateway_handson06.png)

- Create API Method

![gateway_handson06](./pic/gateway_handson07.png)

![gateway_handson08](./pic/gateway_handson08.png)

![gateway_handson08](./pic/gateway_handson12.png)

- Lambda has been integrate

![gateway_handson08](./pic/gateway_handson13.png)

- lambda policy has been updated

![gateway_handson08](./pic/gateway_handson14.png)

- Test API

![gateway_handson08](./pic/gateway_handson15.png)

![gateway_handson08](./pic/gateway_handson16.png)

- Create resource
  - then create new lambda function to be integrated.

![gateway_handson08](./pic/gateway_handson17.png)

![gateway_handson08](./pic/gateway_handson18.png)

- Deploy API

![gateway_handson08](./pic/gateway_handson19.png)

![gateway_handson08](./pic/gateway_handson20.png)

![gateway_handson08](./pic/gateway_handson21.png)

- Test in browser

![gateway_handson08](./pic/gateway_handson22.png)

![gateway_handson08](./pic/gateway_handson23.png)

---

[TOP](#aws---api-gateway)
