# AWS - EC2

[Back](../index.md)

- [AWS - EC2](#aws---ec2)
  - [Amazon EC2](#amazon-ec2)
  - [EC2 sizing \& configuration options](#ec2-sizing--configuration-options)
  - [EC2 User Data](#ec2-user-data)
    - [Hands-on](#hands-on)
  - [EC2 Instance Types](#ec2-instance-types)
  - [Security Groups](#security-groups)
  - [SSH](#ssh)
  - [EC2 Instance Connect](#ec2-instance-connect)
  - [Attach aws role to EC2 instance](#attach-aws-role-to-ec2-instance)
  - [Purchasing Options](#purchasing-options)
    - [On Demand](#on-demand)
    - [EC2 Reserved Instances](#ec2-reserved-instances)
      - [Hands-on](#hands-on-1)
    - [Savings Plans](#savings-plans)
    - [Spot Instances](#spot-instances)
    - [Dedicated Hosts](#dedicated-hosts)
    - [Dedicated Instances](#dedicated-instances)
    - [Capacity Reservations](#capacity-reservations)
    - [Right Option](#right-option)
  - [Spot Instance Requests](#spot-instance-requests)
    - [Hand-on](#hand-on)
  - [Spot Fleets](#spot-fleets)
    - [Hands-on](#hands-on-2)

---

## Amazon EC2

- `Amazon EC2`:
  - `Elastic Compute Cloud`
  - Infrastructure as a Service

- It mainly consists in the capability of :
  - Renting virtual machines (EC2)
  - Storing data on virtual drives (EBS)
  - Distributing load across machines (ELB)
  - Scaling the services using an auto-scaling group (ASG)

---

## EC2 sizing & configuration options


- **Operating System (OS)**: Linux, Windows or Mac OS
- How much **compute power & cores (CPU)**
- How much **random-access memory (RAM)**
- How much **storage** space:
  - Network-attached (EBS & EFS)
  - hardware (EC2 Instance Store)
- **Network card**: speed of the card, Public IP address
- **Firewall rules**: security group
- **Bootstrap script** (configure at first launch): EC2 User Data 

---

## EC2 User Data

- It is possible to **bootstrap** our instances using an EC2 User data script.
- `bootstrapping`:
  - **launching commands** when a machine starts
  - That script is only run once **at the instance first start**


- EC2 user data is used to automate boot tasks such as:
  - Installing updates
  - Installing software
  - Downloading common files from the internet
  - Anything you can think of
- The EC2 User Data Script runs with the **root user**. (script can skip `sudo`)

### Hands-on

- Create an EC2 as a linux server using user data

```sh
#!/bin/bash
# Use this for your user data (script from top to bottom)
# install httpd (Linux 2 version)
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello World from $(hostname -f)</h1>" > /var/www/html/index.html
```

---

## EC2 Instance Types

- Naming convention: `[instance_class][generation].[size]`
  - eg: `m5.2xlarge`, `t2.micro`
 
- different types of EC2 instances that are optimised for different use cases
  - ref: https://aws.amazon.com/ec2/instance-types/

| Type              | Feature                                                  | Use Case            | Example |
| ----------------- | -------------------------------------------------------- | ------------------- | ------- |
| General Purpose   | for a diversity of workloads                             | web servers         | `t2`    |
| Compute Optimized | for compute-intensive tasks                              | ML, Gaming server   | `C6g`   |
| Memory Optimized  | for workloads that process large data sets in memory     | In-memory databases | `R5`    |
| Storage Optimized | for intensive access to large data sets on local storage | OLTP                | `I3`    |

---

## Security Groups

- `Security Groups`
  - acts as a “firewall” on EC2 instances that control how traffic is allowed into or out of an EC2 Instances.
  - only contain rules
  - can reference by IP or by security group
  - Does live “outside” the EC2 – if traffic is blocked the EC2 instance won’t see it
  - It’s good to maintain one separate security group for SSH access

- They regulate: 
  - Access to Ports 
  - Authorised IP ranges - IPv4 and IPv6 
  - Control of **inbound network** (from other to the instance) 
    - All **inbound** traffic is **blocked by default**
  - Control of **outbound network** (from the instance to other)
    - All **outbound** traffic is **authorised by default**

- SG can be attached to multiple instances; An instance can have multiple SG.

- SG Locked down to a region / VPC combination
  - SG is not effect in different region or VPC

- Troubleshooting:
  - If your application is not accessible (`time out`), then it’s a security group issue
  - If your application gives a “`connection refused`“ error, then it’s an application error or it’s not launched

- Classic Ports

| Port   | Protocol                             | Use case                       |
| ------ | ------------------------------------ | ------------------------------ |
| `22`   | SSH (Secure Shell)                   | log into a Linux instance      |
| `22`   | SFTP (Secure File Transfer Protocol) | upload files using SSH         |
| `21`   | FTP (File Transfer Protocol)         | upload files into a file share |
| `80`   | HTTP                                 | access unsecured websites      |
| `443`  | HTTPS                                | access secured websites        |
| `3389` | RDP (Remote Desktop Protocol)        | log into a Windows instance    |

- `0.0.0.0/0`: any IPv4
- `::/0`: any IPv4

![sg_inbound](../ec2/pic/sg_inbound.png)

---

## SSH

- `SSH`: `Secure Shell` or `Secure Socket Shell`
  - a network **protocol** that gives users, particularly system administrators, **a secure way to access** a computer over an unsecured network.

- `ssh -i pem_file hostname@public_ip`

---

## EC2 Instance Connect

- Connect to your EC2 instance within your browser
- No need to use your key file that was downloaded
- The “magic” is that a temporary key is uploaded onto EC2 by AWS
- Works only out-of-the-box with Amazon Linux 2
- **Need to make sure the port 22** is still opened!

---

## Attach aws role to EC2 instance

- After create an instance

![role](./pic/role.png)

- Result: 
  - Security: instance can access aws services without keep access key in the instance.

![role](./pic/apply_role.png)

---

## Purchasing Options

| Option                                                  | Feature                                                    |
| ------------------------------------------------------- | ---------------------------------------------------------- |
| On-Demand Instances                                     | short workload, predictable pricing, pay by second         |
| Reserved (1 & 3 years) - Reserved                       | long workloads                                             |
| Reserved (1 & 3 years) - Convertible Reserved Instances | long workloads with flexible instances                     |
| Savings Plans (1 & 3 years)                             | commitment to an amount of usage, long workload            |
| Spot Instances                                          | short workloads, cheap, can lose instances (less reliable) |
| Dedicated Hosts                                         | book an entire physical server, control instance placement |
| Dedicated Instances                                     | no other customers will share your hardware                |
| Capacity Reservations                                   | reserve capacity in a specific AZ for any duration         |

---

### On Demand

- Pay for what you use:
  - Linux or Windows - billing per second, after the first minute
  - All other operating systems - billing per hour
- Has the **highest cost** but **no upfront payment**
- No long-term commitment
- Recommended for** short-term** and **un-interrupted workloads**, where you can't predict how the application will behave 

---

### EC2 Reserved Instances

- Up to 72% **discount** compared to On-demand
- You reserve a specific **instance attributes** (Instance Type, Region, Tenancy, OS)
- Reservation **Period** 
  - 1 year (+discount)
  - 3 years (+++discount)

- **Payment** Options 
  - No Upfront (+), 
  - Partial Upfront (++), 
  - All Upfront (+++)

- Reserved Instance’s **Scope** 
  - Regional
  - Zonal (reserve capacity in an AZ)

- **Recommended** 
  - for **steady-state usage applications** (think database)

- You can buy and sell in the **Reserved Instance Marketplace**

- **Convertible Reserved Instance**
  - Can **change** the EC2 instance type, instance family, OS, scope and tenancy
  - Up to 66% discount

#### Hands-on

![reserve_instance](./pic/reserve_instance.png)

---

### Savings Plans

- Get a discount based on **long-term usage** (up to 72% - same as RIs)
- Commit to a **certain type of usage** ($10/hour for 1 or 3 years)
- Usage beyond EC2 Savings Plans is billed at the **On-Demand price**
- **Locked** to a specific instance family & AWS region (e.g., M5 in us-east-1)
- **Flexible** across:
  - Instance Size (e.g., m5.xlarge, m5.2xlarge)
  - OS (e.g., Linux, Windows)
  - Tenancy (Host, Dedicated, Default)

- Hands-on

![ec2_saving_plan](./pic/ec2_saving_plan.png)

- will redirect to Cost management

![saving_plan_compute](./pic/saving_plan_compute.png)

---

### Spot Instances

- Can get a **discount of up to 90%** compared to On-demand. Most discount
- Instances that you **can “lose”** at any point of time if your max price is less than the current spot price
- The **MOST cost-efficient instances** in AWS
- Useful for workloads that are **resilient to failure**
  - Batch jobs
  - Data analysis
  - Image processing
  - Any distributed workloads
  - Workloads with a flexible start and end time

- **Not suitable for critical jobs or databases**

---

### Dedicated Hosts

- A **physical server** with EC2 instance capacity **fully dedicated** to your use
- Allows you **address compliance requirements** and use your existing server-bound software **licenses** (per-socket, per-core, pe—VM software licenses)
- Purchasing Options:
  - On-demand – pay per second for active Dedicated Host
  - Reserved - 1 or 3 years (No Upfront, Partial Upfront, All Upfront)

- The **most expensive** option

- Useful
  - for software that have complicated **licensing** model (BYOL – Bring Your Own License)
  - for companies that have strong regulatory or **compliance** needs

- Hands-on

![Allocate_Dedicated_Host](./pic/Allocate_Dedicated_Host.png)

---

### Dedicated Instances

- Instances run on **hardware** that’s dedicated to you
- May **share** hardware with other instances **in same account**
- No control over instance placement (can move hardware after Stop / Start)

---

### Capacity Reservations

- Reserve On-Demand instances capacity **in a specific AZ** for **any duration**
  - You always have access to EC2 capacity when you need it
- No time commitment (create/cancel anytime), no billing discounts
- Combine with Regional Reserved Instances and Savings Plans to benefit from billing discounts
- You’re charged at **On-Demand rate** whether you **run instances or not**
- Suitable for short-term, uninterrupted workloads that needs to be in a specific AZ

![Capacity_Reservation](./pic/Capacity_Reservation.png)

---

### Right Option

- Spot instances: the hotel allows people to **bid for the empty rooms** and the highest bidder keeps the rooms. You can get kicked out at any time
- On demand: coming and staying in resort whenever we like, we pay the **full** price
- Reserved: like **planning ahead** and if we plan to stay **for a long time**, we may get a good discount.
- Savings Plans: pay **a certain amount** per hour **for certain period** and stay in any room **type** (e.g., King, Suite, Sea View, …)
- Capacity Reservations: you **book a room for a period** with full price even you don’t stay in it
- Dedicated Hosts: We book an **entire** building of the resort

---

## Spot Instance Requests

- Can get a **discount of up to 90%** compared to On-demand
- Define **max spot price** and get the instance while current spot price < max
  - The hourly spot price varies based on offer and capacity
  - If the current spot price > your max price you can choose to **stop or terminate** your instance with a 2 minutes grace period.
- Other strategy: **Spot Block**
  - “block” spot instance during a specified time frame (1 to 6 hours) without interruptions
  - In rare situations, the instance may be reclaimed

- Used for batch jobs, data analysis, or workloads that are resilient to failures.
- Not great for critical jobs or databases

- terminate Spot Instances:
  - You can only cancel Spot Instance requests that are open, active, or disabled.
  - Cancelling a Spot Request **does not terminate instances**
  - You must **first cancel a Spot Request**, and then terminate the associated Spot Instance

![terminate_spot_instance](./pic/terminate_spot_instance.png)

---

### Hand-on

- `EC2` > `Instances` > `Launch an instance`

![spot_instances](./pic/spot_instances.png)

---

## Spot Fleets

- Spot Fleets allow us to automatically **request Spot Instances with the lowest price**

- `Spot Fleets`
  - **set** of Spot Instances + (optional) On-Demand Instances
- The Spot Fleet will try to meet the target capacity with **price constraints**
  - Define possible **launch pools**: instance type (m5.large), OS, Availability Zone
  - Can have multiple launch pools, so that the fleet can choose
  - Spot Fleet stops launching instances when reaching capacity or max cost


- **Strategies** to allocate Spot Instances:
  - **lowestPrice**: from the pool with the **lowest price** (cost optimization, short workload)
  - **diversified**: distributed across **all pools** (great for availability, long workloads)
  - **capacityOptimized**: pool with the **optimal capacity** for the number of instances
  - **priceCapacityOptimized** (recommended): pools with **highest capacity** available, then select the pool with the **lowest price** (best choice for most workloads)

---

### Hands-on

- `EC2` > `Spot requests` > `Request Spot Instances`

![spot_req](./pic/spot_req.png)

![spot_Instance_pricing_history](./pic/spot_Instance_pricing_history.png)

![allocation_strategy](./pic/allocation_strategy.png)

---

[TOP](#aws---ec2)