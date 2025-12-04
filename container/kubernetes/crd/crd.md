# Kubernetes - Custom Resource Definition(CRD)

[Back](../index.md)

- [Kubernetes - Custom Resource Definition(CRD)](#kubernetes---custom-resource-definitioncrd)
  - [Custom Resource Definition(CRD)](#custom-resource-definitioncrd)
  - [Custom Controller](#custom-controller)
  - [Operator Framework](#operator-framework)

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
