# ArgoCD - Fundamental

[Back](../index.md)

- [ArgoCD - Fundamental](#argocd---fundamental)
  - [GitOps](#gitops)
  - [ArgoCD](#argocd)
    - [Core Concepts](#core-concepts)
  - [Architecture](#architecture)
    - [ArgoCD Server](#argocd-server)
    - [Repo Server](#repo-server)
    - [Application controller](#application-controller)
    - [Additional Components](#additional-components)

---

## GitOps

- `GitOps`
  - an **operational framework** that uses `Git` repositories as the "**single source of truth**" to define, manage, and deploy infrastructure and applications.

- **Principles of GitOps**
  - **Declarative Infrastructure**:
    - The **desired state** of the system is defined **declaratively** (e.g., Kubernetes YAML files) rather than through manual, imperative commands.
  - **Versioned and Immutable**:
    - All infrastructure and application configurations are **stored in Git**, ensuring a complete, versioned history for auditing and easy rollbacks.
  - **Automated Synchronization**:
    - Software agents (e.g., in the cluster) **automatically pull changes from the Git** repository and **update** the live environment, eliminating manual deployment steps.
  - **Continuous Reconciliation**:
    - The system **constantly monitors** for discrepancies between the Git repository and the actual state, automatically correcting any drift to ensure alignment.

---

## ArgoCD

- `ArgoCD`
  - a GitOps **continues delivery** tool for Kubernetes.

- Not a CI tool

![pic](./pic/vs_push_model.png)

![pic](./pic/argocd_pull_model.png)

- Features
  - `Git` as the **source of truth**.
    - Developer and DevOps engineer will update the Git code only.
  - Keep your cluster in **sync** with `Git`.
  - Easy **rollback**.
  - More security : Grant **access to ArgoCD** only.
  - Disaster recovery solution : You easily deploy the same apps to any k8s cluster.

---

### Core Concepts

- `Application`
  - a Kubernetes `Custom Resource Definition (CRD)` that defines the **desired state of an application** in a target cluster, **sourcing** its configuration (YAML, Helm, Kustomize) from a Git repository.
  - **the unit of deployment** and tracking, enabling GitOps by monitoring for differences between the Git repository and the cluster.
- **Source** :
  - Helm charts
  - Kustomize application
  - k8s manifests
  - jsonnet
- **Destination**: cluster and namespace.

---

- `Projects`
  - provide a **logical grouping** of `applications`.
  - a **logical grouping** of `applications` used to organize, restrict, and manage access **in multi-tenant environments**.
  - acts as a **safety boundary**, defining **which Git repositories** can be used, **where** applications can be deployed (clusters/namespaces), and **which users** can perform actions via RBAC.

- Use case:
  - when ArgoCD is used by multiple teams.

---

- `Desired state` vs `Actual state`
- `Desired state`:
  - the **definitive version** of what Kubernetes resources should look like, as defined by the **manifests stored in `Git` repository**.

- `Actual state`:
  - what is **currently running** in Kubernetes cluster.

- `Sync`
  - the process that **reconciles** the `desired state` of an `application` (defined in Git) with its `actual state` in a Kubernetes cluster.
  - makes the **live cluster** **match** the **`Git` repository**, applying manifest changes, creating new resources, or deleting removed ones.
  - can be manual or automated.

- `Refresh` (`Compare`)
  - **updates** the application's **status** by **comparing** the desired Git state with the live cluster state, **without changing cluster resources**.
  - By default, automatically refreshes every 3 minutes.

---

## Architecture

3 main components:

- ArgoCD Server (API + Web Server).
- ArgoCD Repo Server.
- ArgoCD Application Controller.

---

### ArgoCD Server

- Its a gRPC/REST server which **exposes the API** consumed by the **Web UI, CLI**.
  - Application management (Create, Update, Delete).
  - Application operations (ex: Sync, Rollback)
  - Repos and clusters management.
  - Authentication.

![pic](./pic/architecture_components_api_server.png)

---

### Repo Server

- `Repo Server`
  - acts as the bridge between `Git repositories` and `Kubernetes`.
  - roles:
    - **Clones** and keeps Git repositories **up-to-date**.
    - **generates** Kubernetes manifests (via Helm, Kustomize, etc.),
    - and **caches** them

![pic](./pic/architecture_components_repo_server.png)

---

### Application controller

- `Application controller`
  - a Kubernetes controller which **continuously monitors** running applications and **compares** the current, live state against the desired target state.

- Roles:
  - Communicate with `Repo server` to get the generated manifests.
  - Communicate with `k8s API` to get actual cluster state.
  - **Deploy** apps manifests to destination clusters.
  - **Detects** OutofSync Apps and take corrective actions “If needed”.
  - Invoking **user-defined hooks** for lifecycle events (PreSync, Sync, PostSync).

- How it Works:
  - **Observes**:
    - It looks at the `Argo CD Application CRD` and the target cluster.
  - **Compares**:
    - It **fetches the desired manifests** from the repo server and **compares** them to the `actual state`.
  - **Acts**:
    - It **updates** the Application status and **synchronizes** the cluster if enabled.

![pic](./pic/architecture_components_application_controller.png)

---

### Additional Components

- `Redis`: used for caching.
- `Dex`: **identity service** to integrate with **external identity providers**.
- `ApplicationSet Controller`: It automates the **generation of Argo CD Applications**

![pic](./pic/architecture_components.png)
