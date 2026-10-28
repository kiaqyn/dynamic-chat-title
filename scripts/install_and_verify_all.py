#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meta-Driven Universal Adaptive Installer & Verifier for `dynamic-chat-title`
----------------------------------------------------------------------------
1. Auto-detects installed AI Agent platforms (Core 5 + 7 Third-Party Agents)
   and deploys the appropriate format (`SKILL.md` bundle, slash command, or rule).
2. Verifies Universal Third-Party Adapters (`adapters/`):
   - System Prompt / Rules Snippet (`universal_system_prompt.md`)
   - OpenAI Function Calling & MCP Tool Schema (`openai_function_tool.json`)
   - Middleware Regex Parser & OpenWebUI Outlet Filter (`middleware_regex_parser.py`)
3. Runs Official Codex Validator (`quick_validate.py`) and MVP Test Suite (`TC-01`~`TC-10`).
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()

# Meta-driven registry of Core + Third-Party Agent Platforms
PLATFORM_REGISTRY = [
    {
        "name": "Antigravity",
        "probe_dir": HOME / ".gemini",
        "target_dir": HOME / ".gemini" / "config" / "skills" / "dynamic-chat-title",
        "mode": "skill_dir",
        "core": True,
    },
    {
        "name": "OpenAI Codex",
        "probe_dir": HOME / ".codex",
        "target_dir": HOME / ".codex" / "skills" / "dynamic-chat-title",
        "mode": "skill_dir",
        "core": True,
    },
    {
        "name": "Claude Code (Skill)",
        "probe_dir": HOME / ".claude",
        "target_dir": HOME / ".claude" / "skills" / "dynamic-chat-title",
        "mode": "skill_dir",
        "core": True,
    },
    {
        "name": "Claude Code (/cmd)",
        "probe_dir": HOME / ".claude",
        "target_file": HOME / ".claude" / "commands" / "dynamic-chat-title.md",
        "mode": "single_md",
        "core": True,
    },
    {
        "name": "Cursor",
        "probe_dir": HOME / ".cursor",
        "target_dir": HOME / ".cursor" / "skills" / "dynamic-chat-title",
        "mode": "skill_dir",
        "core": True,
    },
    {
        "name": "Universal (.agents)",
        "probe_dir": HOME / ".agents",
        "target_dir": HOME / ".agents" / "skills" / "dynamic-chat-title",
        "mode": "skill_dir",
        "core": True,
    },
    # Third-Party IDE / CLI Agent Platforms (Auto-probed dynamically)
    {
        "name": "Windsurf (Codeium)",
        "probe_dir": HOME / ".codeium" / "windsurf",
        "target_dir": HOME / ".codeium" / "windsurf" / "skills" / "dynamic-chat-title",
        "mode": "skill_dir",
        "core": False,
    },
    {
        "name": "Cline",
        "probe_dir": HOME / ".cline",
        "target_dir": HOME / ".cline" / "skills" / "dynamic-chat-title",
        "mode": "skill_dir",
        "core": False,
    },
    {
        "name": "Roo Code",
        "probe_dir": HOME / ".roo",
        "target_dir": HOME / ".roo" / "skills" / "dynamic-chat-title",
        "mode": "skill_dir",
        "core": False,
    },
    {
        "name": "Trae",
        "probe_dir": HOME / ".trae",
        "target_dir": HOME / ".trae" / "skills" / "dynamic-chat-title",
        "mode": "skill_dir",
        "core": False,
    },
    {
        "name": "OpenCode",
        "probe_dir": HOME / ".config" / "opencode",
        "target_dir": HOME / ".config" / "opencode" / "skills" / "dynamic-chat-title",
        "mode": "skill_dir",
        "core": False,
    },
    {
        "name": "Continue.dev",
        "probe_dir": HOME / ".continue",
        "target_file": HOME / ".continue" / "rules" / "dynamic-chat-title.md",
        "mode": "single_md",
        "core": False,
    },
    {
        "name": "Goose",
        "probe_dir": HOME / ".config" / "goose",
        "target_dir": HOME / ".config" / "goose" / "skills" / "dynamic-chat-title",
        "mode": "skill_dir",
        "core": False,
    },
]

CODEX_OFFICIAL_VALIDATOR = (
    HOME / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
)


def adaptive_probe_and_sync(force_all: bool = False) -> list:
    print("=== [Step 1] Adaptive Environment Probing & Multi-Platform Sync ===")
    ignore_patterns = shutil.ignore_patterns("__pycache__", "*.pyc", ".git")
    skill_md_content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    installed_skill_dirs = []

    for entry in PLATFORM_REGISTRY:
        name = entry["name"]
        detected = entry["probe_dir"].exists()
        if not (entry["core"] or detected or force_all):
            print(f"  [AUTO-SKIP] {name:<22} (Host not detected at {entry['probe_dir']})")
            continue

        if entry["mode"] == "skill_dir":
            target_dir = entry["target_dir"]
            target_dir.parent.mkdir(parents=True, exist_ok=True)
            if target_dir.exists():
                shutil.rmtree(target_dir)
            shutil.copytree(ROOT, target_dir, ignore=ignore_patterns)
            installed_skill_dirs.append((name, target_dir))
            print(f"  [INSTALLED] {name:<22} -> {target_dir}")
        elif entry["mode"] == "single_md":
            target_file = entry["target_file"]
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(skill_md_content, encoding="utf-8")
            print(f"  [INSTALLED] {name:<22} -> {target_file}")

    return installed_skill_dirs


def verify_cross_platform_schema() -> None:
    print("\n=== [Step 2] Verifying Universal Schema & 4-Tier Adaptive Protocol ===")
    skill_md = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", skill_md, re.DOTALL)
    assert match, "SKILL.md missing valid YAML frontmatter block"
    fm_text = match.group(1)

    name_m = re.search(r"^name:\s*(.+)$", fm_text, re.MULTILINE)
    desc_m = re.search(r"^description:\s*(.+)$", fm_text, re.MULTILINE)
    assert name_m and desc_m, "Frontmatter must include `name` and `description`"

    name = name_m.group(1).strip().strip('"').strip("'")
    desc = desc_m.group(1).strip().strip('"').strip("'")

    assert name == "dynamic-chat-title", f"Name mismatch: {name}"
    assert re.match(r"^[a-z0-9-]+$", name), "Name must match ^[a-z0-9-]+$"
    assert 1 <= len(name) <= 64, "Name length must be 1..64"
    assert 20 <= len(desc) <= 1024, f"Description length {len(desc)} out of bounds (20..1024)"
    assert "<" not in desc and ">" not in desc, "Description cannot contain angle brackets (< or >)"
    assert "Tier 1" in skill_md and "Tier 2" in skill_md, "Missing 4-Tier Adaptive Protocol in SKILL.md"
    print("  [PASS] Universal Single-Line YAML Frontmatter & 4-Tier Adaptive Protocol")

    openai_yaml_path = ROOT / "agents" / "openai.yaml"
    assert openai_yaml_path.is_file(), "Missing agents/openai.yaml for Codex UI integration"
    openai_yaml = openai_yaml_path.read_text(encoding="utf-8")
    short_m = re.search(r'short_description:\s*"([^"]+)"', openai_yaml)
    prompt_m = re.search(r'default_prompt:\s*"([^"]+)"', openai_yaml)
    assert short_m and prompt_m, "Missing required fields in agents/openai.yaml"
    assert 25 <= len(short_m.group(1)) <= 64, "Codex short_description must be 25..64 chars"
    assert "$dynamic-chat-title" in prompt_m.group(1), "Codex default_prompt must reference $dynamic-chat-title"
    print("  [PASS] Codex Native UI Config (`agents/openai.yaml`)")


def verify_third_party_adapters() -> None:
    print("\n=== [Step 3] Verifying Universal Third-Party Adapters (`adapters/`) ===")
    # 1. Universal System Prompt snippet
    prompt_file = ROOT / "adapters" / "universal_system_prompt.md"
    assert prompt_file.is_file() and prompt_file.stat().st_size > 100, "Missing universal_system_prompt.md"
    print("  [PASS] Adapter 1: `adapters/universal_system_prompt.md` (Web UIs / .windsurfrules / .clinerules)")

    # 2. OpenAI Function Calling & MCP Tool JSON Schema
    schema_file = ROOT / "adapters" / "openai_function_tool.json"
    assert schema_file.is_file(), "Missing openai_function_tool.json"
    schema_data = json.loads(schema_file.read_text(encoding="utf-8"))
    assert schema_data["openai_tool"]["function"]["name"] == "update_chat_title"
    assert schema_data["mcp_tool"]["name"] == "update_chat_title"
    print("  [PASS] Adapter 2: `adapters/openai_function_tool.json` (Dify / Coze / FastGPT / LangChain / MCP)")

    # 3. Middleware Regex Parser & OpenWebUI Filter live test
    sys.path.insert(0, str(ROOT / "adapters"))
    import middleware_regex_parser as mw

    # Test Tier 2 HTML comment tag extraction
    t1, c1 = mw.extract_dynamic_title("好的，这是代码实现。\n<!-- dynamic-chat-title: 跨平台动态标题适配器 -->")
    assert t1 == "跨平台动态标题适配器" and "<!--" not in c1, f"Tag parser failed: {t1}"

    # Test Tier 3/4 Advisory line extraction
    t2, _ = mw.extract_dynamic_title("已完成重构。\n💡 **建议更新会话标题**：「Python 异步并发性能优化」")
    assert t2 == "Python 异步并发性能优化", f"Advisory parser failed: {t2}"

    # Test OpenWebUI Filter.outlet() hook
    flt = mw.Filter()
    mock_body = {
        "messages": [
            {"role": "user", "content": "帮我重构数据库索引"},
            {"role": "assistant", "content": "索引已优化。\n<!-- dynamic-chat-title: 数据库索引重构与优化 -->"},
        ]
    }
    out_body = flt.outlet(mock_body)
    assert out_body.get("dynamic_chat_title") == "数据库索引重构与优化"
    print("  [PASS] Adapter 3: `adapters/middleware_regex_parser.py` (Tag + Advisory + OpenWebUI Filter)")


def run_codex_official_validator(installed_skill_dirs: list) -> None:
    print("\n=== [Step 4] Running Official Codex Skill Validator (`quick_validate.py`) ===")
    if not CODEX_OFFICIAL_VALIDATOR.is_file():
        print("  [SKIP] Official Codex validator script not found on disk.")
        return

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    for platform_name, target_dir in installed_skill_dirs:
        res = subprocess.run(
            [sys.executable, str(CODEX_OFFICIAL_VALIDATOR), str(target_dir)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            check=False,
        )
        output = (res.stdout + res.stderr).strip()
        assert res.returncode == 0, f"Codex validator failed on {platform_name}: {output}"
        print(f"  [PASS] {platform_name:<22} -> Official Validator: {output}")


def run_mvp_test_suite() -> None:
    print("\n=== [Step 5] Running MVP Behavioral & Test Case Suite (`validate_skill.py`) ===")
    validator_script = ROOT / "tests" / "validate_skill.py"
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    res = subprocess.run(
        [sys.executable, str(validator_script)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        check=False,
    )
    assert res.returncode == 0, f"MVP test suite failed:\n{res.stdout}\n{res.stderr}"
    for line in res.stdout.strip().splitlines():
        print(f"  {line}")


def main() -> int:
    force_all = "--all" in sys.argv
    try:
        installed = adaptive_probe_and_sync(force_all=force_all)
        verify_cross_platform_schema()
        verify_third_party_adapters()
        run_codex_official_validator(installed)
        run_mvp_test_suite()
        print("\n======================================================================")
        print("ALL DETECTED PLATFORMS & UNIVERSAL THIRD-PARTY ADAPTERS 100% VERIFIED!")
        print("======================================================================")
        return 0
    except AssertionError as exc:
        print(f"\n[FAIL] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
