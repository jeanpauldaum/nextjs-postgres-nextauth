---
name: explainer-sheet
description: >
  Make a one-page explainer sheet or diagram as a single HTML/SVG file, in the
  style of an engineering drawing (zone frame, lettered panels, title block),
  and render it to PNG or PDF. Use when an idea has spatial structure (parts that
  connect, a flow, a comparison, a hierarchy, rules with approved/not-approved
  status); when the user asks for a diagram, a cheat sheet, a one-pager, a
  reference card, or "make it visual"; or when the format router picks step 1.
  Also /explainer-sheet /diagram.
---

# Explainer sheet

A sheet is a view of a text brief. The brief stays the source of truth
(`explainer-format-router`). The sheet shows the same facts on one page, so the
reader sees the structure at a glance.

## Style

The model is an engineering drawing sheet, for example an ASD-STE100 overview.

- Landscape page, 1600 x 1000 CSS px. Render at 2x for a sharp PNG.
- A thin frame with drawing zones: columns 1-8 on top and bottom, rows A-D on
  the sides.
- 4 to 6 panels. Each panel has a letter badge (A, B, C...), a short title,
  and a small mono tag on the right (the source or the unit).
- A title block in the bottom-right corner: title, source of truth (the brief
  path), owner, status ("Generated view"), and "Sheet 1 of 1".
- Hairlines, white panels on a porcelain page. No shadows, gradients, emoji,
  or stock icons.
- One accent color for "approved" and the main path. One fail color for "not
  approved". Mono type for examples, commands, and values.

**Tokens.** Use the project's brand tokens (read `AGENTS.md`). The template
defaults are FleetScale: porcelain `#F7F8FB`, ink `#12141A`, brand `#4F6CF7`.
For small brand-color text, use the darker `--brand-text` (`#3B54D6`). This gives
at least 4.5:1 contrast on white.

## Building blocks (all in the template)

| Block | Use it for | Markup |
|-------|-----------|--------|
| Flow diagram | Steps, pipelines, hierarchies | inline `<svg class="flow">` with `.node`, `.gate` (decision), `.edge`, `.lbl` |
| Lists | Paths, names, short items in columns | `.cols` with `.list-head` and `ul.plain` (add `.mono` for paths) |
| Annotated example | Show why a line is right or wrong | `.annot` with `.m[data-n]` balloons and a `.legend` |
| Status table | Rules, options, approved / not approved | `<table>` with `.ok` / `.no` marks |
| Limit bars | Maximum values, budgets, ranges | `.track` with `--val` and `--max` |
| Timeline | Dates, versions, phases | `.timeline` with one `<div>` per point |
| Checklist | Checks before hand-over | `ul.check` |
| Title block | Title, source, owner, status, sheet | `.title-block` |

Layout: a 12-column grid with two rows. Give each panel a width class (`w2` to
`w12`). Use `.stack` to put a panel above the title block. For one large
diagram, use `.field.one-row` with one `w12` panel.

## Workflow

1. Write the brief. Lint it (`explainer-plain-writing`).
2. List the 4 to 6 questions that the reader has. Give each question one panel.
3. Pick one building block for each panel.
4. Copy the template next to the brief:
   `cp <skill>/assets/sheet-template.html <topic>/sheet.html`
5. Replace the content. Keep the CSS. Delete the blocks that you do not use.
6. Put the brief path in the title block.
7. Lint the sheet text:
   `python3 <skills>/explainer-plain-writing/scripts/ste_lint.py <topic>/sheet.html`
8. Render the sheet:
   `python3 <skill>/scripts/render_html.py <topic>/sheet.html <topic>/sheet.png`
9. Open the PNG. Do the checks below.
10. Fix the problems. Then render again.

`<skill>` is this folder: `.agents/skills/explainer-sheet` in the repo, or
`~/.cursor/skills/explainer-sheet` for a user install. The render script needs
Chrome or Chromium. Set `CHROME=/path/to/browser` if the script cannot find it.
Use a `.pdf` output path to print to PDF.

Add `data-lint="skip"` to an element that shows bad text on purpose, for example
a "before" sentence.

## Checks

- [ ] Each label, number, and name is in the brief. The sheet adds no claims.
- [ ] All text is fully visible. No labels overlap lines or other labels.
- [ ] Body text is at least 10.5 px. Nothing is smaller than 9 px.
- [ ] The eye can follow each flow from start to end.
- [ ] Each panel answers one question. Its title says which question.
- [ ] Status marks use the accent color and the fail color only.
- [ ] The title block names the brief path and says "Generated view".
- [ ] The sheet text passes `ste_lint.py`.

## Red flags

- More than 6 panels, or paragraphs in a panel. Split into two sheets, or
  go back to text.
- Decoration that carries no information.
- Fixing a fact in the SVG and not in the brief.
- A quick diagram for a chat or a PR: Mermaid in Markdown is fine when the
  viewer renders it. Use this sheet when other people must review or share the view.

## Related

- `explainer-format-router` — when to make a sheet
- `explainer-plain-writing` — the brief and the lint
- `explainer-interactive-html` — when the reader must explore, not only look
- `design-engineer-craft` — contrast and hierarchy checks (FleetScale repo)
