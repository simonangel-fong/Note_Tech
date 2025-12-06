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

```sh
# Install the Gateway API resources
kubectl kustomize "https://github.com/nginx/nginx-gateway-fabric/config/crd/gateway-api/standard?ref=v1.5.1" | kubectl apply -f -

# Deploy the NGINX Gateway Fabric CRDs
kubectl apply -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.6.1/deploy/crds.yaml

# Deploy NGINX Gateway Fabric
kubectl apply -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.6.1/deploy/nodeport/deploy.yaml

# Verify the Deployment
kubectl get pods -n nginx-gateway

# View the nginx-gateway service
kubectl get svc -n nginx-gateway nginx-gateway -o yaml

# Update the nginx-gateway service to expose ports 30080 for HTTP and 30081 for HTTPS
kubectl patch svc nginx-gateway -n nginx-gateway --type='json' -p='[
  {"op": "replace", "path": "/spec/ports/0/nodePort", "value": 30080},
  {"op": "replace", "path": "/spec/ports/1/nodePort", "value": 30081}
]'

# Create a Kubernetes Gateway resource
tee gw.yaml <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: nginx-gateway
  namespace: nginx-gateway
spec:
  gatewayClassName: nginx
  listeners:
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: All 
EOF

kubectl create -f gw.yaml

tee route.yaml<<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: frontend-route
spec:
  parentRefs:
  - name: nginx-gateway
  hostnames:
  - "*"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: frontend-svc
      port: 80
EOF

kubectl apply -f route.yaml
```