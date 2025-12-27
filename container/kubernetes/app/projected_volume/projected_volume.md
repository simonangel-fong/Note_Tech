# Kubernetes - Pod: Projected Volumes

[Back](../../index.md)

- [Kubernetes - Pod: Projected Volumes](#kubernetes---pod-projected-volumes)
  - [Projected Volumes](#projected-volumes)
  - [Lab: Prodjected Volume](#lab-prodjected-volume)

---

## Projected Volumes

- solve the limitations:

  - **can't** inject the files from these **different sources**, or even multiple sources of the same type, into the same file directory.
  - the `subPath` field allows to inject individual files from **multiple volumes**, it **prevents** the files from being **updated** when the source values change.

- `Projected volumes`

  - allow to **combine** information **from multiple** `config maps`, `secrets`, and the `Downward API` into a **single** `pod volume` that can then be mounted in the pod’s containers.

- field: `pod.spec.volumes.projected`
  - configmap: `pod.spec.volumes.projected.sources.configMap`
  - secret: `pod.spec.volumes.projected.sources.secret`

---

## Lab: Prodjected Volume

```yaml
# demo-projected-volume.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-projected-volume
  labels:
    os: busybox
spec:
  volumes:
    - name: projected-volume
      projected:
        sources:
          - configMap:
              name: configmap-env-bulk
          - configMap:
              name: configmap-env-key
              items:
                - key: KEY_C
                  path: key_c
                - key: KEY_D
                  path: KEY_D
          - configMap:
              name: configmap-file-key
              items:
                - key: index.html
                  path: index.html
          - secret:
              name: secret-env-bulk
          - secret:
              name: secret-env-key
              items:
                - key: secret3
                  path: secret3
                - key: secret4
                  path: secret4
          - downwardAPI:
              items:
                - path: pod_name
                  fieldRef:
                    fieldPath: metadata.name
                - path: "cpu_request"
                  resourceFieldRef:
                    containerName: busybox
                    resource: requests.cpu
                    divisor: 1m
                - path: "cpu_limit"
                  resourceFieldRef:
                    containerName: busybox
                    resource: limits.cpu
                    divisor: 1m
  containers:
    - name: busybox
      image: busybox
      resources:
        requests:
          cpu: "250m"
          memory: "100Mi"
        limits:
          cpu: "500m"
          memory: "200Mi"
      volumeMounts:
        - name: projected-volume
          mountPath: /projected-volume
      command:
        - sh
      args:
        - "-c"
        - |
          echo "configMap configmap-env-bulk key_a: $(cat /projected-volume/key_a)"
          echo "configMap configmap-env-bulk key_b: $(cat /projected-volume/key_b)"
          echo "configMap configmap-env-key KEY_C: $(cat /projected-volume/key_c)"
          echo "configMap configmap-env-key KEY_D: $(cat /projected-volume/KEY_D)"
          echo "configMap configmap-file-key index.html: $(cat /projected-volume/index.html)"

          echo "secret secret-env-bulk secret1: $(cat /projected-volume/secret1)"
          echo "secret secret-env-bulk secret2: $(cat /projected-volume/secret2)"
          echo "secret secret-env-key secret3: $(cat /projected-volume/secret3)"
          echo "secret secret-env-key secret4: $(cat /projected-volume/secret4)"

          echo "downward api pod_name: $(cat /projected-volume/pod_name)"
          echo "downward api cpu_request: $(cat /projected-volume/cpu_request)"
          echo "downward api cpu_limit: $(cat /projected-volume/cpu_limit)"

          sleep 500
```

```sh
# cm: configMap-env-bulk
kubectl create configmap configmap-env-bulk --from-literal=key_a="var a" --from-literal=key_b="var b"
# configmap/configmap-env-bulk created

# cm: configMap-env-key
kubectl create configmap configmap-env-key --from-literal=KEY_C="var c" --from-literal=KEY_D="var d"
# configmap/configmap-env-key created

# cm: configMap-file-key
kubectl create configmap configmap-file-key --from-file=index.html --from-file=error.html
# configmap/configmap-file-key created

# cm: secret-env-bulk
kubectl create secret generic secret-env-bulk --from-literal=secret1=secret1 --from-literal=secret2=secret2
# secret/secret-env-bulk created

# cm: secret-env-key
kubectl create secret generic secret-env-key --from-literal=secret3=secret3 --from-literal=secret4=secret4
# secret/secret-env-key created

kubectl apply -f demo-projected-volume.yaml
# pod/demo-projected-volume created

# confirm log
kubectl logs pod/demo-projected-volume
# configMap configmap-env-bulk key_a: var a
# configMap configmap-env-bulk key_b: var b
# configMap configmap-env-key KEY_C: var c
# configMap configmap-env-key KEY_D: var d
# configMap configmap-file-key index.html: <html>
# <title>Home</title>
# <body>
# <h1> Home </h1>
# <p> This is home page </p>
# </body>
# </html>
# secret secret-env-bulk secret1: secret1
# secret secret-env-bulk secret2: secret2
# secret secret-env-key secret3: secret3
# secret secret-env-key secret4: secret4
# downward api pod_name: demo-projected-volume
# downward api cpu_request: 250
# downward api cpu_limit: 500
```
