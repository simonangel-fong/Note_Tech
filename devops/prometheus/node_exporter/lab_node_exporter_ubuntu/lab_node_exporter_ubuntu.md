# Prometheus - Node Exporter: Ubuntu

[Back](../../index.md)

- [Prometheus - Node Exporter: Ubuntu](#prometheus---node-exporter-ubuntu)
  - [Prometheus Server](#prometheus-server)
  - [Client Node](#client-node)

---

## Prometheus Server

```sh
# install docker

# Uninstall old versions
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

# Add Docker's official GPG key:
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

# Install the Docker packages
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# confirm
docker --version

sudo tee ~/compose.yaml<<EOF
services:
  prometheus:
    container_name: prometheus
    image: prom/prometheus
    restart: unless-stopped
    ports:
      - 9090:9090
    volumes:
      - prom_data:/prometheus

volumes:
  prom_data:
EOF

sudo docker compose up -d
```

---

## Client Node

```sh

```
