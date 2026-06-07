# Kubernetes Cluster - Controller Manager

[Back](../../index.md)

- [Kubernetes Cluster - Controller Manager](#kubernetes-cluster---controller-manager)
  - [Configuration](#configuration)
  - [Controller Manager](#controller-manager)
  - [Controllers](#controllers)
  - [Common Controllers](#common-controllers)
    - [Workload controllers](#workload-controllers)
    - [Node \& service discovery](#node--service-discovery)
    - [Config \& security](#config--security)
    - [Storage](#storage)
    - [Autoscaling \& disruption](#autoscaling--disruption)
  - [Lab: Controller Manager Failure](#lab-controller-manager-failure)

---

## Configuration

1. API server connection

| Options                       | Description                                                                   |
| ----------------------------- | ----------------------------------------------------------------------------- |
| `--kubeconfig`                | Kubeconfig used by the controller manager to connect to the kube-apiserver.   |
| `--authentication-kubeconfig` | Kubeconfig used to connect to the API server for token authentication checks. |
| `--authorization-kubeconfig`  | Kubeconfig used to connect to the API server for authorization checks.        |

2. Controller behavior

| Options                             | Description                                                                                                   |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `--controllers`                     | List of controllers to enable or disable. `*` enables all default controllers; `-name` disables a controller. |
| `--leader-elect`                    | Enables leader election so only one controller manager instance is active in an HA control plane.             |
| `--use-service-account-credentials` | Runs each controller using its own service account credentials instead of one shared credential.              |

3. Node and Pod CIDR management

| Options                 | Description                                                                                       |
| ----------------------- | ------------------------------------------------------------------------------------------------- |
| `--allocate-node-cidrs` | Enables the controller manager to allocate Pod CIDR ranges to nodes. Requires `--cluster-cidr`.   |
| `--cluster-cidr`        | CIDR range used for Pod IP allocation across the cluster. Used when `--allocate-node-cidrs=true`. |

4. Service networking

| Options                      | Description                                                 |
| ---------------------------- | ----------------------------------------------------------- |
| `--service-cluster-ip-range` | CIDR range used for Kubernetes Service ClusterIP addresses. |

5. Certificates and signing

| Options                          | Description                                                                                                      |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `--cluster-signing-cert-file`    | CA certificate used by the controller manager to sign cluster certificates, such as kubelet client certificates. |
| `--cluster-signing-key-file`     | Private key used with `--cluster-signing-cert-file` to sign cluster certificates.                                |
| `--root-ca-file`                 | Root CA certificate included in service account token secrets so Pods can trust the API server.                  |
| `--client-ca-file`               | CA certificate used to verify client certificates for requests to the controller manager.                        |
| `--requestheader-client-ca-file` | CA certificate used to verify front-proxy client certificates for request-header authentication.                 |

6. Service account token handling

| Options                              | Description                                                                                      |
| ------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `--service-account-private-key-file` | Private key used to sign legacy service account tokens.                                          |
| `--use-service-account-credentials`  | Runs each controller using its own service account credentials instead of one shared credential. |

7. Serving / endpoint configuration

| Options          | Description                                                                          |
| ---------------- | ------------------------------------------------------------------------------------ |
| `--bind-address` | IP address where the controller manager listens for its secure endpoint and metrics. |

---

- example: controller-manager

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: kube-controller-manager
      command:
        - kube-controller-manager
        - --allocate-node-cidrs=true
        - --authentication-kubeconfig=/etc/kubernetes/controller-manager.conf
        - --authorization-kubeconfig=/etc/kubernetes/controller-manager.conf
        - --bind-address=127.0.0.1
        - --client-ca-file=/etc/kubernetes/pki/ca.crt
        - --cluster-cidr=10.244.0.0/16
        - --cluster-name=kubernetes
        - --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt
        - --cluster-signing-key-file=/etc/kubernetes/pki/ca.key
        - --controllers=*,bootstrapsigner,tokencleaner
        - --kubeconfig=/etc/kubernetes/controller-manager.conf
        - --leader-elect=true
        - --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
        - --root-ca-file=/etc/kubernetes/pki/ca.crt
        - --service-account-private-key-file=/etc/kubernetes/pki/sa.key
        - --service-cluster-ip-range=10.96.0.0/12
        - --use-service-account-credentials=true
      image: registry.k8s.io/kube-controller-manager:v1.32.11
      imagePullPolicy: IfNotPresent
      volumeMounts:
        - mountPath: /etc/ssl/certs
          name: ca-certs
          readOnly: true
        - mountPath: /etc/ca-certificates
          name: etc-ca-certificates
          readOnly: true
        - mountPath: /usr/libexec/kubernetes/kubelet-plugins/volume/exec
          name: flexvolume-dir
        - mountPath: /etc/kubernetes/pki
          name: k8s-certs
          readOnly: true
        - mountPath: /etc/kubernetes/controller-manager.conf
          name: kubeconfig
          readOnly: true
        - mountPath: /usr/local/share/ca-certificates
          name: usr-local-share-ca-certificates
          readOnly: true
        - mountPath: /usr/share/ca-certificates
          name: usr-share-ca-certificates
          readOnly: true
```

---

## Controller Manager

- `Controller Manager`
  - A `control plane` component that runs `controller processes`, which continuously monitor the cluster through the `API Server` and reconcile the **actual** cluster state to match the **desired** state.
  - act as the **automation brain**
    - **constantly watching** the `API Server` and **taking action** to drive the system **toward the declared configuration**.

- a `control plane` **service** that runs on `master node(s)`, hosting **multiple** controllers in **one process** to ensure the **cluster state** matches the **desired state**.

- Roles of controllers
  - **Watching resource objects** via the API Server.
  - **Detecting differences** between **desired** state (from etcd) and **actual** state
  - Reconciling: taking corrective action to move toward the desired state.

- `Kubernetes Controller Manager (kube-controller-manager)`
  - a single process to manage all controllers
  - `ps -aux | grep kube-controller-manager`

---

```sh
kubectl get pods -n kube-system
# kube-controller-manager-docker-desktop   1/1     Running   126 (4h2m ago)   148d
```

---

## Controllers

- `controllers`
  - a **control loops** that **watch the state** of cluster, then make or request changes where needed.

---

## Common Controllers

### Workload controllers

| Controller               | Description                                                                |
| ------------------------ | -------------------------------------------------------------------------- |
| `ReplicaSet Controller`  | Keeps an exact number of identical Pods running.                           |
| `Deployment Controller`  | Manages stateless apps via ReplicaSets; handles rolling updates/rollbacks. |
| `StatefulSet Controller` | Stable Pod IDs and storage; ordered rollout/scale for stateful apps.       |
| `DaemonSet Controller`   | Ensures one Pod per (matching) node (agents, CNIs, CSI nodes).             |
| `Job Controller`         | Runs Pods to completion with retries/backoff.                              |
| `CronJob Controller`     | Schedules Jobs on a cron timetable.                                        |

---

### Node & service discovery

| Controller                             | Description                                                       |
| -------------------------------------- | ----------------------------------------------------------------- |
| `Node controller Controller`           | Tracks node health; taints/evicts from NotReady nodes.            |
| `Endpoints / EndpointSlice Controller` | Maintains Service → Pod endpoint lists for traffic routing.       |
| `Service controller` (cloud)           | Creates/updates external load balancers for `type: LoadBalancer`. |

---

### Config & security

| Controller                                   | Description                                                  |
| -------------------------------------------- | ------------------------------------------------------------ |
| `ServiceAccount Controller`                  | Creates default ServiceAccounts in namespaces.               |
| `Token Controller`                           | Manages projected service account tokens for Pods.           |
| `ResourceQuota Controller`                   | Enforces per-namespace quotas (CPU/mem/PVCs, etc.).          |
| `LimitRange Controller`                      | Sets default/max/min resource requests/limits per namespace. |
| `Namespace Controller`                       | Finalizes resources during namespace deletion.               |
| `Garbage Collector Controller`               | Cleans up dependents via ownerReferences/finalizers.         |
| `TTLAfterFinished Controller`                | Deletes completed Jobs/Pods after a set TTL.                 |
| `CertificateSigningRequest (CSR) Controller` | Approves/signs node/user certs per policy (if enabled).      |

---

### Storage

| Controller                                | Description                                        |
| ----------------------------------------- | -------------------------------------------------- |
| `PersistentVolume (PV) binder Controller` | Binds PVCs to PVs per StorageClass & access modes. |
| `Attach/Detach Controller`                | Safely attaches/detaches volumes to nodes.         |
| `Volume expansion Controller`             | Handles PVC resize (online if driver supports it). |

---

### Autoscaling & disruption

| Controller                                 | Description                                                  |
| ------------------------------------------ | ------------------------------------------------------------ |
| `HorizontalPodAutoscaler (HPA) Controller` | Scales replicas based on metrics (CPU/memory/custom).        |
| `PodDisruptionBudget (PDB) Controller`     | Limits voluntary disruptions to keep minimum Pods available. |

---

## Lab: Controller Manager Failure

```sh
# disable controler manager by rename the manifest
cd /etc/kubernetes/manifests
ls
# etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-scheduler.yaml

sudo mv kube-controller-manager.yaml .kube-controller-manager.yaml

# confirm
kubectl get po -n kube-system | grep controller
# none

# create deployment
kubectl create deployment web --image=nginx --replicas=3
# deployment.apps/web created

kubectl get deploy
# NAME   READY   UP-TO-DATE   AVAILABLE   AGE
# web    0/3     0            0           18s

kubectl get po
# none

# restore manifest
sudo mv .kube-controller-manager.yaml kube-controller-manager.yaml
# confirm
kubectl get po -n kube-system | grep controller
# kube-controller-manager-controlplane        1/1     Running       0               24s

kubectl get deploy
# NAME   READY   UP-TO-DATE   AVAILABLE   AGE
# web    3/3     3            3           3m9s

kubectl get po
# NAME                   READY   STATUS    RESTARTS   AGE
# web-65d846d465-29rvx   1/1     Running   0          43s
# web-65d846d465-pf6wx   1/1     Running   0          43s
# web-65d846d465-q86f9   1/1     Running   0          43s

```
