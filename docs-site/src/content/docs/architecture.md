---
title: Architecture
description: The discovery, measurement, filtering, and rendering pipeline.
---

## Pipeline

```text
CLI arguments
    │
    ▼
mount provider ──► normalized Mount records ──► statfs measurement
                                                    │
                                                    ▼
                                      visibility and --local filters
                                                    │
                                                    ▼
                                           columns and color renderer
```

The provider boundary keeps operating-system APIs out of formatting code.
`Mount` is the normalized seam: native providers and file fixtures both return
the same record, then the shared `refresh_stats` function performs bounded
arithmetic.

## Platform policy

macOS uses `getmntinfo(3)` and copies the native source, mount directory, and
filesystem type strings. This is why APFS volumes are visible without relying
on Linux's `/proc/self/mounts`. Linux uses that kernel-backed listing as its
default provider and supports the same parser for explicit overrides.

The minimal native view is capacity-based and type-aware. It does not assume
that every real filesystem starts with `/dev`; that matters for overlay,
squashfs, ZFS, and other valid filesystem sources.

## Decisions

The durable architecture record is
[ADR-0001](https://github.com/averyfreeman/dfrs/blob/release/0.8.0/docs/adr/0001-platform-aware-mount-discovery.md).
