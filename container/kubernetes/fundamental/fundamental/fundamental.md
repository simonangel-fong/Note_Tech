# Kubernetes - Fundamental

[Back](../../index.md)

- [Kubernetes - Fundamental](#kubernetes---fundamental)
  - [Container vs Orchestration](#container-vs-orchestration)
    - [Container](#container)
  - [Kubernetes](#kubernetes)
  - [Architecture](#architecture)
    - [Components](#components)

---

## Container vs Orchestration

### Container

- `Container`

  - completely isolated environments

- Benefits

  - Compatibility/Dependency Issue
  - Long setup time
  - Different Dev/Test/Prod environment

- Address by Containerizing Applications

  - Run each service with its own dependenciesin separate containers

- `Container Orchestration`

---

## Kubernetes

- `Kubernetes`
  - a container management technology which helps in creating and managing containerization of application.
  - an open source system
  - originally developed by `Google` and now maintained by the `Cloud Native Computing Foundation (CNCF)`

---

- It can run application **on clusters of physical and virtual machine infrastructure**.
- It also has the capability to **run applications on cloud**.
  - It helps in moving from **host-centric infrastructure** to **container-centric infrastructure**.

---

## Architecture

- `node (Minions)`

  - a machine, physical or virtual, on which kubernetesis installed.
  - a worker machine where containers will be launched by kubernetes.

- `cluster`

  - a set of nodes grouped together.
  - This way even if one node fails you have your application still accessible from the other nodes. -
  - Moreover having multiple nodes helps in sharing load as well.

- `master`
  - a node with Kubernetes installed in it, and is configured as a Master.
  - The master **watches over** the nodes in the cluster and is responsible for the **actual orchestration** of containers on the worker nodes.

---

### Components

- Components

  - **API Server**
    - the front-end for kubernetes
    - The users, management devices, Command line interfaces all talk to the API server to interact with the kubernetes cluster.
  - **An ETCD service**
    - a distributed reliable **key-value store** used by kubernetesto store all data used to manage the cluster.
    - stores all that information on all the nodes in the cluster in a distributed manner
    - responsible for implementing locks within the cluster to ensure there are no conflicts between the Masters.
  - **A kubelet service**
    - agent that runs on each node in the cluster.
    - responsible for making sure that the containers are running on the nodes as expected.
  - **A Container Runtime**
    - the underlying software that is used to run containers.
    - example: docker
  - **Controllers**

    - responsible for noticing and responding when nodes, containers or endpoints **goes down**.
    - The controllers makes decisions to **bring up new containers** in such cases.

  - **Schedulers**
    - s responsible for **distributing** work or containers across multiple nodes.
    - looks for newly created containers and assigns them to Nodes.

![pic](./pic/master_vs_worker.png)

---
