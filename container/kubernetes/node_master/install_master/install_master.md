# Kubernetes - Fundamental

[Back](../index.md)

- [Kubernetes - Fundamental](#kubernetes---fundamental)
  - [Install](#install)
  - [Create VM](#create-vm)
  - [Setup Controlplane: v](#setup-controlplane-v)
    - [Configure VM](#configure-vm)
    - [Install `containerd`](#install-containerd)
    - [Install `kubeadm`](#install-kubeadm)
    - [Create Cluster with `kubeadm`](#create-cluster-with-kubeadm)
    - [Generate Token for Node to join](#generate-token-for-node-to-join)

---

## Install

Steps

- Create VMs
- Install container runtime on each node
- Install kubeadm on each node
- Initialize master server
- install pod network
- Join all worker nodes to the master node

---

## Create VM

- Virtual Network

  - VMnet2
  - Type: NAT
  - DHCP: enabled
  - Subnet: 192.168.10.0/24
  - Gateway: 192.168.10.2

- Master Node:

  - Hostname: controlplane
  - OS: Ubuntu 24.04 LTS
  - CPU: 4 vCPU
  - Memory: 4 GB
  - Disk: 40GB
  - IP: 192.168.10.150

- Worker Node 1:

  - Hostname: node01
  - OS: Ubuntu 24.04 LTS
  - CPU: 2 vCPU
  - Memory: 2 GB
  - Disk: 40GB
  - IP: 192.168.10.151

- Worker Node 2:
  - Hostname: node02
  - OS: Ubuntu 24.04 LTS
  - CPU: 2 vCPU
  - Memory: 2 GB
  - Disk: 40GB
  - IP: 192.168.10.152

---

## Setup Controlplane: v

### Configure VM

```sh
# ##############################
# set hostname
# ##############################
sudo hostnamectl set-hostname controlplane

# add hosts
sudo tee -a /etc/hosts <<EOF
192.168.10.150   controlplane
127.0.0.1        localhost
EOF


# ##############################
# Netplan Static IP Configuration
# ##############################
sudo tee /etc/netplan/01-netcfg.yaml > /dev/null <<EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    ens33:
      dhcp4: false
      addresses:
        - 192.168.10.150/24
      routes:
        - to: default
          via: 192.168.10.2
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
EOF

sudo chmod 600 /etc/netplan/*
sudo netplan apply

# confirm
ip a
ping -c 3 google.com

# ##############################
# Update Packages + Install Basic Tools
# ##############################
sudo apt update && sudo apt upgrade -y
sudo apt install -y vim git curl ca-certificates net-tools traceroute tcpdump htop

# ##############################
# Disable Swap
# ##############################
sudo swapoff -a
sudo sed -i '/swap/ s/^/#/' /etc/fstab

# confirm
free -h

# ##############################
# Reboot
# ##############################
sudo reboot
```

---

### Install `containerd`

```sh
# ##############################
# Install containerd
# ##############################
sudo apt-get update
sudo apt-get install -y containerd

# ##############################
# Configure containerd
# ##############################
# Generate default config
sudo mkdir -pv /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

# Set systemd cgroup driver: Sets SystemdCgroup = true
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# apply the change
sudo systemctl restart containerd
sudo systemctl enable --now containerd
# sudo systemctl status containerd
```

---

### Install `kubeadm`

```sh
# ##############################
# Install support packages
# ##############################
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

# ##############################
# Configure Kubernetes apt repo
# ##############################
sudo mkdir -pv /etc/apt/keyrings

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

# ##############################
# Install kubelet kubeadm kubectl
# ##############################
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# Enable the kubelet service
sudo systemctl enable --now kubelet

# confirm client version
kubectl version --client
# Client Version: v1.33.6
# Kustomize Version: v5.6.0
```

---

### Create Cluster with `kubeadm`

```sh
# ##############################
# Kernel modules for Kubernetes networking
# ##############################
sudo tee /etc/modules-load.d/k8s.conf <<EOF
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# ##############################
# Enable IP forwarding & bridge settings
# ##############################
sudo tee /etc/sysctl.d/k8s.conf <<EOF
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward = 1
EOF

# apply all sysctl configs
sudo sysctl --system

# confirm
sysctl net.ipv4.ip_forward
# expected: net.ipv4.ip_forward = 1

# ##############################
# Initialize control plane
# ##############################
sudo kubeadm init --apiserver-advertise-address=192.168.10.150 --pod-network-cidr=10.244.0.0/16

# ##############################
# Configure kubectl for current user
# ##############################
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# ##############################
# Deploy pod network (Flannel)
# ##############################
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml

# confirm
kubectl get nodes
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   11m   v1.33.6
```

---


### Generate Token for Node to join

```sh
kubeadm token create --print-join-command
```