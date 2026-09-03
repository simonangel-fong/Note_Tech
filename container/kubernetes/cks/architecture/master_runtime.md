# CKS - Master node: Runtime

[Back](../../index.md)

- [CKS - Master node: Runtime](#cks---master-node-runtime)
  - [Install `containerd`](#install-containerd)
  - [Install `crictl`](#install-crictl)

---

## Install `containerd`

- Reference: [containerd getting started](https://github.com/containerd/containerd/blob/main/docs/getting-started.md)

```sh
# ##############################
# Install containerd
# ##############################
sudo apt-get update
sudo apt-get install -y containerd

# confirm versions
containerd --version
# containerd github.com/containerd/containerd/v2 2.2.1
runc --version
# runc version 1.3.4-0ubuntu1~24.04.1
# spec: 1.2.1
# go: go1.24.4
# libseccomp: 2.5.5

# confirm binary paths
command -v containerd runc
# /usr/bin/containerd
# /usr/sbin/runc

# ##############################
# Configure containerd
# ##############################
sudo mkdir -pv /etc/containerd
# mkdir: created directory '/etc/containerd'
containerd config default | sudo tee /etc/containerd/config.toml >/dev/null
# Set systemd cgroup driver: Sets SystemdCgroup = true
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# enable and restart containerd
sudo systemctl enable containerd
sudo systemctl restart containerd

# confirm
sudo systemctl status containerd --no-pager
# ● containerd.service - containerd container runtime
#      Loaded: loaded (/usr/lib/systemd/system/containerd.service; enabled; preset: enabled)
#      Active: active (running) since Thu 2026-09-03 07:32:22 EDT; 9s ago
#        Docs: https://containerd.io
#    Main PID: 3832 (containerd)
#       Tasks: 7
#      Memory: 14.1M (peak: 17.2M)
#         CPU: 58ms
#      CGroup: /system.slice/containerd.service
#              └─3832 /usr/bin/containerd

# Sep 03 07:32:22 controlplane containerd[3832]: time="2026-09-03T07:32:22.407941058-04:00" level=info msg="Start cni network …default"
# Sep 03 07:32:22 controlplane containerd[3832]: time="2026-09-03T07:32:22.407945191-04:00" level=info msg="Start streaming server"
# Sep 03 07:32:22 controlplane containerd[3832]: time="2026-09-03T07:32:22.407956742-04:00" level=info msg="Registered namespa…ith NRI"
# Sep 03 07:32:22 controlplane containerd[3832]: time="2026-09-03T07:32:22.407961077-04:00" level=info msg="runtime interface …g up..."
# Sep 03 07:32:22 controlplane containerd[3832]: time="2026-09-03T07:32:22.407964995-04:00" level=info msg="starting plugins..."
# Sep 03 07:32:22 controlplane containerd[3832]: time="2026-09-03T07:32:22.407971054-04:00" level=info msg="Synchronizing NRI …e state"
# Sep 03 07:32:22 controlplane containerd[3832]: time="2026-09-03T07:32:22.408173560-04:00" level=info msg=serving... address=…ck.ttrpc
# Sep 03 07:32:22 controlplane containerd[3832]: time="2026-09-03T07:32:22.408215868-04:00" level=info msg=serving... address=…erd.sock
# Sep 03 07:32:22 controlplane containerd[3832]: time="2026-09-03T07:32:22.408292077-04:00" level=info msg="containerd success…017426s"
# Sep 03 07:32:22 controlplane systemd[1]: Started containerd.service - containerd container runtime.
# Hint: Some lines were ellipsized, use -l to show in full.
```

---

## Install `crictl`

```sh
export CRICTL_VERSION=v1.35.0

cd /tmp
curl -fLO "https://github.com/kubernetes-sigs/cri-tools/releases/download/${CRICTL_VERSION}/crictl-${CRICTL_VERSION}-linux-amd64.tar.gz"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
#   0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
# 100 18.2M  100 18.2M    0     0  17.7M      0  0:00:01  0:00:01 --:--:-- 28.0M

sudo tar -xzf "crictl-${CRICTL_VERSION}-linux-amd64.tar.gz" -C /usr/local/bin
# crictl

# config file
cat <<'EOF' | sudo tee /etc/crictl.yaml
runtime-endpoint: unix:///run/containerd/containerd.sock
image-endpoint: unix:///run/containerd/containerd.sock
timeout: 10
EOF
# runtime-endpoint: unix:///run/containerd/containerd.sock
# image-endpoint: unix:///run/containerd/containerd.sock
# timeout: 10

# confirm CRI connection
sudo crictl version
# Version:  0.1.0
# RuntimeName:  containerd
# RuntimeVersion:  2.2.1
# RuntimeApiVersion:  v1

sudo crictl ps
# CONTAINER           IMAGE               CREATED             STATE               NAME                ATTEMPT             POD ID              POD                 NAMESPACE
```

---
