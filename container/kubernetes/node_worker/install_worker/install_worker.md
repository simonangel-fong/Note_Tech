# Kubernetes: Worker Node - Installation

[Back](../../index.md)

- [Kubernetes: Worker Node - Installation](#kubernetes-worker-node---installation)
  - [Node01](#node01)
    - [VM: Node01](#vm-node01)
    - [Install `containerd`](#install-containerd)
    - [Install `kubeadm`](#install-kubeadm)
    - [Join cluster](#join-cluster)
  - [Node02](#node02)
    - [VM: Node02](#vm-node02)
    - [Install `containerd`](#install-containerd-1)
    - [Install `kubeadm`](#install-kubeadm-1)
    - [Join cluster](#join-cluster-1)

---

## Node01

### VM: Node01

```sh
# ##############################
# set hostname
# ##############################
sudo hostnamectl set-hostname node01

# add hosts
sudo tee -a /etc/hosts <<EOF
127.0.0.1         localhost
192.168.10.151    node01
192.168.10.150    controlplane
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
        - 192.168.10.151/24
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
sudo apt install -y vim git curl apt-transport-https ca-certificates net-tools traceroute tcpdump htop

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
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

# Enable SystemdCgroup = true (required for kubeadm)
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

sudo systemctl restart containerd
sudo systemctl enable --now containerd

```

### Install `kubeadm`

```sh
# ##############################
# Install Kubernetes packages
# ##############################
sudo apt-get update
sudo apt-get install -y apt-transport-https curl ca-certificates gpg

sudo mkdir -pv /etc/apt/keyrings

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

sudo systemctl enable --now kubelet
```

---

### Join cluster

```sh
# ##############################
# Load Kubernetes kernel modules
# ##############################
sudo tee /etc/modules-load.d/k8s.conf <<EOF
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# ##############################
# Enable IP forwarding + bridge filter
# ##############################
sudo tee /etc/sysctl.d/k8s.conf <<EOF
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward = 1
EOF

sudo sysctl --system

# confirm
sysctl net.ipv4.ip_forward
# net.ipv4.ip_forward = 1


sudo kubeadm join 192.168.10.150:6443 --token <TOKEN> --discovery-token-ca-cert-hash sha256:<HASH>
# [preflight] Running pre-flight checks
# [preflight] Reading configuration from the "kubeadm-config" ConfigMap in namespace "kube-system"...
# [preflight] Use 'kubeadm init phase upload-config --config your-config-file' to re-upload it.
# [kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
# [kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
# [kubelet-start] Starting the kubelet
# [kubelet-check] Waiting for a healthy kubelet at http://127.0.0.1:10248/healthz. This can take up to 4m0s
# [kubelet-check] The kubelet is healthy after 504.029571ms
# [kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap

# This node has joined the cluster:
# * Certificate signing request was sent to apiserver and a response was received.
# * The Kubelet was informed of the new secure connection details.

# Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

- In controlplane

```sh
kubectl get nodes
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   45m   v1.33.6
# node01         Ready    <none>          53s   v1.33.6
```

---

## Node02

### VM: Node02

```sh
# ##############################
# set hostname
# ##############################
sudo hostnamectl set-hostname node02

# add hosts
sudo tee -a /etc/hosts <<EOF
127.0.0.1         localhost
192.168.10.152    node02
192.168.10.150    controlplane
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
        - 192.168.10.152/24
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
sudo apt install -y vim git curl apt-transport-https ca-certificates net-tools traceroute tcpdump htop

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
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

# Enable SystemdCgroup = true (required for kubeadm)
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

sudo systemctl restart containerd
sudo systemctl enable --now containerd

```

### Install `kubeadm`

```sh
# ##############################
# Install Kubernetes packages
# ##############################
sudo apt-get update
sudo apt-get install -y apt-transport-https curl ca-certificates gpg

sudo mkdir -pv /etc/apt/keyrings

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

sudo systemctl enable --now kubelet
```

---

### Join cluster

```sh
# ##############################
# Load Kubernetes kernel modules
# ##############################
sudo tee /etc/modules-load.d/k8s.conf <<EOF
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# ##############################
# Enable IP forwarding + bridge filter
# ##############################
sudo tee /etc/sysctl.d/k8s.conf <<EOF
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward = 1
EOF

sudo sysctl --system

# confirm
sysctl net.ipv4.ip_forward
# net.ipv4.ip_forward = 1

sudo kubeadm join 192.168.10.150:6443 --token <TOKEN> --discovery-token-ca-cert-hash sha256:<HASH>

```

- In controlplane

```sh
kubectl get nodes
# NAME           STATUS     ROLES           AGE   VERSION
# controlplane   Ready      control-plane   89m   v1.33.6
# node01         NotReady   <none>          44m   v1.33.6
# node02         Ready      <none>          29s   v1.33.6
```

---
