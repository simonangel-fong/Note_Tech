# DevOps - GitHub Actions

[Back](../../index.md)

---

- [Fundamental](./fundamental/fundamental.md)
- [Execution Flow](./flow/flow.md)
- [Caching](./caching/caching.md)
- [Artifacts](./artifacts/artifacts.md)
- [Custom Actions](./actions/actions.md)
- [Reusable workflow](./reusable/reusable.md)
- [Security](./security/security.md)

---

## Install

- [Setup Local Test](./local_test/local_test.md)

---

## vs `Jenkins`

| Category            | Jenkins                                                                                 | GitHub Actions                                                                                        |
| ------------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Infrastructure**  |                                                                                         |                                                                                                       |
| Hosting             | Self-hosted; you manage server, OS, and updates                                         | Cloud-hosted by GitHub; self-hosted runners also available                                            |
| Config format       | Groovy-based `Jenkinsfile` (declarative or scripted)                                    | YAML in `.github/workflows/`                                                                          |
| Ecosystem           | 1,800+ plugins via Plugin Manager                                                       | 20,000+ actions on GitHub Marketplace                                                                 |
| SCM integration     | Any SCM (GitHub, GitLab, Bitbucket, SVN…)                                               | Native GitHub only                                                                                    |
| **Core concepts**   |                                                                                         |                                                                                                       |
| Executor unit       | `agent` — node or pod that runs the pipeline                                            | `runner` — GitHub-hosted VM or self-hosted machine                                                    |
| Pipeline structure  | `stage` / `step`                                                                        | `job` / `step`                                                                                        |
| Reusability         | `shared library` — Groovy libs loaded from SCM                                          | `action` or `reusable workflow` (called via `uses:`)                                                  |
| Trigger             | `trigger` block — cron, SCM poll, upstream jobs, webhooks                               | `on:` — push, pull_request, schedule, workflow_dispatch, etc.                                         |
| Environment vars    | `env` block or `environment` directive (pipeline or stage scope)                        | `env:` at workflow, job, or step level                                                                |
| **Secrets**         |                                                                                         |                                                                                                       |
| Secrets management  | Credentials Plugin — stored in Jenkins credential store, injected via `withCredentials` | Repository / org secrets, injected as `${{ secrets.NAME }}`                                           |
| **Flow control**    |                                                                                         |                                                                                                       |
| Parallelism         | `parallel` block inside a stage                                                         | `matrix` strategy on a job; or multiple jobs running concurrently                                     |
| Parameters / inputs | `parameters` directive — string, choice, boolean, etc.                                  | `inputs:` on `workflow_dispatch` or `workflow_call`                                                   |
| Concurrency control | `disableConcurrentBuilds()` option in pipeline                                          | `concurrency:` key — cancel in-progress or queue runs per group                                       |
| Conditions          | `when` directive — branch, environment, expression, etc.                                | `if:` expression using `${{ }}` context and functions                                                 |
| **Post-run**        |                                                                                         |                                                                                                       |
| Post actions        | `post` block with `success`, `failure`, `always`, `unstable`, `cleanup`                 | Step-level conditionals: `if: success()`, `if: failure()`, `if: always()`                             |
| Artifacts           | `archiveArtifacts` step; retained on Jenkins controller                                 | `actions/upload-artifact` / `actions/download-artifact`; stored by GitHub with configurable retention |
