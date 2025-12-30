# Kubernetes Service - LoadBalancer

[Back](../../index.md)

- [Kubernetes Service - LoadBalancer](#kubernetes-service---loadbalancer)
  - [LoadBalancer](#loadbalancer)
  - [Install MetalLB](#install-metallb)

---

## LoadBalancer

- `LoadBalancer`

  - a Kubernetes Service type that **exposes application** to the **outside** world using a **cloud provider’s** load balancer.
  - automatically provisions an **external** `load balancer` (e.g., AWS ELB, GCP LB, Azure LB) and links it to the Service.
    - External clients can reach the app using the LB’s `public IP` or `DNS name`.
  - Internally, it still uses `ClusterIP` + `NodePort` under the hood.

- How it works

- with AWS cloud

```yaml
# nginx-loadbalancer.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-loadbalancer
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80 # Service port (LB port)
      targetPort: 80 # Pod port
```

1. Service Creation
   - cmd: `kubectl apply -f nginx-loadbalancer.yaml`
   - `API server` store Service into `etcd`
   - `cloud-controller-manager` call AWS API to create AWS ELB with
     - public IP address
     - DNS name
   - automatically create a `NodePort` on each node
   - automatically create a `ClusterIP` for nginx

- 2. Client request
  - Client (Internet) → `AWS ELB` (3.120.45.67:80) → `NodeIP`:31234 → `ClusterIP` (10.96.0.20:80) → `Pod` IP (10.244.x.x:80)
  - kube-proxy Handles Pod Selection
    - Traffic hitting `NodePort` 31234 is **forwarded** to Service `ClusterIP` 10.96.0.20.
    - `ClusterIP` is mapped to the `Endpoints` list (your Nginx Pods).
    - `kube-proxy` load balances traffic across Pods (whether local or on other Nodes).

---

- `LoadBalancer` service type is an **extension** of the `NodePort` type,

  - `load balancer` **stands in front** of the `nodes` and handles the connections coming from the clients.
  - **routes each connection** to the `service` by **forwarding** it to the `node port` on one of the `nodes`.

- the client **never** attempts to connect to an `unavailable node` because the `load balancer` **forwards traffic** only to `healthy nodes`.

---

## Install MetalLB

- ref: https://metallb.io/


```sh
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.15.3/config/manifests/metallb-frr.yaml
```

