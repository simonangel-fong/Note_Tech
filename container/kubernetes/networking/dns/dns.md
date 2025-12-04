# Kubernetes - Cluster DNS

[Back](../../index.md)

- [Kubernetes - Cluster DNS](#kubernetes---cluster-dns)
  - [DNS Solution within the Cluster](#dns-solution-within-the-cluster)
  - [CoreDNS](#coredns)
  - [Lab: CoreDNS](#lab-coredns)

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

