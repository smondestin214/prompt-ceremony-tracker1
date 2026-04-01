# Prompt Engineering Ceremony Tracker

A single-page web app for content design teams to track prompt engineering work from strategy through post-launch evaluation.

## What it does

Each project moves through 7 ceremony stages:

| Stage | Purpose |
|-------|---------|
| 🎯 Prompt strategy | Document purpose, scope, constraints, and ownership before any prompting begins |
| 🔍 Prompt crit | Review and give feedback on the first prompt draft |
| 🐝 Swarming | Collaborative prompt iteration session with the full team |
| 🐛 Bug bash | Open testing to surface edge cases and failures |
| 🧪 Testing | Structured evaluation against defined test cases |
| 📊 Evals | Score outputs against a rubric and make a go/no-go call |
| 🚀 Post-launch eval | Evaluate real-world performance after launch |

### Key features

- **Per-item sign-off** — team members initial each checklist item to mark it complete
- **Auto status tracking** — ceremonies automatically move from "not started" → "in progress" → "done" as items are signed off
- **Notes per checklist item** — add context or callouts inline under any item
- **Target dates** — set a launch date and ceremony target dates are calculated automatically, working backwards
- **Bug tracking** — log bugs with severity (low / medium / high / blocking), type (prompt-fixable / engineering / other), a title, and detail notes
- **Document links** — attach relevant docs (briefs, specs, style guides) to each project
- **Team sync** — connect a GitHub token to sync project data across your team via a shared JSON file

## Getting started

The app runs entirely in the browser — no installation needed.

**To use the hosted version:** visit the GitHub Pages URL for this repo.

**To run locally:** open `index.html` in any browser. That's it.

## Setting up team sync

By default, data is saved to your browser's local storage. To share data across your team:

1. Create a `shared-data.json` file in a GitHub repo your team has access to
2. Generate a GitHub Personal Access Token with **Contents: Read and Write** permissions on that repo
3. Click the sync badge in the top right of the app and enter your token + repo details

Each team member connects with their own token. Changes sync automatically on save.

## Tech

- Vanilla HTML, CSS, and JavaScript — no build step, no dependencies
- `localStorage` for local persistence
- GitHub Contents API for optional team sync
- Hosted via GitHub Pages
