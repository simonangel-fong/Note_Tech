# GitHub Actions: Artifacts

[Back](../index.md)

- [GitHub Actions: Artifacts](#github-actions-artifacts)
  - [Artifacts](#artifacts)

---

## Artifacts

- `Artifacts`
  - Share data between jobs and store data after workflows have completed

- vs `cache`

| Artifacts                                                   | Caching                            | Use-case                                                                   |
| ----------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------- |
| Stored for up to 90 days                                    | up to 7 days                       | files to be accessed outside the workflow(Build outputs,Test results,Logs) |
| Managed via two actions (upload-artifact,download-artifact) | Managed via a single action(cache) | files to be accessed within the workflow (Build dependencies)              |
