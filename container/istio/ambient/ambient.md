# Istio - Ambient Mode

[Back](../index.md)

- [Istio - Ambient Mode](#istio---ambient-mode)
  - [Ambient Mode](#ambient-mode)
    - [How it works](#how-it-works)
    - [Key component](#key-component)
    - [vs sidecar](#vs-sidecar)
  - [HBONE](#hbone)

---

## Ambient Mode

- `Ambient Mode`
  - Istio service mesh **without sidecars**, using `ztunnel` for basic **mesh security** and `waypoint proxies` when you need **HTTP-level control**.
  - **without injecting** an `Envoy sidecar` into every application pod.

---

### How it works

```
Layer 7 features, optional
--------------------------
waypoint proxy
HTTP routing, retries, header rules, L7 authz, canary, traffic splitting

Layer 4 secure mesh, default
----------------------------
ztunnel
mTLS, TCP routing, identity, basic policy, telemetry
```

---

### Key component

- `ztunnel` = basic secure mesh, a per-node `Layer 4 (L4)` proxy
- `waypoint` = advanced HTTP service mesh features, optionally a per-namespace `Layer 7 (L7)` proxy.

---

- `ztunnel` / `zero-trust tunnel`
  - a **node-level proxy** runs as a `DaemonSet`
    - one `ztunnel pod` **per Kubernetes node**.
  - secure service-to-service traffic without putting a proxy inside every pod.
  - handles Layer 4 traffic:
    - mTLS
    - service identity
    - basic authorization
    - TCP traffic forwarding
    - basic telemetry

```
Node 1
├── frontend-a pod
├── frontend-b pod
└── ztunnel pod

Node 2
├── backend-a pod pod
└── ztunnel pod

frontend-a pod -> ztunnel -> ztunnel -> backend-a pod
```

---

- `waypoint proxy`
  - Envoy-based component that handles `Layer 7 (L7)` traffic processing
  - run **outside** application pods per `namespace` or `service account`
    - only pay for advanced L7 processing where needed.
  - optional
  - roles
    - /path-based routing
    - header-based routing
    - HTTP retries
    - traffic splitting
    - canary routing
    - L7 authorization policy
    - request-level telemetry

```
frontend pod
   |
ztunnel
   |
waypoint proxy
   |
ztunnel
   |
backend pod
```

---

### vs sidecar

- `ambient` solves `sidecar` drawback
  - Every pod gets an extra container
  - More CPU and memory usage
  - Sidecar injection can break workloads
  - App restart may be needed to add/remove sidecar
  - Operational overhead increases with pod count

---

## HBONE

- `HBONE (HTTP-Based Overlay Network Environment)`
  - a **secure tunneling protocol** used in the Istio service mesh. 
  - transparently **encrypts** and **multiplexes** application traffic between network services, acting as an encrypted overlay tunnel so microservices can communicate safely and efficiently.