#!/usr/bin/env python3
"""Create a new dated blog post in collections/_posts/."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "collections" / "_posts"


def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    slug = ascii_title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[-\s]+", "-", slug).strip("-")
    return slug or "untitled"


def build_front_matter(title: str, post_date: date, category: str) -> str:
    date_str = post_date.isoformat()
    return f"""---
layout: post
title: {title}
date: {date_str}
summary: TODO: add a one-line summary.
categories: {category}
---

"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new blog post markdown file.")
    parser.add_argument("title", help='Post title, e.g. "How to take care of plants"')
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Post date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--category",
        default="general",
        help="Category for front matter (default: general)",
    )
    args = parser.parse_args()

    try:
        post_date = date.fromisoformat(args.date)
    except ValueError:
        print(f"Invalid date: {args.date!r}. Use YYYY-MM-DD.", file=sys.stderr)
        return 1

    slug = slugify(args.title)
    filename = f"{post_date.isoformat()}-{slug}.md"
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    target = POSTS_DIR / filename

    if target.exists():
        print(f"Post already exists: {target}", file=sys.stderr)
        return 1

    target.write_text(build_front_matter(args.title, post_date, args.category), encoding="utf-8")
    print(f"Created {target.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
