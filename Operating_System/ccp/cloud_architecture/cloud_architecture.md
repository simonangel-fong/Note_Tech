# AWS - Global Infrastructure

[Back](../index.md)

- [AWS - Global Infrastructure](#aws---global-infrastructure)
  - [Terminologies](#terminologies)
  - [High Availability](#high-availability)
  - [High Scalability](#high-scalability)
  - [High Elasticity](#high-elasticity)
  - [Highly Fault Tolerant](#highly-fault-tolerant)
  - [High Durability](#high-durability)
    - [Business Continuity Plan](#business-continuity-plan)
  - [Architectural Diagram Example](#architectural-diagram-example)

---

## Terminologies

- `Solution Architect`:

  - A role in a technical organization that architects a technical solution using multiple systems via researching, documentation, experimentation.

- `Cloud Architect`
  - A solution architect that is focused solely on architecting technical solution **using cloud services**.
  - needs to understand the following terms and factor them into their designed architecture based on the business requirement.
    - Availability: The ability to ensure a service remains available. e.g. Highly Available(HA)
    - Scalability: The ability to grow rapidly or unimpeded.
    - Elasticity: The abilibty to shrink and grow to meet the demand.
    - Fault Tolerance: The ability to prevent a failure.
    - Disaster Recovery: The ability to recover from a failure. e.g.Highly Durable(DR)
    - Security: How secure is this solution?
    - Cost: How much is this going to cose.

---

## High Availability

- The ability for the service to **remain available** by ensuring there is **no single point of failure** and/or ensure a certain level of performance.

- Example: Multiple Availability Zones
  ![high availability](./pic/high_availability.png)

- Use Case: Beanstalk
  ![beanstalk](./pic/ha_example_beanstalk01.png)

- Use Case: RDS
  ![beanstalk](./pic/ha_example_rds01.png)

- `Elastic Load Balancer`

  - A load balancer allows to evenly distribute traffic to multiple servers in one or more datacenter. If a datacenter or server becomes unavailable (unhealthy) the load balancer will route the traffic to only available dataceners with servers.

---

## High Scalability

- The ablity to **increase the capacity** based on the increasing demand of traffic, memory and computing power.

- `Vertical Scaling`:

  - `Scaling Up`: Upgrade to a bigger server.

- `Horizonal Scaling`

  - `Scaling Out`: Add more servers of the same size.

---

## High Elasticity

- The ability to **automatically** increase or decrease the capacity based on the current demand of traffic, memory and computing power.

- `Horizonal Scaling`

  - `Scaling Out`: Add more servers of the same size.
  - `Scaling In`: Removing underutilized servers of the same size.

- `Vertical Scaling` is generally hard for traditional architecture so user will usually **only see horizontal scaling** described with Elasticity.

- `Auto Scaling Groups` (`ASG`)
  - an AWS feature that will automatically add or remove servers based on scaling rules user define based on metrics.

---

## Highly Fault Tolerant

- The ability for the service to ensure there is **no single point of failure**, preventing the chance of failure.

- `Fail-overs`

  - When user have a plan to shift traffic to a redundant system in case the primary system fails.

- Example: RDS Multi-AZ
  ![Highly Fault Tolerant](./pic/highly_fault_tolerant.png)

---

## High Durability

- The ability to **recover** from a disaster and to **prevent the loss of data**.

- `Disaster Revocery (DR)`

  - the solution that recover from a disaster.
  - factors to be considered:
    - Do you have a backup?
    - How fast can you restore that backup?
    - Does your backup still work?
    - How do you ensure current live data is not corrupt?

- `CloudEndure Disaster Recovery`
  - continuously replicates user's machines into a low-cost staging area in user's target AWS account and preferred Region enabling fast and reliable recovery in case of IT data center failures.

---

### Business Continuity Plan

- `Business Continuity Plan (BCP)`

  - a document that outlines how a business will continue operating **during an unplanned distruption in services**.

  ![bcp](./pic/disaster_recovery_bcp.png)

- Disaster Recovery Option

  - `Backup & Restore`: backup data and restore them **to new infrastructure**.

    - Lower priority use cases
    - Restore Data after event
    - Deploy resources after event
    - Cost: $

  - `Pilot Light`: data is replicated **to another region** with the minimal services running

    - Less stringent RTO & ROP
    - Core Services
    - Start and scale resources after event
    - Cost: $$

  - `Warm Standby`: scaled down copy of user's infrastructure running ready to scale up.

    - Business Critical Services
    - Scale resources after event
    - Cost: $$$

  - `Multi-site`: Scaled up copy of user's infrastructure **in another region**.
    - Zero downtime
    - Nero zero loss
    - Mission Critical Services
    - Cost: $$$$

  ![option](./pic/disaster_recovery_option.png)

- `Recoery Time Objective (RTO)`

  - the maximum acceptable delay between the interruption of service and restoration of service.
  - This objective determines what is considered an acceptable time window when service is unavailble and is defined by the organization.

  ![rto](./pic/disaster_recovery_rto.png)

- `Recoery Point Objective (RPO)`

  - the maximum acceptable amount of data since the last data recovery point.
  - This objective determines what is considered an acceptable loss of data between the last recovery point and interruption of service and is defined by the organization.

  ![rpo](./pic/disaster_recovery_rpo.png)

---

## Architectural Diagram Example

- AWS Architecture Icons: https://aws.amazon.com/architecture/icons/

---

[Top](#aws---global-infrastructure)
