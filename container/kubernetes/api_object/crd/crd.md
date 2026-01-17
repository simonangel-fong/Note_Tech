# Kubernetes - Custom Resource Definition(CRD)

[Back](../../index.md)

- [Kubernetes - Custom Resource Definition(CRD)](#kubernetes---custom-resource-definitioncrd)
  - [Custom Resource Definition(CRD)](#custom-resource-definitioncrd)
  - [Custom Controller](#custom-controller)
  - [Operator Framework](#operator-framework)
    - [Imperative Commands](#imperative-commands)
  - [Lab: Create CRD](#lab-create-crd)

---

## Custom Resource Definition(CRD)

- custom resource
- custom controller
- CRD

- Example: CRD

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: flighttickets.com
spec:
  # if a namespaced object
  scope: Namespaced
  # group in the apiVersion section
  group: flight.com
  names:
    # resouce kind
    kind: FlightTicket
    # singular name
    singular: flightticket
    # plural name; used by API server, e.g., k api-resources
    plural: flightticket
    # short version name:
    shortNames:
      - ft
  versions:
    # version name in the apiVersion section
    - name: v1
      served: true
      storage: true
      # the parameters can be define in the spec section
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                from:
                  type: string
                to:
                  type: string
                number:
                  type: integer
                  minimum: 1
                  maximum: 10
      selectableFields:
        - jsonPath: .spec.from
        - jsonPath: .spec.to
        - jsonPath: .spec.number
      additionalPrinterColumns:
        - jsonPath: .spec.from
          name: From
          type: string
        - jsonPath: .spec.to
          name: To
          type: string
        - jsonPath: .spec.number
          name: Number
          type: integer
```

- Example of creating a flight ticket object

```yaml
apiVersion: flights.com/v1
kind: FlightTicket
metadata:
  name: my-ticket
spec:
  from: London
  to: Paris
  number: 2
```

- can be managed
  - get, delete, describe

---

## Custom Controller

- role

  - monitor the data in ETCD
  - implement based on the data change

- code in go

---

## Operator Framework

- used to pack both crd and custom controller
- OperatorHub.io

---

### Imperative Commands

|
k get crd

---

## Lab: Create CRD

```yaml
# crd-crontab.yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.stable.example.com
spec:
  group: stable.example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                cronSpec:
                  type: string
                image:
                  type: string
                replicas:
                  type: integer
  scope: Namespaced
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
    shortNames:
      - ct
```

```sh
kubectl apply -f crd-crontab.yaml
# customresourcedefinition.apiextensions.k8s.io/crontabs.stable.example.com created

kubectl get crd
# NAME                          CREATED AT
# crontabs.stable.example.com   2026-01-16T03:22:35Z
```

```yaml
# my-crontab.yaml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  name: my-new-cron-object
spec:
  cronSpec: "* * * * */5"
  image: my-awesome-cron-image
  replicas: 3
```

```sh
kubectl apply -f my-crontab.yaml
# crontab.stable.example.com/my-new-cron-object created

kubectl get ct
# NAME                 AGE
# my-new-cron-object   48s
```
