# Kubernetes: Container - Co-located Containers

[Back](../../index.md)

- [Kubernetes: Container - Co-located Containers](#kubernetes-container---co-located-containers)
  - [Co-located Containers](#co-located-containers)
    - [Lab: Co-located Containers](#lab-co-located-containers)

---

## Co-located Containers

- `co-located containers`
  - individual **containers** that run together inside a Pod
  - containers are **equal partners** inside the Pod.
    - all start together, not in a sequence

---

- Manifest File

```yaml
spec:
  containers:
    - name: main-1
    - name: main-2
```

---

### Lab: Co-located Containers

- `colocated_container.yaml`

```yaml
# demo-container-colocated.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-container-colocated
spec:
  containers:
    - name: main-01
      image: busybox
      command:
        - "sh"
        - "-c"
      args:
        - |
          echo "$(date) main-01 start."
          while true; do
             echo "$(date) main-01 running...";
             sleep 1;
          done
    - name: main-02
      image: busybox
      command:
        - "sh"
        - "-c"
      args:
        - |
          echo "$(date) main-02 start."
          while true; do
             echo "$(date) main-02 running...";
             sleep 1;
          done
```

```sh
kubectl apply -f demo-container-colocated.yaml
# pod/demo-container-colocated created

kubectl get pod -w
# NAME                       READY   STATUS    RESTARTS   AGE
# demo-container-colocated   0/2     Pending   0          0s
# demo-container-colocated   0/2     Pending   0          0s
# demo-container-colocated   0/2     ContainerCreating   0          0s
# demo-container-colocated   2/2     Running             0          4s

kubectl describe pod demo-container-colocated
# Containers:
#   main-01:
#     State:          Running
#     Ready:          True
#   main-02:
#     State:          Running
#     Ready:          True

# Events:
#   Type    Reason     Age   From               Message
#   ----    ------     ----  ----               -------
#   Normal  Scheduled  103s  default-scheduler  Successfully assigned default/demo-container-colocated to docker-desktop
#   Normal  Pulling    103s  kubelet            Pulling image "busybox"
#   Normal  Pulled     102s  kubelet            Successfully pulled image "busybox" in 1.158s (1.158s including waiting). Image size: 2224358 bytes.
#   Normal  Created    102s  kubelet            Created container: main-01
#   Normal  Started    102s  kubelet            Started container main-01
#   Normal  Pulling    102s  kubelet            Pulling image "busybox"
#   Normal  Pulled     101s  kubelet            Successfully pulled image "busybox" in 964ms (964ms including waiting). Image size: 2224358 bytes.
#   Normal  Created    101s  kubelet            Created container: main-02
#   Normal  Started    100s  kubelet            Started container main-02


# confirm log
kubectl logs demo-container-colocated --all-containers
# Sun Jan  4 02:36:31 UTC 2026 main-01 start.
# Sun Jan  4 02:36:31 UTC 2026 main-01 running...
# Sun Jan  4 02:36:32 UTC 2026 main-01 running...
# Sun Jan  4 02:36:33 UTC 2026 main-01 running...
# Sun Jan  4 02:36:33 UTC 2026 main-02 start.
# Sun Jan  4 02:36:33 UTC 2026 main-02 running...
# Sun Jan  4 02:36:34 UTC 2026 main-02 running...
# Sun Jan  4 02:36:35 UTC 2026 main-02 running...
```

---
