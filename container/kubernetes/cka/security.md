# CKA - Security

[Back](../index.md)

- [CKA - Security](#cka---security)
  - [Security](#security)
    - [Task: Security Standard](#task-security-standard)
    - [Task: RBAC](#task-rbac)
    - [Task: RBAC](#task-rbac-1)
    - [Task: \*\*\*csr + user + role](#task-csr--user--role)
    - [Task: SA](#task-sa)
    - [Task: Security Context - Cacapabilities](#task-security-context---cacapabilities)
    - [Task: create po with non-root user](#task-create-po-with-non-root-user)

---

## Security

### Task: Security Standard

Enforce the Restricted Pod Security Standard on the namespace restricted-ns.
Pods in that namespace cannot:
. have privileged access
· host networking
. have any elevated rights

---

- Setup env

```sh
kubectl create ns restricted-ns
```

---

- Solution

- ref: https://kubernetes.io/docs/tasks/configure-pod-container/enforce-standards-namespace-labels/

```sh
# label ns as restricted
kubectl label --overwrite ns restricted-ns pod-security.kubernetes.io/enforce=restricted
# namespace/restricted-ns labeled

# confirm
kubectl describe ns restricted-ns
# Labels:       kubernetes.io/metadata.name=restricted-ns
#               pod-security.kubernetes.io/enforce=restricted
```

- If to set it to a specific version

```sh
kubectl label --overwrite ns restricted-ns pod-security.kubernetes.io/enforce-version=v1.35
# namespace/restricted-ns labeled

kubectl describe ns restricted-ns
# Labels:       kubernetes.io/metadata.name=restricted-ns
#               pod-security.kubernetes.io/enforce-version=v1.35

```

---

### Task: RBAC

CKA EXAM OBJECTIVE: Manage role based access control (RBAC)
TASK:

1. Create a ClusterRole named app-creator that allows create permissions for Deployments, StatefulSets, and DaemonSets.
2. Create a ServiceAccount named app-dev.
3. Bind the ServiceAccount app-dev to the ClusterRole app-creator using a ClusterRoleBinding.

---

- Solution

```sh
kubectl create clusterrole app-creator --verb=create --resource=deployments,statefulsets,daemonsets --dry-run=client -o yaml > clusterrole.yaml

k apply -f clusterrole.yaml
# clusterrole.rbac.authorization.k8s.io/app-creator created

k describe clusterrole app-creator
# Name:         app-creator
# Labels:       <none>
# Annotations:  <none>
# PolicyRule:
#   Resources          Non-Resource URLs  Resource Names  Verbs
#   ---------          -----------------  --------------  -----
#   daemonsets.apps    []                 []              [create]
#   deployments.apps   []                 []              [create]
#   statefulsets.apps  []                 []              [create]

kubectl create serviceaccount app-dev
# serviceaccount/app-dev created

kubectl describe sa app-dev
# Name:                app-dev
# Namespace:           default
# Labels:              <none>
# Annotations:         <none>
# Image pull secrets:  <none>
# Mountable secrets:   <none>
# Tokens:              <none>
# Events:              <none>


kubectl create clusterrolebinding app-creator-binding --clusterrole=app-creator --serviceaccount=default:app-dev
# clusterrolebinding.rbac.authorization.k8s.io/app-creator-binding created

kubectl describe clusterrolebinding app-creator-binding
# Name:         app-creator-binding
# Labels:       <none>
# Annotations:  <none>
# Role:
#   Kind:  ClusterRole
#   Name:  app-creator
# Subjects:
#   Kind            Name     Namespace
#   ----            ----     ---------
#   ServiceAccount  app-dev  default

```

### Task: RBAC

Context
为部署流水线创建一个新的 ClusterRole 并将其绑定到范围为特定的 namespace 的特定 ServiceAccount。

Task
创建一个名为 deployment-clusterrole 且仅允许创建以下资源类型的新 ClusterRole：
Deployment
StatefulSet
DaemonSet
在现有的 namespace app-team1 中创建一个名为 cicd-token 的新 ServiceAccount。
限于 namespace app-team1 中，将新的 ClusterRole deployment-clusterrole 绑定到新的 ServiceAccount cicd-token。Copy

---

- Solution

```sh
# create cluster role
kubectl create clusterrole deployment-clusterrole --resource=deployment,statefulsets,daemonsets --verb=create
# clusterrole.rbac.authorization.k8s.io/deployment-clusterrole created

# create sa
kubectl create sa cicd-token -n app-team1
# serviceaccount/cicd-token created

# cluster role binding
kubectl create rolebinding cicd-token-rolebinding --clusterrole=deployment-clusterrole --serviceaccount=app-team1:cicd-token -n app-team1

# confirm
kubectl -n app-team1 describe rolebinding cicd-token-rolebinding
# Name:         cicd-token-rolebinding
# Labels:       <none>
# Annotations:  <none>
# Role:
#   Kind:  ClusterRole
#   Name:  deployment-clusterrole
# Subjects:
#   Kind            Name        Namespace
#   ----            ----        ---------
#   ServiceAccount  cicd-token  app-team1

```

---

### Task: \*\*\*csr + user + role

- ref: https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/

Create a new user called `john`. Grant him access to the cluster using a `csr` named `john-developer`. Create a `role` **developer** which should grant John the permission to **create, list, get, update** and **delete** pods in the `development` namespace .

The private key exists in the location: ~/csr/john.key and csr at ~/csr/john.csr.

- Setup env

```sh
mkdir -pv ~/csr
cd csr
# create private key
openssl genrsa -out john.key 3072

# create csr.
openssl req -new -key john.key -out john.csr -subj "/CN=john"

k create ns development
```

---

- key
  Solution manifest file to create a CSR as follows:

```sh
# Encode the CSR document using this command:
cat john.csr | base64 | tr -d "\n"
# LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJRFZqQ0NBYjRDQVFBd0VURVBNQTBHQTFVRUF3d0diWGwxYzJWeU1JSUJvakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVk4QU1JSUJpZ0tDQVlFQXNEQnhFTDN0Z3BDTkpzKzNMSHVMMVRtb1ZqRDZGYnBvU2s5azFBaDVhZ0RyCnZzRUcyWDdEL0ZnU2J4RUhXTE1LYlNBTWFlT21HZG8xQmxVZDNXcjNKeDN3S2ZsRlZvWmxHSDdJMHdWTlpEMG8KSmVRVlUwQW5SQ21xaldTVWhDZVkzN0tiMDVOc2xFNC9YYzBCamVhaGNOajZmbFRFRmJwaG92RDl2cjNDekNUUApBNnlzNmpSa2ZYYnJ1T3JTbjBGbUFhUFJVU0R2TG1ndytVbStoTFBHR3p2MXFCcndCWFV4eUxxL0Q1WFlFSk9PCkNKL004aVBCcXUyYzZIVUdQSkhlMmhoS3RBaGtyQXNRQ3VqOGhQdFRDek1qNTJPSHBUSXhhVWV3cEVYTmZWMmIKaVlJMWN5UUNCYXhPNmxHVnU2djQwSnBXRkpQSDN1QkZ2Z1RBbDE4QnZrRzBiWjh1N2FBWXFrZHFVa3NZWi8vUApYa0xDeHY5b2dFWTdiQnZ6dXEvc2g0MzExTVJGMERwWVZxNjl5c1pXOE11V0VHdW9rejNqZmdyUE5hTkpBSkZ5CkZITVNlcXRGbGQrbUJKd2RscEdVL1VVT1kzWW80L2daWHVsQjQrQlA1R2QwTGF5dElscCtMNk9mNGVTMUxhejgKc1BEVUFXdDBEVnNjV0ZnSmFhaVJBZ01CQUFHZ0FEQU5CZ2txaGtpRzl3MEJBUXNGQUFPQ0FZRUFmdE5aUVRrcgpJQnlHdm1laWxHSlR4RzUwMnlnb2FBQ3ZLWEVJTTkxRC9NOStzVWttMGRwckd5Yk5IYkM1dWlvQjJNOElXV0s1CkFtYmFLaDA1RnB0OFdoaEVoQkJ1aVArRTZTWTV3eXpGZXo5N0Y4TnpnUjhVekhyTk9qaFU2RXM1UWlXbVYyY2gKcW5MeXFNNmxBL2ZZaEdlT3h3eGNTVTVseWNvck5IQVlwTWZUajZzeU1raDBGM3UxRkpFL295L1dyYklORGFObgozWFVyckF1YlVuWHpHQUJDZ0xNYi9jdlBjM1RtU0xHMmIwZ0ltUUtlZW0ySjJQTWNVMVVuczJSMS9RT3pRVEdMCjJQT2hGL3BMV25ZNDRrOEhsQmpHUWtROEtVWEhJN1NNUjViT1RrZjM1Y2d2WUZpYnhid0ZlQ2VyWUVKUFlaaGsKT2dZSm9aTFNnc3RtUGc5NndKWTVKNnhWcW0xbGpJZ3FLR1RyYlBOZm1VSVRTZVZkRS9wNTFMR3U1bktzOTlqTgp3dDRES3VxdkUxUWZudlJPaDlBZW5ET0kzMnNrUHliTVVOQTArZjBYRStvcDNma0syUmRkMXprR3JLd1hvY2QvCkFZVmZyUjd0V3JNY0Rmckd6TUlRU2FPOGtPVFFFdE1wS2RpMEVRZENVMzhWcmFhdXZvOGNJQXRmCi0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
```

```yaml
# csr.yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: john-developer
spec:
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJRFZqQ0NBYjRDQVFBd0VURVBNQTBHQTFVRUF3d0diWGwxYzJWeU1JSUJvakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVk4QU1JSUJpZ0tDQVlFQXNEQnhFTDN0Z3BDTkpzKzNMSHVMMVRtb1ZqRDZGYnBvU2s5azFBaDVhZ0RyCnZzRUcyWDdEL0ZnU2J4RUhXTE1LYlNBTWFlT21HZG8xQmxVZDNXcjNKeDN3S2ZsRlZvWmxHSDdJMHdWTlpEMG8KSmVRVlUwQW5SQ21xaldTVWhDZVkzN0tiMDVOc2xFNC9YYzBCamVhaGNOajZmbFRFRmJwaG92RDl2cjNDekNUUApBNnlzNmpSa2ZYYnJ1T3JTbjBGbUFhUFJVU0R2TG1ndytVbStoTFBHR3p2MXFCcndCWFV4eUxxL0Q1WFlFSk9PCkNKL004aVBCcXUyYzZIVUdQSkhlMmhoS3RBaGtyQXNRQ3VqOGhQdFRDek1qNTJPSHBUSXhhVWV3cEVYTmZWMmIKaVlJMWN5UUNCYXhPNmxHVnU2djQwSnBXRkpQSDN1QkZ2Z1RBbDE4QnZrRzBiWjh1N2FBWXFrZHFVa3NZWi8vUApYa0xDeHY5b2dFWTdiQnZ6dXEvc2g0MzExTVJGMERwWVZxNjl5c1pXOE11V0VHdW9rejNqZmdyUE5hTkpBSkZ5CkZITVNlcXRGbGQrbUJKd2RscEdVL1VVT1kzWW80L2daWHVsQjQrQlA1R2QwTGF5dElscCtMNk9mNGVTMUxhejgKc1BEVUFXdDBEVnNjV0ZnSmFhaVJBZ01CQUFHZ0FEQU5CZ2txaGtpRzl3MEJBUXNGQUFPQ0FZRUFmdE5aUVRrcgpJQnlHdm1laWxHSlR4RzUwMnlnb2FBQ3ZLWEVJTTkxRC9NOStzVWttMGRwckd5Yk5IYkM1dWlvQjJNOElXV0s1CkFtYmFLaDA1RnB0OFdoaEVoQkJ1aVArRTZTWTV3eXpGZXo5N0Y4TnpnUjhVekhyTk9qaFU2RXM1UWlXbVYyY2gKcW5MeXFNNmxBL2ZZaEdlT3h3eGNTVTVseWNvck5IQVlwTWZUajZzeU1raDBGM3UxRkpFL295L1dyYklORGFObgozWFVyckF1YlVuWHpHQUJDZ0xNYi9jdlBjM1RtU0xHMmIwZ0ltUUtlZW0ySjJQTWNVMVVuczJSMS9RT3pRVEdMCjJQT2hGL3BMV25ZNDRrOEhsQmpHUWtROEtVWEhJN1NNUjViT1RrZjM1Y2d2WUZpYnhid0ZlQ2VyWUVKUFlaaGsKT2dZSm9aTFNnc3RtUGc5NndKWTVKNnhWcW0xbGpJZ3FLR1RyYlBOZm1VSVRTZVZkRS9wNTFMR3U1bktzOTlqTgp3dDRES3VxdkUxUWZudlJPaDlBZW5ET0kzMnNrUHliTVVOQTArZjBYRStvcDNma0syUmRkMXprR3JLd1hvY2QvCkFZVmZyUjd0V3JNY0Rmckd6TUlRU2FPOGtPVFFFdE1wS2RpMEVRZENVMzhWcmFhdXZvOGNJQXRmCi0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400
  usages:
    - client auth
```

```sh
k apply -f csr.yaml
# certificatesigningrequest.certificates.k8s.io/john-developer created

k get csr
# NAME             AGE     SIGNERNAME                                    REQUESTOR                  REQUESTEDDURATION   CONDITION
# john-developer   7s      kubernetes.io/kube-apiserver-client           kubernetes-admin           24h                 Pending

# approve csr
kubectl certificate approve john-developer
# certificatesigningrequest.certificates.k8s.io/john-developer approved

# confirm
k get csr
# NAME             AGE     SIGNERNAME                                    REQUESTOR                  REQUESTEDDURATION   CONDITION
# john-developer   69s     kubernetes.io/kube-apiserver-client           kubernetes-admin           24h                 Approved,Issued

# create role
kubectl create role developer --resource=pods --verb=create,list,get,update,delete --namespace=development
# role.rbac.authorization.k8s.io/developer created

# create rolebinding
kubectl create rolebinding developer-role-binding --role=developer --user=john --namespace=development
# rolebinding.rbac.authorization.k8s.io/developer-role-binding created

# confirm
kubectl describe rolebinding developer-role-binding -n development
# Name:         developer-role-binding
# Labels:       <none>
# Annotations:  <none>
# Role:
#   Kind:  Role
#   Name:  developer
# Subjects:
#   Kind  Name  Namespace
#   ----  ----  ---------
#   User  john

# confirm
kubectl auth can-i create pods --as=john --namespace=default
# no
kubectl auth can-i update pods --as=john --namespace=development
# yes
kubectl auth can-i create deployments --as=john --namespace=development
# no
```

---

### Task: SA

Create a new service account with the name pvviewer. Grant this Service account access to list all PersistentVolumes in the cluster by creating an appropriate cluster role called pvviewer-role and ClusterRoleBinding called pvviewer-role-binding.
Next, create a pod called pvviewer with the image: redis and serviceAccount: pvviewer in the default namespace.

---

- Solution

```sh
kubectl create sa pvviewer
# serviceaccount/pvviewer created

kubectl create clusterrole pvviewer-role --verb=list --resource=PersistentVolumes
# clusterrole.rbac.authorization.k8s.io/pvviewer-role created

kubectl describe clusterrole pvviewer-role
# Name:         pvviewer-role
# Labels:       <none>
# Annotations:  <none>
# PolicyRule:
#   Resources          Non-Resource URLs  Resource Names  Verbs
#   ---------          -----------------  --------------  -----
#   persistentvolumes  []                 []              [list]

kubectl create clusterrolebinding pvviewer-role-binding --clusterrole=pvviewer-role --serviceaccount=default:pvviewer
# clusterrolebinding.rbac.authorization.k8s.io/pvviewer-role-binding created

kubectl describe clusterrolebinding pvviewer-role-binding
# Name:         pvviewer-role-binding
# Labels:       <none>
# Annotations:  <none>
# Role:
#   Kind:  ClusterRole
#   Name:  pvviewer-role
# Subjects:
#   Kind            Name      Namespace
#   ----            ----      ---------
#   ServiceAccount  pvviewer  default

tee vi sa-pod.yaml<<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: pvviewer
spec:
  serviceAccountName: pvviewer
  containers:
  - name: redis
    image: redis
EOF

kubectl apply -f sa-pod.yaml

# confirm
kubectl describe pod pvviewer | grep -i account
# Service Account:  pvviewer

```

---

### Task: Security Context - Cacapabilities

Create a new pod named admin-pod using the image busybox:1.28. Ensure the pod has the permission to set the system time. The container should sleep for 1000 seconds.

- Solution:

```yaml
# sc_pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: admin-pod
spec:
  containers:
    - name: admin-pod
      image: busybox:1.28
      command: ["sh", "-c", "sleep 1000"]
      securityContext:
        capabilities:
          add: ["SYS_TIME"]
```

```sh
k create -f sc_pod.yaml
```

---

### Task: create po with non-root user

pod name 'non-root-pod' with redis image
set 'runAsUser' = 1000, 'fsGroup' = 2000

---

- solution

```yaml
# non-root-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: non-root-pod
spec:
  securityContext:
    runAsUser: 1000
    fsGroup: 2000
  containers:
    - name: non-root-pod
      image: redis
```

```sh
kubectl apply -f non-root-pod.yaml

# cofnirm
k exec -it non-root-pod -- sh
id
# uid=1000 gid=0(root) groups=0(root),2000
id -G
# 0 2000
mkdir folder
# mkdir: cannot create directory 'folder': Permission denied
```

---
