# Kubernetes - Image

[Back](../index.md)

- [Kubernetes - Image](#kubernetes---image)
  - [Image](#image)
    - [Lab: pull image from private repo](#lab-pull-image-from-private-repo)

---

## Image

- library:

  - the default account where Docker's official images are stored.
  - can be ommited: `library/nginx` = `nginx`

- a specific user/account

  - `image: user_account/image_repo`

- Source:

  - by default:
    - Docker default registry `docker.io`
    - `image: docker.io/library/nginx` = `image: nginx`
  - common registeries
    - `gcr.io`: google registery

- `private repository`
  - the repo only used internally

---

### Lab: pull image from private repo

- Authentication

```sh
# create docker secret with built-in secret type docker-registry
kubectl create secret docker-registry regcred \
    --docker-server= private-registry.io
    --docker-username= username
    --docker-password= pwd
    --docker-email= email

```

- Apply secret in pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: private-reg
spec:
  containers:
  - name: private-reg-container
    image: <your-private-image>
  imagePullSecrets:
  - name: regcred
```
