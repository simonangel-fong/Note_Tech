# Jenkins - Fundamental

[Back](../index.md)

- [Jenkins - Fundamental](#jenkins---fundamental)
  - [Fundamental](#fundamental)
    - [Items](#items)
    - [Build](#build)
  - [Architecture](#architecture)
  - [Core Components](#core-components)
    - [Jenkins Controller (Master)](#jenkins-controller-master)
    - [Jenkins Agents (Workers)](#jenkins-agents-workers)
    - [How It Works (Execution Flow)](#how-it-works-execution-flow)
    - [Common Deployment Patterns](#common-deployment-patterns)
    - [Plugins](#plugins)
  - [Common Configurations](#common-configurations)
    - [Environment Variables](#environment-variables)
    - [Jenkins URL](#jenkins-url)
    - [Notification](#notification)
  - [Common Practices](#common-practices)
    - [Blue-Green deployment strategy](#blue-green-deployment-strategy)
    - [Backup](#backup)

---

## Fundamental

- default path:
  - Windows: `C:\Program Files (x86)\Jenkins\`
  - Linux: `/var/lib/jenkins`

- Restart:
  - manually on control panel
  - cli: sudo systemctl restart jenkins

- Default **Port Number**: `8080`
- `Jenkins Build Executor`:
  - a **processing slot** on a build **agent (or controller)** that runs a single concurrent **build task**, effectively acting as a worker thread.

- `Jenkins Pipeline as Code`
  - the practice of defining a project’s entire build, test, and deployment process through code rather than manual configuration in the Jenkins web UI.

---

### Items

| Items                  | Description                                                                               |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| `Pipeline`             | A continuous delivery pipeline, which is configured via a Jenkinsfile (Pipeline as Code). |
| `Freestyle Project`    | General-purpose job type.                                                                 |
| `Folder`               | A container that stores nested items                                                      |
| `Multibranch Pipeline` | managing CI/CD pipelines for **multiple branches** in **one** version control repository. |
| `Organization Folders` | Creates a set of multibranch project subfolders by scanning for repositories.             |

---

### Build

- `build`
  - a **single execution instance** of a Jenkins job or project.

**Jenkins build lifecycle**:

1. **Triggering a Build**:
   - Initiating the build process through manual, scheduled, or event-driven triggers.
2. **Initialization**:
   - Setting up the build environment and resources.
3. **Source Code Checkout**:
   - Getting the latest code from version control.
4. **Build Process**:
   - Executing build scripts, compiling code, and performing necessary tasks.
5. **Testing**:
   - Running test suites and reporting results.
6. **Deployment**:
   - Releasing built artifacts to target environments.
7. **Post-Build Actions**:
   - Archiving artifacts, publishing reports, and sending notifications.
8. **Recording and Reporting**:
   - Collecting and storing build data and results.
9. **Clean-Up**:
   - Managing resources and resetting the environment.

- **Notifications**: Keeping stakeholders informed of build status.
- **Artifact Storage**: Storing generated artifacts for future use.
- **Logging and Auditing**: Maintaining detailed logs for auditing and troubleshooting.
- **Post-Build Analysis and Continuous Improvement**: Analyzing build results for process enhancement.

---

## Architecture

- a **controller–agent (master–worker) architecture**

```txt
        +----------------------+
        |     Jenkins UI       |
        |  (Web Interface/API) |
        +----------+-----------+
                   |
                   v
        +----------------------+
        |   Jenkins Controller |
        |  (Master Node)       |
        +----------+-----------+
                   |
        ----------------------------
        |            |            |
        v            v            v
+-------------+ +-------------+ +-------------+
|   Agent 1   | |   Agent 2   | |   Agent N   |
| (Worker)    | | (Worker)    | | (Worker)    |
+-------------+ +-------------+ +-------------+
```

---

## Core Components

### Jenkins Controller (Master)

- `Jenkins Controller`
  - the central controlling serve
- Responsibilities:
  - Manage `jobs` and `pipelines`
  - Schedule `builds`
  - Assign `tasks` to `agents`
  - Store configuration and build history
- Provides:
  - Web UI
  - REST API
  - Authentication & authorization

- `Controller` does not run heavy workloads
- `Agents` handle:
  - Compilation
  - Testing
  - Deployment

---

- `Jenkins jobs`
  - the **runnable**, configurable **projects** or **tasks** within the Jenkins automation server that **automate** software development workflows, such as building, testing, and deploying applications.

- `Jenkins Pipeline`
  - **automated process** that describes your entire software delivery workflow (Build, Test, Deploy).

  - Types:
    - **Pipeline** (Jenkinsfile) (recommended)
    - **Freestyle jobs** (basic UI-driven)
      - Written in Groovy-based DSL
      - Supports CI/CD workflows

- `Queue`
  - a **temporary waiting area** for scheduled build jobs that are pending execution due to a lack of available executors (nodes).
  - Controller schedules jobs based on:
    - Available executors
    - Node labels
    - Resource constraints

- `Plugins`
  - a **software extension** that **adds specific features** or integrations to the core Jenkins environment
  - Common plugins:
    - Git / GitHub integration
    - Docker
    - Kubernetes
    - AWS
    - Pipeline plugins

---

### Jenkins Agents (Workers)

- `Jenkins Agents`
  - the machines, containers, or cloud instances that connect to the `Jenkins Controller` **to execute build jobs and pipelines**.

  - Types:
    - `Static agents` (pre-configured)
    - `Dynamic agents` (provisioned on demand, e.g., Kubernetes)

---

- `Executor`
  - a **dedicated slot** on a build agent (or controller) that **executes a single build job or pipeline stage** at a time.
  - acts as a **thread** within an agent, meaning the number of executors per node determines how many jobs can run concurrently.
  - Example:
    - 1 agent with 4 executors → can run 4 jobs concurrently

- `Workspace`
  - a **disposable directory** on the file system of a Jenkins `Node` where a specific job or Pipeline executes its work.
  - It serves as a **temporary "sandbox"** for checking out source code, compiling files, and running tests.
  - Stores:
    - Source code
    - Build artifacts
    - Temporary files

---

### How It Works (Execution Flow)

1. Developer **pushes code** to GitHub
2. `Jenkins` **detects** change (webhook or polling)
3. `Job` is **triggered** and placed in `queue`
4. `Controller` selects an available `agent`
5. `Agent` **executes** pipeline steps
6. Results are sent back to `controller`
7. **Output** shown in `Jenkins UI`

---

### Common Deployment Patterns

1. **Single Node (Small Setup)**
   Controller + executor on **same** machine
   Simple but not scalable
2. **Controller + Multiple Agents (Recommended)**
   Production-ready setup
3. **Cloud-Native Jenkins**
   Controller in VM/container
   Agents dynamically provisioned (Kubernetes)

---

### Plugins

- `Jenkins plugins`
  - **add-on modules** that **extend the functionality** of the core Jenkins automation server, allowing it to integrate with thousands of tools for CI/CD, source control (Git), cloud platforms (Docker, Kubernetes), and build tools (Maven).

- Common plugins:
  - `Pipeline: Stage ViewVersion`

---

## Common Configurations

### Environment Variables

- **Built-in global variable env**
  - ref: https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#using-environment-variables
- **Custome global env var**
  - Manage Jenkins > System > Global properties > check `Environment variables`
- **Pipeline env var**

```groovy
pipeline {
    agent {
        label '!windows'
    }

    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE    = 'sqlite'
    }

    stages {
        stage('Build') {
            steps {
                echo "Database engine is ${DB_ENGINE}"
                echo "DISABLE_AUTH is ${DISABLE_AUTH}"
                sh 'printenv'
            }
        }
    }
}
```

---

### Jenkins URL

- Manage Jenkins > System > Jenkins Location
  - Jenkins URL:

---

### Notification

- **Email**
  - Plugin: `Email Extension Plugin`

---

## Common Practices

### Blue-Green deployment strategy

- Implementing a Blue-Green deployment in Jenkins involves:
  - Setting up **two identical environments**: `blue` and `green`.
  - Deploying the **new version** to the `green` environment.
  - **Testing** in the `green` environment.
  - **Switching traffic** to green if testing succeeds.
  - Monitoring and potential **rollback** if issues arise.

- Key benefits:
  - zero downtime,
  - quick rollback,
  - reduced risk,
  - safe testing,
  - continuous delivery, scalability, enhanced monitoring, and improved confidence in deploying changes.

---

### Backup

- Backup `JENKINS_HOME` directory
- Use ThinBackup plugin
- Use Backup plugin
- Version control job configurations
