import os
import sys
import storage_librarian as v1

ARCHIVES = {".zip",".7z",".rar",".iso",".img"}
INSTALLERS = {".exe",".msi"}
MODELS = {".gguf",".safetensors",".pt",".pth"}
MEDIA = {".mp4",".mov",".mkv",".wav",".flac"}

RECOVERY_FOLDERS = {"aubum_control","aubumtools","aubum_action_sandbox","llama-cuda-b10689"}

def recommend(name, size, is_folder=False):
    low = name.lower()
    ext = os.path.splitext(low)[1]

    if is_folder:
        if low in RECOVERY_FOLDERS:
            return "BACKUP TO D"
        if any(x in low for x in ("backup","archive","old")):
            return "ARCHIVE TO E"
        if any(x in low for x in ("cache","temp","tmp","output","screenshots")):
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

target = sys.argv[1] if len(sys.argv) > 1 else "."
root, dirs, files = v1._scan(target)

print("\nStorage Librarian Phase 2A - RECOMMENDATIONS ONLY")
print(f"Scanning: {root}\n")

for name, size in dirs:
    print(f"DIR   {v1._humanize(size):>14}  {recommend(name,size,True):<28} {name}")

for name, size in files:
    print(f"FILE  {v1._humanize(size):>14}  {recommend(name,size):<28} {name}")

print("\nREAD-ONLY: nothing in the scanned target was moved, deleted, renamed, or modified.")
