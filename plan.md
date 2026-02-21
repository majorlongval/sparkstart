# Plan: sparkstart as an MCP Tool for Claude Code

## Goal

Expose `sparkstart` as a set of tools consumable by Claude Code (and any
MCP-compatible host such as GitHub Copilot / Codex) via the
[Model Context Protocol](https://modelcontextprotocol.io).
After setup, an AI assistant can call `create_project`, `delete_project`, etc.
as first-class tools during a conversation.

---

## Architecture

**Approach: Direct Python integration (Option A)**

Add an `mcp_server.py` module inside the existing `sparkstart` package that
imports and calls `core.py` directly — no subprocess overhead, full access to
internals and structured return values.

A thin entry point (`sparkstart-mcp` / `sparkstart serve-mcp`) starts the
server so users can point their MCP host at it.

---

## Open Questions (decide before coding)

1. **Working directory** — Should `create_project` create the project relative
   to the MCP server's `cwd`, or accept an explicit `parent_dir` parameter?
   *(Recommendation: accept `parent_dir`, default to `cwd`.)*

2. **GitHub token in headless mode** — No interactive prompt is possible via
   MCP.  Read `GITHUB_TOKEN` env var only, or also accept a `token` parameter?
   *(Recommendation: env var only, document clearly.)*

3. **Return value of `create_project`** — Return the absolute path of the
   created directory so the AI can `cd` into it or open it.

4. **Standalone package?** — Keep everything inside `sparkstart`, or publish a
   separate `sparkstart-mcp` PyPI package?
   *(Recommendation: keep in `sparkstart` for now, revisit if adoption grows.)*

---

## Tools to Expose

```
create_project
  name          str   required
  language      enum  python | rust | javascript | cpp   (default: python)
  template      enum  pygame | none                       (optional)
  tutorial      bool  (default: false)
  devcontainer  bool  (default: false)
  tools         bool  (default: false)
  github        bool  (default: false)
  parent_dir    str   (default: cwd)

delete_project
  name          str   required
  github        bool  (default: false)

list_options
  → returns available languages, templates, and feature flags

check_environment
  → returns availability of Docker, Git, VS Code
```

---

## Files to Create / Modify

| Action     | File                           | What changes                                              |
|------------|--------------------------------|-----------------------------------------------------------|
| **NEW**    | `sparkstart/mcp_server.py`     | MCP server: tool schemas + handlers calling `core.py`     |
| **MODIFY** | `pyproject.toml`               | Add `mcp` optional dep + `sparkstart-mcp` entry point     |
| **MODIFY** | `sparkstart/cli.py`            | Add `serve-mcp` Typer sub-command                         |
| **MODIFY** | `README.md`                    | Add "Use with Claude Code / MCP" section                  |
| **NEW**    | `docs/mcp-integration.md`      | Full setup guide + `.mcp.json` example                    |

---

## Phase Breakdown

### Phase 1 — MCP server module

File: `sparkstart/mcp_server.py`

- Install/add dependency: `mcp>=1.0` (the official Python MCP SDK)
- Use `@server.tool()` decorators to define each tool with a JSON schema
- Call `sparkstart.core` functions directly (skip the Typer CLI layer)
- Return structured dicts: `{success, message, project_path, files_created, next_steps}`
- Handle exceptions gracefully and surface them as MCP error responses

```python
# Rough sketch
from mcp.server import Server
from mcp.server.stdio import stdio_server
import sparkstart.core as core

server = Server("sparkstart")

@server.tool()
async def create_project(name: str, language: str = "python", ...) -> dict:
    ...

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())
```

### Phase 2 — Package wiring

`pyproject.toml`:
```toml
[project.optional-dependencies]
mcp = ["mcp>=1.0"]

[project.scripts]
sparkstart     = "sparkstart.cli:app"
sparkstart-mcp = "sparkstart.mcp_server:main"
```

`sparkstart/cli.py` — add:
```python
@app.command("serve-mcp")
def serve_mcp():
    """Start the sparkstart MCP server (for Claude Code / Codex integration)."""
    import asyncio
    from sparkstart.mcp_server import main
    asyncio.run(main())
```

Install with MCP support:
```bash
pip install "sparkstart[mcp]"
```

### Phase 3 — Claude Code / MCP host configuration

Users add to `.mcp.json` (project-level) or `~/.claude/mcp.json` (global):

```json
{
  "mcpServers": {
    "sparkstart": {
      "command": "sparkstart-mcp"
    }
  }
}
```

After restarting Claude Code, the tools appear automatically.

### Phase 4 — Docs & tests

- `docs/mcp-integration.md`: prerequisites, install steps, `.mcp.json` snippet,
  per-tool usage examples, token setup for GitHub integration.
- `README.md`: short "Claude Code" section linking to the full guide.
- `tests/test_mcp_server.py`: unit tests for each tool handler (mock `core.py`
  calls, assert return shape).
- Manual smoke-test checklist: start server, run Claude Code, ask it to create
  a Python project, verify directory is created.

---

## Success Criteria

- [ ] `sparkstart-mcp` starts without error and lists tools via MCP
- [ ] Claude Code shows `create_project`, `delete_project`, `list_options`,
      `check_environment` in its tool list
- [ ] `create_project` creates a correctly scaffolded directory
- [ ] `delete_project` removes it (with confirmation handled by the AI)
- [ ] `list_options` returns current languages/templates without side effects
- [ ] GitHub integration works when `GITHUB_TOKEN` is set in environment
- [ ] All existing `sparkstart` tests still pass
- [ ] Docs are clear enough for a first-time user to set up in < 5 minutes
