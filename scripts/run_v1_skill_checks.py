#!/usr/bin/env python3
"""Run the gen-tgo-ppt-skill V1 maintenance test harness."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TEXT_EXTS = {".md", ".py", ".yaml", ".yml", ".json", ".txt"}
EXPECTED_VERSION = "V1"


def run(cmd: list[str], cwd: Path | None = None, expect: int | None = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if expect is not None and result.returncode != expect:
        raise AssertionError(
            f"Command failed: {' '.join(cmd)}\nreturncode={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
        )
    return result


def read_text_files() -> dict[Path, str]:
    texts: dict[Path, str] = {}
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.name == "run_v1_skill_checks.py":
            continue
        if path.is_file() and path.suffix.lower() in TEXT_EXTS:
            texts[path] = path.read_text(encoding="utf-8")
    return texts


def check_frontmatter() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", skill, flags=re.S)
    if not match:
        raise AssertionError("SKILL.md frontmatter missing")
    fields = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            raise AssertionError(f"Invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    if set(fields) != {"name", "description"}:
        raise AssertionError(f"Unexpected frontmatter fields: {sorted(fields)}")
    if fields["name"] != "gen-tgo-ppt-skill" or not fields["description"]:
        raise AssertionError("SKILL.md frontmatter values invalid")


def check_no_stale_text() -> None:
    texts = read_text_files()
    forbidden = {
        "V8.02": "stale version",
        "rule-layout-safety-v802": "stale rule file path",
        "/path/to/gen-tgo-ppt-skill": "stale script placeholder",
        "python scripts/inspect_pptx_style.py": "relative inspect script path",
        "all eight styles": "stale visual style count",
        "所有独立规则都必须有独立规则子智能体": "over-strict subagent rule",
        "为本次已加载的每个 rule 文件分配不同规则子智能体": "over-strict workflow subagent rule",
        "不得让同一个子智能体代审多个 rule": "over-strict guardrail subagent rule",
    }
    for path, text in texts.items():
        for needle, reason in forbidden.items():
            if needle in text:
                raise AssertionError(f"{reason}: {path}")


def check_manifest_paths() -> None:
    manifest = json.loads((ROOT / "references" / "template-manifest.json").read_text(encoding="utf-8"))
    if manifest.get("version") != EXPECTED_VERSION:
        raise AssertionError("template-manifest.json version is not V1")
    paths: set[str] = set()

    def walk(value: object) -> None:
        if isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, str) and value.startswith(("assets/", "references/", "scripts/")):
            paths.add(value)

    walk(manifest)
    missing = sorted(path for path in paths if not (ROOT / path).exists())
    if missing:
        raise AssertionError(f"Missing manifest paths: {missing}")


def check_scripts_compile_and_help() -> None:
    scripts = sorted(path for path in SCRIPTS.glob("*.py"))
    run([sys.executable, "-m", "py_compile", *(str(path) for path in scripts)])
    for cache_dir in ROOT.rglob("__pycache__"):
        shutil.rmtree(cache_dir)
    for script in scripts:
        if script.name == "run_v1_skill_checks.py":
            continue
        result = run([sys.executable, str(script), "--help"])
        if "usage:" not in result.stdout.lower():
            raise AssertionError(f"--help missing usage for {script.name}")


def check_generation_log_template() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        result = run([sys.executable, str(SCRIPTS / "create_generation_log.py"), "--title", "测试"], cwd=Path(tmp))
        log_path = Path(result.stdout.strip())
        text = log_path.read_text(encoding="utf-8")
        if "Skill 版本：V1" not in text or "排版安全版本：V1" not in text:
            raise AssertionError("generation log version mismatch")
        if "## 待处理问题\n\n- 无。" in text:
            raise AssertionError("generation log must not default unresolved issues to none")


def check_html_checker() -> None:
    good = """<!doctype html>
<html><head><style>
.slide { aspect-ratio: 16 / 9; width: 1600px; height: 900px; }
@media print { .slide { page-break-after: always; } }
</style></head><body>
<section class="slide"><h1>标题</h1></section>
<section class="slide"><h1>嘉宾介绍</h1></section>
<section class="slide"><h1>目录</h1><p>一、背景</p></section>
<section class="slide"><h1>感谢聆听</h1></section>
</body></html>"""
    bad = """<!doctype html><html><body>
<section class="slide"><p>""" + ("长文本" * 700) + """</p><p>MANDATORY PAGE</p></section>
</body></html>"""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        good_path = tmp_path / "good.html"
        bad_path = tmp_path / "bad.html"
        good_path.write_text(good, encoding="utf-8")
        bad_path.write_text(bad, encoding="utf-8")
        good_result = run([sys.executable, str(SCRIPTS / "check_html_layout.py"), str(good_path), "--json"])
        if json.loads(good_result.stdout)[0]["status"] != "PASS":
            raise AssertionError(f"good HTML fixture did not pass: {good_result.stdout}")
        bad_result = run([sys.executable, str(SCRIPTS / "check_html_layout.py"), str(bad_path), "--json"], expect=None)
        if bad_result.returncode == 0:
            raise AssertionError("bad HTML fixture unexpectedly passed")
        if json.loads(bad_result.stdout)[0]["status"] != "FAIL":
            raise AssertionError(f"bad HTML fixture did not fail: {bad_result.stdout}")


def check_scan_task_context_noise() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "Design.md").write_text("# Design\n", encoding="utf-8")
        (root / "Content.md").write_text("# Content\n", encoding="utf-8")
        (root / "gen-tgo-ppt-生成日志-20260709-010101.md").write_text("# Log\n", encoding="utf-8")
        (root / "gen-tgo-ppt-SSOT-20260709-010101.md").write_text("# SSOT\n", encoding="utf-8")
        (root / "source.md").write_text("# Source\n", encoding="utf-8")
        (root / "tgo-gtlc-style-branches-contact-sheet.png").write_bytes(b"not really an image")
        (root / "brand-logo.png").write_bytes(b"not really an image")
        result = run([sys.executable, str(SCRIPTS / "scan_task_context.py"), str(root), "--recent-limit", "20"])
        data = json.loads(result.stdout)
        source_names = {item["name"] for item in data["categories"]["source_candidate"]["recent"]}
        if source_names != {"source.md"}:
            raise AssertionError(f"source_candidate noise: {source_names}")
        logo_names = {item["name"] for item in data["categories"]["logo_candidate"]["recent"]}
        if logo_names != {"brand-logo.png"}:
            raise AssertionError(f"logo_candidate noise: {logo_names}")


def check_packaging() -> None:
    git_dirs = [path for path in ROOT.rglob(".git") if path.is_dir()]
    nested_git_dirs = [path for path in git_dirs if path.parent != ROOT]
    if nested_git_dirs:
        raise AssertionError(f"nested .git directories must not be bundled inside the skill: {nested_git_dirs}")
    if list(ROOT.rglob("__pycache__")):
        raise AssertionError("__pycache__ directories must not be bundled inside the skill")
    readme = ROOT / "README.md"
    if not readme.exists():
        raise AssertionError("README.md must document how to add new templates")
    text = readme.read_text(encoding="utf-8")
    required = ["如何增加新模板", "方式 A：在 Codex 中加入", "方式 B：直接放入文件夹", "run_v1_skill_checks.py"]
    missing = [item for item in required if item not in text]
    if missing:
        raise AssertionError(f"README.md missing required template instructions: {missing}")


def main() -> None:
    checks = [
        check_frontmatter,
        check_no_stale_text,
        check_manifest_paths,
        check_scripts_compile_and_help,
        check_generation_log_template,
        check_html_checker,
        check_scan_task_context_noise,
        check_packaging,
    ]
    results = []
    for check in checks:
        check()
        results.append({"check": check.__name__, "status": "PASS"})
    print(json.dumps({"status": "PASS", "checks": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
