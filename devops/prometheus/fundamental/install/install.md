# Prometheus - Installation

[Back](../../index.md)

- [Prometheus - Installation](#prometheus---installation)
  - [Ubuntu](#ubuntu)
  - [Docker](#docker)

---

## Ubuntu

- Download Page: https://prometheus.io/download/
  - Url: https://github.com/prometheus/prometheus/releases/download/v3.5.0/prometheus-3.5.0.linux-amd64.tar.gz

```sh
wget https://github.com/prometheus/prometheus/releases/download/v3.5.0/prometheus-3.5.0.linux-amd64.tar.gz

ls -lh
# total 116M
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin 116M Jul 14 12:43 prometheus-3.5.0.linux-amd64.tar.gz

# create a user and group
sudo groupadd --system prometheus
sudo useradd prometheus -s /sbin/nologin --system -g prometheus

# create dir in var
sudo mkdir -pv /var/lib/prometheus
sudo mkdir -pv /var/lib/prometheus/rules
sudo mkdir -pv /var/lib/prometheus/rules.s
sudo mkdir -pv /var/lib/prometheus/files_sd

# unzip
sudo tar -xvf prometheus-3.5.0.linux-amd64.tar.gz

cd prometheus-3.5.0.linux-amd64/
ls -hl
# total 296M
# -rw-r--r-- 1 1001 118  12K Jul 14 12:36 LICENSE
# -rw-r--r-- 1 1001 118 3.7K Jul 14 12:36 NOTICE
# -rwxr-xr-x 1 1001 118 153M Jul 14 12:17 prometheus
# -rw-r--r-- 1 1001 118 1.1K Jul 14 12:36 prometheus.yml
# -rwxr-xr-x 1 1001 118 144M Jul 14 12:17 promtool

# move binary files
sudo mv prometheus promtool /usr/local/bin/

# confirm
prometheus --version
# prometheus, version 3.5.0 (branch: HEAD, revision: 8be3a9560fbdd18a94dedec4b747c35178177202)
#   build user:       root@4451b64cb451
#   build date:       20250714-16:15:23
#   go version:       go1.24.5
#   platform:         linux/amd64
#   tags:             netgo,builtinassets

# move the cf to etc
sudo mkdir -vp /etc/prometheus/
sudo mv prometheus.yml /etc/prometheus/prometheus.yml

# change dir owner
sudo chown -Rv prometheus:prometheus /etc/prometheus/
# ownership of '/etc/prometheus/prometheus.yml' retained as prometheus:prometheus
sudo chown -Rv prometheus:prometheus /var/lib/prometheus/
# changed ownership of '/var/lib/prometheus/files_sd' from root:root to prometheus:prometheus
# changed ownership of '/var/lib/prometheus/rules' from root:root to prometheus:prometheus
# changed ownership of '/var/lib/prometheus/rules.s' from root:root to prometheus:prometheus

# grant permission
sudo chmod -Rv 775 /etc/prometheus/*
# mode of '/etc/prometheus/prometheus.yml' changed from 0644 (rw-r--r--) to 0775 (rwxrwxr-x)


# configure prometheus as a service
sudo tee /etc/systemd/system/prometheus.service<<EOF
[Unit]
Description=Prometheus
Documentation=https://prometheus.io/docs/introduction/overview/
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=prometheus
Group=prometheus
ExecReload=/bin/kill -HUP $MAINPID
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries \
  --web.listen-address=0.0.0.0:9090 \
  --web.external-url=

SyslogIdentifier=prometheus
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# start service
sudo systemctl daemon-reload
sudo systemctl enable --now prometheus
# Created symlink /etc/systemd/system/multi-user.target.wants/prometheus.service → /etc/systemd/system/prometheus.service.

# confirm
sudo systemctl status prometheus
```

- Confirm
  - Browse ubuntu_ip:9090

---

## Docker

```sh
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
