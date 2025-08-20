# Ansible - Collection

[Back](../ansible.md)

---

## Collection

- `collection`

  - a **distribution format** for Ansible content.
  - a bundle of related Ansible **roles**, **modules**, **plugins**, **playbooks**, and **documentation** that can be shared, versioned, and reused.

- Benefits:
  - **Packaging system**:
    - Collections group multiple Ansible **artifacts** (roles, modules, plugins, playbooks) **into one installable package**.
  - **Versioning**:
    - Each collection can have its own version (independent of Ansible core).
  - **Distribution**:
    - Collections are published and downloaded from Ansible Galaxy or private automation hubs.
  - **Namespace + Name**:
    - Collections are identified by `namespace.collection_name` (e.g., community.mysql).

---

### Install and use

```sh
ansible-galaxy collection install -r requirements.yaml  # install collection based on a requirement file
ansible-galaxy collection install amazon.aws

```

```yaml
- host: localhost
  collections:
    - amazon.aws

  tasks:
    - name: Create S3 bucket
      aws_s3_bucket:
        name: my-bucket
        region: us-west-1
```
