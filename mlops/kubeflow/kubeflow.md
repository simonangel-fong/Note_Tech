# MLOPS - Kubeflow

[Back](../index.md)

- [MLOPS - Kubeflow](#mlops---kubeflow)
  - [Kubeflow](#kubeflow)
    - [Key Components of Kubeflow](#key-components-of-kubeflow)

---

## Kubeflow

- `Kubeflow`
  - an open-source, cloud-native platform designed to run, scale, and manage **machine learning (ML) workflows** on top of Kubernetes.

- is a collection of projects
  - Spark Operator
  - Trainer
  - Kalib
  - KServe
  - Notebooks
  - Pipelines
  - Dashboard
  - Model Reistry

---

### Key Components of Kubeflow

- `Kubeflow` breaks down the complex machine learning lifecycle into **modular, reusable tools**:
  - **Kubeflow Notebooks**:
    - Provides managed, **browser-based development** environments like `JupyterLab`, `RStudio`, and `VS Code` directly inside the cluster.
  - **Kubeflow Pipelines**:
    - An orchestration engine and toolkit used to build and automate repeatable, multi-step ML workflows.
  - **Kubeflow Trainer**:
    - Manages distributed **model training** and large language model (LLM) **fine-tuning** across multiple nodes and GPUs.
  - **Katib**:
    - Handles automated **hyperparameter tuning** and **model optimization** using various search algorithms.
  - **Kubeflow Hub (Model Registry)**:
    - Acts as a **central catalog** to version, track, and manage **model artifacts** as they move to production.

---
