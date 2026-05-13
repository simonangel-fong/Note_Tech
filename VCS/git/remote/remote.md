# Git - Remote

[Back](../index.md)

---

## Common Practices

- Work on `feature-*` branch
- Pull from `main`
- Push to current feature branch

---

```sh
# 1. Global config
git config --global pull.rebase false      # merge on pull
git config --global pull.ff only           # safety: fail on divergence
git config --global push.default simple    # push to same-name upstream only

# 2. Branch config — leave as-is
git branch -vv                              # feature-app → origin/feature-app

# 3. Daily workflow — explicit, no ambiguity
git fetch origin
git merge origin/main                       # bring main into feature-app
git add <files>
git commit -m "descriptive message"
git push                                    # → origin/feature-app
```
