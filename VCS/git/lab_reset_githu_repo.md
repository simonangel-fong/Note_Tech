# Lab: Reset GitHub Repo

[Back](./lab_reset_githu_repo.md)

- [Lab: Reset GitHub Repo](#lab-reset-github-repo)
  - [Backup repo](#backup-repo)
  - [Re-init](#re-init)
  - [Manage remote branch](#manage-remote-branch)

---

## Backup repo

```sh
# pull remote repo
git pull

# back up
cp repo_dir remote_dir
```

---

## Re-init

```sh
# remove .git
# linux
rm -rf .git

# windows
Remove-Item -Recurse -Force .git

# init
git init

# update git ignore
touch .gitignore

# add and commit
git status
git add .
git commit -m "Initial clean commit"

# add remote
git remote add origin remote_url
git remote -v

git status
git branch -M main
# Force-push to GitHub
git push -u origin main --force

# confirm in log:
git log --oneline
# a6e1b1f (HEAD -> main, origin/main) Initial clean commit
```

---

## Manage remote branch

```sh
# view branches:
git branch -r

# Delete a remote brach
git push origin --delete testing
```











delete old branches/tags on GitHub


```sh

```
