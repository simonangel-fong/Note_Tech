# Kubenetes: `kubectl apply`

[Back](../../index.md)

- [Kubenetes: `kubectl apply`](#kubenetes-kubectl-apply)
  - [kubectl apply](#kubectl-apply)
    - [3-way merge patch](#3-way-merge-patch)

---

## kubectl apply

- `kubectl apply`
  - the local yaml file will also convert to a json file in the `last applied configuration`
  - the local yaml file will convert to a yaml file in the `live object configuration` in the control plane

- e.g., the image of a pod get changed in the local yaml
  - then API server compares and update `last applied configuration` and update it
  - API server compares with `live object configuration` and update the image

- `live object configuration`
  - reside in the k8s memory
  - the actual object status
- `last applied configuration`
  - reside in the `live object configuration` as annotation
  - helps compare with the local yaml file to identify the changes
  - only apply to `kubectl apply` command
    - not to `kubectl create/replace` (not store last applied config)

---

### 3-way merge patch
