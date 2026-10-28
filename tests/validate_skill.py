#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lightweight self-check & validation script for dynamic-chat-title Skill.
Zero external dependencies required (pure Python 3 standard library).
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "examples/conversations.md",
    "tests/test-cases.md",
]

FORBIDDEN_PATTERNS = [
    r"关于.+的讨论",
    r"关于.+的交流",
    r"震惊[！!]",
    r"sk-[a-zA-Z0-9]{10,}",
]


def is_valid_title(title: str) -> tuple[bool, str]:
    """Validate generated title against SKILL.md formatting & safety rules."""
    if not title or not title.strip():
        return False, "Title is empty"
    cjk_chars = re.findall(r"[\u4e00-\u9fff]", title)
    if cjk_chars:
        if not 6 <= len(cjk_chars) <= 16:
            return False, f"CJK title must have 6-16 Chinese chars: {title!r}"
    elif not 3 <= len(title.split()) <= 8:
        return False, f"English title must have 3-8 words: {title!r}"
    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, title):
            return False, f"Title matched forbidden pattern {pat!r}: {title!r}"
    return True, "OK"


def evaluate_title_decision(case: dict) -> str:
    """Reference MVP decision logic mirroring SKILL.md rules."""
    if case.get("user_explicit"):
        return "RENAME_ADVISORY" if not case.get("host_supports_rename", True) else "RENAME"
    if case.get("missing_history") or case.get("is_chitchat") or case.get("single_turn_tangent"):
        return "KEEP"
    if case.get("sustained_topic_shift") or case.get("umbrella_needed") or case.get("returned_to_main"):
        return "RENAME_ADVISORY" if not case.get("host_supports_rename", True) else "RENAME"
    return "KEEP"


SIMULATED_CASES = [
    {"id": "TC-01", "expected": "KEEP", "title": "Python 列表推导式与循环优化"},
    {"id": "TC-02", "expected": "KEEP", "title": "Photoshop 图层蒙版非破坏性修图", "single_turn_tangent": True},
    {"id": "TC-03", "expected": "RENAME", "title": "开发动态对话标题 Agent Skill", "sustained_topic_shift": True},
    {"id": "TC-04", "expected": "RENAME", "title": "Python 空间站函数与字典实战", "returned_to_main": True},
    {"id": "TC-05", "expected": "RENAME", "title": "Linux 服务器部署与安全加固", "umbrella_needed": True},
    {"id": "TC-06", "expected": "RENAME", "title": "琪与浅的认知分级记忆中枢", "user_explicit": True},
    {"id": "TC-07", "expected": "KEEP", "title": "JetBrains 全家桶配置与快捷键"},
    {"id": "TC-08", "expected": "KEEP", "title": "项目架构重构方案", "missing_history": True},
    {"id": "TC-09", "expected": "RENAME_ADVISORY", "title": "开发动态对话标题 Skill", "user_explicit": True, "host_supports_rename": False},
    {"id": "TC-10", "expected": "KEEP", "title": "长假日常闲聊与摸鱼", "is_chitchat": True},
]


def main() -> int:
    print("=== [dynamic-chat-title] MVP Self-Check & Validation ===")

    # 1. File integrity check
    for rel in REQUIRED_FILES:
        p = ROOT / rel
        assert p.is_file() and p.stat().st_size > 0, f"Missing or empty file: {rel}"
    print(f"[PASS] All {len(REQUIRED_FILES)} required files exist and are non-empty.")

    # 2. YAML Frontmatter check
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert re.match(r"^---\r?\n", skill_text), "SKILL.md must start with YAML frontmatter"
    assert "name: dynamic-chat-title" in skill_text, "SKILL.md missing required name field"
    assert "description:" in skill_text, "SKILL.md missing required description field"
    print("[PASS] SKILL.md YAML frontmatter valid.")

    # 3. Test cases document coverage check (TC-01 to TC-10)
    tc_text = (ROOT / "tests/test-cases.md").read_text(encoding="utf-8")
    for i in range(1, 11):
        tc_id = f"TC-{i:02d}"
        assert tc_id in tc_text, f"Missing {tc_id} in tests/test-cases.md"
    print("[PASS] All 10 standard test cases (TC-01 ~ TC-10) documented in tests/test-cases.md.")

    # 4. Decision logic & title specification check
    for item in SIMULATED_CASES:
        actual = evaluate_title_decision(item)
        assert actual == item["expected"], f"{item['id']} failed: got {actual}, expected {item['expected']}"
        ok, msg = is_valid_title(item["title"])
        assert ok, f"{item['id']} title invalid: {msg}"
    print(f"[PASS] All {len(SIMULATED_CASES)} simulated decision & title lint checks passed.")
    print("=== ALL CHECKS PASSED (100%) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
