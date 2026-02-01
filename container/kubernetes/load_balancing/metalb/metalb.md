# Kubernetes Networking: Load Balancing - MetalLB

[Back](../../index.md)

- [Kubernetes Networking: Load Balancing - MetalLB](#kubernetes-networking-load-balancing---metallb)
  - [Lab: Install `MetalLB`](#lab-install-metallb)

---

## Lab: Install `MetalLB`

```sh
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.15.3/config/manifests/metallb-native.yaml
# namespace/metallb-system created
# customresourcedefinition.apiextensions.k8s.io/bfdprofiles.metallb.io created
# customresourcedefinition.apiextensions.k8s.io/bgpadvertisements.metallb.io created
# customresourcedefinition.apiextensions.k8s.io/bgppeers.metallb.io created
# customresourcedefinition.apiextensions.k8s.io/communities.metallb.io created
# customresourcedefinition.apiextensions.k8s.io/configurationstates.metallb.io created
# customresourcedefinition.apiextensions.k8s.io/ipaddresspools.metallb.io created
# customresourcedefinition.apiextensions.k8s.io/l2advertisements.metallb.io created
# customresourcedefinition.apiextensions.k8s.io/servicebgpstatuses.metallb.io created
# customresourcedefinition.apiextensions.k8s.io/servicel2statuses.metallb.io created
# serviceaccount/controller created
# serviceaccount/speaker created
# role.rbac.authorization.k8s.io/controller created
# role.rbac.authorization.k8s.io/pod-lister created
# clusterrole.rbac.authorization.k8s.io/metallb-system:controller created
# clusterrole.rbac.authorization.k8s.io/metallb-system:speaker created
# rolebinding.rbac.authorization.k8s.io/controller created
# rolebinding.rbac.authorization.k8s.io/pod-lister created
# clusterrolebinding.rbac.authorization.k8s.io/metallb-system:controller created
# clusterrolebinding.rbac.authorization.k8s.io/metallb-system:speaker created
# configmap/metallb-excludel2 created
# secret/metallb-webhook-cert created
# service/metallb-webhook-service created
# deployment.apps/controller created
# daemonset.apps/speaker created
# validatingwebhookconfiguration.admissionregistration.k8s.io/metallb-webhook-configuration created

# confirm
kubectl get pods -n metallb-system
# NAME                         READY   STATUS    RESTARTS   AGE
# controller-9c6cff498-bxxf7   1/1     Running   0          50s
# speaker-9xdrj                1/1     Running   0          50s
# speaker-fh4fg                1/1     Running   0          50s
# speaker-lr7qg                1/1     Running   0          50s

# Create IPAddressPool that MetalLB can assign from.
tee ~/metallb-ip-pool.yaml <<EOF
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: web-pool
  namespace: metallb-system
spec:
  addresses:
  - 192.168.10.200-192.168.10.210
EOF

kubectl apply -f ~/metallb-ip-pool.yaml
# ipaddresspool.metallb.io/web-pool created

k get IPAddressPool web-pool -n metallb-system
# NAME       AUTO ASSIGN   AVOID BUGGY IPS   ADDRESSES
# web-pool   true          false             ["192.168.10.200-192.168.10.210"]

# Create L2Advertisement to announce those IPs via ARP.
tee ~/metallb-l2adv.yaml <<EOF
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: web-l2
  namespace: metallb-system
spec:
  ipAddressPools:
  - web-pool
EOF

kubectl apply -f ~/metallb-l2adv.yaml
# l2advertisement.metallb.io/web-l2 created

kubectl get L2Advertisement web-l2 -n metallb-system
# NAME     IPADDRESSPOOLS   IPADDRESSPOOL SELECTORS   INTERFACES
# web-l2   ["web-pool"]


# confirm: MetalLB assign an external IP to Nginx Gateway Service
kubectl get svc -n nginx-gateway
# NAME                TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)        AGE
# nginx-gateway       ClusterIP      10.110.3.253     <none>           443/TCP        4d23h
# web-gateway-nginx   LoadBalancer   10.101.172.191   192.168.10.201   80:30603/TCP   20m
```

---
