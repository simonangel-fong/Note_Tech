# Guiding Principle & Guardrails

[Back](./index.md)

- [Guiding Principle \& Guardrails](#guiding-principle--guardrails)
  - [AI Guiding Principle](#ai-guiding-principle)
  - [Guardrail](#guardrail)
    - [Types of AI Guardrails](#types-of-ai-guardrails)
      - [Input Guardrails (Pre-processing)](#input-guardrails-pre-processing)
      - [Output Guardrails (Post-processing)](#output-guardrails-post-processing)
      - [Policy-Based Guardrails](#policy-based-guardrails)
      - [Contextual Guardrails](#contextual-guardrails)
      - [Tool / Action Guardrails (Critical for AI Agents)](#tool--action-guardrails-critical-for-ai-agents)
  - [How Guardrails Are Implemented](#how-guardrails-are-implemented)
      - [Rule-Based Filters](#rule-based-filters)
      - [ML-Based Moderation](#ml-based-moderation)
      - [Prompt Engineering](#prompt-engineering)
      - [Human-in-the-Loop](#human-in-the-loop)

---

## AI Guiding Principle

- **Veracity & Robustness**
  - to achieve correct output
  - reduce hallucination

- **Safety**
  - prevent harmful system output and misuse
    - `toxicity`: the offensive, discriminatory or harmful content

- **Privacy and Security**
  - protect data and models
  - prevent leaks of PII data or confidential data, copyright infringement

- **Explainability**
  - ensure decision making can be traced and explained

- **Fairness**
  - ensure diversity

- **Transparency**
  - Communicate info about AI system to stakeholders

- **Controllability**
  - monitor and steer AI behavior

- **Governance**
  - incorporate best practices into the AI supply chain.

---

## Guardrail

- `Guardrails`
  - **rules, filters, and control mechanisms** designed to ensure an AI system **behaves safely, ethically**, and within intended boundaries, and **ensure the reliability, safety**, and compliance of large language models (LLMs) by implementing validation checks on input and output data.

---

### Types of AI Guardrails

```txt
ser Input → [Input Guardrails] → AI Model → [Output Guardrails] → User
                               ↓
                        [Action Guardrails]
```

#### Input Guardrails (Pre-processing)

Control what users are allowed to send into the AI.

**Examples:**

- Block malicious prompts (e.g., prompt injection)
- Filter sensitive data (passwords, personal info)
- Reject disallowed topics

**Example Scenario:**

> User tries to request illegal instructions → blocked before reaching the model

---

#### Output Guardrails (Post-processing)

Filter or modify the AI’s response before returning it.

**Examples:**

- Remove harmful content
- Detect hallucinations
- Enforce tone (professional, neutral)

**Example Scenario:**

> AI generates unsafe advice → system rewrites or blocks it

---

#### Policy-Based Guardrails

Rules defined by organizations or platforms.

**Examples:**

- No hate speech
- No illegal guidance
- Restricted domains (e.g., medical/legal advice)

Used heavily in enterprise AI systems.

---

#### Contextual Guardrails

Limit AI behavior based on **user role or scenario**.

**Examples:**

- Admin vs normal user permissions
- Internal tool vs public chatbot
- Region-based restrictions

---

#### Tool / Action Guardrails (Critical for AI Agents)

Control what actions an AI agent can take.

**Examples:**

- Restrict API calls
- Limit file access (read-only vs write)
- Prevent destructive operations (e.g., deleting data)

---

## How Guardrails Are Implemented

#### Rule-Based Filters

- Regex, keyword matching
- Fast but limited

#### ML-Based Moderation

- Classifiers detect harmful content
- More flexible than rules

#### Prompt Engineering

Define behavior via system instructions.

```text
You are a DevOps assistant.
Do not suggest destructive commands.
Do not expose secrets.
```

#### Human-in-the-Loop

Require approval for critical or high-risk actions
