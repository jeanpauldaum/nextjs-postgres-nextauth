---
name: product-ownership
description: >
  Use when building product features, improving UX quality, trust, retention, or
  brand voice; when stuck polishing parameters; when the user cares about product
  judgment not only code; when ownership, architecture, or "what kind of product
  is this" is at stake. Also /product-ownership.
---

# Product ownership

## Overview

**Own the product outcome, not just the open implementation path.** Challenge the frame before polishing the mechanism. Prefer designs that maximize user experience even when they transfer authorship to the human or reduce “AI does everything.”

## When to use

- Quality / trust / bounce / “feels robotic” / brand complaints  
- Feature work where multiple architectures exist  
- Anytime you catch yourself only tuning the last agreed approach  

## Standing rules

1. **Product quality > AI completeness.** A better product that needs a human voice file, design decision, or static asset is a win — recommend it early.
2. **Frame before polish.** Before parameter tweaks, ask: kill / freeze static / pre-bake / route / personalize / generate live.
3. **Two-track every non-trivial UX issue**  
   - **A. Frame challenge** — architecture options (1–3) + recommendation  
   - **B. Path inside current frame** — only after A  
4. **Don’t wait for the human to invent the architecture.** Surface category-level moves proactively.
5. **Ownership = decision quality + execution.** You own framing, options, tradeoffs, recommendation, and all automatable implementation. Human owns taste, brand performance, risk, recorded voice when that *is* the product.
6. **Make human authorship cheap.** When handing work back: exact script, length, tone, format, drop path, how you’ll wire it.

## Mandatory checkpoint (quality / trust / retention)

Answer out loud before more polish:

- What *kind* of surface is this — fixed, adaptive, or hybrid?  
- What would a strong product lead freeze as static?  
- What only the human can author well?  

Then act on the answers.

## Red flags — STOP and reframe

- Only adjusting model temperature / prompts / copy density after “sounds bad”  
- Avoiding “you need to record / design / decide this” because it feels awkward  
- Optimizing a generator for content that is the same for every user  
- Shipping monologues when the product is a guide/concierge  
- Waiting for the user to suggest the architectural move  

**All of these mean:** re-classify the surface; offer frame options; then implement.

## Rationalizations

| Excuse | Reality |
|--------|---------|
| “I can fix it with better generation” | Fixed brand surfaces often shouldn’t be generated. |
| “Asking the human is friction” | Visitor friction is what matters; 15s of authorship can beat days of TTS tuning. |
| “They already approved this path” | Approving a path ≠ forever; quality feedback reopens the frame. |
| “Ownership means I do it all myself” | Ownership means the best product path, including handoffs. |
| “Stay in scope of the last task” | Product ownership includes challenging scope when the object is misclassified. |

## Output shape (when this skill applies)

1. **Frame:** fixed / adaptive / hybrid + why  
2. **Options:** 2–3 architectures with tradeoffs  
3. **Recommendation:** one clear pick  
4. **Human ask (if any):** minimal, ready-to-execute brief  
5. **Implement:** everything else without waiting  

## Related

- **multi-lens-reasoning** — ontology, epistemology, psychology, cognitive topology, pattern recognition  
- **human-centered-product-taste** — creativity, taste, human feel  
- **creative-product-ontology** — reframe the object before optimizing  
- **quality-first-authorship** — who authors which layer  
- **fixed-vs-adaptive-surfaces** — classification checklist  
- **avery-site-concierge** (project) — FleetScale Avery application  
