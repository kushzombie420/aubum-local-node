import os
import sys
import storage_librarian as v1

ARCHIVES = {".zip", ".7z", ".rar", ".iso", ".img"}
INSTALLERS = {".exe", ".msi"}
MODELS = {".gguf", ".safetensors", ".pt", ".pth"}
MEDIA = {".mp4", ".mov", ".mkv", ".wav", ".flac"}

RECOVERY_FOLDERS = {
    "aubum_control",
    "aubumtools",
    "aubum_action_sandbox",
    "llama-cuda-b10689",
}

RECOVERY_TARGETS = {
    "aubum_control": r"D:\Aubum Recovery\Core\Aubum_Control",
    "aubumtools": r"D:\Aubum Recovery\Core\AubumTools",
    "aubum_action_sandbox": r"D:\Aubum Recovery\Core\Aubum_Action_Sandbox",
    "llama-cuda-b10689": r"D:\Aubum Recovery\Runtime\llama-cuda-b10689",
}

PROJECT_ARCHIVES = r"E:\Project Archives"
SOFTWARE_ARCHIVES = r"E:\Software Archives"
UNREAL_ARCHIVES = r"E:\Unreal Archives"
ASSET_LIBRARY = r"E:\Asset Library"
AI_MEDIA = r"E:\AI Media"


def recommend(name, size, is_folder=False):
    low = name.lower()
    ext = os.path.splitext(low)[1]

    if is_folder:
        if low in RECOVERY_FOLDERS:
            return "BACKUP TO D"
        if any(x in low for x in ("backup", "archive", "old")):
            return "ARCHIVE TO E"
        if any(x in low for x in ("cache", "temp", "tmp", "output", "screenshots")):
            return "BULK/CACHE REVIEW"
        if size >= 1 * 1024**3:
            return "LARGE FOLDER REVIEW"
        return "KEEP / REVIEW"

    if ext in ARCHIVES:
        return "ARCHIVE TO E"
    if ext in INSTALLERS:
        return "ARCHIVE TO E"
    if ext in MODELS:
        return "KEEP ON C IF ACTIVE"
    if ext in MEDIA and size >= 1024**3:
        return "ARCHIVE TO E"
    if size >= 10 * 1024**3:
        return "LARGE FILE REVIEW"
    return "KEEP / REVIEW"


def proposed_destination(name, recommendation, is_folder=False):
    low = name.lower()

    if recommendation == "BACKUP TO D":
        return RECOVERY_TARGETS.get(low)

    if recommendation != "ARCHIVE TO E":
        return None

    if is_folder:
        # C:\AIWork\Archive is a container for retired project work.
        # Its contents belong under the existing Project Archives tree.
        if low == "archive":
            return PROJECT_ARCHIVES
        return os.path.join(PROJECT_ARCHIVES, name)

    ext = os.path.splitext(low)[1]

    if ext in INSTALLERS or ext in ARCHIVES:
        return os.path.join(SOFTWARE_ARCHIVES, name)

    if ext in MEDIA:
        return os.path.join(AI_MEDIA, name)

    return os.path.join(PROJECT_ARCHIVES, name)


def folder_size(path):
    total = 0
    for dirpath, _dirnames, filenames in os.walk(path, followlinks=False):
        for fname in filenames:
            fp = os.path.join(dirpath, fname)
            try:
                total += os.path.getsize(fp)
            except (OSError, ValueError):
                pass
    return total


def include_known_recovery_folders(root, dirs):
    present = {name.lower() for name, _size in dirs}
    extras = []

    try:
        entries = list(os.scandir(root))
    except OSError:
        return dirs

    for entry in entries:
        try:
            if not entry.is_dir(follow_symlinks=False):
                continue
        except OSError:
            continue

        low = entry.name.lower()
        if low in RECOVERY_FOLDERS and low not in present:
            extras.append((entry.name, folder_size(entry.path)))

    return dirs + extras


def destination_status(destination, source_size, is_folder):
    if not destination:
        return None

    if not os.path.exists(destination):
        return "MISSING"

    try:
        if is_folder:
            dest_size = folder_size(destination)
        else:
            dest_size = os.path.getsize(destination)
    except (OSError, ValueError):
        return "EXISTS - SIZE UNKNOWN"

    if dest_size == source_size:
        return f"EXISTS - SIZE MATCH ({v1._humanize(dest_size).strip()})"

    delta = dest_size - source_size
    sign = "+" if delta >= 0 else "-"
    return (
        f"EXISTS - SIZE DIFF "
        f"(dest {v1._humanize(dest_size).strip()}, "
        f"{sign}{v1._humanize(abs(delta)).strip()})"
    )


def plan_for(name, size, is_folder=False):
    recommendation = recommend(name, size, is_folder)
    destination = proposed_destination(name, recommendation, is_folder)

    if recommendation == "BACKUP TO D":
        action = "COPY -> VERIFY SHA256"
        source_delete = "NO"
    elif recommendation == "ARCHIVE TO E":
        if is_folder and name.lower() == "archive":
            action = "COPY CONTENTS -> VERIFY SHA256"
        else:
            action = "COPY -> VERIFY SHA256"
        source_delete = "EXPLICIT APPROVAL ONLY"
    else:
        action = "NONE"
        source_delete = "NO"

    return recommendation, destination, action, source_delete


def print_entry(kind, name, size, is_folder=False):
    recommendation, destination, action, source_delete = plan_for(
        name, size, is_folder
    )

    print(
        f"{kind:<4}  {v1._humanize(size):>14}  "
        f"{recommendation:<28} {name}"
    )

    if destination:
        status = destination_status(destination, size, is_folder)
        print(f"      PROPOSED DESTINATION: {destination}")
        print(f"      DESTINATION STATUS:   {status}")
        print(f"      ACTION:               {action}")
        print(f"      SOURCE DELETE:        {source_delete}")


target = sys.argv[1] if len(sys.argv) > 1 else "."
root, dirs, files = v1._scan(target)
dirs = include_known_recovery_folders(root, dirs)

print("\nStorage Librarian Phase 3.3 - REAL E: LAYOUT")
print(f"Scanning: {root}\n")

for name, size in dirs:
    print_entry("DIR", name, size, True)

for name, size in files:
    print_entry("FILE", name, size, False)

print(
    "\nREAD-ONLY: no files or folders were moved, copied, deleted, "
    "renamed, hashed, or modified."
)
