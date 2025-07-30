# Grafana - Install

[Back](../../index.md)

- [Grafana - Install](#grafana---install)
  - [Install - Ubuntu](#install---ubuntu)
  - [Install - CentOS](#install---centos)
  - [Install - Docker](#install---docker)
    - [Docker Compose](#docker-compose)

---

## Install - Ubuntu

- ref:
  - https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/

```sh
sudo apt-get update

# Install the prerequisite packages:
sudo apt-get install -y apt-transport-https software-properties-common wget

# Import the GPG key:
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null

# To add a repository for stable releases, run the following command:
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list

# Updates the list of available packages
sudo apt-get update

# Installs the latest OSS release:
sudo apt-get install -y grafana

# confirm
sudo systemctl enable --now grafana-server
sudo systemctl status grafana-server
```

- Login
  - http://host_ip:3000
  - default username and pwd: admin

---

## Install - CentOS

- OS:

  - CentOS
  - Fedora
  - RedHat
  - Amazon Linux

- Ref:
  - https://grafana.com/docs/grafana/latest/setup-grafana/installation/redhat-rhel-fedora/

```sh
sudo dnf update

wget -q -O gpg.key https://rpm.grafana.com/gpg.key
sudo rpm --import gpg.key

sudo tee /etc/yum.repos.d/grafana.repo <<EOF
[grafana]
name=grafana
baseurl=https://rpm.grafana.com
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://rpm.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
EOF

sudo dnf install grafana

sudo systemctl enable --now grafana-server
sudo systemctl status grafana-server
```

---

## Install - Docker

### Docker Compose

- ref:

  - https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/

- `compose.grafana.yaml` file.

```yaml
services:
  grafana:
    image: grafana/grafana-enterprise
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
```

```sh
docker compose -f compose.grafana.yaml up -d --build

docker compose -f compose.grafana.yaml down
```
