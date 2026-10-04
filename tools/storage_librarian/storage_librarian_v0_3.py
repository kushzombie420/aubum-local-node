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

ARCHIVE_ROOT = r"E:\Archive"


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
        return os.path.join(ARCHIVE_ROOT, name)

    ext = os.path.splitext(low)[1]
    if ext in INSTALLERS:
        bucket = "Installers"
    elif ext in ARCHIVES:
        bucket = "Archives"
    elif ext in MEDIA:
        bucket = "Media"
    else:
        bucket = "Misc"

    return os.path.join(ARCHIVE_ROOT, bucket, name)


def plan_for(name, size, is_folder=False):
    recommendation = recommend(name, size, is_folder)
    destination = proposed_destination(name, recommendation, is_folder)

    if recommendation == "BACKUP TO D":
        action = "COPY -> VERIFY SHA256"
        source_delete = "NO"
    elif recommendation == "ARCHIVE TO E":
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
        print(f"      PROPOSED DESTINATION: {destination}")
        print(f"      ACTION:               {action}")
        print(f"      SOURCE DELETE:        {source_delete}")


target = sys.argv[1] if len(sys.argv) > 1 else "."
root, dirs, files = v1._scan(target)

print("\nStorage Librarian Phase 3 - PROPOSED ACTION PLAN")
print(f"Scanning: {root}\n")

for name, size in dirs:
    print_entry("DIR", name, size, True)

for name, size in files:
    print_entry("FILE", name, size, False)

print(
    "\nREAD-ONLY: no files or folders were moved, copied, deleted, "
    "renamed, hashed, or modified."
)
