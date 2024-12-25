# Linux - Container: Fundamental

[Back](../../index.md)

- [Linux - Container: Fundamental](#linux---container-fundamental)
  - [Container](#container)
    - [How Containers Work](#how-containers-work)
    - [Containers vs. Virtual Machines (VMs)](#containers-vs-virtual-machines-vms)
    - [Common Container Tools](#common-container-tools)

---

## Container

- `container`

  - a **standard unit of software** that includes everything needed to run an application: **code**, **runtime**, **libraries**, **dependencies**, and **configuration**.
  - **isolated** from each other and the underlying operating system, making them a preferred method for deploying and managing applications.

- Features

  - **Isolation**:
    - Each container runs **in its own environment**, **separate** from other containers and the host system.
    - Achieved using technologies like `namespaces` (process, network, filesystem) and `cgroups` (resource control).
  - **Lightweight:**
    - Containers **share** the host operating system's **kernel**, **avoiding the overhead** of a full operating system per container (unlike virtual machines).
  - **Portability:**
    - Containers run **consistently across different environments** (development, testing, production) since all dependencies are packaged with the application.
  - **Efficiency:**
    - Containers **use fewer resources** than virtual machines because they don't need a full OS for each instance.
  - **Scalability:**
    - Containers can be created, stopped, and destroyed **quickly**, enabling fast scaling of applications.

- An OS can run single or multiple containers at the same time.
- Roles:
  - developer: mostly use containers to write codes, build, and deploy applications
  - system administrator: install, congigure, and manage them.

---

### How Containers Work

- `Containers` rely on **containerization technology**, which is a form of operating **system-level virtualization**.
- Key components include:
  - **Container Engine:**
    - Software like `Docker`, `Podman`, or containerd that manages containers.
  - **Container Images:**
    - A container runs from an `image`, which is a static, immutable **template** containing the application and its dependencies.
      - Example: An Nginx image might include the Nginx server, its dependencies, and configuration files.
  - **Container Runtime:**
    - Executes and **manages containers** on the host system.
    - Examples: runc, CRI-O, or Docker's built-in runtime.

---

### Containers vs. Virtual Machines (VMs)

| Feature        | Containers                                   | Virtual Machines                              |
| -------------- | -------------------------------------------- | --------------------------------------------- |
| Isolation      | **Process**-level isolation                  | Full **hardware virtualization**              |
| Startup Time   | Seconds or less                              | Minutes                                       |
| Resource Usage | Lightweight (**shares** host OS **kernel**)  | Heavy (requires **full OS** for each VM)      |
| Portability    | Easily portable across environments          | Less portable due to dependence on hypervisor |
| Use Case       | **Microservices**, cloud-native applications | Legacy applications, **full OS** environments |

---

### Common Container Tools

- `Docker`:
  - not supported in RHEL 8.
  - Most popular containerization platform.
  - Includes tools for building, running, and managing containers.
- `Podman`:
  - default in Redhat
  - A **daemonless** alternative to Docker.
  - Designed to work without root privileges for better security.
- `Kubernetes`:
  - Orchestrates containers across **clusters** for high availability, scaling, and management.
- `CRI-O`:
  - A lightweight container runtime for Kubernetes.

---

[TOP](#linux---container-fundamental)
