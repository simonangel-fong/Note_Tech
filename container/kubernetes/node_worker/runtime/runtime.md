# Worker Node - Container Runtime

[Back](../../index.md)

---

## Lab: Disable Runtime

```sh
# worker node: disable container runtime
sudo systemctl stop containerd
sudo systemctl status containerd
# ○ containerd.service - containerd container runtime
#      Loaded: loaded (/usr/lib/systemd/system/containerd.service; enabled; preset: enabled)
#      Active: inactive (dead) since Fri 2026-06-05 15:49:29 EDT; 6s ago
#    Duration: 1h 12min 14.294s
#        Docs: https://containerd.io
#     Process: 36445 ExecStart=/usr/bin/containerd (code=exited, status=0/SUCCESS)
#    Main PID: 36445 (code=exited, status=0/SUCCESS)
#       Tasks: 196
#      Memory: 214.5M (peak: 505.2M)
#         CPU: 47.807s
#      CGroup: /system.slice/containerd.service


# create pod
kubectl run web --image=nginx
# pod/web created

kubectl get po
# NAME   READY   STATUS    RESTARTS   AGE
# web    0/1     Pending   0          13s

kubectl describe po web
# Events:
#   Type     Reason            Age   From               Message
#   ----     ------            ----  ----               -------
#   Warning  FailedScheduling  33s   default-scheduler  0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 1 node(s) had untolerated taint {node.kubernetes.io/not-ready: }, 1 node(s) had untolerated taint {node.kubernetes.io/unreachable: }. preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling.

# workder node: restore
sudo systemctl start containerd
sudo systemctl status containerd

# confirm
kubectl get po
# NAME   READY   STATUS    RESTARTS   AGE
# web    1/1     Running   0          66s

kubectl describe po web
# Events:
#   Type     Reason            Age   From               Message
#   ----     ------            ----  ----               -------
#   Warning  FailedScheduling  77s   default-scheduler  0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 1 node(s) had untolerated taint {node.kubernetes.io/not-ready: }, 1 node(s) had untolerated taint {node.kubernetes.io/unreachable: }. preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling.
#   Normal   Scheduled         55s   default-scheduler  Successfully assigned default/web to node01
#   Normal   Pulling           55s   kubelet            Pulling image "nginx"
#   Normal   Pulled            54s   kubelet            Successfully pulled image "nginx" in 475ms (475ms including waiting). Image size: 63120520 bytes.
#   Normal   Created           54s   kubelet            Created container: web
#   Normal   Started           54s   kubelet            Started container web
```
