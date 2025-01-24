# RHCSA Container

[Back](../../index.md)

- [RHCSA Container](#rhcsa-container)
  - [Question](#question)
    - [Solution](#solution)
  - [Question](#question-1)
    - [Solution](#solution-1)

---

## Question

```conf
Download containerfile from http://rhcsa-server/download/ContainerFile
Do not make any modification.
Build image with this container file.
```

- Create dockerfile

- `vi ContainerFile`

```dockerfile
# Use the official CentOS image as the base
FROM centos:latest

# Set the hostname to "Docker-Server"
RUN echo "Docker-Server" > /etc/hostname

# Set the default command to keep the container running
CMD ["/bin/bash"]
```

---

### Solution

```sh
# create dir
mkdir /root/mycontainer
cd /root/mycontainer

# get the containerfile
curl -O http://rhcsa-server/download/ContainerFile
#  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                 Dload  Upload   Total   Spent    Left  Speed
# 100    78  100    78    0     0   6000      0 --:--:-- --:--:-- --:--:--  6000

# confirm
cat Containerfile
# FROM centos:latest
# RUN echo "Docker-Server" > /etc/hostname
# CMD ["/bin/bash"]

# create image
podman build -t my-image -f Containerfile
# STEP 1/3: FROM centos:latest
# Resolved "centos" as an alias (/etc/containers/registries.conf.d/000-shortnames.conf)
# Trying to pull quay.io/centos/centos:latest...
# Getting image source signatures
# Copying blob 7a0437f04f83 done   |
# Copying config 300e315adb done   |
# Writing manifest to image destination
# STEP 2/3: RUN echo "Docker-Server" > /etc/hostname
# --> 9362003fb534
# STEP 3/3: CMD ["/bin/bash"]
# COMMIT my-image
# --> 59d8f7f78f3f
# Successfully tagged localhost/my-image:latest
# 59d8f7f78f3f8329f03e3cff47a0eddd6f64e9600ac30c7c847132e8076038a8

# confirm
podman images
# REPOSITORY             TAG         IMAGE ID      CREATED         SIZE
# localhost/my-image     latest      59d8f7f78f3f  24 minutes ago  217 MB
```

- Troubleshooting

```sh
# remove image
podman rmi image_id
```

---

## Question

```conf
Configure a container to start automatically
Create a container named "mycontainer" using the image which build previously.
Configure the selrvice to automatically mount the directory "/opt/file" to container directory "/opt/incoming". And user directory "/opt/processed" to container directory "/opt/outgoing"
Configure it to run as a systemd service that should run from the existing user "xanadu" only
The service should be named "mycontainer" and should automatically start a system reboot
without any manual intervention.
```

- need Create user xanadu and dirs for volume

```sh
useradd xanadu
passwd xanadu

mkdir -p /opt/file
mkdir -p /opt/processed
chown -R xanadu:xanadu /opt/file
chown -R xanadu:xanadu /opt/processed
```

---

### Solution

```sh
# login as xanadu
su - xanadu

# Create dir
mkdir -p /home/xanadu/mycontainer
cd /home/xanadu/mycontainer

# get the docker file
curl -O http://rhcsa-server/download/Containerfile
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100  3971  100  3971    0     0  26298      0 --:--:-- --:--:-- --:--:-- 28775

# build image
podman build -t myimage:v1 -f Containerfile
# STEP 1/2: FROM nginx:latest
# Resolved "nginx" as an alias (/home/xanadu/.cache/containers/short-name-aliases.conf)
# Trying to pull docker.io/library/nginx:latest...
# Getting image source signatures
# Copying blob 9e9aab598f58 done   |
# Copying blob af302e5c37e9 done   |
# Copying blob 38e992d287c5 done   |
# Copying blob 0256c04a8d84 done   |
# Copying blob 207b812743af done   |
# Copying blob 841e383b441e done   |
# Copying blob 4de87b37f4ad done   |
# Copying config 9bea9f2796 done   |
# Writing manifest to image destination
# STEP 2/2: LABEL maintainer="RHCSA"
# COMMIT myimage:v1
# --> 021598a184ff
# Successfully tagged localhost/myimage:v1
# 021598a184ff1b6530692fe8acaaa0572c63bf5ea5da75787021a954581b8bb9


# confirm
podman images
# REPOSITORY               TAG         IMAGE ID      CREATED        SIZE
# localhost/myimage        v1          021598a184ff  5 seconds ago  196 MB
# docker.io/library/nginx  latest      9bea9f2796e2  8 weeks ago    196 MB


# run container
podman run -d --name mycontainer -v /opt/file:/opt/incoming:Z -v /opt/processed:/opt/outgoing:Z localhost/myimage:v1
# confirm
podman ps
# CONTAINER ID  IMAGE                 COMMAND               CREATED         STATUS         PORTS       NAMES
# 021217d638bb  localhost/myimage:v1  nginx -g daemon o...  21 seconds ago  Up 21 seconds  80/tcp      mycontainer


# Enable Systemd User Services at Boot
loginctl enable-linger xanadu
# Verify linger is enabled
loginctl show-user xanadu | grep Linger
# Linger=yes


# Generate a Systemd Unit File
podman generate systemd --name mycontainer --files --new
# confirm
ll
# total 8
# -rw-r--r--. 1 xanadu xanadu  43 Jan 23 19:35 Containerfile
# -rw-r--r--. 1 xanadu xanadu 827 Jan 23 19:44 container-mycontainer.service

# Create user's systemd directory
mkdir -p ~/.config/systemd/user
# Move the service file to the user's systemd directory
mv /home/xanadu/mycontainer/container-mycontainer.service /home/xanadu/.config/systemd/user/mycontainer.service


# Enable and Start the Service
systemctl --user daemon-reload
systemctl --user enable mycontainer.service
# Created symlink /home/xanadu/.config/systemd/user/default.target.wants/mycontainer.service → /home/xanadu/.config/systemd/user/mycontainer.service.
systemctl --user start mycontainer.service
systemctl --user status mycontainer.service
# ● mycontainer.service - Podman container-mycontainer.service
#      Loaded: loaded (/home/xanadu/.config/systemd/user/mycontainer.service; enabled; preset: disa>
#      Active: active (running) since Thu 2025-01-23 20:02:06 EST; 4s ago
#        Docs: man:podman-generate-systemd(1)
#    Main PID: 6467 (conmon)
#       Tasks: 2 (limit: 10748)
#      Memory: 18.3M
#         CPU: 132ms
#      CGroup: /user.slice/user-1003.slice/user@1003.service/app.slice/mycontainer.service
#              ├─6465 /usr/bin/pasta --config-net --dns-forward 169.254.0.1 -t none -u none -T none>
#              └─6467 /usr/bin/conmon --api-version 1 -c b6996bb02f11d223532903db07f15d1f3712eaf8f0

# confirm in podman
podman ps
# CONTAINER ID  IMAGE                 COMMAND               CREATED         STATUS         PORTS       NAMES
# b6996bb02f11  localhost/myimage:v1  nginx -g daemon o...  40 seconds ago  Up 40 seconds  80/tcp      mycontainer
```

- Troubleshooting

```sh
# common error:
podman images
# WARN[0000] The cgroupv2 manager is set to systemd but there is no systemd user session available
# WARN[0000] For using systemd, you may need to log in using a user session
# WARN[0000] Alternatively, you can enable lingering with: `loginctl enable-linger 1003` (possibly as root)
# WARN[0000] Falling back to --cgroup-manager=cgroupfs
# WARN[0000] The cgroupv2 manager is set to systemd but there is no systemd user session available
# WARN[0000] For using systemd, you may need to log in using a user session
# WARN[0000] Alternatively, you can enable lingering with: `loginctl enable-linger 1003` (possibly as root)
# WARN[0000] Falling back to --cgroup-manager=cgroupfs
# REPOSITORY             TAG         IMAGE ID      CREATED      SIZE
# quay.io/centos/centos  latest      300e315adb2f  4 years ago  217 MB

# solution:
loginctl enable-linger $USER

podman images
# REPOSITORY             TAG         IMAGE ID      CREATED      SIZE
# quay.io/centos/centos  latest      300e315adb2f  4 years ago  217 MB
```

- Note: never login as xanadu using `su - xanadu`
  - Otherwise, for the `systemctl --user enable mycontainer.service` part it return no medium error.
  - Solution: login using ssh command
