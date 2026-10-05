---
name: design-engineer-craft
description: >
  Design-engineer craft playbook: inspiration workflow, anti-AI-slop quality bar,
  OKLCH/color contrast mindset, motion restraint, and pre-ship UI checklist for
  marketing and product surfaces. Derived from designengineer.tools craft stack
  (60fps, Design Spells, Godly, Mobbin, easings, OKLCH). Use when polishing UI,
  redesigning a page, reviewing visual quality, or /design-engineer-craft /craft.
---

# Design Engineer Craft

Load **before** implementing visual UI when quality matters. Pair with `human-centered-product-taste` and `design-engineer-tools`.

## AI-native without slop

| Do | Don’t |
|----|--------|
| Quiet systems, clear hierarchy | Neon cyberpunk / purple fog |
| One idea per section | Collage of unrelated effects |
| Human + product truth | Stock handshake over globe |
| Intentional motion (one primary motion) | Everything bouncing |
| OKLCH / accessible contrast | Random Tailwind rainbow |
| Own the component code | Unedited v0 dump |

## Inspiration workflow (agent)

1. **Classify surface:** marketing hero · product app · pitch · empty state  
2. **Pull 2–3 refs** (not 20):  
   - Marketing: Godly, 60fps, Minimal Gallery, Saaspo  
   - Product UI: Mobbin, Design Spells  
   - Game/HUD energy only if product is game-like: HUDS+GUIS, Game UI Database  
3. **Extract principles**, not pixels: type scale, spacing rhythm, one accent color, motion budget  
4. **Execute original** in brand tokens — never clone a SaaS landing page  
5. **Taste pass:** would a design engineer ship this without apology?

Sources: designengineer.tools Inspiration category.

## Color

- Prefer **OKLCH** for tokens (perceptual lightness) — [oklch.com](https://oklch.com/)  
- Check text/UI contrast before ship — [color.review](https://color.review/) mindset  
- One dominant brand hue; mute the rest  
- Easing gradients only when the gradient is a hero moment — [easing gradients](https://larsenwork.com/easing-gradients/)

## Motion

- Default curves from [easings.net](https://easings.net/) — not linear for UI  
- Prefer **opacity + transform** (composite-friendly)  
- Honor `prefers-reduced-motion: reduce` → static or opacity-only  
- One signature motion per page; secondary motions quieter  
- Lottie/Rive only when CSS/Motion primitives can’t express it cleanly  

See `design-engineer-motion` for stack choices.

## Typography

- Pair display + body with clear role split  
- Prefer licensed free fonts with clear OFL/commercial terms (Fontshare, etc.)  
- Line length ~45–75ch; avoid orphan titles  

## Component quality bar

Ship only if:

- [ ] Spacing uses a consistent scale (4/8)  
- [ ] Focus states visible for interactive controls  
- [ ] Hover/active states intentional, not browser default only  
- [ ] Empty/loading/error states exist for data UI  
- [ ] Mobile layout not a shrunk desktop  
- [ ] No illegible text on image  
- [ ] Bundle: no three animation libraries for one fade  

## Pre-ship checklist

1. Hierarchy readable at arm’s length (squint test)  
2. Brand tokens only — no leftover demo purple/pink  
3. Motion OK under reduced-motion  
4. Contrast OK for body text  
5. Lighthouse/perf not destroyed by hero video/3D  
6. Copy sounds human (pair `quality-first-authorship` / narrative skills)  

## Related

- `design-engineer-tools` — catalog  
- `design-engineer-components` — shadcn / React Bits  
- `human-centered-product-taste`  
- `imagine` — only for photographic/mood art  

## Slash

`/design-engineer-craft` · `/craft`
