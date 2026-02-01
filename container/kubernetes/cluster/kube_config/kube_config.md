# Kubernetes - `kubectl config`

[Back](../../index.md)

- [Kubernetes - `kubectl config`](#kubernetes---kubectl-config)
  - [Configuration](#configuration)
    - [Imperative Command](#imperative-command)
    - [Lab: `config` file](#lab-config-file)
    - [Lab: `kube config` set context](#lab-kube-config-set-context)

---

## Configuration

- Config file
  - default:
    - `$HOME/.kube/config`
  - can be specified:
    - env var `KUBECONFIG`
    - `--kubeconfig` option:
      - e.g.: `kubectl get node --kubeconfig`
- Context entries:
  - cluster
  - user
  - credentials

---

### Imperative Command

| CMD                                                | DESC                                                              |
| -------------------------------------------------- | ----------------------------------------------------------------- |
| `kubectl config get-contexts`                      | Describe one or many contexts                                     |
| `kubectl config view`                              | Display merged kubeconfig settings or a specified kubeconfig file |
| `kubectl config current-context`                   | Display the current-context                                       |
| `kubectl config use-context CONTEXT`               | Set the current-context in a kubeconfig file                      |
| `kubectl config rename-context OLD NEW`            | Rename a context from the kubeconfig file                         |
| `kubectl config set-context --current --key=value` | Set the current context entry in kubeconfig                       |
| `kubectl config set-context CONTEXT --key=value`   | Set a context entry in kubeconfig                                 |
| `kubectl config delete-context CONTEXT`            | Delete the specified context from the kubeconfig                  |
| `kubectl config get-users`                         | Display users defined in the kubeconfig                           |
| `kubectl config delete-user`                       | Delete the specified user from the kubeconfig                     |
| `kubectl config set`                               | Set an individual value in a kubeconfig file                      |
| `kubectl config unset KEY.VALUE`                   | Unset an individual value in a kubeconfig file                    |
| `kubectl config get-clusters`                      | Display clusters defined in the kubeconfig                        |
| `kubectl config set-cluster`                       | Set a cluster entry in kubeconfig                                 |
| `kubectl config delete-cluster`                    | Delete the specified cluster from the kubeconfig                  |
| `kubectl config set-credentials`                   | Set a user entry in kubeconfig                                    |

---

### Lab: `config` file

```sh
cat ~/.kube/config
# apiVersion: v1
# kind: Config
# users:
# - name: kubernetes-admin
#   user:
#     client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tC...
#     client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJV...
# clusters:
# - cluster:
#     certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0...
#     server: https://192.168.10.150:6443
#   name: kubernetes
# contexts:
# - context:
#     cluster: kubernetes
#     user: kubernetes-admin
#   name: kubernetes-admin@kubernetes
# current-context: kubernetes-admin@kubernetes
# preferences: {}
```

---

### Lab: `kube config` set context

```sh
# view current context
kubectl config view
# apiVersion: v1
# kind: Config
# users:
# - name: kubernetes-admin
#   user:
#     client-certificate-data: DATA+OMITTED
#     client-key-data: DATA+OMITTED
# clusters:
# - cluster:
#     certificate-authority-data: DATA+OMITTED
#     server: https://192.168.10.150:6443
#   name: kubernetes
# contexts:
# - context:
#     cluster: kubernetes
#     user: kubernetes-admin
#   name: kubernetes-admin@kubernetes
# current-context: kubernetes-admin@kubernetes
# preferences: {}

# list context
kubectl config get-contexts
# CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
# *         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin

# list contexts names
kubectl config get-contexts -o name
# kubernetes-admin@kubernetes

# set namespace
kubectl config set-context --current --namespace kube-system
# Context "kubernetes-admin@kubernetes" modified.

kubectl config view
# - context:
#     cluster: kubernetes
#     namespace: kube-system

kubectl get po
# NAME                                   READY   STATUS    RESTARTS      AGE
# coredns-668d6bf9bc-7g786               1/1     Running   2 (20m ago)   7d21h
# coredns-668d6bf9bc-m8qmh               1/1     Running   2 (20m ago)   7d21h
# etcd-controlplane                      1/1     Running   2 (20m ago)   7d22h
# kube-apiserver-controlplane            1/1     Running   2 (20m ago)   7d22h
# kube-controller-manager-controlplane   1/1     Running   2 (20m ago)   7d22h
# kube-proxy-5kcw4                       1/1     Running   2 (20m ago)   7d21h
# kube-proxy-6pnx2                       1/1     Running   0             7d21h
# kube-proxy-kfjxb                       1/1     Running   0             7d21h
# kube-scheduler-controlplane            1/1     Running   2 (20m ago)   7d22h
```

---
