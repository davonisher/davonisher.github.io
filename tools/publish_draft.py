#!/usr/bin/env python3
"""Move a draft from collections/_drafts/ to collections/_posts/ for publishing."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DRAFTS_DIR = REPO_ROOT / "collections" / "_drafts"
POSTS_DIR = REPO_ROOT / "collections" / "_posts"


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = ascii_text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[-\s]+", "-", slug).strip("-")
    return slug or "untitled"


def parse_front_matter(content: str) -> tuple[dict[str, str], str]:
    if not content.startswith("---"):
        raise ValueError("Draft is missing YAML front matter.")

    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Draft front matter is malformed.")

    front_matter: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        front_matter[key.strip()] = value.strip()

    body = parts[2]
    if not body.startswith("\n"):
        body = "\n" + body
    return front_matter, body


def render_front_matter(front_matter: dict[str, str]) -> str:
    lines = ["---"]
    for key in ("layout", "title", "date", "summary", "categories"):
        if key in front_matter:
            lines.append(f"{key}: {front_matter[key]}")
    for key, value in front_matter.items():
        if key not in {"layout", "title", "date", "summary", "categories"}:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def resolve_draft_path(draft_arg: str) -> Path:
    candidate = Path(draft_arg)
    if candidate.exists():
        return candidate.resolve()

    drafts_candidate = DRAFTS_DIR / draft_arg
    if drafts_candidate.exists():
        return drafts_candidate.resolve()

    if not draft_arg.endswith(".md"):
        drafts_candidate = DRAFTS_DIR / f"{draft_arg}.md"
        if drafts_candidate.exists():
            return drafts_candidate.resolve()

    raise FileNotFoundError(f"Draft not found: {draft_arg}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish a draft as a dated blog post.")
    parser.add_argument(
        "draft",
        help="Draft filename or path inside collections/_drafts/",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Publish date in YYYY-MM-DD format (default: today)",
    )
    args = parser.parse_args()

    try:
        publish_date = date.fromisoformat(args.date)
    except ValueError:
        print(f"Invalid date: {args.date!r}. Use YYYY-MM-DD.", file=sys.stderr)
        return 1

    try:
        draft_path = resolve_draft_path(args.draft)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if DRAFTS_DIR.resolve() not in draft_path.parents:
        print(f"Draft must live in {DRAFTS_DIR}", file=sys.stderr)
        return 1

    content = draft_path.read_text(encoding="utf-8")
    try:
        front_matter, body = parse_front_matter(content)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    title = front_matter.get("title", draft_path.stem)
    slug = slugify(title)
    filename = f"{publish_date.isoformat()}-{slug}.md"
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    target = POSTS_DIR / filename

    if target.exists():
        print(f"Post already exists: {target}", file=sys.stderr)
        return 1

    front_matter.setdefault("layout", "post")
    front_matter["date"] = publish_date.isoformat()
    if not front_matter.get("summary"):
        front_matter["summary"] = "TODO: add a one-line summary."

    target.write_text(render_front_matter(front_matter) + body.lstrip("\n"), encoding="utf-8")
    draft_path.unlink()

    print(f"Published {target.relative_to(REPO_ROOT)}")
    print(f"Removed draft {draft_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
