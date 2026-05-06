# ArgoCD - Repository

[Back](../index.md)

- [ArgoCD - Repository](#argocd---repository)
  - [Repository](#repository)
    - [Common Commands](#common-commands)
  - [Lab: Add Public Repo](#lab-add-public-repo)
    - [GitHub Repo](#github-repo)
    - [Helm Repo](#helm-repo)
  - [Lab: Private Repo](#lab-private-repo)
    - [GitHub via HTTPS](#github-via-https)
    - [GitHub via HTTPS - Declarative](#github-via-https---declarative)
    - [GitHub via SSH](#github-via-ssh)
    - [GitHub via SSH - Declarative](#github-via-ssh---declarative)
  - [Lab: Create App with private repo](#lab-create-app-with-private-repo)

---

## Repository

- `Repository`
  - the **source of truth**—a Git or Helm repository **containing Kubernetes manifests** (YAML, Helm charts, Kustomize) that define the desired state of an application.
  - monitors this repository and syncs changes to the target Kubernetes cluster, acting as a GitOps-based CD controller.

- `Public repos` can be **used directly** in application.
- `Private repos` needs to be registered in ArgoCD with proper authentication before using it in applications.
  - `HTTPs`: using **username** and **password** or access token.
  - `SSH`: using `ssh private key`.
  - GitHub / GitHub Enterprise : **GitHub App credentials**.
- **Private repos credentials** are stored in normal `k8s secrets`.
- You can register repos using declarative approach, cli and web UI.

---

### Common Commands

| Command                                  | Description                                                   |
| ---------------------------------------- | ------------------------------------------------------------- |
| `argocd repo list`                       | List repositories registered in Argo CD.                      |
| `argocd repo get <repo-url>`             | Show details of one registered repository.                    |
| `argocd repo add <repo-url>`             | Add a Git or Helm repository to Argo CD.                      |
| `argocd repo rm <repo-url>`              | Remove a repository from Argo CD.                             |
| `argocd repocreds list`                  | List repository credential templates.                         |
| `argocd repocreds add <repo-url-prefix>` | Add reusable credentials for repositories under a URL prefix. |
| `argocd repocreds rm <repo-url-prefix>`  | Remove repository credential template.                        |

---

## Lab: Add Public Repo

### GitHub Repo

```sh
argocd repo add https://github.com/simonangel-fong/Terraform_Demo_AWS_EKS_ArgoCD.git --name eks --project default
# Repository 'https://github.com/simonangel-fong/Terraform_Demo_AWS_EKS_ArgoCD.git' added

argocd repo list
# TYPE  NAME  REPO                                                                  INSECURE  OCI    LFS    CREDS  STATUS      MESSAGE  PROJECT
# git   eks   https://github.com/simonangel-fong/Terraform_Demo_AWS_EKS_ArgoCD.git  false     false  false  false  Successful           default

argocd repo get  https://github.com/simonangel-fong/Terraform_Demo_AWS_EKS_ArgoCD.git
# TYPE  NAME  REPO                                                                  INSECURE  OCI    LFS    CREDS  STATUS      MESSAGE  PROJECT
# git   eks   https://github.com/simonangel-fong/Terraform_Demo_AWS_EKS_ArgoCD.git  false     false  false  false  Successful           default

argocd repo rm  https://github.com/simonangel-fong/Terraform_Demo_AWS_EKS_ArgoCD.git
# Repository 'https://github.com/simonangel-fong/Terraform_Demo_AWS_EKS_ArgoCD.git' removed
```

---

### Helm Repo

```sh
argocd repo add https://simonangel-fong.github.io/Demo_Helm_Public_Repo/ --type helm --name web-app --project default
# Repository 'https://simonangel-fong.github.io/Demo_Helm_Public_Repo/' added

argocd repo list
# TYPE  NAME     REPO                                                      INSECURE  OCI    LFS    CREDS  STATUS      MESSAGE  PROJECT
# helm  web-app  https://simonangel-fong.github.io/Demo_Helm_Public_Repo/  false     false  false  false  Successful           default

argocd repo rm https://simonangel-fong.github.io/Demo_Helm_Public_Repo/
# Repository 'https://simonangel-fong.github.io/Demo_Helm_Public_Repo/' removed
```

---

## Lab: Private Repo

### GitHub via HTTPS

```sh
argocd repo add https://github.com/simonangel-fong/Demo_Helm_Private_Repo.git --name web-app --project default --username simonangel-fong
# input pwd
# Repository 'https://github.com/simonangel-fong/Demo_Helm_Private_Repo.git' added

argocd repo list
# TYPE  NAME     REPO                                                           INSECURE  OCI    LFS    CREDS  STATUS      MESSAGE  PROJECT
# git   web-app  https://github.com/simonangel-fong/Demo_Helm_Private_Repo.git  false     false  false  false  Successful           default

argocd repo rm https://github.com/simonangel-fong/Demo_Helm_Private_Repo.git
# Repository 'https://github.com/simonangel-fong/Demo_Helm_Private_Repo.git' removed
```

---

### GitHub via HTTPS - Declarative

- `private_repo_https.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: private-repo
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  name: web-app
  project: default
  url: https://github.com/simonangel-fong/Demo_Helm_Private_Repo.git
  type: git
  username: simonangel-fong
  password: 
```

```sh
# create secret
kubectl apply -f private_repo_https.yaml
# secret/private-repo created

argocd repo list
# TYPE  NAME  REPO                                                           INSECURE  OCI    LFS    CREDS  STATUS      MESSAGE  PROJECT
# git         https://github.com/simonangel-fong/Demo_Helm_Private_Repo.git  false     false  false  false  Successful           default

# delete secret
kubectl delete -f private_repo_https.yaml
```

---

### GitHub via SSH

- Create key

```sh
ssh-keygen -t ed25519 -C "simonangelfong@gmail.com" -f ./id_ed25519_argocd
```

- Upload deploy key
  - settings > Deploy keys > create > paste pub

```sh
argocd repo add git@github.com:simonangel-fong/Demo_Helm_Private_Repo.git --ssh-private-key-path ./id_ed25519_argocd --name web-app --project default
# Repository 'git@github.com:simonangel-fong/Demo_Helm_Private_Repo.git' added

argocd repo list
# TYPE  NAME     REPO                                                       INSECURE  OCI    LFS    CREDS  STATUS      MESSAGE  PROJECT
# git   web-app  git@github.com:simonangel-fong/Demo_Helm_Private_Repo.git  false     false  false  false  Successful           default

argocd repo rm git@github.com:simonangel-fong/Demo_Helm_Private_Repo.git
# Repository 'git@github.com:simonangel-fong/Demo_Helm_Private_Repo.git' removed
```

---

### GitHub via SSH - Declarative

- `private_repo_ssh.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: private-repo-ssh
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  name: web-app
  project: default
  url: git@github.com:simonangel-fong/Demo_Helm_Private_Repo.git
  type: git
  sshPrivateKey: |
    -----BEGIN OPENSSH PRIVATE KEY-----
    ...
    -----END OPENSSH PRIVATE KEY-----
```

```sh
# create secret
kubectl apply -f private_repo_ssh.yaml
# secret/private-repo-ssh created

argocd repo list
# TYPE  NAME  REPO                                                       INSECURE  OCI    LFS    CREDS  STATUS      MESSAGE  PROJECT
# git         git@github.com:simonangel-fong/Demo_Helm_Private_Repo.git  false     false  false  false  Successful

# delete secret
kubectl delete -f private_repo_ssh.yaml
# secret "private-repo-ssh" deleted from argocd namespace
```

---

## Lab: Create App with private repo

```yaml


```