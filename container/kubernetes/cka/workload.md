# CKA - Workload

[Back](../index.md)

- [CKA - Workload](#cka---workload)
  - [HPA](#hpa)
    - [TASK: Autoscaling](#task-autoscaling)
    - [Solution](#solution)

---

## HPA

### TASK: Autoscaling

Deploy a sample workload and configure Horizontal Pod Autoscaling for it. Specifically:
. Use the existing deployment `cpu-demo'
. Configure an HPA to scale this deployment from 1 up to 5 replicas when the average CPU utilization exceeds 50%.

- Setup Environment

```sh
kubectl create deploy cpu-demo --image=busybox -- sleep infinity 
```

---

### Solution

```sh
kubectl autoscale deploy/cpu-demo --min=1 --max=5 --cpu=50%
# horizontalpodautoscaler.autoscaling/cpu-demo autoscaled

kubectl get hpa
# NAME       REFERENCE             TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
# cpu-demo   Deployment/cpu-demo   cpu: <unknown>/50%   1         5         1          84s

kubectl describe hpa cpu-demo
# Metrics:                                               ( current / target )
#   resource cpu on pods  (as a percentage of request):  <unknown> / 50%
# Min replicas:                                          1
# Max replicas:                                          5


```