# Kubernetes - KubeConfig

[Back](../index.md)

- [Kubernetes - KubeConfig](#kubernetes---kubeconfig)
  - [KubeConfig](#kubeconfig)
  - [Declarative method](#declarative-method)
  - [Imperative Commands](#imperative-commands)

---

## KubeConfig

- `kubeconfig file`

  - the configuration file used by `kubectl`, **client libraries**, and **automation tools** to **connect** to a Kubernetes cluster.
  - primarily used by the `kubectl` command-line tool to authenticate and interact with a Kubernetes cluster's `API server`.
  - used to specify which the user starts the connection with what cluster.

- Default path: `$HOME/.kube/config`.

  - can specify a different location using the `--kubeconfig` flag or the `KUBECONFIG` environment variable.
  - Order of precedence (highest → lowest):
    - `--kubeconfig` flag
    - `$KUBECONFIG` environment variable
    - `~/.kube/config`

- 3 sections:

  - **Clusters**:
    - Defines the details of the Kubernetes clusters to access
    - `certificate-authority-data` / `certificate-authority`:
      - The **CA certificate** data or path to the file containing it, used to **verify the API server's authenticity**.
    - `server`:
      - The URL of the Kubernetes API server.
    - `name`:
      - A unique name for the cluster.
  - **Users**:
    - Defines the **authentication credentials** for users interacting with the clusters
    - `client-certificate-data`/`client-certificate`:
      - The **client certificate** data or path to the file containing it.
    - `client-key-data` / `client-key`:
      - The client **key data** or path to the file containing it.
    - `token`:
      - An authentication token.
    - `name`:
      - A unique name for the user.
  - **Contexts**:
    - **Links a specific user** to a **specific cluster** and optionally a **namespace**, defining a particular **access environment**.
    - Each context includes:
      - `cluster`: The name of the cluster to use.
      - `user`: The name of the user to authenticate with.
      - `namespace` (optional): The default namespace to use for commands.
      - `name`: A unique name for the context.

- Purpose and Usage:

  - **Authentication and Authorization**:
    - It provides the **necessary credentials** for kubectl to authenticate with the Kubernetes API server and perform authorized actions.
  - **Managing Multiple Clusters**:
    - A **single** kubeconfig file can **define access to multiple** Kubernetes clusters, allowing users to easily switch between them using kubectl config use-context.
  - **Organizing Access**:
    - It helps organize cluster access information, making it easier for administrators and developers to manage and interact with various Kubernetes environments.

---

- Example:

```sh
# access api server via url with cert and key
curl https://my-kube-playground:6443/api/v1/pods \
--key admin.key
--cert admin.crt
--cacert ca.crt

# issue kubectl command with cert and key
kubectl get pods --server my-kube-playground:6443 --client-key admin.key --client-certificate admin.crt --certificate-authority ca.crt
```

- The cert and key can be organize with a kubefig file, making it easy for authentication

```sh
tee config fiel<<EOF
--server my-kube-playground:6443
--client-key admin.key
--client-certificate admin.crt
--certificate-authority ca.crt
EOF

kubectl get pods --kubeconfig config
```

---

## Declarative method

- Example

```yaml
apiVersion: v1
kind: Config
# define default context
current-context: my-kube-admin@my-kube
clusters:
  - name: my-kube
    cluster:
      # can be a full path
      certificate-authority: /etc/kubernetes/pki/ca.crt
      # can be the base64 code
      certificate-authority-data: base64_code
      server: https://my-kube:6443

contexts:
  - name: my-kube-admin@my-kube
    context:
      cluster: my-kube
      user: my-kube-admin
      # option: specify a ns
      namespace: dev

users:
  - name: my-kube-admin
    user:
      client-certificate: admin.crt
      client-key: admin.key
```

---

## Imperative Commands

| **CMD**                                                                                | **DESC**                                              |
| -------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `kubectl config get-contexts`                                                          | List all contexts in the kubeconfig.                  |
| `kubectl config current-context`                                                       | Show the currently active context.                    |
| `kubectl config view`                                                                  | View the default kubeconfig.                          |
| `kubectl config use-context context_name`                                              | Switch to a specific context.                         |
| `kubectl config set-context <name> --cluster=<c> --user=<u> --namespace=<ns>`          | Create or update a context.                           |
| `kubectl config set-context --current --namespace=<ns>`                                | Change the default namespace for the current context. |
| `kubectl config delete-context <ctx>`                                                  | Remove a context from kubeconfig.                     |
| `kubectl config set-cluster <name> --server=<url> --certificate-authority=<file>`      | Add or modify a cluster entry.                        |
| `kubectl config delete-cluster <name>`                                                 | Delete a cluster entry.                               |
| `kubectl config set-credentials <name> --client-certificate=<cert> --client-key=<key>` | Add or update user credentials.                       |
| `kubectl config delete-user <name>`                                                    | Delete a user entry.                                  |
| `kubectl config rename-context <old> <new>`                                            | Rename a context.                                     |
| `kubectl config unset <key>`                                                           | Remove a specific property (advanced).                |
| `kubectl config set <key> <value>`                                                     | Set arbitrary kubeconfig fields (advanced).           |
| `kubectl config view --merge --flatten > ~/.kube/config`                               | Permanently merge multiple kubeconfig files.          |

---

```sh
# specify and persist a custom config file
echo 'export KUBECONFIG=/root/my-kube-config' >> ~/.bashrc
source ~/.bashrc

# confirm
echo $KUBECONFIG
# view default config
kubectl config view
```
