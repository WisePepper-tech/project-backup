from pathlib import Path
import logging
from typing import Callable, Optional

from scanner import scan_folder, count_files
from copier import copy_files
from models import ScanResult, CopyResult, ProgressEvent, DryRunResult


def run_backup(
    source: Path,
    destination: Path,
    dry_run: bool = False,
    on_progress: Optional[Callable[[ProgressEvent], None]] = None,
    logger=None,
) -> CopyResult:
    logger = logger or logging.getLogger(__name__)

    total_files = count_files(source)

    def wrapped_progress(processed: int):
        if not on_progress:
            return

        percent = int((processed / total_files) * 100) if total_files else 100

        on_progress(
            ProgressEvent(
                processed=processed,
                total=total_files,
                percent=percent,
            )
        )

    scan_result: ScanResult = scan_folder(source, on_progress=wrapped_progress)

    copy_stats = copy_files(
        files=scan_result.files,
        src_root=source,
        dst_root=destination,
        dry_run=dry_run,
        logger=logger,
    )

    if copy_stats.get("dry_run"):
        return DryRunResult(
            planned_copies=copy_stats["planned_copies"],
            planned_versions=copy_stats["planned_versions"],
            planned_skips=copy_stats["planned_skips"],
        )

    return CopyResult(
        copied=copy_stats["copied"],
        skipped=copy_stats["skipped"],
        versions_created=copy_stats["versions_created"],
        total_files=total_files,
    )
