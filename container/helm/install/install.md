# Helm - Install

[Back](../index.md)

- [Helm - Install](#helm---install)
  - [Install helm](#install-helm)

---

## Install helm

- Windows

```sh
choco install kubernetes-helm
```

- Ubuntu

```sh
sudo apt-get install curl gpg apt-transport-https --yes
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

---
