---
status: accepted
---

# Platform-aware mount discovery behind a stable CLI

dfrs will keep its public surface as the existing CLI and flags while moving
mount enumeration behind a platform-aware provider: macOS uses native mount
discovery so APFS is visible, while Linux keeps deterministic mount-file
parsing for explicit `--mounts` inputs and can use native discovery for its
default. This preserves scripts and fixtures without treating a Linux-only
mount file as a cross-platform contract, and keeps filtering, statfs, and
rendering above the provider boundary.
