# Kubernetes - ServiceAccount

[Back](../../index.md)

- [Kubernetes - ServiceAccount](#kubernetes---serviceaccount)
  - [Service Account](#service-account)
    - [Imperative Commands](#imperative-commands)
    - [Declarative Manifest](#declarative-manifest)
    - [Lab: Default Service Account](#lab-default-service-account)
    - [Lab: Create, use, and delete Service Account](#lab-create-use-and-delete-service-account)
  - [Service Account Token.](#service-account-token)
    - [Imperative Commands](#imperative-commands-1)
    - [Lab: Create Service Account Token](#lab-create-service-account-token)

---

## Service Account

- `ServiceAccount (SA)`

  - an **identity** used by Pods to **authenticate** to the Kubernetes **API server**.

- `Default ServiceAccount`

  - Every `namespace` has a `default ServiceAccount` created automatically.
  - When a `Pod` is created, it automatically uses the `default` SA unless you specify another.

- The `service account` token is mounted inside the `Pod` at: `/var/run/secrets/kubernetes.io/serviceaccount/token`

  - K8s create a **short lived token** in the pod
  - K8s rotate and **expire** the token **automatically**

- `ServiceAccount Admission Controller`:
  - the controller that creates `Service accounts` automatically and associated it with `Pods`.

---

### Imperative Commands

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

### Declarative Manifest

- `pod.spec.serviceAccountName` field:

  - specify the sa to use

- Create SA

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

---

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

### Lab: Default Service Account

```sh
kubectl get sa -A
# NAMESPACE              NAME                                          SECRETS   AGE
# default                default                                       0         62d
# envoy-gateway-system   default                                       0         26h
# envoy-gateway-system   eg-gateway-helm-certgen                       0         26h
# envoy-gateway-system   envoy-default-nginx-gateway-42c88ea3          0         26h
# envoy-gateway-system   envoy-gateway                                 0         26h
# ingress-nginx          default                                       0         8d
# ingress-nginx          ingress-nginx                                 0         8d
# ingress-nginx          ingress-nginx-admission                       0         8d
# kube-node-lease        default                                       0         62d
# kube-public            default                                       0         62d
# kube-system            attachdetach-controller                       0         62d
# kube-system            bootstrap-signer                              0         62d
# kube-system            certificate-controller                        0         62d
# kube-system            clusterrole-aggregation-controller            0         62d
# kube-system            coredns                                       0         62d
# kube-system            cronjob-controller                            0         62d
# kube-system            daemon-set-controller                         0         62d
# kube-system            default                                       0         62d
# kube-system            deployment-controller                         0         62d
# kube-system            disruption-controller                         0         62d
# kube-system            endpoint-controller                           0         62d
# kube-system            endpointslice-controller                      0         62d
# kube-system            endpointslicemirroring-controller             0         62d
# kube-system            ephemeral-volume-controller                   0         62d
# kube-system            expand-controller                             0         62d
# kube-system            generic-garbage-collector                     0         62d
# kube-system            horizontal-pod-autoscaler                     0         62d
# kube-system            job-controller                                0         62d
# kube-system            kube-proxy                                    0         62d
# kube-system            legacy-service-account-token-cleaner          0         62d
# kube-system            namespace-controller                          0         62d
# kube-system            node-controller                               0         62d
# kube-system            persistent-volume-binder                      0         62d
# kube-system            pod-garbage-collector                         0         62d
# kube-system            pv-protection-controller                      0         62d
# kube-system            pvc-protection-controller                     0         62d
# kube-system            replicaset-controller                         0         62d
# kube-system            replication-controller                        0         62d
# kube-system            resource-claim-controller                     0         62d
# kube-system            resourcequota-controller                      0         62d
# kube-system            root-ca-cert-publisher                        0         62d
# kube-system            service-account-controller                    0         62d
# kube-system            service-cidrs-controller                      0         62d
# kube-system            statefulset-controller                        0         62d
# kube-system            storage-provisioner                           0         62d
# kube-system            token-cleaner                                 0         62d
# kube-system            ttl-after-finished-controller                 0         62d
# kube-system            ttl-controller                                0         62d
# kube-system            validatingadmissionpolicy-status-controller   0         62d
# kube-system            volumeattributesclass-protection-controller   0         62d
# kube-system            vpnkit-controller                             0         62d
# kubernetes-dashboard   default                                       0         17d
# kubernetes-dashboard   kubernetes-dashboard                          0         17d
# kubernetes-dashboard   kubernetes-dashboard-api                      0         17d
# kubernetes-dashboard   kubernetes-dashboard-kong                     0         17d
# kubernetes-dashboard   kubernetes-dashboard-metrics-scraper          0         17d
# kubernetes-dashboard   kubernetes-dashboard-web                      0         17d

# default sa
kubectl get sa default
# NAME      SECRETS   AGE
# default   0         62d

kubectl describe sa default
# Name:                default
# Namespace:           default
# Labels:              <none>
# Annotations:         <none>
# Image pull secrets:  <none>
# Mountable secrets:   <none>
# Tokens:              <none>
# Events:              <none>
```

---

### Lab: Create, use, and delete Service Account

```sh
# create sa
kubectl create serviceaccount jenkins
# serviceaccount/jenkins created

# confirm
kubectl get sa
# NAME      SECRETS   AGE
# default   0         62d
# jenkins   0         72s

kubectl describe sa jenkins
# Name:                jenkins
# Namespace:           default
# Labels:              <none>
# Annotations:         <none>
# Image pull secrets:  <none>
# Mountable secrets:   <none>
# Tokens:              <none>
# Events:              <none>
```

```yaml
# demo-sa-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: jenkins
spec:
  serviceAccountName: jenkins # specify sa
  containers:
    - name: jenkins
      image: jenkins/jenkins:lts
      ports:
        - name: httpport
          containerPort: 8080
```

```sh
kubectl apply -f demo-sa-pod.yaml
# pod/jenkins created

kubectl get pod jenkins
# NAME      READY   STATUS    RESTARTS   AGE
# jenkins   1/1     Running   0          85s

# confirm sa mount
kubectl describe pod jenkins
# Containers:
#   jenkins:
#     Mounts:
#       /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-zcvvr (ro)

# confirm
kubectl get pod jenkins -o yaml
# spec:
#   serviceAccount: jenkins
#   serviceAccountName: jenkins

```

- Delete

```sh
kubectl delete pod jenkins
# pod "jenkins" deleted from default namespace

kubectl delete sa jenkins
# serviceaccount "jenkins" deleted from default namespace
```

---

## Service Account Token.

- `ServiceAccount tokens`

  - can be used outside the cluster (CI/CD, automation tools).
  - `Bearer tokens` are mounted into pods at well-known locations, and allow in-cluster processes to talk to the API server:
    - `Authorization: Bearer <token>`
  - Default token lifetime is **1 hour**.

- Useful for: CI/CD pipelines, GitHub Actions, external automation, integrating monitoring tools.

- Used for external request

```sh
curl https://cluster_ip:6443/api -insecure --header "Authorization: Bearer <token>"
```

---

### Imperative Commands

| **Command**                                                | **Description**                               |
| ---------------------------------------------------------- | --------------------------------------------- |
| `kubectl create token SA_NAME -n NAMESPACE`                | Generate a short-lived token.                 |
| `kubectl create token SA_NAME --duration=24h -n NAMESPACE` | Generate a token with custom expiration time. |

---

### Lab: Create Service Account Token

```sh
# create sa
kubectl create sa prometheus-admin
# serviceaccount/prometheus-admin created

# confirm
kubectl get sa prometheus-admin
# NAME               SECRETS   AGE
# prometheus-admin   0         7s

# create token
kubectl create token prometheus-admin
# eyJhbGciOiJSUzI1NiIsImtpZCI6IkJXZUVvaGtMaHU3enlyZzdZb0M4YjE3V2xCMUNWR1BFb3RVSGRDSWpoaWcifQ.
```
