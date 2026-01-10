# Kubernetes - Pod: Horizontal Scaling

[Back](../../index.md)

- [Kubernetes - Pod: Horizontal Scaling](#kubernetes---pod-horizontal-scaling)
  - [Manually Horizontal Scaling](#manually-horizontal-scaling)
    - [Lab: Manual Scaling](#lab-manual-scaling)
  - [Horizontal Pod Autoscaler(HPA)](#horizontal-pod-autoscalerhpa)
    - [Imperative Commands](#imperative-commands)
    - [Declarative method](#declarative-method)
    - [Lab: Create HPA - Imperative command](#lab-create-hpa---imperative-command)
    - [Lab: Create HPA - Declarative method](#lab-create-hpa---declarative-method)

---

## Manually Horizontal Scaling

- When there are insufficient resources for cluster,
  - the command `kubectl scale` leads to some pods reach the limit, and unscaled pods **remain pending state**.

| CMD                                                      | DESC                                                                     |
| -------------------------------------------------------- | ------------------------------------------------------------------------ |
| `kubectl top nodes`                                      | List all nodes' CPU and memory consumption                               |
| `kubectl top pods`                                       | List all pods' CPU and memory consumption                                |
| `kubectl scale rs/NAME --replicas=N`                     | Scale a ReplicaSet directly (rare—usually let the Deployment manage it). |
| `kubectl scale deploy/NAME --replicas=N`                 | Scale Deployment replica count. Preferred for stateless services.        |
| `kubectl scale sts/NAME --replicas=N`                    | Scale a StatefulSet (ordered, one-by-one; respect storage/identity).     |
| `kubectl edit deploy/NAME`                               | Open editor; set `.spec.replicas` manually, then save to apply.          |
| `kubectl patch deploy/NAME -p '{"spec":{"replicas":N}}'` | Quick JSON patch to set replicas without an editor.                      |

---

### Lab: Manual Scaling

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: nginx
          resources:
            requests:
              cpu: "250m"
            limits:
              cpu: "500m"
```

```sh
kubectl create -f app-deploy.yaml && kubectl rollout status deploy my-app
# deployment.apps/my-app created
# Waiting for deployment "my-app" rollout to finish: 0 of 1 updated replicas are available...
# deployment "my-app" successfully rolled out

# confirm
kubectl get pod
# NAME                      READY   STATUS    RESTARTS        AGE
# my-app-7cb77b7584-dcf5f   1/1     Running   0                20s

# manually monitor resource consumption
kubectl top pod my-app-7cb77b7584-dcf5f
# NAME                      CPU(cores)   MEMORY(bytes)
# my-app-7cb77b7584-dcf5f   0m           4Mi

# manually scale pod
kubectl scale deploy my-app --replicas=3 && kubectl rollout status deploy my-app
# deployment.apps/my-app scaled
# Waiting for deployment "my-app" rollout to finish: 1 out of 3 new replicas have been updated...
# Waiting for deployment "my-app" rollout to finish: 1 of 3 updated replicas are available...
# Waiting for deployment "my-app" rollout to finish: 2 of 3 updated replicas are available...
# deployment "my-app" successfully rolled out

# confirm
kubectl get deploy
# NAME     READY   UP-TO-DATE   AVAILABLE   AGE
# my-app   3/3     3            3           2m33s

# cleanup
kubectl delete deploy my-app
# deployment.apps "my-app" deleted from default namespace

```

---

## Horizontal Pod Autoscaler(HPA)

- `Horizontal Pod Autoscaler(HPA)`

  - an **API resource and controller** that **automatically adjusts** the number of Pod **replicas** in a `Deployment`, `StatefulSet`, or `ReplicaSet`.
    - continuously monitor the metrics,
    - automatically scale the number of pods,
    - balance the thresholds,
    - track multiple metrics.
  - since version 1.23
  - prerequistie: metric server
  - metrics from
    - internal sources:
      - metrics server
      - custom metric adapter
    - external sources
      - datadog
      - dynatrace

- HPA requires
  - metric server
  - resource limits defined in pod
    - otherwise the target in hpa shows **unknown** instead of the % of the CPU usage.

---

### Imperative Commands

- Manage

| CMD                         | DESC                                                                   |
| --------------------------- | ---------------------------------------------------------------------- |
| `kubectl top pods`          | Check live CPU/MEM.                                                    |
| `kubectl get hpa`           | List HPAs.                                                             |
| `kubectl describe hpa/NAME` | Show details: metrics, events, scale decisions, stabilization windows. |
| `kubectl edit hpa/NAME`     | Change min/max replicas, metrics, or behavior.                         |
| `kubectl delete hpa/NAME`   | Remove autoscaling so manual replicas sticks.                          |

- Create

| CMD                                                                      | DESC                             |
| ------------------------------------------------------------------------ | -------------------------------- |
| `kubectl autoscale deploy/NAME --min=MIN --max=MAX --cpu-percent=TARGET` | Create an HPA for a Deployment.  |
| `kubectl autoscale sts/NAME --min=MIN --max=MAX --cpu-percent=TARGET`    | Create an HPA for a StatefulSet. |

---

### Declarative method

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
```

---

### Lab: Create HPA - Imperative command

- Create deployment

```yaml
# app-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: nginx
          resources:
            requests:
              cpu: "250m"
            limits:
              cpu: "500m"
```

```sh
kubectl create -f app-deploy.yaml && kubectl rollout status deploy my-app
# deployment.apps/my-app created
# Waiting for deployment "my-app" rollout to finish: 0 of 1 updated replicas are available...
# deployment "my-app" successfully rolled out

# confirm
kubectl get deploy
# NAME     READY   UP-TO-DATE   AVAILABLE   AGE
# my-app   1/1     1            1           114s

# create a HPA for a deployment, min number of pod:1, max pods:10
kubectl autoscale deploy my-app --cpu=50% --min=1 --max=10
# horizontalpodautoscaler.autoscaling/my-app autoscaled

# confirm
kubectl get hpa
# NAME     REFERENCE           TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
# my-app   Deployment/my-app   cpu: 0%/50%   1         10        1          21s

kubectl describe hpa my-app
# Name:                                                  my-app
# Namespace:                                             default
# Labels:                                                <none>
# Annotations:                                           <none>
# CreationTimestamp:                                     Fri, 31 Oct 2025 17:43:25 -0400
# Reference:                                             Deployment/my-app
# Metrics:                                               ( current / target )
#   resource cpu on pods  (as a percentage of request):  0% (0) / 50%
# Min replicas:                                          1
# Max replicas:                                          10
# Deployment pods:                                       1 current / 1 desired
# Conditions:
#   Type            Status  Reason               Message
#   ----            ------  ------               -------
#   AbleToScale     True    ScaleDownStabilized  recent recommendations were higher than current one, applying the highest recent recommendation
#   ScalingActive   True    ValidMetricFound     the HPA was able to successfully calculate a replica count from cpu resource utilization (percentage of request)
#   ScalingLimited  False   DesiredWithinRange   the desired count is within the acceptable range
# Events:           <none>

# update: 50% -> 30%
kubectl edit hpa my-app
# horizontalpodautoscaler.autoscaling/my-app edited

# confirm
kubectl get hpa
# NAME     REFERENCE           TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
# my-app   Deployment/my-app   cpu: 0%/30%   1         10        1          3m6s

# delete
kubectl delete hpa my-app
# horizontalpodautoscaler.autoscaling "my-app" deleted from default namespace
```

---

### Lab: Create HPA - Declarative method

```yaml
# my-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app-deploy
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
```

```sh
kubectl create -f my-hpa.yaml
# horizontalpodautoscaler.autoscaling/web-hpa created

kubectl get hpa
# NAME      REFERENCE               TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
# web-hpa   Deployment/app-deploy   cpu: <unknown>/60%   2         10        0          32s

kubectl delete hpa web-hpa
# horizontalpodautoscaler.autoscaling "web-hpa" deleted from default namespace
```
