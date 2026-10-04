import argparse
import json
import os
import sys

import storage_librarian_v0_3_5 as v35


def build_manifest(target):
    root, dirs, files = v35.v1._scan(target)
    dirs = v35.include_known_recovery_folders(root, dirs)

    items = []

    def add_item(kind, source_path, name, size, is_folder, archive_context=False):
        if archive_context:
            destination = os.path.join(v35.PROJECT_ARCHIVES, name)
            recommendation = "ARCHIVE TO E"
            action = "COPY -> VERIFY SHA256"
            source_delete = "EXPLICIT APPROVAL ONLY"
        else:
            recommendation, destination, action, source_delete = v35.plan_for(
                name, size, is_folder
            )

        if not destination:
            return

        items.append(
            {
                "kind": kind,
                "source": source_path,
                "size_bytes": size,
                "recommendation": recommendation,
                "destination": destination,
                "destination_status": v35.destination_status(
                    destination, size, is_folder
                ),
                "action": action,
                "source_delete": source_delete,
            }
        )

    for name, size in dirs:
        source_path = os.path.join(root, name)

        if name.lower() == "archive":
            try:
                entries = list(os.scandir(source_path))
            except OSError:
                continue

            for entry in entries:
                try:
                    if entry.is_dir(follow_symlinks=False):
                        child_size = v35.folder_size(entry.path)
                        add_item(
                            "DIR",
                            entry.path,
                            entry.name,
                            child_size,
                            True,
                            archive_context=True,
                        )
                    elif entry.is_file(follow_symlinks=False):
                        child_size = entry.stat().st_size
                        add_item(
                            "FILE",
                            entry.path,
                            entry.name,
                            child_size,
                            False,
                            archive_context=True,
                        )
                except (OSError, ValueError):
                    pass
            continue

        add_item("DIR", source_path, name, size, True)

    for name, size in files:
        source_path = os.path.join(root, name)
        add_item("FILE", source_path, name, size, False)

    return {
        "phase": "4A",
        "mode": "APPROVAL MANIFEST ONLY",
        "target": root,
        "item_count": len(items),
        "items": items,
        "safety": {
            "copies_performed": False,
            "hashes_performed": False,
            "moves_performed": False,
            "deletes_performed": False,
            "renames_performed": False,
            "scanned_target_modified": False,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Storage Librarian Phase 4A approval manifest generator."
    )
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument(
        "--out",
        help="Optional JSON output path. If omitted, prints JSON only.",
    )
    args = parser.parse_args()

    manifest = build_manifest(args.target)
    text = json.dumps(manifest, indent=2)

    if args.out:
        out_path = os.path.abspath(args.out)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
            f.write("\n")
        print(f"Manifest written: {out_path}")
    else:
        print(text)

    print(
        "\nREAD-ONLY TARGET: no files or folders in the scanned target were "
        "moved, copied, deleted, renamed, hashed, or modified."
    )


if __name__ == "__main__":
    main()
