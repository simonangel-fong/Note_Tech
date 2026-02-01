# Kubernetes - kubectl

[Back](../../index.md)

- [Kubernetes - kubectl](#kubernetes---kubectl)
  - [`kubectl`](#kubectl)
    - [Imperative Command](#imperative-command)
    - [Lab: Cluster Info](#lab-cluster-info)

---

## `kubectl`

- `kubectl`:
  - a **command line** tool for **communicating** with a Kubernetes cluster's `control plane`, using the `Kubernetes API`.

### Imperative Command

- Get object info

| CMD                                             | DESC                                            |
| ----------------------------------------------- | ----------------------------------------------- |
| `kubectl get RESOURCE`                          | List all objects of a resource                  |
| `kubectl get RESOURCE --sort-by=.metadata.name` | List and sort objects by name                   |
| `kubectl get pods --selector=key=value`         | List objects with a label                       |
| `kubectl get RESOURCE -A`                       | List all objects of a resource in all namespace |
| `kubectl get RESOURCE -o wide`                  | List all objects of a resource with more info   |
| `kubectl get RESOURCE NAME -o yaml`             | Output a resource object in yaml file           |
| `kubectl describe RESOURCE NAME`                | Output a resource object details                |
| `kubectl events --types=Warning`                | Get warning evernts                             |
| `kubectl diff -f ./MANIFEST`                    | Compares the current state against the manifest |

- Mange

| CMD                                   | DESC                                                 |
| ------------------------------------- | ---------------------------------------------------- |
| `kubectl api-resources`               | List all supported resource types                    |
| `kubectl explain RESOURCE`            | Show the documentation for a resource                |
| `kubectl create -f MANIFEST MANIFEST` | creates resources from a manifest                    |
| `kubectl replace --force -f MANIFEST` | force to replace a resource                          |
| `kubectl apply -f MANIFEST MANIFEST`  | creates and updates resources from manifests         |
| `kubectl apply -f DIR`                | creates and updates resources from a dir             |
| `kubectl apply -f REMOTE_URL`         | creates and updates resources from a remote manifest |
| `kubectl delete -f MANIFEST MANIFEST` | delete and updates resources                         |
| `kubectl create RESOURCE NAME`        | creates a resource                                   |
| `kubectl edit RESOURCE NAME`          | Edit resource's definition                           |
| `kubectl delete RESOURCE NAME`        | Delete a resource                                    |
| `kubectl patch RESOURCE NAME -p '{}'` | Patching resources                                   |

- Cluster

| CMD                                                | DESC                                                              |
| -------------------------------------------------- | ----------------------------------------------------------------- |
| `kubectl version`                                  | Display the Kubernetes version                                    |
| `kubectl cluster-info`                             | Print the address of the control plane and cluster services       |
| `kubectl cluster-info dump`                        | Exports the entire state of the cluster                           |
| `kubectl cluster-info dump --output-directory=DIR` | Exports the entire state of the cluster to a dir                  |
| `kubectl cluster-info dump --namespace NAMESPACE`  | Exports the entire state of a ns                                  |
| `kubectl api-versions`                             | List the supported API versions, in the form of "group/version".  |
| `kubectl options`                                  | List of global command-line options, which apply to all commands. |
| `kubectl proxy`                                    | Run a proxy to the Kubernetes API server.                         |

- Security

| CMD                                            | DESC                                 |
| ---------------------------------------------- | ------------------------------------ |
| `kubectl auth can-i VERB RESOURCE`             | Inspect authorization.               |
| `kubectl auth reconcile -f my-rbac-rules.yaml` | Reconcile RBAC resources from a file |

---

### Lab: Cluster Info

```sh
kubectl cluster-info
# Kubernetes control plane is running at https://192.168.10.150:6443
# CoreDNS is running at https://192.168.10.150:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

---
