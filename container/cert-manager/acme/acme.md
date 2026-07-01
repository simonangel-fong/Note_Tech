# cert-manage - `ACME Issuer`

[Back](../index.md)

- [cert-manage - `ACME Issuer`](#cert-manage---acme-issuer)
  - [`ACME Issuer`](#acme-issuer)
  - [Solving Challenges](#solving-challenges)
    - [HTTP01](#http01)
    - [DNS01](#dns01)
    - [DNS-01 vs HTTP-01](#dns-01-vs-http-01)

---

## `ACME Issuer`

- `ACME Issuer`
  - represents a single account registered with the `Automated Certificate Management Environment (ACME)` **Certificate Authority server**.
  - When you create a new `ACME Issuer`, cert-manager will **generate a private key** which is used to identify you with the ACME server.

- a website that is backed by an `ACME certificate` will be trusted by default by most client's web browsers.
- ACME certificates are typically **free**.

---

## Solving Challenges

- `challenge validations`
  - the process for the `ACME CA server` to **verify that a client owns the domain, or domains**
- `cert-manager` offers two challenges
  - `HTTP01`
  - `DNS01`

---

### HTTP01

- `HTTP01 challenges`
  - a way to prove that you **control a domain** by serving a special **validation token over HTTP**.
  - HTTP URL: `http://<domain_name>/.well-known/acme-challenge/<token>`

- Requirement:
  - The domain must be publicly reachable
  - Domain must point to your load balancer
  - Let’s Encrypt must access HTTP port 80
  - Challenge path must reach the solver Pod

```
1. You create a Certificate or Ingress with cert-manager annotation

2. cert-manager contacts the ACME server

3. ACME server returns an HTTP-01 challenge

4. cert-manager creates temporary resources:
   - temporary Pod
   - temporary Service
   - temporary Ingress / HTTPRoute

5. The domain must route to your cluster load balancer

6. ACME server calls:
   http://your-domain/.well-known/acme-challenge/<token>

7. The request reaches the temporary cert-manager solver Pod

8. Solver Pod returns the expected token

9. ACME server validates the domain

10. Certificate is issued

11. cert-manager stores the certificate in a Kubernetes Secret
```

---

### DNS01

- `DNS01 challenges`
  - a way to prove that you control a domain by **creating a special DNS TXT record**.
  - DNS TXT record: `_acme-challenge.<domain_name>`

- Use cases:
  - **Wildcard certificate**: Required for `*.example.com`
  - **Private/internal cluster**: App does not need to be publicly reachable
  - **No public Ingress**: Validation happens through DNS, not HTTP
  - **Central DNS automation**: Works well with Route 53, Cloudflare, Azure DNS, etc.

```txt
1. You create a Certificate resource.

2. cert-manager contacts the ACME server, for example Let’s Encrypt.

3. The ACME server returns a DNS-01 challenge.

4. cert-manager creates a DNS TXT record:
   _acme-challenge.app.example.com

5. The ACME server checks public DNS for that TXT record.

6. If the expected value exists, domain ownership is verified.

7. The certificate is issued.

8. cert-manager stores the certificate in a Kubernetes Secret.

9. cert-manager removes the temporary TXT record.
```

---

### DNS-01 vs HTTP-01

| Challenge   | How it proves ownership    | Needs public app endpoint? | Supports wildcard cert? |
| ----------- | -------------------------- | -------------------------- | ----------------------- |
| **HTTP-01** | Serve token over HTTP path | Yes                        | No                      |
| **DNS-01**  | Create DNS TXT record      | No                         | Yes                     |

---

- Example: Creating a Basic ACME Issuer

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    email: user@example.com
    profile: tlsserver  # If the ACME server supports profiles
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    # Secret resource that will be used to store the account's private key.
    privateKeySecretRef:
      name: example-issuer-account-key # 
    # Add a single challenge solver, HTTP01 using nginx
    solvers:
      - http01:
          ingress:
            ingressClassName: nginx
```
