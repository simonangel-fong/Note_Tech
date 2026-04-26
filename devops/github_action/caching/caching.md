# GitHub Actions: Caching

[Back](../index.md)

- [GitHub Actions: Caching](#github-actions-caching)
  - [Caching](#caching)
    - [Lab: Caching](#lab-caching)
    - [Lab: Caching across Jobs](#lab-caching-across-jobs)

---

## Caching

- `Caching`
  - ref: https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching
  - Speed up workflow runs by caching stable files
  - store files and later retrieve them based on a key.
- Workflows can access the cache from their branch or from the default branch.
- Use case:
  - Cache dependencies to speed up execution by avoiding always downloading and installing them.

- Workflow run starts -> Execute cache step -> Cache matching key?
  - yes: Restore cache
  - No: Install dependencies
  - -> Execute lint & testing

- retained for a maximum of **7 days** since they were **last accessed**.

---

- example:

```yaml
steps:
  - uses: actions/cache@v3
    id: cache
    with:
      path: node_modules
      key: ${{ hashFiles('**/package-lock.json') }}

   - name: Install dependencies
     if: steps.cache.outputs.cache-hit != 'true'
     run: npm ci

   - name: Lint & test
     run: |
      npm run lint
      npm run test
```

---

### Lab: Caching

```yaml
name: 13 - caching

on:
  workflow_dispatch:
    inputs:
      use-cache:
        type: boolean
        default: true
        description: Whether to use cache

jobs:
  build:
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
        if: ${{ inputs.use-cache }}
        uses: actions/cache@v5
        with:
          path: react-app/node_modules
          key: deps-node-modules-${{ hashFiles('react-app/package-lock.json') }}

      - name: Install dependencies
        if: steps.cache-deps.outputs.cache-hit != 'true'
        run: npm ci

      - name: Testing
        run: npm run test

      - name: Building
        run: npm run build

      - name: Deploying
        run: echo "Deploying to nonprod"
```

> from 43s -> 26s
> key log:
> **no Caching**
>
> - **Post Download dependencies**
>   Sent 44832387 of 44832387 (100.0%), 46.8 MBs/sec
>   Cache saved with key: deps-node-modules-4e51da629d104b02c6198499472f35027b1d0783d5450e91e6cc8e30af96d8c2
>
> **Caching**
>
> - **Download dependencies**
>   Cache hit for: deps-node-modules-4e51da629d104b02c6198499472f35027b1d0783d5450e91e6cc8e30af96d8c2
>   Received 44832387 of 44832387 (100.0%), 125.0 MBs/sec
>   Cache Size: ~43 MB (44832387 B)
>   Cache restored successfully
>   Cache restored from key: deps-node-modules-4e51da629d104b02c6198499472f35027b1d0783d5450e91e6cc8e30af96d8c2
> - **Install dependencies**: skiped

---

### Lab: Caching across Jobs

- pre-install job:
  - build and cache
  - Generate the cache key and output
- build job:
  - hit cache key and download

```yaml
name: 13 - caching across jobs

on:
  workflow_dispatch:
    inputs:
      use-cache:
        type: boolean
        default: true
        description: Whether to use cache

jobs:
  pre-install:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: react-app
    outputs:
      deps-cache-key: ${{ steps.cache-key.outputs.CACHE_KEY }}
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: setup node
        uses: actions/setup-node@v6
        with:
          node-version: "24.x"

      - name: Generate cache key
        id: cache-key
        run: |
          echo "CACHE_KEY=deps-node-modules-${{ hashFiles('react-app/package-lock.json') }}" >> "$GITHUB_OUTPUT"

      - name: Download dependencies
        id: cache-deps
        if: ${{ inputs.use-cache }}
        uses: actions/cache@v5
        with:
          path: react-app/node_modules
          key: ${{ steps.cache-key.outputs.CACHE_KEY }}

      - name: Install dependencies
        if: steps.cache-deps.outputs.cache-hit != 'true'
        run: npm ci

  build:
    runs-on: ubuntu-latest
    needs: pre-install
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
        if: ${{ inputs.use-cache }}
        uses: actions/cache@v5
        with:
          path: react-app/node_modules
          key: ${{ needs.pre-install.outputs.deps-cache-key }}

      - name: Install dependencies
        if: steps.cache-deps.outputs.cache-hit != 'true'
        run: npm ci

      - name: Testing
        run: npm run test

      - name: Building
        run: npm run build

      - name: Deploying
        run: echo "Deploying to nonprod"
```

- Extensions
  - one caching can be shared with multiple jobs
