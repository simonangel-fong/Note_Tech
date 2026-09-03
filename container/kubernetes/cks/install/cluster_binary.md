# Advanced - Install cluster with binary

[back](../../index.md)

- [Advanced - Install cluster with binary](#advanced---install-cluster-with-binary)
    - [Prepare directories](#prepare-directories)
    - [Audit policy](#audit-policy)
    - [Install `kube-scheduler`](#install-kube-scheduler)
    - [Verify control plane](#verify-control-plane)
  - [Confirm encryption at rest](#confirm-encryption-at-rest)
    - [RBAC for apiserver -\> kubelet](#rbac-for-apiserver---kubelet)
  - [Install `kubelet` and `kube-proxy`](#install-kubelet-and-kube-proxy)
  - [Phase 7: CNI](#phase-7-cni)
  - [Phase 8: CoreDNS](#phase-8-coredns)
    - [If CoreDNS is in `CrashLoopBackOff`](#if-coredns-is-in-crashloopbackoff)
  - [Verification](#verification)
    - [Control plane completion checklist](#control-plane-completion-checklist)

---

---

### Prepare directories

Both directories below are referenced by the apiserver flags and by nothing
that creates them -- miss these and `kube-apiserver` exits immediately.

```sh
# holds encryption-config.yaml, audit-policy.yaml, kube-scheduler.yaml
sudo mkdir -pv /etc/kubernetes/config
# mkdir: created directory '/etc/kubernetes/config'

# --audit-log-path writes here
sudo mkdir -pv /var/log/kubernetes
# mkdir: created directory '/var/log/kubernetes'
```

---

### Audit policy

```sh
cat <<'EOF' | sudo tee /etc/kubernetes/config/audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages:
  - RequestReceived
rules:
  - level: RequestResponse
    resources:
      - group: ""
        resources: ["secrets", "configmaps"]
  - level: Metadata
EOF
```

---


### Install `kube-scheduler`

```sh
export K8S_VERSION=v1.35.8

# ##############################
# Download kube-scheduler
# ##############################
cd /tmp
curl -L -o kube-scheduler "https://dl.k8s.io/${K8S_VERSION}/bin/linux/amd64/kube-scheduler"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100 46.1M  100 46.1M    0     0  11.4M      0  0:00:04  0:00:04 --:--:-- 11.4M

sudo install -v -m 755 kube-scheduler /usr/local/bin/
# 'kube-scheduler' -> '/usr/local/bin/kube-scheduler'

kube-scheduler --version
# Kubernetes v1.35.8

# ##############################
# Configure kube-scheduler
# ##############################
cat <<'EOF' | sudo tee /etc/kubernetes/config/kube-scheduler.yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
clientConnection:
  kubeconfig: /etc/kubernetes/kube-scheduler.kubeconfig
leaderElection:
  leaderElect: true
EOF

# ##############################
# Configure systemd unit: kube-scheduler
# ##############################
cat <<'EOF' | sudo tee /etc/systemd/system/kube-scheduler.service
[Unit]
Description=Kubernetes Scheduler
Documentation=https://kubernetes.io/docs/concepts/overview/components/
After=kube-apiserver.service

[Service]
ExecStart=/usr/local/bin/kube-scheduler \
  --config=/etc/kubernetes/config/kube-scheduler.yaml \
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# reload config
sudo systemctl daemon-reload
# start and enable
sudo systemctl enable --now kube-scheduler
# Created symlink /etc/systemd/system/multi-user.target.wants/kube-scheduler.service → /etc/systemd/system/kube-scheduler.service.

# confirm
sudo systemctl status kube-scheduler --no-pager
# ● kube-scheduler.service - Kubernetes Scheduler
#      Loaded: loaded (/etc/systemd/system/kube-scheduler.service; enabled; preset: enabled)
#      Active: active (running) since Wed 2026-09-02 17:53:35 EDT; 11s ago
#        Docs: https://kubernetes.io/docs/concepts/overview/components/
#    Main PID: 3613 (kube-scheduler)
#       Tasks: 9 (limit: 7689)
#      Memory: 13.1M (peak: 13.3M)
#         CPU: 242ms
#      CGroup: /system.slice/kube-scheduler.service
#              └─3613 /usr/local/bin/kube-scheduler --config=/etc/kubernetes/config/kube-scheduler.yaml --v=2

# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570145    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570223    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570252    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570263    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570275    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570003    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570439    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.569931    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.661775    3613 leaderelection.go:258] "Attempting to acqui…heduler"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.668143    3613 leaderelection.go:272] "Successfully acquir…heduler"
# Hint: Some lines were ellipsized, use -l to show in full.
```

---

### Verify control plane

```sh
sudo systemctl status kube-apiserver kube-controller-manager kube-scheduler --no-pager

# component health
kubectl get --raw='/readyz?verbose'
# [+]ping ok
# [+]log ok
# [+]etcd ok
# [+]etcd-readiness ok
# [+]informer-sync ok
# [+]poststarthook/start-apiserver-admission-initializer ok
# [+]poststarthook/generic-apiserver-start-informers ok
# [+]poststarthook/priority-and-fairness-config-consumer ok
# [+]poststarthook/priority-and-fairness-filter ok
# [+]poststarthook/storage-object-count-tracker-hook ok
# [+]poststarthook/start-apiextensions-informers ok
# [+]poststarthook/start-apiextensions-controllers ok
# [+]poststarthook/crd-informer-synced ok
# [+]poststarthook/start-system-namespaces-controller ok
# [+]poststarthook/start-cluster-authentication-info-controller ok
# [+]poststarthook/start-kube-apiserver-identity-lease-controller ok
# [+]poststarthook/start-kube-apiserver-identity-lease-garbage-collector ok
# [+]poststarthook/start-legacy-token-tracking-controller ok
# [+]poststarthook/start-service-ip-repair-controllers ok
# [+]poststarthook/rbac/bootstrap-roles ok
# [+]poststarthook/scheduling/bootstrap-system-priority-classes ok
# [+]poststarthook/priority-and-fairness-config-producer ok
# [+]poststarthook/bootstrap-controller ok
# [+]poststarthook/start-kubernetes-service-cidr-controller ok
# [+]poststarthook/aggregator-reload-proxy-client-cert ok
# [+]poststarthook/start-kube-aggregator-informers ok
# [+]poststarthook/apiservice-status-local-available-controller ok
# [+]poststarthook/apiservice-status-remote-available-controller ok
# [+]poststarthook/apiservice-registration-controller ok
# [+]poststarthook/apiservice-discovery-controller ok
# [+]poststarthook/kube-apiserver-autoregistration ok
# [+]autoregister-completion ok
# [+]poststarthook/apiservice-openapi-controller ok
# [+]poststarthook/apiservice-openapiv3-controller ok
# [+]shutdown ok
# readyz check passed

kubectl cluster-info
# Kubernetes control plane is running at https://127.0.0.1:6443

# get lease
kubectl -n kube-system get lease
# NAME                                   HOLDER                                                                      AGE
# apiserver-ivtlveyukuyrha5ia44unn7io4   apiserver-ivtlveyukuyrha5ia44unn7io4_dd022c6a-3c0c-486c-9601-5ea07599f05f   7m56s
# kube-controller-manager                controlplane_8cd40c99-2c7d-437f-9252-28f342842551                           4m21s
# kube-scheduler                         controlplane_658947a0-c1b6-49c9-ad75-2d15b38166c2                           114s
```

---

## Confirm encryption at rest

```sh
# sample secret to test
kubectl create secret generic sample-test --from-literal=key=value
# secret/sample-test created

# get from etcd
sudo etcdctl get /registry/secrets/default/sample-test --hex \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/ca.pem \
  --cert=/etc/kubernetes/pki/etcd-server.pem \
  --key=/etc/kubernetes/pki/etcd-server-key.pem | head -5
# \x2f\x72\x65\x67\x69\x73\x74\x72\x79\x2f\x73\x65\x63\x72\x65\x74\x73\x2f\x64\x65\x66\x61\x75\x6c\x74\x2f\x73\x61\x6d\x70\x6c\x65\x2d\x74\x65\x73\x74
# \x6b\x38\x73\x3a\x65\x6e\x63\x3a\x61\x65\x73\x63\x62\x63\x3a\x76\x31\x3a\x6b\x65\x79\x31\x3a\x3f\xd9\x0f\xb0\x38\x25\x81\xca\x8d\xe6\x31\x73\x57\x0f\x23\x8c\x2a\x74\xa7\x2c\xef\xfd\x89\x09\x7e\xf3\x3f\x55\x52\x7b\xad\x39\xe5\xa5\x8d\x73\x7d\xb4\x2d\x59\x04\x66\x0b\xdd\x2a\x7c\x70\xac\x71\x9e\x38\x8b\xaf\x07\x5e\x46\xd7\x65\x8f\x87\xe1\xd0\x10\xdd\x75\x7d\x3c\x59\xda\xe0\x04\xa5\xa1\x35\x7e\xc4\xc3\x6a\xa6\x6b\x00\xfb\x41\x8c\x58\x61\xd3\x80\xbb\x44\xab\xcc\xc3\xa4\x69\x76\xca\x40\x2e\xfc\x91\xdc\x0b\x16\x0a\x2f\x5f\xf6\xbd\x55\xcc\xe9\x1e\x1b\xc5\x06\x2a\xf8\xb7\x85\xd7\xb6\xb3\x84\x27\x21\x07\x6b\xe5\x27\x6a\xcf\x5a\x8b\x5e\xdb\x30\xd9\x8b\x08\xdc\x7a\x33\xe4\x39\x38\x05\xc6\x95\x01\x84\x9b\xb7\x7d\xec\xab\x3a\x40\x8e\x96\x42\x04\xcc\x23\xd5\x52\x03\x2d\xae\x7b\x21\x49\x0c\x64\xf2\x9f\x1a\xad\x44\x5b\xa0\xe2\xcb\x81\x54\x88\xe8\x63\x45\x1c\xdb\x84\x16\xbe\xec\x9f\xa2\x6d\xed\x14\x8b\x71\x2e\x43\xe8\xb8\xd2\x60\x72\xf1\x76\xc9\xb3\x1a\x64\xc0\xba\xf5\x8e\x1e\x02\xa1\xcb\x20\x6f\x73\x26\x86\xc7\xeb\x13\xb2\x13\x39\x27\x62\x7e\x88\xb3\x71\xc5\x6a\x12\xda\xab\xf8\x94\x3c\x31\x1a\xb9\xed\x6f\xc1\xbb\xa0

kubectl delete secret sample-test
# secret "sample-test" deleted from default namespac
```

---

### RBAC for apiserver -> kubelet

The apiserver needs explicit permission to reach kubelet endpoints, or
`kubectl logs` and `kubectl exec` fail with 403.

```sh
cat <<'EOF' | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: system:kube-apiserver-to-kubelet
rules:
  - apiGroups: [""]
    resources:
      - nodes/proxy
      - nodes/stats
      - nodes/log
      - nodes/spec
      - nodes/metrics
    verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: system:kube-apiserver
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:kube-apiserver-to-kubelet
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: User
    name: kube-apiserver-kubelet-client
EOF
# clusterrole.rbac.authorization.k8s.io/system:kube-apiserver-to-kubelet created
# clusterrolebinding.rbac.authorization.k8s.io/system:kube-apiserver created
```

The `name` here must match the `CN` of `apiserver-kubelet-client` exactly.

---

## Install `kubelet` and `kube-proxy`

```sh
export K8S_VERSION=v1.35.8

cd /tmp

# ##############################
# Install kubelet
# ##############################
curl -L -o "kubelet" "https://dl.k8s.io/${K8S_VERSION}/bin/linux/amd64/kubelet"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100 56.2M  100 56.2M    0     0  13.4M      0  0:00:04  0:00:04 --:--:-- 13.7M

sudo install -m 755 "kubelet" /usr/local/bin/
# 'kubelet' -> '/usr/local/bin/kubelet'

# ##############################
# Install kube-proxy
# ##############################
curl -L -o "kube-proxy" "https://dl.k8s.io/${K8S_VERSION}/bin/linux/amd64/kube-proxy"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100 41.8M  100 41.8M    0     0  10.0M      0  0:00:04  0:00:04 --:--:-- 10.5M

sudo install -m 755 "kube-proxy" /usr/local/bin/
# 'kube-proxy' -> '/usr/local/bin/kube-proxy'

# ##############################
# kubelet config
# ##############################
sudo install -v -m 644 ~/pki/controlplane.crt /var/lib/kubelet/controlplane.pem
# '/home/ubuntuadmin/pki/controlplane.crt' -> '/var/lib/kubelet/controlplane.pem'
sudo install -v -m 600 ~/pki/controlplane.key /var/lib/kubelet/controlplane-key.pem
# '/home/ubuntuadmin/pki/controlplane.key' -> '/var/lib/kubelet/controlplane-key.pem'
sudo install -v -m 644 ~/pki/ca.crt /var/lib/kubernetes/ca.pem
# '/home/ubuntuadmin/pki/ca.crt' -> '/var/lib/kubernetes/ca.pem'

# ##############################
# config file: kubelet
# ##############################
cat <<'EOF' | sudo tee /var/lib/kubelet/kubelet-config.yaml
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
authentication:
  anonymous:
    enabled: false
  webhook:
    enabled: true
  x509:
    clientCAFile: /var/lib/kubernetes/ca.pem
authorization:
  mode: Webhook
clusterDomain: cluster.local
clusterDNS:
  - 10.96.0.10
cgroupDriver: systemd
runtimeRequestTimeout: "15m"
tlsCertFile: /var/lib/kubelet/controlplane.pem
tlsPrivateKeyFile: /var/lib/kubelet/controlplane-key.pem
readOnlyPort: 0
protectKernelDefaults: true
seccompDefault: true
EOF

# NOTE: protectKernelDefaults: true makes the kubelet REFUSE TO START unless
# the six sysctls in /etc/sysctl.d/90-kubelet.conf (Preparation) are already
# set -- it will not retune the host itself. Symptom if missing:
#   Failed to start ContainerManager: invalid kernel flag: vm/overcommit_memory
# readOnlyPort: 0 closes the unauthenticated :10255 metrics port, and
# authorization.mode: Webhook makes every kubelet API call go through the
# apiserver's RBAC -- both are named CKS hardening items.

# ##############################
# systemd unit: kubelet
# ##############################
cat <<'EOF' | sudo tee /etc/systemd/system/kubelet.service
[Unit]
Description=Kubernetes Kubelet
After=containerd.service
Requires=containerd.service

[Service]
ExecStart=/usr/local/bin/kubelet \
  --config=/var/lib/kubelet/kubelet-config.yaml \
  --kubeconfig=/var/lib/kubelet/kubeconfig \
  --container-runtime-endpoint=unix:///run/containerd/containerd.sock \
  --register-node=true \
  --node-ip=192.168.10.180 \
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF


# ##############################
# config file: kube-proxy
# ##############################
cat <<'EOF' | sudo tee /var/lib/kube-proxy/kube-proxy-config.yaml
kind: KubeProxyConfiguration
apiVersion: kubeproxy.config.k8s.io/v1alpha1
clientConnection:
  kubeconfig: /var/lib/kube-proxy/kubeconfig
mode: iptables
clusterCIDR: 10.244.0.0/16
hostnameOverride: controlplane
EOF

# ##############################
# systemd unit: kube-proxy
# ##############################
cat <<'EOF' | sudo tee /etc/systemd/system/kube-proxy.service
[Unit]
Description=Kubernetes Kube Proxy
After=kube-apiserver.service

[Service]
ExecStart=/usr/local/bin/kube-proxy \
  --config=/var/lib/kube-proxy/kube-proxy-config.yaml
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# ##############################
# start service
# ##############################
sudo systemctl daemon-reload
sudo systemctl enable --now kubelet kube-proxy
# Created symlink /etc/systemd/system/multi-user.target.wants/kubelet.service → /etc/systemd/system/kubelet.service.
# Created symlink /etc/systemd/system/multi-user.target.wants/kube-proxy.service → /etc/systemd/system/kube-proxy.service.

sudo systemctl status kubelet --no-pager
# ● kubelet.service - Kubernetes Kubelet
#      Loaded: loaded (/etc/systemd/system/kubelet.service; enabled; preset: enabled)
#      Active: active (running) since Wed 2026-09-02 18:08:32 EDT; 22ms ago
#    Main PID: 4158 (kubelet)
#       Tasks: 6 (limit: 7689)
#      Memory: 5.0M (peak: 5.0M)
#         CPU: 15ms
#      CGroup: /system.slice/kubelet.service
#              └─4158 /usr/local/bin/kubelet --config=/var/lib/kubelet/kubelet-config.yaml --kubeconfig=/var/lib/kubelet/kubeconfig --…

# Sep 02 18:08:32 controlplane systemd[1]: Started kubelet.service - Kubernetes Kubelet.

# ##############################
# confirm registration
# ##############################
# the kubelet stays "active (running)" even when registration fails -- it
# retries silently -- so systemctl status alone proves nothing. Read the log.
sudo journalctl -u kubelet -n 20 --no-pager --output=cat
# "Successfully registered node" node="controlplane"

kubectl get nodes
# NAME           STATUS     ROLES    AGE   VERSION
# controlplane   NotReady   <none>   15s   v1.35.8

sudo systemctl status kube-proxy --no-pager
# ● kube-proxy.service - Kubernetes Kube Proxy
#      Loaded: loaded (/etc/systemd/system/kube-proxy.service; enabled; preset: enabled)
#      Active: active (running) since Wed 2026-09-02 18:08:32 EDT; 17min ago
#    Main PID: 4157 (kube-proxy)
#       Tasks: 6 (limit: 7689)
#      Memory: 11.6M (peak: 14.3M)
#         CPU: 2.824s
#      CGroup: /system.slice/kube-proxy.service
#              └─4157 /usr/local/bin/kube-proxy --config=/var/lib/kube-proxy/kube-proxy-config.yaml

# Sep 02 18:19:05 controlplane kube-proxy[4157]: E0902 18:19:05.091011    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:19:53 controlplane kube-proxy[4157]: E0902 18:19:53.631932    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:20:47 controlplane kube-proxy[4157]: E0902 18:20:47.185752    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:21:26 controlplane kube-proxy[4157]: E0902 18:21:26.932890    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:22:06 controlplane kube-proxy[4157]: E0902 18:22:06.464710    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:22:57 controlplane kube-proxy[4157]: E0902 18:22:57.770523    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:23:46 controlplane kube-proxy[4157]: E0902 18:23:46.196506    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:24:18 controlplane kube-proxy[4157]: E0902 18:24:18.379399    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:25:12 controlplane kube-proxy[4157]: E0902 18:25:12.179101    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:26:08 controlplane kube-proxy[4157]: E0902 18:26:08.089221    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Hint: Some lines were ellipsized, use -l to show in full.
```

---

## Phase 7: CNI

See also: [Cilium](../../cilium.md).

```sh
# get stable version
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)

# download
curl -L --fail -o /tmp/cilium.tar.gz \
  "https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-amd64.tar.gz"

#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
#   0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
# 100 72.6M  100 72.6M    0     0  29.7M      0  0:00:02  0:00:02 --:--:-- 34.0M

sudo tar xzvfC /tmp/cilium.tar.gz /usr/local/bin
# cilium

cilium install \
  --set ipam.mode=kubernetes \
  --set k8sServiceHost=192.168.10.180 \
  --set k8sServicePort=6443

# ℹ️  Using Cilium version 1.20.1
# 🔮 Auto-detected cluster name: kubernetes

cilium status --wait
#     /¯¯\
#  /¯¯\__/¯¯\    Cilium:             OK
#  \__/¯¯\__/    Operator:           OK
#  /¯¯\__/¯¯\    Envoy DaemonSet:    OK
#  \__/¯¯\__/    Hubble Relay:       disabled
#     \__/       ClusterMesh:        disabled

# DaemonSet              cilium                   Desired: 1, Ready: 1/1, Available: 1/1
# DaemonSet              cilium-envoy             Desired: 1, Ready: 1/1, Available: 1/1
# Deployment             cilium-operator          Desired: 1, Ready: 1/1, Available: 1/1
# Containers:            cilium                   Running: 1
#                        cilium-envoy             Running: 1
#                        cilium-operator          Running: 1
#                        clustermesh-apiserver
#                        hubble-relay
# Cluster Pods:          2/2 managed by Cilium
# Helm chart version:    1.20.1
# Image versions         cilium             quay.io/cilium/cilium:v1.20.1@sha256:ae9ea21f7427fe24bc6ea7247eb552157a1b0a431744045d3f641545ca71d11b: 1
#                        cilium-envoy       quay.io/cilium/cilium-envoy:v1.37.5-1786810558-766ccfb37260a43e9d228837aa84ce3faf9f64e7@sha256:75b8094c7127736a2ffd2dce3945e0931cb6df21b0372ff661940eca26730b91: 1
#                        cilium-operator    quay.io/cilium/operator-generic:v1.20.1@sha256:6c3885fc7b629099fdbe2a5c87869c86feb825fa18fae299eac0f61918d16ecf: 1

# confirm by node
kubectl get nodes
# NAME           STATUS   ROLES    AGE     VERSION
# controlplane   Ready    <none>   4m48s   v1.35.8

# confirm dataplane
kubectl -n kube-system exec ds/cilium -- cilium-dbg status \
  | grep -iE 'kubeproxyreplacement|masquerad|routing'

# KubeProxyReplacement:    True   [ens33      192.168.10.180 10.0.0.167 2607:fea8:2adc:8500:82fc:e402:83ea:c9f6 2607:fea8:2adc:8500:20c:29ff:fecd:d439 fe80::20c:29ff:fecd:d439 (Direct Routing)]
# Routing:                 Network: Tunnel [vxlan]   Host: Legacy
# Masquerading:            IPTables [IPv4: Enabled, IPv6: Disabled]

# pod egress
kubectl run nettest --image=busybox:1.36 --rm -it --restart=Never -- \
  nslookup kubernetes.io 8.8.8.8
```

If `nslookup` times out, pod egress is broken -- fix it here, not in Phase 8.
Locate the drop with:

```sh
kubectl -n kube-system exec ds/cilium -- cilium-dbg monitor --type drop
```

---

## Phase 8: CoreDNS

The upstream base manifest ships with `__PILLAR__` placeholders, so render it
before applying:

```sh
# download -- pin to the release branch matching K8S_VERSION, not master
curl -sL -o /tmp/coredns.yaml \
  https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.35/cluster/addons/dns/coredns/coredns.yaml.base

sed -i \
  -e 's/__DNS__DOMAIN__/cluster.local/g' \
  -e 's/__DNS__SERVER__/10.96.0.10/g' \
  -e 's/__DNS__MEMORY__LIMIT__/170Mi/g' \
  -e 's/__PILLAR__DNS__DOMAIN__/cluster.local/g' \
  -e 's/__PILLAR__DNS__SERVER__/10.96.0.10/g' \
  -e 's/__PILLAR__DNS__MEMORY__LIMIT__/170Mi/g' \
  -e 's/__PILLAR__CLUSTER__DNS__/10.96.0.10/g' \
  /tmp/coredns.yaml

# REQUIRED on Ubuntu: the manifest ships "forward . /etc/resolv.conf", which
# on Ubuntu is the systemd-resolved stub (127.0.0.53) -- CoreDNS then forwards
# to itself and dies with "plugin/loop: Loop ... detected for zone ."
sed -i 's|forward . /etc/resolv.conf|forward . 8.8.8.8 1.1.1.1|' /tmp/coredns.yaml

grep -n 'forward' /tmp/coredns.yaml
#        forward . 8.8.8.8 1.1.1.1 {

kubectl apply -f /tmp/coredns.yaml
# serviceaccount/coredns created
# clusterrole.rbac.authorization.k8s.io/system:coredns created
# clusterrolebinding.rbac.authorization.k8s.io/system:coredns created
# configmap/coredns created
# deployment.apps/coredns created
# service/kube-dns created

kubectl -n kube-system get pods -l k8s-app=kube-dns
# NAME                       READY   STATUS    RESTARTS   AGE
# coredns-6f8d6ffb66-62kc2   1/1     Running   0          16s

# confirm the forwarder in the RUNNING ConfigMap, not just the local file
kubectl -n kube-system get cm coredns -o jsonpath='{.data.Corefile}' | grep forward
#        forward . 8.8.8.8 1.1.1.1 {
```

The control plane is tainted by default only under `kubeadm`; here it is not,
so CoreDNS schedules fine on a single node.

### If CoreDNS is in `CrashLoopBackOff`

```sh
kubectl -n kube-system logs -l k8s-app=kube-dns
# note: "kubectl logs pods -l ..." is invalid -- pass EITHER a pod name OR -l,
# and -w is not a flag for logs (use -f to follow)
```

| Log line                                              | Cause                                                                                    |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `[FATAL] plugin/loop: Loop ... detected for zone "."` | `forward . /etc/resolv.conf` resolving to the `127.0.0.53` stub -- apply the `sed` above |
| `SERVFAIL` on external names, pod otherwise `Running` | usually **not** CoreDNS -- check pod egress/masquerading in Phase 7 first                |
| `Listen: listen tcp :53: bind: permission denied`     | missing `NET_BIND_SERVICE` capability in the manifest                                    |
| pod `Pending`                                         | CNI not ready -- finish Phase 7 first                                                    |

Do **not** "fix" the loop by deleting the `loop` plugin from the Corefile, a
common suggestion online. The plugin is a guard, not the fault: removing it
turns an immediate crash into an unbounded query amplification loop between
CoreDNS and itself.

An alternative to hardcoding upstream IPs is `forward . /run/systemd/resolve/resolv.conf`
-- the _real_ resolver list rather than the stub, which is what `kubeadm` does.
It requires mounting that path into the pod, so the explicit addresses above
are simpler for a lab. Either way the addresses should match the `nameservers`
set in netplan during Preparation.

---

## Verification

```sh
# ##############################
# confirm
# ##############################
kubectl get nodes -o wide
# NAME           STATUS   ROLES    AGE   VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
# controlplane   Ready    <none>   10m   v1.35.8   192.168.10.180   <none>        Ubuntu 24.04.4 LTS   7.0.0-30-generic   containerd://2.2.1

kubectl get pods -A
# NAMESPACE     NAME                               READY   STATUS    RESTARTS   AGE
# kube-system   cilium-9jstq                       1/1     Running   0          7m13s
# kube-system   cilium-envoy-cmh7d                 1/1     Running   0          7m13s
# kube-system   cilium-operator-66df494884-htr2n   1/1     Running   0          7m13s
# kube-system   coredns-6f8d6ffb66-62kc2           1/1     Running   0          59s

kubectl get --raw='/readyz?verbose'

# ##############################
# DNS check
# ##############################
# run test pod
kubectl run dnsutils --image=registry.k8s.io/e2e-test-images/agnhost:2.39
# pod/dnsutils created

kubectl get pod dnsutils
# NAME       READY   STATUS    RESTARTS   AGE
# dnsutils   1/1     Running   0          10s

# test: service DNS
kubectl exec -it dnsutils -- nslookup kubernetes.default
# Server:         10.96.0.10
# Address:        10.96.0.10#53
#
# Name:   kubernetes.default.svc.cluster.local
# Address: 10.96.0.1

# test: fully qualified
kubectl exec -it dnsutils -- nslookup kubernetes.default.svc.cluster.local
# Server:         10.96.0.10
# Address:        10.96.0.10#53

# Name:   kubernetes.default.svc.cluster.local
# Address: 10.96.0.1

# test: (external) resolution
kubectl exec -it dnsutils -- nslookup kubernetes.io
# Server:         10.96.0.10
# Address:        10.96.0.10#53
#
# Non-authoritative answer:
# Name:   kubernetes.io
# Address: 147.75.40.148

# FAILURE MODE -- if you get this instead:
#   ** server can't find kubernetes.io: SERVFAIL
#   command terminated with exit code 1
# there are TWO possible causes and they live in different phases. Check the
# CoreDNS config FIRST, because it is one command:
#
#   kubectl -n kube-system get cm coredns -o jsonpath='{.data.Corefile}' | grep forward
#
# a) shows "forward . /etc/resolv.conf"  -> Phase 8: CoreDNS is forwarding to
#    Ubuntu's 127.0.0.53 stub. Re-apply the rendered manifest.
# b) shows "forward . 8.8.8.8 1.1.1.1"   -> CoreDNS is FINE. The fault is pod
#    egress, i.e. Phase 7. Prove it by bypassing CoreDNS entirely:
#      kubectl run nettest --image=busybox:1.36 --rm -it --restart=Never -- #        nslookup kubernetes.io 8.8.8.8
#    A timeout there means masquerading is off -- see Phase 7. Note the node
#    itself resolving fine (dig +short @8.8.8.8 kubernetes.io) proves nothing;
#    the node is not masqueraded, pods are.

# confirm config file
kubectl exec -it dnsutils -- cat /etc/resolv.conf
# search default.svc.cluster.local svc.cluster.local cluster.local
# nameserver 10.96.0.10
# options ndots:5

kubectl delete pod dnsutils
# pod "dnsutils" deleted from default namespace

# ##############################
# Confirm Secret encryption at rest
# ##############################
kubectl create secret generic test-secret --from-literal=password=supersecret
# secret/test-secret created

sudo etcdctl get /registry/secrets/default/test-secret \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/ca.pem \
  --cert=/etc/kubernetes/pki/etcd-server.pem \
  --key=/etc/kubernetes/pki/etcd-server-key.pem | hexdump -C | head

# 00000000  2f 72 65 67 69 73 74 72  79 2f 73 65 63 72 65 74  |/registry/secret|
# 00000010  73 2f 64 65 66 61 75 6c  74 2f 74 65 73 74 2d 73  |s/default/test-s|
# 00000020  65 63 72 65 74 0a 6b 38  73 3a 65 6e 63 3a 61 65  |ecret.k8s:enc:ae|
# 00000030  73 63 62 63 3a 76 31 3a  6b 65 79 31 3a 00 49 42  |scbc:v1:key1:.IB|
# 00000040  d6 e4 9f 6e 1e 17 5f 38  e9 d7 ad f5 67 dc d3 f9  |...n.._8....g...|
# 00000050  c4 ab c4 1d fd c4 da 75  5d 9b dd 4c 2d 16 db 11  |.......u]..L-...|
# 00000060  83 92 3d 30 ea ba 19 a6  00 c1 f0 57 8a 30 c3 fb  |..=0.......W.0..|
# 00000070  9e e3 bf c4 79 c2 bb 06  b8 0c a0 8b 03 a6 3e 2d  |....y.........>-|
# 00000080  8a fa b4 7f ad 6c 4f 2c  66 08 a0 bb 1a 50 20 17  |.....lO,f....P .|
# 00000090  9a 82 7d bd a5 ce cf 77  7c 7f 2d 03 3a 9d 8d 2b  |..}....w|.-.:..+|


# ##############################
# Confirm the apiserver -> kubelet path (RBAC + kubelet authz)
# ##############################
# exercises the ClusterRoleBinding created earlier; 403 here means the binding
# is missing or its User name does not match the client cert CN
kubectl run pathtest --image=registry.k8s.io/e2e-test-images/agnhost:2.39
kubectl wait --for=condition=Ready pod/pathtest --timeout=60s

kubectl logs pathtest >/dev/null && echo "logs OK"
# logs OK
kubectl exec pathtest -- echo works
# works
kubectl delete pod pathtest

# ##############################
# Confirm the kubelet read-only port is closed
# ##############################
# readOnlyPort: 0 -- this port serves node and pod metadata with NO auth
curl -s --max-time 5 http://192.168.10.180:10255/pods; echo "exit=$?"
# exit=7   (connection refused -- correct)

# the authenticated port answers, but rejects anonymous callers
curl -sk --max-time 5 https://192.168.10.180:10250/pods | head -c 200
# Unauthorized

# ##############################
# Confirm audit logging is actually being written
# ##############################
sudo test -s /var/log/kubernetes/audit.log && echo "audit log has content"
# audit log has content

# Secrets are logged at RequestResponse level per the policy
sudo grep -c '"resource":"secrets"' /var/log/kubernetes/audit.log
# (non-zero -- the test-secret above produced entries)

# ##############################
# Confirm NodeRestriction admission is loaded
# ##############################
sudo journalctl -u kube-apiserver | grep -i "NodeRestriction" | head -2

# ##############################
# Confirm pod networking end to end (not just DNS)
# ##############################
kubectl create deployment nettest --image=nginx:alpine --replicas=2
kubectl wait --for=condition=Available deployment/nettest --timeout=120s
kubectl expose deployment nettest --port=80

# pod -> service ClusterIP
kubectl run curltest --image=curlimages/curl:8.10.1 --restart=Never -- \
  sh -c 'curl -s -o /dev/null -w "%{http_code}" http://nettest'
sleep 10
kubectl logs curltest
# 200

kubectl delete pod curltest
kubectl delete service nettest
kubectl delete deployment nettest

# ##############################
# Confirm anonymous access is closed:
# ##############################
curl -k https://192.168.10.180:6443/api/v1/nodes
# {
#   "kind": "Status",
#   "apiVersion": "v1",
#   "metadata": {},
#   "status": "Failure",
#   "message": "Unauthorized",
#   "reason": "Unauthorized",
#   "code": 401
# }
```

### Control plane completion checklist

The master node is done only when every row passes. A `Ready` node and running
pods are necessary but not sufficient -- several of the hardening settings fail
silently.

| #   | Check                                    | Pass condition                                       |
| --- | ---------------------------------------- | ---------------------------------------------------- |
| 1   | `kubectl get nodes`                      | `controlplane   Ready`                               |
| 2   | `kubectl get pods -A`                    | all cilium + coredns pods `1/1 Running`              |
| 3   | `kubectl get --raw='/readyz?verbose'`    | `readyz check passed`                                |
| 4   | `kubectl -n kube-system get lease`       | controller-manager and scheduler both held           |
| 5   | `nslookup kubernetes.default` in a pod   | resolves to `10.96.0.1`                              |
| 6   | `nslookup kubernetes.io` in a pod        | resolves -- **SERVFAIL means Phase 8 is unfinished** |
| 7   | pod -> Service ClusterIP over HTTP       | `200`                                                |
| 8   | Secret in etcd                           | starts `k8s:enc:aescbc:v1:key1`, no plaintext        |
| 9   | `curl -k https://<ip>:6443/api/v1/nodes` | `401 Unauthorized`                                   |
| 10  | `curl http://<ip>:10255/pods`            | connection refused                                   |
| 11  | `kubectl logs` / `kubectl exec` on a pod | succeed (not 403)                                    |
| 12  | `/var/log/kubernetes/audit.log`          | non-empty, contains `"resource":"secrets"`           |

Rows 1-4 prove the cluster runs. Rows 5-7 prove networking. Rows 8-12 prove the
CKS-relevant hardening is actually in effect rather than merely configured --
that distinction is the point of this build.

---
