---
name: quality-first-authorship
description: >
  Use when deciding who should create content or assets (human vs agent vs model);
  when voice, video, hero copy, or brand-critical surfaces need quality; when
  pre-record vs live generation, static vs dynamic, or transferring authorship to
  the human would improve the product. Also /quality-first-authorship.
---

# Quality-first authorship

## Overview

**Put the right author on the right layer.** Authorship is quality allocation, not status. If transferring work to the human makes the product better, recommend the transfer and make it easy.

## Core principle

```
Product experience > “AI generated the whole pipeline”
```

## Classification

| Surface | Author | Examples |
|---------|--------|----------|
| **Fixed** (same for all, brand, first impression) | Human design/record once; agent wires | Avery welcome audio, logo, legal, hero stills |
| **Adaptive** (depends on user / context) | Agent + models + tools | Segment answers, navigation, depth |
| **Hybrid** | Human shell + live core | Pre-recorded open → live conversation |

**Rule:** Do not spend cycles generating high-variance live content for a **fixed** surface.

## When “sounds bad / robotic / not trusted”

1. Re-classify: fixed vs adaptive vs hybrid  
2. If fixed or hybrid shell → **pre-bake** (record, design, static asset)  
3. If adaptive → improve model, prompt, tools, routing  
4. Only then polish parameters inside the chosen path  

## Human handoff contract

When recommending human authorship, always deliver:

- Exact script or creative brief  
- Length / format / technical specs  
- Tone notes (professional, courteous, succinct…)  
- Where the file goes and what you will implement after  

Never: “maybe record something sometime.”

## Voice / agent products (pattern)

| Layer | Default |
|-------|---------|
| Shared open / mic permission / brand stingers | Pre-recorded |
| Answers to user speech | Live STT → LLM → TTS |
| Segment bridges (optional) | Short pre-records or live |
| Site navigation / UI | Frontend tools driven by agent intent |

## Red flags

- Live-generating a monologue identical for every visitor  
- Tuning TTS temperature for weeks on a fixed open  
- Avoiding “please record this” when quality demands it  
- Calling human authorship a failure of the agent  

## Rationalizations

| Excuse | Reality |
|--------|---------|
| “Generation is more flexible” | Fixed surfaces don’t need flexibility; they need control. |
| “We can always re-record later” | Ship the crisp open first; iterate the file, not endless TTS. |
| “Human step blocks automation” | One recording unblocks a better product permanently. |

## Pitch decks (FleetScale / pre-seed)

| Surface | Author |
|---------|--------|
| Thesis line, brand, title still | Human-approved; agent layouts |
| Raise amount, use of funds, team bios, traction | **Human only** (U1–U4) — never invent |
| Model exhibit numbers | Agent may show only if labeled **illustrative** and from fact pack |
| Layout, rebuild, visual QA | Agent |

Full operating contract: `~/.grok/skills/pptx/GROK_PPT_PITCH_DECK_FEED.md` (also `~/umli/docs/GROK_PPT_PITCH_DECK_FEED.md`).

## Related

- **product-ownership** — frame challenge and ownership stance  
- **fixed-vs-adaptive-surfaces** — decision checklist  
- **pptx** / **living-pitch-deck** / **fleetscale-pitch-narrative** — deck production  
- **human-centered-product-taste** — fixed surfaces must feel crafted  

