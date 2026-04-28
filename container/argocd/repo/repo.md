# ArgoCD - Repository

[Back](../index.md)

- [ArgoCD - Repository](#argocd---repository)
  - [Repository](#repository)
    - [Common Commands](#common-commands)
  - [Lab: add repo](#lab-add-repo)
  - [Lab: Private Repo with https](#lab-private-repo-with-https)
  - [Lab: Private Repo with ssh](#lab-private-repo-with-ssh)
  - [Helm Repos](#helm-repos)
  - [Lab: add a private helm repos](#lab-add-a-private-helm-repos)
  - [Credential Templates](#credential-templates)

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

| Command                                   | Description                                                   |
| ----------------------------------------- | ------------------------------------------------------------- |
| `argocd repo list`                        | List repositories registered in Argo CD.                      |
| `argocd repo get <repo-url>`              | Show details of one registered repository.                    |
| `argocd repo add <repo-url>`              | Add a Git or Helm repository to Argo CD.                      |
| `argocd repo rm <repo-url>`               | Remove a repository from Argo CD.                             |
| `argocd repo update <repo-url>`           | Update repository connection settings.                        |
| `argocd repo creds list`                  | List repository credential templates.                         |
| `argocd repo creds add <repo-url-prefix>` | Add reusable credentials for repositories under a URL prefix. |
| `argocd repo creds rm <repo-url-prefix>`  | Remove repository credential template.                        |

---

## Lab: add repo

## Lab: Private Repo with https

## Lab: Private Repo with ssh

---

## Helm Repos

- **Public standard** `Helm repos` can be used directly in application.
- **Non standard** `Helm repositories` have to be **registered explicitly**.
- **Private** `Helm repos` needs to be **registered** in ArgoCD with proper authentication before using it in applications.
- ArgoCD support connecting to **private** Helm repos using **username/password** and tls **cert/key**.
- Registering Helm repos in ArgoCD can be done declaratively, CLI and Web UI.

---

## Lab: add a private helm repos


---

## Credential Templates


- Used If you want to **use the same credentials** for **multiple repositories** in your organization without having to repeat credential configuration.