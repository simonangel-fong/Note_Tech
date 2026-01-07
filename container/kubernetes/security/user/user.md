# Kubernetes - User

[Back](../../index.md)

- [Kubernetes - User](#kubernetes---user)
  - [Users in Kubernetes](#users-in-kubernetes)
    - [Normal Users](#normal-users)
    - [Service Accounts](#service-accounts)

---

## Users in Kubernetes

- All Kubernetes clusters have two categories of users:

  - `service accounts` managed by Kubernetes
  - `normal users`

- **API requests** are
  - **tied to**
    - either a `normal user`
    - or a `service account`,
  - or are treated as **anonymous requests**.

---

### Normal Users

- Kubernetes **does not have objects** which represent `normal user` accounts.

  - `Normal users` **cannot be added** to a cluster **through an API call**.

- `normal users` are managed in the ways:

  - an **administrator** distributing private keys
  - a `user store` like Keystone or Google Accounts
  - a `file` with a list of usernames and passwords

- any `user` that presents a **valid certificate signed by the cluster's `certificate authority (CA)`** is considered normal.
  - `username` is determined from the **common name field** in the **'subject'** of the cert (e.g., "/CN=bob").
  - `role based access control (RBAC)` sub-system would determine whether the user is **authorized** to perform a specific **operation** on a resource.

---

### Service Accounts

- `Service Accounts`
  - the users **managed by the Kubernetes API**.
  - **bound** to specific `namespaces`, and **created** automatically by the API server or manually **through API calls**.
  - tied to a set of **credentials** stored as `Secrets`, which are **mounted into pods** allowing in-cluster `processes` to talk to the `Kubernetes API`.
