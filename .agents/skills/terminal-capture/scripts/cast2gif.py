#!/usr/bin/env python3
"""Render an asciicast v2 (.cast) file to an animated GIF.

Pure-Python fallback for environments where agg cannot be installed
(no Rust toolchain, blocked binary downloads). Uses pyte for VT100
emulation and Pillow for rasterisation.

Deps: pip install pyte pillow

Usage:
  python3 cast2gif.py input.cast output.gif [options]

Options:
  --speed FLOAT        Playback speed multiplier (default 1.0)
  --idle-limit FLOAT   Cap idle gaps between events, seconds (default 2.0, 0 = no cap)
  --font-size INT      Font size in px (default 16)
  --font PATH          Path to a monospace TTF (default: DejaVu Sans Mono)
  --min-frame FLOAT    Merge events closer than this, seconds (default 0.04)
  --cols INT           Override terminal columns
  --rows INT           Override terminal rows

Exits non-zero on error. Prints a timing summary (cast duration,
adjusted duration, GIF duration, frame count) on success. GIF frame
durations are quantised to 10ms (the GIF format's granularity); the
renderer carries the rounding error forward so total duration stays
accurate.
"""
import argparse
import json
import sys

try:
    import pyte
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    sys.exit(f"Missing dependency: {e.name}. Run: pip install pyte pillow")

# 16-colour palette (VGA-ish, matches common terminal defaults)
PALETTE = {
    "black": (0, 0, 0), "red": (205, 49, 49), "green": (13, 188, 121),
    "brown": (229, 229, 16), "yellow": (229, 229, 16), "blue": (36, 114, 200),
    "magenta": (188, 63, 188), "cyan": (17, 168, 205), "white": (229, 229, 229),
    "brightblack": (102, 102, 102), "brightred": (241, 76, 76),
    "brightgreen": (35, 209, 139), "brightbrown": (245, 245, 67),
    "brightyellow": (245, 245, 67), "brightblue": (59, 142, 234),
    "brightmagenta": (214, 112, 214), "brightcyan": (41, 184, 219),
    "brightwhite": (255, 255, 255),
}
DEFAULT_FG = (229, 229, 229)
DEFAULT_BG = (16, 16, 16)
DEFAULT_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def resolve_colour(value, default, bold=False):
    if value in ("default", None):
        return default
    if isinstance(value, str):
        if bold and not value.startswith("bright") and "bright" + value in PALETTE:
            return PALETTE["bright" + value]
        if value in PALETTE:
            return PALETTE[value]
        try:  # pyte reports 256/truecolour as 6-digit hex
            v = value.lstrip("#")
            return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))
        except (ValueError, IndexError):
            return default
    return default


def load_cast(path):
    with open(path) as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip()]
    header = json.loads(lines[0])
    if header.get("version") != 2:
        sys.exit(f"Unsupported asciicast version: {header.get('version')} (only v2)")
    events = []
    for ln in lines[1:]:
        ts, kind, data = json.loads(ln)
        if kind == "o":
            events.append((float(ts), data))
    return header, events


def build_frames(events, speed, idle_limit, min_frame):
    """Return [(duration_seconds, accumulated_data)] with idle capping,
    speed adjustment, and merging of near-simultaneous events."""
    if not events:
        return []
    # Recompute a compressed timeline: cap gaps, then divide by speed
    timeline = []
    prev_ts = 0.0
    t = 0.0
    for ts, data in events:
        gap = ts - prev_ts
        if idle_limit > 0:
            gap = min(gap, idle_limit)
        t += gap / speed
        timeline.append((t, data))
        prev_ts = ts
    # Merge events closer together than min_frame
    frames = []  # (start_time, data)
    for t, data in timeline:
        if frames and (t - frames[-1][0]) < min_frame:
            frames[-1] = (frames[-1][0], frames[-1][1] + data)
        else:
            frames.append((t, data))
    # Convert start times to durations (duration of frame i = time until frame i+1)
    out = []
    for i, (t, data) in enumerate(frames):
        if i + 1 < len(frames):
            dur = frames[i + 1][0] - t
        else:
            dur = 1.0  # hold the final frame for a second
        out.append((dur, data))
    return out


def render(header, frames, out_path, font_path, font_size, cols, rows):
    cols = cols or header.get("width", 80)
    rows = rows or header.get("height", 24)
    font = ImageFont.truetype(font_path, font_size)
    try:
        bold_font = ImageFont.truetype(BOLD_FONT, font_size)
    except OSError:
        bold_font = font
    bbox = font.getbbox("M")
    cw = font.getlength("M")
    ascent, descent = font.getmetrics()
    ch = ascent + descent
    cw = int(round(cw))
    img_w, img_h = cols * cw, rows * ch

    screen = pyte.Screen(cols, rows)
    stream = pyte.Stream(screen)

    images, durations_ms = [], []
    err_ms = 0.0  # carry GIF 10ms quantisation error forward
    for dur, data in frames:
        stream.feed(data)
        img = Image.new("RGB", (img_w, img_h), DEFAULT_BG)
        draw = ImageDraw.Draw(img)
        buf = screen.buffer
        for y in range(rows):
            row = buf.get(y, {})
            for x in range(cols):
                cell = row.get(x)
                if cell is None:
                    continue
                fg = resolve_colour(cell.fg, DEFAULT_FG, cell.bold)
                bg = resolve_colour(cell.bg, DEFAULT_BG)
                if cell.reverse:
                    fg, bg = bg, fg
                px, py = x * cw, y * ch
                if bg != DEFAULT_BG:
                    draw.rectangle([px, py, px + cw - 1, py + ch - 1], fill=bg)
                if cell.data and cell.data != " ":
                    f = bold_font if cell.bold else font
                    draw.text((px, py), cell.data, font=f, fill=fg)
        # cursor block
        if not screen.cursor.hidden:
            cx, cy = screen.cursor.x, screen.cursor.y
            if cx < cols and cy < rows:
                px, py = cx * cw, cy * ch
                draw.rectangle([px, py, px + cw - 1, py + ch - 1],
                               fill=DEFAULT_FG)
                cell = buf.get(cy, {}).get(cx)
                if cell and cell.data and cell.data != " ":
                    draw.text((px, py), cell.data, font=font, fill=DEFAULT_BG)
        images.append(img)
        # quantise to 10ms with error diffusion so totals stay honest
        want = dur * 1000 + err_ms
        q = max(20, int(round(want / 10.0)) * 10)  # <20ms is unreliable in viewers
        err_ms = want - q
        durations_ms.append(q)

    if not images:
        sys.exit("No output events in cast; nothing to render")
    images[0].save(
        out_path, save_all=True, append_images=images[1:],
        duration=durations_ms, loop=0, optimize=True, disposal=1,
    )
    return durations_ms


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cast")
    ap.add_argument("gif")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--idle-limit", type=float, default=2.0)
    ap.add_argument("--font-size", type=int, default=16)
    ap.add_argument("--font", default=DEFAULT_FONT)
    ap.add_argument("--min-frame", type=float, default=0.04)
    ap.add_argument("--cols", type=int)
    ap.add_argument("--rows", type=int)
    args = ap.parse_args()

    header, events = load_cast(args.cast)
    if not events:
        sys.exit("Cast contains no output events")
    cast_dur = events[-1][0]
    frames = build_frames(events, args.speed, args.idle_limit, args.min_frame)
    adjusted = sum(d for d, _ in frames[:-1])  # excludes final hold
    durations = render(header, frames, args.gif, args.font,
                       args.font_size, args.cols, args.rows)
    gif_dur = sum(durations) / 1000.0
    print(f"cast duration:      {cast_dur:.2f}s ({len(events)} output events)")
    print(f"adjusted timeline:  {adjusted:.2f}s "
          f"(speed x{args.speed}, idle capped at {args.idle_limit}s)")
    print(f"gif written:        {args.gif}")
    print(f"gif frames:         {len(durations)}")
    print(f"gif duration:       {gif_dur:.2f}s (includes 1.0s final-frame hold)")


if __name__ == "__main__":
    main()
