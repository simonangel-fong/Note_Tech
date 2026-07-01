# cert-manage - with `Istio Gateway`

[Back](../index.md)

- [cert-manage - with `Istio Gateway`](#cert-manage---with-istio-gateway)
  - [with `Istio Gateway`](#with-istio-gateway)

---

## with `Istio Gateway`

- ref: https://istio.io/latest/docs/ops/integrations/certmanager/

- configure an `Issuer` resource

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: ca-issuer
  namespace: istio-system
spec:
  ca:
    secretName: ca-key-pair
```

- configure a `Certificate` resource
  - created in the same namespace as the `istio-ingressgateway` deployment.
    - secret created in the istio-system namespace.

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: ingress-cert
  namespace: istio-system
spec:
  secretName: ingress-cert
  commonName: my.example.com
  dnsNames:
    - my.example.com
```

- configure gateway
  - referenced in the `tls` config for a Gateway

```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: gateway
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: ingress-cert # This should match the Certificate secretName
      hosts:
        - my.example.com # This should match a DNS name in the Certificate
```

---
