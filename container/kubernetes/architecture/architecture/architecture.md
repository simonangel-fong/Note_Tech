# Kubernetes - Architecture

[Back](../../index.md)

- [Kubernetes - Architecture](#kubernetes---architecture)
  - [Architecture](#architecture)
    - [Node and Cluster](#node-and-cluster)
    - [Components](#components)
  - [Master Machine Components](#master-machine-components)
  - [Node Components](#node-components)

---

## Architecture

![kub_architecture](./pic/kub_architecture.png)

![pic](./pic/master_vs_worker.png)

---

### Node and Cluster

- `Node` / `Minions`

  - A machine, physical or virtual, that provides the resources required to run workloads.

- `Worker Node`

  - A type of `node` that runs the **application workloads** (pods) and provides compute, storage, and networking.

- `Master Node` / `Control Plane Node`

  - A type of `node` that runs the **control plane components** responsible for scheduling, orchestrating, and monitoring workloads across worker nodes.

- `Cluster`

  - A **collection** of `nodes`, master and worker, that operate together as a single system for running and managing applications.

---

### Components

- **API Server**
  - the front-end for kubernetes
  - The users, management devices, Command line interfaces all talk to the API server to interact with the kubernetes cluster.
- **ETCD service**
  - a distributed reliable **key-value store** used by kubernetesto store all data used **to manage the cluster**.
  - stores all that **information on all the nodes** in the cluster in a distributed manner
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

## Master Machine Components

- `Control Plane Components`

  - Manage the overall state of the cluster

- `etcd`

  - a **distributed, key-value store** that Kubernetes uses as its **primary datastore**.
  - used to **stores the configuration information** which can be used by **each of the nodes** in the cluster.
  - distributed among multiple nodes.
  - accessible **only** by `Kubernetes API server` as it may have some sensitive information.

- `API Server`

  - a `control plane` component that serves as the **central point of access** for interacting with the cluster
  - a `RESTful API` over HTTP, enabling users, other cluster components, and external systems to manage, query, and **manipulate the state** of Kubernetes objects like Pods, Services, and Deployments.

- `Controller Manager`

  - a `control plane` component used to run controller processes.
  - a **daemon** which runs in **nonterminating loop** and is responsible for **collecting and sending information** to `API server`.
  - To **get the shared state** of cluster and then **change the current status** of the server to the **desired state**.
  - key controllers
    - `replication controller`,
    - `endpoint controller`,
    - `namespace controller`,
    - and `service account controller`.

- `Scheduler`

  - a `control plane` component used to **allocate** `Pods` to `Nodes` in the cluster and **distribute the workload**.
  - To **track utilization** of working load on cluster nodes and then **place the workload** on which resources are available and accept the workload.
  - **Default** scheduler: `kube-scheduler`.

- `cloud controller manager`
  - A `control plane` component that embeds **cloud**-specific control **logic**.
  - Optional component.

---

## Node Components

- `Container runtime`

  - A node component that empowers Kubernetes to **run containers** effectively.
  - To **manage the execution and lifecycle** of containers within the Kubernetes environment.

- `kubelet`

  - An **agent** that runs on **each node** in the cluster.
  - To **ensure** that containers are **running** in a Pod.
    - **relay information** to and from `control plane` service.
    - **interact** with `etcd` store to **read configuration** details and wright values.
    - **receive commands** and work.
    - **manage** network rules, port forwarding, etc.

- `kube proxy`
  - a **network proxy** that runs on each **node** in cluster, implementing the Kubernetes Service.
  - **forward the request** to correct containers
  - **perform** primitive **load balancing**
  - **maintains network rules** on nodes.
  - optional
