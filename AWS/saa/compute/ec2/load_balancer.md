# AWS Compute - Elatic Load Balancer

[Back](../../index.md)

- [AWS Compute - Elatic Load Balancer](#aws-compute---elatic-load-balancer)
  - [`Elastic Load Balancer`](#elastic-load-balancer)
    - [Load Balancer Security Groups](#load-balancer-security-groups)
    - [Types of load balancer on AWS](#types-of-load-balancer-on-aws)
      - [Classic Load Balancers (v1) 已过时, 不用考](#classic-load-balancers-v1-已过时-不用考)
      - [`Application Load Balancer` (v2)](#application-load-balancer-v2)
        - [Target Groups: http](#target-groups-http)
      - [Hands-On: ALB](#hands-on-alb)
      - [`Network Load Balancer` (v2)](#network-load-balancer-v2)
      - [Hands-On: NLB](#hands-on-nlb)
      - [`Gateway Load Balancer`](#gateway-load-balancer)
    - [Sticky Sessions (Session Affinity)](#sticky-sessions-session-affinity)
        - [Cookie Types and Names](#cookie-types-and-names)
      - [Hands-On: Stickness Cookie](#hands-on-stickness-cookie)
    - [Cross-Zone Load Balancing](#cross-zone-load-balancing)
    - [SSL/TLS](#ssltls)
      - [SSL Certificates](#ssl-certificates)
      - [Server Name Indication (SNI): Certificate](#server-name-indication-sni-certificate)
      - [Hands-on: SSL](#hands-on-ssl)
    - [Connection Draining](#connection-draining)

---

## `Elastic Load Balancer`

- `Load Balancers` are servers that **forward traffic to multiple servers** (e.g., EC2 instances) downstream

- Purpose
  - **Spread load** across multiple downstream instances
  - Expose a **single point of access (DNS)** to your application
  - Seamlessly **handle failures** of downstream instances
  - Do regular **health checks** to your instances
    - When you enable ELB Health Checks, your **ELB won't send traffic** to unhealthy (crashed) EC2 instances.
  - Provide **SSL termination (HTTPS)** for your websites
  - Enforce stickiness with **cookies**
  - High **availability** across zones
  - **Separate** public traffic from private traffic

![diagram](./pic/load_balancer_diagram.png)

---

- An `Elastic Load Balancer` is a **managed load balancer**

  - AWS guarantees that it will be working
  - AWS takes care of upgrades, maintenance, high availability
  - AWS provides only a few configuration knobs

- It **costs less** to setup your own load balancer but it will be a lot more effort on your end

- It is **integrated** with many AWS offerings / services
  - EC2, EC2 Auto Scaling Groups, Amazon ECS
  - AWS Certificate Manager (ACM), CloudWatch
  - Route 53, AWS WAF, AWS Global Accelerator

---

### Load Balancer Security Groups

![load_balancer_sg](./pic/load_balancer_sg.png)

- Load balancer sg accept traffic from anywhere.

![load_balancer_sg](./pic/load_balancer_sg_lb.png)

- EC2 sg accept traffic only from load balancer.

![load_balancer_sg](./pic/load_balancer_sg_ec2.png)

---

### Types of load balancer on AWS

- AWS has 4 kinds of managed Load Balancers

  - `Classic Load Balancer` (v1 - old generation) – 2009 – `CLB`
    - HTTP, HTTPS, TCP, SSL (secure TCP)
  - `Application Load Balancer` (v2 - new generation) – 2016 – `ALB`
    - HTTP, HTTPS, WebSocket
  - `Network Load Balancer` (v2 - new generation) – 2017 – `NLB`
    - TCP, TLS (secure TCP), UDP
  - `Gateway Load Balancer` – 2020 – `GWLB`
    - Operates at layer 3 (Network layer) – IP Protocol

- Overall, it is recommended to use the **newer** generation load balancers as they provide more features
- Some load balancers can be setup as internal (private) or external (public) ELBs

---

#### Classic Load Balancers (v1) 已过时, 不用考

- **Supports**

  - TCP (Layer 4), HTTP & HTTPS (Layer 7)

- **Health checks**:

  - TCP or HTTP based

- **Fixed hostname**
  - XXX.region.elb.amazonaws.com

![clb](./pic/load_balancer_clb.png)

---

#### `Application Load Balancer` (v2)

- Application load balancers is **Layer 7 (HTTP)**
- **Feature**

  - Load balancing to **multiple HTTP applications across machines**(target groups)
  - Load balancing to **multiple applications on the same machine**(ex: containers)

- **Expose**:

  - Application Load Balancers and Classic Load Balancers have a **static DNS name**.

- **Support**

  - `HTTP/2` and `WebSocket`
  - redirects (from `HTTP` to `HTTPS` for example)

- Routing tables to **different target groups** based on:

  - **Url path**:
    - example.com/users & example.com/posts
  - **hostname**:
    - one.example.com & other.example.com
  - **Query String**
    - example.com/users?id=123&order=false
  - **HTTP Headers**

- ALB are a great fit for **micro services** & **container-based application **(example: Docker & Amazon ECS)
- Has a **port mapping** feature to redirect to a dynamic port in ECS
- In comparison, we’d need multiple Classic Load Balancer per application

- **HTTP Based Traffic diagram**:

  ![diagram](./pic/load_balancer_alb_diagram_http.png)

- **Query Strings/Parameters Routing**

  ![diagram](./pic/load_balancer_alb_diagram_query.png)

- **Good to Know**

  - **Fixed hostname** (XXX.region.elb.amazonaws.com)
  - The application servers **don’t see the IP of the client** directly
  - Method to get:
    - **IP of the client**: `X-Forwarded-For` in the header
    - **Port**: `X-Forwarded-For` in the header
    - **Protocal**: `X-Forwarded-Proto` in the header

  ![diagram](./pic/load_balancer_alb_diagram_good_to_know.png)

---

##### Target Groups: http

- Target Group of ALB can be:

  - **EC2 instances** (can be managed by an Auto Scaling Group) – `HTTP`
  - **ECS tasks** (managed by ECS itself) – `HTTP`
  - **Lambda functions** – HTTP request is translated into a **JSON event**
  - **IP Addresses** – must be **private** IPs

- ALB can route to **multiple** target groups
- Health checks are **at the target group level**

- `Health Checks`

  - crucial for Load Balancers
  - They enable the load balancer to know **if instances it forwards traffic to are available to reply to requests**
  - The health check is done on a **port** and a **route** (/health is common)
  - If the response is **not 200 (OK)**, then the instance is **unhealthy**
  - If the instance is unhealthy, ALB stop sending request to this instance.

  ![health_check](./pic/health_check.png)

---

#### Hands-On: ALB

- Create a new sg only allowing http

![sg](./pic/load_balancer_alb_create_newsg.png)

![sg](./pic/load_balancer_alb_create_newsg02.png)

- Create a new target group

![target](./pic/load_balancer_alb_create_new_target_group.png)

- Create ALB

![create](./pic/load_balancer_alb_create.png)

![create](./pic/load_balancer_alb_create_sg.png)

![create](./pic/load_balancer_alb_create_done.png)

- Verify: Uses the DNS name to visit in browser

![create](./pic/load_balancer_alb_create_visit01.png)

![create](./pic/load_balancer_alb_create_visit02.png)

---

- Limit EC2 only access from a ALB, not for public IP of instance.

![create](./pic/load_balancer_alb_create_sg_advanced.png)

- Add Rules: filter request by path and response a fixed message.

![rule](./pic/load_balancer_alb_rule_create.png)

![rule](./pic/load_balancer_alb_rule_add_condition.png)

![rule](./pic/load_balancer_alb_rule_add_condition02.png)

![rule](./pic/load_balancer_alb_rule_add_condition03.png)

![rule](./pic/load_balancer_alb_rule_add_condition04.png)

![rule](./pic/load_balancer_alb_rule_add_condition05.png)

![rule](./pic/load_balancer_alb_rule_add_condition06.png)

![rule](./pic/load_balancer_alb_rule_add_condition07.png)

---

#### `Network Load Balancer` (v2)

- Network load balancers (Layer 4) allow to:

  - Forward **TCP & UDP** traffic to your instances
  - Handle **millions of request** per seconds
  - Less **latency** ~100 ms (vs 400 ms for ALB)

- NLB has **one static IP per AZ**, and supports assigning Elastic IP (helpful for whitelisting specific IP)
  - 考题: app limits access to a few ip
- NLB are used for extreme **performance**, TCP or UDP traffic
- **Not** included in the AWS free tier

- **TCP (Layer 4) Based Traffic**

![rule](./pic/load_balancer_nlb_diagram.png)

- **Target Group**:

  - EC2 instances
  - IP Addresses – must be private IPs
  - **Application Load Balancer**
  - **Health Checks**:
    - TCP,
    - HTTP
    - HTTPS

  ![tg](./pic/load_balancer_nlb_ec2_diagram.png)

  ![tg](./pic/load_balancer_nlb_ip_diagram.png)

  ![tg](./pic/load_balancer_nlb_alb_diagram.png)

---

#### Hands-On: NLB

- Create sg

![sg](./pic/load_balancer_nlb_sg.png)

- Create Target Group

![sg](./pic/load_balancer_nlb_target_group.png)

![sg](./pic/load_balancer_nlb_target_group_health_check.png)

![sg](./pic/load_balancer_nlb_target_group_health_check02.png)

![sg](./pic/load_balancer_nlb_target_group_health_check03.png)

- Create network load balancer

![create](./pic/load_balancer_nlb_create.png)

![create](./pic/load_balancer_nlb_create_sg.png)

![create](./pic/load_balancer_nlb_create_listener_target_group.png)

- Update sg of istances, allowing inboud of NLB

![sg](./pic/load_balancer_nlb_ec2_sg.png)

- Verify

![sg](./pic/load_balancer_nlb_create_done.png)

![sg](./pic/load_balancer_nlb_create_done02.png)

![sg](./pic/load_balancer_nlb_create_done03.png)

---

#### `Gateway Load Balancer`

- Deploy, scale, and manage a fleet of **3rd party network virtual appliances** in AWS
- Example: Firewalls, Intrusion Detection and Prevention Systems, Deep Packet Inspection Systems, payload manipulation, …
- Operates at **Layer 3 (Network Layer) – IP Packets**

- Combines the following functions:

  - `Transparent Network Gateway`:
    - single entry/exit for all traffic
  - `Load Balancer`
    - distributes traffic to your virtual appliances

- Uses the **GENEVE protocol** on port **6081**

- Traffic will hit target group before reach the application.

![sg](./pic/load_balancer_gwlb_diagram.png)

- **Target Group**

  - EC2 instances
  - IP Addresses – must be private IPs

  ![sg](./pic/load_balancer_gwlb_ec2_diagram.png)

  ![sg](./pic/load_balancer_gwlb_ip_diagram.png)

---

### Sticky Sessions (Session Affinity)

- It is possible to implement stickiness so that the **same client** is always **redirected** to the **same instance** behind a load balancer
- This works for `Classic Load Balancer`, `Application Load Balancer`, and `Network Load Balancer`
- For both CLB & ALB, the “cookie” used for stickiness has an expiration date you control
- Use case:
  - make sure the user **doesn’t lose his session data**
- Enabling stickiness may bring imbalance to the load over the backend EC2 instances

![stickiness](./pic/load_balancer_stickiness_diagram.png)

---

##### Cookie Types and Names

- **Application-based Cookies**

  - **Application cookie**

    - Generated by the load balancer
    - Cookie name
      - **AWSALBAPP**

  - **Custom cookie**

    - Generated by the target (application itself)
    - Can include any custom attributes required by the application
    - Cookie name must be **specified individually for each target group**
    - Don’t use **AWSALB**, **AWSALBAPP**, or **AWSALBTG** (reserved for use by the ELB)

- **Duration-based Cookies**
  - Cookie generated by the load balancer
  - Cookie name
    - **AWSALB** for ALB
    - **AWSELB** for CLB

---

#### Hands-On: Stickness Cookie

- Edit target group attributes:

![stickness](./pic/load_balancer_tg_stickiness01.png)

![stickness](./pic/load_balancer_tg_stickiness02.png)

- Visit app always using the same instance, ip address always the same.

![stickness](./pic/load_balancer_tg_stickiness03.png)

---

### Cross-Zone Load Balancing

- Without Cross Zone Load Balancing:
  - Requests are distributed in the instances of the node of the Elastic Load Balancer

![cross_zone](./pic/load_balancer_cross_zone_diagram_without.png)

- With Cross Zone Load Balancing:
  - each load balancer instance **distributes evenly** across all registered instances in all AZ

![cross_zone](./pic/load_balancer_cross_zone_diagram_with.png)

---

- **Application Load Balancer**
  - **Enabled by default** (can be disabled at the Target Group level)
  - **No charges** for inter AZ data

![cz](./pic/load_balancer_alb_cross_zone01.png)

![cz](./pic/load_balancer_alb_cross_zone02.png)

- By default, cross za is enable. But can be change in the target group.

![cz](./pic/load_balancer_alb_cross_zone03.png)

---

- **Network Load Balancer** & **Gateway Load Balancer**
  - **Disabled** by default
    - You pay **charges** ($) for inter AZ data if enabled

![cz](./pic/load_balancer_nlb_cross_az01.png)

![cz](./pic/load_balancer_nlb_cross_az02.png)

---

- **Classic Load Balancer**
  - **Disabled** by default
  - **No charges** for inter AZ data if enabled

---

### SSL/TLS

- An **SSL Certificate** allows traffic between your clients and your load balancer to be **encrypted in transit** (in-flight encryption)

  - `SSL`: `Secure Sockets Layer`, used to **encrypt connections**
  - `TLS`: `Transport Layer Security`, which is a newer version
  - Nowadays, `TLS` certificates are mainly used, but people still refer as `SSL`

- Public SSL certificates are issued by `Certificate Authorities (CA)`
  - Comodo, Symantec, GoDaddy, GlobalSign, Digicert, Letsencrypt, etc…
- SSL certificates have an **expiration date** (you set) and must be renewed

---

#### SSL Certificates

- The load balancer uses an X.509 certificate (SSL/TLS server certificate)
- You can manage certificates using `ACM (AWS Certificate Manager)`
- You can create upload your own certificates alternatively

- **HTTPS listener**:
  - You must specify a default certificate
  - You can add an optional list of certs to support multiple domains
  - Clients can use `SNI (Server Name Indication)` to specify the hostname they reach
  - Ability to specify a security policy to support older versions of SSL / TLS (legacy clients)

![diagram](./pic/load_balancer_ssl_diagram.png)

- **Classic Load Balancer (v1)**

  - Support only one SSL certificate
  - Must use multiple CLB for multiple hostname with multiple SSL certificates

- **Application Load Balancer (v2)**

  - Supports **multiple** listeners with **multiple** SSL certificates
  - Uses Server Name Indication (SNI) to make it work

- **Network Load Balancer (v2)**
  - Supports **multiple** listeners with **multiple** SSL certificates
  - Uses Server Name Indication (SNI) to make it work

---

#### Server Name Indication (SNI): Certificate

- `SNI` solves the problem of loading **multiple SSL certificates** onto one web server (to serve multiple websites)
- Server Name Indication (SNI) allows you to **expose multiple HTTPS applications** each **with its own SSL certificate** on the same listener.
- It’s a “newer” protocol, and requires the client to indicate the hostname of the target server in the initial SSL handshake
- The server will then find the correct certificate, or return the default one
- Note:
  - **Only works for ALB & NLB (newer generation), CloudFront**
  - Does not work for CLB (older gen)

![eni](./pic/load_balancer_ssl_sni_diagram.png)

---

#### Hands-on: SSL

- ALB:

![alb_ssl](./pic/load_balancer_alb_ssl_add01.png)

- Specify target group

![alb_ssl](./pic/load_balancer_alb_ssl_add02.png)

- Specify policy and certificate
  - From ACM
  - From IAM
  - import to ACM

![alb_ssl](./pic/load_balancer_alb_ssl_add03.png)

---

### Connection Draining

- **Feature naming** 在不同的 balancer 中有不同的名称

  - Connection Draining – for CLB
  - Deregistration Delay – for ALB & NLB

- **Connection Draining**

  - **Give time to complete** “in-flight requests” while the instance is de-registering or unhealthy
  - **Stops sending new requests** to the EC2 instance which is de-registering

- Parameterize
  - Between 1 to 3600 seconds (default: 300 seconds)
  - Can be disabled (set value to 0)
  - Set to a low value if your requests are short

![alb_ssl](./pic/load_balancer_draining_diagram.png)

---

[Top](#aws-compute---elatic-load-balancer)
