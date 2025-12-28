# Kubernetes - Objects: Annotations

[Back](../../index.md)

- [Kubernetes - Objects: Annotations](#kubernetes---objects-annotations)
  - [Annotation](#annotation)
    - [Imperative Commands](#imperative-commands)
    - [Declarative Manifest](#declarative-manifest)
  - [Lab: Annotation](#lab-annotation)

---

## Annotation

- limitation of labels:

  - maximum length of a **label value** is only **63 characters**
  - the value **can’t** contain **whitespace** at all.

- `Annotation`

  - **a key–value pair of metadata** attached to an object that is intended only for **information storage and reference**
  - not for identification, grouping, or selection.
  - up to 256 KB
  - can contain any character
  - must be a string
    - can contain **plain text**, `YAML`, `JSON`, or even a `Base64-Encoded value`.

- Common use cases:

  - attach the URL of the Git repository
  - the Git commit hash
  - the build timestamp
  - pod description
  - creator of the object
  - bool value to signal to the deployment tool

- vs label

  - `Labels`: selection & grouping
  - `Annotations`: configuration & behavior

- Whether trigger roll out?
  - only when the Pod template changed in Deployment
    - `.spec.template.metadata.annotations` triggers roll out
  - not when pod, svc, etc.

---

### Imperative Commands

| CMD                                                         | DESC                                        |
| ----------------------------------------------------------- | ------------------------------------------- |
| `kubectl annotate pod mypod key=value`                      | Add an annotation                           |
| `kubectl annotate pod mypod key=value key2=value2`          | Add multiple annotations                    |
| `kubectl annotate pod mypod key=value --overwrite`          | Update existing annotation                  |
| `kubectl annotate pod mypod key-`                           | Delete an annotation                        |
| `kubectl annotate pod mypod --list`                         | List annotations on the object              |
| `kubectl annotate deploy myapp team=backend`                | Annotate a Deployment                       |
| `kubectl annotate svc mysvc description="internal service"` | Annotate a Service                          |
| `kubectl annotate node node1 zone=us-east-1a`               | Annotate a Node                             |
| `kubectl annotate ns dev owner=platform-team`               | Annotate a Namespace                        |
| `kubectl annotate pod mypod key=value --record`             | Record annotation change in rollout history |

- Create pod with annotation

```sh
kubectl run nginx-demo --image=nginx --annotations="owner=platform-team,env=dev,purpose=demo"
```

- View Annotations

| CMD                                                           | DESC                           |
| ------------------------------------------------------------- | ------------------------------ |
| `kubectl get pod mypod -o yaml`                               | View all annotations           |
| `kubectl describe pod mypod`                                  | Human readable annotation view |
| `kubectl get pod mypod -o jsonpath='{.metadata.annotations}'` | Print annotations only         |

- Real-World Examples

| Purpose      | Example                                            |
| ------------ | -------------------------------------------------- |
| AWS ALB      | `alb.ingress.kubernetes.io/scheme=internet-facing` |
| cert-manager | `cert-manager.io/cluster-issuer=letsencrypt-prod`  |
| ArgoCD       | `argocd.argoproj.io/sync-wave=5`                   |
| Helm         | `meta.helm.sh/release-name=myapp`                  |

---

### Declarative Manifest

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-annotated
  labels:
    app: nginx
  annotations:
    # pod info
    description: "Demo nginx pod with annotations"
    owner: "platform-team"
    last-updated-by: "kubectl"
    purpose: "testing-annotation"
    # Auto Scrape
    prometheus.io/scrape: "true"
    prometheus.io/port: "80"
    prometheus.io/path: "/metrics"
spec:
  containers:
    - name: nginx
      image: nginx:latest
      ports:
        - containerPort: 80
```

---

## Lab: Annotation

```sh
# create pod with annotation
kubectl run nginx --image=nginx --annotations="owner=platform-team,env=dev,purpose=demo"
# pod/nginx created

kubectl describe pod nginx
# Annotations:      owner: platform-team,env=dev,purpose=demo

# add annotation
kubectl annotate pod nginx created-by='creator' managed-by='terraform'
# pod/nginx annotated

# confirm
kubectl get pod nginx -o jsonpath='{.metadata.annotations}'
# '{"created-by":"'creator'","managed-by":"'terraform'","owner":"platform-team,env=dev,purpose=demo"}'

# update
kubectl annotate pod nginx managed-by='helm' --overwrite
# pod/nginx annotated

# confirm
kubectl get pod nginx -o jsonpath='{.metadata.annotations.managed-by}'
# ''helm''

# delete
kubectl annotate pod nginx managed-by- created-by-
# pod/nginx annotated

# confirm 
kubectl get pod nginx -o=jsonpath="{.metadata.annotations}"
# {"owner":"platform-team,env=dev,purpose=demo"}
```