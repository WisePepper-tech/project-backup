import shutil
from pathlib import Path
from datetime import datetime


def create_snapshot_dir(backup_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    snapshot_dir = backup_root / timestamp
    snapshot_dir.mkdir(parents=True, exist_ok=False)
    return snapshot_dir


def copy_files(files: list[Path], source_root: Path, snapshot_root: Path):
    copied = 0
    errors = 0

    for file_path in files:
        try:
            relative_path = file_path.relative_to(source_root)
            destination = snapshot_root / relative_path

            destination.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(file_path, destination)
            copied += 1

        except Exception:
            errors += 1

    return {
        "copied": copied,
        "errors": errors,
    }
