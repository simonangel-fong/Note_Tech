# GitHub Actions: Fundamental

[Back](../index.md)

- [GitHub Actions: Fundamental](#github-actions-fundamental)
  - [Components](#components)
  - [Events](#events)
    - [Event Filters](#event-filters)
    - [Activity Types](#activity-types)
  - [Runners](#runners)
  - [Actions](#actions)
    - [GitHub Marketplace](#github-marketplace)
  - [Contexts](#contexts)
  - [Expressions \& Variables](#expressions--variables)
  - [Functions](#functions)
  - [Inputs](#inputs)
    - [Lab: Control Build-deploy flow by inputs](#lab-control-build-deploy-flow-by-inputs)
  - [Outputs](#outputs)
    - [Lab: output](#lab-output)

---

- ref:
  - https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

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

### Event Filters

- `Event Filters`
  - Specify under which **conditions** a specific event triggers our workflow
  - If **multiple** filters are specified, **all** of them **must be satisfied** for the workflow to run!

- `push` event
  - `branches`:
    - Specifies which **branches must match** in order for the workflow to execute
  - `branches_ignore`:
    - Specifies which branches must not match in order for the workflow to execute
  - `tags`
  - `tags_ignore`
  - `paths`
  - `paths_ignore`

- Example:

```yaml
on:
  push:
  branches:
    - main
    - "releases/**"
  paths-ignore:
    - "docs/**"
```

---

### Activity Types

- `Activity Types`:
  - Specify which **types of certain triggers** execute our workflow

- `pull_request` event
  - ref: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request
  - `opened`
    - Runs the workflow whenever a **PR is opened**.
  - `synchronize`
    - Runs the workflow whenever a **new commit is pushed to the HEAD ref of the PR.**
  - `closed`
  - `assigned`
  - `labeled`
  - `edited`

- Example

```yaml
on:
  pull_request:
    types: [opened, synchronize]
    branches:
      - main
      - 'releases/**
```

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

---

## Actions

- `Actions`:
  - pre-defined, reusable unit of code that performs a specific, complex, but repetitive task within a GitHub Actions workflow.
  - the smallest building block of a workflow.

- benefits:
  - **Reduces Repetition**
  - **Reusable Extension**: Acts as a plugin
  - **Interacts with APIs**: Actions can interact with the GitHub API or any other public API to perform tasks like sending Slack notifications or creating Jira tickets.

- syntax:

```sh
- uses: {owner}/{repo}@{ref}
  with:
    param: value
```

- `actions/` pre-fix:
  - official actions released by github

- Common actions:
  - `actions/checkout`
  - `actions/setup-node`

---

### GitHub Marketplace

- `GitHub Marketplace`
  - a ce**ntral platform for discovering and sharing pre-built tools** to automate software development workflows.
  - two types of extensions:
    - `GitHub Actions`
    - `GitHub Apps`

---

## Contexts

- `Contexts`:
  - ref: https://docs.github.com/en/actions/reference/workflows-and-actions/contexts
  - objects that allow you to **access information about workflow runs, runner environments, jobs, and steps**

- Syntax: `${{ <context> }}`

- Common Context

| Context               | Description                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `github`              | metadata about the workflow run, the repository, and the specific event that triggered the run.                         |
| `env`                 | variables that have been defined in a workflow, job, or step.                                                           |
| `secrets`             | sensitive data like API keys or tokens, which are automatically masked in the logs.                                     |
| `vars`                | variables defined at the organization, repository, or environment level.                                                |
| `job` / `jobs`        | the current job info; jobs (for reusable workflows) provides outputs from other jobs in that workflow.                  |
| `steps`               | information and outputs from steps that have already completed in the current job.                                      |
| `runner`              | Includes details about the machine executing the job, such as the operating system (runner.os).                         |
| `matrix` / `strategy` | Used in matrix builds to access properties of the current iteration                                                     |
| `needs`               | dependencies for the current job.                                                                                       |
| `inputs`              | input properties passed via the keyword with to an action, to a reusable workflow, or to a manually triggered workflow. |
|                       |

---

```yaml
name: 06 - Context
run-name: my run name ${{ github.event_name }} | DEBUG - ${{ inputs.debug }}

on:
  push:
  workflow_dispatch:
    inputs:
      debug:
        type: boolean
        default: false

env:
  MY_WORKFLOW_ENV: "workflow"
  MY_OVERWRITTEN_ENV: "workflow"

jobs:
  echo-context:
    runs-on: ubuntu-latest
    env:
      MY_JOB_ENV: "job"
      MY_OVERWRITTEN_ENV: "job"
    steps:
      - name: Display github info
        run: |
          echo "Event Name: ${{ github.event_name }}"
          echo "ref: ${{ github.ref }}"
          echo "SHA: ${{ github.sha }}"
          echo "Actor: ${{ github.actor }}"
          echo "Workflow: ${{ github.workflow }}"
          echo "Run ID: ${{ github.run_id }}"
          echo "Run number: ${{ github.run_number }}"

      - name: Display variable
        run: |
          echo "Variable value: ${{ vars.MY_VAR }}"

      - name: Print env
        env:
          MY_OVERWRITTEN_ENV: "step"
        run: |
          echo "my workflow env: ${{env.MY_WORKFLOW_ENV}}"
          echo "my job env: ${{env.MY_JOB_ENV}}"
          echo "my overwritten env: ${{env.MY_OVERWRITTEN_ENV}}"

      - name: Print env
        run: |
          echo "my workflow env: ${{env.MY_WORKFLOW_ENV}}"
          echo "my job env: ${{env.MY_JOB_ENV}}"
          echo "my overwritten env: ${{env.MY_OVERWRITTEN_ENV}}"

  echo-context-2:
    runs-on: ubuntu-latest
    steps:
      - name: Print workflow env
        run: |
          echo "workflow: $MY_WORKFLOW_ENV"
          echo "Overwritten: $MY_OVERWRITTEN_ENV"
```

---

## Expressions & Variables

- `Expressions`:
  - Use dynamic values and expressions in your workflows

- Syntax:
  - `${{ <expression> }}`

- Can be any combination of:
  - **Literal values**:
    - Strings, numbers, booleans, null.
  - **Context values**：
    - Values passed via the many workflow contexts.
  - **Functions**
    - Built-in functions provided by GitHub Actions.

- Support the use of functions and operators such as `!`, `<`, `>`, `!=`, `.&`, `.|`, and many others.

- Example:
  - `if: ${{ github.event_name == "push" }}`
  - `MY_ENV: ${{ vars.MY_VAR && 'my_var' || 'no_var' }}`
  - `MY_ENV: ${{ vars.MY_VAR || 'default_value' }}`

---

- `Variables`
  - Set and reuse non-sensitive configuration information

- Variable level:
  - lower level override the upper level

- Single workflow
  - workflow
  - job
  - step

- Multiple workflows
  - organization
  - repository
  - environment

---

## Functions

- `Functions`
  - ref: https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#functions
  - Out-of-the-box functions to model complex behavior

- Common Functions:
  - `contains()`
  - `startsWith()`
  - `endsWith()`
  - `fromJSON()`
  - `toJSON()`
  - `success()`
  - `failure()`
  - `always()`
  - `cancelled()`

- Example

```yaml
name: 09 - function

on:
  pull_request:
  workflow_dispatch:

jobs:
  echo1:
    runs-on: ubuntu-latest
    steps:
      - name: Print PR title
        run: echo ${{ github.event.pull_request.title }}

      - name: print PR labels
        run: |
          cat <<EOF
              ${{ toJson(github.event.pull_request.labels )}}
          EOF

      - name: Bug step
        if: ${{ !cancelled() && contains(github.event.pull_request.title,'fix')  }}
        run: echo "bug fixed"

      - name: Sleep for 20 seconds
        run: sleep 20

      - name: Failing step
        run: exit 1

      - name: step when success
        if: ${{ success() }}
        run: echo "Execute only when success"

      - name: step when failure
        if: ${{ failure() }}
        run: echo "Execute only when failure"

      - name: step when cancel
        if: ${{ cancelled() }}
        run: echo "Execute only when cancelled"

      - name: step when not cancel
        if: ${{ !cancelled() }}
        run: echo "Execute only when not cancelled"
```

---

## Inputs

- `Inputs`
  - Provide information to customize workflows and actions
  - enable to **request specific information** from the workflow or action caller and use this information at runtime.

- Inputs must be defined in the definition of `reusable workflows` or `custom actions` so that they can be correctly used.

- Define inputs:

```yaml
inputs:
  url:
    description: "..."
    required: true
  max-trials:
    description: "..."
    required: false
    default: "60"
```

- Call inputs

```yaml
jobs:
  job1:
    steps:
      - name: Ping URL
        uses: ping-url-example@v1
        with:
          url: https:./www.google.com
          max-trials: 10
```

---

### Lab: Control Build-deploy flow by inputs

```yaml
name: 11 - Inputs

on:
  workflow_dispatch:
    inputs:
      dry-run:
        type: boolean
        description: Skip deployment and only print build output
        default: false
      target:
        type: environment
        required: true
        description: Specify the target environment
      tag:
        type: choice
        options:
          - v1
          - v2
          - v3
        default: v3
        description: The release to build
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: echo "Building from tag ${{ inputs.tag }}"

  deploy:
    runs-on: ubuntu-latest
    if: ${{ !inputs.dry-run }}
    needs: build
    environment: ${{ inputs.target }}
    steps:
      - name: Deploy
        run: echo "Deploy to ${{ inputs.target }}"
```

---

## Outputs

- Output data from jobs for later usage

1. Set step id
2. pass key-value pair to `$GITHUB_OUTPUT` variable
3. Specify key and value in the `outputs` key
4. refer to outputs by `needs.<job-id>.outputs.<key-name>`


- Example

```yaml
jobs:
  welcome:
    runs-on: ubuntu-latest
    outputs:
      name: ${{ steps.step1.outputs.NAME }}
    steps:
      - id: step1
        run: echo "NAME=Lauro" >> "$GITHUB_OUTPUT"
  goodbye:
    runs-on: ubuntu-latest
    needs: welcome
    steps:
      - run: echo "Bye, ${{ needs.welcome.outputs.name }}"
```

---

### Lab: output

```yaml
name: 12 - Outputs

on:
    workflow_dispatch:
        inputs:
            build-status:
                type: choice
                options:
                    - success
                    - failure
                default: success

jobs:
    build:
        runs-on: ubuntu-latest
        outputs:
            build-status: ${{ steps.build.outputs.status }}
        steps:
            - name: Print GITHUB_OUTPUT path
              run: echo "$GITHUB_OUTPUT"

            - name: Build
              id: build
              run: echo "status=${{ inputs.build-status }}" >> "$GITHUB_OUTPUT"
            
            - name: Pass multiple k-v github_output, and Accidentally remove
              run: |
                echo "key1=val1" >> "$GITHUB_OUTPUT"
                echo "key2=val2" >> "$GITHUB_OUTPUT"
                cat "$GITHUB_OUTPUT"

                echo "key3=val3" > "$GITHUB_OUTPUT"
                cat "$GITHUB_OUTPUT"

    deploy:
        runs-on: ubuntu-latest
        needs: build
        if: ${{ needs.build.outputs.build-status == 'success' }}
        steps:
            - name: Deploy
              run: echo "Deploying"

```
> GITHUB_OUTPUT path: /home/runner/work/_temp/_runner_file_commands/set_output_uuid
> they are the files different across steps, that is why it needs to specify the step id in the outputs key