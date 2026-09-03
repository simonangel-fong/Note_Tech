# MLOPS - KServe

[Back](../index.md)

- [MLOPS - KServe](#mlops---kserve)
  - [KServe](#kserve)

---

## KServe

- `KServe`
  - an open-source, Kubernetes-native platform designed for **deploying and serving** machine learning and AI models at scale.
  - acts as an **abstraction layer** that handles the complex underlying infrastructure, so data scientists and engineers can focus purely on model performance.
    - e.g, autoscaling, networking, health checks, and request routing

- **Key Features**
  - **Serverless Scale-to-Zero**:
    - Automatically adjusts compute resources **based on live traffic**, scaling down to **zero when idle** to minimize cloud costs.
  - **Multi-Framework & Generative AI Support**:
    - Pluggable runtimes support classical machine learning **frameworks** (TensorFlow, PyTorch, Scikit-Learn) alongside modern **generative AI engines** like `vLLM`.
  - **Standardized Protocol**:
    - Implements the `V2 Open Inference Protocol`, giving clients a **unified API** regardless of the underlying model framework.
  - **Advanced Traffic Management**:
    - Enables `canary rollouts`, `A/B testing`, and `multi-model inference pipelines` via custom resources like `InferenceService` and `InferenceGraph`.
