# Kubernetes - Security Context

[Back](../../index.md)

- [Kubernetes - Security Context](#kubernetes---security-context)
  - [Docker Security](#docker-security)
    - [Process Isolation — How Docker Isolates Containers on a Host](#process-isolation--how-docker-isolates-containers-on-a-host)
    - [Users in Docker](#users-in-docker)
    - [Capabilities of the Container Root User](#capabilities-of-the-container-root-user)
  - [Security Context](#security-context)
    - [security context for a Pod](#security-context-for-a-pod)
    - [Set the security context for a Container](#set-the-security-context-for-a-container)

---

## Docker Security

### Process Isolation — How Docker Isolates Containers on a Host

- **Containers are processes on the host**
  - When you run a `Docker container`, it is executed as one or more regular **Linux processes** on the host system.
  - These processes are managed by Docker but still run directly on the host OS, not inside a VM.
- **Containers share the host kernel**
  - Docker does **not** provide a separate **kernel** for each container.
  - All containers running on a host use the **same** `Linux kernel`, which is why containers are lightweight and fast to start.
- **Isolation is achieved using `Linux namespaces`**
  - Docker relies on `Linux namespaces` (PID, NET, IPC, UTS, MNT, USER) to create isolated views of system resources.
  - Each container receives its own set of namespaces—its own "world"—separate from the host's namespace.
- **Processes run in their container’s namespace**
  - Although container processes run on the host, they **appear isolated** because each container sees:
    - Its own process tree (PID namespace)
    - Its own network stack (NET namespace)
    - Its own filesystem view (MNT namespace)
  - Processes inside a container **can only see other processes within the same PID namespace**.
- **The host can see everything**
  - The `host` can **view and manage all container processes** because the host sits in the `root namespace`.
  - A single process may have different PIDs in the host and the container due to PID `namespace mapping`.

---

### Users in Docker

- Default user is `root` (inside the container)

  - By default, processes inside a `Docker container` run as the container’s `root user`.
  - This container root is not the same as the host root user, because its privileges are restricted by namespaces and capabilities.

- Running a container as a specific user

  - You can override the user when starting a container:
    - `docker run --user 1001 ubuntu sleep 3600`
    - This runs the container process as UID 1001 inside the container.

- Best practice:
  - define a non-root user in the Dockerfile
  - To avoid running as root, create a user and set it as the default:
    - This ensures the container always runs as a non-root user unless overridden.

```dockerfile
FROM ubuntu
RUN useradd -u 1000 appuser
USER appuser
```

---

### Capabilities of the Container Root User

- `Container root` ≠ `host root`

  - Even though the default user inside a container is root, its privileges are restricted by Linux namespaces and dropped capabilities.
  - Container root cannot:
    - Shut down the host
    - Modify host kernel parameters
    - Interfere with other containers
    - Access host files outside bind mounts

- Modifying capabilities

  - Docker allows you to fine-tune what a container can do by adding or removing capabilities:
    - `docker run --cap-add=MAC_ADMIN ubuntu`
    - `docker run --cap-drop=KILL ubuntu`
  - Capabilities provide granular control over privileges (e.g., admin network settings, raw sockets, mounting filesystems).

- Privileged mode
  - To give the container root almost full host-like privileges, use:
    - `docker run --privileged ubuntu`
      - Adds all capabilities
      - Loosens most namespace restrictions
      - Gives access to host devices under /dev
        - This should be avoided in production unless absolutely required.

---

## Security Context

- `Security Context`

  - a field of pod definition to control container security

- Security settings level:
  - pod level
    - all containers in the same pod share the same setting
  - container level
    - the setting only applys to a container.

---

### security context for a Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-context-demo
spec:
  securityContext: # security context for a pod
    runAsUser: 1000 # set the user in a pod
    runAsGroup: 3000
    fsGroup: 2000
    supplementalGroups: [4000]
  volumes:
    - name: sec-ctx-vol
      emptyDir: {}
  containers:
    - name: sec-ctx-demo
      image: busybox:1.28
      command: ["sh", "-c", "sleep 1h"]
      volumeMounts:
        - name: sec-ctx-vol
          mountPath: /data/demo
      securityContext: # security context for a container
        allowPrivilegeEscalation: false
```

---

### Set the security context for a Container

- capability can be modified only at the container level.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-context-demo-2
spec:
  securityContext:
    runAsUser: 1000
  containers:
    - name: sec-ctx-demo-2
      image: gcr.io/google-samples/hello-app:2.0
      securityContext: # security context for a container
        runAsUser: 2000
        allowPrivilegeEscalation: false
        capabilities: # set capability;
          add: ["NET_ADMIN", "SYS_TIME"]
```
