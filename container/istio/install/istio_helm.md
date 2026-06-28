# Istio - Install `Istio` via `helm`

[Back](../index.md)

- [Istio - Install `Istio` via `helm`](#istio---install-istio-via-helm)
  - [Install `Istio` via `helm`](#install-istio-via-helm)
  - [Uninstall](#uninstall)

---

## Install `Istio` via `helm`

- ref: https://istio.io/latest/docs/setup/install/helm/

```sh
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update

KUBECONFIG=./kubeconfig istioctl version
# Istio is not present in the cluster: no running Istio pods in namespace "istio-system"
# client version: 1.30.2

# ##############################
# istio base
# ##############################
helm search repo istio/base
# NAME            CHART VERSION   APP VERSION     DESCRIPTION
# istio/base      1.30.2          1.30.2          Helm chart for deploying Istio cluster resource...

# install
KUBECONFIG=./kubeconfig helm install istio-base istio/base --version 1.30.2 -n istio-system --create-namespace
# NAME: istio-base
# LAST DEPLOYED: Sun Jun 28 15:26:21 2026
# NAMESPACE: istio-system
# STATUS: deployed
# REVISION: 1
# DESCRIPTION: Install complete
# TEST SUITE: None
# NOTES:
# Istio base successfully installed!

# To learn more about the release, try:
#   $ helm status istio-base -n istio-system
#   $ helm get all istio-base -n istio-system

# ##############################
# istio istiod
# ##############################
helm search repo istio/istiod
# NAME                    CHART VERSION   APP VERSION     DESCRIPTION
# istio/istiod            1.30.2          1.30.2          Helm chart for istio control plane

KUBECONFIG=./kubeconfig helm install istiod istio/istiod --version 1.30.2 -n istio-system --wait
# NAME: istiod
# LAST DEPLOYED: Sun Jun 28 15:27:25 2026
# NAMESPACE: istio-system
# STATUS: deployed
# REVISION: 1
# DESCRIPTION: Install complete
# TEST SUITE: None
# NOTES:
# "istiod" successfully installed!

# To learn more about the release, try:
#   $ helm status istiod -n istio-system
#   $ helm get all istiod -n istio-system

# Next steps:
#   * Deploy a Gateway: https://istio.io/latest/docs/setup/additional-setup/gateway/
#   * Try out our tasks to get started on common configurations:
#     * https://istio.io/latest/docs/tasks/traffic-management
#     * https://istio.io/latest/docs/tasks/security/
#     * https://istio.io/latest/docs/tasks/policy-enforcement/
#   * Review the list of actively supported releases, CVE publications and our hardening guide:
#     * https://istio.io/latest/docs/releases/supported-releases/
#     * https://istio.io/latest/news/security/
#     * https://istio.io/latest/docs/ops/best-practices/security/

# For further documentation see https://istio.io website

KUBECONFIG=./kubeconfig k get po -n istio-system
# NAME                      READY   STATUS    RESTARTS   AGE
# istiod-6fdc665455-j9csh   1/1     Running   0          49s

# ##############################
# istio gateway
# ##############################
helm search repo istio/gateway
# NAME            CHART VERSION   APP VERSION     DESCRIPTION
# istio/gateway   1.30.2          1.30.2          Helm chart for deploying Istio gateways

KUBECONFIG=./kubeconfig helm install istio-ingress istio/gateway --version 1.30.2 -n istio-ingress --create-namespace
# NAME: istio-ingress
# LAST DEPLOYED: Sun Jun 28 15:28:56 2026
# NAMESPACE: istio-ingress
# STATUS: deployed
# REVISION: 1
# DESCRIPTION: Install complete
# TEST SUITE: None
# NOTES:
# "istio-ingress" successfully installed!

# To learn more about the release, try:
#   $ helm status istio-ingress -n istio-ingress
#   $ helm get all istio-ingress -n istio-ingress

# Next steps:
#   * Deploy an HTTP Gateway: https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/
#   * Deploy an HTTPS Gateway: https://istio.io/latest/docs/tasks/traffic-management/ingress/secure-ingress/

KUBECONFIG=./kubeconfig k get po -n istio-ingress
# NAME                             READY   STATUS    RESTARTS   AGE
# istio-ingress-7f4b95f59f-2m2tl   1/1     Running   0          59s

```

## Uninstall 

```sh
KUBECONFIG=./kubeconfig helm uninstall istio-ingress -n istio-ingress
# release "istio-ingress" uninstalled

KUBECONFIG=./kubeconfig helm uninstall istiod -n istio-system
# release "istiod" uninstalled

KUBECONFIG=./kubeconfig helm uninstall istio-base -n istio-system
# These resources were kept due to the resource policy:
# [CustomResourceDefinition] trafficextensions.extensions.istio.io
# [CustomResourceDefinition] workloadentries.networking.istio.io
# [CustomResourceDefinition] workloadgroups.networking.istio.io
# [CustomResourceDefinition] authorizationpolicies.security.istio.io
# [CustomResourceDefinition] peerauthentications.security.istio.io
# [CustomResourceDefinition] requestauthentications.security.istio.io
# [CustomResourceDefinition] telemetries.telemetry.istio.io
# [CustomResourceDefinition] wasmplugins.extensions.istio.io
# [CustomResourceDefinition] destinationrules.networking.istio.io
# [CustomResourceDefinition] envoyfilters.networking.istio.io
# [CustomResourceDefinition] gateways.networking.istio.io
# [CustomResourceDefinition] proxyconfigs.networking.istio.io
# [CustomResourceDefinition] serviceentries.networking.istio.io
# [CustomResourceDefinition] sidecars.networking.istio.io
# [CustomResourceDefinition] virtualservices.networking.istio.io

# release "istio-base" uninstalled

KUBECONFIG=./kubeconfig kubectl get crds -oname | grep --color=never 'istio.io' | xargs kubectl --kubeconfig=./kubeconfig delete
# customresourcedefinition.apiextensions.k8s.io "authorizationpolicies.security.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "destinationrules.networking.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "envoyfilters.networking.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "gateways.networking.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "peerauthentications.security.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "proxyconfigs.networking.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "requestauthentications.security.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "serviceentries.networking.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "sidecars.networking.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "telemetries.telemetry.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "trafficextensions.extensions.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "virtualservices.networking.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "wasmplugins.extensions.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "workloadentries.networking.istio.io" deleted
# customresourcedefinition.apiextensions.k8s.io "workloadgroups.networking.istio.io" deleted

```


