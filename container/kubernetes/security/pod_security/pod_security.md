# Kubernetes Security: Pod Security Standards

[Back](../../index.md)

---

## Pod Security Standards

- The `Pod Security Standards` define 3 different `policies` to broadly cover the security spectrum.

| Policy Profile | Description                                                                                                                     |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `Privileged`   | **Unrestricted** policy allows for known **privilege escalations**.                                                             |
| `Baseline`     | **Minimally restrictive** policy prevents privilege escalations but lllows the default (minimally specified) Pod configuration. |
| `Restricted`   | **Heavily restricted** policy, following current Pod hardening best practices.                                                  |

- `baseline` & `restricted`:
  - If any of the listed containers **fails** to meet the requirements, the entire pod will **fail validation**.

---

## Enforce Pod Security Standards with Namespace Labels

- `Namespaces` can be **labeled** to enforce the `Pod Security Standards`.

### `baseline` Pod Security Standard with namespace labels

- `pod-security.kubernetes.io/enforce: baseline`:
  - **Blocks** any pods that **don't satisfy** the `baseline` policy requirements.
- `pod-security.kubernetes.io/enforce-version`:
  - Pins the versions of the baseline and restricted policies to v1.35.
- `pod-security.kubernetes.io/warn: restricted`:
  - Generates a `user-facing warning`
- `pod-security.kubernetes.io/audit: restricted`:
  - adds an `audit annotation` to any created pod that does not meet the restricted policy requirements.

---

### Lab: Labels an existing namespaces

```sh
# create a new ns
kubectl create ns security-ns
# namespace/security-ns created

kubectl get ns security-ns
# NAME          STATUS   AGE
# security-ns   Active   51s

# output update file
kubectl label --dry-run=server --overwrite ns security-ns pod-security.kubernetes.io/enforce=baseline -o yaml
# apiVersion: v1
# kind: Namespace
# metadata:
#   creationTimestamp: "2026-01-10T05:49:57Z"
#   labels:
#     kubernetes.io/metadata.name: security-ns
#     pod-security.kubernetes.io/enforce: baseline
#   name: security-ns
#   resourceVersion: "525056"
#   uid: 8d63147f-98da-4834-a96a-dbf6813d5287
# spec:
#   finalizers:
#   - kubernetes
# status:
#   phase: Active

# output
kubectl label --overwrite ns security-ns pod-security.kubernetes.io/enforce=restricted  pod-security.kubernetes.io/audit=restricted pod-security.kubernetes.io/warn=restricted
# namespace/security-ns labeled

# confirm
kubectl describe ns security-ns
# Name:         security-ns
# Labels:       kubernetes.io/metadata.name=security-ns
#               pod-security.kubernetes.io/audit=restricted
#               pod-security.kubernetes.io/enforce=restricted
#               pod-security.kubernetes.io/warn=restricted
# Annotations:  <none>
# Status:       Active

# No resource quota.

# No LimitRange resource.
```

- Create a pod need privilege escalations

```yaml
# privilege-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: privilege-pod
  namespace: security-ns
spec:
  volumes:
    - name: sec-ctx-vol
      emptyDir: {}
  containers:
    - name: busybox
      image: busybox
      command: ["sh", "-c", "sleep 1h"]
      # privilege escalation
      securityContext:
        allowPrivilegeEscalation: true
      volumeMounts:
        - name: sec-ctx-vol
          mountPath: /data
```

```sh
# creating pod is forbidden.
kubectl apply -f privilege-pod.yaml
# Error from server (Forbidden): error when creating "privilege-pod.yaml": pods "privilege-pod" is forbidden: violates PodSecurity "restricted:latest": allowPrivilegeEscalation != false (container "busybox" must set securityContext.allowPrivilegeEscalation=false), unrestricted capabilities (container "busybox" must set securityContext.capabilities.drop=["ALL"]), runAsNonRoot != true (pod or container "busybox" must set securityContext.runAsNonRoot=true), seccompProfile (pod or container "busybox" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
```
