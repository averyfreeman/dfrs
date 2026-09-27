---
name: terminal-capture
description: Record terminal workflows with asciinema and share them as .cast files or GIFs, with visual verification of GIF timing. Use whenever the user wants to record, capture, demo, or screencast a terminal session, CLI workflow, or shell commands; wants a terminal GIF for a README, PR, Slack, or docs; mentions asciinema, .cast files, or agg; or asks to convert a terminal recording to a GIF. Also use when a user says things like "show people how this command works" or "make a demo of this CLI tool".
---

# Terminal Capture

Record a terminal workflow with asciinema, optionally convert it to a GIF,
and visually verify the GIF's timing before sharing. Works headless
(Claude's container, Claude Code non-interactive) and on a user's machine.

## Workflow overview

1. Record the workflow to a `.cast` file (asciinema)
2. Offer GIF conversion (agg preferred, bundled `scripts/cast2gif.py` as fallback)
3. Verify the GIF: run `scripts/verify_gif.py`, then visually inspect the
   exported sample frames
4. Deliver the `.cast` and/or `.gif` to the user

Always offer step 2 after recording. A `.cast` file is small and
high-fidelity but needs a player; a GIF plays anywhere (READMEs, Slack,
PR descriptions). Ask which the user wants if unclear, or produce both.

## 1. Recording

Check for asciinema, install if missing:

```bash
asciinema --version || pip install asciinema --break-system-packages || pipx install asciinema || brew install asciinema
```

### Headless / scripted recording (Claude container, Claude Code)

Wrap the workflow in a script and record it non-interactively:

```bash
asciinema rec demo.cast -c ./workflow.sh -q --overwrite
```

Write `workflow.sh` to look like a real session, not raw command output.
Echo a fake prompt before each command, and pace it with short sleeps so
the recording reads naturally:

```bash
#!/bin/bash
PS1='\[\e[32m\]user@host\[\e[0m\]:\[\e[34m\]~/project\[\e[0m\]$ '
echo -e "${PS1@P}git status"        # show the command being "typed"
sleep 0.6                            # beat before output appears
git status
sleep 1.5                            # let the viewer read the output
```

Notes:
- `${PS1@P}` is bash-only; use a plain `echo -e "\e[32muser@host\e[0m$ cmd"` for sh
- 0.4 to 0.8s pause after a "typed" command, 1 to 2s after its output; anything
  longer gets capped at conversion time anyway
- Terminal size comes from the recording environment. Force it if the default
  is wrong for the content: `asciinema rec --cols 100 --rows 30 ...` (v3) or
  run under `stty cols 100 rows 30` inside the wrapped script (v2 ignores
  size flags; header records the pty size)
- Destructive or stateful commands: run them for real only if the user asked;
  otherwise fake the output with `echo`/`cat` so the demo is safe to re-record

### Interactive recording (user's own machine)

If the user wants to record themselves driving the session, give them the
command to run in their own terminal and wait:

```bash
asciinema rec demo.cast      # exit the shell or Ctrl-D to stop
```

Then continue from their `.cast` file.

## 2. GIF conversion (offer this)

Preferred converter: **agg** (asciinema's own renderer, best glyph and
theme quality). Getting agg, in order of preference:

```bash
# 1. Package manager (user machines)
brew install agg || sudo apt install agg 2>/dev/null

# 2. Prebuilt binary (fails in sandboxes that block release-assets.githubusercontent.com)
curl -fsSL -o /usr/local/bin/agg https://github.com/asciinema/agg/releases/latest/download/agg-$(uname -m)-unknown-linux-gnu && chmod +x /usr/local/bin/agg

# 3. Build from source. HEAD needs Rust >= 1.85 (edition 2024); with an
#    older toolchain (Ubuntu 24 ships 1.75) pin a pre-2024 tag AND use
#    --locked, or unpinned transitive deps (e.g. zeroize) pull edition-2024
#    crates and break the build:
cargo install --git https://github.com/asciinema/agg --tag v1.5.0 --locked
```

Do not `cargo install agg` from crates.io: that is an unrelated crate.

The source build takes several minutes. In Claude's container, background
processes die between tool calls and commands have a time limit, so set
`CARGO_TARGET_DIR=/tmp/agg-target` and re-run the same `cargo install`
under `timeout 110` until it finishes; the persistent target dir makes each
retry resume where it stopped. In Claude Code, run it in the background.
If the build is more trouble than it is worth, use the fallback renderer;
output quality is close enough for most demos.

agg usage:

```bash
agg demo.cast demo.gif --idle-time-limit 2 --speed 1 --font-size 16
```

**Fallback when agg is unavailable** (common in Claude's container): use the
bundled renderer. Same knobs, pure Python (pyte + Pillow):

```bash
pip install pyte pillow --break-system-packages
python3 scripts/cast2gif.py demo.cast demo.gif --idle-limit 2 --speed 1
```

It prints a timing summary (cast duration, adjusted timeline, GIF duration).

Both converters hold the final frame so the end state is readable before
the loop restarts, but by different amounts: the bundled renderer holds
for 1s, agg for 3s (`--last-frame-duration`, default 3). The verifier
needs to know which, see below.

### Timing knobs

- `--idle-limit` / `--idle-time-limit`: cap dead air between events.
  2s is a good default; 1s for snappy demos
- `--speed`: 1.0 for typed-feel demos; 1.5 to 2 for long build/test output
- GIF delays are quantised to 10ms and delays under 20ms get clamped to
  ~100ms by many viewers. The bundled renderer merges near-simultaneous
  events and carries quantisation error forward, so totals stay honest

## 3. Verify the GIF (always do this before delivering)

Run the bundled verifier. It checks total playback time against the cast
timeline (with the same speed and idle-limit values used for conversion)
and exports evenly spaced sample frames:

```bash
python3 scripts/verify_gif.py demo.gif --cast demo.cast --idle-limit 2 --speed 1 --samples 4 --outdir ./frames
```

Exit 0 means timing is within tolerance (default 15%); exit 1 means
mismatch. `--final-hold` must match the converter's end-of-loop hold:
`1` for the bundled renderer (the default), `3` for agg's default, or
whatever `--last-frame-duration` was set to. A mismatch here is the top
cause of false timing failures; a suspiciously clean error of exactly
2 to 3 seconds usually means the wrong `--final-hold`.

Then **look at the exported frames** with the image viewer (`view` in
Claude, Read in Claude Code) and confirm:

- First frame: not blank, shows the opening state
- Middle frames: visible progression (commands appear before their output;
  a progress bar mid-way, not already complete)
- Last frame: the finished state, nothing truncated, cursor not covering
  the punchline
- No garbled glyphs, mis-aligned columns, or wrong colours
- Heed the verifier's warning about sub-20ms frame delays: if present,
  re-convert with a larger `--min-frame` or lower fps

If timing is off: check speed/idle-limit mismatch between conversion and
verification first (the most common cause), then re-convert. If frames look
wrong: fix the workflow script pacing and re-record; do not hand-edit frames.

## 4. Delivering

- Present the `.gif` (and `.cast` if the user wants it) via the file
  presentation tool in Claude, or tell the user the paths in Claude Code
- Mention the observed size; GIFs of long sessions get large. Over ~5MB,
  offer to re-convert at higher `--speed`, smaller `--font-size`, or
  tighter `--idle-limit`
- `asciinema upload demo.cast` publishes to asciinema.org. It is public by
  default: never upload without the user explicitly asking, and warn about
  secrets in scrollback either way
- Recordings capture everything printed, including env vars, tokens in
  URLs, and file contents. Scan the cast (`grep -iE 'token|secret|key|password' demo.cast`)
  before sharing and re-record rather than trying to edit leaks out

## Environment gotchas (learned by testing)

- pip installs asciinema 2.x; `rec` needs `--overwrite` to replace an
  existing cast, and `-q` suppresses the start/stop banners
- Headless recording gets `TERM=linux` and no `$SHELL`; fine for scripted
  demos, but set `TERM=xterm-256color` inside the script if a tool degrades
  its output without it
- asciinema needs a real pty; `rec -c` provides one, so it works in
  containers without a tty on stdin
- The bundled renderer expects asciicast v2. asciinema 3.x records v3
  ("asciicast" header line); convert with `asciinema convert -f asciicast-v2 in.cast out.cast`
  or record with the pip-installed 2.x
