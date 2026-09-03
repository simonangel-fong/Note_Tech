# MLOPS - Experiment Tracking

[Back](../index.md)

- [MLOPS - Experiment Tracking](#mlops---experiment-tracking)
  - [Experiment Tracking](#experiment-tracking)
  - [MLflow](#mlflow)
  - [Installation](#installation)

---

## Experiment Tracking

- `Experiment tracking`
  - the process of **saving and organizing details** for machine learning tests.
  - helps repeat past work and pick the best model.
- Key items include:
  - **Parameters**: Learning rate and batch size
  - **Metrics**: Accuracy and loss values
  - **Code**: Git commit tags and scripts
  - **Data**: Version hashes and files

---

## MLflow

- ref: https://mlflow.org/docs/latest/ml/

- `MLflow`
  - an open-source **platform** that **manages** the machine learning **lifecycle**, featuring MLflow Tracking, MLflow Projects, and MLflow Models.
  - It helps teams record experiments, reuse code, and deploy AI applications Databricks with ease.

- **Core Components**
  - `MLflow Tracking`:
    - Logs metrics, parameters, and output files `ML Experiment Tracking` during training.
  - `MLflow Projects`:
    - **Packages data science code** Machine Learning with MLflow into a standard format.
  - `MLflow Models`:
    - Provides a **consistent format to deploy** models anywhere.
  - `MLflow Model Registry`:
    - Acts as a central store for model version control ML Model Registry.

---

## Installation

```sh
pip install --upgrade "mlflow>=3.1"
```
