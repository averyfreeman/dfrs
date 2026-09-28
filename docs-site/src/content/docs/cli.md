---
title: CLI reference
description: Commands and options for the dfrs terminal report.
---

## Basic use

```sh
dfrs
dfrs /var/log /Users
dfrs --local --human-readable
```

With no path arguments, dfrs reports visible capacity-bearing mounts. With path
arguments, it selects the deepest matching mount for each canonicalized path.

## See it in action

The recordings below use `tests/fixtures/mounts.txt` so their output stays
stable across machines. Omit `--mounts tests/fixtures/mounts.txt` to use the
native mount provider on your system.

### Default filtering and broader visibility

```sh
dfrs --color always --mounts tests/fixtures/mounts.txt
dfrs --color always --all --mounts tests/fixtures/mounts.txt
```

The first command shows the concise capacity-bearing view; `--all` also keeps
pseudo mounts such as `tmpfs` in the report.

<div class="dfrs-terminal-still">
  <img src="/dfrs/demos/dfrs-visibility.png" alt="Default and --all dfrs reports" />
</div>

### Custom output columns

```sh
dfrs --color always --si \
  --columns filesystem,bar,used_percentage,available,capacity,mounted_on \
  --mounts tests/fixtures/mounts.txt
```

Use `--columns` to keep the report focused, and `--si` when decimal units are
more useful than powers of 1024.

<div class="dfrs-terminal-still">
  <img src="/dfrs/demos/dfrs-columns.png" alt="Custom dfrs output columns" />
</div>

## Visibility

- `-a` / `--more` broadens the listing; repeat `-a` or use `--all` to include
  pseudo filesystems.
- The default hides runtime pseudo mounts such as `proc`, `sysfs`, `tmpfs`, and
  `devfs` while retaining capacity-bearing APFS, ZFS, squashfs, ext4, btrfs,
  and other real filesystems.
- `-l` / `--local` removes known remote filesystem types.

## Formatting

- `-h` / `--human-readable` uses powers of 1024.
- `-H` / `--si` uses powers of 1000.
- `-i` / `--inodes` reports inode capacity instead of byte capacity.
- `--columns filesystem,type,bar,used_percentage,available,used,capacity,mounted_on`
  selects the table columns.
- `--color auto|always|never` and `-c` control terminal color behavior.

## Mount discovery

```sh
dfrs --mounts ./tests/fixtures/mounts.txt --all
```

`--mounts FILE` is an explicit override. Mount-file fields follow the Linux
format and decode octal escapes such as `\040` for a space. Without the
override, macOS uses `getmntinfo(3)` and Linux reads `/proc/self/mounts`.

## Other commands

```sh
dfrs completions bash > ~/.local/share/bash-completion/completions/dfrs
dfrs --help
dfrs --version
```
