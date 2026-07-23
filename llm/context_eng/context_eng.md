# LLM - Context & Context Engineering

[Back](../index.md)

- [LLM - Context \& Context Engineering](#llm---context--context-engineering)
  - [Context Engineering](#context-engineering)
    - [Layers](#layers)
    - [Prompt engineering vs. context engineering](#prompt-engineering-vs-context-engineering)

---

## Context Engineering

- `Context`
  - all the information an AI model can **use when generating its next response**.
  - Information available to the model during the current request.

- Sources of context:
  - system instructions
  - user's current question
  - chat history
  - Documents or data retrieved from external sources (RAG)
  - Tool results, such as an API response (Tool calling / MCP)
  - Examples showing the expected output (Prompt)
  - Information about the task, user, environment, and constraints (Guardrails)

- AI output = model + current context

---

### Layers

- **Instructions**
  - What the AI should do
- **Role**
  - What perspective the AI should use
- **Environment**
  - Facts about the system:
- **Task state**
  - What is happening now
- **Evidence**
  - Logs, metrics, events, manifests, code, or API results:
- **History**
  - Relevant previous actions
- **Constraints**
  - What the AI must or must not do
- **Output format**
  - How the answer should be returned

---

- context template

```yaml
role: You are a Kubernetes troubleshooting assistant.

goal: Identify the likely cause of the application failure.

environment:
  platform: AWS EKS
  namespace: payments
  deployment_tool: Argo CD

current_state:
  deployment_status: unavailable
  pod_status: CrashLoopBackOff

evidence:
  logs: ...
  events: ...
  recent_changes: ...

actions_already_taken:
  - checked pod status
  - checked service endpoints

constraints:
  - read-only investigation
  - redact credentials
  - do not restart workloads
  - do not guess when evidence is insufficient

available_tools:
  - get_pods
  - get_events
  - get_logs
  - get_deployment_diff

expected_output:
  - incident summary
  - likely root cause
  - supporting evidence
  - confidence level
  - recommended next action
```

---

- `context window`
  - the **maximum amount of information** the model can process at one time.

- usually contains:
  - System instructions
  - conversation history
  - user request
  - retrieved documents
  - tool outputs
  - generated response

---

- `context engineering`
  - the process of **designing, selecting, organizing, and updating the information** given to an AI model so it can complete a task reliably.

- mindset
  - What information should the model receive?
  - Where should it come from?
  - How should it be structured?
  - When should it be updated?
  - What should be removed?

---

### Prompt engineering vs. context engineering

- `Prompt engineering`
  - Focuses mainly on the **instruction itself**
  - Focuses on the complete **input package**
