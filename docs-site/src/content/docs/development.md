---
title: Development
description: Build, test, document, and validate dfrs locally.
---

## Toolchain

The repository pins Rust `1.96.0` in `rust-toolchain.toml` and declares
`rust-version = "1.96"` in `Cargo.toml`. `rustup` is the only Rust toolchain
manager expected on a development machine.

```sh
rustc --version
cargo test --locked
cargo fmt -- --check
cargo clippy --locked --all-targets -- -D warnings
cargo doc --locked --no-deps --document-private-items
```

Supported build targets are `aarch64-apple-darwin`,
`x86_64-unknown-linux-gnu`, and `aarch64-unknown-linux-gnu`. Windows and
Intel macOS are intentionally outside this release line.

## Documentation site

The site is an adapted, pinned Dockit Astro/Starlight snapshot and uses pnpm:

```sh
cd docs-site
pnpm install --frozen-lockfile
pnpm run check
pnpm run build:rustdoc
pnpm run build
```

The Pages workflow generates RustDoc into `public/rustdoc` before Astro builds
the static site. Generated output and package-manager directories are ignored
and are not treated as source files.

## Change discipline

Keep the CLI flags stable, add parser/provider tests with behavior changes,
and update the CLI docs when output or discovery semantics change. Use the
Git-BBQ records and `.githabits.yaml` for architecture and Git lifecycle
decisions.
