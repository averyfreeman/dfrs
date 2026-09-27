# dfrs 0.8.0 modernization

## Goal

Upgrade dfrs for Rust 1.96.0 with native APFS support on macOS arm64, required Linux x86_64 and arm64 support, comprehensive CLI-oriented Rustdoc, repository-local SonarQube tracking, and a fork-ready 0.8.0 release handoff.

## Acceptance criteria

- The CLI remains CLI-only and preserves existing flags except for the platform-aware default mount provider.
- macOS uses native mount discovery and supports APFS; Linux retains deterministic mount-file parsing and native discovery.
- Default output is df-like, with capacity-bearing local filesystems visible and pseudo mounts hidden unless broader filters are requested.
- Rust 1.96.0, formatting, tests, Clippy, Rustdoc, CI, and documentation-site workflows are documented and verifiable.
- Git-BBQ records the glossary, ADR, explicit Git habits, Sonar backlog, and release notes.

## Verification

`cargo test --locked`
