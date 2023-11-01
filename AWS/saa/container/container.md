# AWS - Container

[Back](../index.md)

- [AWS - Container](#aws---container)
  - [Docker](#docker)
    - [Docker Repositories](#docker-repositories)
    - [Docker vs. Virtual Machines](#docker-vs-virtual-machines)
  - [Docker Containers Management on AWS](#docker-containers-management-on-aws)
  - [AWS App Runner](#aws-app-runner)
    - [Hands-On](#hands-on)

---

## Docker

- `Docker`

  - a software development platform to deploy apps

- Apps are **packaged in containers** that can be **run on any OS**

  - Apps run the same, regardless of where they’re run
  - Any machine
  - No compatibility issues
  - Predictable behavior
  - Less work
  - Easier to maintain and deploy
  - Works with any language, any OS, any technology

- **Use cases**:
  - microservices architecture,
  - lift-and-shift apps from on-premises to the AWS cloud, …

![container_diagram](./pic/container_diagram.png)

![container_diagram02](./pic/container_diagram02.png)

---

### Docker Repositories

- `Docker images` are stored in `Docker Repositories`
- `Docker Hub` (https://hub.docker.com)

  - Public repository
  - Find base images for many technologies or OS (e.g., Ubuntu, MySQL, …)

- `Amazon ECR (Amazon Elastic Container Registry)`
  - Private repository
  - Public repository (Amazon ECR Public Gallery https://gallery.ecr.aws)

---

### Docker vs. Virtual Machines

- Docker is ”sort of” a virtualization technology, but not exactly
- **Resources** are **shared with the host** => many containers on one server

![container_vs_vm](./pic/container_vs_vm.png)

---

## Docker Containers Management on AWS

- `Amazon Elastic Container Service (Amazon ECS)`

  - Amazon’s own container platform

- `Amazon Elastic Kubernetes Service (Amazon EKS)`

  - Amazon’s managed Kubernetes (open source)

- `AWS Fargate`

  - Amazon’s own **Serverless** container platform
  - Works with `ECS` and with `EKS`

- `Amazon ECR`:
  - Store container **images**

![container_aws_services](./pic/container_aws_services.png)

---

## AWS App Runner

- **Fully managed** service that makes it easy to deploy web applications and APIs at scale
- No **infrastructure experience required**
- Start with your **source code** or **container image**
- Automatically **builds and deploy** the web app
- Automatic **scaling**, highly **available**, **load balancer**, **encryption**
- **VPC access** support
- Connect to **database**, **cache**, and **message queue** services

- **Use cases**:
  - web apps,
  - APIs,
  - microservices,
  - rapid production deployments

![app_runner_diagram.png](./pic/app_runner_diagram.png)

- Sample:
  - A developer has a running website and APIs on his local machine using containers and he wants to deploy both of them on AWS. The developer is new to AWS and **doesn’t know much about different AWS services**. Which of the following AWS services allows the developer to build and deploy the website and the APIs in the easiest way according to AWS best practices?
  - App Runner.

---

### Hands-On

![app_runner_handson01](./pic/app_runner_handson01.png)

---

[TOP](#aws---container)
