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
  - [Lab: Upgrade Cluster](#lab-upgrade-cluster)

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
  - upgrade **all at onece**
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

| Command                         | Description                  |
| ------------------------------- | ---------------------------- |
| `kubectl version`               | Get the cluster version      |
| `kubeadm version`               | Get the kubeadm version      |
| `apt-get upgrade -y kubeadm`    | Upgrade kubeadm tools        |
| `kubeadm upgrade plan`          | Create an upgrade plan       |
| `kubeadm upgrade apply v1.33.6` | Execute upgrade              |
| `apt-get upgrade -y kubelet`    | Upgrade kubelet on each node |
| `system restart kubelet`        | Restart kubelet              |

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

## Lab: Upgrade Cluster

```sh
sudo apt-cache madison kubeadm
# kubeadm | 1.33.6-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubeadm | 1.33.5-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubeadm | 1.33.4-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubeadm | 1.33.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubeadm | 1.33.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubeadm | 1.33.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubeadm | 1.33.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages

sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm='1.33.6-1.1' && \
sudo apt-mark hold kubeadm

kubeadm version
# kubeadm version: &version.Info{Major:"1", Minor:"33", EmulationMajor:"", EmulationMinor:"", MinCompatibilityMajor:"", MinCompatibilityMinor:"", GitVersion:"v1.33.6", GitCommit:"1e09fec02ac194c1044224e45e60d249e98cd092", GitTreeState:"clean", BuildDate:"2025-11-11T19:13:44Z", GoVersion:"go1.24.9", Compiler:"gc", Platform:"linux/amd64"}

sudo kubeadm upgrade plan
# [preflight] Running pre-flight checks.
# [upgrade/config] Reading configuration from the "kubeadm-config" ConfigMap in namespace "kube-system"...
# [upgrade/config] Use 'kubeadm init phase upload-config --config your-config-file' to re-upload it.
# [upgrade] Running cluster health checks
# [upgrade] Fetching available versions to upgrade to
# [upgrade/versions] Cluster version: 1.33.0
# [upgrade/versions] kubeadm version: v1.33.6
# I1125 00:42:15.269622   25703 version.go:261] remote version is much newer: v1.34.2; falling back to: stable-1.33
# [upgrade/versions] Target version: v1.33.6
# [upgrade/versions] Latest version in the v1.33 series: v1.33.6

# Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
# COMPONENT   NODE           CURRENT   TARGET
# kubelet     controlplane   v1.33.0   v1.33.6
# kubelet     node01         v1.33.0   v1.33.6

# Upgrade to the latest version in the v1.33 series:

# COMPONENT                 NODE           CURRENT    TARGET
# kube-apiserver            controlplane   v1.33.0    v1.33.6
# kube-controller-manager   controlplane   v1.33.0    v1.33.6
# kube-scheduler            controlplane   v1.33.0    v1.33.6
# kube-proxy                               1.33.0     v1.33.6
# CoreDNS                                  v1.10.1    v1.12.0
# etcd                      controlplane   3.5.21-0   3.5.24-0

# You can now apply the upgrade by executing the following command:

#         kubeadm upgrade apply v1.33.6

# _____________________________________________________________________


# The table below shows the current state of component configs as understood by this version of kubeadm.
# Configs that have a "yes" mark in the "MANUAL UPGRADE REQUIRED" column require manual config upgrade or
# resetting to kubeadm defaults before a successful upgrade can be performed. The version to manually
# upgrade to is denoted in the "PREFERRED VERSION" column.

# API GROUP                 CURRENT VERSION   PREFERRED VERSION   MANUAL UPGRADE REQUIRED
# kubeproxy.config.k8s.io   v1alpha1          v1alpha1            no
# kubelet.config.k8s.io     v1beta1           v1beta1             no
# _____________________________________________________________________

kubeadm upgrade apply v1.33.6


sudo apt-mark unhold kubelet kubectl && \
sudo apt-get update && sudo apt-get install -y kubelet='v1.33.5' kubectl='v1.33.5' && \
sudo apt-mark hold kubelet kubectl

sudo systemctl daemon-reload
sudo systemctl restart kubelet

kubectl uncordon controlplane
```
