# Implementation plan

This projection is derived from the Git-BBQ context and ADR documents.

## Problem

Upgrade dfrs for Rust 1.96.0 while preserving its CLI boundary and preparing
platform-aware filesystem discovery for macOS APFS and Linux.

## Languages

rust

## Decisions

- [Platform-aware mount discovery behind a stable CLI](docs/adr/0001-platform-aware-mount-discovery.md) — accepted

## SonarQube and repository secret protection

- [x] Use the authenticated SonarCloud project key `averyfreeman_dfrs`.
- [x] Ignore repository-local `.env*` files without copying credentials into
  the project.
- [x] Install project-scoped SonarQube hooks and MCP configuration for Codex.
- [x] Record the authenticated secrets scan and server issue-list result in
  [the SonarQube backlog](docs/sonar-backlog.md).
- [ ] Re-run source-quality analysis after SonarCloud enables Vortex for the
  organization; the current six-file source attempt was skipped with `403`.
