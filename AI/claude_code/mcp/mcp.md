# Claude Code - MCP

[Back](../index.md)

- [Claude Code - MCP](#claude-code---mcp)
  - [MCP](#mcp)

---

## MCP

- ref: https://context7.com/

```sh
# add Context7 MCP server
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY

# confirm
claude mcp list
# context7: npx -y @upstash/context7-mcp --api-key api_key - ✔ Connected
```

- use mcp
  - cc

```sh
list tools for context7
what is the latest version of langGraph? use context7
```