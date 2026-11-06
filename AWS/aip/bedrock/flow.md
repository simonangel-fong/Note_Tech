# Amazon Bedrock: Flow

[Back](../index.md)

- [AIP: Amazon Bedrock](#aip-amazon-bedrock)
  - [Bedrock](#bedrock)
    - [Bedrock IAM permissions](#bedrock-iam-permissions)
  - [Lab: Bedrock - Playground](#lab-bedrock---playground)
  - [Converse API](#converse-api)
  - [Fine-tuning in Bedrock: “Custom Models”](#fine-tuning-in-bedrock-custom-models)
  - [Prompt Management](#prompt-management)
    - [Prompt Flows](#prompt-flows)
    - [Bedrock Flows with Prompts](#bedrock-flows-with-prompts)
  - [Lab: Prompt Management](#lab-prompt-management)

---

## Flow

- `Flows`
  - a visual, **no-code orchestration** feature in Amazon Bedrock that lets developers build, test, and deploy multi-step **generative AI workflows**.

- How It Works
  - use a drag-and-drop **visual builder** to connect modular blocks (called nodes):
    - `Prompt Nodes`: Interact with Foundation Models (such as Claude) to generate text or classify inputs.
    - `Condition Nodes`: Route logic down different paths based on rules or criteria.
    - `Knowledge Base Nodes`: Retrieve information from your own data sources.
    - `Code Nodes`: Execute custom logic using AWS Lambda functions.
    - `AI Services Nodes`: Connect external services like Amazon Lex.
    - `Guardrails`: Apply safety controls—such as masking personally identifiable information (PII)—to inputs and outputs.
