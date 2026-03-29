#!/usr/bin/env python3
"""Bidirectional audit for Markdown image references and local image assets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")
MARKDOWN_SUFFIXES = (".md", ".markdown")
IMAGE_REF_RE = re.compile(
    r"(?P<path>/[^)\"' <>\s]+\.(?:png|jpg|jpeg|gif|webp|svg))",
    re.IGNORECASE,
)


def normalize_public_path(value: str) -> str:
    return "/" + value.lstrip("/")


def content_files(root: Path) -> list[Path]:
    content_root = root / "content"
    files: list[Path] = []
    for suffix in MARKDOWN_SUFFIXES:
        files.extend(content_root.rglob(f"*{suffix}"))
    return sorted(files)


def collect_markdown_references(root: Path) -> dict[str, list[str]]:
    refs: dict[str, list[str]] = defaultdict(list)
    for file_path in content_files(root):
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()

        rel_path = file_path.relative_to(root).as_posix()
        for line_no, line in enumerate(lines, start=1):
            for match in IMAGE_REF_RE.finditer(line):
                public_path = normalize_public_path(match.group("path").rstrip())
                refs[public_path].append(f"{rel_path}:{line_no}")
    return dict(sorted(refs.items()))


def collect_assets(root: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    assets: dict[str, list[str]] = defaultdict(list)
    collisions: dict[str, list[str]] = {}

    for base_dir_name in ("static", "assets"):
        base_dir = root / base_dir_name
        if not base_dir.exists():
            continue

        for file_path in sorted(base_dir.rglob("*")):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            public_path = normalize_public_path(file_path.relative_to(base_dir).as_posix())
            assets[public_path].append(file_path.relative_to(root).as_posix())

    for public_path, physical_paths in assets.items():
        if len(physical_paths) > 1:
            collisions[public_path] = physical_paths

    return dict(sorted(assets.items())), dict(sorted(collisions.items()))


def build_report(root: Path) -> dict[str, object]:
    refs = collect_markdown_references(root)
    assets, collisions = collect_assets(root)

    missing = {
        public_path: refs[public_path]
        for public_path in sorted(set(refs) - set(assets))
    }
    unused = {
        public_path: assets[public_path]
        for public_path in sorted(set(assets) - set(refs))
    }

    return {
        "summary": {
            "markdown_reference_count": len(refs),
            "asset_count": len(assets),
            "missing_count": len(missing),
            "unused_count": len(unused),
            "collision_count": len(collisions),
        },
        "missing": missing,
        "unused": unused,
        "collisions": collisions,
    }


def render_text(report: dict[str, object]) -> str:
    summary = report["summary"]
    missing = report["missing"]
    unused = report["unused"]
    collisions = report["collisions"]

    lines = [
        "Markdown image audit",
        (
            "summary: "
            f"refs={summary['markdown_reference_count']}, "
            f"assets={summary['asset_count']}, "
            f"missing={summary['missing_count']}, "
            f"unused={summary['unused_count']}, "
            f"collisions={summary['collision_count']}"
        ),
        "",
        "[missing]",
    ]

    if missing:
        for public_path, sources in missing.items():
            lines.append(f"- {public_path}")
            for source in sources:
                lines.append(f"  {source}")
    else:
        lines.append("(none)")

    lines.extend(["", "[unused]"])
    if unused:
        for public_path, physical_paths in unused.items():
            lines.append(f"- {public_path}")
            for physical_path in physical_paths:
                lines.append(f"  {physical_path}")
    else:
        lines.append("(none)")

    lines.extend(["", "[collisions]"])
    if collisions:
        for public_path, physical_paths in collisions.items():
            lines.append(f"- {public_path}")
            for physical_path in physical_paths:
                lines.append(f"  {physical_path}")
    else:
        lines.append("(none)")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify Markdown image references against local image assets."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root. Defaults to the parent of scripts/.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of text.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    report = build_report(root)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))

    summary = report["summary"]
    has_issues = any(
        summary[key] > 0 for key in ("missing_count", "unused_count", "collision_count")
    )
    return 1 if has_issues else 0


if __name__ == "__main__":
    sys.exit(main())
