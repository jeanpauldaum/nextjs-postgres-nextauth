---
name: fixed-vs-adaptive-surfaces
description: >
  Use when classifying product surfaces as fixed, adaptive, or hybrid before
  implementing generation, TTS, copy, or personalization; when the same content
  plays for every user; when building voice agents, marketing sites, onboarding,
  or any system with a shared open and personalized path. Also /fixed-vs-adaptive.
---

# Fixed vs adaptive surfaces

## Overview

Before implementing, **classify the surface**. Fixed surfaces get designed once (often human-authored). Adaptive surfaces use live models and tools. Hybrid = static shell + live core.

## Decision

```
Is the content the same for every user at this moment?
  YES → FIXED (or hybrid shell)
  NO  → depends on who they are / what they said → ADAPTIVE
```

### Fixed

- Same for all visitors  
- Brand / first impression / legal / permission prompts  
- **Author:** design or record once; ship as static asset when quality matters  
- **Do not:** endlessly generate live variants of the same monologue  

### Adaptive

- Changes with segment, answer, history, or page state  
- **Author:** agent + models + tools  
- **Do:** personalize depth, route, next step  

### Hybrid (common for voice / guides)

1. Fixed open (hook, identity, what I can do)  
2. One routing question  
3. Adaptive path (talk + navigate + depth)  

## Checklist (run before polish loops)

- [ ] Named the surface (e.g. “Avery welcome”, “segment answer”)  
- [ ] Labeled fixed / adaptive / hybrid  
- [ ] If fixed: static asset path considered  
- [ ] If adaptive: inputs that change output listed  
- [ ] If hybrid: boundary between shell and core stated  

## Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Live TTS for identical welcome | Pre-record open |
| Same long thesis for capital and operator | Route + depth packs |
| Generating UI navigation in prose only | Emit navigate intents; frontend executes |
| Polishing generator when object is misclassified | Re-classify first |

## Related

- **quality-first-authorship**  
- **product-ownership**  
