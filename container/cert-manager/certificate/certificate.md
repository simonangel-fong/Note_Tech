# cert-manage - `Certificate`

[Back](../index.md)

- [cert-manage - `Certificate`](#cert-manage---certificate)
  - [`Certificate`](#certificate)
  - [`CertificateRequest`](#certificaterequest)

---

## `Certificate`

- `Certificate`
  - a Kubernetes custom resource used to **request and manage** a `TLS certificate`.

- role:
  - generate `CertificateRequest` resource for a **signed certificate** from an `Issuer` or `ClusterIssuer`.
  - generate a private key
  - Automatically renews `certificate` before expiration.

```txt
Certificate
   ↓ references
Issuer / ClusterIssuer
   ↓ issues cert from
CA / ACME provider
   ↓ stores cert in
Secret
   ↓ used by
Ingress / Gateway / App
```

- result:
  - **Saves** the `certificate` and `private key` into a `Kubernetes Secret`.
  - cert-manager will auto-renew the certificate.

- example

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: app-tls
  namespace: default
spec:
  # Secret where the certificate and private key are stored.
  secretName: app-tls-secret

  dnsNames:
    - app.example.com

  duration: 2160h # 90d
  renewBefore: 360h # 15d

  # Which Issuer or ClusterIssuer should issue the certificate.
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
```

---

## `CertificateRequest`

- `CertificateRequest`
  - a Kubernetes custom resource that represents an **actual request to issue a certificate**.

- usually do not create CertificateRequest manually when using normal cert-manager flow.
  - When a `Certificate` is created, cert-manager creates `CertificateRequest`
