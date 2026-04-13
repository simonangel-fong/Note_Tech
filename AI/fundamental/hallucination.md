# Hallucination

[Back](./index.md)

- [Hallucination](#hallucination)
  - [Hallucination](#hallucination-1)
  - [Causes](#causes)
  - [Types of Hallucination](#types-of-hallucination)
  - [How to Detect \& Evaluate Hallucination](#how-to-detect--evaluate-hallucination)
  - [How to Reduce Hallucination](#how-to-reduce-hallucination)
    - [Prompt Engineering](#prompt-engineering)
    - [Retrieval-Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
    - [Tool Use / Function Calling](#tool-use--function-calling)
    - [Fine-Tuning / Instruction Tuning](#fine-tuning--instruction-tuning)
    - [Output Constraints](#output-constraints)
    - [Post-Processing Validation](#post-processing-validation)
    - [Confidence \& Citations](#confidence--citations)

---

## Hallucination

- `Hallucination`
  - when a `large language model (LLM)` generates information that is **incorrect, fabricated, or not grounded in reality**, yet presents it as if it were true.

> In short: _confident-sounding nonsense or unsupported claims._

---

## Causes

Hallucination is not a bug—it’s a **byproduct of how LLMs are trained**.

- **Probabilistic Nature**
  - LLMs predict the **next most likely token**, not the “true” answer
  - No built-in fact-checking mechanism

- **Training Objective Mismatch**
  - Objective: **minimize prediction error (loss)**
  - Not: ensure factual correctness

- **Incomplete / Noisy Training Data**
  - Training data may contain:
    - Errors
    - Conflicting information
    - Gaps in knowledge

- **Lack of Grounding**
  - No real-time connection to:
    - Databases
    - External APIs
    - Verified sources (unless explicitly integrated)

- **Overgeneralization**
  - Models **pattern-match aggressively**
  - Fill missing details using learned patterns → can fabricate

- **Prompt Ambiguity**
  - Vague or underspecified prompts → model “guesses”

---

## Types of Hallucination

- **Factual Hallucination**
  - Incorrect facts
  - Example: wrong dates, wrong definitions

- **Fabricated Content**
  - Completely made-up information
  - Example: fake papers, fake APIs, fake commands

- **Contextual Hallucination**
  - Contradicts given input/context
  - Example: ignoring constraints in prompt

- **Logical Hallucination**
  - Reasoning errors
  - Example: flawed step-by-step logic

- **Citation Hallucination**
  - Fake references or sources
  - Common in academic-style answers

- **Instruction Drift**
  - Ignores or partially follows instructions

---

## How to Detect & Evaluate Hallucination

- **Human Evaluation (Most Reliable)**
  - Domain expert verification
  - **Checklist**
    - Is it factually correct?
    - Is it supported by evidence?
    - Does it follow instructions?

---

- **Automatic Evaluation Methods**
  - a. **Ground Truth Comparison**
    - Compare output vs. known correct answer
    - **Metrics**
      - Exact Match (EM)
      - F1 Score

  - b. **Retrieval-Based Verification**
    - Cross-check with trusted sources (RAG)
    - If unsupported → likely hallucination

  - c. **Self-Consistency Check**
    - Ask model multiple times
    - If answers vary → low reliability
  - d. **LLM-as-a-Judge**
    - Use another model to verify:
      - factuality
      - consistency

---

- **Signal-Based Detection**

Look for patterns like:

- Overly confident tone with no evidence
- Specific details without sources
- Inconsistent answers across runs
- “Looks right” but unverifiable

---

## How to Reduce Hallucination

### Prompt Engineering

**Good practices**

- Be specific and constrained
- Ask for uncertainty handling

```txt
If you are unsure, say "I don’t know".
Only answer based on the provided context.
```

### Retrieval-Augmented Generation (RAG)

Inject external knowledge into the prompt to ground responses in real data.

**Flow:**

1. **Retrieve** relevant documents.
2. **Provide** documents as context.
3. **Generate** an answer based on that context.

---

### Tool Use / Function Calling

Allow the model to interact with external systems to replace "guessing" with real-time data retrieval:

- **APIs**
- **Databases**
- **Search engines**

---

### Fine-Tuning / Instruction Tuning

Train the model on specialized datasets to improve performance:

- **High-quality** examples.
- **Domain-specific** knowledge.
- **Verified** data.

---

### Output Constraints

Use structured outputs to force the model to be more precise:

- **JSON schema** enforcement.
- **Required fields** definitions.

---

### Post-Processing Validation

Add a verification layer after the model generates a response:

- **Rule-based checks** (e.g., regex, data types).
- **External validation** (e.g., running code, checking a database).
- **Secondary model review** (using a critic model).

---

### Confidence & Citations

Improve transparency by asking the model to:

- **Provide sources** for its claims.
- **Estimate confidence** levels in its answers.

```txt
Include references for each claim.
If no source is available, say so.
```
