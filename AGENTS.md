# Agent instructions

Read [CONTEXT.md](./CONTEXT.md) for dfrs vocabulary, then consult the relevant
records under [docs/adr](./docs/adr) before changing filesystem discovery,
filtering, or release behavior.

Project-local agent notes live under `.gitbbq/`. The Matt Pocock skills
dependency is pinned under `.gitbbq/mattpocock/`.

Use `git-bbq validate` before persisting architecture projections. Git behavior
is governed by `.githabits.yaml`; do not create branches, tags, commits, or
remote changes without an approved workflow action.
