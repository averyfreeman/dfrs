#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

export TERM=xterm-256color
export LC_ALL=C

dfrs_bin="${DFRS_BIN:-$repo_root/target/debug/dfrs}"
if [[ ! -x "$dfrs_bin" ]]; then
    printf 'Build dfrs first or set DFRS_BIN to an executable.\n' >&2
    exit 1
fi

type_text() {
    local text="$1"
    local char

    while [[ -n "$text" ]]; do
        char="${text:0:1}"
        printf '%s' "$char"
        text="${text:1}"
        sleep 0.07
    done
}

command_text="dfrs --color always --mounts tests/fixtures/mounts.txt"

printf '\033[1;35mdemo@host\033[0m:\033[1;34m~/dfrs\033[0m$ '
type_text "$command_text"
printf '\r\n'
sleep 0.35

"$dfrs_bin" --color always --mounts "$repo_root/tests/fixtures/mounts.txt"

# Keep the painted report visible before emitting a harmless final event. The
# final event gives an asciicast player a five-second end-of-recording hold.
sleep 5
printf '\033[0m'
