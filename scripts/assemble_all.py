"""One-command final assembly: all chapters + full thesis with index and references."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def run(name: str) -> None:
    subprocess.run([sys.executable, str(SCRIPTS / name)], check=True)


def assemble_all() -> None:
    """Generate figures + full thesis (skips individual docx if locked)."""
    from generate_full_thesis import main as build_full
    build_full()


def main() -> None:
    assemble_all()


if __name__ == "__main__":
    main()
