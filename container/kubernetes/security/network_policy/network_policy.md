# Kubernetes - Network Policy

[Back](../../index.md)

- [Kubernetes - Network Policy](#kubernetes---network-policy)
  - [Network Policy](#network-policy)
    - [Declarative Manifest](#declarative-manifest)
    - [Imperative Commands](#imperative-commands)
  - [Default policies](#default-policies)
    - [Default deny all ingress traffic](#default-deny-all-ingress-traffic)
    - [Default deny all egress traffic](#default-deny-all-egress-traffic)
    - [Allow all ingress traffic](#allow-all-ingress-traffic)
    - [Allow all egress traffic](#allow-all-egress-traffic)
    - [Default deny all ingress and all egress traffic](#default-deny-all-ingress-and-all-egress-traffic)
  - [Lab: Control DB connection](#lab-control-db-connection)
    - [Create App](#create-app)
    - [Create Default Network Policy](#create-default-network-policy)
    - [Create](#create)

---

## Network Policy

- `Network Policy`

  - an API object to regulate the traffic flow within the cluster, and between Pods and the outside world.
  - traffic flow control at the `IP`, port level for `TCP`, `UDP`, and `SCTP` protocols.

- The `Identifiers` used to **control `Pod` communication** includes:

  - `podSelector`: identify the `pod` that are allowed
  - `namespaceSelector`: identify `Namespaces` that are allowed
  - `ipBlocks`: identify the IP blocks (CIDR ranges)

---

- `Ingress`

  - the **incoming traffic** from the users

- `Egress`

  - the **outgoing traffic** from the app

- **Default** `all allow` rule:

  - Allow traffic from any pod to any other pod or services within the cluster.
    - **all outbound and inbound** connections are **allowed**.
  - enable pods can comuncate with each other.

- **Reply traffic**:

  - `Reply traffic` for those **allowed connections** will also be **implicitly** allowed.

- `Network policies` **do not conflict**; they are **additive**.

  - If any policy or policies apply to a given pod for a given direction, the **connections allowed** in that direction from that pod is the **union** of what the applicable **policies allow**.
  - Thus, **order** of evaluation does **not affect** the policy result.

---

### Declarative Manifest

- `spec.podSelector` field:

  - the pod associate with the policy
  - `{}`: all pods in the current `namespace`

- `spec.policyType`: field:

  - specify the **type of traffic** is associated with the policy
  - `Ingress`/`Egress`
  - can be both

- `spec.ingress` field:
  - Define a list of **allowed ingress rules**.
  - `{}`: Allow **ingress traffic** from **ANY source** on **ANY port**.
  - `spec.ingress.from` field:
    - Define a list of sources
  - `spec.ingress.to` field:
    - Define a list of destination
  - `spec.ingress.port` field:
    - Define allowed ports

---

- **Selectors** in `ingress from` section or `egress to` section
  - `podSelector`: specify the `pod selector`
  - `namespaceSelector`: specify the `namespace selector`
  - `ipBlock`: specify the allowed `IP CIDR ranges`

---

- target a **range of ports**.

```yaml
spec:
  egress:
    - to:
      # the range 32000 and 32768
      ports:
        - protocol: TCP
          port: 32000
          endPort: 32768
```

---

- multiple namespaces by label

```yaml
spec:
  egress:
    - to:
        - namespaceSelector:
            matchExpressions:
              - key: namespace
                operator: In
                values: ["frontend", "backend"] # multiple ns
```

---

- Targeting a Namespace by its name
  - use `kubernetes.io/metadata.name`

---

- **OR** logic:
  - allow the `pod` matches either one of the rules

```yaml
spec:
  ingress:
    - from:
        - ipBlock:
        - namespaceSelector:
        - podSelector:
```

- **AND** logic:
  - allow the `pod` matches all rules

```yaml
spec:
  ingress:
    - from:
        - ipBlock:
          namespaceSelector:
          podSelector:
```

---

- example

```yaml
# limit mysql access
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
    - Ingress
  # ingress rule
  ingress:
    # from/to
    - from:
        - podSelector:
            matchLabels:
              name: api-pod
      # port
      ports:
        - protocal: TCP
          port: 3306
```

---

- Example: protect mysql db

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  # associate with selected pods
  podSelector:
    matchLabels:
      role: db
    # define type of policy
    policyTypes:
      - Ingress
      - Egress
    # rules
    ingress:
      - from:
          # only allow request from api-pod
          - podSelector:
              matchLabel:
                name: api-pod
            # alllow request from a specific ns
            namespaceSelector:
              matchLabel:
                kubernetes.io/metadata.name: prod
          # allow pod with an ip
          - ipBlock:
            cidr: 192.168.5.10/32
        ports:
          - protocal: TCP
            port: 3306
    egress:
    - to:
        # allow request from db to a specific ip pod
        - ipBlock:
            cidr: 192.168.5.10/32
        ports:
        - protocal: TCP
          port: 80
```

> Note: ingress rule has 2 selectors in the above case:
>
> 1. api-pod within the prod ns
> 2. the pod with a given IP

---

### Imperative Commands

| Command                                                                                  | Description                                                                                  |
| ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `kubectl explain networkpolicy`                                                          | Display documentation for the NetworkPolicy API.                                             |
| `kubectl get networkpolicy`/`kubectl get netpol`                                         | List all NetworkPolicies in the current namespace.                                           |
| `kubectl get networkpolicy -A`                                                           | List all NetworkPolicies across all namespaces.                                              |
| `kubectl describe networkpolicy <name>`                                                  | Show details of a specific NetworkPolicy.                                                    |
| `kubectl create networkpolicy <name> --pod-selector=<k=v> --policy-types=Ingress,Egress` | Create a minimal NetworkPolicy allowing **no ingress/egress** except explicitly added rules. |
| `kubectl delete networkpolicy <name>`                                                    | Delete a specific NetworkPolicy.                                                             |
| `kubectl edit networkpolicy <name>`                                                      | Edit an existing NetworkPolicy in-place.                                                     |

---

## Default policies

- By default, if **no policies exist** in a `namespace`, then **all** ingress and egress traffic is **allowed** to and from pods in that namespace.

### Default deny all ingress traffic

- can create a "**default" ingress** isolation policy for a namespace by creating a `NetworkPolicy` that **selects all pods** but **does not allow** any ingress traffic to those pods.

- Default deny ingress policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {} # all pods
  policyTypes:
    - Ingress
```

---

### Default deny all egress traffic

- deny all egress traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
spec:
  podSelector: {} # all pods
  policyTypes:
    - Egress
```

---

### Allow all ingress traffic

- allow all incoming connections to all pods in a namespace

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-ingress
spec:
  podSelector: {} # all pods
  policyTypes:
    - Ingress
  ingress:
    - {} # allow all sources and all ports
```

---

### Allow all egress traffic

- Allow all egress traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-egress
spec:
  podSelector: {} # pod
  policyTypes:
    - Egress
  egress:
    - {} # allow all sources and all ports
```

---

### Default deny all ingress and all egress traffic

- Deny all

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

---

## Lab: Control DB connection

### Create App

- namespace:
  - db: for database
  - backend: for backend
  - default: for test annonymous connection

```sh
# create db ns
kubectl create ns db
# namespace/db created

# create backend ns
kubectl create ns backend
# namespace/backend created

# confirm
kubectl get ns
# NAME                   STATUS   AGE
# backend                Active   3m39s
# db                     Active   3m48s

# create db
kubectl create deploy mongo -n db --image=mongo --port=27017
# deployment.apps/mongo created

kubectl get deploy mongo -n db
# NAME    READY   UP-TO-DATE   AVAILABLE   AGE
# mongo   1/1     1            1           61s

kubectl get pod -n db -L app
# NAME                     READY   STATUS    RESTARTS   AGE   APP
# mongo-689485f9f7-2fhw7   1/1     Running   0          78s   mongo

kubectl expose deploy mongo -n db --port=27017 --target-port=27017
# service/mongo exposed

kubectl get svc -n db -o wide
# NAME    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)     AGE   SELECTOR
# mongo   ClusterIP   10.108.202.161   <none>        27017/TCP   6s    app=mongo

kubectl describe svc mongo -n db
# Name:                     mongo
# Namespace:                db
# Labels:                   app=mongo
# Annotations:              <none>
# Selector:                 app=mongo
# Type:                     ClusterIP
# IP Family Policy:         SingleStack
# IP Families:              IPv4
# IP:                       10.108.202.161
# IPs:                      10.108.202.161
# Port:                     <unset>  27017/TCP
# TargetPort:               27017/TCP
# Endpoints:                10.244.2.70:27017
# Session Affinity:         None
# Internal Traffic Policy:  Cluster
# Events:                   <none>

# test from backend
kubectl run test-backend -n backend --image=mongo --labels=role=backend -it --rm -- mongosh --host mongo.db --port 27017 --eval "db.runCommand({ ping: 1 })"
# { ok: 1 }

# test from default
kubectl run test-default -n default --image=mongo --labels=role=random -it --rm -- mongosh --host mongo.db --port 27017 --eval "db.runCommand({ ping: 1 })"
# { ok: 1 }
```

---

### Create Default Network Policy

```yaml
# db-deny-all-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-deny-all-ingress
  namespace: db
spec:
  podSelector:
    matchLabels:
      app: mongo
  policyTypes:
    - Ingress
```

```sh
kubectl apply -f db-deny-all-ingress.yaml
# networkpolicy.networking.k8s.io/db-deny-all-ingress created

kubectl get networkpolicy -n db
# NAME                  POD-SELECTOR   AGE
# db-deny-all-ingress   app=mongo      3m10s

kubectl describe networkpolicy db-deny-all-ingress -n db
# Name:         db-deny-all-ingress
# Namespace:    db
# Created on:   2026-01-07 16:16:54 -0500 EST
# Labels:       <none>
# Annotations:  <none>
# Spec:
#   PodSelector:     app=mongo
#   Allowing ingress traffic:
#     <none> (Selected pods are isolated for ingress connectivity)
#   Not affecting egress traffic
#   Policy Types: Ingress

# test backend
kubectl run test-backend -n backend --image=mongo -it --rm -- mongosh --host mongo.db --port 27017 --eval "db.runCommand({ ping: 1 })"
# { ok: 1 }
```

---

### Create

```yaml
# allow-backend.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend
  namespace: db
spec:
  podSelector:
    matchLabels:
      app: mongo
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: backend
          podSelector: {}
      ports:
        - protocol: TCP
          port: 27017
```

```sh
kubectl apply -f allow-backend.yaml
# networkpolicy.networking.k8s.io/allow-backend created

# test backend
kubectl run test-backend -n backend --image=mongo -it --rm -- mongosh --host mongo.db --port 27017 --eval "db.runCommand({ ping: 1 })"
# { ok: 1 }

# test default
kubectl run test-default -n default --image=mongo -it --rm -- mongosh --host mongo.db --port 27017 --eval "db.runCommand({ ping: 1 })"
# { ok: 1 }
```


---

- Install calico

```sh
# Install the Tigera Operator and custom resource definitions.
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.3/manifests/tigera-operator.yaml
# sercontent.com/projectcalico/calico/v3.31.3/manifests/tigera-operator.yaml
# namespace/tigera-operator created
# serviceaccount/tigera-operator created
# clusterrole.rbac.authorization.k8s.io/tigera-operator-secrets created
# clusterrole.rbac.authorization.k8s.io/tigera-operator created
# clusterrolebinding.rbac.authorization.k8s.io/tigera-operator created
# rolebinding.rbac.authorization.k8s.io/tigera-operator-secrets created
# deployment.apps/tigera-operator created

# Install Calico by creating the necessary custom resources.
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.3/manifests/custom-resources.yaml
# sercontent.com/projectcalico/calico/v3.31.3/manifests/custom-resources.yaml
# installation.operator.tigera.io/default created
# apiserver.operator.tigera.io/default created
# goldmane.operator.tigera.io/default created
# whisker.operator.tigera.io/default created


# confirm
watch kubectl get tigerastatus



kubectl delete ns db --force --grace-period=0
# Source - https://stackoverflow.com/a
# Posted by teoincontatto
# Retrieved 2026-01-07, License - CC BY-SA 4.0

kubectl get namespace "db" -o json \
  | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" \
  | kubectl replace --raw /api/v1/namespaces/db/finalize -f -

```