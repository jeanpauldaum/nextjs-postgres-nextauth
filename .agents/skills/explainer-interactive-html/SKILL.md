---
name: explainer-interactive-html
description: >
  Make a self-contained, single-file interactive HTML explainer (no CDN, no
  build step) that a reader can step through, change parameters in, or explore,
  and check it with headless screenshots. Use when the reader must explore and
  not only look: step through a process, compare options, change a value, or
  pick a depth; when the user asks for an explainer "in HTML", an interactive
  page, a demo page, or a playground; or when the format router picks step 2.
  Also /explainer-html.
---

# Interactive HTML explainer

The page is a view of a text brief. The brief stays the source of truth
(`explainer-format-router`). The page lets the reader move through the same
facts at their own speed.

## Contract

- **One file.** Inline CSS and JS. No CDN, no web fonts from a service, no build
  step. The file opens from disk and works offline.
- **One interaction model.** Pick one main interaction: a stepper, a parameter
  control, a filter, or a compare toggle. Add a second one only if the brief
  needs it.
- **Content in HTML.** Put the step text in HTML elements, not in JS strings.
  The lint can then read it, and the page still has its text without JS.
- **Addressable state.** Each state has a URL fragment (for example
  `#step-3-video`). The render script uses this to take a screenshot of each
  state.
- **Accessible.** Use real `<button>` elements, keyboard keys, visible focus,
  `aria-live` for changing text, and `prefers-reduced-motion`.
- **Calm motion.** Use short opacity and color transitions only. Motion shows a
  change of state. It is not decoration.
- **Source line.** The footer names the brief path and says "Generated view".

Tokens: use the project's brand tokens (read `AGENTS.md`). The template defaults
are FleetScale: porcelain `#F7F8FB`, ink `#12141A`, brand `#4F6CF7`.

## Template

`assets/interactive-template.html` is a working stepper with a diagram:

- `#step-content` holds one `<article data-on="node ids">` for each step.
- `NODES`, `EDGES`, and `FORMATS` in the script define the diagram and the
  parameter control.
- Arrow keys move between steps. Number keys pick a format.

Change the content and the data. You usually do not need to change the
rendering code.

## Workflow

1. Write the brief. Lint it (`explainer-plain-writing`).
2. Pick the one interaction that fits the brief.
3. Copy the template next to the brief:
   `cp <skill>/assets/interactive-template.html <topic>/page.html`
4. Replace the step content, the nodes, and the edges.
5. Lint the page text:
   `python3 <skills>/explainer-plain-writing/scripts/ste_lint.py <topic>/page.html`
6. Take a screenshot of each state. The `--console` flag records JS errors:
   `python3 <skills>/explainer-sheet/scripts/render_html.py <topic>/page.html <topic>/shots/step-1.png --width 1280 --height 800 --scale 1 --hash step-1 --console`
7. Take one narrow screenshot (`--width 420 --height 900`) to check the mobile
   layout.
8. Open each screenshot. Do the checks below.
9. Fix the problems. Then take the screenshots again.

`<skills>` is the skills folder: `.agents/skills` in the repo, or
`~/.cursor/skills` for a user install. The render script exits with code 3 if
the page logs a JS error.

## Checks

- [ ] Each label and each step is in the brief. The page adds no claims.
- [ ] Each state renders without JS errors (`--console`).
- [ ] All text is fully visible. No labels overlap lines or other labels.
- [ ] The keyboard alone can reach every state. Focus is visible.
- [ ] The narrow layout works.
- [ ] The file has no external requests (search for `http`).
- [ ] The footer names the brief path.

## Red flags

- A framework or a CDN script for a page with one interaction.
- Scroll-jacking, parallax, or effects that play for no reason.
- Facts that exist only in JS strings or only in the page.
- Screenshots that you did not open.

## Related

- `explainer-format-router` — when to make a page
- `explainer-sheet` — the render script and the static style
- `explainer-video` — when the idea unfolds in time
- `design-engineer-motion` — motion rules (FleetScale repo)
