import argparse
import hashlib
import json
import os

import storage_librarian_v0_3_6 as v36


def sha256_file(path, chunk_size=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def sha256_tree(root):
    h = hashlib.sha256()

    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        filenames.sort()

        for filename in filenames:
            path = os.path.join(dirpath, filename)
            rel = os.path.relpath(path, root).replace("\\", "/")

            try:
                size = os.path.getsize(path)
                file_hash = sha256_file(path)
            except OSError:
                continue

            h.update(rel.encode("utf-8", errors="surrogatepass"))
            h.update(b"\0")
            h.update(str(size).encode("ascii"))
            h.update(b"\0")
            h.update(file_hash.encode("ascii"))
            h.update(b"\n")

    return h.hexdigest()


def verify_pair(source, destination, is_folder):
    if not os.path.exists(destination):
        return {
            "status": "MISSING",
            "source_sha256": None,
            "destination_sha256": None,
        }

    if is_folder != os.path.isdir(destination):
        return {
            "status": "TYPE MISMATCH",
            "source_sha256": None,
            "destination_sha256": None,
        }

    if is_folder:
        source_hash = sha256_tree(source)
        destination_hash = sha256_tree(destination)
    else:
        source_hash = sha256_file(source)
        destination_hash = sha256_file(destination)

    return {
        "status": "MATCH" if source_hash == destination_hash else "DIFFERENT",
        "source_sha256": source_hash,
        "destination_sha256": destination_hash,
    }


def collect_items(target):
    root, dirs, files = v36.v1._scan(target)
    dirs = v36.include_known_recovery_folders(root, dirs)
    items = []

    def add_item(kind, source_path, name, size, is_folder, archive_context=False):
        if archive_context:
            recommendation = "ARCHIVE TO E"
            destination = os.path.join(v36.PROJECT_ARCHIVES, name)
            action = "COPY -> VERIFY SHA256"
            source_delete = "EXPLICIT APPROVAL ONLY"
        else:
            recommendation, destination, action, source_delete = v36.plan_for(
                name, size, is_folder, source_path
            )

        if recommendation == "FAILED DOWNLOAD REVIEW":
            items.append(
                {
                    "kind": kind,
                    "source": source_path,
                    "size_bytes": size,
                    "recommendation": recommendation,
                    "destination": None,
                    "verification": {
                        "status": "NOT APPLICABLE",
                        "source_sha256": None,
                        "destination_sha256": None,
                    },
                    "action": action,
                    "source_delete": source_delete,
                }
            )
            return

        if not destination:
            return

        verification = verify_pair(source_path, destination, is_folder)

        items.append(
            {
                "kind": kind,
                "source": source_path,
                "size_bytes": size,
                "recommendation": recommendation,
                "destination": destination,
                "verification": verification,
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
                        add_item(
                            "DIR",
                            entry.path,
                            entry.name,
                            v36.folder_size(entry.path),
                            True,
                            archive_context=True,
                        )
                    elif entry.is_file(follow_symlinks=False):
                        add_item(
                            "FILE",
                            entry.path,
                            entry.name,
                            entry.stat().st_size,
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

    return root, items


def main():
    parser = argparse.ArgumentParser(
        description="Storage Librarian Phase 4B read-only verification planner."
    )
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument(
        "--out",
        help="Optional JSON output path. If omitted, prints JSON only.",
    )
    args = parser.parse_args()

    root, items = collect_items(args.target)

    manifest = {
        "phase": "4B",
        "mode": "READ-ONLY VERIFICATION",
        "target": root,
        "item_count": len(items),
        "items": items,
        "safety": {
            "copies_performed": False,
            "moves_performed": False,
            "deletes_performed": False,
            "renames_performed": False,
            "source_or_destination_modified": False,
            "hashes_read_only": True,
        },
    }

    text = json.dumps(manifest, indent=2)

    if args.out:
        out_path = os.path.abspath(args.out)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
            f.write("\n")
        print(f"Verification manifest written: {out_path}")
    else:
        print(text)

    print(
        "\nREAD-ONLY: files may have been hashed for comparison, but no "
        "source or destination files were copied, moved, deleted, renamed, "
        "or modified."
    )


if __name__ == "__main__":
    main()
