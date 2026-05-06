# Helm - Helm Chart Repo (Github Repo)

[Back](../index.md)

- [Helm - Helm Chart Repo (Github Repo)](#helm---helm-chart-repo-github-repo)
  - [Creating an Exclusive Helm Repository using Github Pages](#creating-an-exclusive-helm-repository-using-github-pages)

---

## Creating an Exclusive Helm Repository using Github Pages


- Create helm chart at `charts/`

```sh
helm create charts
```

- Create a `GitHub` repo, can be private/public.
- Create a branch called `gh-pages`

```sh
git branch gh-pages
git checkout gh-pages
git push
```

- Configure github pages
  - settings > GitHub Pages > Branch: `gh-pages`
- Create workflow:
  - Checkout Code -> Install Helm -> Release Helm

- `.github/workflows/helm-release.yml`

```yaml
name: Release Helm Chart

on:
  push:
    branches:
      - master
    # paths:
    #   - 'web-demo/**'
    
jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Configure Git
        run: |
          git config user.name "$GITHUB_ACTOR"
          git config user.email "$GITHUB_ACTOR@users.noreply.github.com"

      - name: Set up Helm
        uses: azure/setup-helm@v4

      - name: Run chart-releaser
        uses: helm/chart-releaser-action@v1.7.0
        with:
          charts_dir: .
        env:
          CR_TOKEN: "${{ secrets.GITHUB_TOKEN }}"

```

- Test

```sh
helm repo add simonangel-fong https://simonangel-fong.github.io/Demo_Helm_Public_Repo
helm repo update

helm install web-demo simonangel-fong/web-demo
# level=WARN msg="unable to find exact version; falling back to closest available version" chart=web-demo requested="" selected=0.2.0
# NAME: web-demo
# LAST DEPLOYED: Wed May  6 00:50:14 2026
# NAMESPACE: default
# STATUS: deployed
# REVISION: 1
# DESCRIPTION: Install complete
# NOTES:
# 1. Get the application URL by running these commands:
#   export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=web-demo,app.kubernetes.io/instance=web-demo" -o jsonpath="{.items[0].metadata.name}")
#   export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
#   echo "Visit http://127.0.0.1:8080 to use your application"
#   kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT

helm list
# NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
# web-demo        default         1               2026-05-06 00:50:14.2093535 -0400 EDT   deployed        web-demo-0.2.0  1.16.0   

helm upgrade --install web-demo simonangel-fong/web-demo
helm uninstall web-demo 
```
