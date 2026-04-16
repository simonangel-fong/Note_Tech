# AI Fundamental - Prompt Engineering

[Back](./index.md)

- [AI Fundamental - Prompt Engineering](#ai-fundamental---prompt-engineering)
  - [Prompt Engineering](#prompt-engineering)
    - [Attention Mechanism](#attention-mechanism)
  - [Common Techniques](#common-techniques)
  - [Recommended Pattern](#recommended-pattern)
    - [Example](#example)

---

## Prompt Engineering

- `Prompt engineering`
  - the practice of **designing and refining inputs (`prompts`)** to **guide an AI model** (like an LLM) to produce accurate, relevant, and structured outputs.

- It focuses on:
  - **Task Definition:** Clearly defining the **objective**.
  - **Contextualization:** Providing the right **background information**.
  - **Behavioral Control:** Controlling the format and tone of the **response**.

---

### Attention Mechanism

- `Attention Mechanism`
  - a **machine learning technique** that directs deep learning models to **focus on the most relevant words** when generating each token
  - by assigning weights (importance) to different parts of the input

- **Important parts** get more influence
  - Clear instructions → higher attention → better results
  - Noisy/long context → diluted attention → worse results
- **Position** bias exists
  - Tokens at:
    - Beginning
    - End
  - tend to receive stronger attention

- **Long prompts** can **degrade** quality
  - Attention is spread across many tokens
  - Model may:
    - Miss key info
    - Ignore earlier instructions

- Structured prompts improve attention
  - Good structure helps the model:
    - Locate key signals
    - Prioritize correctly

---

## Common Techniques

- `Zero-shot Prompting`
  - a technique where a Large Language Model (LLM) is given a task **without any prior examples**, **relying entirely** on its **pre-trained knowledge** to generate a response.

> **Example:** "Summarize the following text in one sentence: [Insert Text]"

---

- `One-shot prompting`
  - a technique where you provide a Large Language Model (LLM) **with a single example (or "shot")** of a task within the prompt before asking it to perform a new, similar task.

---

- `Few-shot Prompting`
  - a prompt engineering technique that provides an AI model with **a few examples (or "shots")** in the prompt to demonstrate the **desired behavior** before asking it to perform a new task.

> **Example:** > Translate English to French:
>
> - Hello → Bonjour
> - Goodbye → Au revoir
> - Thank you →

---

- `Role/Instruction Prompting`
  - a technique where you **assign a specific persona, profession, or character** to an AI to guide its tone, expertise, and style.

> **Example:** "You are a senior DevOps engineer. Explain CI/CD pipelines clearly."

---

- `Step-by-step (Chain-of-Thought) Prompting`
  - a technique that improves large language model (LLM) reasoning by **guiding it to generate intermediate, step-by-step logic** before providing a final answer.

> **Example:** "Solve the following math problem step by step:"

---

- **Output Formatting**

Specifying the exact structure of the response.

> **Example:** Explain Kubernetes in:
>
> - 1 sentence summary
> - 3 bullet points

---

- **Context Injection**

Providing relevant data to improve accuracy and grounding.

> **Example:** "Based on the following logs, identify the issue: `<logs here>`"

---

- **Constraint-based Prompting**

Setting specific rules or limitations.

> **Example:** "Answer in less than 50 words. Do not use technical jargon."

---

## Recommended Pattern

```txt
You are a senior DevOps engineer.          ← Role

Your task is to analyze a CI/CD failure.   ← Task

Context:
<logs / data here>                         ← Context

Instructions:
- Think step by step
- Identify root cause first                ← Reasoning guidance

Available tools:
- log_parser                              ← (optional)

Output format:
- Root Cause
- Fix                                     ← Structure

Constraints:
- Max 100 words
- Be concise                              ← Limits
```

### Example

```txt
You are a senior DevOps engineer.

Your task is to analyze the following CI/CD pipeline failure, identify the root cause, and suggest a fix.

Context:
ERROR: Docker build failed
Step 3/5 : COPY requirements.txt .
COPY failed: file not found in build context

Instructions:
- Think step by step
- Identify the root cause first
- Then suggest the most likely fix

Available tools:
- None

Output format:
- Root Cause
- Fix

Constraints:
- Keep the explanation under 80 words
- Avoid unnecessary jargon
```
