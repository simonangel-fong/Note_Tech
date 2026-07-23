# LLM - Prompt & Prompt Engineering

[Back](../index.md)

- [LLM - Prompt \& Prompt Engineering](#llm---prompt--prompt-engineering)
  - [prompt engineering](#prompt-engineering)
    - [Component of well-designed prompt](#component-of-well-designed-prompt)
    - [reusable prompt structure](#reusable-prompt-structure)
  - [Types](#types)

---

## prompt engineering

- `prompt`
  - the **input** given to a large language model so it can produce an output.
- LLM reads the `prompt` and **predicts** the most likely next tokens.

---

- `prompt engineering`
  - the **practice of designing and improving** `prompts` so an LLM produces more useful, accurate, consistent, and appropriately formatted results.
- Prompt engineering = **communicating the task clearly** to the LLM

---

### Component of well-designed prompt

- **Role**
  - The perspective the model should take.
  - can help guide tone and priorities, but it does not give the model special knowledge or permissions.
- **Task**
  - What the model should do.
- **Context**
  - Background information about the situation.
- **Input**
  - The data the model should work with.
- **Constraints**
  - Rules or boundaries.
- **Output format**
  - How the response should be structured.
- **Examples**
  - Examples can show the model what good output looks like.

---

### reusable prompt structure

```txt
Role:
You are a [role].

Task:
[Describe what you want done.]

Context:
[Provide relevant background.]

Input:
[Provide the content or data.]

Constraints:
[Explain limits, rules, and exclusions.]

Output:
[Describe the desired format and level of detail.]
```

- example

```txt
Role:
You are a senior Kubernetes engineer.

Task:
Analyze why the application pod is failing.

Context:
The application runs on EKS in the payments namespace.
It was working before the latest Helm deployment.

Input:
Pod status: CrashLoopBackOff

Log:
Missing required environment variable DATABASE_URL

Constraints:
Use only the evidence provided.
Do not assume the database itself is unavailable.
Do not suggest destructive commands.

Output:
Return:
1. Likely root cause
2. Supporting evidence
3. Verification steps
4. Recommended fix
```

---

## Types

- `System prompt`
  - defines high-level behavior and rules.
  - application usually controls this message.

- `User prompt`
  - contains the user's request.

- `Assistant message`
  - Previous assistant responses may also be included in the conversation context.
