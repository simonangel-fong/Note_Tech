# Kubernetes - Security Context

[Back](../../index.md)

- [Kubernetes - Security Context](#kubernetes---security-context)
  - [Security Context](#security-context)
    - [Declarative Manifests](#declarative-manifests)
    - [Set capabilities for a Container](#set-capabilities-for-a-container)
    - [Set the Seccomp Profile](#set-the-seccomp-profile)
  - [Lab: Security Context](#lab-security-context)

---

## Security Context

- `Security Context`
  - a **field** of pod definition to **control container security**

  - used to define privilege and access control settings for a Pod or Container.

- Security settings level:
  - pod level
    - all containers in the same pod share the same setting
  - container level
    - the setting only applys to a container.

---

### Declarative Manifests

- `Pod.spec.securityContext` field
  - specify the pod Security Context
- `Pod.spec.containers.securityContext` field
  - specify the container security context
  - **override** settings made at the Pod level when there is overlap.

- `securityContext.runAsUser`:
  - default: `root(0)`
  - specify user ID to run all processes
- `securityContext.runAsUser`:
  - specify group ID to run all processes
- `securityContext.fsGroup`:
  - specify group of the file system

---

- `securityContext.supplementalGroups`:
  - []
  - all processes of the container are also part of the specified groups.

- `securityContext.supplementalGroupsPolicy`
  - defines the **policy** for calculating the `supplementary groups` for the container processes in a pod.
  - values:
    - `Merge`:
      - default
      - The group membership defined in `/etc/group` for the container's primary user will be **merged**.
    - `Strict`:
      - Only group IDs in `fsGroup`, `supplementalGroups`, or `runAsGroup` fields are attached as the `supplementary groups` of the container processes.
      - **no group membership** from `/etc/group` for the container's primary user will be **merged**.

---

### Set capabilities for a Container

- `securityContext.capabilities`
  - specify Linux capabilities for a Container

- Example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-capabilities
spec:
  containers:
    - name: demo
      image: busybox:1.28
      command: ["sh", "-c", "sleep 1h"]
      securityContext:
        capabilities:
          add: ["NET_ADMIN", "SYS_TIME"]
```

---

### Set the Seccomp Profile

- `securityContext.seccompProfile `
  - specify Linux capabilities for a Container
- `seccompProfile.type`:
  - specify type of profile
  - value: `RuntimeDefault`, `Unconfined`, and `Localhost`
- `seccompProfile.localhostProfile`:
  - indicates the path of the pre-configured profile on the node

- Example:

```yaml
securityContext:
  seccompProfile:
    type: RuntimeDefault
---
securityContext:
  seccompProfile:
    type: Localhost
    localhostProfile: my-profiles/profile-allow.json
```

---

## Lab: Security Context

```yaml
# demo-sc.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-sc
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
    supplementalGroups: [4000]
  volumes:
    - name: sec-ctx-vol
      emptyDir: {}
  containers:
    - name: sec-ctx-demo
      image: ubuntu
      command: ["sh", "-c", "sleep 1h"]
      volumeMounts:
        - name: sec-ctx-vol
          mountPath: /data/demo
      securityContext:
        allowPrivilegeEscalation: false
```

```sh
kubectl apply -f demo-sc.yaml
# pod/demo-sc created

kubectl exec -it demo-sc -- sh
id
# uid=1000 gid=3000 groups=2000,3000,4000
```

---
