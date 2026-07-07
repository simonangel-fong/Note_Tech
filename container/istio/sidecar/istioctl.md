# Istio - Install `istioctl`

[Back](../index.md)

- [Istio - Install `istioctl`](#istio---install-istioctl)
  - [Install `istioctl`](#install-istioctl)

---

## Install `istioctl`

- ref:
  - https://istio.io/latest/docs/setup/additional-setup/download-istio-release/

```sh
# Install the istioctl binary
curl -sL https://istio.io/downloadIstioctl | sh -
# Downloading istioctl-1.30.2 from https://github.com/istio/istio/releases/download/1.30.2/istioctl-1.30.2-linux-amd64.tar.gz ...
# istioctl-1.30.2-linux-amd64.tar.gz download complete!

# Add the istioctl to your path with:
#   export PATH=$HOME/.istioctl/bin:$PATH

# Begin the Istio pre-installation check by running:
#          istioctl x precheck

# Need more information? Visit https://istio.io/docs/reference/commands/istioctl/

export PATH=$HOME/.istioctl/bin:$PATH

KUBECONFIG=./kubeconfig istioctl version
# Istio is not present in the cluster: no running Istio pods in namespace "istio-system"
# client version: 1.30.2
```
