# Jenkins - Installation

[Back](../jenkins.md)

- [Jenkins - Installation](#jenkins---installation)
  - [Installation](#installation)
    - [RedHat](#redhat)
    - [Ubuntu](#ubuntu)
    - [Docker](#docker)
      - [Install Docker on Ubuntu](#install-docker-on-ubuntu)
      - [Install Docker on Ubuntu](#install-docker-on-ubuntu-1)
      - [Docker Compose](#docker-compose)
    - [Docker Run](#docker-run)

---

## Installation

### RedHat

- ref: https://www.jenkins.io/doc/book/installing/linux/#red-hat-centos

```sh
# update repo
sudo wget -O /etc/yum.repos.d/jenkins.repo \
    https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo yum upgrade -y

# Add required dependencies for the jenkins package
sudo yum install -y fontconfig java-21-openjdk
sudo yum install -y jenkins

# start service
sudo systemctl daemon-reload
sudo systemctl enable jenkins --now

# enable port
sudo firewall-cmd --permanent --add-port=8080/tcp
```

- http://ip_address:8080

```sh
# get init password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

---

### Ubuntu

- ref: https://www.jenkins.io/doc/book/installing/linux/#debianubuntu

```sh
# update repo
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update -y

# Add required dependencies for the jenkins package
sudo apt update
sudo apt install -y fontconfig openjdk-21-jre
sudo apt-get install -y jenkins

# start service
sudo systemctl daemon-reload
sudo systemctl enable jenkins --now
```

- http://ip_address:8080

```sh
# get init password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

---

### Docker

#### Install Docker on Ubuntu

```sh
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

---

#### Install Docker on Ubuntu

```sh
# remove previous version
sudo dnf remove -y docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine \
                  podman \
                  runc

# install
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl enable --now docker

# add the current user to docker group
sudo usermod -aG docker "$USER"
# change the current group ID to refresh the current session without reboot
newgrp docker

# pull jenkins image
docker pull jenkins/jenkins
```

---

#### Docker Compose

```sh
cat > docker-compose.yaml<<EOF
services:
  jenkins:
    container_name: jenkins
    restart: unless-stopped
    image: jenkins/jenkins
    # privileged: true
    # user: root
    ports:
      - "8080:8080"
    volumes:
      - ./jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - net
networks:
  net:
EOF

# create dir for persistence
mkdir -pv jenkins_home
chown $USER:$USER -Rv jenkins_home

docker compose up -d

# get init pwd from log
docker logs jenkins
```

---

### Docker Run


```sh
docker network create jenkins

docker run \
  --name jenkins-docker \
  --rm \
  -d \
  --privileged \
  --network jenkins \
  --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume jenkins-docker-certs:/certs/client \
  --volume jenkins-data:/var/jenkins_home \
  --publish 2376:2376 \
  docker:dind \
  --storage-driver overlay2
```