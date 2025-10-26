# Kubernetes - Taints and Tolerations

[Back](../../index.md)

- [Kubernetes - Taints and Tolerations](#kubernetes---taints-and-tolerations)
  - [Taints \& Tolerations](#taints--tolerations)
  - [Use Cases](#use-cases)
  - [Imperative Commands](#imperative-commands)
  - [Lab: Taint NoSchedule Effect](#lab-taint-noschedule-effect)
  - [Lab: Taint NoExecute Effect](#lab-taint-noexecute-effect)

---

## Taints & Tolerations

- `taint`

  - a **restriction** applied to a `node` that prevent `pods` from being **scheduled** onto the Node unless allowed.
    - set on the node
  - format: `key=value:effect`
    - key/value pair to identify the toleration that is allowed.
  - By default in Kubernetes, the `control-plane` / `master Node` is **tainted** so that regular Pods are not scheduled onto it.

- By default, master node usually gets taints to prevent pod other than control-plane.

  - `kubectl describe node kubemaster | grep Taint`

- Effects options:
  - `NoSchedule`
    - **New** Pods without matching `toleration` are **not scheduled**.
  - `PreferNoSchedule`:
    - Scheduler tries to avoid placing Pods, but not strictly enforced.
  - `NoExecute`
    - Prevents **scheduling** and **evicts** **existing** non-tolerating Pods.

---

- `Tolerations`

  - a **exceptions** applied to a `pod` that **allow pods to be scheduled** even if a `taint` **exists** on a node.
  - set on the pod, allowing a pod to be scheduled
    - key/value pair identifys toleration that is allowed
      - e.g., taint: `app=web:NoSchedule` == toleration `app=web`

- With `taint`

  - `Taints` on `Nodes` **repel** `Pods`.
  - `Tolerations` on `Pods` allow **exceptions**.
  - But `toleration` alone does **not guarantee** `scheduling` on a `tainted` Node
    - it just makes it **possible**.
    - Kubernetes still considers other scheduling rules (like resource requests, affinities, etc.).

- e.g.:

```yaml
spec:
  tolerations:
    - key: "key"
      operator: "Equal"
      value: "value"
      effect: "NoSchedule"
```

---

## Use Cases

- **Dedicated nodes**
  - Ensure that **only specific workloads** (e.g., databases, monitoring agents) run on **certain nodes**.
- **Node maintenance / cordon**
  - Temporarily taint nodes so no new Pods are scheduled.
- **Special hardware** (e.g., GPU nodes)
  - Taint GPU nodes; only GPU workloads with tolerations can land there.
- **Critical system Pods**
  - Nodes can be tainted `NoExecute` so only Pods with tolerations (like kube-dns) survive.

---

## Imperative Commands

| **CMD**                                                    | **DESC**                                                                    |
| ---------------------------------------------------------- | --------------------------------------------------------------------------- |
| `kubectl describe node node_name \| grep Taint`            | Get taint info from a node                                                  |
| `kubectl taint nodes node_name key=value:NoSchedule`       | Taint to a Node; **prevents** scheduling Pods without matching toleration.  |
| `kubectl taint nodes node_name key=value:PreferNoSchedule` | Taint to a Node; scheduler **avoids** placing Pods there, but not strictly. |
| `kubectl taint nodes node_name key=value:NoExecute`        | Taint; **blocks** new Pods without toleration and evicts existing ones.     |
| `kubectl taint nodes node_name key=value:NoSchedule-`      | Remove a specific taint from a Node (note the trailing `-`).                |
| `kubectl describe node node_name`                          | Show details of a Node, including its taints.                               |

---

## Lab: Taint NoSchedule Effect

```sh
# get the taint info
kubectl describe node minikube | grep Taint
# Taints:             <none>

# add taint
kubectl taint node minikube app=web:NoSchedule
# node/minikube tainted

kubectl describe node minikube | grep Taint
# Taints:             app=web:NoSchedule
```

---

- Create pod without toleration

```sh
kubectl run nginx --image=nginx
# pod/nginx created

kubectl get pod
# NAME        READY   STATUS    RESTARTS   AGE
# nginx       0/1     Pending   0          3s
```

- Create pod with toleration

```sh
tee pod-toleration.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx-con
    image: nginx
  tolerations:
  - key: "app"
    operator: "Equal"
    value: "web"
    effect: "NoSchedule"
EOF

kubectl apply -f pod-toleration.yaml
# pod/nginx-pod created

kubectl get pod
# NAME        READY   STATUS    RESTARTS   AGE
# nginx       0/1     Pending   0          46s
# nginx-pod   1/1     Running   0          4s
```

- Delete taint

```sh
kubectl taint node minikube app=web:NoSchedule-
# node/minikube untainted

kubectl describe node minikube | grep Taint
# Taints:             <none>

kubectl get pod
# NAME        READY   STATUS    RESTARTS   AGE
# nginx       1/1     Running   0          110s
# nginx-pod   1/1     Running   0          68s
```

---

## Lab: Taint NoExecute Effect

- Create pod before tainting

```sh
# get the taint info
kubectl describe node minikube | grep Taint
# Taints:             <none>

kubectl run nginx --image=nginx
# pod/nginx created

kubectl get pod
# NAME    READY   STATUS    RESTARTS   AGE
# nginx   1/1     Running   0          9s
```

- taint node

```sh
# tain a node
kubectl taint node minikube app=web:NoExecute
# node/minikube tainted

# confirm
kubectl describe node minikube | grep Taint
# Taints:             app=web:NoExecute

# get existing pod
kubectl get pod
# No resources found in default namespace.
```

- Create pod with toleration

```sh
tee pod-toleration.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx-con
    image: nginx
  tolerations:
  - key: "app"
    operator: "Equal"
    value: "web"
    effect: "NoExecute"
EOF

kubectl apply -f pod-toleration.yaml
# pod/nginx-pod created

kubectl get pod
# NAME        READY   STATUS    RESTARTS   AGE
# nginx-pod   1/1     Running   0          5s
```

- Remove taint and create pod wihtout toleration

```sh
kubectl taint node minikube app=web:NoExecute-
# node/minikube untainted

kubectl describe node minikube | grep Taints
# Taints:             <none>

kubectl run ngin --image=nginx
# pod/ngin created

kubectl get pod
# NAME        READY   STATUS    RESTARTS   AGE
# ngin        1/1     Running   0          17s
# nginx-pod   1/1     Running   0          3m3s
```

- Clean up

```sh
kubectl delete pod ngin nginx-pod
# pod "ngin" deleted from default namespace
# pod "nginx-pod" deleted from default namespace
```
