## Ingress limitation

- Ingress cannot support for

  - multi-tenancy:
    - ingress paths must be managed by one tenancy
  - Namespace isolation
  - No RBAC
  - No resource isolations
  - ...

- gateway api

  - provide layer 4 and 7 routing

- GatewayClass:
  - infractructure providers
  - e.g., nginx, loadbalancer
- Gateway:
  - Cluster Operators
- HttpRouter / TCPRoute / GRPCRoute
  - application Developers

---

## GatewayClass

- Example

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: example-class
spec:
  controllerName: example.com/gateway-controller
```

---

## Gateway

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: example-class
spec:
  gatewayClassName: example-class
  listeners:
    - name: http
      protocol: HTTP
      port: 80
```

---

## HTTPRouter

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: example-httproute
spec:
  parentRefs:
    - name: example-gateway
  hostnames:
    - "www.example.com"
  rules:
    - matches:
        - path:
          type: PathPrefiex
          value: /login
      backendRefs:
        - name: example-svc
          port: 8080
```

---

## Ingress vs Gateway API

---

## Lab:

https://learn.kodekloud.com/user/courses/udemy-labs-certified-kubernetes-administrator-with-practice-tests/module/739eaf7b-4898-4732-9aa1-290db7d422d1/lesson/eb8a1359-4412-4e5d-9d03-b576db8c0d14
