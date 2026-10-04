#!/usr/bin/env python3
"""
Storage Librarian v0.1

Read-only storage analyzer extracted from the private Aubum prototype.

Given a target directory, it:
- recursively totals each immediate subfolder;
- prints progress while scanning;
- lists the 20 largest immediate subfolders;
- lists the 30 largest immediate files.

It does not move, delete, rename, hash, or otherwise modify user data.
"""

from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

TOP_FOLDERS = 20
TOP_FILES = 30


def format_size(size_bytes: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    value = float(size_bytes)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value):,} B"
            return f"{value:,.0f} {unit}"
        value /= 1024

    return f"{size_bytes:,} B"


def is_reparse_point(entry: os.DirEntry[str]) -> bool:
    """Avoid following Windows junctions/reparse points during recursive scans."""
    try:
        attrs = getattr(entry.stat(follow_symlinks=False), "st_file_attributes", 0)
        flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        return bool(flag and attrs & flag)
    except OSError:
        return False


def folder_size(path: Path) -> int:
    total = 0
    pending = [path]

    while pending:
        current = pending.pop()

        try:
            with os.scandir(current) as entries:
                for entry in entries:
                    try:
                        if entry.is_symlink() or is_reparse_point(entry):
                            continue

                        if entry.is_file(follow_symlinks=False):
                            total += entry.stat(follow_symlinks=False).st_size
                        elif entry.is_dir(follow_symlinks=False):
                            pending.append(Path(entry.path))
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            continue

    return total


def scan(target: Path) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    folders: list[tuple[int, str]] = []
    files: list[tuple[int, str]] = []

    try:
        entries = sorted(target.iterdir(), key=lambda p: p.name.casefold())
    except OSError as exc:
        raise RuntimeError(f"Could not read target: {target}: {exc}") from exc

    for entry in entries:
        try:
            if entry.is_dir() and not entry.is_symlink():
                print(f"Scanning: {entry}")
                size = folder_size(entry)
                print(f"  {entry.name}: {format_size(size):>12}")
                folders.append((size, entry.name))
            elif entry.is_file():
                files.append((entry.stat().st_size, entry.name))
        except (OSError, PermissionError):
            continue

    folders.sort(reverse=True, key=lambda item: item[0])
    files.sort(reverse=True, key=lambda item: item[0])
    return folders, files


def print_ranked(title: str, rows: list[tuple[int, str]], name_label: str) -> None:
    print()
    print(title)
    print(f"{'Rank':<6}{'Size':>14}  {name_label}")
    print("-" * 50)

    for rank, (size, name) in enumerate(rows, start=1):
        print(f"{rank:<6}{format_size(size):>14}  {name}")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python storage_librarian.py <folder>")
        return 2

    target = Path(sys.argv[1]).expanduser()

    if not target.exists():
        print(f"Target does not exist: {target}")
        return 2

    if not target.is_dir():
        print(f"Target is not a directory: {target}")
        return 2

    folders, files = scan(target)

    print()
    print("Storage Librarian  Phase 1  (read-only)")
    print(f"Scanning: {target}")

    print_ranked(
        f"Top {TOP_FOLDERS} largest subfolders:",
        folders[:TOP_FOLDERS],
        "Folder",
    )
    print_ranked(
        f"Top {TOP_FILES} largest files:",
        files[:TOP_FILES],
        "File",
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
