# skills.sh design-related installs (optional)

Core 6 for craft (run only if user wants ecosystem skills):

```bash
npx skills add anthropics/skills --skill frontend-design
npx skills add leonxlnx/taste-skill --skill design-taste-frontend
npx skills add emilkowalski/skills --skill emil-design-eng
npx skills add https://uizze.com --skill anti-ui-slop
npx skills add vercel-labs/agent-skills --skill web-design-guidelines
npx skills add pbakaus/impeccable --skill impeccable
```

React product extras:
```bash
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices
npx skills add vercel-labs/agent-skills --skill vercel-composition-patterns
```

**Prefer Grok local `design-engineer-*` skills for FleetScale** so brand tokens and pitch hygiene stay coherent.

Pipeline: taste → craft (emil) → audit (guidelines + anti-ui-slop) → polish (impeccable).
Pin porcelain `#F7F8FB` / ink `#12141A` / brand `#4F6CF7` before any taste skill.
