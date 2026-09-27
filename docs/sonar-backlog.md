# SonarQube backlog

This is the repository-local backlog for the `dfrs` SonarQube project. The
project key is `dfrs`, and analysis is intentionally local to this fork; no
Sonar findings are mirrored into GitHub Issues.

## Scan status

The scan configuration is checked in at
[`sonar-project.properties`](../sonar-project.properties). The SonarQube CLI
was not available in the implementation environment, so no invented issue
keys or severities are recorded here. Once the local CLI is authenticated,
run the project-local scan and copy each returned issue into the table below.

```sh
sonar analyze -p dfrs
sonar list-issues -p dfrs
```

Keep the issue key, rule, severity, file/line, concise explanation, and the
planned fix in this document. Resolve entries only after the code change and
the relevant Rust/doc test pass.

## Tickets

| Status | Sonar issue | Rule | Location | Planned fix |
| --- | --- | --- | --- | --- |
| Pending scan | — | — | — | Run the authenticated local SonarQube analysis and populate this table. |

## Review boundary

Sonar findings are a prioritization input, not a replacement for Rust 1.96
compilation, Clippy, tests, native macOS smoke coverage, or the Linux target
checks. Security and correctness findings take precedence over cosmetic
refactoring when the scan is available.
