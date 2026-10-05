import argparse
import os
import shutil
import sys

import storage_librarian_v0_3_6 as v36
import storage_librarian_v0_4b as v4b

ALLOWED_DESTINATION_ROOTS = (
    os.path.abspath(r"D:\Aubum Recovery"),
    os.path.abspath(r"E:\Project Archives"),
    os.path.abspath(r"E:\Software Archives"),
    os.path.abspath(r"E:\Unreal Archives"),
    os.path.abspath(r"E:\Asset Library"),
    os.path.abspath(r"E:\AI Media"),
)


def is_allowed_destination(path):
    dest = os.path.abspath(path)
    for root in ALLOWED_DESTINATION_ROOTS:
        try:
            if os.path.commonpath([dest, root]) == root:
                return True
        except ValueError:
            continue
    return False


def collect_items(target):
    root, dirs, files = v36.v1._scan(target)
    dirs = v36.include_known_recovery_folders(root, dirs)
    items = []

    def add_item(kind, source_path, name, size, is_folder, archive_context=False):
        if archive_context:
            recommendation = "ARCHIVE TO E"
            destination = os.path.join(v36.PROJECT_ARCHIVES, name)
            source_delete = "EXPLICIT APPROVAL ONLY"
        else:
            recommendation, destination, _action, source_delete = v36.plan_for(
                name, size, is_folder, source_path
            )

        if recommendation == "FAILED DOWNLOAD REVIEW":
            items.append(
                {
                    "kind": kind,
                    "source": source_path,
                    "size_bytes": size,
                    "is_folder": is_folder,
                    "recommendation": recommendation,
                    "destination": None,
                    "source_delete": source_delete,
                }
            )
            return

        if destination:
            items.append(
                {
                    "kind": kind,
                    "source": source_path,
                    "size_bytes": size,
                    "is_folder": is_folder,
                    "recommendation": recommendation,
                    "destination": destination,
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


def copy_missing_item(item):
    source = item["source"]
    destination = item["destination"]
    is_folder = item["is_folder"]

    parent = os.path.dirname(destination)
    if parent:
        os.makedirs(parent, exist_ok=True)

    if is_folder:
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)

    return v4b.verify_pair(source, destination, is_folder)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Storage Librarian Phase 4C. Copies only to missing destinations, "
            "verifies with SHA256, never deletes source files, and refuses to "
            "overwrite existing destinations."
        )
    )
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Enable interactive COPY prompts. Without this flag, plan only.",
    )
    args = parser.parse_args()

    root, items = collect_items(args.target)

    print("\nStorage Librarian Phase 4C - MISSING-ONLY COPY + VERIFY")
    print(f"Scanning: {root}")
    print("NO DELETE CODE. EXISTING DESTINATIONS ARE NEVER OVERWRITTEN.\n")

    copied = 0
    matched = 0
    refused = 0
    skipped = 0
    failed = 0

    for item in items:
        source = item["source"]
        destination = item["destination"]

        if item["recommendation"] == "FAILED DOWNLOAD REVIEW":
            print(f"SKIP FAILED DOWNLOAD: {source}")
            skipped += 1
            continue

        if not destination or not is_allowed_destination(destination):
            print(f"REFUSE DESTINATION: {destination}")
            refused += 1
            continue

        if os.path.exists(destination):
            result = v4b.verify_pair(source, destination, item["is_folder"])
            status = result["status"]

            if status == "MATCH":
                print(f"SKIP MATCH: {source}")
                matched += 1
            else:
                print(f"REFUSE EXISTING {status}: {destination}")
                refused += 1
            continue

        print("\nCOPY CANDIDATE")
        print(f"  SOURCE:      {source}")
        print(f"  DESTINATION: {destination}")
        print(f"  POLICY:      source delete = {item['source_delete']}")

        if not args.execute:
            print("  PLAN ONLY: use --execute to allow an interactive copy prompt.")
            skipped += 1
            continue

        confirmation = input("  Type COPY to create this destination: ").strip()
        if confirmation != "COPY":
            print("  SKIPPED: approval not given.")
            skipped += 1
            continue

        try:
            result = copy_missing_item(item)
        except Exception as exc:
            print(f"  COPY FAILED: {exc}")
            failed += 1
            continue

        if result["status"] == "MATCH":
            print("  VERIFIED MATCH: copy completed successfully.")
            copied += 1
        else:
            print(
                "  VERIFY FAILED: destination was left in place for manual review. "
                f"Status: {result['status']}"
            )
            failed += 1

    print("\nSUMMARY")
    print(f"  copied+verified: {copied}")
    print(f"  already matched: {matched}")
    print(f"  refused existing/different: {refused}")
    print(f"  skipped: {skipped}")
    print(f"  failed: {failed}")
    print(
        "\nSAFETY: this phase has no delete operation and never overwrites an "
        "existing destination."
    )


if __name__ == "__main__":
    main()
