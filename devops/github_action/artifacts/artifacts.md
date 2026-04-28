# GitHub Actions: Artifacts

[Back](../index.md)

- [GitHub Actions: Artifacts](#github-actions-artifacts)
  - [Artifacts](#artifacts)
  - [Lab: Artifacts](#lab-artifacts)

---

## Artifacts

- `Artifacts`
  - Share data between jobs and store data after workflows have completed

- vs `cache`

| Artifacts                                                   | Caching                            | Use-case                                                                   |
| ----------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------- |
| Stored for up to 90 days                                    | up to 7 days                       | files to be accessed outside the workflow(Build outputs,Test results,Logs) |
| Managed via two actions (upload-artifact,download-artifact) | Managed via a single action(cache) | files to be accessed within the workflow (Build dependencies)              |

---

## Lab: Artifacts

```yaml
name: 14 - artifacts

on:
  workflow_dispatch:

env:
  build-artifact-key: app-${{ github.sha }}
  test-report-key: test-report-${{ github.sha }}

jobs:
  test-build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: react-app
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: setup node
        uses: actions/setup-node@v6
        with:
          node-version: "24.x"

      - name: Download dependencies
        id: cache-deps
        uses: actions/cache@v5
        with:
          path: react-app/node_modules
          key: deps-node-modules-${{ hashFiles('react-app/package-lock.json') }}

      - name: Install dependencies
        if: steps.cache-deps.outputs.cache-hit != 'true'
        run: npm ci

      - name: Testing
        run: npm run test -- --coverage

      - name: Upload test report
        uses: actions/upload-artifact@v7
        with:
          name: ${{ env.test-report-key }}
          path: react-app/coverage

      - name: Building
        run: npm run build

      - name: Upload build files
        uses: actions/upload-artifact@v7
        with:
          name: ${{ env.build-artifact-key }}
          path: react-app/build

  deploy:
    runs-on: ubuntu-latest
    needs:
      - test-build
    steps:
      - name: Download build artifact
        uses: actions/download-artifact@v8
        with:
          name: ${{ env.build-artifact-key }}
          path: build
      - name: Show folder
        run: ls -R

```