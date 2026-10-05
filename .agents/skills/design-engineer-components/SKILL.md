---
name: design-engineer-components
description: >
  Adopt design-engineer component stacks: shadcn/ui, React Bits, Motion
  Primitives, NumberFlow, 21st.dev patterns. Install, customize, license
  awareness, and anti-bloat rules for React/Vite/Next marketing and product UI.
  Use when adding UI components, animated bits, ProfileCard-like modules, or
  /design-engineer-components /react-bits /shadcn-components.
---

# Design Engineer Components

Catalog origin: [designengineer.tools → Components](https://designengineer.tools/).

## Stack choice

| Need | Prefer | Avoid |
|------|--------|--------|
| App chrome, forms, dialogs | **shadcn/ui** (own the code) | Random UI kit npm black box |
| Marketing delight (tilt, text anim, backgrounds) | **React Bits** selective copy | Pasting 10 Bits on one page |
| Micro-interactions | **Motion Primitives** / Motion | Custom GSAP for every hover |
| Animated numbers / stats | **NumberFlow** | CSS-only hacky counters |
| Explore trendy blocks | **21st.dev** as reference | Blind copy without brand fit |

## shadcn/ui

- Docs: https://ui.shadcn.com/  
- Repo: https://github.com/shadcn-ui/ui  
- Model: **copy into repo** — you maintain CSS/Tailwind variants  
- Install example: `npx shadcn@latest init` then `npx shadcn@latest add button`  
- Rules:  
  1. Init once; match project CSS strategy (CSS vars / Tailwind)  
  2. Customize tokens to brand before shipping demo zinc theme  
  3. Prefer composition over forking 10 variants of the same component  
  4. A11y: keep Radix behaviors; don’t strip focus rings  
  5. Don’t re-install over customized files without diff  

## React Bits

- Docs: https://www.reactbits.dev/  
- Repo: https://github.com/DavidHDev/react-bits  
- **Back pocket (read this first):** `references/REACT_BITS_POCKET.md`  
  also `docs/design-engineer-tools/REACT_BITS_POCKET.md`  
- Install one: `npx shadcn@latest add @react-bits/<Component>-TS-CSS`  
- **License:** MIT + Commons Clause — use in FleetScale; do not sell the kit  
- Rules: one signature motion per section; CSS variant; no extra WebGL on the video hero; prefer Bits already in `web/src/components/`  

FleetScale live: MetallicPaint, Beams. Threads/Strands copied, not on current landing.

## Motion Primitives

- Docs: https://motion-primitives.com/  
- Repo: https://github.com/ibelick/motion-primitives  
- Built on **Motion** + Tailwind; beta — APIs may move  
- Rules: use for text/in-view reveals; keep reduced-motion fallbacks; don’t nest conflicting animation systems  

## NumberFlow

- https://number-flow.barvian.me/ · github.com/barvian/number-flow  
- Use for KPI/stat ticks on marketing pages  
- Don’t animate every number in a dense table  

## 21st.dev / Fancy Components / Cursify

- Use as **inspiration + optional paste**  
- Always re-skin to brand; check deps and licenses before merge  

## Agent procedure

```
1. Prefer shadcn for structure
2. Add at most 1–2 React Bits for signature moments
3. Run build; fix hydration/SSR if Next
4. Visual QA: resting state visible, no layout jump
5. Document new components in project design notes
```

## Anti-patterns

- Three animation libraries (Framer Motion + GSAP + Anime) on one marketing site  
- Animated background + animated text + tilt card + Lottie hero  
- Shipping default shadcn zinc with purple accents as “brand”  

## Slash

`/design-engineer-components`
