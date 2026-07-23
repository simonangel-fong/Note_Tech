# LLM - MCP

[Back](../index.md)

- [LLM - MCP](#llm---mcp)
  - [Tool calling](#tool-calling)
  - [MCP](#mcp)

---

## Tool calling

- `Tool calling`
  - a mechanism that lets an LLM **request** that an **application** execute an external function.

- The `LLM` **selects and requests** the tool.
- The surrounding application actually **executes** it.

- simple tool definition:
  - A name
  - A description
  - Input parameters
  - Parameter types
  - Required fields

- sample

```json
{
  "name": "get_weather",
  "description": "Get current weather for a city",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string"
      }
    },
    "required": ["city"]
  }
}
```

- LLM request:

```json
{
  "tool": "get_weather",
  "arguments": {
    "city": "Toronto"
  }
}
```

---

## MCP

- `Model Context Protocol(MCP)`
  - an open standard for connecting AI applications to **external data, tools, and workflows** through a common protocol.
  - standardizes how an AI application discovers and **communicates with external capabilities**.
    - reduce integration complexity
    - improve interoperability.

- architecture

```
User
  ↓
MCP Host
  ↓
MCP Client
  ↓
MCP Server
  ↓
External system
```

- `MCP host`
  - The application the user interacts with.
  - manages the **user** experience, **model** interaction, permissions, and **connections** to `MCP servers`.
  - e.g., AI chatbot, AI-enabled IDE

- `MCP client`
  - A protocol component **inside the host**.
  - communicates with one `MCP server` and handles protocol messages.

- `MCP server`
  - A program that **exposes capabilities** through MCP.
  - wrap an existing API, CLI, database, filesystem, or service. MCP servers expose capabilities using standardized interfaces.
  - e.g., GitHub API, Kubernetes API server, PostgreSQL, Local filesystem, AWS APIs

- MCP servers primarily expose three categories:

| MCP primitive | Purpose                            |
| ------------- | ---------------------------------- |
| Tools         | Perform an operation               |
| Resources     | Supply data or context             |
| Prompts       | Supply reusable workflow templates |
