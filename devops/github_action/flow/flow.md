# GitHub Actions: Execution Flow

[Back](../index.md)

- [GitHub Actions: Execution Flow](#github-actions-execution-flow)
  - [Control Execution Flow](#control-execution-flow)
    - [Step Execution](#step-execution)
    - [Job Execution](#job-execution)
  - [Lab: Control Execution Flow](#lab-control-execution-flow)

---

## Control Execution Flow

### Step Execution

- Standard execution:
  - step 1 > step 2(fail) > step 3(not execute)
- Conditional execution
  - step 1 > step 2(fail) > step 3 if: ${{ !cancelled() }}(execute)

---

### Job Execution

- `needs` key
- `continue-on-error` key: true/false

- Non-dependent execution: executed in parallel
  - jobs:
    - job1:
    - job2:
    - job3:
    - job4:

- Dependent execution
  - jobs:
    - job1:
    - job2:
    - job3:
      - needs:
        - job1
        - job2
    - job4:
      - needs:
        - job1

---

## Lab: Control Execution Flow

```yaml
name: 10 - Execution Flow

on:
  workflow_dispatch:
    inputs:
      pass-unit-test:
        type: boolean
        description: whether unit tests pass
        default: true

jobs:
  lint-build:
    runs-on: ubuntu-latest
    steps:
      - name: lint and build
        run: echo "Lint and build"

  unit-test:
    runs-on: ubuntu-latest
    # continue-on-error: true
    steps:
      - name: unit test
        run: echo "running unit test"
      - name: failing tests
        if: ${{ !inputs.pass-unit-test }}
        run: exit 1
  deploy-stage:
    runs-on: ubuntu-latest
    needs:
      - lint-build
      - unit-test
    steps:
      - name: Deploy stage
        run: echo "Deploy stage"
  e2e-test:
    runs-on: ubuntu-latest
    needs:
      - deploy-stage
    steps:
      - name: end-to-end test
        run: echo "e2e test"
  load-test:
    runs-on: ubuntu-latest
    needs:
      - deploy-stage
    steps:
      - name: load test
        run: echo "load test"
  deploy-prod:
    runs-on: ubuntu-latest
    needs:
      - e2e-test
      - load-test
    steps:
      - name: deploy prod
        run: echo "deploy prod"
```

![pic](./flow.png)
