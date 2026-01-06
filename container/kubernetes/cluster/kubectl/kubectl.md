# Kubernetes - kubectl

[Back](../../index.md)

- [Kubernetes - kubectl](#kubernetes---kubectl)
  - [`kubectl`](#kubectl)
  - [kubectl apply](#kubectl-apply)

---

## `kubectl`

- `kubectl`:
  - the command line utilities
  - used to **deploy and manage applications** on a kubernetes cluster, to get cluster information, get the status of nodes in the cluster and many other things.

| CMD                    | DESC                                   |
| ---------------------- | -------------------------------------- |
| `kubectl cluster-info` | view information about the cluster     |
| `kubectl run app_name` | deploy an application on the cluster   |
| `kubectl get nodes`    | list all the nodes part of the cluster |

---

## kubectl apply

- kubectl apply

  - the local yaml file will also convert to a json file in the `last applied configuration`
  - the local yaml file will convert to a yaml file in the `live object configuration` in the control plane

- e.g., the image of a pod get changed in the local yaml

  - then API server compares and update `last applied configuration` and update it
  - API server compares with `live object configuration` and update the image

- `live object configuration`
  - reside in the k8s memory
  - the actual object status
- `last applied configuration`
  - reside in the `live object configuration` as annotation
  - helps compare with the local yaml file to identify the changes
  - only apply to `kubectl apply` command
    - not to `kubectl create/replace` (not store last applied config)

---
