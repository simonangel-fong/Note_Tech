# GitHub Actions: Fundamental

[Back](../index.md)

- [GitHub Actions: Fundamental](#github-actions-fundamental)
  - [Components](#components)
  - [Events](#events)
  - [Runners](#runners)

---

## Components

- `Workflows`:
  - a configurable **automated process** that runs one or more jobs to **automate tasks** throughout your software development lifecycle
  - defined at the **repository level**
  - Define which `triggers` actually start the workflow
  - composed of one or more jobs
- `Jobs`:
  - a set of `steps` in a `workflow` that executes **on the same `runner`**.
  - defined at the **workflow level**
  - Define **in which execution environment** they are run
  - composed of one or more steps
  - Run in **parallel by default**
- `Runner`:
  - the **server or virtual machine (VM)** that executes the `jobs` defined in workflow.
- `Steps`:
  - defined at the **job level**
  - Define the **actual script** or `GitHub Action` that will be **executed**
  - Run **sequentially by default**
- `GitHub action`
  - the **smallest building blocks** used within a job's `steps`.
  - a **standalone, reusable application** that performs a specific complex task.

- `.github/`
  - a **special configuration folder** at the **root** of a GitHub repository used to store GitHub-specific automation
- `.github/workflows/`:
  - subdirectory for Actions workflow configuration files
  - in `.yml` or `.yaml` format

---

- Example:

```yaml
name: 01 - Building Block

on: push

jobs:
  echo-hello:
    runs-on: ubuntu-latest
    steps:
      - name: say hello
        run: |
          echo "hello world"
  echo-bye:
    runs-on: ubuntu-latest
    steps:
      - name: fails
        run: |
          echo "will fail"
          exit 1
      - name: say bye
        run: echo "Bye"
```

---

## Events

- `Workflow events`:
  - specific activities that **trigger the execution** of a workflow.

- Repository Events:
  - `push`
    - Triggered when someone pushes to the repo
  - `issues`
    - Triggered by a variety of events related to issues
  - `pull_request`:
    - Triggered by a variety of events related to **PRs**
  - `pull_request_review`
    - Triggered by a variety of events related to **PR reviews** (submitting, editing, deleting)
  - `fork`
    - Triggered when your repository is fork
- Schedule
  - Runs as a cron job
    - Minimal interval: 5min
- Manual trigger
  - Triggered via the UI
    - Triggered from the Actions tab in GitHub
  - Triggered via an API call
    - Triggered via GitHub's REST API
  - Triggered from another workflow
    - Triggered from within another workflow

---

- Example

```yaml
name: 02 - workflow event

on:
  push:
  pull_request:
  schedule:
    - cron: "*/5 * * * *"
  workflow_dispatch:

jobs:
  echo:
    runs-on: ubuntu-latest
    steps:
      - name: Show trigger
        run: echo "triggerred by ${{github.event_name}}" # triggerred by push
```

> triggerred by push
> triggerred by workflow_dispatch
> triggerred by pull_request

---

## Runners

- `runner`:
  - Virtual servers that execute jobs from workflows

- Types:
  - **GitHub-hosted (standard)**
    - Managed service
    - A VM is scoped to a job:
      - **steps share the VM**, but jobs don't
      - by default, each job receives a clean VM instance

    - OS: windows / ubuntu
      - spec(cpu/memory/storage): 2 cores/7 GB/14 GB
    - OS: Mac
      - spec(cpu/memory/storage): 3 cores/14 GB/14 GB

  - **Self-hosted**
    - Run workflows on (almost) any **infrastructure** of your choice
    - Full control over the VM infrastructure
    - It's **not managed**, meaning we need to take care of OS patching, software updates, among other ops tasks
    - Can be added at the repository, organization, or enterprise level
    - Jobs do not necessarily have to run on clean instances
    - **Warning**
      - Do not use self-hosted runners in public repositories!

---

- Example:

```yaml
name: 03 - runner
on: push

jobs:
  echo-ubuntu:
    runs-on: ubuntu-latest
    steps:
      - name: show os
        run: |
          echo Runner: ${{runner.os}}
  echo-windows:
    runs-on: windows-latest
    steps:
      - name: show os
        # required in win
        shell: bash 
        run: |
          echo Runner: ${{runner.os}}
```
> Runner: Linux
> Runner: Windows