# git - Branch

[back](../index.md)

- [git - Branch](#git---branch)
  - [Local Repository Branch Operations](#local-repository-branch-operations)

---

## Local Repository Branch Operations

| Git Command                       | Description                                                              |
| --------------------------------- | ------------------------------------------------------------------------ |
| `git branch`                      | **List** all local branches                                              |
| `git branch branch_name`          | **Create** a new local branch                                            |
| `git checkout branch_name`        | **Switch** to a different local branch                                   |
| `git switch branch_name`          | **Alternative** to checkout for switching branches                       |
| `git switch -c branch_name`       | **Create and switch** to a new branch                                    |
| `git merge branch_name`           | **Merge** the specified branch **into the current branch**               |
| `git branch -d branch_name`       | **Delete** a local branch (safe, **warns if unmerged**)                  |
| `git branch -D branch_name`       | **Force delete** a local branch                                          |
| `git log --oneline --graph --all` | **View branch history** in a compact graph                               |
| `git stash` / `git stash pop`     | **Save** and retrieve **local changes** (useful when switching branches) |
