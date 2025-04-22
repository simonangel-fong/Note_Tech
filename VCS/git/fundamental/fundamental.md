# git - Fundamental

[back](../index.md)

- [git - Fundamental](#git---fundamental)
  - [Fundamental](#fundamental)
  - [File Lifecycle Stages in Git](#file-lifecycle-stages-in-git)
  - [Workflow](#workflow)

---

## Fundamental

- `git`:
  - a popular `version control system`

## File Lifecycle Stages in Git

| Stage Name       | Description                                           | Common Commands         |
| ---------------- | ----------------------------------------------------- | ----------------------- |
| `Untracked`      | File is not tracked by Git                            | `git status`(untracked) |
| `Staged` (Index) | Changes have been added to the staging area           | `git add <file>`        |
| `Committed`      | Changes are committed to the local repository history | `git commit -m "msg"`   |

---

## Workflow

- key steps involved in using Git:
  - `Clone`
    - The first step is cloning a **remote repository** to your **local machine**.
    - It **creates a local copy** of the project's files and history on your computer.
  - `Branch`
    - create a **new branch** to work on a specific **task** or **feature**.
    - Branching **isolates** the local changes from main codebase until it can be merged.
  - `Work`
    - **Changes** that are made to the files in your **branch**, such as **adding new features**, fixing bugs, or making alterations.
  - `Commit`
    - As changes are made, you **periodically commit** them to your local repository.
    - Each commit is represented as a **snapshot of the project** at a particular time.
  - `Pull`
    - To **incorporate the changes** made by other developers, you can **pull the latest changes** from the remote repository.
  - `Merge`
    - Once your work is completed and **tested**, you can **merge the changes** into the **main branch**.
    - This integrates your changes with the rest of the project.
  - `Push`
    - The last step is to **push your changes** or local commits to the **remote repository**, so that your work is shared with other team members.
