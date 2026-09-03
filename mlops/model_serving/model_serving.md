# MLOPS - Model Serving

[Back](../index.md)

- [MLOPS - Model Serving](#mlops---model-serving)
  - [Model Serving](#model-serving)
  - [Methods](#methods)

---

## Model Serving

- `Model serving`
  - the process of **deploying a trained machine learning or AI model** into a production environment so that external applications, systems, or users can send input data and receive live predictions via an API.
  - bridges the gap between **data science experimentation** and **real-world business value**.

- a `served model` runs as an **active service** and gets ready to process requests on demand.
- **How Model Serving Works**
  - **The Request**:
    - An app or user **sends data** (like a user's browsing history or an image) to a web address.
  - **The API Endpoint**:
    - A framework like `FastAPI` or `gRPC` receives the data and passes it to the model.
  - **The Inference**:
    - The server runs the data through the model to **calculate a result**.
  - **The Response**:
    - The prediction (like a product recommendation or a classification) is sent back to the application.

---

## Methods

- Deploys on VM with script and app
- Uses cloud provider service, e.g., `Amazon SageMaker`
- Deploys on k8s via manifests
- Deploys on k8s cluster via KServe
