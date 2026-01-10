# CKA - Node

[Back](../index.md)

- [CKA - Node](#cka---node)
  - [Node](#node)
    - [Task: Node Affinity](#task-node-affinity)
      - [Solution](#solution)

---

## Node

### Task: Node Affinity

Only schedule a Pod on the node that has a `disktype=ssd' label.

---

#### Solution

```yaml
# task-affinity.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: disktype
                operator: In
                values:
                  - ssd
  containers:
    - name: nginx
      image: nginx
```

```sh
kubectl get node -l disktype=ssd
# NAME     STATUS                     ROLES    AGE   VERSION
# node02   Ready,SchedulingDisabled   <none>   44d   v1.33.6

kubectl apply -f task-affinity.yaml
# pod/nginx created

kubectl get pod nginx
```