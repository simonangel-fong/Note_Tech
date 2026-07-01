# cert-manage - SelfSigned issuers

[Back](../index.md)

- [cert-manage - SelfSigned issuers](#cert-manage---selfsigned-issuers)
  - [SelfSigned issuers](#selfsigned-issuers)
  - [Manifest](#manifest)

---

## SelfSigned issuers

- `SelfSigned issuers`
  - generally useful for bootstrapping a `PKI` locally, which is a complex topic for advanced users.
- If you're not planning to run your own PKI, use a different issuer type.

- The `SelfSigned issuer` denotes that certificates will "sign themselves" using a given `private key`.
  - the `private key` of the `certificate` will be used to **sign** the certificate itself.

- Use case:
  - bootstrapping a `root certificate` for a custom PKI (Public Key Infrastructure),
  - creating **simple ad-hoc certificates** for a quick test.

---

## Manifest

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: selfsigned-issuer
  namespace: sandbox
spec:
  selfSigned: {}
```

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-cluster-issuer
spec:
  selfSigned: {}
```

---

- example
  - create a `SelfSigned issuer`
  - issue a `root certificate`
  - use that `root` as a `CA issuer`:

```yaml
# SelfSigned issuer
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
---
# root certificate
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: my-selfsigned-ca
  # Create CA root secret in `cert-manager` namespace instead of `sandbox` namespace.
  namespace: cert-manager
spec:
  isCA: true
  commonName: my-selfsigned-ca
  secretName: root-secret
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer
    group: cert-manager.io
---
CA issuer
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: my-ca-issuer
spec:
  ca:
    # `ClusterIssuer` resource is not namespaced, so `secretName` is assumed to reference secret in `cert-manager` namespace.
    secretName: root-secret
```
