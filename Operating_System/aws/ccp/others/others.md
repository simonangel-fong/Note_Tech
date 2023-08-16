# AWS - Other AWS services (Rarely)

[Back](../index.md)

- [AWS - Other AWS services (Rarely)](#aws---other-aws-services-rarely)
  - [Desktop](#desktop)
    - [`Amazon WorkSpaces` - Desktop, DaaS, VDI, hybrid](#amazon-workspaces---desktop-daas-vdi-hybrid)
      - [Amazon WorkSpaces–Multiple Regions](#amazon-workspacesmultiple-regions)
    - [`Amazon AppStream 2.0` - app Streaming, web browser](#amazon-appstream-20---app-streaming-web-browser)
      - [Amazon AppStream 2.0 vs WorkSpaces](#amazon-appstream-20-vs-workspaces)
  - [Mobile](#mobile)
    - [`AWS Amplify` - Beanstalk like suit for mobile app, full stack](#aws-amplify---beanstalk-like-suit-for-mobile-app-full-stack)
    - [`AWS Device Farm` - test app, configure device settings](#aws-device-farm---test-app-configure-device-settings)
    - [`AWS IoT Core` - internet-connected devices](#aws-iot-core---internet-connected-devices)
    - [`AWS AppSync` - GraphQL, sync data, real-time](#aws-appsync---graphql-sync-data-real-time)
    - [`Amazon Elastic Transcoder` - convert S3 media files](#amazon-elastic-transcoder---convert-s3-media-files)
  - [Sync, Backup, and DR](#sync-backup-and-dr)
    - [`AWS DataSync` - incrementally move data to AWS](#aws-datasync---incrementally-move-data-to-aws)
    - [`AWS Backup` - centrally backups, Cross-Account, Cross-Region](#aws-backup---centrally-backups-cross-account-cross-region)
      - [Disaster Recovery Strategies](#disaster-recovery-strategies)
    - [`AWS Elastic Disaster Recovery (DRS)` - recover into AWS, Continuous protect database](#aws-elastic-disaster-recovery-drs---recover-into-aws-continuous-protect-database)
    - [`AWS Fault Injection Simulator (FIS)` - fault injection experiments,Chaos Engineering](#aws-fault-injection-simulator-fis---fault-injection-experimentschaos-engineering)
  - [Migration](#migration)
    - [`AWS Application Discovery Service` - migration planning](#aws-application-discovery-service---migration-planning)
    - [`AWS Application Migration Service (MGN)` - simplify migration](#aws-application-migration-service-mgn---simplify-migration)
  - [Others](#others)
    - [`AWS Step Functions` - serverless visual workflow](#aws-step-functions---serverless-visual-workflow)
    - [`AWS Ground Station` - satellite, edge](#aws-ground-station---satellite-edge)
    - [`Amazon Pinpoint` - marketing communications service, SMS](#amazon-pinpoint---marketing-communications-service-sms)

---

## Desktop

### `Amazon WorkSpaces` - Desktop, DaaS, VDI, hybrid

- Managed `Desktop as a Service (DaaS)` solution to easily provision **Windows or Linux desktops**
- Great to eliminate management of **on-premise VDI (Virtual Desktop Infrastructure)**
- Fast and quickly scalable to **thousands** of users
- Secured data – integrates with KMS
- Pay-as-you-go service with monthly or hourly rates

#### Amazon WorkSpaces–Multiple Regions

- Closer, less latency

---

### `Amazon AppStream 2.0` - app Streaming, web browser

- Desktop **Application Streaming** Service
- Deliver to any computer, without acquiring, provisioning infrastructure
- The application is delivered from within a **web browser**

#### Amazon AppStream 2.0 vs WorkSpaces

- **Workspaces**

  - Fully managed **VDI and desktop** available
  - The users connect to the VDI and open **native or WAM applications**
  - Workspaces are on-demand or always on

- **AppStream 2.0**
  - **Stream a desktop application to web browsers** (no need to connect to a VDI)
  - Works with any device (that has a **web browser**)
  - Allow to configure an instance type per application type (CPU, RAM, GPU)

---

## Mobile

### `AWS Amplify` - Beanstalk like suit for mobile app, full stack

- A set of tools and services that helps you develop and deploy scalable **full stack web and mobile applications**
- Authentication, Storage, API (REST, GraphQL), CI/CD, PubSub, Analytics, AI/ML Predictions, Monitoring, Source Code from AWS, GitHub, etc…

---

### `AWS Device Farm` - test app, configure device settings

- Fully-managed service that **tests your web and mobile apps** against desktop browsers, real mobile **devices**, and tablets
- Run tests concurrently on multiple devices (speed up execution)
- Ability to **configure device settings** (GPS, language, Wi-Fi, Bluetooth, …)

---

### `AWS IoT Core` - internet-connected devices

- `Internet of Things (IoT)`
  - **the network of internet-connected devices** that are able to collect and transfer data
- `AWS IoT Core` allows you to easily **connect** IoT devices to the AWS Cloud
- **Serverless**, secure & scalable to billions of devices and trillions of messages
- Your applications can communicate with your devices even when they aren’t connected
- Integrates with a lot of AWS services (Lambda, S3, SageMaker, etc.)
- Build IoT applications that gather, process, analyze, and act on **data**

---

### `AWS AppSync` - GraphQL, sync data, real-time

- Store and **sync** data across mobile and web apps in **real-time**
- Makes use of **GraphQL** (mobile technology from Facebook)
- **Client Code** can be generated automatically
- Integrations with DynamoDB / Lambda
- **Real-time** subscriptions
- **Offline data synchronization** (replaces Cognito Sync)
- Fine Grained Security
- `AWS Amplify` can leverage AWS AppSync in the background!

---

### `Amazon Elastic Transcoder` - convert S3 media files

- Elastic Transcoder is used to **convert media files stored in S3** into media files in the formats required by consumer playback **devices** (phones etc..)
- Benefits:
  - Easy to use
  - Highly scalable – can handle large volumes of media files and large file sizes
  - Cost effective – duration-based pricing model
  - Fully managed & secure, pay for what you use

---

## Sync, Backup, and DR

### `AWS DataSync` - incrementally move data to AWS

- Move large amount of data **from on-premises to AWS**
- Can **synchronize** to: Amazon S3 (any storage classes – including Glacier), Amazon EFS, Amazon FSx for Windows
- Replication tasks can be scheduled hourly, daily, weekly
- The replication tasks are **incremental** after the first full load

---

### `AWS Backup` - centrally backups, Cross-Account, Cross-Region

- Fully-managed service to centrally manage and **automate backups** across AWS services
- **On-demand** and **scheduled** backups
- Supports `PITR (Point-in-time Recovery)`
- Retention Periods, Lifecycle Management, Backup Policies, …
- Cross-Region Backup
- Cross-Account Backup (using AWS Organizations)

---

#### Disaster Recovery Strategies

- Backup and Restore

  - S3
  - cheapest

- Pilot Light

  - **Core functions** of the app **Ready to scale**, but **minimal setup**
  - medium

- Warm Standby

  - **full version** of the app, but at **minimum size**
  - high

- Multi-Site / Hot-Site

  - **full version** of the app, at **full size**
  - highest

- Typical DR Setup for Cloud Deployments: **multi-region**

---

### `AWS Elastic Disaster Recovery (DRS)` - recover into AWS, Continuous protect database

- Used to be named “CloudEndure Disaster Recovery”
- Quickly and easily **recover** your physical, virtual, and cloud-based servers into AWS
- Example: protect your most critical databases (including Oracle, MySQL, and SQL Server), enterprise apps (SAP), protect your data from ransomware attacks, …
- Continuous block-level replication for your servers

---

### `AWS Fault Injection Simulator (FIS)` - fault injection experiments,Chaos Engineering

- A fully managed service for running fault injection experiments on AWS workloads
- Based on **Chaos Engineering** – stressing an application by creating disruptive events (e.g., sudden increase in CPU or memory), observing how the system responds, and implementing improvements
- Helps you uncover hidden bugs and performance bottlenecks
- Supports the following AWS services: EC2, ECS, EKS, RDS…
- Use **pre-built templates** that generate the desired disruptions

---

## Migration

### `AWS Application Discovery Service` - migration planning

- Plan migration projects by gathering information about on-premises data centers
- Server utilization data and dependency mapping are important for migrations
- **Agentless Discovery (AWS Agentless Discovery Connector)**
  - VM inventory, configuration, and performance history such as CPU, memory, and disk usage
- **Agent-based Discovery (AWS Application Discovery Agent)**
  - System configuration, system performance, running processes, and details of the network connections between systems
- Resulting data can be viewed within `AWS Migration Hub`

---

### `AWS Application Migration Service (MGN)` - simplify migration

- The “AWS evolution” of CloudEndure Migration, replacing AWS Server Migration Service (SMS)
- Lift-and-shift (rehost) solution which **simplify migrating applications to AWS**
- **Converts** your physical, virtual, and cloud-based servers **to run natively on AWS**
- Supports wide range of platforms, Operating Systems, and databases
- Minimal downtime, reduced costs

---

## Others

### `AWS Step Functions` - serverless visual workflow

- Build **serverless visual workflow** to orchestrate your Lambda functions
- Features: sequence, parallel, conditions, timeouts, error handling, …
- Can integrate with EC2, ECS, On-premises servers, API Gateway, SQS queues, etc
  …
- Possibility of implementing human approval feature
- Use cases: order fulfillment, data processing, web applications, any workflow

---

### `AWS Ground Station` - satellite, edge

- Fully managed service that lets you **control satellite communications**, process data, and scale your satellite operations
- Provides a global network of satellite ground stations near AWS regions
- Allows you to **download satellite data** to your AWS VPC within seconds
- Send **satellite data to S3 or EC2 instance **
- Use cases: weather forecasting, surface imaging, communications, video broadcasts

---

### `Amazon Pinpoint` - marketing communications service, SMS

- Scalable **2-way (outbound/inbound) marketing communications service**
- Supports email, SMS, push, voice, and in-app messaging
- Ability to segment and **personalize** messages with the right content to customers
- Possibility to receive replies
- Scales to billions of messages per day
- Use cases: run campaigns by sending marketing, bulk, transactional SMS messages
- **Versus Amazon SNS or Amazon SES**
  - In SNS & SES you **managed each** message's audience, content, and delivery schedule
  - In Amazon Pinpoint, you create message **templates**, delivery schedules, highly-targeted segments, and full campaigns

---

[TOP](#aws---other-aws-services-rarely)
