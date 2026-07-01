# cert-manager - Installation

[Back](../index.md)

---

## Install

- ref: https://cert-manager.io/docs/installation/

```sh
helm install \
  cert-manager oci://quay.io/jetstack/charts/cert-manager \
  --version v1.20.3 \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true
```
