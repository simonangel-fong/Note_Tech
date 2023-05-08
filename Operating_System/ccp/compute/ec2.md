# AWS - EC2

[Back](../index.md)

- [AWS - EC2](#aws---ec2)
  - [EC2](#ec2)
  - [EC2 Instance Families](#ec2-instance-families)
  - [Instance Types](#instance-types)
  - [Dedicted Host](#dedicted-host)
  - [EC2 Tenancy](#ec2-tenancy)
  - [Pricing Models](#pricing-models)
    - [On-Demand](#on-demand)
    - [Reserved Instances (RI)](#reserved-instances-ri)
  - [Spot Instances](#spot-instances)
  - [Dedicated Instances](#dedicated-instances)
  - [Saving Plan](#saving-plan)

---

## EC2

- `Elastic Compute Cloud (EC2)`
  - a highly configuration virtual server
  - resizable compute capacity.
  - takes minutes to launch new instances.
  - Everything on AWS uses EC2 instance underneath.

![ec2](./pic/ec2.png)

---

## EC2 Instance Families

- `Instance Families`

  - different combinations of CPU, Memory, Storage, and Networking capacity.
  - allow to choose the appropriate combination of capacity to meet user's application's unique requirements.

![family](./pic/instance_family.png)

---

## Instance Types

- `Instance Types`

  - a combination of size and family.

- EC2 Instance Sizes generally double in price and key attributes

---

## Dedicted Host

- `Dedicted Host`
  - single-tenant EC2 instances designed to let user Bring-Your-Own-License (BYOL) based on machine characteristic.

![Dedicted Host](./pic/ec2_dedicated_host.png)

---

## EC2 Tenancy

- 3 levels of tenancy
  - `Dedicated Host`
    - User has whole server and control of the physical attribute.
  - `Dedicated Instance`
  - `Default`

![tenancy](./pic/ec2_tenancy.png)

---

## Pricing Models

- 5 ways to pay for EC2

![pricing](./pic/ec2_pricing_model.png)

---

### On-Demand

- `On-Demand`

  - Pay-As-You-Go (PAYG), where user consumes compute and then pay.

- `On-demand` has **no up-front payment** and **no long-term commitment**.

- It is **by default** using On-Demand pricing when an EC2 is launched.

- EC2s are charged by **per-second** (minumum of 60 seconds) or **per-hour**. When looking up pricing it will always show EC2 pricing is the **hourly rate**.

  - `per-second`
    - for Linux, Windows, Windows with SQL Enterprise, Windows with SQL Standard, and Windows with SQL Web Instances **that do not have a separate hourly charge**.
  - `per-hour`
    - full hour for all other instance types.

- On-Demand is for applications where the **workload is for short-term, spikey or unpredictable**.
  - For users whos have a new app **for deveplopment** or want to run **experiment**.

---

### Reserved Instances (RI)

- `Reserved Instances (RI)`

  - is designed for application that have a steady-state, predictable usage, or require reserved capacity.

- Reduced pricing is based on **Term**, **Class Offering**, **RI Attributes**, and **Payment Option**.

- **Term**: The longer the term, the greater savings.

  - User commit to a **1 Year** or **3 Year** contract.
  - Reserved instances do **not renew automatically**.
  - The instance will use **On-Demand** with no interruption to service when **expiring**.

- **Class**: The less flexible the greater the savings.

  - **Standard**

    - Up to 75% reduced pricing compared to on-demand.
    - User can modify RI Attributes.

  - **Convertible**

    - Up to 54% reduced pricing compared to on-demand.
    - User can exchange RI based on RI Attributes if greater or equal in value.

- **Payment Option**: The greater upfront the greate the savings

  - **All Upfront**
    - Full payment is made at the start of the term
  - **Partial Upfront**
    - A portion of the cost must be upfront and the remaining hours in the term are billed at a discounted hourly rate.
  - **No Upfront**
    - Users are billed a discounted hourly rate for every hour within the term, regardless of whether the Reserved Instance is being used.

- RI can be **shared between multiple accounts** within an AWS Organization.
- **Unused RIs can be sold** in the Reserved Instance Maketplace.

---

- `RI Attributes / Instance Attributes`

  - are limited based on Class Offering and can affect the final price of an RI Instance.

- There are 4 RI Attributes

  - Instance Type:
    - is composed of the instance family and the instance size.eg. m4.large
  - Region
    - The region in which the reserved instance is purchased.
  - Tenancy
    - Whether instance runs on shared(default) or single-tenant(dedicated) hardware.
  - Platform
    - The Operating System. eg.windows or Linux/Unix.

---

- Regional and Zonal RI

- When purchasing a RI, user determines the scope of the Reserved Instance.
  - The scope does not affect the price.

| Regional RI:purchase for a Region                                                                                                                           | Zonal RI: purchase for an AZ                                                                                      |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| does not reserve capacity                                                                                                                                   | reserves capacity in the specified AZ                                                                             |
| RI discount applies to instance usage in any AZ in the Region.                                                                                              | RI discount applies to instance in the selected AZ(No AZ Flexibility)                                             |
| RI discount applies to instance usage within the instance family, regardless of size. Only supported on Amazon Linux Reserved Instances with default tenacy | No instance size flexibility. RI discount applies to instance usage for the specified instance type and size only |
| User can queue purchases for regional RI                                                                                                                    | User cannot queue purchases for zonal RI                                                                          |

---

- `RI Limit`
  - a limit to the number of Reserved Instances that user can purchase per month.
- Per month user can purchase

  - 20 Regional Reserved Instances per Region
  - 20 Zonal Reserved Instances per AZ

- `Regional Limits`

  - The default **On-Demand Instance limit** is 20.
  - User cannot exceed user's running **On-Demand Instance limit** by purchasing regional Reserved Instances.
  - Before purchasing RI user must ensure On-Demand limit is equal to or greater than the RI that user intends to purchase.
  - Regional Limits <= On-Demand = 20

- `Zonal Limits`

  - User can exeed the running On-Demand Instance limit by purchasing zonal Reserved Instances.
  - If user already have 20 running On-Demand Instances, and purchase 20 zonal RIs, user can launch a furhter 20 On-Demand Instance that match the specifications of the zonal RI.

---

- `Capacity Reservation`

  - a service of EC2 that allows user to request a reserve of EC2 type for a specific Region and AZ.
  - EC2 instances are backed by different kind of hardware, and so there is a finite amount of servers available within an AZ per instance type or family.
    - So AWS may have ran out of a specific type of server when user launch an EC2.

- The reserved capacity is charged at the selected instance type's **On-Demand rate** wether an instance is running in it or not.

- User can also use regional RI with Capacity Reservations to benefit from billing discounts.

---

- Standard RI vs Convertible RI

![difference](./pic/ec2_pricing_RI_vs_converable.png)

---

- RI Marketplace

  - EC2 Reserved Instance Marketplace allows user to sell unused **Standard RI** to recoup RI spend for RI user do not intend or cannot use.

![Marketplace](./pic/ec2_pricing_marketplace.png)

---

## Spot Instances

- `Spot instance` provide a discount of 90% compared to On-Demand Pricing.

  - can be terminated if the computing capacity is needed by other On-Demand customers.
  - AWS has unused compute capacity that they want to maximize the utility of their idle servers.
  - For application that have flexible start and end times or applications that are only feasible at very low compute costs.

- `AWS Batch`

  - a aws service using `Spot Pricing`.

- **Termiantion Conditions**
  - Instance can be terminated by AWS at anytime.
  - If instance is terminated by AWS, user does not get charged for a partial hour of usage.
  - If user termiantes an instance, user will still be charged for any hour that it ran.

---

## Dedicated Instances

- `Dedicated Instances`

  - are designed to meet regulatory requirements.
  - For users who have strict server-bound licening that won't support multi-tenancy or cloud deployments.

- Enterprises and Large Organizations may have security concerns or obligations about against sharing the same hardware with other AWS Cutomers.

- `Multi-Tenant`

  - When **multiple customers** are running workloads on the same hardware.
  - **Virtuall Isolation** is what separate customers.

- `Single Tenant`

  - When a single customer has dedicated hardware.
  - **Physical Isolation** is what separates customers.

- Dedicated can be offer for :
  - **On-demand**
  - **Reserved** (up to 60% savings)
  - **Spot** (up to 90% savings)

![Dedicated Instances](./pic/ec2_pricing_dedicated_instance.png)

---

## Saving Plan

- `Saving Plans`

  - offer users the similar disounts as RI but simplify the purchasing process.

- 3 types of saving plans
  - `Compute`:
    - provide the most flexibility and help reduce costs by up to 66%.
    - automatically apply to EC2 instance usage, Fargate, and Lambda service usage regardless of instance family, size, AZ, region, OS, or tenancy.
  - `EC2 Instance`:
    - provide the lowest prices, offering savings up to 72% in exchange for commitment to usage of individual instance families in a region.
    - automatically reduces cost on the selected family in that region regardless of AZ, size, OS, or tenancy.
    - offer the flexibility to change usage between instances within a family in that region.
  - `SageMaker`
    - Help reduce SageMaker costs by up to 64%.
    - automatically apply to SageMaker usage regardless of instance family, size, component, or AWS region.

![types](./pic/ec2_pricing_saving_plan_types.png)

- Terms:

  - 1 Year
  - 3 Year

- Payment Options
  - All Upfront
  - Partial Upfront
  - No Upfront

![Payment](./pic/ec2_pricing_saving_plan_payment.png)

---

[TOP](#aws---ec2)
