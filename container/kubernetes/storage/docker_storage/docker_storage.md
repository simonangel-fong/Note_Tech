# Kubernetes - Storage: Docker Storage

[Back](../../index.md)

- [Kubernetes - Storage: Docker Storage](#kubernetes---storage-docker-storage)
  - [Docker Storage](#docker-storage)
    - [Storage Driver](#storage-driver)
  - [Docker Volume](#docker-volume)
    - [Volume Drivers](#volume-drivers)

---

## Docker Storage

- Docker File System:

  - `var/lib/docker`
    - aufs
    - containers
    - image
    - volumes

- `Image Layer` Architecture

  - command: `docker build`
  - Each line of instruction in a Dockerfile creates new layer in the Docker image.
  - Each lay stores the changes from the previous layer.
    - When building an image, Docker tries to reuse the unchanged previous layer and creates only the changed layers.
  - read only
    - Layers are immutable, and get modified only by a new build.

- `Container layer`:
  - Docker creates a new writable layer on top of the `image layers`.
  - a read write layer.
  - stores data created by the container.
    - e.g., log files, temporary files, files modified by user.
  - `Copy on write mechanism`
    - When the file in the `image layer` gets modified, Docker automatically creates a copy of the `image layer` in the `container layer` and enables read / write.
  - live only when the container is running
    - new layer gets destroyed along with container.

---

### Storage Driver

- the component to enable layered architecture, e.g., create layers, move files across layers
- Common Storage Drivers, depends on the OS
  - `AUFS`: default in Ubuntu
  - `ZFS`
  - `BTRFS`
  - `Device Mapper`: fedora/ CentOS
  - `Overlay`
  - `Overlay2`

---

## Docker Volume

- `Volume`

  - used persist the data in `Container Layer`

- command: `docker volume create data_volume`

  - File system
    - create a new dir: `/var/lib/docker/data_volum`

- `Volume Mounting`

  - mounts a volume from the volumes dir.
  - `docker run -v data_volume:/var/lib/mysql mysql`
  - if the volume is not created yet, Docker automatically creates the volume

- `Bind mounting`

  - mount a directory
  - `docker run -v /data/mysql:/var/lib/mysql mysql`

- `--mount`: new style with key value pair

```sh
docker run --mount type=bind,source=/data/mysqll,target/var/lib/mysql mysql
```

---

### Volume Drivers

- `volume drivers plugin`

  - the component to handle Docker volumes
  - default: `local`

- Can be specified in the container

```sh
# save data in the AWS ebs
docker run -it\
    --name mysql    \
    --volume-driver rexray/ebs  \
    --mount src=ebs-vol,target=/var/lib/mysql   \
    mysql
```

---
