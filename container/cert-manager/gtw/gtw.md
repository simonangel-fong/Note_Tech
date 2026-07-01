# cert-manage - with `Gateway`

[Back](../index.md)

- [cert-manage - with `Gateway`](#cert-manage---with-gateway)
  - [with `Gateway`](#with-gateway)
  - [example](#example)

---

## with `Gateway`

- With Annotated `Gateway API`, cert-manager can **automatically create and manage** `TLS certificates` for a Gateway.

```txt
Gateway
  ↓ annotated with cert-manager issuer
cert-manager
  ↓ creates Certificate
Certificate
  ↓ uses Issuer / ClusterIssuer
ACME / CA
  ↓ issues TLS certificate
Secret
  ↓ referenced by Gateway HTTPS listener
Gateway serves HTTPS traffic
```

---

## example

- **enable the Gateway API support**

```sh
helm upgrade --install cert-manager oci://quay.io/jetstack/charts/cert-manager
    --namespace cert-manager \
    --set config.enableGatewayAPI=true

kubectl rollout restart deployment cert-manager -n cert-manager
```

---

```yaml
# ClusterIssuer
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    email: admin@example.com
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
      # tells cert-manager to use ACME HTTP-01 validation
      - http01:
          gatewayHTTPRoute:
            parentRefs:
              - name: public-gateway
                namespace: default
---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: public-gateway
  namespace: default
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod # specify issuer to use
spec:
  gatewayClassName: envoy-gateway
  listeners:
    - name: http
      protocol: HTTP
      port: 80
      hostname: app.example.com

    - name: https
      protocol: HTTPS
      port: 443
      hostname: app.example.com
      tls:
        mode: Terminate # Gateway terminates HTTPS
        certificateRefs:
          - name: app-example-com-tls # Secret stores the certificate
            kind: Secret
```
