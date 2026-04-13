# AI Fundamental - Fine-Tuning

[Back](./index.md)

- [AI Fundamental - Fine-Tuning](#ai-fundamental---fine-tuning)
  - [Fine-Tuning](#fine-tuning)
  - [Common Techniques](#common-techniques)
    - [Full Fine-Tuning](#full-fine-tuning)
    - [Parameter-Efficient Fine-Tuning (PEFT)](#parameter-efficient-fine-tuning-peft)
    - [Instruction Fine-Tuning](#instruction-fine-tuning)
  - [Simple Example](#simple-example)
    - [Step 1: Prepare Dataset](#step-1-prepare-dataset)
    - [Step 2: Choose Base Model](#step-2-choose-base-model)
    - [Step 3: Train (Fine-Tune)](#step-3-train-fine-tune)
    - [Step 4: Evaluate](#step-4-evaluate)
    - [Step 5: Deploy](#step-5-deploy)
  - [Fine-Tuning vs RAG](#fine-tuning-vs-rag)
  - [Avoid fine-tuning](#avoid-fine-tuning)

---

## Fine-Tuning

- `Fine-tuning`
  - the process of taking a `pre-trained model` (like GPT or LLaMA) and training it further **on a specific dataset**.
  - using **proprietary** or **domain specific data** to improve **output quality and domain relevant results**

- **Base model**: General knowledge
- **Fine-tuned model**: Specialized behavior

> **The Analogy:**
>
> - **Pretrained LLM:** A smart generalist who has read the entire internet.
> - **Fine-tuning:** Sending that generalist to a specific job-training program to learn your company's unique workflows.

---

- When Do You Use Fine-Tuning?

Use fine-tuning when `prompting (Zero-shot or Few-shot)` alone is not enough to achieve the desired consistency or specialized behavior.

---

- **Common Use Cases**

1.  **Domain-specific knowledge:** Medical, legal, finance, or internal company policies.
2.  **Style & Tone Control:** Customer support tone, brand voice (formal, friendly, etc.).
3.  **Structured Outputs:** Consistently generating JSON, API responses, or SQL queries.
4.  **Classification Tasks:** Sentiment analysis, ticket routing, or fraud detection.
5.  **Task Specialization:** Code generation for specific frameworks or **Log Analysis** (a high-value DevOps use case).

## Common Techniques

There are three main levels of fine-tuning used in the industry today:

### Full Fine-Tuning

Training all model parameters.

- **Pros:** Highest potential performance.
- **Cons:** Extremely expensive (GPU/Compute), time-consuming, and prone to "catastrophic forgetting."
- **Status:** Not common in practice for most enterprises.

---

### Parameter-Efficient Fine-Tuning (PEFT)

The industry standard for most applications.

- **Examples:** `LoRA (Low-Rank Adaptation)`, `QLoRA`, `Adapters`.
- **Concept:** Freeze 99% of the model weights and only train small "adapter" layers.
- **Pros:** Cheap, fast, requires much less VRAM, and highly portable.

---

### Instruction Fine-Tuning

Training the model specifically on an `Instruction -> Response` format.

- **Example:**
  - _Instruction:_ Summarize this log.
  - _Input:_ `<log data>`
  - _Output:_ `<summary>`
- **Goal:** Teaches the model how to follow specific human commands.

---

## Simple Example

Goal: Train a model to analyze CI/CD failures automatically.

### Step 1: Prepare Dataset

Format your data as input &rarr; output pairs:

```json
{
  "input": "ERROR: Docker build failed COPY requirements.txt not found",
  "output": "Root Cause: requirements.txt missing from build context. Fix: ensure file exists or correct path."
}
```

Requirement: 100–10,000+ high-quality examples.

---

### Step 2: Choose Base Model

Examples:

- Open models: LLaMA, Mistral
- API-based: OpenAI models (fine-tuning supported)

---

### Step 3: Train (Fine-Tune)

Using `LoRA` (typical modern approach):

- Load base model
- Freeze weights
- Train small adapters on your dataset

---

### Step 4: Evaluate

Test with unseen logs:

- Input:

```txt
ERROR: npm install failed package.json missing
```

- Expected output:

```txt
Root Cause: package.json missing
Fix: add package.json or correct working directory
```

---

### Step 5: Deploy

Use it in your pipeline:

- CI/CD fails →
- Send logs →
- Model returns:
  - Root cause
  - Fix suggestion

---

## Fine-Tuning vs RAG

| Method                               | Purpose                     |
| ------------------------------------ | --------------------------- |
| Fine-tuning                          | Change model behavior/style |
| RAG (Retrieval-Augmented Generation) | Inject external knowledge   |

**Rule of thumb:**

- Use `RAG` → for knowledge (policies, docs)
- Use `Fine-tuning` → for behavior (how to respond)

---

## Avoid fine-tuning

- just need **better prompts** → use `prompt engineering`
- **Knowledge changes frequently** → use `RAG`
- Small dataset → may **overfit**
