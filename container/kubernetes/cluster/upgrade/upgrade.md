# Kubernetes Cluster: Update

[Back](../../index.md)

- [Kubernetes Cluster: Update](#kubernetes-cluster-update)
  - [Kubernetes Version](#kubernetes-version)
  - [Cluster Upgrade](#cluster-upgrade)
    - [Upgrade Steps](#upgrade-steps)
    - [Upgrade Worker Nodes Strategy](#upgrade-worker-nodes-strategy)
  - [Upgrade Master Node](#upgrade-master-node)
  - [Upgrade Worker Nodes](#upgrade-worker-nodes)
    - [Imperative Commands](#imperative-commands)
  - [Lab: Upgrade Cluster to another `minor` release - from 1.33 to 1.34](#lab-upgrade-cluster-to-another-minor-release---from-133-to-134)
    - [Changing the package repository](#changing-the-package-repository)
    - [Upgrading `kubeadm`](#upgrading-kubeadm)
    - [Upgrading Cluster](#upgrading-cluster)
    - [Upgrading `kubectl` and `kubelet`](#upgrading-kubectl-and-kubelet)
  - [Lab: Upgrade Worker Node](#lab-upgrade-worker-node)
    - [Changing the package repository](#changing-the-package-repository-1)
    - [Upgrading `kubeadm`](#upgrading-kubeadm-1)
    - [Upgrading Worker Node Configuration](#upgrading-worker-node-configuration)
    - [Upgrading `kubelet` \& `kubectl`](#upgrading-kubelet--kubectl)

---

## Kubernetes Version

- `major`.`minor`.`patch`

  - `patch`: bug fixes
  - `minor`:
    - features, functionalities
    - every few months

- **alpha realse**:

  - e.g.,: v1.10.0-alpha
  - **new features** are **disabled** by default.
  - requires a flag to enable them

- **beta realse**:

  - e.g., v1.10.0-beta
  - new features are enabled by default.

- Components can have different release versions.
  - `etcd cluster` and `core dns` have their own versions
  - No other components should have a higher version than the API server.

---

## Cluster Upgrade

![pic](./pic/version.png)

- K8s supports only up to the recent 3 minor versions.
  - v1.12
  - v1.11
  - v1.10
- **Upgrade timing**:
  - before the new release.
- **Recommended approach**:
  - upgrade one **minor version** at a time.
- Upgrade process depends on how the cluster is set up.

  - cloud providers offers easy upgrade solution.
  - **kubeadm**:
    - `kubectl upgrade plan`
    - `kubectl upgrade apply`
  - manual way

---

### Upgrade Steps

1. upgrade `master node`

- cannot access with kubectl
- cannot deploy/modify/delete the existing application.
- no new pods will be automatically created.

2. upgrade `worker node`

---

### Upgrade Worker Nodes Strategy

- **Strategy A**
  - upgrade **all at once**
  - lead to **downtime**
- **Strategy B**
  - upgrade **one node at a time**
  - **no** downtime
- **Strategy C**

  - **add new node** with upgraded version at a time
  - **no** down time
  - common when using a cloud provider

- After upgrading the cluster, the `kubelets` are needed to upgrad **manually**.
- `kubeadm` should be upgraded **before the cluster upgrade**.

---

## Upgrade Master Node

1. Upgrade `kubeadm`
2. Create and output an `upgrade plan`
3. Execute **upgrade**
4. Upgrade `kubelet` on the `master node`, if applied

| Command                                   | Description                  |
| ----------------------------------------- | ---------------------------- |
| `kubectl version`                         | Get the cluster version      |
| `kubeadm version`                         | Get the kubeadm version      |
| `apt-get install -y kubeadm='1.33.6-1.1'` | Install kubeadm of a version |
| `apt-get install -y kubelet='1.35.x-*'`   | Upgrade kubelet of a version |
| `apt-get install -y kubectl='1.35.x-*'`   | Upgrade kubectl of a version |
| `kubeadm upgrade plan`                    | Create an upgrade plan       |
| `kubeadm upgrade apply v1.33.6`           | Execute upgrade              |
| `system restart kubelet`                  | Restart kubelet              |

---

## Upgrade Worker Nodes

1. **Cordon** the node
2. **Drain** the `pod` from the a `worker node`
3. **Upgrade** `kubeadm` and `kubelet`
4. **Upgrade** the kube **configuration**
5. **Uncordon** the node

---

### Imperative Commands

| Command                                                      | Description                         |
| ------------------------------------------------------------ | ----------------------------------- |
| `kubectl drain node_name`                                    | Drain existing pods and cordon node |
| `apt-get upgrade -y kubeadm`                                 | Upgrade kubelet on each node        |
| `apt-get upgrade -y kubelet`                                 | Upgrade kubelet on each node        |
| `kubectl upgrade node config --kubelet-version version_name` | Upgrade the kube configuration      |
| `system restart kubelet`                                     | Restart kubelet                     |
| `kubectl uncordon node_name`                                 | Uncordon the node                   |

---

## Lab: Upgrade Cluster to another `minor` release - from 1.33 to 1.34

### Changing the package repository

```sh
# check the current Kubernetes package repositories
cat /etc/apt/sources.list.d/kubernetes.list
# deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /

# update minor release from 1.33 to 1.34
sudo nano /etc/apt/sources.list.d/kubernetes.list
# https://pkgs.k8s.io/core:/stable:/v1.34/deb/ /

# confirm
cat /etc/apt/sources.list.d/kubernetes.list
# deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.34/deb/ /

```

---

### Upgrading `kubeadm`

```sh
# update available packages list
sudo apt update

# Find the latest patch release
sudo apt-cache madison kubeadm
# kubeadm | 1.34.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubeadm | 1.34.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubeadm | 1.34.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubeadm | 1.34.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages

# #################################
# Upgrade kubeadm
# #################################
# Unset kubeadm set as held back
sudo apt-mark unhold kubeadm
# Canceled hold on kubeadm.

# update package list
sudo apt-get update

# install a specific version
sudo apt-get install -y kubeadm='1.34.3-1.1'

# Mark kubeadm as held back
sudo apt-mark hold kubeadm
# kubeadm set on hold.

# confirm
kubeadm version
# kubeadm version: &version.Info{Major:"1", Minor:"34", EmulationMajor:"", EmulationMinor:"", MinCompatibilityMajor:"", MinCompatibilityMinor:"", GitVersion:"v1.34.3", GitCommit:"df11db1c0f08fab3c0baee1e5ce6efbf816af7f1", GitTreeState:"clean", BuildDate:"2025-12-09T15:05:15Z", GoVersion:"go1.24.11", Compiler:"gc", Platform:"linux/amd64"}
```

---

### Upgrading Cluster

```sh
# Create cluster upgradeable plan
sudo kubeadm upgrade plan
# [preflight] Running pre-flight checks.
# [upgrade/config] Reading configuration from the "kubeadm-config" ConfigMap in namespace "kube-system"...
# [upgrade/config] Use 'kubeadm init phase upload-config kubeadm --config your-config-file' to re-upload it.
# [upgrade] Running cluster health checks
# [upgrade] Fetching available versions to upgrade to
# [upgrade/versions] Cluster version: 1.33.7
# [upgrade/versions] kubeadm version: v1.34.3
# I0114 17:33:53.488160   55380 version.go:260] remote version is much newer: v1.35.0; falling back to: stable-1.34
# [upgrade/versions] Target version: v1.34.3
# [upgrade/versions] Latest version in the v1.33 series: v1.33.7

# Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
# COMPONENT   NODE           CURRENT   TARGET
# kubelet     controlplane   v1.33.7   v1.34.3
# kubelet     node01         v1.34.3   v1.34.3
# kubelet     node02         v1.34.3   v1.34.3

# Upgrade to the latest stable version:

# COMPONENT                 NODE           CURRENT    TARGET
# kube-apiserver            controlplane   v1.33.7    v1.34.3
# kube-controller-manager   controlplane   v1.33.7    v1.34.3
# kube-scheduler            controlplane   v1.33.7    v1.34.3
# kube-proxy                               1.33.7     v1.34.3
# CoreDNS                                  v1.12.0    v1.12.1
# etcd                      controlplane   3.5.24-0   3.6.5-0

# You can now apply the upgrade by executing the following command:

#         kubeadm upgrade apply v1.34.3

# _____________________________________________________________________


# The table below shows the current state of component configs as understood by this version of kubeadm.
# Configs that have a "yes" mark in the "MANUAL UPGRADE REQUIRED" column require manual config upgrade or
# resetting to kubeadm defaults before a successful upgrade can be performed. The version to manually
# upgrade to is denoted in the "PREFERRED VERSION" column.

# API GROUP                 CURRENT VERSION   PREFERRED VERSION   MANUAL UPGRADE REQUIRED
# kubeproxy.config.k8s.io   v1alpha1          v1alpha1            no
# kubelet.config.k8s.io     v1beta1           v1beta1             no
# _____________________________________________________________________

# update cluster
sudo kubeadm upgrade apply v1.34.3 -
# [upgrade] Reading configuration from the "kubeadm-config" ConfigMap in namespace "kube-system"...
# [upgrade] Use 'kubeadm init phase upload-config kubeadm --config your-config-file' to re-upload it.
# [upgrade/preflight] Running preflight checks
# [upgrade] Running cluster health checks
# [upgrade/preflight] You have chosen to upgrade the cluster version to "v1.34.3"
# [upgrade/versions] Cluster version: v1.33.7
# [upgrade/versions] kubeadm version: v1.34.3
# [upgrade/preflight] Pulling images required for setting up a Kubernetes cluster
# [upgrade/preflight] This might take a minute or two, depending on the speed of your internet connection
# [upgrade/preflight] You can also perform this action beforehand using 'kubeadm config images pull'
# W0114 17:41:10.003772   57221 checks.go:827] detected that the sandbox image "registry.k8s.io/pause:3.8" of the container runtime is inconsistent with that used by kubeadm. It is recommended to use "registry.k8s.io/pause:3.10.1" as the CRI sandbox image.
# [upgrade/control-plane] Upgrading your static Pod-hosted control plane to version "v1.34.3" (timeout: 5m0s)...
# [upgrade/staticpods] Writing new Static Pod manifests to "/etc/kubernetes/tmp/kubeadm-upgraded-manifests3943742347"
# [upgrade/staticpods] Preparing for "etcd" upgrade
# [upgrade/staticpods] Renewing etcd-server certificate
# [upgrade/staticpods] Renewing etcd-peer certificate
# [upgrade/staticpods] Renewing etcd-healthcheck-client certificate
# [upgrade/staticpods] Moving new manifest to "/etc/kubernetes/manifests/etcd.yaml" and backing up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2026-01-14-17-41-36/etcd.yaml"
# [upgrade/staticpods] Waiting for the kubelet to restart the component
# [upgrade/staticpods] This can take up to 5m0s
# [apiclient] Found 1 Pods for label selector component=etcd
# [upgrade/staticpods] Component "etcd" upgraded successfully!
# [upgrade/etcd] Waiting for etcd to become available
# [upgrade/staticpods] Preparing for "kube-apiserver" upgrade
# [upgrade/staticpods] Renewing apiserver certificate
# [upgrade/staticpods] Renewing apiserver-kubelet-client certificate
# [upgrade/staticpods] Renewing front-proxy-client certificate
# [upgrade/staticpods] Renewing apiserver-etcd-client certificate
# [upgrade/staticpods] Moving new manifest to "/etc/kubernetes/manifests/kube-apiserver.yaml" and backing up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2026-01-14-17-41-36/kube-apiserver.yaml"
# [upgrade/staticpods] Waiting for the kubelet to restart the component
# [upgrade/staticpods] This can take up to 5m0s
# [apiclient] Found 1 Pods for label selector component=kube-apiserver
# [upgrade/staticpods] Component "kube-apiserver" upgraded successfully!
# [upgrade/staticpods] Preparing for "kube-controller-manager" upgrade
# [upgrade/staticpods] Renewing controller-manager.conf certificate
# [upgrade/staticpods] Moving new manifest to "/etc/kubernetes/manifests/kube-controller-manager.yaml" and backing up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2026-01-14-17-41-36/kube-controller-manager.yaml"
# [upgrade/staticpods] Waiting for the kubelet to restart the component
# [upgrade/staticpods] This can take up to 5m0s
# [apiclient] Found 1 Pods for label selector component=kube-controller-manager
# [upgrade/staticpods] Component "kube-controller-manager" upgraded successfully!
# [upgrade/staticpods] Preparing for "kube-scheduler" upgrade
# [upgrade/staticpods] Renewing scheduler.conf certificate
# [upgrade/staticpods] Moving new manifest to "/etc/kubernetes/manifests/kube-scheduler.yaml" and backing up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2026-01-14-17-41-36/kube-scheduler.yaml"
# [upgrade/staticpods] Waiting for the kubelet to restart the component
# [upgrade/staticpods] This can take up to 5m0s
# [apiclient] Found 1 Pods for label selector component=kube-scheduler
# [upgrade/staticpods] Component "kube-scheduler" upgraded successfully!
# [upgrade/control-plane] The control plane instance for this node was successfully upgraded!
# [upload-config] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
# [kubelet] Creating a ConfigMap "kubelet-config" in namespace kube-system with the configuration for the kubelets in the cluster
# [upgrade/kubeconfig] The kubeconfig files for this node were successfully upgraded!
# W0114 17:44:54.019109   57221 postupgrade.go:116] Using temporary directory /etc/kubernetes/tmp/kubeadm-kubelet-config64290263 for kubelet config. To override it set the environment variable KUBEADM_UPGRADE_DRYRUN_DIR
# [upgrade] Backing up kubelet config file to /etc/kubernetes/tmp/kubeadm-kubelet-config64290263/config.yaml
# [kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
# [kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/instance-config.yaml"
# [patches] Applied patch of type "application/strategic-merge-patch+json" to target "kubeletconfiguration"
# [kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
# [upgrade/kubelet-config] The kubelet configuration for this node was successfully upgraded!
# [upgrade/bootstrap-token] Configuring bootstrap token and cluster-info RBAC rules
# [bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to get nodes
# [bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
# [bootstrap-token] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
# [bootstrap-token] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
# [addons] Applied essential addon: CoreDNS
# [addons] Applied essential addon: kube-proxy

# [upgrade] SUCCESS! A control plane node of your cluster was upgraded to "v1.34.3".

# [upgrade] Now please proceed with upgrading the rest of the nodes by following the right order.
```

---

### Upgrading `kubectl` and `kubelet`

```sh
# Drain the node, marking it unschedulable and evicting the workloads
kubectl drain controlplane --ignore-daemonsets
# node/controlplane cordoned
# Warning: ignoring DaemonSet-managed Pods: kube-flannel/kube-flannel-ds-jwtcj, kube-system/kube-proxy-v54gx
# node/controlplane drained

# Unset kubelet kubectl set as held back
sudo apt-mark unhold kubelet kubectl
# Canceled hold on kubelet.
# Canceled hold on kubectl.

# update package list
sudo apt-get update

# Find the latest patch release
sudo apt-cache madison kubectl kubelet
#  kubectl | 1.34.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubectl | 1.34.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubectl | 1.34.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubectl | 1.34.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubelet | 1.34.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubelet | 1.34.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubelet | 1.34.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubelet | 1.34.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages

# install a specific version
sudo apt-get install -y kubectl='1.34.3-1.1' kubelet='1.34.3-1.1'

# Mark kubelet kubectl as held back
sudo apt-mark hold kubelet kubectl
# kubelet set on hold.
# kubectl set on hold.

# Restart the kubelet
sudo systemctl daemon-reload
sudo systemctl restart kubelet

# Uncordon the node, marking it schedulable
kubectl uncordon controlplane
# node/controlplane uncordoned

# confirm
kubectl get node
# NAME           STATUS   ROLES           AGE    VERSION
# controlplane   Ready    control-plane   46h    v1.34.3
```

---

## Lab: Upgrade Worker Node

### Changing the package repository

```sh
# check the current Kubernetes package repositories
cat /etc/apt/sources.list.d/kubernetes.list
# deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /

# update minor release from 1.33 to 1.34
sudo nano /etc/apt/sources.list.d/kubernetes.list
# https://pkgs.k8s.io/core:/stable:/v1.34/deb/ /

# confirm
cat /etc/apt/sources.list.d/kubernetes.list
# deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.34/deb/ /

```

---

### Upgrading `kubeadm`

```sh
# update available packages list
sudo apt update

# Find the latest patch release
sudo apt-cache madison kubeadm
# kubeadm | 1.34.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubeadm | 1.34.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubeadm | 1.34.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubeadm | 1.34.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages

# #################################
# Upgrade kubeadm
# #################################
# Unset kubeadm set as held back
sudo apt-mark unhold kubeadm
# Canceled hold on kubeadm.

# update package list
sudo apt-get update

# install a specific version
sudo apt-get install -y kubeadm='1.34.3-1.1'

# Mark kubeadm as held back
sudo apt-mark hold kubeadm
# kubeadm set on hold.

# confirm
kubeadm version
# kubeadm version: &version.Info{Major:"1", Minor:"34", EmulationMajor:"", EmulationMinor:"", MinCompatibilityMajor:"", MinCompatibilityMinor:"", GitVersion:"v1.34.3", GitCommit:"df11db1c0f08fab3c0baee1e5ce6efbf816af7f1", GitTreeState:"clean", BuildDate:"2025-12-09T15:05:15Z", GoVersion:"go1.24.11", Compiler:"gc", Platform:"linux/amd64"}
```

---

### Upgrading Worker Node Configuration

```sh
# upgrades the local kubelet configuration
sudo kubeadm upgrade node
# [upgrade] Reading configuration from the "kubeadm-config" ConfigMap in namespace "kube-system"...
# [upgrade] Use 'kubeadm init phase upload-config kubeadm --config your-config-file' to re-upload it.
# [upgrade/preflight] Running pre-flight checks
# [upgrade/preflight] Skipping prepull. Not a control plane node.
# [upgrade/control-plane] Skipping phase. Not a control plane node.
# [upgrade/kubeconfig] Skipping phase. Not a control plane node.
# W0114 18:19:18.181386   13569 postupgrade.go:116] Using temporary directory /etc/kubernetes/tmp/kubeadm-kubelet-config3985649104 for kubelet config. To override it set the environment variable KUBEADM_UPGRADE_DRYRUN_DIR
# [upgrade] Backing up kubelet config file to /etc/kubernetes/tmp/kubeadm-kubelet-config3985649104/config.yaml
# [kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
# [kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/instance-config.yaml"
# [patches] Applied patch of type "application/strategic-merge-patch+json" to target "kubeletconfiguration"
# [kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
# [upgrade/kubelet-config] The kubelet configuration for this node was successfully upgraded!
# [upgrade/addon] Skipping the addon/coredns phase. Not a control plane node.
# [upgrade/addon] Skipping the addon/kube-proxy phase. Not a control plane node.
```

---

### Upgrading `kubelet` & `kubectl`

- Master node

```sh
# Drain the node
kubectl drain node --ignore-daemonsets
# node/node01 cordoned
# Warning: ignoring DaemonSet-managed Pods: kube-flannel/kube-flannel-ds-c7p97, kube-system/kube-proxy-tdkr8
# evicting pod kube-system/coredns-66bc5c9577-7t6dp
# pod/coredns-66bc5c9577-7t6dp evicted
# node/node01 drained
```

- Worker node

```sh
# Unset kubelet kubectl set as held back
sudo apt-mark unhold kubelet kubectl
# Canceled hold on kubelet.
# Canceled hold on kubectl.

# update package list
sudo apt-get update

# Find the latest patch release
sudo apt-cache madison kubectl kubelet
#  kubectl | 1.34.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubectl | 1.34.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubectl | 1.34.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubectl | 1.34.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubelet | 1.34.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubelet | 1.34.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubelet | 1.34.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubelet | 1.34.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages

# install a specific version
sudo apt-get install -y kubectl='1.34.3-1.1' kubelet='1.34.3-1.1'

# Mark kubelet kubectl as held back
sudo apt-mark hold kubelet kubectl
# kubelet set on hold.
# kubectl set on hold.

# Restart the kubelet
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

- Master node

```sh
# Uncordon the node, marking it schedulable
kubectl uncordon node01
# node/node01 already uncordoned

# confirm
kubectl get node
# NAME           STATUS   ROLES           AGE    VERSION
# controlplane   Ready    control-plane   47h    v1.34.3
# node01         Ready    <none>          157m   v1.34.3

```
