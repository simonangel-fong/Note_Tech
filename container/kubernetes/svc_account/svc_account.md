# Kubernetes - ServiceAccount

[Back](../index.md)

- [Kubernetes - ServiceAccount](#kubernetes---serviceaccount)
  - [Account](#account)
  - [Imperative Commands](#imperative-commands)
  - [Declarative](#declarative)
  - [Token](#token)
  - [Imperative Commands](#imperative-commands-1)

---

## Account

- 2 types of accounts

  - user account
    - the account used by human
  - service account
    - the account used by machines, bots
    - used to authenticate the request by services
    - use token for authentication

---

- `ServiceAccount (SA)`

  - an **identity** used by Pods to **authenticate** to the Kubernetes API server.
  - Every namespace has a `default` ServiceAccount created automatically.
  - When a Pod is created, it automatically uses the `default` SA unless you specify another.

- The service account token is mounted inside the Pod at: `/var/run/secrets/kubernetes.io/serviceaccount/token`

---

## Imperative Commands

| **Command**                                                                               | **Description**                                   |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `kubectl get sa -A`                                                                       | List _all_ ServiceAccounts across namespaces.     |
| `kubectl get serviceaccounts -n NAMESPACE`                                                | List all ServiceAccounts in a namespace.          |
| `kubectl describe serviceaccount NAME -n NAMESPACE`                                       | Show details.                                     |
| `kubectl create serviceaccount NAME -n NAMESPACE`                                         | Create a ServiceAccount in a namespace.           |
| `kubectl delete serviceaccount NAME -n NAMESPACE`                                         | Delete a ServiceAccount.                          |
| `kubectl run PODNAME --image=nginx --serviceaccount=NAME -n NS`                           | Create a Pod that uses a specific ServiceAccount. |
| `kubectl patch serviceaccount NAME -p '{"imagePullSecrets":[{"name":"mysecret"}]}' -n NS` | Attach an imagePullSecret to an SA.               |

---

## Declarative

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: prometheus
  namespace: default
```

- Associate a service account with a pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: prometheus
spec:
  serviceAccountName: prometheus
```

- K8s create a short lived token in the pod
- K8s rotate and expire the token automatically

---

- Disable auto-mount for SA

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dashboard-sa
  namespace: default
automountServiceAccountToken: false # disable auto mount token
```

- Disable auto-mount for a pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: prometheus
spec:
  serviceAccountName: prometheus
  automountServiceAccountToken: false # disable auto mount token
```

---

## Token

- ServiceAccount `tokens`

  - can be used outside the cluster (CI/CD, automation tools).
  - They authenticate to the API server using:
    - `Authorization: Bearer <token>`
  - Default token lifetime is 1 hour.
  - Useful for: CI/CD pipelines, GitHub Actions, external automation, integrating monitoring tools.

- Used for external request

```sh
curl https://cluster_ip:6443/api -insecure --header "Authorization: Bearer <token>"
```

---

## Imperative Commands

| **Command**                                             | **Description**                               |
| ------------------------------------------------------- | --------------------------------------------- |
| `kubectl create token NAME -n NAMESPACE`                | Generate a short-lived token.                 |
| `kubectl create token NAME --duration=24h -n NAMESPACE` | Generate a token with custom expiration time. |
