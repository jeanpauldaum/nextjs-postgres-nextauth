---
name: design-engineer-tools
description: >
  Master index of design-engineer tooling from designengineer.tools (James Warner
  curated list) plus how to pick Inspiration, Components, Motion, Web Utility,
  Interface, 3D/glTF, AI Code, and related agent skills. Use when choosing design
  tools, building polished web UI, researching motion/components, or running
  /design-engineer-tools /de-tools /designengineer.
---

# Design Engineer Tools (catalog skill)

**Source:** [designengineer.tools](https://designengineer.tools/) — curated by James Warner.  
**Shape:** Single-page directory of **outbound tools** (not multi-page product docs).  
**Local catalog:** `references/catalog.json` (20 categories, ~126 tools).

## When to load this skill

- User asks for design-engineer tooling, component libraries, motion stacks, inspiration sources
- Building marketing/product UI and needs **craft stack**, not generic AI UI
- Deciding open-source code adoption vs commercial SaaS only

## Bot handoff (site design pack)

Full pack for any Grok bot: `references/GROK_BOTS_SITE_DESIGN.md`  
Also indexed in global MEMORY and `umli/AGENTS.md`.

**Default path:** `/de-tools` → `/craft` → components → `/motion-craft`.

## Companion skills (install / load)

| Skill | Role |
|-------|------|
| `design-engineer-craft` | Inspiration → craft playbook, anti-slop, ship checklist |
| `design-engineer-components` | shadcn, React Bits, Motion Primitives, NumberFlow |
| `design-engineer-motion` | Easing, Motion, Theatre, Lottie, reduced-motion |
| `design-engineer-3d` | gltfjsx, gltfpack, Rive/Spline boundaries |
| `design-engineer-interface` | Figma/Framer/Penpot/Rive decision tree |
| `design-engineer-ai-code` | Cursor/v0/skills.sh vs local craft skills |
| `design-engineer-type-visual` | Fonts + shader boundaries |
| `human-centered-product-taste` | Taste / anti-generic AI |
| `vercel-react-best-practices` | Perf for React/Next |
| `shadcn` (plugin) | shadcn CLI/theming if available |
| `imagine` | Image gen when art > code charts |

## Category map (from designengineer.tools)

1. **Inspiration** — 60fps, Godly, Mobbin, Design Spells, HUDS+GUIS, Minimal Gallery, Saaspo…  
2. **AI Code** — Cursor, Claude Code, v0, Codex, skills.sh, Bolt, Windsurf, Zed  
3. **Components** — shadcn/ui, React Bits, Motion Primitives, NumberFlow, 21st.dev, Fancy Components  
4. **Web Utility** — OKLCH, Color.review, easings.net, easing gradients, SVGOMG, Ray.so  
5. **Desktop Utility** — Raycast, Warp, Granola, LocalSend, Wispr, Deskflow  
6. **Video & Capture** — OBS, Screen Studio, LosslessCut, OpenCut, ShareX  
7. **Whiteboard** — Excalidraw, tldraw, FigJam, Miro  
8. **Organization** — Linear, Obsidian, AFFiNE, Are.na, Eagle  
9. **Fonts** — Fontshare, Free Faces, Fonts In Use, UNCUT  
10. **Visual** — ShaderToy, NodeToy, cables.gl, Unicorn.studio, TouchDesigner  
11. **Interface** — Figma, Framer, Penpot, Rive, Paper, Stitch  
12. **Motion** — Theatre.js, Jitter, Lottie Creator, Lottielab, Cavalry  
13. **Audio** — ElevenLabs, FMOD, Splice  
14. **Volumetric** — Luma, Polycam, SuperSplat, RealityScan  
15. **3D** — Blender, Spline, Houdini, Bezi, Womp  
16. **glTF** — gltfjsx, gltfpack, Needle Viewer  
17. **Digital Fashion** — CLO, Marvelous Designer, Style3D  
18. **Research** — ChatGPT, Gemini, NotebookLM  
19. **Browser** — Arc, Brave, Firefox, Zen  
20. **Emoji** — MakeEmoji  

Full name→URL list: `references/catalog.json`.

## Open-source priority (code agents can adopt)

| Tool | Repo / entry | Adopt how |
|------|----------------|-----------|
| shadcn/ui | github.com/shadcn-ui/ui | CLI copy into project; own the code |
| React Bits | github.com/DavidHDev/react-bits | Copy-paste / shadcn registry; **MIT + Commons Clause** — no selling the component lib itself |
| Motion Primitives | github.com/ibelick/motion-primitives | Motion + Tailwind primitives |
| NumberFlow | github.com/barvian/number-flow | Animated numbers |
| Theatre.js | github.com/theatre-js/theatre | Timeline animation authoring |
| tldraw | github.com/tldraw/tldraw | Canvas / whiteboard SDK |
| Excalidraw | github.com/excalidraw/excalidraw | Diagram embed |
| gltfjsx | github.com/pmndrs/gltfjsx | glTF → React Three Fiber |
| gltfpack | github.com/zeux/meshoptimizer | Compress glTF |
| Penpot | github.com/penpot/penpot | Open design tool |
| skills.sh | skills.sh | Discover installable agent skills |

**Commercial-only** (recommend product, don’t “extract source”): Figma, Framer, Mobbin, Screen Studio, Jitter, Spline (hosted), most Desktop/Video SaaS.

## Agent workflow (default)

```
1. Intent: marketing page | product UI | motion | 3D | pitch visual
2. Load design-engineer-craft for quality bar + anti-slop
3. Components: prefer shadcn primitives + selective React Bits / Motion Primitives
4. Color: OKLCH tokens; check contrast (color.review mindset)
5. Motion: easings.net curves; respect prefers-reduced-motion
6. Inspiration: 2–3 refs from Godly/60fps/Mobbin/Design Spells — then original execution
7. Never dump v0/Bolt output without human-centered-product-taste pass
```

## skills.sh design-related installs (optional)

```bash
# examples — run only if user wants ecosystem skills
npx skills add vercel-labs/agent-skills   # web-design-guidelines, composition
npx skills add anthropics/skills         # frontend-design (if published path)
npx skills add shadcn/ui                 # shadcn skill when available
```

Prefer **Grok local skills** in `~/.grok/skills/design-engineer-*` for FleetScale work so stack stays coherent.

## Anti-patterns

- Treating designengineer.tools as if every link has scrapable source  
- Installing 100 SaaS tools as “skills”  
- Copying animated React Bits into every page (weight + noise)  
- Ignoring licenses (Commons Clause on React Bits)  
- Fake dashboards / neon cyberpunk “AI design”

## FleetScale defaults

- Site tokens: porcelain `#F7F8FB`, ink `#12141A`, brand `#4F6CF7`  
- Prefer **code-built UI** over Imagine for exact layout; Imagine for photography/mood  
- Pitch decks: `pptx` + `fleetscale-pitch-narrative` + craft skills  

## Slash

`/design-engineer-tools` · `/de-tools`
