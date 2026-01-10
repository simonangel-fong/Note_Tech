# CKA - Security

[Back](../index.md)

- [CKA - Security](#cka---security)
  - [Security](#security)
    - [Task: pod security](#task-pod-security)
      - [Solution](#solution)

---

## Security

### Task: pod security

Enforce the Restricted Pod Security Standard on the namespace restricted-ns.
Pods in that namespace cannot:
. have privileged access
· host networking
. have any elevated rights

---

- Setup env

```sh
kubectl create ns restricted-ns
```

---

#### Solution

```sh
# label ns as restricted
kubectl label --overwrite ns restricted-ns pod-security.kubernetes.io/enforce=restricted
# namespace/restricted-ns labeled

# confirm
kubectl describe ns restricted-ns
# Labels:       kubernetes.io/metadata.name=restricted-ns
#               pod-security.kubernetes.io/enforce=restricted
```

- If to set it to a specific version

```sh
kubectl label --overwrite ns restricted-ns pod-security.kubernetes.io/enforce-version=v1.35
# namespace/restricted-ns labeled

kubectl describe ns restricted-ns
# Labels:       kubernetes.io/metadata.name=restricted-ns
#               pod-security.kubernetes.io/enforce-version=v1.35

```
