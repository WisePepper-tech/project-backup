import shutil
import logging
from pathlib import Path
from datetime import datetime


def copy_files(
    files,
    src_root: Path,
    dst_root: Path,
    dry_run: bool = False,
    logger=None,
):
    logger = logger or logging.getLogger(__name__)

    copied = 0
    skipped = 0
    versions_created = 0

    planned_copies = 0
    planned_versions = 0
    planned_skips = 0

    for src_path in files:
        rel_path = src_path.relative_to(src_root)
        dst_path = dst_root / rel_path
        if not dry_run:
            dst_path.parent.mkdir(parents=True, exist_ok=True)

        if not dst_path.exists():
            if dry_run:
                logger.info(f"[DRY-RUN] Would copy new file: {rel_path}")
                planned_copies += 1
            else:
                shutil.copy2(src_path, dst_path)
                copied += 1
            continue

        if dst_path.exists():
            if dry_run:
                planned_skips += 1
            else:
                skipped += 1
            continue

        src_stat = src_path.stat()
        dst_stat = dst_path.stat()

        if src_stat.st_size == dst_stat.st_size and int(src_stat.st_mtime) == int(
            dst_stat.st_mtime
        ):
            skipped += 1
            continue

        # VERSIONED BACKUP
        timestamp = datetime.now().strftime("%Y-%m-%d - %H.%M")
        versioned_name = dst_path.stem + f"_{timestamp}" + dst_path.suffix
        versioned_path = dst_path.with_name(versioned_name)

        if dry_run:
            logger.info(
                f"[DRY-RUN] Would create version: "
                f"{versioned_path.name} → replace with new file"
            )
            planned_versions += 1
            planned_copies += 1
        else:
            shutil.move(dst_path, versioned_path)
            shutil.copy2(src_path, dst_path)
            versions_created += 1
            copied += 1

    if dry_run:
        return {
            "dry_run": True,
            "planned_copies": planned_copies,
            "planned_versions": planned_versions,
            "planned_skips": planned_skips,
        }

    return {
        "dry_run": False,
        "copied": copied,
        "versions_created": versions_created,
        "skipped": skipped,
    }
