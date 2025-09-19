# Kubernetes: `minikube` Installation on Ubuntu

[Back](../../index.md)

- [Kubernetes: `minikube` Installation on Ubuntu](#kubernetes-minikube-installation-on-ubuntu)
  - [Overview](#overview)
  - [Create a Ubuntu VM](#create-a-ubuntu-vm)
  - [Install `docker`](#install-docker)
  - [`kubectl` Installation](#kubectl-installation)
  - [`minikube` Installation](#minikube-installation)
  - [Deploy applications](#deploy-applications)

---

## Overview

- `minikube`

  - a tool that enables developers to run a local **single-node Kubernetes cluster** on their personal computer.
  - This allows for **testing** and **development** of Kubernetes applications without needing a full-scale, cloud-based cluster. It supports various operating systems and is designed to be lightweight and portable.

- Goal:

  - Setup single-node Kubernetes cluster on Ubuntu to practice CKA.

- Ref:
  - https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download

---

## Create a Ubuntu VM

- Skip

```sh
# configure network
nmcli c modify ens160 ipv4.addresses 192.168.128.43/24
nmcli c modify ens160 ipv4.gateway 192.168.128.2
nmcli c modify ens160 ipv4.dns 192.168.128.2
nmcli c up ens160

ip a
ip r
```

---

## Install `docker`

```sh
sudo apt-get update && sudo apt-get upgrade -y
sudo reboot


# uninstall all conflicting packages
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
  sudo apt-get remove $pkg;
done

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install the Docker packages
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start Docker Engine.
sudo systemctl enable --now docker
# Verify
sudo docker run hello-world
```

---

## `kubectl` Installation

```sh
# Download the latest release
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# verify
kubectl version --client
```

---

## `minikube` Installation

```sh
# Install minikube

# install the latest minikube stable release on x86-64 Linux using Debian package
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb

# use unprivilege user, due to minikube cannot start as root.
su - ubuntuadmin
sudo usermod -aG docker $USER && newgrp docker
minikube start --driver=docker
# 😄  minikube v1.35.0 on Redhat 8.10
# ✨  Using the docker driver based on user configuration
# 📌  Using Docker driver with root privileges
# 👍  Starting "minikube" primary control-plane node in "minikube" cluster
# 🚜  Pulling base image v0.0.46 ...
# 💾  Downloading Kubernetes v1.32.0 preload ...
#     > preloaded-images-k8s-v18-v1...:  333.57 MiB / 333.57 MiB  100.00% 7.72 Mi
#     > gcr.io/k8s-minikube/kicbase...:  500.31 MiB / 500.31 MiB  100.00% 6.85 Mi
# 🔥  Creating docker container (CPUs=2, Memory=2200MB) ...
# 🐳  Preparing Kubernetes v1.32.0 on Docker 27.4.1 ...
#     ▪ Generating certificates and keys ...
#     ▪ Booting up control plane ...
#     ▪ Configuring RBAC rules ...
# 🔗  Configuring bridge CNI (Container Networking Interface) ...
# 🔎  Verifying Kubernetes components...
#     ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
# 🌟  Enabled addons: storage-provisioner, default-storageclass
# 🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default

# confirm
kubectl version
# Client Version: v1.34.1
# Kustomize Version: v5.7.1
# Server Version: v1.34.0

minikube version
# minikube version: v1.37.0

# Set minikube as service
sudo tee /etc/systemd/system/minikube.service <<EOF
[Unit]
Description=Minikube Kubernetes Cluster
After=docker.service

[Service]
ExecStart=/usr/bin/minikube start --driver=docker
ExecStop=/usr/bin/minikube stop
Restart=on-failure
User=${USER}
Type=oneshot
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

# reload config
sudo systemctl daemon-reload
# enable
sudo systemctl enable --now minikube

kubectl get nodes
# NAME       STATUS   ROLES           AGE     VERSION
# minikube   Ready    control-plane   6m15s   v1.34.0

minikube dashboard
```

## Deploy applications

```sh
# Create a sample deployment and expose it on port 8080
kubectl create deployment hello-minikube --image=kicbase/echo-server:1.0
kubectl expose deployment hello-minikube --type=NodePort --port=8080

# confirm
kubectl get services hello-minikube
# NAME             TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
# hello-minikube   NodePort   10.109.203.179   <none>        8080:31960/TCP   8s

# use minikube launch a web browser
minikube service hello-minikube
# |-----------|----------------|-------------|---------------------------|
# | NAMESPACE |      NAME      | TARGET PORT |            URL            |
# |-----------|----------------|-------------|---------------------------|
# | default   | hello-minikube |        8080 | http://192.168.49.2:31213 |
# |-----------|----------------|-------------|---------------------------|
# 🎉  Opening service default/hello-minikube in default browser...

```

![pic](./pic/deployment.png)

- Cleanup

```sh
kubectl delete service hello-minikube
# service "hello-minikube" deleted
kubectl delete deployment hello-minikube
# deployment.apps "hello-minikube" deleted

# confirm
kubectl get services hello-minikube
# Error from server (NotFound): services "hello-minikube" not found

kubectl get deployment hello-minikube
# Error from server (NotFound): deployments.apps "hello-minikube" not found

kubectl get pods
# No resources found in default namespace.
```
