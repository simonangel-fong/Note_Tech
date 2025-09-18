# Kubernetes - Controller Manager

[Back](../index.md)

- [Kubernetes - Controller Manager](#kubernetes---controller-manager)
  - [Controller Manager](#controller-manager)
  - [Node Controller](#node-controller)
  - [Replication Controller](#replication-controller)
  - [Deployment Controller](#deployment-controller)
  - [Namespace Controller](#namespace-controller)
  - [Endpoint Controller](#endpoint-controller)
  - [Job Controller](#job-controller)
  - [PV Protection Controller](#pv-protection-controller)
  - [PV-Binder Controller](#pv-binder-controller)
  - [Service Account Controller](#service-account-controller)
  - [Stateful-Set](#stateful-set)
  - [Replicaset](#replicaset)
  - [CronJob](#cronjob)

---

## Controller Manager

- Responsibilities

  - watch status
  - remediate situation

- controller

  - a process that
    - continuously monitors the state of various components within the system
    - takes necessary actions to remediate the situation

- `Controller Manager`
  - a single process to manage all controllers
  - `ps -aux | grep kube-controller-manager`

---

```sh
kubectl get pods -n kube-system
# kube-controller-manager-docker-desktop   1/1     Running   126 (4h2m ago)   148d
```

---

## Node Controller

- `node controller`
  - used to monitor the status of the nodes
  - ensure to bring the whole system to the desired functioning state.
  - watch node status via `api server`
  - default
    - check the status of the nodes every 5 seconds
    - mark the node as `unreachable` if it cannot receive heartbeat for 40s.
    - give the `unreachable` node 5 min to come back
    - remove the `pods` running on `unreachable node`
      - provision the removed `pods` on a healthy ones.

---

## Replication Controller

- `replication controller`
  - used to monitor the status of the replica sets
  - ensure the desired number of pods are available at all times within the set.
    - if a pod dies, it creates another one
  - watch node status via `api server`

## Deployment Controller

## Namespace Controller

## Endpoint Controller

## Job Controller

## PV Protection Controller

## PV-Binder Controller

## Service Account Controller

## Stateful-Set

## Replicaset

## CronJob
