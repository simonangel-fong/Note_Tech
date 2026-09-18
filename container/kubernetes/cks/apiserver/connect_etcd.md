# CKS - API Server: connect with etd

[Back](../../index.md)

- [CKS - API Server: connect with etd](#cks---api-server-connect-with-etd)
  - [Connect with etcd](#connect-with-etcd)
    - [Configuration Workflow](#configuration-workflow)
  - [Lab](#lab)

---

## Connect with etcd

- etcd requires:
  - Listen on HTTPS
  - Certificate Authentication Required

- therefore, connection between api server and etcd requires Certificate

### Configuration Workflow

- **Generate certificates** for API Server from trusted Certificate Authority
- API Server should connect to etcd over **HTTPS endpoint**

---

## Lab

```sh

```