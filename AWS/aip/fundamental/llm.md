# AIP Fundamental: LLM

[Back](../index.md)

- [AIP Fundamental: LLM](#aip-fundamental-llm)

---

- `multimodal large language model (MLLM)`
  - an AI system that extends a traditional text-only language model so it can process, understand, and reason across **multiple types of data**—called modalities—such as text, images, audio, and video.

- **How It Works**
  - **Modality Encoders**:
    - **Specialized** sub-models (like a vision encoder for images or audio processors) **convert** non-text data into **numerical representations** called `embeddings`.
  - **Connectors / Projectors**:
    - Adapter layers **translate or align** those `non-text embeddings` so the core language model can interpret them just like words or tokens.
  - **Shared Vector Space / Backbone LLM**:
    - The core language model processes everything together, allowing it to perform cross-modal reasoning (e.g., looking at a chart and reading surrounding text simultaneously).
