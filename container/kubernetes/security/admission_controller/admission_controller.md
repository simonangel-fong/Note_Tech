# Kubernetes Security: Admission Controllers

[Back](../../index.md)

- [Kubernetes Security: Admission Controllers](#kubernetes-security-admission-controllers)
  - [Adminssion Controller](#adminssion-controller)
    - [Imperative Commands](#imperative-commands)
  - [Validating \& Mutating Admission Controller](#validating--mutating-admission-controller)
  - [Mutating/Validating Admission Webhook](#mutatingvalidating-admission-webhook)

---

## Adminssion Controller

- user issue command to create pod via k8s api

  - authentication via cert
  - authorization via rbac
  - admission controllers
  - create pod on worker node

- `admission controller`

  - used to intercept requests to the Kubernetes API server after `authentication` and `authorization`, but before the request is persisted in etcd, the cluster's data store.
  - act as "gatekeepers" to enforce policies and ensure the integrity and security of the cluster.

- Purpose:

  - validate a configuration
  - perform additional operations before the pod gets created
  - implement security measures

- Common admission controllers:
  - AlwaysPullImages
  - DefaultStorageClass
  - EventRateLimit
  - NamespaceExists

---

- example: command to create a pod in blue ns
  - `kubectl run nginx --image nginx --namespace blue`
  - the `NamespaceExists` controller
    - comes in after the user is authenticated and authorized
    - checks the ns if exists before the pod creation.

---

- Admission Controller plugin management

```conf
# kube-apiserver.service
ExecStart=/usr/local/bin/kube-apiserver \\
  --enable-admission-plugins=NodeRestrictions,NamespaceAutoProvision
  --disable-admission-plugins=DefaultStorageClass
```

```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml
spec:
  containers:
    - command:
        - kube-apiserver
        - --enable-admission-plugins=NodeRestrictions,NamespaceAutoProvision
        - --disable-admission-plugins=DefaultStorageClass
```

- Please be aware that the NamespaceExists and NamespaceAutoProvision admission controllers have been deprecated and are now succeeded by the NamespaceLifecycle admission controller.

The NamespaceLifecycle admission controller ensures that any requests made to a non-existent namespace are rejected, and it safeguards the default namespaces, including default, kube-system, and kube-public, from being deleted.

---

### Imperative Commands

| CMD                                                                                                             | DESC                          |
| --------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `kube-apiserver -h \| grep enable-admission-plugins`                                                            | List enabled admission plugin |
| `kubectl exec kube-apiserver-controlplane -n kube-system -- kube-apiserver -h \| grep enable-admission-plugins` | List enabled admission plugin |
| `ps -ef \| grep kube-apiserver \| grep admission-plugins`                                                       | List enabled plugin           |

---

```sh
kubectl exec kube-apiserver-controlplane -n kube-system -- kube-apiserver -h | grep admission-plugins
# --disable-admission-plugins strings            admission plugins that should be disabled although they are in the default enabled plugins list (NamespaceLifecycle, LimitRanger, ServiceAccount, TaintNodesByCondition, PodSecurity, Priority, DefaultTolerationSeconds, DefaultStorageClass, StorageObjectInUseProtection, PersistentVolumeClaimResize, RuntimeClass, CertificateApproval, CertificateSigning, ClusterTrustBundleAttest, CertificateSubjectRestriction, DefaultIngressClass, PodTopologyLabels, MutatingAdmissionPolicy, MutatingAdmissionWebhook, ValidatingAdmissionPolicy, ValidatingAdmissionWebhook, ResourceQuota).
# Comma-delimited list of admission plugins: AlwaysAdmit, AlwaysDeny, AlwaysPullImages, CertificateApproval, CertificateSigning, CertificateSubjectRestriction, ClusterTrustBundleAttest, DefaultIngressClass, DefaultStorageClass, DefaultTolerationSeconds, DenyServiceExternalIPs, EventRateLimit, ExtendedResourceToleration, ImagePolicyWebhook, LimitPodHardAntiAffinityTopology, LimitRanger, MutatingAdmissionPolicy, MutatingAdmissionWebhook, NamespaceAutoProvision, NamespaceExists, NamespaceLifecycle, NodeRestriction, OwnerReferencesPermissionEnforcement, PersistentVolumeClaimResize, PodNodeSelector, PodSecurity, PodTolerationRestriction, PodTopologyLabels, Priority, ResourceQuota, RuntimeClass, ServiceAccount, StorageObjectInUseProtection, TaintNodesByCondition, ValidatingAdmissionPolicy, ValidatingAdmissionWebhook. The order of plugins in this flag does not matter.
# --enable-admission-plugins strings             admission plugins that should be enabled in addition to default enabled ones (NamespaceLifecycle, LimitRanger, ServiceAccount, TaintNodesByCondition, PodSecurity, Priority, DefaultTolerationSeconds, DefaultStorageClass, StorageObjectInUseProtection, PersistentVolumeClaimResize, RuntimeClass, CertificateApproval, CertificateSigning, ClusterTrustBundleAttest, CertificateSubjectRestriction, DefaultIngressClass, PodTopologyLabels, MutatingAdmissionPolicy, MutatingAdmissionWebhook, ValidatingAdmissionPolicy, ValidatingAdmissionWebhook, ResourceQuota).
# Comma-delimited list of admission plugins: AlwaysAdmit, AlwaysDeny, AlwaysPullImages, CertificateApproval, CertificateSigning, CertificateSubjectRestriction, ClusterTrustBundleAttest, DefaultIngressClass, DefaultStorageClass, DefaultTolerationSeconds, DenyServiceExternalIPs, EventRateLimit, ExtendedResourceToleration, ImagePolicyWebhook, LimitPodHardAntiAffinityTopology, LimitRanger, MutatingAdmissionPolicy, MutatingAdmissionWebhook, NamespaceAutoProvision, NamespaceExists, NamespaceLifecycle, NodeRestriction, OwnerReferencesPermissionEnforcement, PersistentVolumeClaimResize, PodNodeSelector, PodSecurity, PodTolerationRestriction, PodTopologyLabels, Priority, ResourceQuota, RuntimeClass, ServiceAccount, StorageObjectInUseProtection, TaintNodesByCondition, ValidatingAdmissionPolicy, ValidatingAdmissionWebhook. The order of plugins in this flag does not matter.

# query the default enable plugin
cat /etc/kubernetes/manifests/kube-apiserver.yaml
# - --enable-admission-plugins=NodeRestriction

# try to create a pod in a ns that does not exist
kubectl run nginx --image nginx -n blue
# Error from server (NotFound): namespaces "blue" not found

# enable NamespaceAutoProvision plugin
vi /etc/kubernetes/manifests/kube-apiserver.yaml
# - --enable-admission-plugins=NodeRestriction,NamespaceAutoProvision

# try pod creation
kubectl run nginx --image nginx -n blue
# pod/nginx created

kubectl get ns
# NAME              STATUS   AGE
# blue              Active   32s

# disable the DefaultStorageClass admission controller
vi /etc/kubernetes/manifests/kube-apiserver.yaml
# - --disable-admission-plugins=DefaultStorageClass

# list all plugins with ps command
ps -ef | grep kube-apiserver | grep admission-plugins
# root       23121   22999  0 21:55 ?        00:00:10 kube-apiserver --advertise-address=192.168.104.29 --allow-privileged=true --authorization-mode=Node,RBAC --client-ca-file=/etc/kubernetes/pki/ca.crt --enable-admission-plugins=NodeRestriction,NamespaceAutoProvision --disable-admission-plugins=DefaultStorageClass --enable-bootstrap-token-auth=true --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key --etcd-servers=https://127.0.0.1:2379 --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key --requestheader-allowed-names=front-proxy-client --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt --requestheader-extra-headers-prefix=X-Remote-Extra- --requestheader-group-headers=X-Remote-Group --requestheader-username-headers=X-Remote-User --secure-port=6443 --service-account-issuer=https://kubernetes.default.svc.cluster.local --service-account-key-file=/etc/kubernetes/pki/sa.pub --service-account-signing-key-file=/etc/kubernetes/pki/sa.key --service-cluster-ip-range=172.20.0.0/16 --tls-cert-file=/etc/kubernetes/pki/apiserver.crt --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
```

---

## Validating & Mutating Admission Controller

- 2 types of admission controller

- `validating admission controller`

  - a plugin that **intercepts** requests to the Kubernetes API server (like creating pods, services) to check and enforce policies, **allowing or denying the request based on whether it meets predefined rules**, without altering the object itself.
  - the plugins to validate the request, allow or deny

- `mutating Admission Controller`

  - a powerful plugin that intercepts API requests (like creating a Pod or Deployment) and **modifies (mutates) the object's data** before it's persisted, adding defaults, injecting sidecars, setting labels, or altering resource requests/limits, acting as a first line of defense to enforce cluster policies and automate configurations before validation.
  - the plugins can change the request

- A plugins can do both

- `mutating ac` usually are invoked first before `validating ac`

---

## Mutating/Validating Admission Webhook

- Customize admission controller with costomized logic

- Steps:
  - set up webhook server with customized logic
  - configure webhook on k8s by creating a webhook configuration object

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: "pod-policy.example.com"
webhooks:
  - name: "pod-policy.example.com"
    clientConfig:
      service:
        namespace: "webhook-namespace"
        name: "webhook-service"
      caBundle: "Ci0tLS0tQk.....tLS0K"
    rules:
      - apiGroups: [""]
        apiVersions: ["v1"]
        operations: ["CREATE"]
        resources: ["pods"]
        scope: "Namespaced"
```
