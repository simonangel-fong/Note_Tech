# cert-manage - `Issuer` & `ClusterIssuer`

[Back](../index.md)

- [cert-manage - `Issuer` \& `ClusterIssuer`](#cert-manage---issuer--clusterissuer)
  - [`Issuer` \& `ClusterIssuer`](#issuer--clusterissuer)
    - [Common Issuer Types](#common-issuer-types)

---

## `Issuer` & `ClusterIssuer`

- `Issuer`:
  - A **namespace-scoped** resource.
  - can only issue certificates **within the specific Kubernetes namespace** where it is created.
- `ClusterIssuer`:
  - A **cluster-wide** resource, not tied to a single namespace
  - it can be used to issue certificates across any namespace in your cluster.

- Role
  - Every `Certificate` or `CertificateRequest` resource in Kubernetes **must reference** an `Issuer` or `ClusterIssuer` in its configuration.
  - Without a configured and "Ready" Issuer, cert-manager **cannot generate or renew TLS certificates**.

---

### Common Issuer Types

- `Automated Certificate Management Environment (ACME)`
  - an open, standardized **communications protocol** (RFC 8555) used to **automate** the issuance, validation, and renewal of SSL/TLS certificates.
  - Automatically issues **free, publicly trusted** `TLS certificates` by verifying domain ownership via HTTP or DNS challenges.
  - e.g., `Let's Encrypt`
- `CA`:
  - Uses **internal root or intermediate certificate** and **private key** (stored inside the cluster as a secret) to sign certificates.
- `Vault`:
  - Integrates with HashiCorp Vault's PKI secrets engine to dynamically generate and sign certificates.
- `SelfSigned`:
  - Creates self-signed certificates, which are often used to build a Root CA.

---
