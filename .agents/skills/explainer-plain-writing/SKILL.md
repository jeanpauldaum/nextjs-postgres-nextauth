---
name: explainer-plain-writing
description: >
  Write plain technical English at "80% of ASD-STE100" (Simplified Technical
  English): short sentences, one instruction per sentence, active voice, simple
  tenses, approved-style words. Includes a dependency-free lint script. Use for
  explanations, summaries, reports, PR descriptions, docs, runbooks, procedures,
  and the text brief behind any sheet, page, or video; when output is wordy, vague,
  or hard to scan; or when the user asks for STE, "plain English", or "simple
  writing". Also /plain-writing /ste.
---

# Plain technical writing (80% ASD-STE100)

ASD-STE100 is a controlled language from aerospace maintenance. Its rules make
text short, direct, and hard to misread. This skill keeps the writing rules and
drops the strict 900-word dictionary.

## Rules to keep

| Rule | Limit |
|------|-------|
| Procedural sentence (a command) | max 20 words |
| Descriptive sentence | max 25 words |
| Paragraph | max 6 sentences, one topic |
| Noun cluster | max 3 words ("hydraulic reservoir" = 2) |
| Instructions per sentence | 1 (2 only for simultaneous actions) |

**Verbs**

- Use the imperative, simple present, simple past, simple future, infinitive,
  and the past participle as an adjective ("the closed valve").
- Do not use progressive tenses ("is closing") or perfect tenses ("has closed").
- Use the active voice in procedures. In descriptive text, use the passive only
  when the actor is unknown or not important.

**Procedures**

- Write each step as a command. Put one instruction in each step.
- Put the condition first: "If the check fails, fix the branch."
- Number the steps in a vertical list.
- Write a warning as a command, then the reason: "Do not merge to `main`. The
  merge deploys the site."

**Descriptive text**

- Put the main point in the first sentence.
- Keep one topic in each paragraph. Use a vertical list for complex text.

**Words**

- Use the same word for the same thing every time.
- Give each word one meaning. "Close" is a verb ("close the valve"), not "near".
- Keep "the", "a", and "this". Do not write in telegraph style.
- Use technical names (code, paths, product names) as they are. Put code in
  backticks.
- Use short, common words. See the swaps below.

## What this profile drops (the other 20%)

- The 900-word approved dictionary. Common words and technical names are fine.
- The strict ban on "-ing" words in noun use ("the loading step").
- Rules for specific maintenance documents.
- Markdown structure is fine: headings, tables, and code blocks. The lint
  skips them.

## Word swaps

| Not approved | Use |
|--------------|-----|
| utilize, leverage | use |
| commence, initiate | start |
| prior to | before |
| in order to | to |
| approximately | about |
| ensure | make sure |
| replenish | fill |
| terminate | stop, end |
| facilitate | help |
| subsequently | then, after |
| in the event that | if |
| due to the fact that | because |
| sufficient / additional / numerous | enough / more / many |
| demonstrate, indicate | show |
| modify / obtain / assist | change / get / help |
| e.g. / i.e. / etc. | for example / that is / the full list |
| delve | look at |
| seamless, robust | say what it does |
| it is important to note that | (delete) |

The script holds the full list (`WORD_SWAPS` in `scripts/ste_lint.py`).

## Examples

| Before | After |
|--------|-------|
| It is imperative that the operator ensures the hydraulic reservoir is replenished prior to commencing operation. | Make sure the hydraulic reservoir is full before you start the operation. |
| I've gone ahead and updated the config so that changes are now being shipped whenever main is updated. | I changed the config. Now each merge to `main` deploys the site. |
| Open the workflow page and check the run status, then utilize the logs. | 1. Open the workflow page. 2. Check the run status. 3. Read the logs. |

## Shape of an agent answer

1. First sentence: the answer or the outcome.
2. Then the facts (bullets) or the steps (numbered). Use one idea for each line.
3. Then the open risks or decisions that the reader must make.

## Lint your own output

Run the script on each draft before you hand it over. It uses only the Python
standard library.

```bash
S=.agents/skills/explainer-plain-writing/scripts   # user install: ~/.cursor/skills/explainer-plain-writing/scripts
python3 $S/ste_lint.py brief.md                    # Markdown or plain text
python3 $S/ste_lint.py sheet.html storyboard.json  # HTML views, video narration
echo "Draft text." | python3 $S/ste_lint.py -      # stdin
python3 $S/ste_lint.py --threshold 0.9 --json notes.md
```

- **Score:** the share of clean sentences. The default pass mark is 80%.
  `--strict` sets it to 100%. Exit code 0 = pass, 1 = fail, 2 = usage error.
- **Rules:** `sentence-length`, `paragraph-length`, `passive`, `progressive`,
  `perfect`, `one-instruction`, `word`, and `noun-cluster` (advisory, not
  scored). Skip a rule with `--ignore rule1,rule2`.
- **Limits:** the script uses heuristics, not a grammar parser. A finding is a
  prompt to read the sentence again. Fix real problems. Do not make a clear
  sentence worse only to satisfy the script.

## Workflow

1. Write the draft.
2. Run the lint.
3. Fix the real findings.
4. Read the text once as the reader. Make sure the first sentence gives the
   answer.

## Related

- `explainer-format-router` — when text is not enough
- `explainer-sheet`, `explainer-interactive-html`, `explainer-video` — views
  that start from this text
