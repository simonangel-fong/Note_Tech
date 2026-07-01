# cert-manage - Fundamental

[Back](../index.md)

- [cert-manage - Fundamental](#cert-manage---fundamental)
  - [TLS](#tls)
  - [Certificate \& CA](#certificate--ca)

---

## TLS

- `Transport Layer Security (TLS)`
  - a cryptographic protocol designed to **provide secure, private communications** over a computer network, such as the internet.

- Role
  - **Encryption**:
    - **Scrambles transmitted data into unreadable code** so eavesdroppers cannot understand it.
  - **Integrity**:
    - Ensures data cannot be secretly altered or corrupted during transit.
  - **Authentication**:
    - **Verifies the identities** of the communicating parties to confirm you are connecting to the intended server.

- `TLS Handshake`
  - a process undergoes between the client (e.g., your web browser) and the server before data is sent.
  - Hello:
    - The client and server greet each other, agree on the **TLS version** (like TLS 1.3), and **select cryptographic algorithms**.
  - Authentication:
    - The **server proves its identity** to the client using a `digital (SSL/TLS) certificate`.
  - Key Exchange:
    - Both sides securely **exchange cryptographic keys** to encrypt all future communications.

---

## Certificate & CA

- `certificate`
  - a **digital credential** that **verifies the identity of a website or server** and creates an encrypted connection between the server and browser.

---

- `Certificate Authority (CA)`
  - **a trusted, third-party organization** that **issues digital certificates** used in `TLS (Transport Layer Security)`.

- Role:
  - **Identity Verification**:
    - When a website owner needs a TLS certificate, they apply to a CA.
    - The CA verifies that the applicant actually owns the domain or organization.
  - **Digital Signing**:
    - Once verified, the CA **issues a digitally signed certificate** containing the website's public key.
    - By signing it, the CA guarantees that the public key definitively belongs to that specific website.
  - **The Chain of Trust**:
    - Browsers (like Chrome, Safari, or Firefox) have a **pre-installed list** of `trusted "Root" CAs`.
    - When visit a site, browser uses the `Root CA`'s **cryptographic signature** to verify the site's certificate.

---

    | **Issuer** | Defines how certificates are issued within a single namespace. |
    | **ClusterIssuer** | Defines how certificates are issued cluster-wide. |
    | **CertificateRequest** | Internal resource representing a request for a certificate. |
    | **Order** | ACME-specific resource used during certificate issuance. |
    | **Challenge** | ACME-specific resource used to prove domain ownership. |
    | **ACME** | Protocol used by Let’s Encrypt and other CAs to issue certificates. |
    | **CA** | Certificate Authority that signs and issues certificates. |
    | **Let’s Encrypt** | Common public CA used with cert-manager. |
    | **DNS-01 Challenge** | Proves domain ownership by creating a DNS TXT record. |
    | **HTTP-01 Challenge** | Proves domain ownership by serving a token over HTTP. |
    | **Secret** | Kubernetes Secret where the issued TLS certificate and private key are stored. |
    | **Ingress TLS** | Common use case where cert-manager creates TLS certs for Kubernetes Ingress. |
    | **Gateway API TLS** | Newer use case where certificates are used with Gateway API listeners. |
    | **Renewal** | cert-manager automatically renews certificates before they expire. |
    | **Private Key** | Key generated and stored with the certificate, usually in a Secret. |
    | **SelfSigned Issuer** | Issues certificates signed by their own private key. |
    | **CA Issuer** | Issues certificates using a custom internal CA. |
    | **Webhook** | cert-manager component used for validation and mutation of resources. |
    | **Controller** | cert-manager component that watches resources and reconciles certificates. |
    | **cainjector** | cert-manager component that injects CA bundles into Kubernetes resources. |
