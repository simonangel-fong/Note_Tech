# Kubernetes: Container - Startup Probe

[Back](../../index.md)

- [Kubernetes: Container - Startup Probe](#kubernetes-container---startup-probe)
  - [Startup Probe](#startup-probe)
    - [Manifest file](#manifest-file)
  - [Best Pracices](#best-pracices)

---

## Startup Probe

- `startup probe`

  - used to balance between:
    - the requirment that application takes too long to start
    - the negative effect on the normal operation of the application caused by the high result of `periodSeconds` \* `failureThreshold`,
  - If a `startup probe` is **defined** for a `container`, **only** the `startup probe` is **executed** when the container is **started**.
    - When the `startup probe` **succeeds**, Kubernetes **switches** to using the `liveness probe`, which is configured to quickly detect when the application becomes unhealthy.
  - work with `liveness probe`
    - **long period** `startup probe`: allow time-consumed startup
    - **short period** `liveness probe`: allow faster detection

- 3 types of the `startup probe`:

  - `exec`
  - `tcpSocket`
  - `httpGet`

### Manifest file

- startup probe + liveness probe

```yaml
spec:
  containers:
    - name: con_name
      startupProbe:
        httpGet:
          path: /
          port: http
        periodSeconds: 10
        failureThreshold: 12
      livenessProbe:
        httpGet:
          path: /
          port: http
        periodSeconds: 5
        failureThreshold: 2
```

---

## Best Pracices

- To provide a better `liveness check`, web applications typically **expose a specific health-check endpoint**, such as `/healthz`.

  - When this endpoint is called, the application performs an **internal status check** of all the major components running within the application to ensure that none of them have died or are no longer doing what they should.

- Make sure that the `/healthz` HTTP endpoint doesn’t require **authentication** or the **probe** will always **fail**, causing your container to be restarted continuously

- Make sure that the application **checks only the operation of its internal components** and nothing that is **influenced by an external factor**.

  - For example, the health-check endpoint of a **frontend** service should never respond with failure when it can’t connect to a backend service.

- The handler invoked by a `liveness probe` **shouldn’t** use too much **computing resources** and shouldn’t take too **long** to complete.

  - By default, probes are executed relatively often and only given one second to complete.
  - e.g., use an `HTTP GET probe` instead of an `exec liveness probe` that **starts an entire JVM**.

- Dont set the `failureThreshold` field to a **higher value** so that the probe must fail several times before the application is considered unhealthy.

---
