#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Host Session Title Updater (`rename_host_session.py`)
---------------------------------------------------------------
Enables CLI/IDE Agents without a built-in MCP rename tool (such as Claude Code)
to physically update their active session title in local session storage and
terminal window headers.

Usage:
    python rename_host_session.py "<new_title>" [--host auto|claude|terminal]
"""

import json
import os
import sys
from pathlib import Path

HOME = Path.home()


def set_terminal_window_title(title: str) -> None:
    """Emit OSC 0 ANSI escape sequence to update terminal tab/window title."""
    sys.stdout.write(f"\033]0;{title}\007")
    sys.stdout.flush()


def update_claude_code_session_title(title: str) -> str:
    """
    Locate the most recently active Claude Code session JSONL file in
    ~/.claude/projects/ and append a custom-title / summary record so
    `claude --resume` and session pickers display the updated title.
    """
    projects_dir = HOME / ".claude" / "projects"
    if not projects_dir.is_dir():
        return "claude_projects_dir_not_found"

    jsonl_files = list(projects_dir.rglob("*.jsonl"))
    if not jsonl_files:
        return "no_claude_session_files"

    latest_file = max(jsonl_files, key=lambda p: p.stat().st_mtime)
    session_id = latest_file.stem

    # Read last leaf uuid if present
    leaf_uuid = None
    try:
        lines = latest_file.read_text(encoding="utf-8", errors="ignore").splitlines()
        for line in reversed(lines):
            if not line.strip():
                continue
            data = json.loads(line)
            if "uuid" in data:
                leaf_uuid = data["uuid"]
                break
    except Exception:
        pass

    records = [
        {
            "type": "custom-title",
            "customTitle": title,
            "sessionId": session_id,
        }
    ]
    if leaf_uuid:
        records.append(
            {
                "type": "summary",
                "summary": title,
                "leafUuid": leaf_uuid,
            }
        )

    with latest_file.open("a", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    return str(latest_file)


def main() -> int:
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("Usage: python rename_host_session.py <new_title>", file=sys.stderr)
        return 1

    new_title = sys.argv[1].strip()
    set_terminal_window_title(new_title)
    claude_res = update_claude_code_session_title(new_title)
    print(
        json.dumps(
            {
                "status": "ok",
                "new_title": new_title,
                "terminal_title_updated": True,
                "claude_session_updated": claude_res,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
