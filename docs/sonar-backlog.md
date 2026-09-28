# SonarQube backlog

This is the repository-local backlog for the `dfrs` SonarQube project. The
SonarCloud project key is `averyfreeman_dfrs`; analysis is intentionally local
to this fork, and no Sonar findings are mirrored into GitHub Issues.

## Authentication and project

The Homebrew-managed SonarQube CLI is authenticated against SonarCloud EU for
the `averyfreeman` organization. `sonar auth status` reports that the token is
stored in the macOS Keychain, so no `.env` file is needed.

The checked-in project configuration is in
[`sonar-project.properties`](../sonar-project.properties). The current CLI
syntax for the server-side issue list is:

```sh
sonar auth status
sonar list issues -p averyfreeman_dfrs --format toon
```

## Authenticated scan instructions

Run the following from the repository root after authenticating with the
Keychain-backed CLI:

```sh
sonar auth status
sonar analyze --project averyfreeman_dfrs --depth DEEP --format json \
  --file src/args.rs --file src/errors.rs --file src/main.rs \
  --file src/mount.rs --file src/theme.rs --file src/util.rs
sonar analyze secrets src tests
sonar list issues -p averyfreeman_dfrs --format toon
sonar quality-gate status -p averyfreeman_dfrs --format json
```

## Scan status

- `sonar auth status`: authenticated to `https://sonarcloud.io` as
  `averyfreeman`, with credentials sourced from the OS Keychain.
- Rust source analysis was attempted with the authenticated CLI at `DEEP`
  depth for all six files under `src/`. SonarCloud returned `403 Forbidden`
  because Vortex analysis is not enabled for this organization. The CLI
  skipped all six files; this is not counted as a clean source-quality scan.
- `sonar analyze secrets src tests`: **no issues found**.
- `sonar list issues -p averyfreeman_dfrs --format toon`: **0 issues** in the
  default `OPEN,CONFIRMED` status set.
- `sonar quality-gate status -p averyfreeman_dfrs --format json`: `NOT_COMPUTED`
  on `main`, because no server-side analysis has been published for the
  project.

## Tickets

| Status | Sonar issue | Rule | Location | Planned fix |
| --- | --- | --- | --- | --- |
| Clean server issue list | — | — | `averyfreeman_dfrs` | None currently; recheck after a published analysis. |
| Clean secrets scan | — | — | `src/`, `tests/` | None. Keep the repository secret-scanning hook enabled. |
| Awaiting analysis entitlement | — | — | `src/*.rs` | Re-run the authenticated source-quality scan when Vortex is enabled; do not treat skipped files as clean. |

## Review boundary

Sonar findings are a prioritization input, not a replacement for Rust 1.96
compilation, Clippy, tests, native macOS smoke coverage, or the Linux target
checks. Security and correctness findings take precedence over cosmetic
refactoring when a complete source-quality scan is available.
