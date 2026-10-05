import argparse
import os
import shutil

import storage_librarian_v0_3_6 as v36
import storage_librarian_v0_4b as v4b
import storage_librarian_v0_4c as v4c

RECOVERY_ROOT = os.path.abspath(r"D:\Aubum Recovery")


def under_recovery_root(path):
    try:
        return os.path.commonpath([os.path.abspath(path), RECOVERY_ROOT]) == RECOVERY_ROOT
    except ValueError:
        return False


def remove_temp(path, is_folder):
    if not os.path.exists(path):
        return
    if is_folder:
        shutil.rmtree(path)
    else:
        os.remove(path)


def copy_to_temp(source, temp_path, is_folder):
    parent = os.path.dirname(temp_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    if is_folder:
        shutil.copytree(source, temp_path)
    else:
        shutil.copy2(source, temp_path)


def refresh_destination(item):
    source = item["source"]
    destination = item["destination"]
    is_folder = item["is_folder"]

    temp_path = destination + ".refresh_tmp"
    old_path = destination + ".refresh_old"

    if os.path.exists(temp_path) or os.path.exists(old_path):
        return "REFUSE", "stale refresh temp/old path already exists"

    try:
        copy_to_temp(source, temp_path, is_folder)
    except Exception as exc:
        return "FAILED", f"temp copy failed: {exc}"

    try:
        temp_check = v4b.verify_pair(source, temp_path, is_folder)
    except Exception as exc:
        try:
            remove_temp(temp_path, is_folder)
        except Exception:
            pass
        return "FAILED", f"temp verification failed: {exc}"

    if temp_check["status"] != "MATCH":
        try:
            remove_temp(temp_path, is_folder)
        except Exception:
            pass
        return "FAILED", f"temp verification status: {temp_check['status']}"

    try:
        os.rename(destination, old_path)
        os.rename(temp_path, destination)
    except Exception as exc:
        if os.path.exists(old_path) and not os.path.exists(destination):
            try:
                os.rename(old_path, destination)
            except Exception:
                pass
        return "FAILED", f"swap failed: {exc}"

    try:
        final_check = v4b.verify_pair(source, destination, is_folder)
    except Exception as exc:
        final_check = {"status": "ERROR", "error": str(exc)}

    if final_check["status"] != "MATCH":
        bad_path = destination + ".refresh_bad"
        try:
            if os.path.exists(bad_path):
                remove_temp(bad_path, is_folder)
            os.rename(destination, bad_path)
            os.rename(old_path, destination)
        except Exception:
            pass
        return "FAILED", f"final verification status: {final_check['status']}"

    try:
        remove_temp(old_path, is_folder)
    except Exception as exc:
        return "SUCCESS_WITH_CLEANUP_WARNING", f"new backup verified; old backup cleanup failed: {exc}"

    return "SUCCESS", "backup refreshed and verified"


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Storage Librarian Phase 4E. Safely refreshes DIFFERENT existing "
            "BACKUP TO D destinations using verified temp copy + swap. "
            "Source files are never deleted."
        )
    )
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument(
        "--execute-refresh",
        action="store_true",
        help="Enable interactive REFRESH prompts. Without this flag, plan only.",
    )
    args = parser.parse_args()

    root, items = v4c.collect_items(args.target)

    print("\nStorage Librarian Phase 4E - VERIFIED BACKUP REFRESH")
    print(f"Scanning: {root}")
    print("SOURCE DELETE: NEVER")
    print("ONLY BACKUP TO D ITEMS ARE ELIGIBLE.\n")

    candidates = 0
    refreshed = 0
    matched = 0
    skipped = 0
    refused = 0
    failed = 0

    for item in items:
        if item["recommendation"] != "BACKUP TO D":
            continue

        source = item["source"]
        destination = item["destination"]

        if not destination or not under_recovery_root(destination):
            print(f"REFUSE DESTINATION: {destination}")
            refused += 1
            continue

        if not os.path.exists(destination):
            print(f"REFUSE MISSING BACKUP DESTINATION: {destination}")
            print("  Use Phase 4C for missing destinations.")
            refused += 1
            continue

        try:
            result = v4b.verify_pair(source, destination, item["is_folder"])
        except Exception as exc:
            print(f"VERIFY FAILED: {source} -> {destination}: {exc}")
            failed += 1
            continue

        if result["status"] == "MATCH":
            print(f"SKIP MATCH: {source}")
            matched += 1
            continue

        if result["status"] != "DIFFERENT":
            print(f"REFUSE STATUS {result['status']}: {destination}")
            refused += 1
            continue

        candidates += 1
        print("\nREFRESH CANDIDATE - VERIFIED DIFFERENT")
        print(f"  SOURCE:      {source}")
        print(f"  DESTINATION: {destination}")
        print("  METHOD:      copy to temp -> SHA256 verify -> swap -> verify -> remove old backup")
        print("  SOURCE DELETE: NEVER")

        if not args.execute_refresh:
            print("  PLAN ONLY: use --execute-refresh to allow a refresh prompt.")
            continue

        confirmation = input(
            "  Type REFRESH exactly to replace ONLY the backup destination shown above: "
        ).strip()

        if confirmation != "REFRESH":
            print("  SKIPPED: refresh approval not given.")
            skipped += 1
            continue

        status, message = refresh_destination(item)

        if status == "SUCCESS":
            print(f"  REFRESHED: {message}.")
            refreshed += 1
        elif status == "SUCCESS_WITH_CLEANUP_WARNING":
            print(f"  REFRESHED WITH WARNING: {message}")
            refreshed += 1
        elif status == "REFUSE":
            print(f"  REFUSED: {message}")
            refused += 1
        else:
            print(f"  REFRESH FAILED: {message}")
            failed += 1

    print("\nSUMMARY")
    print(f"  different backup candidates: {candidates}")
    print(f"  refreshed+verified: {refreshed}")
    print(f"  already matched: {matched}")
    print(f"  skipped: {skipped}")
    print(f"  refused: {refused}")
    print(f"  failed: {failed}")
    print(
        "\nSAFETY: Phase 4E never deletes C: sources. It only replaces an "
        "existing D:\\Aubum Recovery backup after a temporary copy verifies "
        "as an exact SHA256 match."
    )


if __name__ == "__main__":
    main()
