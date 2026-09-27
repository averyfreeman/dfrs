#!/usr/bin/env python3
"""Verify the timing of a GIF produced from an asciicast recording.

Reads per-frame delays from the GIF, compares total duration against
the source .cast timeline (accounting for speed and idle-limit
adjustments), and exports evenly-spaced sample frames as PNGs for
visual inspection.

Deps: pip install pillow

Usage:
  python3 verify_gif.py output.gif [--cast input.cast] [--speed 1.0]
      [--idle-limit 2.0] [--samples 4] [--outdir DIR] [--tolerance 0.15]

Exit codes: 0 = timing within tolerance (or no cast given), 1 = timing
mismatch beyond tolerance, 2 = file/parse error.
"""
import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageSequence
except ImportError:
    sys.exit("Missing dependency: pillow. Run: pip install pillow")


def gif_timing(path):
    im = Image.open(path)
    delays = []
    for frame in ImageSequence.Iterator(im):
        delays.append(frame.info.get("duration", 0))
    return im.size, delays


def cast_expected_duration(path, speed, idle_limit):
    with open(path) as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip()]
    events = [json.loads(ln) for ln in lines[1:]]
    out_ts = [float(e[0]) for e in events if e[1] == "o"]
    if not out_ts:
        return None, 0
    prev, total = 0.0, 0.0
    for ts in out_ts:
        gap = ts - prev
        if idle_limit > 0:
            gap = min(gap, idle_limit)
        total += gap / speed
        prev = ts
    return total, len(out_ts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gif")
    ap.add_argument("--cast")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--idle-limit", type=float, default=2.0)
    ap.add_argument("--samples", type=int, default=4)
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--tolerance", type=float, default=0.15,
                    help="allowed relative error vs cast timeline (default 15%%)")
    ap.add_argument("--final-hold", type=float, default=1.0,
                    help="expected final-frame hold added by the renderer, seconds")
    args = ap.parse_args()

    if not os.path.exists(args.gif):
        sys.exit(2)
    (w, h), delays = gif_timing(args.gif)
    total = sum(delays) / 1000.0
    zero = sum(1 for d in delays if d < 20)

    print(f"gif:            {args.gif}")
    print(f"dimensions:     {w}x{h}")
    print(f"frames:         {len(delays)}")
    print(f"total duration: {total:.2f}s")
    print(f"frame delays:   min={min(delays)}ms max={max(delays)}ms "
          f"mean={sum(delays)/len(delays):.0f}ms")
    if zero:
        print(f"WARNING: {zero} frame(s) with <20ms delay; many viewers "
              f"clamp these to 100ms, which would stretch playback")

    rc = 0
    if args.cast:
        expected, n_events = cast_expected_duration(
            args.cast, args.speed, args.idle_limit)
        if expected is None:
            print("cast has no output events; skipping comparison")
        else:
            playback = total - args.final_hold  # renderer holds last frame
            err = abs(playback - expected) / max(expected, 0.001)
            print(f"cast timeline:  {expected:.2f}s "
                  f"(speed x{args.speed}, idle cap {args.idle_limit}s, "
                  f"{n_events} events)")
            print(f"gif playback:   {playback:.2f}s "
                  f"(excl. {args.final_hold}s final hold)")
            print(f"timing error:   {err*100:.1f}% "
                  f"(tolerance {args.tolerance*100:.0f}%)")
            if err > args.tolerance:
                print("RESULT: TIMING MISMATCH")
                rc = 1
            else:
                print("RESULT: timing OK")

    # export sample frames for visual inspection
    if args.samples > 0:
        outdir = args.outdir or os.path.dirname(os.path.abspath(args.gif))
        os.makedirs(outdir, exist_ok=True)
        im = Image.open(args.gif)
        n = im.n_frames
        idxs = sorted(set(
            min(n - 1, round(i * (n - 1) / max(args.samples - 1, 1)))
            for i in range(args.samples)))
        elapsed = [sum(delays[:i]) / 1000.0 for i in range(n)]
        base = os.path.splitext(os.path.basename(args.gif))[0]
        for i in idxs:
            im.seek(i)
            p = os.path.join(outdir, f"{base}_frame{i:03d}_t{elapsed[i]:.1f}s.png")
            im.convert("RGB").save(p)
            print(f"sample frame:   {p}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
