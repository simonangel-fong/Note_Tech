# Cilium - Install

[Back](../index.md)

- [Cilium - Install](#cilium---install)
  - [Installation](#installation)
  - [Deploy Star Wars Demo](#deploy-star-wars-demo)

---

## Installation

```sh
# ##############################
# Install docker
# ##############################
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


# ##############################
# create kind cluster
# ##############################
curl -LO https://raw.githubusercontent.com/cilium/cilium/1.20.2/Documentation/installation/kind-config.yaml
kind create cluster --config=kind-config.yaml
# kubectl cluster-info --context kind-kind

k get node
# NAME                 STATUS     ROLES           AGE    VERSION
# kind-control-plane   NotReady   control-plane   114s   v1.37.0
# kind-worker          NotReady   <none>          104s   v1.37.0
# kind-worker2         NotReady   <none>          104s   v1.37.0
# kind-worker3         NotReady   <none>          104s   v1.37.0

# ##############################
# Install the Cilium CLI
# ##############################
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then CLI_ARCH=arm64; fi
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-${CLI_ARCH}.tar.gz.sha256sum
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}


# Install Cilium
cilium install 1.20.2
watch -n 1 cilium status

# confirm
cilium connectivity test
```

---

## Deploy Star Wars Demo

```sh
kubectl create -f https://raw.githubusercontent.com/cilium/cilium/1.20.2/examples/minikube/http-sw-app.yaml

# confirm
kubectl get pods,svc
# NAME                             READY   STATUS    RESTARTS   AGE
# pod/deathstar-7cfbb6d849-4nz5s   1/1     Running   0          21s
# pod/deathstar-7cfbb6d849-hwglr   1/1     Running   0          21s
# pod/tiefighter                   1/1     Running   0          21s
# pod/xwing                        1/1     Running   0          21s

# NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
# service/deathstar    ClusterIP   10.96.226.11   <none>        80/TCP    21s
# service/kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP   32m

# inspect endpoint
kubectl -n kube-system get pods -l k8s-app=cilium
# NAME           READY   STATUS    RESTARTS   AGE
# cilium-bh64m   1/1     Running   0          27m
# cilium-c6kxx   1/1     Running   0          27m
# cilium-g4pdl   1/1     Running   0          27m
# cilium-qfwzg   1/1     Running   0          27m

kubectl -n kube-system exec cilium-bh64m -- cilium-dbg endpoint list
# ENDPOINT   POLICY (ingress)   POLICY (egress)   IDENTITY   LABELS (source:key[=value])                                                         IPv6   IPv4           STATUS
#            ENFORCEMENT        ENFORCEMENT
# 176        Disabled           Disabled          4          reserved:health                                                                            10.244.1.48    ready
# 228        Disabled           Disabled          1          reserved:host                                                                                             ready
# 422        Disabled           Disabled          52738      k8s:app=local-path-provisioner                                                             10.244.1.4     ready
#                                                            k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=local-path-storage
#                                                            k8s:io.cilium.k8s.policy.cluster=kind-kind
#                                                            k8s:io.cilium.k8s.policy.serviceaccount=local-path-provisioner-service-account
#                                                            k8s:io.kubernetes.pod.namespace=local-path-storage
# 1185       Disabled           Disabled          1433       gen:io.cilium.k8s.named-ports-1=metrics.TCP.9153_readiness-probe.TCP.8181                  10.244.1.175   ready
#                                                            gen:io.cilium.k8s.named-ports=dns.UDP.53_dns-tcp.TCP.53_liveness-probe.TCP.8080
#                                                            k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=kube-system
#                                                            k8s:io.cilium.k8s.policy.cluster=kind-kind
#                                                            k8s:io.cilium.k8s.policy.serviceaccount=coredns
#                                                            k8s:io.kubernetes.pod.namespace=kube-system
#                                                            k8s:k8s-app=kube-dns
# 1359       Disabled           Disabled          51704      k8s:io.cilium.k8s.namespace.labels.app.kubernetes.io/name=cilium-cli                       10.244.1.75    ready
#                                                            k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=cilium-test-ccnp2
#                                                            k8s:io.cilium.k8s.policy.cluster=kind-kind
#                                                            k8s:io.cilium.k8s.policy.serviceaccount=client-ccnp
#                                                            k8s:io.kubernetes.pod.namespace=cilium-test-ccnp2
#                                                            k8s:kind=ccnp
#                                                            k8s:name=client-ccnp
# 1784       Disabled           Disabled          1433       gen:io.cilium.k8s.named-ports-1=metrics.TCP.9153_readiness-probe.TCP.8181                  10.244.1.103   ready
#                                                            gen:io.cilium.k8s.named-ports=dns.UDP.53_dns-tcp.TCP.53_liveness-probe.TCP.8080
#                                                            k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=kube-system
#                                                            k8s:io.cilium.k8s.policy.cluster=kind-kind
#                                                            k8s:io.cilium.k8s.policy.serviceaccount=coredns
#                                                            k8s:io.kubernetes.pod.namespace=kube-system
#                                                            k8s:k8s-app=kube-dns
# 2801       Disabled           Disabled          27235      k8s:app.kubernetes.io/name=deathstar                                                       10.244.1.16    ready
#                                                            k8s:class=deathstar
#                                                            k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=default
#                                                            k8s:io.cilium.k8s.policy.cluster=kind-kind
#                                                            k8s:io.cilium.k8s.policy.serviceaccount=default
#                                                            k8s:io.kubernetes.pod.namespace=default
#                                                            k8s:org=empire
# 2892       Disabled           Disabled          14244      k8s:io.cilium.k8s.namespace.labels.app.kubernetes.io/name=cilium-cli                       10.244.1.52    ready
#                                                            k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=cilium-test-ccnp1
#                                                            k8s:io.cilium.k8s.policy.cluster=kind-kind
#                                                            k8s:io.cilium.k8s.policy.serviceaccount=client-ccnp
#                                                            k8s:io.kubernetes.pod.namespace=cilium-test-ccnp1
#                                                            k8s:kind=ccnp
#                                                            k8s:name=client-ccnp
# 3183       Disabled           Disabled          39424      k8s:app.kubernetes.io/name=xwing                                                           10.244.1.78    ready
#                                                            k8s:class=xwing
#                                                            k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=default
#                                                            k8s:io.cilium.k8s.policy.cluster=kind-kind
#                                                            k8s:io.cilium.k8s.policy.serviceaccount=default
#                                                            k8s:io.kubernetes.pod.namespace=default
#                                                            k8s:org=alliance
```
