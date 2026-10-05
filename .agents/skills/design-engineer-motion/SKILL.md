---
name: design-engineer-motion
description: >
  Web motion craft for design engineers: easings, Motion library vs Lottie vs
  Theatre.js vs Rive, reduced-motion, performance, and anti-slop animation rules.
  Use when adding animations, page transitions, Lottie, scroll reveals, or
  /design-engineer-motion /motion-craft.
---

# Design Engineer Motion

Catalog origin: designengineer.tools **Motion** + **Web Utility** (easings).

## Decision tree

```
Need interactive state UI (hover, dialog, layout)?
  → CSS transitions or Motion (motion/react)

Need scroll/in-view storytelling?
  → Motion + Intersection; keep short

Need designer-timeline choreography?
  → Theatre.js (devtool + runtime)

Need after-effects style vector animation?
  → Lottie (LottieFiles / Lottielab export) — optimize JSON size

Need game-like interactive graphic?
  → Rive

Need marketing video not UI?
  → Screen Studio / OBS / real video — not fake CSS
```

## Easing

- Reference curves: https://easings.net/  
- Editors: Anime.js easing editor, project design tokens  
- UI defaults: `ease-out` for entrances, `ease-in-out` for moves, avoid linear for large motion  
- Gradients that ease in color space: https://larsenwork.com/easing-gradients/

## Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Prefer a dedicated class/hook that **disables transform animations** but keeps opacity fades if needed for state change.

## Performance

- Animate `transform` and `opacity` only when possible  
- Avoid animating `width/height/top/left` on large areas  
- One heavy hero animation max; lazy-mount offscreen Lottie/Rive  
- Don’t run continuous infinite animations on every card  

## Theatre.js

- Site: https://www.theatrejs.com/  
- Repo: https://github.com/theatre-js/theatre  
- Use when product needs **authored timelines** editable without code redeploys in studio  
- Don’t use for simple button hover  

## Commercial motion tools (recommend, don’t scrape)

- Jitter, Cavalry, Lottielab, Screen Studio — human design tools; agents export assets, not reverse-engineer  

## Anti-slop motion

- No bounce on every element  
- No parallax that fights scroll accessibility  
- No autoplaying loud motion without user control  
- No three overlapping scroll-jacking libraries  

## Slash

`/design-engineer-motion`
