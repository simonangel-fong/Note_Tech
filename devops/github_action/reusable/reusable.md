# GitHub Actions: Reusable Workflows

[Back](../index.md)

- [GitHub Actions: Reusable Workflows](#github-actions-reusable-workflows)
  - [Reusable Workflows](#reusable-workflows)

---

## Reusable Workflows

- `Reusable Workflows`
  - ref: https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows
  - Create and reuse workflows to avoid duplication of common tasks
- Any workflow can be made reusable by adding `workflow_call` to the top-level on key of the workflow definition

- **Reusable Workflow**

```yaml
on:
  workflow_call:
    inputs:
      aws-region:
        type: string
    secrets:
      auth-token:
        required: true
    outputs:
      server-url:
      value: <value>
```

- **Caller Workflow**
  - Inputs are passed via the `with` keyword
  - Secrets are passed via the `secrets` keyword
  - Outputs are accessed via the `outputs` keyword

```yaml
jobs:
  backend-infra-nonprod:
    uses: reusable-deploy@v1
    secrets:
      auth-token: ${{ secrets.GH_PAT }}
    with:
      aws-region: ${{ vars.AWS_REGION }}
```
