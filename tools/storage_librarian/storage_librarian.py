#!/usr/bin/env python3
"""Storage Librarian - Phase 1.

Read-only scanner. Given a folder path, reports the 20 largest immediate
subfolders and the 30 largest files.  Nothing is moved, deleted, renamed,
modified, hashed, or categorised.
"""

import os
import sys

TOP_N_SUBFOLDERS = 20
TOP_N_FILES = 30


def _humanize(nbytes: int) -> str:
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if abs(nbytes) < 1024:
            return f"{nbytes:>10,.0f} {unit}"
        nbytes /= 1024
    return f"{nbytes:>10,.2f} PiB"


def _scan(path: str):
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    subfolder_sizes: list[tuple[str, int]] = []
    file_sizes: list[tuple[str, int]] = []

    for entry in os.scandir(path):
        try:
            if entry.is_dir(follow_symlinks=False):
                print(f"Scanning: {entry.path}")
                total = 0
                for dirpath, _dirnames, filenames in os.walk(
                    entry.path, followlinks=False
                ):
                    for fname in filenames:
                        fp = os.path.join(dirpath, fname)
                        try:
                            total += os.path.getsize(fp)
                        except (OSError, ValueError):
                            pass
                print(f"  {entry.name}: {_humanize(total)}")
                subfolder_sizes.append((entry.name, total))
            elif entry.is_file(follow_symlinks=False):
                try:
                    sz = entry.stat().st_size
                    file_sizes.append((entry.name, sz))
                except (OSError, ValueError):
                    pass
        except (OSError, ValueError):
            pass

    subfolder_sizes.sort(key=lambda x: x[1], reverse=True)
    file_sizes.sort(key=lambda x: x[1], reverse=True)

    return (
        path,
        subfolder_sizes[:TOP_N_SUBFOLDERS],
        file_sizes[:TOP_N_FILES],
    )


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    root, top_dirs, top_files = _scan(target)

    print()
    print(f"Storage Librarian  Phase 1  (read-only)")
    print(f"Scanning: {root}")
    print()

    # --- Subfolders ---
    print(f"Top {TOP_N_SUBFOLDERS} largest subfolders:")
    print(f"{'Rank':<6}{'Size':>14}  Folder")
    print("-" * 50)
    for i, (name, size) in enumerate(top_dirs, 1):
        print(f"{i:<6}{_humanize(size):>14}  {name}")
    print()

    # --- Files ---
    print(f"Top {TOP_N_FILES} largest files:")
    print(f"{'Rank':<6}{'Size':>14}  File")
    print("-" * 50)
    for i, (name, size) in enumerate(top_files, 1):
        print(f"{i:<6}{_humanize(size):>14}  {name}")


if __name__ == "__main__":
    main()
