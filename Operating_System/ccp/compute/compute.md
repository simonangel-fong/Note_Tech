# AWS - Compute

[Back](../index.md)

- [AWS - Compute](#aws---compute)
  - [Elastic Compute Cloud (EC2)](#elastic-compute-cloud-ec2)
  - [Computing Service](#computing-service)
  - [Higher Performance Computing Services](#higher-performance-computing-services)
  - [Edge and Hybrid Computing Services](#edge-and-hybrid-computing-services)
  - [Cost and Capacity Management Computing Services](#cost-and-capacity-management-computing-services)

---

## Elastic Compute Cloud (EC2)

- `Virtual Machine`

  - an emulation of a physical computer using software.
  - `Server Virtualization` allows user to easily create, copy, resize or migrate server.
  - Multiple VMs can run on the same physical server so user can share cost with other customers.
  - Purpose: Server or computer is an executable file on computer.

- `instance`

  - a launched Virtual Machine

- `Amazon Machine Image (AMI)`

  - a **predefined configuration** for a `Virtual Machine`.

- `Elastic Compute Cloud (EC2)`

  - allows user to launch **Virtual Machines(VM)**.

- `EC2` is highly configurable server where user can choose `AMI` that affect options

  - the amount of CPUs
  - the amount of Memory (RAM)
  - the amount of Network Bandwidth
  - the Operation System (OS)
  - Attach multiple virtual hard-drives for storage.

- `EC2` is the backbone of AWS because the majority of AWS Service are using EC2 as their underlying servers.

---

## Computing Service

- Virtual Machine

  - `Amazon LightSail`
    - the managed virtual server service.
    - The friendly version of EC2 Virtual Machines. When user need to lauch a Linux or Windows Server but don't have much AWS knowledge. eg. Launch a Wordpress

- `Container`

  - virtualizing an Operation System to **run multiple workloads** on a single OS instance. Containers are generally used in micro-service architecture.

    - `Elastic Container Service (ECS)`

      - a container orchestration service that **support Docker container**.
      - Launches a cluster of servers on EC2 instances with Docker installed.
      - for user who needs docker as a service or needs to run containers.

    - `Elastic Container Registry (ECR)`

      - repository for **container images**.
      - To launch containers, user need an `image`.
      - `Image`: a saved copy.
      - `Repository`: a storage that has version control.

    - `ECS Fargate`

      - **serverless orchestration container service**.
      - Same as ECS that user pay-on-demand per running container.(With ECS user has to keep a EC2 server running even if user have on containers running.)
      - AWS manages the underlying server, so user does not have to scale or upgrade the EC2 server.

    - `Elastic Kubernetes Service (EKS)`
      - a fully managed **Kubernetes service**.
      - `Kubernetes (K8)`
        - an open-source orchestration software that was created by Google and is generally the standard for managing `microservices`.
        - For ueser who needs to run Kubernetes as a service.

- `Serverless`

  - when the underlying servers are managed by AWS.User does not worry or configure servers.

    - `AWS Lambda`
      - a **serverless function service**.
      - User can run code without provisioning or managing servers
      - User uploads small pieces of code and chooses how much memory and how long function is allowed to run before timing out.
      - Charged based on the runtime of the serverless function rounded to nearest 100ms.

---

## Higher Performance Computing Services

- `Nitro System`

  - a combination of dedicated hardware and lightweight hypervisor enabling faster innovation and enhanced security.
  - All new EC2 instance types use the Nitro System.
  - `Nitro Cards`, specialized cards for VPC, EBS and Instance Storage and controller card.
  - `Nitro Security Chips`, integrated into motherboard. Protects hardware resources.
  - `Nitro Hypervisor`, lightweight hypervisor Memory and CPU allocation Bare Metal-like performance.

- `Bare Metal Instance`

  - User can launch EC2 instance that have no hypervisors so user can run workloads directly on the hardware for maximum performance and control.
  - The **M5 and R5** EC2 instances run bare metal.

  - `Bottlerocket`

    - a Linux-based open-source operation system that is purpose-built by AWS for running containers on Virtual Machines or bare metal hosts.

- `High Performance Computing (HPC)`

  - A cluster of hundreds of thousands of servers with fast connections between each of them with the purpose of boosting computing capacity.
  - For users who need a supercomputer to perform computational problems too large to run on a standard computers or would take too long.
  - AWS HPC: https://aws.amazon.com/hpc/

  - `AWS ParallelCluster`
    - an AWS-supported open source **cluster management tool** that makes it easy for user to **deploy and manage High Performance Computing(HPC) clusters** on AWS.

---

## Edge and Hybrid Computing Services

- `Edge Computing`

  - when user pushes computing workloads outside of user's networks to run close to the destination location.
  - eg.Pushing computing to run on phones, loT Devices, or external servers not within user's Cloud Network.

- `Hybrid Computing`

  - When user runs workloads on both user's on-premise datacenter and `AWS Virtual Private Cloud(VPC)`

- AWS Services:

  - `AWS Outposts`

    - physical racks of servers that can be put in user's data center. AWS Outposts allows to use AWS API and Services such as EC2 right in user's datacenter.

  - `AWS Wavelength`

    - allows to build and launch user applications in a telecom datacenter.
    - User's applications with have ultra-low latency since they will be pushed over a the 5G network and be closest as possible to the end user.

  - `VMWare Cloud on AWS`

    - allows to manage on-premise virtual machines using VMWare as EC2 instances.
    - The data center must be using VMWare for Virtualization.

  - `AWS Local Zones`
    - the edge data centers located outside of an AWS region so user can use AWS closer to end destination.
    - For users who need faster computing, storage, and databases in populated areas that are outside of an AWS Region.

---

## Cost and Capacity Management Computing Services

- `Cost Management`: How to save money
- `Capacity Management`: How to meet the demand of traffic and usages though adding or upgrading servers

- `EC2 Spot Instances, Reserved Instanced and Saving Plan`

  - ways to save on computing, by paying up in full or partially, by committing to a yearly contracts or by being flexible about avaiability and interruption

- `AWS Batch`

  - plans, schedules, and executes batch computing workloads across the full range of AWS compute services, can utilize Spot Instance to save money.

- `AWS Compute Optimizer`

  - suggests how to reduce costs and improve performance by using machine learning to analyze previous usage history.

- `EC2 Autoscaling Groups (ASGs)`

  - Automatically adds or remove EC2 servers to meet the current demand of traffic.
  - Will save money and meet capacity since it only run the amount of servers user needs.

- `Elastic Load Balancer (ELB)`

  - Distributes traffic to multiple instance, can re-route traffic from unhealthy instance to healthy instance.
  - can route traffic to EC2 instances running in different Availability Zones.

- `AWS Elastic Beanstalk (EB)`
  - is for easily deploying web-applications without developers having to worry about setting up and understanding the underlying AWS services.

---

[TOP](#aws---compute)
