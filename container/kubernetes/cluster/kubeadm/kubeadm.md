# Kubernetes - `kubeadm`

[Back](../../index.md)

- [Kubernetes - `kubeadm`](#kubernetes---kubeadm)
  - [`kubeadm`](#kubeadm)
    - [Imperative Command](#imperative-command)
  - [Lab: Installing `kubeadm`, `kubelet` and `kubectl`](#lab-installing-kubeadm-kubelet-and-kubectl)
  - [Lab: Init Controlplane](#lab-init-controlplane)

---

## `kubeadm`

### Imperative Command

| CMD                             | DESC                                                                |
| ------------------------------- | ------------------------------------------------------------------- |
| `kubeadm version`               | Prints the version of kubeadm                                       |
| `kubeadm init`                  | Initializes a control plane node                                    |
| `kubeadm join CLUSTER_IP`       | initializes a new worker node and joins it to the existing cluster. |
| `kubeadm upgrade plan VERSION`  | Check which versions are available to upgrade                       |
| `kubeadm upgrade apply VERSION` | Upgrade Kubernetes cluster to the specified version                 |
| `kubeadm upgrade diff VERSION`  | Show what differences would be applied.                             |
| `kubeadm reset`                 | Performs a best effort revert of changes                            |

- config

| CMD                                     | DESC                                                      |
| --------------------------------------- | --------------------------------------------------------- |
| `kubeadm config print init-defaults`    | Print default init configuration for 'kubeadm init'       |
| `kubeadm config print join-defaults`    | Print default join configuration for 'kubeadm join'       |
| `kubeadm config print reset-defaults`   | Print default reset configuration for 'kubeadm reset'     |
| `kubeadm config print upgrade-defaults` | Print default upgrade configuration for 'kubeadm upgrade' |

- Token

| CMD                      | DESC                                                                     |
| ------------------------ | ------------------------------------------------------------------------ |
| `kubeadm token create`   | Create bootstrap tokens on the server                                    |
| `kubeadm token delete`   | Delete bootstrap tokens on the server                                    |
| `kubeadm token generate` | Generate and print a bootstrap token, but do not create it on the server |
| `kubeadm token list`     | List bootstrap tokens on the server                                      |

---

## Lab: Installing `kubeadm`, `kubelet` and `kubectl`

```sh
# confirm kernel
uname -r
# 6.14.0-37-generic

# confirm os
cat /etc/*-release
# DISTRIB_ID=Ubuntu
# DISTRIB_RELEASE=24.04
# DISTRIB_CODENAME=noble
# DISTRIB_DESCRIPTION="Ubuntu 24.04.3 LTS"
# PRETTY_NAME="Ubuntu 24.04.3 LTS"
# NAME="Ubuntu"
# VERSION_ID="24.04"
# VERSION="24.04.3 LTS (Noble Numbat)"
# VERSION_CODENAME=noble
# ID=ubuntu
# ID_LIKE=debian
# HOME_URL="https://www.ubuntu.com/"
# SUPPORT_URL="https://help.ubuntu.com/"
# BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
# PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
# UBUNTU_CODENAME=noble
# LOGO=ubuntu-logo

# turn off swap
sudo swapoff -a
sudo sed -i '/swap/ s/^/#/' /etc/fstab

# Update the apt package index and install packages
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

# Download the public signing key
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.35/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Add the Kubernetes apt repository
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.35/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Update the apt package index, install kubeadm
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# Enable the kubelet service
sudo systemctl enable --now kubelet
```

---

## Lab: Init Controlplane

```sh
ip a
# 2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
#     link/ether 00:0c:29:81:e1:09 brd ff:ff:ff:ff:ff:ff
#     altname enp2s1
#     inet 192.168.10.150/24 brd 192.168.10.255 scope global ens33
#        valid_lft forever preferred_lft forever

sudo kubeadm init --apiserver-advertise-address=192.168.10.150 --cri-socket=unix:///var/run/containerd/containerd.sock
# Your Kubernetes control-plane has initialized successfully!

# To start using your cluster, you need to run the following as a regular user:

#   mkdir -p $HOME/.kube
#   sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
#   sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Alternatively, if you are the root user, you can run:

#   export KUBECONFIG=/etc/kubernetes/admin.conf

# You should now deploy a pod network to the cluster.
# Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
#   https://kubernetes.io/docs/concepts/cluster-administration/addons/

# Then you can join any number of worker nodes by running the following on each as root:

# kubeadm join 192.168.10.150:6443 --token j3pyeq.x6v6i \
#         --discovery-token-ca-cert-hash sha256:5e9d810d52a10

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# confirm
kubectl get nodes
# NAME           STATUS     ROLES           AGE    VERSION
# controlplane   NotReady   control-plane   108s   v1.35.0

```