# Kubernetes - Security Context

[Back](../../index.md)

- [Kubernetes - Security Context](#kubernetes---security-context)
  - [Security Context](#security-context)
    - [security context for a Pod](#security-context-for-a-pod)
    - [Set the security context for a Container](#set-the-security-context-for-a-container)

---

## Security Context

- `Security Context`

  - a **field** of pod definition to **control container security**

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
