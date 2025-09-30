# Kubernetes Service - ClusterIP

[Back](../../index.md)

- [Kubernetes Service - ClusterIP](#kubernetes-service---clusterip)
  - [ClusterIP](#clusterip)
    - [How It Works](#how-it-works)
    - [Imperative Command](#imperative-command)
  - [Lab: Explore default ClusterIP](#lab-explore-default-clusterip)
  - [Lab: Create ClusterIP](#lab-create-clusterip)

---

## ClusterIP

- `ClusterIP`
  - the **default** service type
  - a Kubernetes Service type that **exposes** a group of `Pods` on an **internal**, **stable** IP address **inside** the `cluster`.
  - The IP is **virtual** (not bound to a specific Node interface).
  - provides a stable IP + DNS name inside the cluster.
  - only **reachable within** the cluster’s network (Pods, Nodes, other Services).
    - Not accessible directly from the outside world.

---

### How It Works

- Example

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-clusterip
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80 # Service port (ClusterIP virtual port)
      targetPort: 80 # Pod’s container port
  type: ClusterIP # Default service type
```

1. Service Creation
   - cmd: `kubectl apply -f nginx-clusterip.yaml`
   - The `API Server`
     - assigns a virtual IP (ClusterIP) to each `pod`
     - **stores** the Service in `etcd`, including the `ClusterIP`, a
     - push update to `kube-proxy` on each node
   - `kube-proxy` Configures Rules
     - installs iptables/IPVS rules
2. Service Discovery
   - CoreDNS registers the Service with a DNS name
     - `nginx-clusterip.default.svc.cluster.local`
3. Client request Inside the cluster
   - cmd: `curl http://nginx-clusterip:80`

- `ClusterIP`: a virtual IP used to represent a collection of pods
- `Endpoints object`: the ip+port for each pod

---

- DNS Resolution: `curl http://nginx-clusterip:80`
  - a pod within the cluster sends a DNS query `nginx-clusterip`
  - `CoreDNS`, the DNS server within the cluster, looks up Services in the API Server and finds:
    - `Service`: nginx-clusterip
    - `ClusterIP`: 10.96.0.15
  - `CoreDNS` sends back the `ClusterIP` 10.96.0.15:80
  - `kube-proxy` looks up the Service rule and randomly/round-robin forward traffic to the `Endpoints object`, a specific pod

---

### Imperative Command

| Command                                                                                            | DESC                                 |
| -------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `kubectl create svc clusterip svc_name --tcp=port`                                                 | Create a ClusterIP service           |
| `kubectl expose deploy deploy_name --name=svc_name --type=ClusterIP --port=80 --target-port=8080 ` | Expose a deploy                      |
| `kubectl expose pod pod_name --name=svc_name --type=ClusterIP --port=80 --target-port=8080 `       | Expose a pod                         |
| `kubectl run nginx --image=nginx --port=80 --expose=true`                                          | Create a pod and a ClusterIP service |

---

## Lab: Explore default ClusterIP

```sh
kubectl get svc
# NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   18h

kubectl describe svc kubernetes
# Name:                     kubernetes
# Namespace:                default
# Labels:                   component=apiserver
#                           provider=kubernetes
# Annotations:              <none>
# Selector:                 <none>
# Type:                     ClusterIP
# IP Family Policy:         SingleStack
# IP Families:              IPv4
# IP:                       10.96.0.1
# IPs:                      10.96.0.1
# Port:                     https  443/TCP
# TargetPort:               6443/TCP
# Endpoints:                192.168.65.3:6443
# Session Affinity:         None
# Internal Traffic Policy:  Cluster
# Events:                   <none>
```

---

## Lab: Create ClusterIP

- `deploy-nginx.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy-nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      name: nginx-pod
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx-con
          image: nginx
```

- `service-clusterip.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: service-clusterip
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
```

```sh
# create
kubectl create -f .
# deployment.apps/deploy-nginx created
# service/service-clusterip created

# confirm
kubectl get all
# NAME                                READY   STATUS    RESTARTS   AGE
# pod/deploy-nginx-5f9767d954-jjm9q   1/1     Running   0          2m21s
# pod/deploy-nginx-5f9767d954-wbrfr   1/1     Running   0          2m21s
# pod/deploy-nginx-5f9767d954-xbtn8   1/1     Running   0          2m21s

# NAME                        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
# service/kubernetes          ClusterIP   10.96.0.1        <none>        443/TCP   18h
# service/service-clusterip   ClusterIP   10.106.146.103   <none>        80/TCP    2m21s

# NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/deploy-nginx   3/3     3            3           2m21s

# NAME                                      DESIRED   CURRENT   READY   AGE
# replicaset.apps/deploy-nginx-5f9767d954   3         3         3       2m21s

# get info
kubectl describe svc service-clusterip
# Name:                     service-clusterip
# Namespace:                default
# Labels:                   <none>
# Annotations:              <none>
# Selector:                 app=nginx
# Type:                     ClusterIP
# IP Family Policy:         SingleStack
# IP Families:              IPv4
# IP:                       10.106.146.103
# IPs:                      10.106.146.103
# Port:                     <unset>  80/TCP
# TargetPort:               80/TCP
# Endpoints:                10.1.2.158:80,10.1.2.159:80,10.1.2.160:80
# Session Affinity:         None
# Internal Traffic Policy:  Cluster
# Events:                   <none>

# create a pod to test clusterIP
kubectl run curlpod --rm -it --image=busybox:1.36 --restart=Never -- sh
# test dns name
wget -qO- http://service-clusterip:80
# test clusterIP/virtual IP
wget -qO- http://10.106.146.103:80
exit

# remove
kubectl delete -f .
# deployment.apps "deploy-nginx" deleted
# service "service-clusterip" deleted
```
