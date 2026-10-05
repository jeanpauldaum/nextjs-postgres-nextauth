---
name: explainer-format-router
description: >
  Pick the output format that makes agent work easiest for a human to understand:
  plain text (80% ASD-STE100), a one-page sheet or diagram, an interactive HTML page,
  or a narrated explainer video. Use when you explain a system, a change, a plan, a
  concept, or a result to a person; when the user asks to "explain", "show me",
  "make a diagram", "make it visual", "make an explainer", "in HTML", or "make a
  video"; or when a long text answer would be hard to follow. Also /explain.
---

# Explainer format router

Based on Andrej Karpathy's ladder of LLM output formats for human understanding:
writing → diagrams → web pages → explainer videos. Each step up shows more, but
costs more to make, to check, and to update.

## The rule

1. **Text is the source of truth.** Always write the plain-text brief first
   (`explainer-plain-writing`). Every fact in a richer format must come from it.
2. **Richer formats are views.** A sheet, page, or video is a throwaway rendering
   of the brief. To change a fact, change the brief first. Then make the view
   again. Do not fix facts only in the view.
3. **Check every view for accuracy.** Render the view. Look at the result.
   Compare each label, number, and claim with the brief. Do not hand over a view
   that you did not look at.

## Pick the format

Start at the bottom of the ladder. Go up one step only when the reader gets a
clear gain.

| Step | Format | Use it when | Skill |
|------|--------|-------------|-------|
| 0 | Plain text (80% STE) | Default. Answers, procedures, decisions, reviews, anything that people quote, search, or diff. | `explainer-plain-writing` |
| 1 | Sheet / diagram | The structure is spatial: 3+ parts that connect, a flow, a comparison, a hierarchy, or a one-page reference card. | `explainer-sheet` |
| 2 | Interactive HTML | The reader must explore: step through a process, change a parameter, filter data, or choose a depth. | `explainer-interactive-html` |
| 3 | Narrated video | The idea unfolds in time (cause and effect, an algorithm, a transform), or the reader is new and passive (onboarding, a pitch, a share link). | `explainer-video` |

Ask these questions before you go up a step:

1. **Who reads it, and for how long?** An expert with 30 seconds needs text or a
   sheet. A newcomer with 5 minutes can take a page or a video.
2. **What is the shape of the idea?** Linear → text. Spatial → sheet.
   Parametric → interactive page. Temporal → video.
3. **What must the reader do next?** If they must act, end with a text procedure,
   even when the main view is a video.
4. **Will the facts change soon?** Volatile facts stay low on the ladder. A video
   is the most expensive format to update.
5. **Can you check it?** If you cannot inspect the view here, give the text. Say
   which view you could not verify.

When the user names a format ("in HTML", "make a video"), use that format. Write
the brief first all the same.

## Workflow

1. Write `brief.md` in plain writing.
2. Run the lint script on it (`explainer-plain-writing/scripts/ste_lint.py`).
3. Pick one view with the table above. Make one view, not three.
4. Build the view from the brief with the matching skill.
5. Render the view. Look at the result.
6. Compare each fact in the view with the brief.
7. Fix the differences. Then render again.
8. Hand over the view and the brief together. Name the brief path in the view
   (title block, footer, or end card).

## Where artifacts go

- Use a scratch or docs folder, for example `docs/explainers/<topic>/` or a
  temp folder. Keep the brief next to its views.
- Never write explainer artifacts into paths that deploy. Read the project's
  `AGENTS.md` to find its ship paths (in this repo: `web/**`, `site/**`,
  `apps/**`, `deploy/**`).
- Views are throwaway. Commit the brief when it has long-term value. Commit a
  view only when the user asks for it.

## Accuracy check (all views)

- [ ] Each label, number, and name in the view is in the brief.
- [ ] Numbers have units and a source. Scenarios and illustrations have a label.
- [ ] You rendered the view and looked at the output (PNG, screenshot, or frames).
- [ ] Text in the view passes `ste_lint.py` (sheets and pages: lint the HTML file;
      videos: lint the storyboard).
- [ ] The view names the brief path.
- [ ] Nothing in the view adds claims that the brief does not make.

## Red flags

- Making a video when a 6-line answer is enough.
- Fixing a wrong number in the SVG and not in the brief.
- Handing over a view that you did not render.
- Stacking formats (sheet + page + video) for one question.
- Decoration that does not carry information.

## Related

- `explainer-plain-writing` — the source-of-truth text and the lint script
- `explainer-sheet` — one-page sheet in engineering-drawing style
- `explainer-interactive-html` — single-file interactive page
- `explainer-video` — Manim animation with narration
- `fixed-vs-adaptive-surfaces` (FleetScale repo) — an explainer that becomes a
  public, fixed surface needs a human design pass, not only regeneration
