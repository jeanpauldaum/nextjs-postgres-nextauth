---
name: design-engineer-interface
description: >
  Design-tool decision tree for design engineers: Figma vs code-first, Framer,
  Penpot, Rive, Paper, Stitch. When agents design vs implement. Use when choosing
  design tooling, Figma handoff, or /design-engineer-interface /figma-vs-code.
---

# Design Engineer Interface Tools

Catalog origin: designengineer.tools **Interface** + **Whiteboard**.

## Decision tree

```
Shipping production app/marketing site in React?
  → Design tokens + implement in code (shadcn / CSS)
  → Figma optional for exploration / stakeholder comps

Stakeholder workshop / flow diagram?
  → FigJam or Excalidraw or tldraw

Open-source design tool requirement?
  → Penpot

Interactive vector state machine (icons, characters)?
  → Rive export to web runtime

Marketing site mostly editorial with CMS?
  → Code or Framer — Framer if non-dev editors own page

Google Stitch / AI layout?
  → Prototype only; rebuild with craft before production
```

## Figma

- Primary industry design surface  
- Agents: use Figma MCP skills when user has file access (`figma-use`, `figma-design-to-code`)  
- Code Connect for mapping components — don’t invent mappings  
- Never claim pixel-perfect without screenshot QA  

## Framer

- Great for marketing owned by designers  
- Don’t dual-maintain Framer + custom React for same page without reason  

## Penpot

- Open-source alternative — github.com/penpot/penpot  
- Prefer when org wants self-host / OSS  

## Rive

- Interactive motion graphics  
- Prefer over Lottie when inputs/state machines needed  
- Export carefully; test reduced motion  

## Whiteboard

| Tool | Use |
|------|-----|
| Excalidraw | Quick diagrams, OSS embed |
| tldraw | Product canvas / SDK |
| FigJam | Team workshops |
| Miro | Enterprise workshops |

## Agent rules

1. Don’t block implementation waiting for perfect Figma if tokens are clear  
2. Don’t rebuild Figma auto-layout pixel noise — implement clean responsive structure  
3. Diagrams for architecture: Excalidraw/tldraw over screenshots of whiteboards  
4. Pair with `design-engineer-craft` before polish  

## Slash

`/design-engineer-interface`
