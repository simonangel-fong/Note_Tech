# AIP: AppSync

[Back](../index.md)

- [AIP: AppSync](#aip-appsync)
  - [AppSync](#appsync)

---

## AppSync

- `AWS AppSync`
  - a fully managed, `serverless` **GraphQL and real-time event API service** from Amazon Web Services.

- Features:
  - **Unified Data Access**:
    - Lets client apps fetch, modify, and combine data **from multiple databases** (like Amazon DynamoDB or Amazon Aurora), **microservices**, **HTTP APIs**, and **AI models** through **a single GraphQL endpoint**.
  - **Real-Time Subscriptions & Events**:
    - Powers **live updates** (such as chat messages, live scores, or stock tickers) using `serverless WebSockets` via AWS AppSync Events.
  - `API Federation`:
    - Combines **multiple** individual GraphQL APIs **into a single, unified "super graph" managed centrally**.
  - **Business Logic & Resolvers**:
    - Lets you write custom data-mapping logic and business rules using JavaScript or TypeScript directly at the API layer.

---

- Connects apps and services to **data and events**
  - `GraphQL` and `Pub/Sub API’s`
    - GraphQL is what it sounds like – **Graph query language**
    - Can **retrieve data** from **different sources** and return it as a graph
    - Developed by Facebook
  - `Serverless`
  - `JavaScript` / `TypeScript` **support** for business logic

- **GenAI applications**
  - Integrate `Lambda` with `AppSync` resolvers **for realtime FM inference**
  - **Transform** `GraphQL` requests to **model inputs** using `Apache Velocity Template Language (VTL)` mapping
  - `VTL` is just what AppSync uses **under the hood** to translate GraphQL requests to your data source
