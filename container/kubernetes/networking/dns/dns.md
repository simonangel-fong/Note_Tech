# Kubernetes - Cluster DNS

[Back](../../index.md)

- [Kubernetes - Cluster DNS](#kubernetes---cluster-dns)
  - [DNS Solution within the Cluster](#dns-solution-within-the-cluster)
  - [CoreDNS](#coredns)
  - [Lab: CoreDNS](#lab-coredns)
  - [Lab: Explore DNS](#lab-explore-dns)
  - [headless service](#headless-service)
  - [Lab: Creating a headless service](#lab-creating-a-headless-service)
    - [Headless services with no label selector](#headless-services-with-no-label-selector)
  - [Lab: Creating a CNAME alias for an existing service](#lab-creating-a-cname-alias-for-an-existing-service)
  - [Configuring services to route traffic to nearby endpoints](#configuring-services-to-route-traffic-to-nearby-endpoints)
  - [Topology-Aware Routing (TAR)](#topology-aware-routing-tar)
  - [readiness probes](#readiness-probes)
    - [readiness probe types](#readiness-probe-types)
  - [Lab: Readiness Probe - httpGet](#lab-readiness-probe---httpget)

---

## DNS Solution within the Cluster

- Help resolve the DNS for the pod
- By default:
  - K8s deploys built-in DNS
- Whenever a service is created, k8s creates a records in cluster DNS, mapping DNS name to IP

  - any pod within the cluster can access the service using service name

- Services & Namespace:

  - same ns:
    - `svc_name`
    - e.g., `curl http://web-service`
  - different ns:
    - `svc_name.ns_name`: service name act as subdomain, the namespace is the domain
    - e.g., `curl http://web-service.apps`

- All services are grouped by a domain `svc`
  - `svc_name.ns_name.svc`
  - e.g., `web-service.apps.svc` is a service named web-service in the apps namespace
- All resources are grouped in the root domain for the cluster `cluster.local`

- Example of an `Fully Qaullify Domain Name` in a cluster

| Service/pod | Hostname    | namespace | Type | Root          | IP            |
| ----------- | ----------- | --------- | ---- | ------------- | ------------- |
| Service     | web-service | apps      | svc  | cluster.local | 10.107.37.188 |
| pod         | 10-244-2-5  | default   | pod  | cluster.local | 10.244.2.5    |

- `curl http://web-service.apps.svc.cluster.local`

---

- A `CNAME record` is a DNS record that **maps** an `alias` to an **existing DNS name** instead of an IP address.
  - Can create an alias in k8s DNS

---

## CoreDNS

- After 1.12, DNS server implemented by CoreDNS
- Deployed using `deployment` in the `kube-system` namespace

- Conf file
  - `/etc/coredns/Corefile`
- service `kube-dns`
  - a service created for pods to access.
- `kubelet` updates the pod dns server
  - the ip addres of the `kube-dns` service is automatically writen in `/etc/resolv.conf` in each pod.
  ```conf
  # /etc/resolve.conf
  nameserver    ip_dns_svc
  search        default.svc.cluster.local svc.cluster.local cluster.local # search the FQDN for service, cannot for a pod
  ```

---

## Lab: CoreDNS

- Get the DNS pods

```sh
kubectl get pod -A | grep dns
# kube-system    coredns-6678bcd974-9s6xl               1/1     Running   0          11m
# kube-system    coredns-6678bcd974-gvh6c               1/1     Running   0          11m
```

- Get the dns service

```sh
kubectl get svc -A | grep dns
# kube-system   kube-dns       ClusterIP   172.20.0.10      <none>        53/UDP,53/TCP,9153/TCP   13m
```

- Get the conf file on each node for the coredns

```sh
# get the conf file from the detail of the dns pod
kubectl get pod -A | grep dns
# kube-system    coredns-6678bcd974-9s6xl               1/1     Running   0          11m
# kube-system    coredns-6678bcd974-gvh6c               1/1     Running   0          11m

# mount using ConfigMap
kubectl describe pod coredns-6678bcd974-9s6xl -n kube-system
    # Args:
    #   -conf
    #   /etc/coredns/Corefile
    # Mounts:
      # /etc/coredns from config-volume (ro)
# Volumes:
  # config-volume:
    # Type:      ConfigMap (a volume populated by a ConfigMap)
    # Name:      coredns
    # Optional:  false

# get detail in the configMap
kubectl get configmap coredns -n kube-system
# NAME      DATA   AGE
# coredns   1      23m

# configmap shows coredns config file entries, the root: cluster.local
kubectl describe configmap coredns -n kube-system
# Name:         coredns
# Namespace:    kube-system
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# Corefile:
# ----
# .:53 {
#     errors
#     health {
#        lameduck 5s
#     }
#     ready
#     kubernetes cluster.local in-addr.arpa ip6.arpa {
#        pods insecure
#        fallthrough in-addr.arpa ip6.arpa
#        ttl 30
#     }
#     prometheus :9153
#     forward . /etc/resolv.conf {
#        max_concurrent 1000
#     }
#     cache 30
#     loop
#     reload
#     loadbalance
# }



# BinaryData
# ====

# Events:  <none>
```

---

## Lab: Explore DNS

- Lookup a service's A record

```sh
# existing svc
kubectl get svc
# NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
# demo-nodeport-svc   NodePort    10.102.182.197   <none>        8080:30977/TCP   6h23m
# kubernetes          ClusterIP   10.96.0.1        <none>        443/TCP          7d3h

# run dns test tool
kubectl run -it --rm dns-test --image=giantswarm/tiny-tools
# lookup a svc
nslookup demo-nodeport-svc
# Server:         10.96.0.10
# Address:        10.96.0.10#53

# Name:   demo-nodeport-svc.default.svc.cluster.local
# Address: 10.102.182.197

dig +search demo-nodeport-svc
# ; <<>> DiG 9.16.6 <<>> +search demo-nodeport-svc
# ;; global options: +cmd
# ;; Got answer:
# ;; WARNING: .local is reserved for Multicast DNS
# ;; You are currently testing what happens when an mDNS query is leaked to DNS
# ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 2173
# ;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
# ;; WARNING: recursion requested but not available

# ;; OPT PSEUDOSECTION:
# ; EDNS: version: 0, flags:; udp: 4096
# ; COOKIE: 778248174117785a (echoed)
# ;; QUESTION SECTION:
# ;demo-nodeport-svc.default.svc.cluster.local. IN        A

# ;; ANSWER SECTION:
# demo-nodeport-svc.default.svc.cluster.local. 30 IN A 10.102.182.197

# ;; Query time: 0 msec
# ;; SERVER: 10.96.0.10#53(10.96.0.10)
# ;; WHEN: Mon Dec 29 03:10:27 UTC 2025
# ;; MSG SIZE  rcvd: 143

dig demo-nodeport-svc.default.svc.cluster.local
# ; <<>> DiG 9.16.6 <<>> demo-nodeport-svc.default.svc.cluster.local
# ;; global options: +cmd
# ;; Got answer:
# ;; WARNING: .local is reserved for Multicast DNS
# ;; You are currently testing what happens when an mDNS query is leaked to DNS
# ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 35983
# ;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
# ;; WARNING: recursion requested but not available

# ;; OPT PSEUDOSECTION:
# ; EDNS: version: 0, flags:; udp: 4096
# ; COOKIE: 3bd363ee51cd0faa (echoed)
# ;; QUESTION SECTION:
# ;demo-nodeport-svc.default.svc.cluster.local. IN        A

# ;; ANSWER SECTION:
# demo-nodeport-svc.default.svc.cluster.local. 30 IN A 10.102.182.197

# ;; Query time: 0 msec
# ;; SERVER: 10.96.0.10#53(10.96.0.10)
# ;; WHEN: Mon Dec 29 03:11:18 UTC 2025
# ;; MSG SIZE  rcvd: 143

```

- Lookup a service's SRV record

```sh
nslookup -query=SRV demo-nodeport-svc
# Server:         10.96.0.10
# Address:        10.96.0.10#53

# demo-nodeport-svc.default.svc.cluster.local     service = 0 100 8080 demo-nodeport-svc.default.svc.cluster.local.

# get the SRV record for the http port
nslookup -query=SRV _http._tcp.demo-nodeport-svc
# Server:         10.96.0.10
# Address:        10.96.0.10#53

# _http._tcp.demo-nodeport-svc.default.svc.cluster.local  service = 0 100 8080 demo-nodeport-svc.default.svc.cluster.local.

# list all services and the ports
nslookup -query=SRV any.demo-nodeport-svc.default.svc.cluster.local

nslookup -query=SRV _http._tcp.demo-nodeport-svc

nslookup -query=SR any.any.svc.cluster.local
```

---

## headless service

- `headless service`
  - a type of **Service** to return the **individual IP addresses** of all the `pods` that match its selector, allowing clients to **connect** to the `pods` **directly**.
  - the `cluster DNS` **returns**
    - a `single A record` pointing to the `service’s cluster IP`
    - **multiple** `A records`
      - one for each `pod` that’s part of the service.
  - **Clients** can therefore **query the DNS** to get the IPs of all the pods in the service.
    - With this information, the client can then **connect directly** to the `pods`.

![pic](./pic/headless_service.png)

- Vs regular service
  - `headless service`: connect directly to the pod IP
  - The difference is that with a headless service you connect directly to
    the pod IP, while with regular services you connect to the cluster IP of the
    service, and your connection is forwarded to one of the pods.

---

## Lab: Creating a headless service

```yaml
# demo-headless-svc.yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-headless-svc
spec:
  clusterIP: None # headless
  selector:
    app: nginx
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 80
```

```sh
kubectl apply -f demo-headless-svc.yaml
# service/demo-headless-svc created

kubectl get svc -o wide
# NAME                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE     SELECTOR
# demo-headless-svc   ClusterIP   None           <none>        8080/TCP         45s     app=nginx
# demo-nodeport-svc   NodePort    10.106.98.10   <none>        8080:30506/TCP   7h55m   app=nginx

kubectl describe svc demo-headless-svc
# Name:                     demo-headless-svc
# Namespace:                default
# Labels:                   <none>
# Annotations:              <none>
# Selector:                 app=nginx
# Type:                     ClusterIP
# IP Family Policy:         SingleStack
# IP Families:              IPv4
# IP:                       None
# IPs:                      None
# Port:                     http  8080/TCP
# TargetPort:               80/TCP
# Endpoints:                10.244.2.18:80,10.244.1.13:80
# Session Affinity:         None
# Internal Traffic Policy:  Cluster
# Events:                   <none>
```

- Confirm headless service return a list IP address of pods

```sh
# list ip of pod
kubectl get pod -o wide
# NAME                     READY   STATUS    RESTARTS      AGE     IP            NODE     NOMINATED NODE   READINESS GATES
# nginx-546c7dd8cf-rts7p   2/2     Running   0             7h59m   10.244.2.18   node02   <none>           <none>
# nginx-546c7dd8cf-t5kws   2/2     Running   2 (45m ago)   7h59m   10.244.1.13   node01   <none>           <none>

# run dns test tool
kubectl run -it --rm dns-test --image=giantswarm/tiny-tools

# lookup service
nslookup demo-headless-svc
# Server:         10.96.0.10
# Address:        10.96.0.10#53

# Name:   demo-headless-svc.default.svc.cluster.local
# Address: 10.244.2.18
# Name:   demo-headless-svc.default.svc.cluster.local
# Address: 10.244.1.13

# confirm: service returns content in pod
curl http://demo-headless-svc
# <h1>node01:nginx-546c7dd8cf-t5kws - Mon Dec 29 04:47:53 UTC 2025</h1>

# #######################
# vs regular svc
# #######################
# headless: connect directly to the pod IP
curl --verbose http://demo-headless-svc
# *   Trying 10.244.2.18:80...)
# * Connected to demo-headless-svc (10.244.2.18) port 80 (#0
# > GET / HTTP/1.1
# > Host: demo-headless-svc
# > User-Agent: curl/7.69.1
# > Accept: */*
# >
# * Mark bundle as not supporting multiuse
# < HTTP/1.1 200 OK
# < Server: nginx/1.29.4
# < Date: Mon, 29 Dec 2025 04:48:09 GMT
# < Content-Type: text/html
# < Content-Length: 70
# < Last-Modified: Mon, 29 Dec 2025 04:48:08 GMT
# < Connection: keep-alive
# < ETag: "69520808-46"
# < Accept-Ranges: bytes
# <
# <h1>node02:nginx-546c7dd8cf-rts7p - Mon Dec 29 04:48:08 UTC 2025</h1>
# * Connection #0 to host demo-headless-svc left intact

# nodeport: connect to nodeport(demo-nodeport-svc (10.106.98.10))
curl --verbose http://demo-nodeport-svc:8080
# *   Trying 10.106.98.10:8080...
# * Connected to demo-nodeport-svc (10.106.98.10) port 8080 (#0)
# > GET / HTTP/1.1
# > Host: demo-nodeport-svc:8080
# > User-Agent: curl/7.69.1
# > Accept: */*
# >
# * Mark bundle as not supporting multiuse
# < HTTP/1.1 200 OK
# < Server: nginx/1.29.4
# < Date: Mon, 29 Dec 2025 04:49:59 GMT
# < Content-Type: text/html
# < Content-Length: 70
# < Last-Modified: Mon, 29 Dec 2025 04:49:59 GMT
# < Connection: keep-alive
# < ETag: "69520877-46"
# < Accept-Ranges: bytes
# <
# <h1>node02:nginx-546c7dd8cf-rts7p - Mon Dec 29 04:49:59 UTC 2025</h1>
# * Connection #0 to host demo-nodeport-svc left intact
```

---

### Headless services with no label selector

- When omitting the `label selector` and set the `clusterIP` to `None`,
  - DNS will return an `A/AAAA record` **for each endpoint**,

---

## Lab: Creating a CNAME alias for an existing service

- Creating an ExternalName service

```yaml
# demo-dns-cname-extralname.yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-dns-cname-extralname
spec:
  type: ExternalName
  externalName: worldtimeapi.org
```

- Connecting to an ExternalName service from a pod

```sh
kubectl apply -f demo-dns-cname-extralname.yaml
# service/demo-dns-cname-extralname created

kubectl get svc
# NAME                        TYPE           CLUSTER-IP       EXTERNAL-IP        PORT(S)          AGE
# demo-dns-cname-extralname   ExternalName   <none>           worldtimeapi.org   <none>           70s

# test connection within cluster
kubectl run -it --rm dns-teset --image=giantswarm/tiny-tools

curl http://demo-dns-cname-extralname/api/timezone/America/Toronto
# {"utc_offset":"-05:00","timezone":"America/Toronto","day_of_week":1,"day_of_year":363,"datetime":"2025-12-29T14:41:25.859594-05:00","utc_datetime":"2025-12-29T19:41:25.859594+00:00","unixtime":1767037285,"raw_offset":-18000,"week_number":1,"dst":false,"abbreviation":"EST","dst_offset":0,"dst_from":null,"dst_until":null,"client_ip":"99.243.74.50"}

# the service points to worldtimeapi.org.
nslookup demo-dns-cname-extralname
# Server:         10.96.0.10
# Address:        10.96.0.10#53

# demo-dns-cname-extralname.default.svc.cluster.local     canonical name = worldtimeapi.org.
# Name:   worldtimeapi.org
# Address: 213.188.196.246
# Name:   worldtimeapi.org
# Address: 2a09:8280:1::3:e

```

---

## Configuring services to route traffic to nearby endpoints

- When you deploy `pods`, they are **distributed across** the `nodes` in the cluster.

  - If cluster `nodes` **span different** `availability zones` or `regions` and the `pods` deployed on those nodes exchange traffic with each other, **network performance and traffic costs** can become an issue.
  - In this case, it makes sense for services to **forward traffic** to pods that aren’t far from the pod where the traffic originates.

- `svc.spec.internalTrafficPolicy` field
  - `local`:
    - traffic from `pods` on a given `node` is **forwarded only to** `pods` on the **same node**.
    - If there are **no** node-local service endpoints, the **connection fails**.

---

## Topology-Aware Routing (TAR)

- `Topology-Aware Routing (TAR)`

  - intelligently directs network traffic to stay **within the same physical zone** (like an AWS Availability Zone) where it started, reducing latency, cutting cloud provider costs for cross-zone data transfer, and improving performance by keeping communication local

- all cluster `nodes` must contain the `kubernetes.io/zone` label to **indicate which zone** each node is located in.
- `service.kubernetes.io/topology-aware-hints`=`auto`

  - adds the hints to each endpoint in the `EndpointSlice` object(s)

- Example:

```yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: example-hints
  labels:
    kubernetes.io/service-name: example-svc
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 80
endpoints:
  - addresses:
      - "10.1.2.3"
    conditions:
      ready: true
    hostname: pod-1
    zone: zone-a
    hints: # hint
      forZones:
        - name: "zone-a"
```

---

## readiness probes

- `readiness probes`
  - allows an application to signal that it’s **ready to accept connections**.
  - periodically determine the **readiness status** of the `pod`.
    - If the probe is **successful**, the pod is considered ready
    - if it fails, **removed** as an `endpoint` from the services to which it belongs, `service` **doesn’t forward** connections to the pod
- **developer** decides what `readiness` means in the **context of their application**.

- `initialDelaySeconds` field
  - time after starting the container
- `periodSeconds` field
- `failureThreshold` field
- `timeoutSeconds` field
- `successThreshold` field

- When `startup probe` is defined, the **initial delay** for the `readiness probe` **begins** when the `startup probe` **succeeds**.

  - When the container is **ready**, the `pod` becomes an `endpoint` of the `services` whose **label selector it matches**.
  - When it’s no longer ready, it’s **removed** from those services.

- `Pods` don’t become `service endpoints` until they’re ready.

---

### readiness probe types

- `exec probe`
  - executes a process in the container.
  - The `exit code` used to terminate the process **determines** whether the container is **ready** or not.
- ` httpGet probe`

  - sends a `GET` request to the container via HTTP or HTTPS.
  - The **response code** determines the container’s readiness status.
    - successful: `response code` > 200 and < 400
    - fails: `response code` is anything else; or the connection attempt fails

- `tcpSocket probe`
  - **opens a TCP connection** to a specified port on the container.
  - If the connection is established, the container is considered ready.

---

- When requires all pods in a group to get A, AAAA, and SRV records **even though they aren’t ready**.
  - set the `publishNotReadyAddresses` field = `true`
  - **nonready pods** are marked as **ready** in both the `Endpoints` and `EndpointSlice` objects.
  - Components like the cluster DNS treat them as ready.

---

- Debatable use case: use readiness probe to check dependency
  - e.g., check the database / cache db ready
  - it makes sense to check if the underlying services are down.
  - however, it also raises problem that once the dependent services are not ready, all the pods are removed from the endpionts, leading that the current pods are unavailabe and take time (successThrehold\*periodSeconds) to recover.
  - As a rule of thumb, `readiness probes` **shouldn’t** test **external dependencies**, but **can test** dependencies **within the same pod**.

---

## Lab: Readiness Probe - httpGet

```yaml
# demo-readiness-probe-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-readiness-probe-pod
  labels:
    app: readiness
spec:
  containers:
    - name: nginx
      image: nginx
      readinessProbe:
        httpGet:
          path: /healthz
          port: 80
          scheme: HTTP
        initialDelaySeconds: 5
        periodSeconds: 10
        timeoutSeconds: 2
        failureThreshold: 3
```

```sh
kubectl apply -f demo-readiness-probe-pod.yaml
# pod/demo-readiness-probe-pod created

kubectl get pod
# NAME                       READY   STATUS    RESTARTS      AGE
# demo-readiness-probe-pod   0/1     Running   0             93s

kubectl describe pod demo-readiness-probe-pod
# Labels:           app=readiness
# Containers:
#   nginx:
#     Ready:          False
#     Readiness:      http-get http://:80/ delay=5s timeout=2s period=10s #success=1 #failure=3
# Events:
#   Type     Reason     Age                From               Message
#   ----     ------     ----               ----               -------
#   Normal   Created    110s               kubelet            Created container: nginx
#   Normal   Started    110s               kubelet            Started container nginx
#   Warning  Unhealthy  0s (x11 over 98s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 404
```

```yaml
# demo-readiness-probe-svc.yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-readiness-probe-svc
spec:
  type: ClusterIP
  selector:
    app: readiness
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 80
```

```sh
kubectl apply -f demo-readiness-probe-svc.yaml
# service/demo-readiness-probe-svc created

kubectl get svc
# NAME                        TYPE           CLUSTER-IP       EXTERNAL-IP        PORT(S)          AGE
# demo-readiness-probe-svc    ClusterIP      10.104.231.1     <none>             8080/TCP         86s

kubectl describe endpointslices demo-readiness-probe-svc
# Name:         demo-readiness-probe-svc-bzspz
# Namespace:    default
# Labels:       endpointslice.kubernetes.io/managed-by=endpointslice-controller.k8s.io
#               kubernetes.io/service-name=demo-readiness-probe-svc
# Annotations:  endpoints.kubernetes.io/last-change-trigger-time: 2025-12-29T21:07:51Z
# AddressType:  IPv4
# Ports:
#   Name  Port  Protocol
#   ----  ----  --------
#   http  80    TCP
# Endpoints:
#   - Addresses:  10.1.3.44
#     Conditions:
#       Ready:    false
#     Hostname:   <unset>
#     TargetRef:  Pod/demo-readiness-probe-pod
#     NodeName:   docker-desktop
#     Zone:       <unset>
# Events:         <none>
```

> endpointslice shows pod but not ready

---

- update yaml

```yaml
# demo-readiness-probe-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-readiness-probe-pod
  labels:
    app: readiness
spec:
  containers:
    - name: nginx
      image: nginx
      readinessProbe:
        httpGet:
          path: / # update path
          port: 80
          scheme: HTTP
        initialDelaySeconds: 5
        periodSeconds: 10
        timeoutSeconds: 2
        failureThreshold: 3
```

```sh
kubectl replace --force -f demo-readiness-probe-pod.yaml
# pod "demo-readiness-probe-pod" deleted from default namespace
# pod/demo-readiness-probe-pod replaced

# confirm
kubectl describe pod/demo-readiness-probe-pod
# Name:             demo-readiness-probe-pod
# Status:           Running
# Containers:
#   nginx:
#     Ready:          False
#     Readiness:      http-get http://:80/ delay=5s timeout=2s period=10s #success=1 #failure=3

kubectl describe svc demo-readiness-probe-svc
# Name:                     demo-readiness-probe-svc
# Namespace:                default
# Labels:                   <none>
# Annotations:              <none>
# Selector:                 app=readiness
# Type:                     ClusterIP
# IP Family Policy:         SingleStack
# IP Families:              IPv4
# IP:                       10.104.231.1
# IPs:                      10.104.231.1
# Port:                     http  8080/TCP
# TargetPort:               80/TCP
# Endpoints:                10.1.3.46:80
# Session Affinity:         None
# Internal Traffic Policy:  Cluster
# Events:                   <none>


kubectl describe endpointslices demo-readiness-probe-svc
# Name:         demo-readiness-probe-svc-bzspz
# Namespace:    default
# Labels:       endpointslice.kubernetes.io/managed-by=endpointslice-controller.k8s.io
#               kubernetes.io/service-name=demo-readiness-probe-svc
# Annotations:  endpoints.kubernetes.io/last-change-trigger-time: 2025-12-29T21:15:31Z
# AddressType:  IPv4
# Ports:
#   Name  Port  Protocol
#   ----  ----  --------
#   http  80    TCP
# Endpoints:
#   - Addresses:  10.1.3.46
#     Conditions:
#       Ready:    true
#     Hostname:   <unset>
#     TargetRef:  Pod/demo-readiness-probe-pod
#     NodeName:   docker-desktop
#     Zone:       <unset>
# Events:         <none>
```
