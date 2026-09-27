# Implementation plan

This projection is derived from the Git-BBQ context and ADR documents.

## Problem

Upgrade dfrs for Rust 1.96.0 while preserving its CLI boundary and preparing
platform-aware filesystem discovery for macOS APFS and Linux.

## Languages

rust

## Decisions

- [Platform-aware mount discovery behind a stable CLI](docs/adr/0001-platform-aware-mount-discovery.md) — accepted
