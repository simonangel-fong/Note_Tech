# Kubernetes Service - ClusterIP

[Back](../../index.md)

- [Kubernetes Service - ClusterIP](#kubernetes-service---clusterip)
  - [ClusterIP](#clusterip)
    - [How It Works](#how-it-works)
    - [Imperative Command](#imperative-command)
  - [Lab: Explore default ClusterIP](#lab-explore-default-clusterip)
  - [Lab: Create ClusterIP](#lab-create-clusterip)
  - [Lab: Create ClusterIP for nginx](#lab-create-clusterip-for-nginx)
    - [Use ClusterIP as Env var](#use-clusterip-as-env-var)
  - [Pod `dnsPolicy` Field](#pod-dnspolicy-field)
  - [Pod `enableServiceLinks` field](#pod-enableservicelinks-field)
    - [Service Discovery](#service-discovery)

---

## ClusterIP

- `ClusterIP`

  - the **default** service type
  - a Kubernetes Service type that **exposes** a group of `Pods` on an **internal**, **stable** IP address **inside** the `cluster`.
  - The IP is **virtual** (not bound to a specific Node interface).
  - provides a stable IP + DNS name inside the cluster.
  - only **reachable within** the cluster’s network (Pods, Nodes, other Services).
    - Not accessible directly from the outside world.

- Cannot access externally
  - `kubectl port-forward` does not work.

---

- Use ClusterIP in the pod
  - can create env var in the pod which refers to the service by ip/dns

```yaml
sep:
  env:
    - name: QUOTE_URL
      value: http://quote/quote
    - name: QUIZ_URL
      value: http://quiz
```

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
| `kubectl set selector service SERVICE KEY=VALUE`                                                   | Update service selector              |

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

---

## Lab: Create ClusterIP for nginx

- Create index and configmap

```sh
# create index.html
tee index.html<<EOF
<html>
<title>Home</title>

<body>
    <h1>Home</h1>
    <p>this is the home page</p>
</body>

</html>
EOF

# create cm with index.html
kubectl create configmap nginx-file --from-file=index.html -o yaml
# configmap/nginx-file created

# confirm
kubectl describe cm nginx-file
# Name:         nginx-file
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# index.html:
# ----
# <html>\r
# <title>Home</title>\r
# \r
# <body>\r
#     <h1>Home</h1>\r
#     <p>this is the home page</p>\r
# </body>\r
# \r
# </html>

```

- Create nginx pod

```sh
tee nginx-pod.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  volumes:
    - name: nginx-file
      configMap:
        name: nginx-file
        optional: true
  containers:
    - name: nginx
      image: nginx
      volumeMounts:
        - name: nginx-file
          mountPath: /usr/share/nginx/html
EOF

kubectl apply -f nginx-pod.yaml
# pod/nginx configured

kubectl get pod -o wide -L app
# NAME    READY   STATUS    RESTARTS   AGE   IP         NODE             NOMINATED NODE   READINESS GATES   APP
# nginx   1/1     Running   0          14m   10.1.3.1   docker-desktop   <none>           <none>            nginx

# confirm home page
kubectl port-forward nginx 8080:80
curl localhost:8080
# <html>
# <title>Home</title>

# <body>
#     <h1>Home</h1>
#     <p>this is the home page</p>
# </body>

# </html>
```

- Create service

```sh
tee nginx-svc.yaml<<EOF
apiVersion: v1
kind: Service
metadata:
  name: nginx-svc
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
  - name: http
    protocol: TCP
    port: 8080
    targetPort: 80
EOF

kubectl apply -f nginx-svc.yaml
# service/nginx-svc created

# confirm
kubectl get svc -o wide
# NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE     SELECTOR
# nginx-svc    ClusterIP   10.111.110.150   <none>        8080/TCP   9m11s   app=nginx

kubectl describe svc nginx-svc
# Name:                     nginx-svc
# Namespace:                default
# Labels:                   <none>
# Annotations:              <none>
# Selector:                 app=nginx
# Type:                     ClusterIP
# IP Family Policy:         SingleStack
# IP Families:              IPv4
# IP:                       10.111.110.150
# IPs:                      10.111.110.150
# Port:                     http  8080/TCP
# TargetPort:               80/TCP
# Endpoints:                10.1.3.1:80
# Session Affinity:         None
# Internal Traffic Policy:  Cluster
# Events:                   <none>

# update selector
kubectl set selector service nginx-svc app=nginx,backend=none
# service/nginx-svc selector updated

kubectl get svc -o wide
# NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE     SELECTOR
# kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP    6d17h   <none>
# nginx-svc    ClusterIP   10.111.110.150   <none>        8080/TCP   10m     app=nginx,backend=none

# update selector
kubectl set selector service nginx-svc app=nginx
# service/nginx-svc selector updated

kubectl get svc -o wide
# NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE     SELECTOR
# kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP    6d17h   <none>
# nginx-svc    ClusterIP   10.111.110.150   <none>        8080/TCP   11m     app=ngin
```

- confirm only within the cluster

```sh
# with ip
kubectl exec -it nginx -- curl 10.111.110.150:8080
# <html>
# <title>Home</title>

# <body>
#     <h1>Home</h1>
#     <p>this is the home page</p>
# </body>

# </html>

# with dns: all the same
kubectl exec -it nginx -- curl nginx-svc:8080
kubectl exec -it nginx -- curl nginx-svc.default:8080
kubectl exec -it nginx -- curl nginx-svc.default.svc:8080
kubectl exec -it nginx -- curl nginx-svc.default.svc.cluster.local:8080
# <html>
# <title>Home</title>

# <body>
#     <h1>Home</h1>
#     <p>this is the home page</p>
# </body>

# </html>
```

- Confirm DNS config in the pod

```sh
# dns resolve point to nameserver
kubectl exec -it nginx -- cat /etc/resolv.conf
# nameserver 10.96.0.10
# search default.svc.cluster.local svc.cluster.local cluster.local
# options ndots:5

# confirm: pod dns point to 10.96.0.10 which is kube-dns
kubectl get svc -A
# NAMESPACE              NAME                                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                  AGE
# default                kubernetes                             ClusterIP   10.96.0.1        <none>        443/TCP                  6d18h
# default                nginx-svc                              ClusterIP   10.111.110.150   <none>        8080/TCP                 43m
# kube-system            kube-dns                               ClusterIP   10.96.0.10       <none>        53/UDP,53/TCP,9153/TCP   52d
# kubernetes-dashboard   dashboard-metrics-scraper              ClusterIP   10.100.98.62     <none>        8000/TCP                 8d
# kubernetes-dashboard   kubernetes-dashboard                   ClusterIP   10.103.84.253    <none>        443/TCP                  8d
# kubernetes-dashboard   kubernetes-dashboard-api               ClusterIP   10.101.197.91    <none>        8000/TCP                 8d
# kubernetes-dashboard   kubernetes-dashboard-auth              ClusterIP   10.111.54.247    <none>        8000/TCP                 8d
# kubernetes-dashboard   kubernetes-dashboard-kong-proxy        ClusterIP   10.108.33.61     <none>        443/TCP                  8d
# kubernetes-dashboard   kubernetes-dashboard-metrics-scraper   ClusterIP   10.105.46.123    <none>        8000/TCP                 8d
# kubernetes-dashboard   kubernetes-dashboard-web               ClusterIP   10.107.83.59     <none>        8000/TCP                 8d
```

- Explore env var

```sh
kubectl exec -it nginx -- env | sort
# NGINX_SVC_PORT_8080_TCP_ADDR=10.111.110.150
# NGINX_SVC_PORT_8080_TCP_PORT=8080
# NGINX_SVC_PORT_8080_TCP_PROTO=tcp
# NGINX_SVC_PORT_8080_TCP=tcp://10.111.110.150:8080
# NGINX_SVC_PORT=tcp://10.111.110.150:8080
# NGINX_SVC_SERVICE_HOST=10.111.110.150
# NGINX_SVC_SERVICE_PORT_HTTP=8080
# NGINX_SVC_SERVICE_PORT=8080
```

---

### Use ClusterIP as Env var

```sh
tee ping-pod.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  name: ping-pod
spec:
  env:
    - name: NGINX_SVC_URL
      value: http://nginx-svc:8080
  containers:
    - name: busybox
      image: busybox
      command:
        - "sh"
      args:
        - "-c"
        - |
         echo "ping-pod"
         wget $NGINX_SVC_URL

         sleep 500
EOF

kubectl apply -f ping-pod.yaml
# pod/ping-pod created

# confirm log
kubectl logs pod/ping-pod
# ping-pod
# Connecting to nginx-svc:8080 (10.111.110.150:8080)
# writing to stdout
# -                    100% |********************************|   110  0:00:00 ETA
# written to stdout
# <html>
# <title>Home</title>

# <body>
#     <h1>Home</h1>
#     <p>this is the home page</p>
# </body>
```


---

## Pod `dnsPolicy` Field

- `spec.dnsPolicy` field
  - update the `resolv.conf` file within the pod, affect pod's DNS behavior
  - `ClusterFirst`:
    - default
    - uses the `internal DNS` `first` and then the `DNS configured` for the cluster node.
  - `Default`:
    - uses the DNS configured for the node
  - `None`:
    - no DNS configuration is provided by Kubernetes
    - use configuration in the using the `dnsConfig` field
  - `ClusterFirstWithHostNet`:
    - special pods that use the host’s network instead of their own

---

## Pod `enableServiceLinks` field

- Whether enable the injection of service information into the environment
- `false`: **disable** the injection of service information

---

### Service Discovery

- `service discovery`

  - use `Services` and an `internal DNS system` (typically CoreDNS).
  - allows applications (pods) to **find and communicate with each other** using **stable names** rather than dynamic, ephemeral IP addresses.

- Legacy: use Env var used to identify service

```sh
# service ip: 10.111.110.150
kubectl get svc -A
# NAMESPACE              NAME                                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                  AGE
# default                nginx-svc                              ClusterIP   10.111.110.150   <none>        8080/TCP                 43m

# env var: set the service ip
kubectl exec -it nginx -- env | sort
# NGINX_SVC_PORT_8080_TCP_ADDR=10.111.110.150
# NGINX_SVC_PORT_8080_TCP_PORT=8080
# NGINX_SVC_PORT_8080_TCP_PROTO=tcp
# NGINX_SVC_PORT_8080_TCP=tcp://10.111.110.150:8080
# NGINX_SVC_PORT=tcp://10.111.110.150:8080
# NGINX_SVC_SERVICE_HOST=10.111.110.150
# NGINX_SVC_SERVICE_PORT_HTTP=8080
# NGINX_SVC_SERVICE_PORT=8080
```

- specify `nameserver` in `resolve.conf` in pod for dns
  - container in `pod` use dns to discover the `service`

```sh
# kube-dns ip: 10.96.0.10
kubectl get svc -A
# NAMESPACE              NAME                                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                  AGE
# kube-system            kube-dns                               ClusterIP   10.96.0.10       <none>        53/UDP,53/TCP,9153/TCP   52d

# resolve sets nameserver==dns
kubectl exec -it nginx -- cat /etc/resolv.conf
# nameserver 10.96.0.10
# search default.svc.cluster.local svc.cluster.local cluster.local
# options ndots:5
```
