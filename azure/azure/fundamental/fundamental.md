# Azure Fundamental

[Back](../index.md)

- [Azure Fundamental](#azure-fundamental)
  - [Shared Responsibility Model](#shared-responsibility-model)
  - [Cloud Pricing](#cloud-pricing)
  - [Cloud Service Types](#cloud-service-types)
  - [Regions](#regions)

---

## Shared Responsibility Model

- `Azure shared responsibility model`
  - a framework dividing security and operational duties.
  - `Microsoft` manages the **physical infrastructure** ("security of the cloud")
  - `customer` is responsible for **everything they build, deploy, and manage ("security in the cloud").**

- **Customer**'s Responsibilities
  - **Data**: Classification, protection, and encryption policies.
  - **Endpoints**: Security and compliance of client devices, laptops, and mobile devices.
  - **Accounts**: Managing user identities, access controls, Multi-Factor Authentication (MFA), and Role-Based Access Control (RBAC).

- **Microsoft’s** Responsibility
  - Microsoft secures the **underlying cloud infrastructure**. This includes:
    - **Physical Security**: Managing access to physical datacenters, cooling, power, and environmental controls.
    - **Physical Network**: Managing switches, routers, and the physical cables connecting the datacenters.
    - **Host Infrastructure**: Maintaining the physical servers, hardware, and virtualization hypervisors.

- Responsibilities That Vary by Service Type

| Responsibility Area                  | On-Premises | IaaS (e.g., VMs) | PaaS (e.g., App Service) | SaaS (e.g., M365) |
| ------------------------------------ | ----------- | ---------------- | ------------------------ | ----------------- |
| Physical Hosts, Network & Datacenter | Customer    | Microsoft        | Microsoft                | Microsoft         |
| Operating System                     | Customer    | Customer         | Microsoft                | Microsoft         |
| Network Controls (e.g., Firewalls)   | Customer    | Customer         | Shared                   | Microsoft         |
| Applications                         | Customer    | Customer         | Shared                   | Shared            |

---

---

## Cloud Pricing

- Pricing calculator
  - https://azure.microsoft.com/en-us/pricing/calculator/

- Consumption Based Model
  - Azure free account
  - Pay as you go
  - Shift from Capex to Opex

---

## Cloud Service Types

- `IaaS`
  - Computing: `Azure VM`
  - storage: `Azure Storage`
  - Networking: `VNet`

- `PaaS`
  - Middleware, dev tools, db
  - Computing: `Azure App Services`
  - Storage: `SQL Database`, `Managed Storage`
  - Networking: `Front Door`, `Load Balancer`, `Firewall`

- `SaaS`

- `Serverless`
  - Not manage servers
  - focus on the code

---

## Regions

- `Region`
  - area where Azure has 3 set of datacenters(minimum 3)
  - map: https://datacenters.microsoft.com/globe/explore

- `region pair`
  - 2 connected regions
  - have highest speed connection

- `Availability Zones`
  - physically and logically **separated datacenters** within a **single** `Azure region`.

- `Zonal Service`
  - service to deploy to **one** specific `AZ`
  - Availabilty by multi-AZ
  - e.g. VM
- `Zone-Redundant Services`
  - automatically deploy across zones
  - e.g., Azure SQL Database
- `Always available services` / `non-regional services`
  - global services, always on
  - e.g., Azure Poral, Entra ID, Azure Front Door

---
