# Kubernetes - Fundamental

[Back](../../index.md)

- [Kubernetes - Fundamental](#kubernetes---fundamental)
  - [Virtualization vs. Containerization vs. Orchestration](#virtualization-vs-containerization-vs-orchestration)
  - [Kubernetes](#kubernetes)
  - [Microservices](#microservices)
    - [Example - Voting system](#example---voting-system)

---

## Virtualization vs. Containerization vs. Orchestration

- `Virtualization`

  - A **hardware-abstraction** solution that **partitions a physical machine** into multiple independent environment, called `virtual machines`, each with its own `operating system`.
  - purpose:
    - Run **multiple OS instances** on one physical machine
  - tool:
    - VMware, Hyper-V, KVM, Proxmox VE

- `Containerization`

  - An **application-abstraction** solution that packages an application and its **dependencies** into a consistent, called `container`, isolated environment running on a shared operating system.
  - purpose:
    - Ensure **consistent application environments** across systems
  - tool:
    - Docker, Podman, LXC

- `Orchestration`
  - An automation solution that coordinates the deployment, scaling, and operation of **applications** across **distributed containerized environments**.
  - purpose:
    - Automate and optimize containerized application lifecycle at scale
  - tool:
    - Kubernetes, Docker Swarm, Amazon ECS

---

| Aspect                   | **Virtualization**             | **Containerization**                      | **Orchestration**         |
| ------------------------ | ------------------------------ | ----------------------------------------- | ------------------------- |
| **Level of Abstraction** | Hardware / OS                  | Application / runtime                     | Infrastructure management |
| **Isolation Target**     | Operating systems              | Applications                              | Application operations    |
| **Overhead**             | High (each VM runs its own OS) | Low (containers share the host OS kernel) | Variable                  |

---

## Kubernetes

- `Kubernetes`

  - An open-source orchestration solution that **automates** the deployment, scaling, networking, and lifecycle management of applications **across clusters of containerized environments**.
  - maintained by the `Cloud Native Computing Foundation (CNCF)`

---

## Microservices

- `Microservices`

  - a **software architecture** that structures a large application as a **collection** of small, **independent**, and **loosely coupled services**, each responsible for a specific business function.
  - vs `monolithic architectures`
    - services **communicate** with each other via lightweight **APIs**
    - services can be **developed**, **deployed**, and **scaled** independently, offering benefits like enhanced agility, resilience, and easier maintenance

---

### Example - Voting system

- Basic services

| Service          | description              |
| ---------------- | ------------------------ |
| Voting service   | Receive votes from users |
| Cache service    | Cache vote data          |
| backend service  | handle vote transaction  |
| database service | persist vote data        |
| result service   | return vote data         |

![pic](./pic/microservices01.png)

- Application Architecture with deployment

![pic](./pic/microservices02.png)
