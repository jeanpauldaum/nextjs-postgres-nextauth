# Site design skills — handoff for Grok bots

**Audience:** any agent working on marketing/product UI, especially **fleetscale.co** / `umli`.  
**Installed (cloud):** repo `.grok/skills/` and `.agents/skills/` on `jeanpauldaum/umli` — Cursor / CoS / Grok load from GitHub.  
**Source:** [designengineer.tools](https://designengineer.tools/) (James Warner curated directory ~126 tools / 20 categories) → **adoption skills**, not a site dump.

---

## Default agent path (site design)

```
/de-tools  (or design-engineer-tools)   → pick stack / catalog
       ↓
/craft  (design-engineer-craft)        → quality bar, anti-slop, ship checklist
       ↓
/design-engineer-components            → shadcn + selective React Bits / Motion Primitives
       ↓
/motion-craft  (design-engineer-motion)→ animate carefully; reduced-motion
```

Load **taste / product** layers when quality, voice, or brand is at stake:

| Skill | Slash | When |
|-------|--------|------|
| `human-centered-product-taste` | `/taste` | Anti-generic AI; human experience |
| `product-ownership` | `/product-ownership` | Frame before polish |
| `quality-first-authorship` | `/quality-first-authorship` | Human vs agent vs model for assets |
| `fixed-vs-adaptive-surfaces` | `/fixed-vs-adaptive` | Fixed shell vs live personalization |
| `avery-site-concierge` | `/avery-site-concierge` | Avery voice rail on fleetscale.co (project: `umli/.grok/skills/`) |

---

## Core pack (8 skills under `~/.grok/skills/`)

| Skill directory | Slash aliases | Role |
|-----------------|---------------|------|
| `design-engineer-tools` | `/de-tools` `/designengineer` | Master index + `references/catalog.json` |
| `design-engineer-craft` | `/craft` | Inspiration workflow, OKLCH/contrast, anti-slop, pre-ship UI checklist |
| `design-engineer-components` | `/react-bits` `/shadcn-components` | shadcn, React Bits, Motion Primitives, NumberFlow, 21st.dev — license-aware |
| `design-engineer-motion` | `/motion-craft` | Motion vs Lottie vs Theatre vs Rive; easings; reduced-motion |
| `design-engineer-3d` | `/gltf` | gltfjsx, gltfpack, poster fallbacks, Rive/Spline boundaries |
| `design-engineer-interface` | `/figma-vs-code` | Figma vs code-first, Framer, Penpot, Rive, Stitch |
| `design-engineer-ai-code` | `/design-engineer-ai-code` | Cursor/v0/Bolt/skills.sh vs local Grok craft skills |
| `design-engineer-type-visual` | `/design-engineer-type` | Fonts (Fontshare…), shaders; license + self-host |

**Artifacts:**

- Catalog: `~/.grok/skills/design-engineer-tools/references/catalog.json`
- Inspiration routing: `…/references/inspiration-routing.md`
- skills.sh optional list: `…/references/skills-sh-top12.md`
- Project mirror: `umli/docs/design-engineer-tools/INDEX.md`

---

## FleetScale site defaults

- **Live:** fleetscale.co · **repo:** `jeanpauldaum/umli` · **ship owner: Grok Bot CoS** (`fleetscale-ship-site`). Never `./scripts/deploy-site.sh` on a laptop.
- **Tokens:** porcelain `#F7F8FB`, ink `#12141A`, brand `#4F6CF7` (Institutional Night / capital-grade calm)
- **React stack adopt order:** shadcn → React Bits (selective) → NumberFlow → Motion Primitives → Fancy (sparingly) → 21st (audit) → Theatre/gltfjsx only if needed
- **React Bits on fleetscale.co:** restraint — one signature moment. Live: MetallicPaint, Beams. Pocket catalog: `docs/design-engineer-tools/REACT_BITS_POCKET.md`. Do not merge the 115 MB zip.
- **React Bits license:** MIT + **Commons Clause** — use in apps; do not resell the kit
- **Fonts:** max two families; self-host; check license; keep Die Grotesk / Georgia unless brand changes (watch decode/CORS failures on prod)
- **Prefer local `design-engineer-*` over skills.sh** so brand tokens stay pinned
- **Code for layout; Imagine for photography/mood** — not for exact UI chrome
- **Pitch decks (related):** `pptx` + `fleetscale-pitch-narrative` + craft rules; deck craft ≠ full web motion stack

---

## Parallel review pattern (site polish)

When reviewing or shipping UI, prefer **specialized parallel subagents** over one mega-pass:

1. craft / anti-slop  
2. motion + reduced-motion  
3. type / visual  
4. components / bloat  
5. a11y + Chrome DevTools  
6. product taste / fixed-vs-adaptive (if voice or personalization)

---

## What NOT to do

- Unedited v0/Bolt dumps as brand UI  
- Neon cyberpunk / purple fog “AI design”  
- Stacking every React Bit on one page  
- Treating designengineer.tools as scrapable monorepo source  
- Ignoring `prefers-reduced-motion` or contrast  
- Inventing a design system from one generated page  

---

## Project rules

- FleetScale agent rules: `~/umli/AGENTS.md`  
- Avery voice: `umli/.grok/skills/avery-site-concierge`  
- Global memory also records this pack under **Site design skill pack**

*Last written for bot handoff: 2026-08-11*
