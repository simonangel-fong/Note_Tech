# Docker - Storage

[Back](../../index.md)

- [Docker - Storage](#docker---storage)
  - [Storage Drivers](#storage-drivers)
  - [File System](#file-system)
  - [Layer Architecture](#layer-architecture)
  - [Command Commands](#command-commands)

---

## Storage Drivers

Manages the layer architecture.
Common drivers:

- aufs
- zfs
- btrfs
- device mapper
- overlay
- overlay2

Dock choose bases on the OS

---

## File System

- `/var/lib/docker`: data root directory on the host
  - `aufs`： old storage driver
  - `overlay2`： current storage driver; Image layers
  - `containers`： runtime data
    - `<container-id>`/
      - config.v2.json: container config
      - hostconfig.json: runtime settings
      - \*.log: container logs (stdout/stderr); `docker logs`
  - `image`： image metadata
  - `volumes`： persistent data
    - `<volume-name>/_data/`

---

## Layer Architecture

- uses a `Union File System` (like OverlayFS).
- How it works:
  - `Container layer` adds a `read-write layer` on top
  - `Image layers` = `read-only`

- `copy-on-write` machenism
  - Modify a file: `copy-on-write`
  - Original image stays unchanged

---

**Types of mounts**

- `Volume mounts`:
  - mount on docker volume
- `Bind mounts`:
  - host-based storage: `docker run -v /host/path:/container/path nginx`

---

## Command Commands

| Command                         | Description                            |
| ------------------------------- | -------------------------------------- |
| `docker volume ls`              | List volumes                           |
| `docker volume create vol_name` | Create a volume                        |
| `docker volume update`          | Update a volume (cluster volumes only) |
| `docker volume rm vol_name`     | Remove one or more volumes             |
