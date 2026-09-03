# Encryption at rest

- https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/

### Encryption at rest

etcd stores Secrets base64-encoded, not encrypted. This config encrypts them
on write -- a named CKS objective.

```sh
ENCRYPTION_KEY=$(head -c 32 /dev/urandom | base64)

cat <<EOF | sudo tee /etc/kubernetes/config/encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: ${ENCRYPTION_KEY}
      - identity: {}
EOF

sudo chmod 600 /etc/kubernetes/config/encryption-config.yaml
```

Provider order matters: `aescbc` first means new writes are encrypted;
`identity` last lets already-plaintext values still be read. Note the heredoc
delimiter here is **unquoted** (`<<EOF`) so `${ENCRYPTION_KEY}` expands -- a
quoted `<<'EOF'` writes the literal string and every Secret write then fails.

---
