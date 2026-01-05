# Kubernetes - Services

[Back](../../index.md)

- [Kubernetes - Services](#kubernetes---services)
  - [Pod Communication](#pod-communication)
  - [Service](#service)
    - [Types of Services](#types-of-services)
    - [Imperative Commands](#imperative-commands)
    - [Declarative Manifest](#declarative-manifest)
  - [ClusterIP](#clusterip)
  - [Load Balancer](#load-balancer)
  - [Common Commands](#common-commands)
  - [Service Networking](#service-networking)
  - [Lab: Get network info](#lab-get-network-info)

---

## Pod Communication

- `Pods` are linked via **a flat network** that requires **no** `NAT`

  - packets exchange between `Pods` only needs the **source** `IP` and `port`, and the **destination** `IP` and `port`,

- constraint
  - `Pods` are **ephemeral**.
  - A `pod` gets its **IP address** only when it’s **assigned** to a node.
  - A simgle IP / DNS to is required; but Each of replicas `Pod` has its own IP address.

---

## Service

- `Service`

  - an object to **provide a single, stable access point** to **a set of pods** that provide the same service.
    - Each `service` has a **stable IP address** that **doesn’t change** for as long as the `service` **exists**.
    - A `service` acts as a `load balancer` in front of those `pods`.
  - `Services` use **labels** and **selectors** to find the right `Pods`.

---

### Types of Services

- `ClusterIP`
  - **default**
  - Exposes Pods on a `virtual internal IP`.
  - Accessible **only within** the `cluster`.
    - e.g. backend services for microservices.
- `NodePort`
  - **Exposes the Service** on a **static port** (30000–32767) on **each** `Node`’s IP.
  - Accessible from **outside** the `cluster` using `NodeIP:NodePort`.
  - Good for **testing**, not ideal for production.
- `LoadBalancer`
  - **Integrates** with cloud provider `load balancers` (`AWS ELB`, `GCP LB`, `Azure LB`).
  - **Exposes** the Service to the `internet`.
  - `Cloud provider` assigns a `public IP`.
- `ExternalName`

  - **Maps** the `Service` to an **external** `DNS` name (like api.example.com).
  - No selector, just returns a `CNAME`.

- `Service Discovery`

  - **Inside** the `cluster`, `Services` are **automatically registered** with `DNS`.
  - e.g., `nginx-service.default.svc.cluster.local`
  - Other Pods can talk to it **using this name** instead of IP.

- **Cannot** `ping` a serivce:
  - because svc is virtual.

---

### Imperative Commands

| Command                                             | Description                                         |
| --------------------------------------------------- | --------------------------------------------------- |
| `kubectl get svc`                                   | List all Services in the current namespace.         |
| `kubectl describe svc service_name`                 | Show detailed information about a specific Service. |
| `kubectl create svc clusterip svc_name --tcp=80`    | Create a ClusterIP service                          |
| `kubectl create svc nodeport svc_name --tcp=80`     | Create a NodePort service                           |
| `kubectl create svc loadbalancer svc_name --tcp=80` | Create a LoadBalancer service                       |
| `kubectl delete svc svc_name`                       | Delete a Service by name.                           |

### Declarative Manifest

- basic fields

| Field       | Description                                                                                                         |
| ----------- | ------------------------------------------------------------------------------------------------------------------- |
| `clusterIP` | The internal IP address within the cluster. blank:k8s assign; `None`:headless service.                              |
| `type`      | the type of Service object: `ClusterIP`(default), `NodePort`, `LoadBalancer`, and `ExternalName`.                   |
| `selector`  | the label keys and values                                                                                           |
| `ports`     | List of ports exposed by this service. can specify the name, protocol, appProtocol, port, nodePort, and targetPort. |

- `spec.sessionAffinity` field
  - whether it should forward all connections from the **same client** to the **same pod**.
  - `None`:
    - default
    - no guarantee to which pod each connection will be forwarded
  - `ClientIP`:
    - all connections **originating from the same IP** will be forwarded to the **same pod**.
- `spec.sessionAffinityConfig.clientIP.timeoutSeconds` field:

  - specify how long the session will persist.
  - default: 3 hours

- `service` **doesn’t** provide **cookie-based session affinity**

---

## ClusterIP

- `ClusterIP`

  - default type of service
  - exposes the `service` within the defined Kubernetes `cluster`.
  - enable communication between `services`
  - a type of Service that provides an **internal, cluster-wide IP address** to enable **communication** between different **components** (typically Pods) within the **same** Kubernetes `cluster`.
  - forward the requests to one of the pods under the service **randomly**

- The service canbe aacessed by other pods using the cluster IP/service name

---

- Definition

```yaml
apiVersion: v1
kind: Service
metadata:
  name: back-end
spec:
  type: ClusterIP
  ports:
    - targetPort: 80 # the port exposed on backend
      port: 80 # the port exposed on service
  selector: # link the service to the pods
    app: myapp
    type: back-end
```

- Create

```sh
kubectl create -f service-cip-def.yaml

kubectl get svc
```

---

## Load Balancer

- `LoadBalancer`
  - a type of Service that provides **external access** to applications running in a Kubernetes cluster.
  - Only works with supported cloud platforms.

---

- Definition

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myservice
spec:
  type: LoadBalancer
  ports:
    - targetPort: 80
      port: 80
      nodePort: 30008
```

---

## Common Commands

- how many services exist on system
  - `kubectl get svc`
- the type of default `kubernetes` service
  - ClusterIP
- what targetPort the default `kubernetes` is configured
  - `kubectl describe svc kubernetes`
  - 6443/TCP
- how many labels are configured on the default `kubernetes` service
  - `kubectl describe svc kubernetes`, labels
- how many endpoint are attached on the default `kubernetes` service
  - `kubectl describe svc kubernetes`, Endpoints

---

## Service Networking

- `kubelet`, the agent on each node, monitor the change on API Server for pod
  - create pod
  - invoke CNI plugin to configure networking for the pod
- `kube proxy`, the agent on each node, monitor the change on API server for services.
  - get the predeined IP address for updated service object
    - `kubectl-api-server --service-cluster-ip-range ipNet`
  - manage forwarding rules to the predefined IP address on each node
    - once the rule created, the request for the service get forwarded to the predefined IP address and port.
    - 3 method to manage the routing rules:
      - userspace
      - iptables
      - ipvs
      - can modify by `kube-proxy --proxy-mode userspace|iptables|ipvs`

---

## Lab: Get network info

- ge the primary network range

```sh
# get master node ip
kubectl get node -o wide
# NAME           STATUS   ROLES           AGE   VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION    CONTAINER-RUNTIME
# controlplane   Ready    control-plane   39m   v1.34.0   192.168.81.31    <none>        Ubuntu 22.04.5 LTS   5.15.0-1083-gcp   containerd://1.6.26

# get master node ip range
ip a
# 4: eth0@if22929: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1410 qdisc noqueue state UP group default
#     link/ether 22:8d:d9:de:30:0b brd ff:ff:ff:ff:ff:ff link-netnsid 0
#     inet 192.168.81.31/32 scope global eth0
#        valid_lft forever preferred_lft forever
#     inet6 fe80::208d:d9ff:fede:300b/64 scope link
#        valid_lft forever preferred_lft forever
```

- get ip range for pods

```sh
# get the cidr from controller manager conf
cat /etc/kubernetes/manifests/kube-controller-manager.yaml | grep cluster-cidr
# - --cluster-cidr=172.17.0.0/16
```

- Get the ip range for services

```sh
# get the service config from the aip server
cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep service-cluster-ip-range
# - --service-cluster-ip-range=172.20.0.0/16
```

- Get the proxy on the node

```sh
kubectl get pod -A | grep proxy
# kube-system   kube-proxy-6c4gt                           1/1     Running   0          59m
# kube-system   kube-proxy-sjt5p                           1/1     Running   0          59m

# get the type of proxy
k logs kube-proxy-sjt5p    -n kube-system
# I1203 18:43:42.896019       1 server_linux.go:132] "Using iptables Proxier"

# get how the proxy is deployed
kubectl get all -A | grep kube-proxy  # use daemonset
# kube-system   pod/kube-proxy-6c4gt                           1/1     Running   0          66m
# kube-system   pod/kube-proxy-sjt5p                           1/1     Running   0          65m
# kube-system   daemonset.apps/kube-proxy   2         2         2       2            2           kubernetes.io/os=linux   66m
```

---
