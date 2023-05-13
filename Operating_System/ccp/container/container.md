# AWS - Containers

[Back](../index.md)

- [AWS - Containers](#aws---containers)
  - [Docker](#docker)
    - [Podman](#podman)
    - [VMs vs Containers](#vms-vs-containers)
    - [Docker images](#docker-images)
  - [Microservices](#microservices)
  - [Kuberenetes](#kuberenetes)
  - [Container Services On AWS](#container-services-on-aws)
    - [Elastic Container Service (ECS)](#elastic-container-service-ecs)

## Docker

- `Docker`
  - a set of Platform as Service (PaaS) products that use OS-level virtualization to deliver software in **packages called containers**.
  - a software development platform **to deploy apps**
- Apps are **packaged** in **containers** that can be run on any OS
- Apps **run the same**, regardless of where they’re run
  - Any machine
  - No compatibility issues
  - Predictable behavior
  - Less work
  - Easier to maintain and deploy
  - Works with any language, any OS, any technology
- Scale containers up and down very quickly (seconds)

![docker](./pic/docker.png)

---

### Podman

![podman](./pic/podman.png)

---

### VMs vs Containers

- `VMs`

  - VMs do **not make best use of space**.
  - Apps are **not isolated** which could cause config conflicts, security problems or resource hogging.

- `Containers`
  - containers allow to run multiple apps which are **virtually isolated** from each other.
  - Launch new containers and configures OS Dependencies per container.

![container](./pic/vm_vs_container.png)

---

### Docker images

- `Docker images` are stored in **Docker Repositories**
- Private: `Amazon ECR (Elastic Container Registry)`

---

## Microservices

- `Monolithic Architecture`

  - **One app** which is resonsible **for everyting** functionality is tightly coupled.

- `Microservices Architecture`
  - Multiple apps which are **each resonsible for one thing functionality** is isolate and stateless.

![miscoservices](./pic/miscoservices.png)

---

## Kuberenetes

- `Kuberenetes`

  - an open-source container orchestration system for automating deployment, scaling, and management of containers.
  - commonly called `K8`

- The advantage of Kubernetes over Docker is the ability to **run containers distributed** across multiple VMs.

- A unique component of Kubernetes are **Pods**.

  - A pod is a group of one more containers with shared storage, network resources, and other shared settings.

- Kuberenetes is ideally for micro-service architectures where a company has tems to hundreds of services they need to manage.

![Kuberenetes](./pic/kuberenetes.png)

---

## Container Services On AWS

### Elastic Container Service (ECS)

- `Elastic Container Service (ECS)`
  - Launch Docker **containers** on AWS
- Has integrations with the `Application Load Balancer`
- You **must provision & maintain the infrastructure (the EC2
  instances)**
- AWS takes care of starting / stopping containers

![services](./pic/container_services.png)

---

[TOP](#aws---containers)
