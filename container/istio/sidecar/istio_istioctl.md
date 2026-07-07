# Istio - Install `Istio` via `istioctl`

[Back](../index.md)

- [Istio - Install `Istio` via `istioctl`](#istio---install-istio-via-istioctl)
  - [Install `Istio` via `istioctl`](#install-istio-via-istioctl)
    - [Uninstall](#uninstall)

---

## Install `Istio` via `istioctl`

```sh
# Apply a default Istio installation and gnerate the demo profile
KUBECONFIG=./kubeconfig istioctl install --set profile=demo -y
#         |\
#         | \
#         |  \
#         |   \
#       /||    \
#      / ||     \
#     /  ||      \
#    /   ||       \
#   /    ||        \
#  /     ||         \
# /______||__________\
# ____________________
#   \__       _____/
#      \_____/

# ✔ Istio core installed ⛵️
# ✔ Istiod installed 🧠
# ✔ Egress gateways installed 🛫
# ✔ Ingress gateways installed 🛬
# ✔ Installation complete

# get version
KUBECONFIG=./kubeconfig istioctl version
# client version: 1.30.2
# control plane version: 1.30.2
# data plane version: 1.30.2 (8 proxies)

# confirm
KUBECONFIG=./kubeconfig kubectl get pods -n istio-system
# NAME                                    READY   STATUS    RESTARTS   AGE
# istio-egressgateway-844b5dc4f7-2d7kc    1/1     Running   0          77s
# istio-ingressgateway-6d6855b4f5-h2wkq   1/1     Running   0          77s
# istiod-55bc777cb4-rctdn                 1/1     Running   0          90s
```

---

### Uninstall

```sh
KUBECONFIG=./kubeconfig istioctl uninstall --set revision=1.30.2 -y
# You are about to remove the following gateways: istio-egressgateway, istio-ingressgateway. To avoid downtime, please quit this command and reinstall the gateway(s) with a revision that is not being removed from the cluster.

#   Removed apps/v1, Kind=Deployment/istio-egressgateway.istio-system.
#   Removed apps/v1, Kind=Deployment/istio-ingressgateway.istio-system.
#   Removed apps/v1, Kind=Deployment/istiod.istio-system.
#   Removed /v1, Kind=Service/istio-egressgateway.istio-system.
#   Removed /v1, Kind=Service/istio-ingressgateway.istio-system.
#   Removed /v1, Kind=Service/istiod.istio-system.
#   Removed /v1, Kind=Service/istiod-revision-tag-default.istio-system.
#   Removed /v1, Kind=ConfigMap/istio.istio-system.
#   Removed /v1, Kind=ConfigMap/istio-sidecar-injector.istio-system.
#   Removed /v1, Kind=ConfigMap/values.istio-system.
#   Removed /v1, Kind=ServiceAccount/istio-egressgateway-service-account.istio-system.
#   Removed /v1, Kind=ServiceAccount/istio-ingressgateway-service-account.istio-system.
#   Removed /v1, Kind=ServiceAccount/istiod.istio-system.
#   Removed rbac.authorization.k8s.io/v1, Kind=RoleBinding/istio-egressgateway-sds.istio-system.
#   Removed rbac.authorization.k8s.io/v1, Kind=RoleBinding/istio-ingressgateway-sds.istio-system.
#   Removed rbac.authorization.k8s.io/v1, Kind=RoleBinding/istiod.istio-system.
#   Removed rbac.authorization.k8s.io/v1, Kind=Role/istio-egressgateway-sds.istio-system.
#   Removed rbac.authorization.k8s.io/v1, Kind=Role/istio-ingressgateway-sds.istio-system.
#   Removed rbac.authorization.k8s.io/v1, Kind=Role/istiod.istio-system.
#   Removed admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration/istio-revision-tag-default..
#   Removed admissionregistration.k8s.io/v1, Kind=MutatingWebhookConfiguration/istio-sidecar-injector..
#   Removed admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration/istio-validator-istio-system..
#   Removed admissionregistration.k8s.io/v1, Kind=ValidatingWebhookConfiguration/istiod-default-validator..
#   Removed rbac.authorization.k8s.io/v1, Kind=ClusterRole/istio-reader-clusterrole-istio-system..
#   Removed rbac.authorization.k8s.io/v1, Kind=ClusterRole/istiod-clusterrole-istio-system..
#   Removed rbac.authorization.k8s.io/v1, Kind=ClusterRole/istiod-gateway-controller-istio-system..
#   Removed rbac.authorization.k8s.io/v1, Kind=ClusterRoleBinding/istio-reader-clusterrole-istio-system..
#   Removed rbac.authorization.k8s.io/v1, Kind=ClusterRoleBinding/istiod-clusterrole-istio-system..
#   Removed rbac.authorization.k8s.io/v1, Kind=ClusterRoleBinding/istiod-gateway-controller-istio-system..
# ✔ Uninstall complete

# confirm
KUBECONFIG=./kubeconfig istioctl version
# Istio is not present in the cluster: no running Istio pods in namespace "istio-system"
# client version: 1.30.2
```

---
