# Kubernetes Networking: Cluster DNS

[Back](../../index.md)

- [Kubernetes Networking: Cluster DNS](#kubernetes-networking-cluster-dns)
  - [DNS Solution within the Cluster](#dns-solution-within-the-cluster)
    - [Services \& Namespace:](#services--namespace)
  - [CoreDNS](#coredns)
    - [Lab: CoreDNS](#lab-coredns)
    - [Lab: Explore DNS](#lab-explore-dns)

---

## DNS Solution within the Cluster

- Help resolve the DNS for the pod
- By default:
  - K8s deploys **built-in DNS**
- Whenever a `service` is **created**, k8s **creates a records** in `cluster DNS`, mapping `DNS name` to `IP`

  - any pod within the cluster can access the `service` **using `service name`**

### Services & Namespace:

- same ns:
  - `svc_name`
  - e.g., `curl http://web-service`
- different ns:

  - `svc_name.ns_name`: service name act as subdomain, the namespace is the domain
  - e.g., `curl http://web-service.apps`

- All services are grouped by a domain `svc`
  - `svc_name.ns_name.svc`
  - e.g., `web-service.apps.svc` is a service named web-service in the apps namespace
- All resources are grouped in the `root domain` for the cluster `cluster.local`

- A `CNAME record` is a DNS record that **maps** an `alias` to an **existing DNS name** instead of an IP address.

  - Can create an **alias** in k8s DNS

- Example of an `Fully Qaullify Domain Name` in a cluster

| Service/pod | Hostname    | namespace | Type | Root          | FQDN                                   | IP            |
| ----------- | ----------- | --------- | ---- | ------------- | -------------------------------------- | ------------- |
| Service     | web-service | apps      | svc  | cluster.local | `web-service.apps.svc.cluster.local`   | 10.107.37.188 |
| pod         | 10-244-2-5  | default   | pod  | cluster.local | `10-244-2-5.default.pod.cluster.local` | 10.244.2.5    |

- `curl http://web-service.apps.svc.cluster.local`

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

### Lab: CoreDNS

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

### Lab: Explore DNS

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
