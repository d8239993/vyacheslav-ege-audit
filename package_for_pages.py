#!/usr/bin/env python3
"""Собирает папку _site для GitHub Pages (только статика для публикации)."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "_site"

SKIP_NAMES = {
    "_site",
    "node_modules",
    ".git",
    ".github",
}
ROOT_FILES = ("index.html", "report.html")
COPY_DIRS = ("css", "charts", "js")
COPY_SUBDIRS = ("physics",)  # physics/index.html + physics/css/


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    for name in ROOT_FILES:
        src = ROOT / name
        if not src.is_file():
            print(f"Нет файла: {src}", file=sys.stderr)
            sys.exit(1)
        shutil.copy2(src, SITE / name)

    for name in COPY_DIRS:
        src = ROOT / name
        if not src.is_dir():
            print(f"Нет каталога: {src}", file=sys.stderr)
            sys.exit(1)
        copy_tree(src, SITE / name)

    for name in COPY_SUBDIRS:
        src = ROOT / name
        if src.is_dir():
            copy_tree(src, SITE / name)

    (SITE / ".nojekyll").touch()
    print(f"OK: собрано в {SITE}", file=sys.stderr)


if __name__ == "__main__":
    main()
