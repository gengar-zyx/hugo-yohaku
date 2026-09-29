#!/usr/bin/env python3
"""Build the example independently, including when the theme directory is renamed."""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hugo", default="hugo", help="Hugo executable (>= 0.165.0)")
    args = parser.parse_args()
    executable = shutil.which(args.hugo)
    if not executable:
        parser.error(f"Hugo executable not found: {args.hugo}")
    subprocess.run([executable, "version"], check=True)
    source = Path(__file__).resolve().parents[1]

    with tempfile.TemporaryDirectory(prefix="yohaku-standalone-", dir="/tmp") as work:
        work = Path(work)
        theme = work / "renamed-theme"
        shutil.copytree(
            source, theme,
            ignore=shutil.ignore_patterns(".git", "public", "resources", "__pycache__", ".hugo_build.lock"),
        )
        for drafts in (False, True):
            output = work / ("drafts" if drafts else "production")
            command = [
                executable, "--source", str(theme / "exampleSite"),
                "--themesDir", str(work), "--theme", theme.name,
                "--cacheDir", str(work / "cache"), "--destination", str(output),
                "--gc", "--minify",
            ]
            if drafts:
                command.append("--buildDrafts")
            subprocess.run(command, check=True, cwd=work)
            subprocess.run(
                [sys.executable, str(theme / "tests/check_build.py"), str(output)],
                check=True, cwd=work,
            )
            draft_page = output / "posts/draft-note/index.html"
            assert draft_page.is_file() == drafts, "Unexpected draft publication state"
            index = json.loads((output / "index.json").read_text())
            indexed_draft = any("/posts/draft-note/" in item["permalink"] for item in index)
            assert indexed_draft == drafts, "Unexpected draft search index state"
            for page in ("search", "archives", "categories", "tags"):
                assert (output / page / "index.html").is_file(), f"Missing {page} page"
        print("PASS: independent renamed theme, production and draft builds, search and list pages.")


if __name__ == "__main__":
    main()
