# Kubernetes - kube-proxy

[Back](../../index.md)

- [Kubernetes - kube-proxy](#kubernetes---kube-proxy)
  - [kube-proxy](#kube-proxy)
  - [Lab: Disable kube-proxy](#lab-disable-kube-proxy)

---

## kube-proxy

- `kube-proxy`
  - a **networking component** that runs **on every node** in a Kubernetes cluster.
  - used to **maintain the network rules** that allow communication to `Services` and the `Pods` behind them.

- Primary Roles
  - **Service Implementation**
    - Watches the `API Server` for `Service` and `Endpoint` objects.
    - Ensures that **traffic** sent to a `Service` (ClusterIP, NodePort, LoadBalancer) is routed to one of its `backend Pods`.
  - **Load Balancing**
    - **Distributes requests** across all healthy Pods behind a Service.
    - Uses round-robin or other mechanisms depending on the backend mode (iptables, IPVS).
  - **Programming Network Rules**
    - Manages `iptables` or `IPVS` rules on the node.
    - Ensures packets destined for a Service are redirected to the correct Pod IPs.

- In kubeadm, `kube-proxy` usually runs as a `DaemonSet`.

---

- Without `kube-proxy`, Pods can still be created, but `Service` networking may fail.
  - Scheduling: Not affected
  - API server static Pods: Not affected
  - impact:
    - `ClusterIP Service`: May not route correctly
    - `NodePort Service`: May not work
    - `Service load balancing`: May fail
    - DNS access to Services: DNS name may resolve, but traffic may not connect
    - Pod-to-Pod networking: May still work, depending on CNI

```sh
kubectl get pods -n kube-system
# kube-proxy-xbtjz                         1/1     Running   122 (4h29m ago)   148d

kubectl get daemonset -n kube-system
# NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
# kube-proxy   1         1         1       1            1           kubernetes.io/os=linux   148d
```

---

## Lab: Disable kube-proxy

```sh
# backup manifest
kubectl -n kube-system get ds kube-proxy -o yaml > kube-proxy-backup.yaml

# disable
kubectl -n kube-system patch daemonset kube-proxy \
  -p '{"spec":{"template":{"spec":{"nodeSelector":{"kube-proxy-disabled":"true"}}}}}'

kubectl get ds -n kube-system kube-proxy
# NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR                                     AGE
# kube-proxy   0         0         0       0            0           kube-proxy-disabled=true,kubernetes.io/os=linux   139d

# create pod and svc
kubectl run web --image=nginx
# pod/web created
kubectl expose pod web --port=80 --name=web-svc
# service/web-svc exposed

kubectl get svc web-svc
# web-svc      ClusterIP   10.111.170.97   <none>        80/TCP    14s

kubectl run test --image=busybox -- sleep 600
# pod/test created

kubectl get po
# NAME   READY   STATUS    RESTARTS   AGE
# test   1/1     Running   0          12s
# web    1/1     Running   0          86s

# test
kubectl exec test -- wget web-svc
# Connecting to web-svc (10.111.170.97:80)
# wget: can't connect to remote host (10.111.170.97): Connection refused
# command terminated with exit code 1
```

- restore proxy

```sh
kubectl replace --force -f kube-proxy-backup.yaml
# daemonset.apps "kube-proxy" deleted
# daemonset.apps/kube-proxy replaced

kubectl get ds -n kube-system kube-proxy
# NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
# kube-proxy   3         3         3       3            3           kubernetes.io/os=linux   2m45s

kubectl exec test -- wget web-svc
# Connecting to web-svc (10.111.170.97:80)
# saving to 'index.html'
# index.html           100% |********************************|   896  0:00:00 ETA
# 'index.html' saved
```
