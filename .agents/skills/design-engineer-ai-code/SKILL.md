---
name: design-engineer-ai-code
description: >
  When design engineers should use Cursor, Claude Code, v0, Bolt, Codex, Windsurf,
  Zed, or skills.sh — and how Grok Build skills complement them without unedited
  AI UI dumps. Use for AI coding tool choice, v0 cleanup, or /design-engineer-ai-code.
---

# Design Engineer — AI Code Tools

Catalog origin: designengineer.tools **AI Code**.

## Tool roles

| Tool | Best for | Don’t |
|------|----------|--------|
| **Cursor / Windsurf / Zed** | Daily IDE agentic edit | Treating IDE as design system owner |
| **Claude Code / Codex / Cline** | Repo-wide agent tasks | Silent force-push without review |
| **v0 / Bolt** | Fast layout prototypes | Shipping raw output as brand UI |
| **skills.sh** | Discover installable agent skills | Installing 50 conflicting skills |
| **Grok Build skills** | Procedural craft + company context | Ignoring FleetScale tokens/narrative |

## Agent rules

1. Prototype in v0/Bolt → **rebuild** with `design-engineer-craft` + brand tokens  
2. Prefer project/user **Grok skills** for FleetScale over random leaderboard skills  
3. `npx skills add <owner/repo>` only with user intent and license check  
4. Pair AI code with `verification-before-completion` and visual QA  
5. Never invent “design system” from one generated page  

## skills.sh highlights (design-adjacent)

See `design-engineer-tools` and optional installs:

- vercel-labs/agent-skills (web-design-guidelines, react best practices)  
- taste / anti-ui-slop skills if user wants extra taste packs  
- shadcn skill when available  

## Slash

`/design-engineer-ai-code`
