---
title: Release notes
description: Release notes for the dfrs fork.
---

## 0.8.2

The documentation-focused patch release adds:

- high-resolution still frames for README and CLI usage examples;
- a lightweight, self-hosted asciinema recording on the landing page;
- a reproducible capture script for refreshing the landing recording.

## 0.8.1

The documentation-focused patch release adds:

- stable terminal recordings for common filtering and formatting workflows;
- a Dracula-inspired dark theme and a genuinely light theme for GitHub Pages;
- README cleanup that removes distro-package references and the broken packaging badge.

## 0.8.0

The fork-ready release line upgrades the project to Rust 1.96.0 and adds:

- native macOS APFS mount discovery;
- Linux x86_64 and arm64 validation;
- explicit mount-file overrides for fixtures and diagnostics;
- df-like default filtering with pseudo-mount suppression;
- escaped mount-path parsing and overflow-safe usage arithmetic;
- CLI-focused RustDoc and this GitHub Pages site.

The release is staged for review on `release/0.8.0`. It uses the unprefixed
SemVer tag `0.8.0` and does not publish a GitHub Release or binary assets as
part of this handoff.
