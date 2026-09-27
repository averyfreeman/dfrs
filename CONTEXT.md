# dfrs

This context defines the vocabulary for dfrs as a command-line filesystem
usage viewer. It keeps platform discovery, filesystem classification, and
display behavior distinct so future changes remain compatible with the CLI.

## Filesystem vocabulary

**Filesystem**:
A mounted storage surface whose capacity and availability dfrs reports.
_Avoid_: disk, volume

**Mount**:
The operating-system association between a filesystem and the directory where
it is available to the process.
_Avoid_: attachment, mount point when referring to the complete association

**Mount provider**:
The platform-specific source of the mounts dfrs can inspect.
_Avoid_: parser, mount file

**Mount-file override**:
An explicit user-supplied mount listing used as the discovery input instead of
the platform default.
_Avoid_: configuration file, fixture

**Capacity-bearing filesystem**:
A filesystem for which the operating system reports usable capacity and free
space, making it eligible for the default report.
_Avoid_: real filesystem, data mount

**Pseudo mount**:
An operating-system or runtime mount that does not represent reportable local
storage capacity in the default view.
_Avoid_: fake filesystem, system filesystem

**Local filesystem**:
A filesystem that dfrs does not classify as remote storage.
_Avoid_: physical filesystem, native filesystem

## Display vocabulary

**Display filter**:
The user-selected breadth of filesystem visibility, from the concise default
through broader views that include pseudo mounts.
_Avoid_: verbosity level when discussing filesystem visibility

**Filesystem alias**:
A shorter human-facing name derived from a filesystem identifier, such as an
LVM device path.
_Avoid_: label, display name

**Output column**:
One named field in the tabular report, such as capacity, available space, or
mount directory.
_Avoid_: metric, table cell

**Path target**:
A file or directory argument whose containing filesystem dfrs reports.
_Avoid_: input file, mount path
