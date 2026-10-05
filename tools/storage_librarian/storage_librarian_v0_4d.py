import argparse
import os
import shutil

import storage_librarian_v0_4b as v4b
import storage_librarian_v0_4c as v4c


def delete_source(path, is_folder):
    if is_folder:
        shutil.rmtree(path)
    else:
        os.remove(path)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Storage Librarian Phase 4D. Deletes archive sources only after "
            "the existing destination SHA256-verifies as an exact match. "
            "BACKUP TO D sources are never delete candidates."
        )
    )
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument(
        "--execute-delete",
        action="store_true",
        help="Enable interactive DELETE prompts. Without this flag, plan only.",
    )
    args = parser.parse_args()

    root, items = v4c.collect_items(args.target)

    print("\nStorage Librarian Phase 4D - VERIFIED ARCHIVE SOURCE CLEANUP")
    print(f"Scanning: {root}")
    print("BACKUP SOURCES ARE NEVER DELETED.")
    print("FAILED DOWNLOADS ARE REVIEW-ONLY IN THIS PHASE.\n")

    eligible = 0
    deleted = 0
    skipped = 0
    refused = 0
    failed = 0

    for item in items:
        source = item["source"]
        destination = item["destination"]
        is_folder = item["is_folder"]
        recommendation = item["recommendation"]

        if recommendation == "BACKUP TO D":
            print(f"SKIP BACKUP SOURCE: {source}")
            skipped += 1
            continue

        if recommendation == "FAILED DOWNLOAD REVIEW":
            print(f"REVIEW ONLY FAILED DOWNLOAD: {source}")
            skipped += 1
            continue

        if recommendation != "ARCHIVE TO E":
            skipped += 1
            continue

        if not os.path.exists(source):
            print(f"SKIP SOURCE MISSING: {source}")
            skipped += 1
            continue

        if not destination or not v4c.is_allowed_destination(destination):
            print(f"REFUSE DESTINATION: {destination}")
            refused += 1
            continue

        if not os.path.exists(destination):
            print(f"REFUSE DESTINATION MISSING: {destination}")
            refused += 1
            continue

        try:
            result = v4b.verify_pair(source, destination, is_folder)
        except Exception as exc:
            print(f"VERIFY FAILED: {source} -> {destination}: {exc}")
            failed += 1
            continue

        if result["status"] != "MATCH":
            print(
                f"REFUSE VERIFIED STATUS {result['status']}: "
                f"{source} -> {destination}"
            )
            refused += 1
            continue

        eligible += 1
        print("\nDELETE CANDIDATE - VERIFIED MATCH")
        print(f"  SOURCE:      {source}")
        print(f"  DESTINATION: {destination}")
        print(f"  SHA256:      {result['source_sha256']}")

        if not args.execute_delete:
            print("  PLAN ONLY: use --execute-delete to allow a delete prompt.")
            continue

        confirmation = input(
            "  Type DELETE exactly to remove ONLY the source shown above: "
        ).strip()

        if confirmation != "DELETE":
            print("  SKIPPED: delete approval not given.")
            skipped += 1
            continue

        try:
            delete_source(source, is_folder)
        except Exception as exc:
            print(f"  DELETE FAILED: {exc}")
            failed += 1
            continue

        if os.path.exists(source):
            print("  DELETE FAILED: source still exists.")
            failed += 1
        else:
            print("  SOURCE DELETED. VERIFIED DESTINATION REMAINS IN PLACE.")
            deleted += 1

    print("\nSUMMARY")
    print(f"  verified delete candidates: {eligible}")
    print(f"  deleted with explicit approval: {deleted}")
    print(f"  skipped: {skipped}")
    print(f"  refused: {refused}")
    print(f"  failed: {failed}")
    print(
        "\nSAFETY: deletion is limited to ARCHIVE TO E items whose existing "
        "destination SHA256 matches the source exactly. Each deletion requires "
        "typing DELETE. BACKUP TO D sources cannot be deleted by this phase."
    )


if __name__ == "__main__":
    main()
