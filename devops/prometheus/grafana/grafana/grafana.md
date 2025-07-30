# Prometheus - Grafana

[Back](../../index.md)

- [Prometheus - Grafana](#prometheus---grafana)
  - [Grafana](#grafana)
  - [Configuration](#configuration)

---

## Grafana

- `Grafana Cloud`:
  - a fully managed cloud-hosted observability platform
  - Metrcis, logs and traces

---

## Configuration

- CF path: `/etc/grafana`

  - default cf: `/etc/grafana/grafana.ini`

- Good practices: backup default cf

```sh
ls /etc/grafana -lh
total 96K
-rw-r----- 1 root grafana  85K Jul 30 15:32 grafana.ini
-rw-r----- 1 root grafana 3.1K Jul 30 15:32 ldap.toml
drwxr-xr-x 7 root grafana 4.0K Jul 30 15:32 provisioning

# backup cf
sudo cp /etc/grafana/grafana.ini /etc/grafana/grafana.ini.bak
```
