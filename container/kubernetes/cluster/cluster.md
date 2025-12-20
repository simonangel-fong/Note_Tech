

```sh
# verify that your cluster is working
kubectl cluster-info
# Kubernetes control plane is running at https://kubernetes.docker.internal:6443
# CoreDNS is running at https://kubernetes.docker.internal:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

# To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

# Listing cluster nodes
kubectl get nodes
# NAME             STATUS   ROLES           AGE   VERSION
# docker-desktop   Ready    control-plane   44d   v1.34.1
```

## Lab: Install Cluster Dashboar

- https://github.com/kubernetes/dashboard

```sh
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
# "kubernetes-dashboard" has been added to your repositories

helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
# Release "kubernetes-dashboard" does not exist. Installing it now.
# level=WARN msg="unable to find exact version; falling back to closest available version" chart=kubernetes-dashboard requested="" selected=7.14.0
# NAME: kubernetes-dashboard
# LAST DEPLOYED: Fri Dec 19 23:19:31 2025
# NAMESPACE: kubernetes-dashboard
# STATUS: deployed
# REVISION: 1
# DESCRIPTION: Install complete
# TEST SUITE: None
# NOTES:
# *************************************************************************************************
# *** PLEASE BE PATIENT: Kubernetes Dashboard may need a few minutes to get up and become ready ***
# *************************************************************************************************

# Congratulations! You have just installed Kubernetes Dashboard in your cluster.

# To access Dashboard run:
#   kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443

# NOTE: In case port-forward command does not work, make sure that kong service name is correct.
#       Check the services in Kubernetes Dashboard namespace using:
#         kubectl -n kubernetes-dashboard get svc

# Dashboard will be available at:
#   https://localhost:8443

kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443



# kubectl -n NAMESPACE create token SERVICE_ACCOUNT
kubectl  create token default 
kubectl -n kube-system create token default 

kubectl -n kube-system get sa


kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-rc5/aio/deploy/recommended.yaml

# create dashboard token
kubectl -n kubernetes-dashboard create token default 
kubectl -n kubernetes-dashboard get token

kubectl proxy
# Starting to serve on 127.0.0.1:8001


kubectl create deployment kiada --image=luksa/kiada:0.1 
# deployment.apps/kiada created 

```