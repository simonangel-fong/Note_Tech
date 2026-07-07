# Istio Ambient - Install `Istio` via `helm`

[Back](../index.md)

- [Istio Ambient - Install `Istio` via `helm`](#istio-ambient---install-istio-via-helm)
  - [Install `Istio` via `helm`](#install-istio-via-helm)
  - [Gateway](#gateway)
  - [Uninstall](#uninstall)

---

## Install `Istio` via `helm`

- `base chart`:
  - contains the **basic CRDs** and **cluster roles** required to set up Istio.
  - installed prior to any other Istio component.

- `istiod chart`
  - installs a revision of Istiod.
  - `Istiod`:
    - the control plane component that **manages and configures the proxies** to **route traffic** within the mesh.

- `cni chart`
  - installs the **Istio CNI node agent**.
  - `CNI node agent`:
    - responsible for **detecting the pods** that belong to the ambient mesh, and **configuring the traffic redirection** between pods and the `ztunnel` node proxy (which will be installed later).

- `ztunnel chart`
  - installs the `ztunnel DaemonSet`, which is the node proxy component of Istio’s ambient mode.

- `Ingress gateway chart`
  - install an ingress gateway

---

```sh
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update istio

# base
helm install istio-base istio/base -n istio-system --create-namespace --wait

# istiod control plane
helm install istiod istio/istiod --namespace istio-system --set profile=ambient --wait

# cni chart
helm install istio-cni istio/cni -n istio-system --set profile=ambient --wait

# ztunnel DaemonSet
helm install ztunnel istio/ztunnel -n istio-system --wait

# confirm
helm ls -n istio-system
# NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
# istio-base      istio-system    1               2026-07-07 14:55:33.59332128 -0400 EDT  deployed        base-1.30.2     1.30.2
# istio-cni       istio-system    1               2026-07-07 15:06:48.638750243 -0400 EDT deployed        cni-1.30.2      1.30.2
# istiod          istio-system    1               2026-07-07 14:58:45.672042706 -0400 EDT deployed        istiod-1.30.2   1.30.2
# ztunnel         istio-system    1               2026-07-07 15:08:08.31590319 -0400 EDT  deployed        ztunnel-1.30.2  1.30.2

kubectl get pods -n istio-system
# NAME                      READY   STATUS    RESTARTS   AGE
# istio-cni-node-bs6cc      1/1     Running   0          113s
# istio-cni-node-mp776      1/1     Running   0          113s
# istiod-856cd6fcbd-cdchd   1/1     Running   0          9m55s
# ztunnel-8n5rt             1/1     Running   0          34s
# ztunnel-z62lp             1/1     Running   0          34s

```

---

## Gateway

```sh
# Install or upgrade the Kubernetes Gateway API CRDs
kubectl get crd gateways.gateway.networking.k8s.io &> /dev/null || \
  kubectl apply --server-side -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.5.1/experimental-install.yaml

# Ingress gateway
helm install istio-ingress istio/gateway -n istio-ingress --create-namespace --wait

# confirm
k get gatewayclass
# NAME             CONTROLLER                    ACCEPTED   AGE
# istio            istio.io/gateway-controller   True       57s
# istio-remote     istio.io/unmanaged-gateway    True       57s
# istio-waypoint   istio.io/mesh-controller      True       57s
```

---

## Uninstall

```sh
# Delete any Istio gateway chart installations:
helm delete istio-ingress -n istio-ingress
# release "istio-ingress" uninstalled
kubectl delete namespace istio-ingress
# namespace "istio-ingress" deleted

# Delete the ztunnel chart:
helm delete ztunnel -n istio-system
# release "ztunnel" uninstalled

# Delete the Istio CNI chart:
helm delete istio-cni -n istio-system
# release "istio-cni" uninstalled

# Delete the istiod control plane chart:
helm delete istiod -n istio-system
# release "istiod" uninstalled

# Delete the Istio base chart:
helm delete istio-base -n istio-system
# release "istio-base" uninstalled

# Delete CRDs installed by Istio
kubectl get crd -oname | grep --color=never 'istio.io' | xargs kubectl delete

# Delete the istio-system namespace
kubectl delete namespace istio-system
```
