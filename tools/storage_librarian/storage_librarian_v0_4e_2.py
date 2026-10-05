import argparse
import hashlib
import os
import shutil

import storage_librarian_v0_4c as v4c

RECOVERY_ROOT = os.path.abspath(r"D:\Aubum Recovery")
SCRATCH_ROOT = os.path.abspath(r"D:\")


def long_path(path):
    path = os.path.abspath(path)
    if os.name != "nt":
        return path
    if path.startswith("\\\\?\\"):
        return path
    if path.startswith("\\\\"):
        return "\\\\?\\UNC\\" + path[2:]
    return "\\\\?\\" + path


def under_recovery_root(path):
    try:
        return os.path.commonpath([os.path.abspath(path), RECOVERY_ROOT]) == RECOVERY_ROOT
    except ValueError:
        return False


def sha256_file(path, chunk_size=1024 * 1024):
    h = hashlib.sha256()
    with open(long_path(path), "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def sha256_tree(root):
    root_lp = long_path(root)
    h = hashlib.sha256()

    for dirpath, dirnames, filenames in os.walk(root_lp, followlinks=False):
        dirnames.sort()
        filenames.sort()

        for filename in filenames:
            path = os.path.join(dirpath, filename)
            rel = os.path.relpath(path, root_lp).replace("\\", "/")
            size = os.path.getsize(path)
            file_hash = sha256_file(path)

            h.update(rel.encode("utf-8", errors="surrogatepass"))
            h.update(b"\0")
            h.update(str(size).encode("ascii"))
            h.update(b"\0")
            h.update(file_hash.encode("ascii"))
            h.update(b"\n")

    return h.hexdigest()


def verify_pair(source, destination, is_folder):
    if not os.path.exists(long_path(destination)):
        return "MISSING"

    if is_folder:
        source_hash = sha256_tree(source)
        destination_hash = sha256_tree(destination)
    else:
        source_hash = sha256_file(source)
        destination_hash = sha256_file(destination)

    return "MATCH" if source_hash == destination_hash else "DIFFERENT"


def scratch_paths(destination):
    tag = hashlib.sha1(
        os.path.abspath(destination).encode("utf-8", errors="surrogatepass")
    ).hexdigest()[:8]
    return (
        os.path.join(SCRATCH_ROOT, f"AR_TMP_{tag}"),
        os.path.join(SCRATCH_ROOT, f"AR_OLD_{tag}"),
    )


def remove_path(path, is_folder):
    lp = long_path(path)
    if not os.path.exists(lp):
        return
    if is_folder:
        shutil.rmtree(lp)
    else:
        os.remove(lp)


def copy_to_temp(source, temp_path, is_folder):
    if is_folder:
        shutil.copytree(long_path(source), long_path(temp_path))
    else:
        shutil.copy2(long_path(source), long_path(temp_path))


def refresh_destination(item):
    source = item["source"]
    destination = item["destination"]
    is_folder = item["is_folder"]

    temp_path, old_path = scratch_paths(destination)

    if os.path.exists(long_path(temp_path)) or os.path.exists(long_path(old_path)):
        return "REFUSE", f"scratch path already exists: {temp_path} or {old_path}"

    try:
        copy_to_temp(source, temp_path, is_folder)
    except Exception as exc:
        return "FAILED", f"temp copy failed: {exc}"

    try:
        temp_status = verify_pair(source, temp_path, is_folder)
    except Exception as exc:
        return "FAILED", f"temp verification failed: {exc}"

    if temp_status != "MATCH":
        return "FAILED", f"temp verification status: {temp_status}"

    try:
        os.rename(long_path(destination), long_path(old_path))
        os.rename(long_path(temp_path), long_path(destination))
    except Exception as exc:
        if os.path.exists(long_path(old_path)) and not os.path.exists(long_path(destination)):
            try:
                os.rename(long_path(old_path), long_path(destination))
            except Exception:
                pass
        return "FAILED", f"swap failed: {exc}"

    try:
        final_status = verify_pair(source, destination, is_folder)
    except Exception as exc:
        final_status = f"ERROR: {exc}"

    if final_status != "MATCH":
        return "FAILED", f"final verification status: {final_status}"

    try:
        remove_path(old_path, is_folder)
    except Exception as exc:
        return (
            "SUCCESS_WITH_CLEANUP_WARNING",
            f"new backup verified; old backup cleanup failed: {exc}",
        )

    return "SUCCESS", "backup refreshed and verified"


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Storage Librarian Phase 4E.2. Safely refreshes DIFFERENT existing "
            "BACKUP TO D destinations using Windows long-path support and a "
            "short D: scratch path. Source files are never deleted."
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

    print("\nStorage Librarian Phase 4E.2 - LONG-PATH SAFE BACKUP REFRESH")
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

        if not os.path.exists(long_path(destination)):
            print(f"REFUSE MISSING BACKUP DESTINATION: {destination}")
            refused += 1
            continue

        try:
            status = verify_pair(source, destination, item["is_folder"])
        except Exception as exc:
            print(f"VERIFY FAILED: {source} -> {destination}: {exc}")
            failed += 1
            continue

        if status == "MATCH":
            print(f"SKIP MATCH: {source}")
            matched += 1
            continue

        if status != "DIFFERENT":
            print(f"REFUSE STATUS {status}: {destination}")
            refused += 1
            continue

        candidates += 1
        temp_path, old_path = scratch_paths(destination)

        print("\nREFRESH CANDIDATE - VERIFIED DIFFERENT")
        print(f"  SOURCE:      {source}")
        print(f"  DESTINATION: {destination}")
        print(f"  TEMP:        {temp_path}")
        print(f"  OLD BACKUP:  {old_path}")
        print("  METHOD:      long-path copy -> SHA256 verify -> swap -> verify -> remove old backup")
        print("  SOURCE DELETE: NEVER")

        legacy_temp = destination + ".refresh_tmp"
        if os.path.exists(long_path(legacy_temp)):
            print(f"  NOTE: legacy partial temp exists from prior failed run: {legacy_temp}")

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
        "\nSAFETY: Phase 4E.2 never deletes C: sources. It only replaces an "
        "existing D:\\Aubum Recovery backup after a long-path-safe temporary "
        "copy verifies as an exact SHA256 match."
    )


if __name__ == "__main__":
    main()
