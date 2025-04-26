# git - Staging Area

[back](../index.md)

- [git - Staging Area](#git---staging-area)
  - [Staging Area](#staging-area)
  - [Untrack to last commited](#untrack-to-last-commited)
  - [Compare diff](#compare-diff)

---

## Staging Area

| Command             | Description                                      |
| ------------------- | ------------------------------------------------ |
| `git status`        | View modified/untracked files                    |
| `git add file_name` | Add a file to staging area                       |
| `git add .`         | Add all file at the current path to staging area |
| `git rm file_name`  | Remove a tracked file from repo and disk         |

---

## Untrack to last commited

| Command                 | Description                                                               |
| ----------------------- | ------------------------------------------------------------------------- |
| `git restore file_name` | Discard changes in working directory, reset to the last committed version |

---

## Compare diff

- Sequence of states
  - unstaged
  - staged
  - commited

| Command                         | Current state | Description                                   |
| ------------------------------- | ------------- | --------------------------------------------- |
| `git diff --name-only`          | unstaged      | List the files that have not been staged      |
| `git diff --name-only --cached` | Stage         | List the names of files that have been staged |
