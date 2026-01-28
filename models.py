from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class ScanResult:
    files: List[Path]
    total_size: int
    processed: int


@dataclass
class CopyResult:
    copied: int
    skipped: int
    versions_created: int
    total_files: int


@dataclass
class ProgressEvent:
    processed: int
    total: int
    percent: int


@dataclass
class DryRunResult:
    planned_copies: int
    planned_versions: int
    planned_skips: int
