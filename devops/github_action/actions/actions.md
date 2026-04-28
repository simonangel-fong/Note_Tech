# GitHub Actions: Custom Actions

[Back](../index.md)

- [GitHub Actions: Custom Actions](#github-actions-custom-actions)
  - [Custom Actions](#custom-actions)
    - [Types](#types)
  - [Lab: Create Composiste Actions](#lab-create-composiste-actions)
  - [Lab: Create a JS action](#lab-create-a-js-action)
  - [Custom Actions](#custom-actions-1)
    - [Input \& Output](#input--output)
    - [Lab: Docker action](#lab-docker-action)

---

## Custom Actions

- `Custom Actions`
  - allow us to **write, encapsulate, and reuse** pieces of **custom logic** in any programming language.

- **Requirements**
  - Requires an `action.yaml` file
  - Must be on its **own repository** if it is to be reused by other repos.

---

### Types

- three types of custom actions:

- **Composite Actions**
  - Pros
    - **Simplest** type of Custom Action.
    - **Grouping** of other GitHub Actions.
  - Cons
    - May not be enough for complex functionality.

- **JavaScript Actions**
  - Pros
    - Allows writing any type of custom logic.
    - `@actions` packages provide lots of functionality.
  - Cons
    - Requires JavaScript knowledge and Node environment.

- **Docker Actions**
  - Pros
    - Allows writing **any type** of custom logic.
    - Can be written in **any programming language**.
  - Cons
    - Might be more verbose as only **JS supports** `@actions` package.

---

## Lab: Create Composiste Actions

- Create file
  - `.github/actions/<composiste_action_name>/action.yaml`

- Purpose of the action:
  - common steps are repeated when building a react app, such as setup node, install dependencies, and test.
  - create an action to modularize steps.

```yaml
name: Cache Node and NPM Dependencies
description: This action allows to cache both node and NPM dependencies based on
  the package-lock.json file.

inputs:
  node-version:
    required: true
    description: NodeJS version to use
    default: 24.x
  working-dir:
    required: false
    description:
      The working directory of the application. By default, the current
      directory
    default: "."
  target-env:
    required: false
    description: "Whether dev dependencies are installed. Default, dev"
    default: dev

runs:
  # define type of action
  using: composite
  # define steps
  steps:
    - name: setup NodeJS version ${{ inputs.node-version }}
      uses: actions/setup-node@v6
      with:
        node-version: ${{ inputs.node-version }}

    - name: Cache dependencies
      id: cache
      uses: actions/cache@v5
      with:
        path: ${{ inputs.working-dir }}/node_modules
        key: node-modules-${{ inputs.target-env }}-${{ hashFiles(format('{0}/{1}', inputs.working-dir, 'package-lock.json')) }}

    - name: Install dependencies
      if: steps.cache.outputs.cache-hit != 'true'
      shell: bash
      working-directory: ${{ inputs.working-dir }}
      run: ${{ inputs.target-env == 'dev' && 'npm ci' || 'npm ci --omit=dev' }}
```

- Create a workflow to use the action

```yaml
name: 17 - Custom Actions - Composite
run-name: 17 - Custom Actions - Composite | env - ${{ inputs.target-env }}

on:
  workflow_dispatch:
    inputs:
      target-env:
        description: "Selete environment for dependencies installation"
        type: choice
        options:
          - dev
          - prod

env:
  working-directory: react-app

jobs:
  build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ${{ env.working-directory }}

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Setup Node and NPM Dependencies
        uses: ./.github/actions/composite-cache-deps
        with:
          node-version: 24.x
          working-dir: ${{ env.working-directory }}
          target-env: ${{ inputs.target-env }}

      - name: Test
        run: npm run test

      - name: Build
        run: npm run build
```

---

## Lab: Create a JS action

- ref: js toolkit
  - https://github.com/actions/toolkit

- Create file
  - `.github/actions/<js_action_name>/action.yaml`

- Purpose of the action:
  - Checks if NPM packages require to update, and creates a PR with the updated pacakge.json files.

- Init npm under `.github/actions/<js_action_name>/`

```sh
# init js project
cd .github/actions/js-dependency-update

npm init -y
npm install @actions/core@latest

```

## Custom Actions

### Input & Output

- Composite actions
  - `inputs` key
  - `outputs` key:
    - using `$GITHUB_OUT`
    - `run: echo "demo_output=1234" >> "$GITHUB_OUTPUT"`
    - call in workflow
      - define step id; `${{ steps.<step_id>.outputs.<output_name> }}`

- Docker actions:
  - `inputs` key
    - main process uses ENV Var to pass values
    - python: `os.getenv`
  - `outputs` key
    - write key-value pair into the GITHUB_OUTPUT file
    - call in workflow
      - define step id; `${{ steps.<step_id>.outputs.<output_name> }}`

---

### Lab: Docker action

- action.yaml

```yaml
name: Ping URL
description: Ping URL untl maximum trials have exceeded. If result is not 200 until then, fails the action.

inputs:
  url:
    description: URL to ping
    required: true
  max_trials:
    description: maximum number of trials
    default: "10"
    required: false
  delay:
    description: Delay in seconds between trials
    default: "5"
    required: false

outputs:
  url-reachable:
    description: Whether the URL is reachable

runs:
  using: docker
  image: Dockerfile
```

- Dockerfile

```dockerfile
FROM python:alpine3.19
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "/app/main.py"]
```

- main.py

```py
import os
import requests
from time import sleep

URL = os.getenv("INPUT_URL", "http://google.com")
DELAY = os.getenv("INPUT_DELAY", '5')
MAX_TRIALS = os.getenv("INPUT_MAX_TRIALS", "10")


def set_output(file_path, key, value):
    with open(file_path, "a") as file:
        print(f"{key}={value}", file=file)


def ping_url(url, delay, max_trials):
    trials = 0

    while trials < max_trials:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Website {url} is reachable.")
                return True
        except requests.ConnectionError:
            print(
                f"Website {url} is unreachable. Retring in {delay} seconds...")
            sleep(delay)

            trials += 1
        except requests.exceptions.MissingSchema:
            print(f"Invalid URL format: {url}")

    return False


def run():
    website_url = URL
    delay = int(DELAY)
    max_trials = int(MAX_TRIALS)

    # get ping return
    website_reachable = ping_url(website_url, delay, max_trials)

    # set output
    set_output(os.getenv('GITHUB_OUTPUT'),'url-reachable',website_reachable)

    if not website_reachable:
        raise Exception(f'Website {website_url} is malformaed or unreachable.')

    print(f"website {website_url} is reachable.")


if __name__ == "__main__":
    run()

```

- Workflow

```yaml
name: 17 - Custom Actions - Docker
run-name: 17 - Custom Actions

on:
  workflow_dispatch:
    inputs:
      url:
        type: string
        default: "https://www.google.com"
      max_trials:
        description: maximum number of trials
        default: "10"
        required: false
      delay:
        description: Delay in seconds between trials
        default: "5"
        required: false

jobs:
  ping-url:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Ping URL
        id: ping-url
        uses: ./.github/actions/docker-ping-url
        with:
          url: ${{ inputs.url }}
          max_trials: ${{ inputs.max_trials }}
          delay: ${{ inputs.delay }}

      - name: Print output
        run: |
          echo "URL reachable: ${{ steps.ping-url.outputs.url-reachable }}"
```
