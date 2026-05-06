# ArgoCD - Private Repository

[Back](../index.md)

- [ArgoCD - Private Repository](#argocd---private-repository)
  - [Private Repository](#private-repository)
    - [connects via HTTPS and SSH](#connects-via-https-and-ssh)
  - [Connect via HTTPS Username And Password Credential](#connect-via-https-username-and-password-credential)

---

## Private Repository

### connects via HTTPS and SSH

- `Argo CD` will look for `secrets` within the `argocd` namespace for the provided repository.
  - Once it finds a matching credential, it will use it to authenticate into the repository.

- Label `argocd.argoproj.io/secret-type: repository`
  - a **mandatory label** that defines which `secrets` contain repository credentials

- ref:
  - https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/
  - https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#repositories

## Connect via HTTPS Username And Password Credential

- HTTPS URL: start with `https://`
- require a username and password

```sh
argocd repo add https://github.com/argoproj/argocd-example-apps --username <username> --password <password>
```


```yaml
apiVersion: v1
kind: Secret
metadata:
  name: private-repo
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  type: git
  url: https://github.com/argoproj/private-repo
  password: my-password
  username: my-username
  project: my-project
---

apiVersion: v1
kind: Secret
metadata:
  name: private-repo
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  type: git
  url: git@github.com:argoproj/my-private-repository.git
  sshPrivateKey: |
    -----BEGIN OPENSSH PRIVATE KEY-----
    ...
    -----END OPENSSH PRIVATE KEY-----
```