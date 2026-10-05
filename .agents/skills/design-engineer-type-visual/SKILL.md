---
name: design-engineer-type-visual
description: >
  Fonts and visual/shader tools for design engineers: Fontshare, Fonts In Use,
  free font licensing, ShaderToy/NodeToy/Unicorn.studio boundaries for web.
  Use when picking type, free fonts, or web shaders, or /design-engineer-type.
---

# Design Engineer — Type & Visual

Catalog origin: designengineer.tools **Fonts** + **Visual**.

## Fonts

| Source | Use |
|--------|-----|
| [Fontshare](https://www.fontshare.com/) | Quality free fonts with clear licenses |
| [Free Faces](https://www.freefaces.gallery/) | Discovery |
| [Fonts In Use](https://fontsinuse.com/) | Real-world pairing references |
| [UNCUT](https://uncut.wtf/) | Indie type |
| [Best Free Fonts](https://bestfreefonts.com/) | Aggregation |

### Agent rules

1. Always check **license** (OFL vs personal-only) before embedding in production  
2. Max **two families** per marketing site (display + body)  
3. Prefer variable fonts when weight flexibility needed and size OK  
4. Self-host fonts for privacy/perf when possible  
5. FleetScale: keep existing Die Grotesk / Georgia system unless brand changes  

## Visual / shader tools

| Tool | Web production? |
|------|-----------------|
| ShaderToy / NodeToy / cables | **Prototype** shaders; port carefully |
| Unicorn.studio | Marketing web effects — weigh bundle |
| TouchDesigner | Offline / install base — not default web |
| Bitspace / Nodes | Creative coding — export assets |

### Rules

- Prefer CSS/canvas/WebGL **only if** craft requires it  
- Always provide non-WebGL fallback  
- Export stills/video when interaction isn’t needed  

## Slash

`/design-engineer-type`
