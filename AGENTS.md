# Agent instructions

Read [CONTEXT.md](./CONTEXT.md) for dfrs vocabulary, then consult the relevant
records under [docs/adr](./docs/adr) before changing filesystem discovery,
filtering, or release behavior.

Project-local agent notes live under `.gitbbq/`. The Matt Pocock skills
dependency is pinned under `.gitbbq/mattpocock/`.

Use `git-bbq validate` before persisting architecture projections. Git behavior
is governed by `.githabits.yaml`; do not create branches, tags, commits, or
remote changes without an approved workflow action.

<!-- sonar:begin:codex-secrets-on-read -->
# SonarQube secrets scanning for files protocol

Before reading any file in this workspace, scan it for secrets with the deterministic scanner:

```bash
sonar analyze secrets <path/to/file>
```

If the command reports that the file contains a secret, **do not read the file**. Instead:

1. Inform the user that the file appears to contain a secret or credential and that reading it would expose the value in chat history, logs, and any downstream telemetry.
2. Advise them to rotate the leaked credential at its source of truth and remove it from the file.
3. Do not proceed with the original request until the secret has been removed.
<!-- sonar:end:codex-secrets-on-read -->
