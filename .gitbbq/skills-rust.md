# Rust

- Rust `1.96.0` is pinned in `rust-toolchain.toml`; `rust-version = "1.96"` in
  `Cargo.toml` is the supported MSRV.
- Keep the binary CLI-only and preserve existing flags unless an approved
  architecture decision records the compatibility impact.
- The supported target baseline is `aarch64-apple-darwin`,
  `x86_64-unknown-linux-gnu`, and `aarch64-unknown-linux-gnu`.
- Before handoff, run `cargo fmt -- --check`, `cargo test --locked`,
  `cargo clippy --all-targets --all-features -- -D warnings`, and
  `cargo doc --no-deps` with the pinned toolchain.
