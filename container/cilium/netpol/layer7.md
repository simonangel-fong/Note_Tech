# Cilium - Network Policy Layer 7 Policies

[Back](../index.md)

- [Cilium - Network Policy Layer 7 Policies](#cilium---network-policy-layer-7-policies)
  - [Layer 7 Policies](#layer-7-policies)
  - [HTTP policies](#http-policies)

---

## Layer 7 Policies

- layer 7 policies
  - application-aware security rules that extend standard network controls to inspect and filter traffic at the application layer, such as by HTTP paths, methods, or headers.

---

## HTTP policies

- `Path`
  - the **path of a request**.
    - If omitted or empty, all paths are all allowed.

- `Method`
  - the method of a request,
    - e.g. GET, POST, PUT, PATCH, DELETE, …
  - If omitted or empty, all methods are allowed.

- `Host`
  - the host header of a request, e.g. foo.com.
  - If omitted or empty, the value of the host header is ignored.

- `Headers`
  - a list of HTTP headers which must be present in the request.
  - If omitted or empty, requests are allowed regardless of headers present.

---

- sample

```yaml
# Allow GET /publi
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "rule1"
spec:
  description: "Allow HTTP GET /public from env=prod to app=service"
  endpointSelector:
    matchLabels:
      app: service
  ingress:
    - fromEndpoints:
        - matchLabels:
            env: prod
      toPorts:
        - ports:
            - port: "80"
              protocol: TCP
          rules:
            http:
              - method: "GET"
                path: "/public"
```

```yaml
# All GET /path1 and PUT /path2 when header set
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "l7-rule"
spec:
  endpointSelector:
    matchLabels:
      app: myService
  ingress:
    - toPorts:
        - ports:
            - port: "80"
              protocol: TCP
          rules:
            http:
              - method: GET
                path: "/path1$"
              - method: PUT
                path: "/path2$"
                headers:
                  - "X-My-Header: true"
```
