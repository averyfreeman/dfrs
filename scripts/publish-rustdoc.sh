#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site_root="$repo_root/docs-site"
generated_root="$site_root/.generated/rustdoc"
published_root="$site_root/public/rustdoc"

rm -rf "$generated_root" "$published_root"
mkdir -p "$generated_root" "$published_root"

(
    cd "$repo_root"
    cargo doc --locked --no-deps --document-private-items --target-dir "$generated_root"
)

cp -R "$generated_root/doc/." "$published_root/"
