#!/usr/bin/env python3
"""Run V1.2 create-flow gates and delegate stable checks to the V1.2 core harness."""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, List, Optional


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
CORE_HARNESS = SCRIPTS / "run_v11_skill_checks.py"
LOG_SCRIPT = SCRIPTS / "create_generation_log.py"
EVAL_ROOT = ROOT / "references" / "evals"
V12_EVAL_SCHEMA = "gen-tgo-ppt-v1.2-create-gates-v1"
V12_GATE_ORDER = ("clarification", "brief_confirmation", "style_confirmation", "sample_confirmation", "full_generation")
STYLE_HEADINGS = ("## Content Expression", "### Image Treatment", "### Diagram Language", "### Data Expression", "### Avoid")
MINIMUM_PYTHON_VERSION = (3, 10)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AssertionError(f"Required JSON file is missing: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"Invalid JSON in {path.relative_to(ROOT)} at line {exc.lineno}, column {exc.colno}"
        ) from exc
    if not isinstance(value, dict):
        raise AssertionError(f"JSON root must be an object: {path.relative_to(ROOT)}")
    return value


def read_required(relative: str, markers: tuple[str, ...]) -> str:
    path = ROOT / relative
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise AssertionError(f"Required V1.2 contract file is missing: {relative}") from exc
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise AssertionError(f"V1.2 contract markers missing from {relative}: {missing}")
    return text


def check_v12_contract_files() -> dict[str, Any]:
    skill_text = read_required("SKILL.md", ("V1.2", "Brief", "风格", "样片"))
    intake_text = read_required(
        "references/rule-intake.md",
        ("最小澄清字段", "Brief", "风格", "图片"),
    )
    workflow_text = read_required(
        "references/workflow.md",
        ("澄清", "Brief", "风格", "样片", "完整生成"),
    )
    template_text = read_required(
        "references/rule-template-selection.md",
        ("预览", "风格", "确认", "智能推荐"),
    )
    expression_text = read_required(
        "references/rule-content-expression.md",
        ("表达类型", "视觉载体", "资产来源", "风格约束"),
    )
    ordered_steps = (
        "补足最小字段",
        "展示解析 Brief",
        "用户可选择具体项或“智能推荐”",
        "生成一页代表性",
        "等待用户确认样片后再完整生成",
    )
    workflow_positions = [workflow_text.index(marker) for marker in ordered_steps]
    if workflow_positions != sorted(workflow_positions):
        raise AssertionError("V1.2 workflow must order clarification -> Brief -> style -> sample -> full generation")
    if "不得静默" not in intake_text + workflow_text + template_text:
        raise AssertionError("V1.2 contracts must explicitly prohibit silent default style selection")
    if "确认" not in skill_text:
        raise AssertionError("SKILL.md must state the V1.2 confirmation contract")
    return {
        "required_contracts": 5,
        "gate_order": list(V12_GATE_ORDER),
        "content_expression_contract": "references/rule-content-expression.md",
    }


def check_visual_style_expression_contracts() -> dict[str, Any]:
    style_paths = sorted((ROOT / "references" / "design" / "visual-styles").glob("style-*/design.md"))
    if len(style_paths) != 9:
        raise AssertionError(f"V1.2 requires exactly nine visual-style design files, found {len(style_paths)}")
    missing_by_style: dict[str, list[str]] = {}
    for path in style_paths:
        text = path.read_text(encoding="utf-8")
        missing = [heading for heading in STYLE_HEADINGS if heading not in text]
        if missing:
            missing_by_style[path.parent.name] = missing
    if missing_by_style:
        raise AssertionError(f"V1.2 style content-expression sections are incomplete: {missing_by_style}")
    return {"style_count": len(style_paths), "required_headings": list(STYLE_HEADINGS)}


def check_v12_create_gate_fixtures() -> dict[str, Any]:
    expected_files = {
        "regression": EVAL_ROOT / "v12-create-gates-regression.json",
        "holdout": EVAL_ROOT / "v12-create-gates-holdout.json",
    }
    gate_coverage: set[str] = set()
    seen_case_ids: set[str] = set()
    cases_per_split: dict[str, int] = {}
    for split, path in expected_files.items():
        corpus = load_json(path)
        if corpus.get("schema_version") != V12_EVAL_SCHEMA or corpus.get("split") != split:
            raise AssertionError(f"V1.2 {split} create-gate fixture schema/split mismatch")
        if corpus.get("evidence_level") != "structural_fixture":
            raise AssertionError(f"V1.2 {split} fixture must be labeled structural_fixture")
        purpose = corpus.get("fixture_purpose")
        if not isinstance(purpose, str) or "not model-behavior evidence" not in purpose:
            raise AssertionError(f"V1.2 {split} fixture must deny model-behavior evidence")
        cases = corpus.get("cases")
        if not isinstance(cases, list) or not cases:
            raise AssertionError(f"V1.2 {split} fixture must contain create cases")
        cases_per_split[split] = len(cases)
        for case in cases:
            if not isinstance(case, dict):
                raise AssertionError(f"V1.2 {split} fixture cases must be objects")
            case_id = case.get("case_id")
            if not isinstance(case_id, str) or case_id in seen_case_ids:
                raise AssertionError("V1.2 create-gate case IDs must be unique")
            seen_case_ids.add(case_id)
            if case.get("case_type") != "create" or not isinstance(case.get("prompt"), str):
                raise AssertionError(f"V1.2 fixture case must be a create prompt: {case_id}")
            gate = case.get("expected_gate")
            if gate not in V12_GATE_ORDER:
                raise AssertionError(f"V1.2 fixture has unknown gate {gate!r}: {case_id}")
            gate_coverage.add(gate)
            forbidden = set(case.get("forbidden_actions", []))
            if gate != "full_generation" and "generate_full_deck" not in forbidden:
                raise AssertionError(f"V1.2 pre-generation gate must forbid full generation: {case_id}")
            if gate == "full_generation":
                if case.get("brief_confirmation") != "confirmed" or case.get("style_confirmation") != "confirmed":
                    raise AssertionError(f"V1.2 full-generation fixture lacks confirmed Brief/style: {case_id}")
                if case.get("sample_confirmation") not in {"confirmed", "explicit_skip_recorded"}:
                    raise AssertionError(f"V1.2 full-generation fixture lacks confirmed or explicitly skipped sample: {case_id}")
    if gate_coverage != set(V12_GATE_ORDER):
        raise AssertionError(f"V1.2 fixtures must cover every gate: {sorted(gate_coverage)}")
    return {
        "fixture_splits": sorted(expected_files),
        "cases_per_split": cases_per_split,
        "gate_coverage": list(V12_GATE_ORDER),
        "evidence_level": "structural_fixture",
    }


def check_generation_log_v12_fields() -> dict[str, Any]:
    source = LOG_SCRIPT.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(LOG_SCRIPT))
    compile(tree, str(LOG_SCRIPT), "exec")
    required_flags = {
        "--clarification-status",
        "--brief-confirmation",
        "--style-confirmation",
        "--sample-confirmation",
        "--asset-source-strategy",
        "--page-expression-plan",
    }
    missing_flags = [flag for flag in required_flags if flag not in source]
    if missing_flags:
        raise AssertionError(f"V1.2 generation-log arguments are missing: {missing_flags}")
    command = [
        sys.executable,
        "-B",
        str(LOG_SCRIPT),
        "--dry-run",
        "--mode",
        "create",
        "--source-authority",
        "current_turn",
        "--clarification-status",
        "confirmed",
        "--brief-confirmation",
        "confirmed",
        "--style-confirmation",
        "confirmed_style_4",
        "--sample-confirmation",
        "confirmed",
        "--asset-source-strategy",
        "approved_ai_visuals",
        "--page-expression-plan",
        "page-2:case/image/approved_ai_visuals/style-4",
    ]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(f"V1.2 generation-log dry-run failed: {result.stderr[-2000:]}")
    required_output = (
        "Skill 版本：V1.2",
        "## V1.2 必经确认门",
        "澄清状态：confirmed",
        "Brief 确认：confirmed",
        "风格确认：confirmed_style_4",
        "样片确认：confirmed",
        "资产来源策略：approved_ai_visuals",
        "页级视觉表达：page-2:case/image/approved_ai_visuals/style-4",
    )
    missing_output = [item for item in required_output if item not in result.stdout]
    if missing_output:
        raise AssertionError(f"V1.2 generation-log output is incomplete: {missing_output}")
    return {"generation_log_fields": len(required_flags), "dry_run_writes": 0}


def check_no_v1_callback() -> dict[str, Any]:
    if not CORE_HARNESS.is_file():
        raise AssertionError("V1.2 core harness is missing")
    if CORE_HARNESS.name != "run_v11_skill_checks.py":
        raise AssertionError("V1.2 current harness must delegate only to the V1.2 core harness")
    return {"core_harness": CORE_HARNESS.relative_to(ROOT).as_posix(), "legacy_callback": False}


def check_low_python_version_guards() -> dict[str, Any]:
    candidate = Path("/usr/local/bin/python3")
    if not candidate.is_file():
        return {"fixture_status": "SKIPPED", "reason": "no optional low-version Python candidate"}
    probe = subprocess.run(
        [str(candidate), "-c", "import sys; print(sys.version_info[0], sys.version_info[1])"],
        text=True,
        capture_output=True,
    )
    if probe.returncode != 0:
        raise AssertionError(f"Cannot probe optional Python candidate: {probe.stderr[-1000:]}")
    try:
        major, minor = (int(value) for value in probe.stdout.split())
    except ValueError as exc:
        raise AssertionError(f"Invalid optional Python version probe: {probe.stdout!r}") from exc
    if (major, minor) >= MINIMUM_PYTHON_VERSION:
        return {
            "fixture_status": "SKIPPED",
            "reason": "optional Python candidate meets the minimum version",
            "candidate_version": f"{major}.{minor}",
        }

    entrypoints = (
        ("v12", SCRIPTS / "run_v12_skill_checks.py", ["--compact"]),
        ("v11_core", CORE_HARNESS, ["--compact"]),
        ("v1_compatibility", SCRIPTS / "run_v1_skill_checks.py", []),
    )
    verified: list[str] = []
    for label, script, extra in entrypoints:
        result = subprocess.run([str(candidate), "-B", str(script), *extra], text=True, capture_output=True)
        if result.returncode != 3:
            raise AssertionError(f"{label} low-Python exit code must be 3, got {result.returncode}")
        if result.stderr or "Traceback" in result.stdout:
            raise AssertionError(f"{label} low-Python guard emitted stderr or a traceback")
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{label} low-Python guard did not emit JSON: {result.stdout!r}") from exc
        if payload.get("status") != "INSUFFICIENT" or payload.get("error_code") != "E_PYTHON_VERSION":
            raise AssertionError(f"{label} low-Python guard returned an unstable payload: {payload}")
        verified.append(label)
    return {
        "fixture_status": "EXECUTED",
        "candidate": str(candidate),
        "candidate_version": f"{major}.{minor}",
        "entrypoints": verified,
        "error_code": "E_PYTHON_VERSION",
    }


V12_CHECKS: list[tuple[str, Callable[[], dict[str, Any]]]] = [
    ("v12_contract_files", check_v12_contract_files),
    ("v12_visual_style_expression_contracts", check_visual_style_expression_contracts),
    ("v12_create_gate_fixtures", check_v12_create_gate_fixtures),
    ("v12_generation_log_fields", check_generation_log_v12_fields),
    ("v12_no_v1_callback", check_no_v1_callback),
    ("v12_low_python_version_guards", check_low_python_version_guards),
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run V1.2 create-flow gates plus the V1.2 core harness.")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON instead of indented JSON.")
    parser.add_argument("--temp-root", type=Path, default=None, help="Forward an existing writable temp root to the core harness.")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    if sys.version_info < MINIMUM_PYTHON_VERSION:
        payload = {
            "status": "INSUFFICIENT",
            "entrypoint": Path(__file__).name,
            "harness_version": "V1.2",
            "error_code": "E_PYTHON_VERSION",
            "error": (
                "gen-tgo-ppt V1.2 Harness requires Python >=3.10; "
                f"current={sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            ),
        }
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return 3
    args = build_parser().parse_args(argv)
    core_command = [sys.executable, "-B", str(CORE_HARNESS), "--compact"]
    if args.temp_root is not None:
        core_command.extend(["--temp-root", str(args.temp_root)])
    core_result = subprocess.run(core_command, text=True, capture_output=True)
    try:
        core_payload = json.loads(core_result.stdout)
    except json.JSONDecodeError:
        core_payload = {"status": "FAIL", "error": f"core harness did not emit JSON: {core_result.stdout[-2000:]}"}

    checks: list[dict[str, Any]] = []
    for name, check in V12_CHECKS:
        try:
            evidence = check()
        except Exception as exc:
            checks.append({"check": name, "status": "FAIL", "error": f"{type(exc).__name__}: {exc}"})
        else:
            checks.append({"check": name, "status": "PASS", "evidence": evidence})
    core_status = core_payload.get("status")
    if core_result.returncode != 0 or core_status != "PASS":
        checks.insert(0, {"check": "v12_core_harness", "status": "FAIL", "evidence": core_payload})
    else:
        checks.insert(0, {"check": "v12_core_harness", "status": "PASS", "evidence": core_payload})
    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    payload = {
        "status": status,
        "entrypoint": Path(__file__).name,
        "harness_version": "V1.2",
        "evidence_level": "structural_and_deterministic_fixture",
        "checks": checks,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=None if args.compact else 2, sort_keys=args.compact))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
