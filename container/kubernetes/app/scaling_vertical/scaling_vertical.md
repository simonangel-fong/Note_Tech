# Kubernetes - Pod: Vertical Scaling

[Back](../../index.md)

- [Kubernetes - Pod: Vertical Scaling](#kubernetes---pod-vertical-scaling)
    - [In-place pod vertical scaling Feature](#in-place-pod-vertical-scaling-feature)
  - [Manually Vertical Scaling](#manually-vertical-scaling)
  - [Vertical Pod Autoscaler (VPA)](#vertical-pod-autoscaler-vpa)
    - [Components of VPA](#components-of-vpa)
    - [VPA modes](#vpa-modes)
  - [Lab: Install VPA](#lab-install-vpa)
  - [Lab: !!!Create VPA](#lab-create-vpa)

---

### In-place pod vertical scaling Feature

skip

---

## Manually Vertical Scaling

- By default, when scaling resources allocated to a pod(`kubectl edit`)
  - k8s delete the old pod and spin up the new pod with resources
- in-place pod resizing feature:

  - by setting `FEATURE_GATES=InPlacePodVerticalScaling=true`
  - without killing the pod

- Command:
  - `kubectl edit deploy/NAME`

---

## Vertical Pod Autoscaler (VPA)

- `Vertical Pod Autoscaler (VPA)`

  - a component that **automatically adjusts the CPU and memory resource** requests and limits for **individual pods** based on their actual usage.
  - by default: not built-in
    - must install
  - cannot be created by imperative command, declarative method only

- Declarative

```yaml
apiVersion: autoscaling.k8s.io/v1beta2
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
      - containerName: "my-app"
        minAllowed:
          cpu: "250m"
        maxAllowed:
          cpu: "2"
        controlledResources: ["cpu"]
```

---

### Components of VPA

- three main components:

  - `Recommender`,
  - `Updater`,
  - `Admission Controller`.

- `Recommender`:

  - **Monitors resource utilization** and **computes target values**.
  - Looks at the metric history, OOM events, and the VPA deployment spec and suggests fair requests. The limits are raised/lowered based on the limits-requests proportion defined.

- `Updater`:

  - **Evicts** those `pods` that need the new resource limits.
  - **Implements** whatever the `Recommender` recommends if `updateMode: Auto` is defined.

- `Admission Controller`:
  - **Changes** the CPU and memory **settings** (using a webhook) before a new pod starts whenever the VPA Updater evicts and restarts a pod.
  - **Evicts** a pod if it needs to change the pod’s resource requests when the `Vertical Pod Autoscaler` is set with an updateMode of “Auto.”

---

### VPA modes

| Mode       | Description                                                 |
| ---------- | ----------------------------------------------------------- |
| `Auto`     | Similar to `Recreate`.                                      |
| `Recreate` | Evicts pods if usage goes beyond range                      |
| `Initial`  | Only changes on Pod creation; **never changes** them later. |
| `Off`      | Only reconmmeds; does not change anything                   |

---

## Lab: Install VPA

- Linux Env
- ref: https://github.com/kubernetes/autoscaler/tree/9f87b78df0f1d6e142234bb32e8acbd71295585a/vertical-pod-autoscaler

```sh
# Install VPA Custom Resource Definitions (CRDs)
# allow Kubernetes to recognize the custom resources that VPA uses to function properly. 
kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/vpa-release-1.0/vertical-pod-autoscaler/deploy/vpa-v1-crd-gen.yaml
# customresourcedefinition.apiextensions.k8s.io/verticalpodautoscalercheckpoints.autoscaling.k8s.io created
# customresourcedefinition.apiextensions.k8s.io/verticalpodautoscalers.autoscaling.k8s.io created

# Install VPA Role-Based Access Control (RBAC)
# ensures that VPA has the appropriate permissions to operate within your Kubernetes cluster. 
kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/vpa-release-1.0/vertical-pod-autoscaler/deploy/vpa-rbac.yaml
# clusterrole.rbac.authorization.k8s.io/system:metrics-reader created
# clusterrole.rbac.authorization.k8s.io/system:vpa-actor created
# clusterrole.rbac.authorization.k8s.io/system:vpa-status-actor created
# clusterrole.rbac.authorization.k8s.io/system:vpa-checkpoint-actor created
# clusterrole.rbac.authorization.k8s.io/system:evictioner created
# clusterrolebinding.rbac.authorization.k8s.io/system:metrics-reader created
# clusterrolebinding.rbac.authorization.k8s.io/system:vpa-actor created
# clusterrolebinding.rbac.authorization.k8s.io/system:vpa-status-actor created
# clusterrolebinding.rbac.authorization.k8s.io/system:vpa-checkpoint-actor created
# clusterrole.rbac.authorization.k8s.io/system:vpa-target-reader created
# clusterrolebinding.rbac.authorization.k8s.io/system:vpa-target-reader-binding created
# clusterrolebinding.rbac.authorization.k8s.io/system:vpa-evictioner-binding created
# serviceaccount/vpa-admission-controller created
# serviceaccount/vpa-recommender created
# serviceaccount/vpa-updater created
# clusterrole.rbac.authorization.k8s.io/system:vpa-admission-controller created
# clusterrolebinding.rbac.authorization.k8s.io/system:vpa-admission-controller created
# clusterrole.rbac.authorization.k8s.io/system:vpa-status-reader created
# clusterrolebinding.rbac.authorization.k8s.io/system:vpa-status-reader-binding created

# Clone the repository
git clone https://github.com/kubernetes/autoscaler.git

# Run the setup script
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh

# confirm
kubectl get deploy -n kube-system
# NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
# vpa-admission-controller   1/1     1            1           4h37m
# vpa-recommender            1/1     1            1           4h37m
# vpa-updater                1/1     1            1           4h37m
```

---

## Lab: !!!Create VPA

- `flask-app-deploy.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app-4
  labels:
    app: flask-app-4
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-app-4
  template:
    metadata:
      labels:
        app: flask-app-4
    spec:
      containers:
      - name: flask-app-4
        image:  kodekloud/flask-session-app:1 
        ports:
        - name: http
          containerPort: 8080
```

- `flask-app-service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-app-4-service
  labels:
    app: flask-app-4
spec:
  type: NodePort
  selector:
    app: flask-app-4
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: 8080
    nodePort: 30080
```

```sh
kubectl create -f flask-app-deploy.yaml
# deployment.apps/flask-app-4 created

kubectl create -f flask-app-service.yaml
# service/flask-app-4-service created

# view the resource consumption of the pods
kubectl top pod
# NAME                         CPU(cores)   MEMORY(bytes)
# flask-app-4-668b99c9-479lx   2m           19Mi
# flask-app-4-668b99c9-bttkl   2m           19Mi
```

- `flask-app-vpa.yaml`

```yaml
apiVersion: "autoscaling.k8s.io/v1"
kind: VerticalPodAutoscaler
metadata:
  name: flask-app
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: flask-app-4
  updatePolicy:
    updateMode: "Off"  # You can set this to "Auto" if you want automatic updates
  resourcePolicy:
    containerPolicies:
      - containerName: '*'
        minAllowed:
          cpu: 100m
        maxAllowed:
          cpu: 1000m
        controlledResources: ["cpu"]
```

```sh
kubectl create -f vpa-cpu.yml 
# verticalpodautoscaler.autoscaling.k8s.io/flask-app created

# confirm
kubectl get vpa
# NAME        MODE   CPU   MEM   PROVIDED   AGE
# flask-app   Off                           22s
```

- Create workload

```sh
#!/bin/bash

echo "Load initiated in the background. Please do not terminate this process."

timeout 1000s bash -c 'for i in {1..10}; do (while true; do curl -s http://controlplane:30080 > /dev/null; done) & done; wait'
```