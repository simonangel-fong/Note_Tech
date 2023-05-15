# AWS - Networking

[Back](../index.md)

- [AWS - Networking](#aws---networking)
  - [Networking](#networking)
    - [IP](#ip)
    - [VPC \& Subnets](#vpc--subnets)
    - [Internet Gateway \& NAT Gateways: access Internet](#internet-gateway--nat-gateways-access-internet)
    - [`Network ACL` \& `Security Groups`: security](#network-acl--security-groups-security)
  - [AWS Network Technology](#aws-network-technology)
    - [`VPC Flow Logs`: Logging](#vpc-flow-logs-logging)
    - [`VPC Peering` - Connect VPCs, not transitive](#vpc-peering---connect-vpcs-not-transitive)
    - [`VPC Endpoints` - VPC access AWS services](#vpc-endpoints---vpc-access-aws-services)
    - [`AWS PrivateLink` (VPC Endpoint Services) - VPC access 3rd party VPC](#aws-privatelink-vpc-endpoint-services---vpc-access-3rd-party-vpc)
    - [`Site to Site VPN` \& `Direct Connect` - on-premises access AWS](#site-to-site-vpn--direct-connect---on-premises-access-aws)
    - [`Client VPN` - computer openvpn access VPC -\> On-permisses](#client-vpn---computer-openvpn-access-vpc---on-permisses)
    - [`Transit Gateway` - connect thousands](#transit-gateway---connect-thousands)
  - [Summary](#summary)

---

## Networking

![diagram](./pic/networking_diagram.png)

---

### IP

- IP Addresses in AWS
- `IPv4`

  - **Internet Protocol version 4** (4.3 Billion Addresses)
  - **Public IPv4** – can be used on the **Internet**
    - EC2 instance gets a **new a public IP address** every time you stop then start it (default)
  - **Private IPv4**
    - **fixed** for EC2 Instances even if you start/stop them
    - can be used **on private networks (LAN)** such as internal AWS networking (e.g., 192.168.1.1)

- `IPv6`

  - **Internet Protocol version 6** (3.4 × 10!" Addresses)
  - Every IP address is public (**no private range**)

- `Elastic IP`
  - allows you to attach a **fixed public IPv4 address** to EC2 instance
  - **Note**: has **ongoing cost** if not attached to EC2 instance or if the EC2 instance is stopped 占有即收费, 即使不使用

---

### VPC & Subnets

- `Virtual Private Cloud (VPC)`

  - **private network** to deploy your esources (**regional resource**)

  - a logically isolated section of the AWS Network where users launch AWS resources.
  - User chooses a range of IPs using CIDR Range.

- `Subnets`

  - break up a logical partition of an IP network into **multiple smaller network segments**.
  - allow you to **partition your network inside your VPC**(Availability Zone resource)
  - 不同 AZ 不同子网可以构成一个 VPC, 达到 high availability

- `public subnet`

  - a subnet that is **accessible from the internet**

- `private subnet`

  - a subnet that is **not accessible from the internet**

- `Route Tables`
  - used to define **access to the internet and between subnets**

![Subnets](./pic/networking_subnets.png)

---

### Internet Gateway & NAT Gateways: access Internet

- `Internet Gateways`

  - helps our **VPC instances connect with the internet**
  - `Public Subnets` have a **route to the internet gateway**.

- `NAT Gateways` (**AWS-managed**) & `NAT Instances` (**self-managed**) allow your **instances in your Private Subnets to access the internet** while remaining private

---

### `Network ACL` & `Security Groups`: security

- `Network Access Control List(Network ACL / NACL)`

  - A **firewall** which **controls traffic from and to subnet**
  - Can have **ALLOW and DENY** rules
  - Are attached at the **Subnet level**
  - Rules only include **IP addresses**
  - **Return traffic** must be explicitly **allowed** by rules, **not stateful**
  - eg.Block a specific IP address known for abuse

- `Security Groups`
  - A **firewall** that **controls traffic to and from an ENI / an EC2 Instance**
  - Can have only **ALLOW** rules
  - Are attached at the **Instance level**
  - Rules include **IP addresses** and other **security groups**
  - **Return traffic** is automatically **allowed**, regardless of any rules, **stateful**
  - eg. allow an EC2 instance access on port 22 for SSH
  - eg. user cannot block a single IP address.

---

## AWS Network Technology

### `VPC Flow Logs`: Logging

- Capture **information about IP traffic** going into your interfaces:

  - **VPC** Flow Logs
  - **Subnet** Flow Logs
  - **Elastic Network Interface** Flow Logs

- Helps to monitor & troubleshoot **connectivity issues**.

  - Example:
    - Subnets to internet
    - Subnets to subnets
    - Internet to subnets

- Captures network information from **AWS managed interfaces** too

  - Elastic Load Balancers,
  - ElastiCache,
  - RDS,
  - Aurora,
  - etc…

- `VPC Flow logs` data can go to **S3, CloudWatch Logs, and Kinesis Data Firehose**

---

### `VPC Peering` - Connect VPCs, not transitive

- **Connect two VPC, privately** using AWS' network
- Make them behave as if they were **in the same network**
- Must **not have overlapping** CIDR (IP address range)
- VPC Peering connection is **not transitive** (must be established for each VPC that need to communicate with one another)

---

### `VPC Endpoints` - VPC access AWS services

- `Endpoints`
  - allow you to connect to _AWS Services_ **using a private network** instead of the public www network
- This gives you enhanced **security and lower latency** to access AWS services

- Types:
  - `VPC Endpoint Gateway`: S3 & DynamoDB
  - `VPC Endpoint Interface`: the rest

---

### `AWS PrivateLink` (VPC Endpoint Services) - VPC access 3rd party VPC

- Most secure & scalable way to expose a service to 1000s of VPCs
- Does not require VPC peering, internet gateway, NAT, route tables…
- Requires a `Network Load Balancer` (Service VPC) and `Elastic Network Interface` (Customer VPC)

---

### `Site to Site VPN` & `Direct Connect` - on-premises access AWS

- `Internet Protocol Security (IPsec)`

  - a **secure network protocol suite** that **authenticates and encrypts the packets** of data to provide secure encrypted communication between two computers over an Internet Protocol network.
  - Used in `AWS VPN`

- `AWS Virtual Private Network (VPN)`

  - allow to establish a secure and private tunnel from **user's network or device** to **the AWS global network**.

- `Site to Site VPN`

  - Connect an **on-premises VPN to AWS**
  - The connection is automatically **encrypted**
  - Goes over the **public** internet

  - On-premises: must use a `Customer Gateway (CGW)`
  - AWS: must use a `Virtual Private Gateway (VGW)`

- `Direct Connect (DX)`

  - Establish a **physical connection** between **on-premises and AWS**
  - The connection is private, secure and fast
  - Goes over a **private** network
  - Takes at least a month to establish

  ![hybred](./pic/networking_hybrid.png)

---

### `Client VPN` - computer openvpn access VPC -> On-permisses

- Connect from your computer **using OpenVPN** to your private network in AWS and on-premises
- Allow you to connect to your EC2 instances **over a private IP** (just **as if you were in the private VPC network**)
- Goes over p**ublic Internet**

Computer with AWS Client VPN (OpenVPN) -> Internet WWW -> AWS VPC -> Site-to-Site VPN -> On-Premises Data Center

---

### `Transit Gateway` - connect thousands

- For having transitive peering between **thousands of VPC and on-premises**, **hub-and-spoke (star) connection**
- **One single Gateway** to provide this functionality
- Works with **Direct Connect Gateway**, **VPN connections**

---

## Summary

- `VPC`
  - Virtual Private Cloud
- `Subnets`

  - **Tied to an AZ**, **network partition** of the VPC

- `Internet Gateway`

  - at the **VPC level**, provide **Internet Access**

- `NAT Gateway / Instances`

  - give **internet access to private subnets**

- `NACL`

  - **Stateless**, **subnet rules** for inbound and outbound

- `Security Groups`

  - **Stateful**, operate at the EC2 **instance level** or ENI

- `VPC Peering`

  - **Connect two VPC** with non overlapping IP ranges, nontransitive

- `Elastic IP`

  - **fixed public IPv4**, **ongoing cost** if not in-use

- `VPC Endpoints`

  - Provide private **access to AWS Services** within VPC

- `PrivateLink`

  - Privately connect to a **service in a 3rd party** VPC

- `VPC Flow Logs`

  - network **traffic logs**

- `Site to Site VPN`

  - VPN over **public internet between on-premises** DC and AWS

- `Client VPN`

  - **OpenVPN** connection from your computer into your VPC

- `Direct Connect`

  - direct private connection to AWS

- `Transit Gateway`

  - **Connect thousands of VPC** and on-premises networks together

---

[TOP](#aws---networking)
