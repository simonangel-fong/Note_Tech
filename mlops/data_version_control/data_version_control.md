# MLOPS - Data Version Control (DVC)

[Back](../index.md)

- [MLOPS - Data Version Control (DVC)](#mlops---data-version-control-dvc)
  - [Data Version Control (DVC)](#data-version-control-dvc)
    - [How DVC Works](#how-dvc-works)
  - [Commands](#commands)
  - [Install](#install)

---

## Data Version Control (DVC)

- ref: https://doc.dvc.org/start

- `Data Version Control (DVC)`
  - an open-source tool designed to manage, track, and version **large datasets**, machine learning models, and code experiments.

### How DVC Works

- **Lightweight Tracking**:
  - `DVC` creates **tiny, human-readable placeholder files** that contain unique data hashes.
    - with a `.dvc` extension
- **Git Integration**:
  - commit these lightweight `.dvc` tracking files into Git repository just like normal code.
- **External Storage**:
  - The actual **heavy datasets** and models are **pushed** to and **stored** in external cloud storage or local servers.
    - e.g., `Amazon S3`, `Google Cloud Storage`, or `Azure Blob`

---

## Commands

- Repo

| Command                                          | Description                                                |
| ------------------------------------------------ | ---------------------------------------------------------- |
| `dvc init`                                       | Initialize DVC repository.                                 |
| `dvc push`                                       | Upload tracked files or directories to remote storage.     |
| `dvc pull`                                       | Download tracked files or directories from remote storage. |
| `dvc checkout`                                   | Checkout data files from cache.                            |
| `dvc dag`                                        | Visualize DVC project DAG.                                 |
| `dvc metrics show`                               | Print metrics, with optional formatting.                   |
| `dvc metrics diff <old_commit> <current_commit>` | Show changes in metrics between commits                    |

- File

| Command                                       | Description                                          |
| --------------------------------------------- | ---------------------------------------------------- |
| `dvc list`                                    | List repository contents.                            |
| `dvc list-url`                                | List directory contents from URL.                    |
| `dvc get <remote_url> <local_path> -o <path>` | Download file or directory tracked by DVC or by Git. |
| `dvc add <targets_file>`                      | Input files/directories to add.                      |
| `dvc remove`                                  | Remove stages                                        |

- remote

| Command                                      | Description                                |
| -------------------------------------------- | ------------------------------------------ |
| `dvc remote add -d remote_name <remote_url>` | Add a new default data remote.             |
| `dvc remote default`                         | Set/unset the default data remote.         |
| `dvc remote modify`                          | Modify the configuration of a data remote. |
| `dvc remote list`                            | List all available data remotes.           |
| `dvc remote remove`                          | Remove a data remote.                      |
| `dvc remote rename`                          | Rename a DVC remote                        |

---

## Install

```sh
# install dvc is with uv
uv tool install dvc

# confirm
uv --version
# uv 0.11.26 (396ef7ce4 2026-06-30 x86_64-pc-windows-msvc)

```
