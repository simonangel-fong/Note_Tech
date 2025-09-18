# Kubernetes - Fundamental

[Back](../../index.md)

- [Kubernetes - Fundamental](#kubernetes---fundamental)
  - [Virtualization vs. Containerization vs. Orchestration](#virtualization-vs-containerization-vs-orchestration)
  - [Kubernetes](#kubernetes)
  - [Microservices](#microservices)
    - [Example - Voting system](#example---voting-system)
  - [Declarative vs Imperative vs Functional vs Procedural](#declarative-vs-imperative-vs-functional-vs-procedural)
    - [K8s = Declarative](#k8s--declarative)

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

---

## Declarative vs Imperative vs Functional vs Procedural

- `Declarative Programming`

  - A paradigm to **describe what the program should accomplish**, **not how to do it**.
  - The **control flow** is abstracted away by the language or framework.
  - **Focuses on results** rather than steps.
  - Examples: SQL, HTML, regular expressions, Prolog.

- `Imperative Programming`

  - A paradigm to explicitly tell the computer **how to perform tasks, step by step**.
  - **define the control flow** with statements that change program state.
  - Focuses on **commands** and **state changes**.
  - Examples: C, Python (when used with loops and assignments), Assembly.

- `Functional Programming`

  - A style of `declarative programming` where computation is treated as the **evaluation of mathematical functions** without changing state or mutable data.
  - Emphasizes pure functions, immutability, and avoiding side effects.
  - Examples: Haskell, Lisp, Scala, Python (functional features: map, lambda, etc.).

- `Procedural Programming`

  - A subset of `imperative programming` that organizes code into **procedures** (functions or routines).
  - Each **procedure** performs a specific **task** and can be reused.
  - Focuses on **procedures** (reusable blocks of code).
  - Examples: C, Pascal, Fortran, Python (when structured into functions).

- `Object-Oriented Programming (OOP)`

  - A paradigm that organizes software design around `objects`
    - bundles of data (**attributes**) and behavior (**methods**).
  - emphasizes **encapsulation**, **inheritance**, and **polymorphism**.
  - Focuses on **objects that model real-world entities**.
  - Examples: Java, C++, C#, Python (when using classes/objects).

- Categorization

  - `Imperative` (broad category: how to do it)
    - `Procedural`
    - `Object-Oriented`
  - `Declarative` (broad category: what to achieve)
    - `Functional`

---

### K8s = Declarative

- Kubernetes is a Declarative style
  - describe the desired state
  - `Kubernetes controllers` work continuously to **reconcile the actual state** with the desired state.
