# Argocd - Account

[Back](../index.md)

- [Argocd - Account](#argocd---account)
  - [Common Commands](#common-commands)
  - [Lab: Admin Login](#lab-admin-login)
    - [Init Admin Login](#init-admin-login)
    - [Update password](#update-password)
  - [Lab: Add a Local User](#lab-add-a-local-user)
    - [Test with new Accounts](#test-with-new-accounts)

---

## Common Commands

| CMD                                                                | DESC                                                                    |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| `argocd account list`                                              | List Argo CD local accounts and enabled capabilities                    |
| `argocd account get --account <username>`                          | Show details for a specific local account                               |
| `argocd account get-user-info`                                     | Show information about the currently logged-in user                     |
| `argocd account update-password`                                   | Change the current user’s password                                      |
| `argocd account update-password --account <username>`              | Change another local user’s password, usually requires admin permission |
| `argocd account generate-token --account <username>`               | Generate an API token for a local account                               |
| `argocd account delete-token --account <username> --id <token-id>` | Delete an API token for a local account                                 |
| `argocd account can-i <action> <resource> <subresource>`           | Check whether the current user has a specific RBAC permission           |
| `kubectl -n argocd get cm argocd-cm -o yaml`                       | View local account configuration                                        |
| `kubectl -n argocd edit cm argocd-cm`                              | Add, enable, or disable local accounts                                  |
| `kubectl -n argocd get cm argocd-rbac-cm -o yaml`                  | View RBAC policy configuration                                          |
| `kubectl -n argocd edit cm argocd-rbac-cm`                         | Edit user roles and permissions                                         |
| `kubectl -n argocd rollout restart deployment argocd-server`       | Restart Argo CD server after ConfigMap changes, if needed               |

---

## Lab: Admin Login

### Init Admin Login

```sh
# get pwd
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# port forward
kubectl port-forward svc/argocd-server -n argocd 8080:443
# login
argocd login localhost:8080
# WARNING: server certificate had error: error creating connection: tls: failed to verify certificate: x509: certificate signed by unknown authority. Proceed insecurely (y/n)? y
# Username: admin
# Password:
# 'admin:login' logged in successfully
# Context 'localhost:8080' updated

# get user info
argocd account get-user-info
# Logged In: true
# Username: admin
# Issuer: argocd
# Groups:

# get context
argocd context
# CURRENT  NAME            SERVER
# *        localhost:8080  localhost:8080

# List accounts
argocd account list
# NAME   ENABLED  CAPABILITIES
# admin  true     login

# Can I sync any app?
argocd account can-i sync applications '*'
# no
```

---

### Update password

```sh
argocd account update-password
# *** Enter password of currently logged in user (admin):
# *** Enter new password for user admin:
# *** Confirm new password for user admin:
# Password updated
# Context 'localhost:8080' updated


```

## Lab: Add a Local User

| Account   | Purpose                  | Permission                   |
| --------- | ------------------------ | ---------------------------- |
| `devops`  | Platform/DevOps engineer | Manage and sync applications |
| `auditor` | Audit/security reviewer  | Read-only access             |

- Create helm values file
  - `argocd-account-lab-values.yaml`

```yaml
configs:
  cm:
    accounts.devops: apiKey, login
    accounts.auditor: login

  rbac:
    policy.default: role:readonly
    policy.csv: |
      # devops role
      p, role:devops, applications, get, */*, allow
      p, role:devops, applications, create, */*, allow
      p, role:devops, applications, update, */*, allow
      p, role:devops, applications, delete, */*, allow
      p, role:devops, applications, sync, */*, allow
      p, role:devops, applications, action/*, */*, allow
      p, role:devops, applications, override, */*, allow

      p, role:devops, projects, get, *, allow
      p, role:devops, repositories, get, *, allow
      p, role:devops, clusters, get, *, allow

      # map users to roles
      g, devops, role:devops
      g, auditor, role:readonly
```

| Config                           | Meaning                                        |
| -------------------------------- | ---------------------------------------------- |
| `accounts.devops: apiKey, login` | `devops` can log in and generate API tokens    |
| `accounts.auditor: login`        | `auditor` can log in only                      |
| `policy.default: role:readonly`  | Default authenticated users are read-only      |
| `g, devops, role:devops`         | Maps `devops` user to custom `devops` role     |
| `g, auditor, role:readonly`      | Maps `auditor` user to built-in read-only role |

- Apply

```sh
helm upgrade --install argocd argo/argo-cd \
  -n argocd \
  --create-namespace \
  -f argocd-account-lab-values.yaml

# confirm with cm
kubectl -n argocd get cm argocd-cm -o yaml
# apiVersion: v1
# data:
#   accounts.auditor: login
#   accounts.devops: apiKey, login

# confirm with rbac
kubectl -n argocd get cm argocd-rbac-cm -o yaml
# apiVersion: v1
# data:
#   policy.csv: |
#     # devops role
#     p, role:devops, applications, get, */*, allow
#     p, role:devops, applications, create, */*, allow
#     p, role:devops, applications, update, */*, allow
#     p, role:devops, applications, delete, */*, allow
#     p, role:devops, applications, sync, */*, 
# ...
```

- admin

```sh
# login as admin
argocd login localhost:8080 --username admin --insecure
# Password:
# 'admin:login' logged in successfully
# Context 'localhost:8080' updated

# confirm account
argocd account list
# NAME     ENABLED  CAPABILITIES
# admin    true     login
# auditor  true     login
# devops   true     apiKey, login

# update pwd
argocd account update-password \
  --account devops \
  --current-password <ADMIN_PASSWORD> \
  --new-password <DEVOPS_PASSWORD>

# Password updated

argocd account update-password \
  --account auditor \
  --current-password <ADMIN_PASSWORD> \
  --new-password <DEVOPS_PASSWORD>

# Password updated

argocd logout localhost:8080
# Logged out from 'localhost:8080'
```

---

### Test with new Accounts

- Audi

```sh
# login
argocd login localhost:8080 \
  --username auditor \
  --password '<AUDITOR_PASSWORD>' \
  --insecure

# 'auditor:login' logged in successfully
# Context 'localhost:8080' updated

# list app as audit
argocd app list
# NAME  CLUSTER  NAMESPACE  PROJECT  STATUS  HEALTH  SYNCPOLICY  CONDITIONS  REPO  PATH  TARGET

# test permission
argocd account can-i get applications '*/*'
# yes
argocd account can-i sync applications '*/*'
# no
```

- Devops

```sh
argocd login localhost:8080 \
  --username devops

# 'devops:login' logged in successfully
# Context 'localhost:8080' updated

# test permission
argocd account can-i get applications '*/*'
# yes
argocd account can-i sync applications '*/*'
# yes
argocd account can-i update applications '*/*'
# yes



```