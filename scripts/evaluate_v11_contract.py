#!/usr/bin/env python3
"""Evaluate V1.1 routing observations against a sealed gold corpus.

This evaluator is deliberately model-agnostic: it validates already-frozen
observations and never presents fixture results as Agent-behavior evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


EVALUATOR_VERSION = "V1.1"
SCHEMA_VERSION = "gen-tgo-ppt-routing-eval-v1.1"
EXIT_CODES = {"PASS": 0, "FAIL": 1, "INVALID": 2, "INSUFFICIENT": 3}
SPLITS = {"regression", "holdout"}
CASE_TYPES = {"create", "convert", "repair", "check_only", "no_trigger", "handoff"}
ROUTES = {"invoke", "no_trigger", "handoff"}
INVOKE_MODES = {"create", "convert", "repair", "check_only"}
EVIDENCE_LEVELS = {"structural_fixture", "observed_model_behavior"}
METRIC_NAMES = {
    "precision",
    "recall",
    "mode_accuracy",
    "specificity",
    "handoff_accuracy",
}
REQUIRED_THRESHOLDS = {
    "regression": {
        "precision": 1.0,
        "recall": 1.0,
        "mode_accuracy": 1.0,
        "specificity": 1.0,
        "handoff_accuracy": 1.0,
    },
    "holdout": {
        "precision": 0.9,
        "recall": 0.9,
        "mode_accuracy": 0.9,
        "specificity": 1.0,
        "handoff_accuracy": 1.0,
    },
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class JsonArgumentParser(argparse.ArgumentParser):
    """Keep invalid CLI invocations on the documented JSON/exit-code contract."""

    def error(self, message: str) -> None:
        emit_report(
            {
                "schema_version": SCHEMA_VERSION,
                "evaluator_version": EVALUATOR_VERSION,
                "status": "INVALID",
                "exit_code": EXIT_CODES["INVALID"],
                "evidence_classification": "invalid",
                "validation_errors": [f"E_CLI_INVALID: {message}"],
            }
        )
        raise SystemExit(EXIT_CODES["INVALID"])


def emit_report(report: dict[str, Any]) -> None:
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


def load_json(path: Path, label: str, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"E_FILE_MISSING: {label} file does not exist: {path}")
    except (OSError, UnicodeError) as exc:
        errors.append(f"E_FILE_READ: cannot read {label} file {path}: {exc}")
    except json.JSONDecodeError as exc:
        errors.append(
            f"E_JSON_INVALID: {label} file {path} is not valid JSON "
            f"(line {exc.lineno}, column {exc.colno})"
        )
    return None


def prompt_digest(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate_corpus_document(
    document: Any,
    *,
    label: str,
    expected_split: str | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return [], [f"E_CORPUS_SCHEMA: {label} root must be an object"]

    if document.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"E_CORPUS_SCHEMA_VERSION: {label} schema_version must be {SCHEMA_VERSION!r}"
        )
    if document.get("corpus_version") != EVALUATOR_VERSION:
        errors.append(
            f"E_CORPUS_VERSION: {label} corpus_version must be {EVALUATOR_VERSION!r}"
        )

    split = document.get("split")
    if split not in SPLITS:
        errors.append(f"E_SPLIT_INVALID: {label} split must be one of {sorted(SPLITS)}")
    if expected_split is not None and split != expected_split:
        errors.append(
            f"E_SPLIT_MISMATCH: {label} split {split!r} does not match {expected_split!r}"
        )

    thresholds = document.get("thresholds")
    if not isinstance(thresholds, dict):
        errors.append(f"E_THRESHOLDS_MISSING: {label} thresholds must be an object")
    else:
        missing_metrics = METRIC_NAMES - set(thresholds)
        unknown_metrics = set(thresholds) - METRIC_NAMES
        if missing_metrics:
            errors.append(
                f"E_THRESHOLD_MISSING: {label} missing thresholds: {sorted(missing_metrics)}"
            )
        if unknown_metrics:
            errors.append(
                f"E_THRESHOLD_UNKNOWN: {label} has unknown thresholds: {sorted(unknown_metrics)}"
            )
        for metric, threshold in thresholds.items():
            if not is_number(threshold) or not 0.0 <= float(threshold) <= 1.0:
                errors.append(
                    f"E_THRESHOLD_INVALID: {label} threshold {metric!r} must be in [0, 1]"
                )
        if split in REQUIRED_THRESHOLDS:
            for metric, required in REQUIRED_THRESHOLDS[split].items():
                actual = thresholds.get(metric)
                if is_number(actual) and float(actual) != required:
                    errors.append(
                        f"E_THRESHOLD_CONTRACT: {label} {split} threshold {metric!r} "
                        f"must be {required}, got {actual}"
                    )

    cases = document.get("cases")
    if not isinstance(cases, list):
        return [], errors + [f"E_CASES_SCHEMA: {label} cases must be an array"]
    if len(cases) != 6:
        errors.append(f"E_CASE_COUNT: {label} must contain exactly 6 cases, got {len(cases)}")

    seen_ids: set[str] = set()
    seen_hashes: set[str] = set()
    case_type_counts: Counter[str] = Counter()
    valid_cases: list[dict[str, Any]] = []

    for index, case in enumerate(cases):
        location = f"{label}.cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"E_CASE_SCHEMA: {location} must be an object")
            continue

        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"E_CASE_ID: {location}.case_id must be a non-empty string")
        elif case_id in seen_ids:
            errors.append(f"E_CASE_DUPLICATE: duplicate case_id {case_id!r} in {label}")
        else:
            seen_ids.add(case_id)

        case_split = case.get("split")
        if case_split != split:
            errors.append(
                f"E_CASE_SPLIT: {location}.split {case_split!r} does not match corpus split {split!r}"
            )

        case_type = case.get("case_type")
        if case_type not in CASE_TYPES:
            errors.append(
                f"E_CASE_TYPE: {location}.case_type must be one of {sorted(CASE_TYPES)}"
            )
        else:
            case_type_counts[case_type] += 1

        prompt = case.get("prompt")
        digest = case.get("prompt_sha256")
        if not isinstance(prompt, str) or not prompt:
            errors.append(f"E_PROMPT_EMPTY: {location}.prompt must be a non-empty string")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            errors.append(f"E_PROMPT_HASH_FORMAT: {location}.prompt_sha256 must be lowercase SHA-256")
        elif isinstance(prompt, str):
            computed = prompt_digest(prompt)
            if digest != computed:
                errors.append(
                    f"E_PROMPT_HASH_MISMATCH: {case_id!r} declares {digest}, computed {computed}"
                )
            if digest in seen_hashes:
                errors.append(f"E_PROMPT_HASH_DUPLICATE: duplicate prompt hash {digest} in {label}")
            else:
                seen_hashes.add(digest)

        attachments = case.get("attachments")
        if not isinstance(attachments, list):
            errors.append(f"E_ATTACHMENTS_SCHEMA: {location}.attachments must be an array")
        elif any(not isinstance(item, dict) for item in attachments):
            errors.append(f"E_ATTACHMENTS_SCHEMA: every attachment in {location} must be an object")

        route = case.get("expected_route")
        mode = case.get("expected_mode")
        handoff = case.get("expected_handoff")
        if route not in ROUTES:
            errors.append(f"E_GOLD_ROUTE: {location}.expected_route must be one of {sorted(ROUTES)}")
        if route == "invoke":
            if mode not in INVOKE_MODES:
                errors.append(
                    f"E_GOLD_MODE: invoke case {case_id!r} needs one of {sorted(INVOKE_MODES)}"
                )
            if handoff is not None:
                errors.append(f"E_GOLD_HANDOFF: invoke case {case_id!r} must use null expected_handoff")
        elif route in {"no_trigger", "handoff"} and mode is not None:
            errors.append(f"E_GOLD_MODE: {route} case {case_id!r} must use null expected_mode")

        if route == "handoff":
            if not isinstance(handoff, dict):
                errors.append(f"E_GOLD_HANDOFF: handoff case {case_id!r} needs an object contract")
            else:
                targets = handoff.get("targets")
                reason_contains = handoff.get("reason_contains")
                if not isinstance(targets, list) or not targets or any(
                    not isinstance(item, str) or not item for item in targets
                ):
                    errors.append(
                        f"E_GOLD_HANDOFF_TARGET: handoff case {case_id!r} needs non-empty targets"
                    )
                if not isinstance(reason_contains, list) or not reason_contains or any(
                    not isinstance(item, str) or not item for item in reason_contains
                ):
                    errors.append(
                        f"E_GOLD_HANDOFF_REASON: handoff case {case_id!r} needs reason_contains"
                    )
        elif handoff is not None:
            errors.append(f"E_GOLD_HANDOFF: non-handoff case {case_id!r} must use null expected_handoff")

        required_route = "invoke" if case_type in INVOKE_MODES else case_type
        required_mode = case_type if case_type in INVOKE_MODES else None
        if case_type in CASE_TYPES and route != required_route:
            errors.append(
                f"E_CASE_ROUTE_CONTRACT: {case_id!r} case_type {case_type!r} "
                f"requires route {required_route!r}"
            )
        if case_type in CASE_TYPES and mode != required_mode:
            errors.append(
                f"E_CASE_MODE_CONTRACT: {case_id!r} case_type {case_type!r} "
                f"requires mode {required_mode!r}"
            )

        provenance = case.get("provenance")
        if not isinstance(provenance, dict):
            errors.append(f"E_PROVENANCE: {location}.provenance must be an object")
        elif split == "holdout" and provenance.get("sealed") is not True:
            errors.append(f"E_HOLDOUT_UNSEALED: holdout case {case_id!r} must declare sealed=true")

        tags = case.get("tags")
        if not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
            errors.append(f"E_TAGS_SCHEMA: {location}.tags must be an array of strings")

        valid_cases.append(case)

    if set(case_type_counts) != CASE_TYPES or any(count != 1 for count in case_type_counts.values()):
        errors.append(
            "E_CASE_COVERAGE: corpus must contain exactly one case for each of "
            + ", ".join(sorted(CASE_TYPES))
        )

    return valid_cases, errors


def validate_counterpart(
    corpus_path: Path,
    corpus: dict[str, Any],
    cases: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    counterpart_name = corpus.get("counterpart_corpus")
    if not isinstance(counterpart_name, str) or not counterpart_name:
        return ["E_COUNTERPART_MISSING: corpus must name counterpart_corpus"]
    if Path(counterpart_name).name != counterpart_name:
        return ["E_COUNTERPART_PATH: counterpart_corpus must be a sibling filename"]

    counterpart_path = corpus_path.parent / counterpart_name
    counterpart = load_json(counterpart_path, "counterpart corpus", errors)
    if counterpart is None:
        return errors
    counterpart_cases, counterpart_errors = validate_corpus_document(
        counterpart,
        label="counterpart corpus",
    )
    errors.extend(counterpart_errors)

    split = corpus.get("split")
    counterpart_split = counterpart.get("split") if isinstance(counterpart, dict) else None
    if counterpart_split == split:
        errors.append(
            f"E_COUNTERPART_SPLIT: counterpart split must differ from {split!r}"
        )
    expected_counterpart_name = corpus.get("counterpart_corpus")
    backlink = counterpart.get("counterpart_corpus") if isinstance(counterpart, dict) else None
    if backlink != corpus_path.name:
        errors.append(
            f"E_COUNTERPART_BACKLINK: {expected_counterpart_name!r} must reference {corpus_path.name!r}"
        )

    case_ids = {case.get("case_id") for case in cases}
    other_ids = {case.get("case_id") for case in counterpart_cases}
    duplicate_ids = sorted(case_ids & other_ids)
    if duplicate_ids:
        errors.append(f"E_CROSS_SPLIT_CASE_ID: shared case IDs: {duplicate_ids}")

    hashes = {case.get("prompt_sha256") for case in cases}
    other_hashes = {case.get("prompt_sha256") for case in counterpart_cases}
    duplicate_hashes = sorted(hashes & other_hashes)
    if duplicate_hashes:
        errors.append(f"E_CROSS_SPLIT_PROMPT: shared prompt hashes: {duplicate_hashes}")
    return errors


def forbidden_observation_paths(value: Any, path: str = "observations") -> list[str]:
    forbidden: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower()
            child_path = f"{path}.{key}"
            if normalized == "gold" or normalized.startswith("expected") or "gold_" in normalized:
                forbidden.append(child_path)
            forbidden.extend(forbidden_observation_paths(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            forbidden.extend(forbidden_observation_paths(child, f"{path}[{index}]"))
    return forbidden


def validate_observations(
    document: Any,
    *,
    split: str,
    cases_by_id: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], str | None, list[str]]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return [], None, ["E_OBSERVATION_SCHEMA: observations root must be an object"]

    if document.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"E_OBSERVATION_SCHEMA_VERSION: schema_version must be {SCHEMA_VERSION!r}"
        )
    observations_version = document.get("observations_version")
    if not isinstance(observations_version, str) or not observations_version.startswith("V1.1"):
        errors.append(
            "E_OBSERVATION_VERSION: observations_version must be a V1.1 identifier"
        )
    if document.get("split") != split:
        errors.append(
            f"E_OBSERVATION_SPLIT: top-level split {document.get('split')!r} does not match {split!r}"
        )
    evidence_level = document.get("evidence_level")
    if evidence_level not in EVIDENCE_LEVELS:
        errors.append(
            f"E_EVIDENCE_LEVEL: evidence_level must be one of {sorted(EVIDENCE_LEVELS)}"
        )

    forbidden = forbidden_observation_paths(document)
    if forbidden:
        errors.append(
            "E_GOLD_LEAKAGE: observations contain forbidden expected/gold fields at "
            + ", ".join(forbidden)
        )

    records = document.get("observations")
    if not isinstance(records, list):
        return [], evidence_level, errors + ["E_OBSERVATIONS_SCHEMA: observations must be an array"]

    seen_run_ids: set[str] = set()
    seen_pairs: set[tuple[str, str]] = set()
    seen_agent_run_ids: set[str] = set()
    seen_evidence_ids: set[str] = set()
    valid_records: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        location = f"observations[{index}]"
        if not isinstance(record, dict):
            errors.append(f"E_OBSERVATION_RECORD: {location} must be an object")
            continue

        case_id = record.get("case_id")
        if not isinstance(case_id, str) or case_id not in cases_by_id:
            errors.append(f"E_OBSERVATION_CASE: {location}.case_id {case_id!r} is not in corpus")
            continue
        if record.get("split") != split:
            errors.append(
                f"E_OBSERVATION_SPLIT: {location}.split {record.get('split')!r} does not match {split!r}"
            )
        if record.get("prompt_sha256") != cases_by_id[case_id].get("prompt_sha256"):
            errors.append(f"E_OBSERVATION_HASH: {location} prompt hash does not match case {case_id!r}")

        record_level = record.get("evidence_level")
        if record_level != evidence_level:
            errors.append(
                f"E_EVIDENCE_LEVEL: {location}.evidence_level {record_level!r} "
                f"does not match top-level {evidence_level!r}"
            )

        run_id = record.get("run_id")
        if not isinstance(run_id, str) or not run_id:
            errors.append(f"E_RUN_ID: {location}.run_id must be a non-empty string")
            run_id = f"<invalid-{index}>"
        if run_id in seen_run_ids:
            errors.append(f"E_RUN_DUPLICATE: duplicate run_id {run_id!r}")
        else:
            seen_run_ids.add(run_id)
        pair = (case_id, run_id)
        if pair in seen_pairs:
            errors.append(f"E_OBSERVATION_DUPLICATE: duplicate case/run pair {pair!r}")
        else:
            seen_pairs.add(pair)

        if evidence_level == "observed_model_behavior":
            for required_field in ("agent_run_id", "evidence_id", "observed_at"):
                if not isinstance(record.get(required_field), str) or not record.get(required_field):
                    errors.append(
                        f"E_OBSERVED_METADATA: {location}.{required_field} is required for observed behavior"
                    )
            agent_run_id = record.get("agent_run_id")
            if isinstance(agent_run_id, str) and agent_run_id:
                if agent_run_id in seen_agent_run_ids:
                    errors.append(
                        f"E_AGENT_RUN_DUPLICATE: observed Agent run {agent_run_id!r} is not independent"
                    )
                else:
                    seen_agent_run_ids.add(agent_run_id)
            evidence_id = record.get("evidence_id")
            if isinstance(evidence_id, str) and evidence_id:
                if evidence_id in seen_evidence_ids:
                    errors.append(f"E_EVIDENCE_DUPLICATE: duplicate evidence_id {evidence_id!r}")
                else:
                    seen_evidence_ids.add(evidence_id)

        status = record.get("status")
        if status not in {"ok", "error"}:
            errors.append(f"E_OBSERVATION_STATUS: {location}.status must be 'ok' or 'error'")
        elif status == "error":
            if not isinstance(record.get("error_code"), str) or not record.get("error_code"):
                errors.append(f"E_OBSERVATION_ERROR: {location}.error_code is required for error status")
        else:
            route = record.get("predicted_route")
            mode = record.get("predicted_mode")
            handoff = record.get("predicted_handoff")
            if route not in ROUTES:
                errors.append(
                    f"E_PREDICTED_ROUTE: {location}.predicted_route must be one of {sorted(ROUTES)}"
                )
            if route == "invoke":
                if mode not in INVOKE_MODES:
                    errors.append(
                        f"E_PREDICTED_MODE: invoke observation {run_id!r} needs one of {sorted(INVOKE_MODES)}"
                    )
                if handoff is not None:
                    errors.append(
                        f"E_PREDICTED_HANDOFF: invoke observation {run_id!r} must use null predicted_handoff"
                    )
            elif route in {"no_trigger", "handoff"} and mode is not None:
                errors.append(
                    f"E_PREDICTED_MODE: {route} observation {run_id!r} must use null predicted_mode"
                )
            if route == "handoff":
                if not isinstance(handoff, dict):
                    errors.append(
                        f"E_PREDICTED_HANDOFF: handoff observation {run_id!r} needs an object"
                    )
                elif not isinstance(handoff.get("target"), str) or not isinstance(
                    handoff.get("reason"), str
                ):
                    errors.append(
                        f"E_PREDICTED_HANDOFF: handoff observation {run_id!r} needs target and reason"
                    )
            elif handoff is not None:
                errors.append(
                    f"E_PREDICTED_HANDOFF: non-handoff observation {run_id!r} must use null predicted_handoff"
                )

        valid_records.append(record)
    return valid_records, evidence_level, errors


def handoff_matches(case: dict[str, Any], observation: dict[str, Any]) -> bool:
    if observation.get("predicted_route") != "handoff":
        return False
    contract = case.get("expected_handoff") or {}
    predicted = observation.get("predicted_handoff") or {}
    target = str(predicted.get("target", "")).casefold()
    allowed_targets = {str(item).casefold() for item in contract.get("targets", [])}
    if target not in allowed_targets:
        return False
    reason = str(predicted.get("reason", "")).casefold()
    return all(str(token).casefold() in reason for token in contract.get("reason_contains", []))


def metric_record(
    numerator: int,
    denominator: int,
    threshold: float,
) -> dict[str, Any]:
    value = numerator / denominator if denominator else None
    return {
        "numerator": numerator,
        "denominator": denominator,
        "value": value,
        "threshold": threshold,
        "passed": None if value is None else value >= threshold,
    }


def evaluate(
    *,
    corpus_path: Path,
    observations_path: Path,
    selected_case_ids: list[str] | None,
    min_runs: int,
) -> tuple[dict[str, Any], int]:
    validation_errors: list[str] = []
    corpus = load_json(corpus_path, "corpus", validation_errors)
    observations_document = load_json(observations_path, "observations", validation_errors)

    base_report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "evaluator_version": EVALUATOR_VERSION,
        "corpus": str(corpus_path),
        "observations": str(observations_path),
        "minimum_runs_per_case": min_runs,
    }
    if min_runs < 1:
        validation_errors.append("E_MIN_RUNS: --min-runs must be at least 1")
    if corpus is None or observations_document is None:
        report = {
            **base_report,
            "status": "INVALID",
            "exit_code": EXIT_CODES["INVALID"],
            "evidence_classification": "invalid",
            "validation_errors": validation_errors,
        }
        return report, EXIT_CODES["INVALID"]

    cases, corpus_errors = validate_corpus_document(corpus, label="corpus")
    validation_errors.extend(corpus_errors)
    if isinstance(corpus, dict):
        validation_errors.extend(validate_counterpart(corpus_path, corpus, cases))

    cases_by_id = {
        case["case_id"]: case
        for case in cases
        if isinstance(case.get("case_id"), str) and case.get("case_id")
    }
    split = corpus.get("split") if isinstance(corpus, dict) else None
    records, evidence_level, observation_errors = validate_observations(
        observations_document,
        split=split,
        cases_by_id=cases_by_id,
    )
    validation_errors.extend(observation_errors)

    requested_ids = selected_case_ids or list(cases_by_id)
    duplicate_requested = sorted(
        case_id for case_id, count in Counter(requested_ids).items() if count > 1
    )
    if duplicate_requested:
        validation_errors.append(
            f"E_CASE_SELECTION_DUPLICATE: repeated --case-id values: {duplicate_requested}"
        )
    unknown_requested = sorted(set(requested_ids) - set(cases_by_id))
    if unknown_requested:
        validation_errors.append(
            f"E_CASE_SELECTION_UNKNOWN: unknown --case-id values: {unknown_requested}"
        )
    selected_ids = [case_id for case_id in requested_ids if case_id in cases_by_id]

    if validation_errors:
        report = {
            **base_report,
            "split": split,
            "evidence_level": evidence_level,
            "evidence_classification": "invalid",
            "selected_case_ids": selected_ids,
            "status": "INVALID",
            "exit_code": EXIT_CODES["INVALID"],
            "validation_errors": validation_errors,
        }
        return report, EXIT_CODES["INVALID"]

    selected_set = set(selected_ids)
    selected_records = [record for record in records if record.get("case_id") in selected_set]
    ignored_records = len(records) - len(selected_records)
    records_by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in selected_records:
        records_by_case[record["case_id"]].append(record)

    insufficiency_reasons: list[str] = []
    missing_cases = [case_id for case_id in selected_ids if not records_by_case[case_id]]
    if missing_cases:
        insufficiency_reasons.append(
            f"E_OBSERVATION_MISSING: no observations for cases {sorted(missing_cases)}"
        )

    errored_records = [record for record in selected_records if record.get("status") == "error"]
    if errored_records:
        identities = [f"{item['case_id']}:{item['run_id']}" for item in errored_records]
        insufficiency_reasons.append(
            f"E_OBSERVATION_ERROR: errored observations are evidence gaps: {identities}"
        )

    successful_by_case = {
        case_id: [record for record in records_by_case[case_id] if record.get("status") == "ok"]
        for case_id in selected_ids
    }
    insufficient_run_cases = {
        case_id: len(successful_by_case[case_id])
        for case_id in selected_ids
        if len(successful_by_case[case_id]) < min_runs
    }
    if insufficient_run_cases:
        insufficiency_reasons.append(
            "E_MIN_RUNS_UNMET: successful observations below --min-runs: "
            + json.dumps(insufficient_run_cases, ensure_ascii=False, sort_keys=True)
        )

    tp = fp = tn = fn = 0
    mode_correct = mode_total = 0
    no_trigger_correct = no_trigger_total = 0
    handoff_correct = handoff_total = 0
    exact_correct = exact_total = 0
    for case_id in selected_ids:
        case = cases_by_id[case_id]
        expected_route = case["expected_route"]
        for observation in successful_by_case[case_id]:
            predicted_route = observation["predicted_route"]
            expected_positive = expected_route in {"invoke", "handoff"}
            predicted_positive = predicted_route in {"invoke", "handoff"}
            if expected_positive and predicted_positive:
                tp += 1
            elif not expected_positive and predicted_positive:
                fp += 1
            elif not expected_positive and not predicted_positive:
                tn += 1
            else:
                fn += 1

            exact_total += 1
            exact = predicted_route == expected_route
            if expected_route == "invoke":
                mode_total += 1
                mode_match = observation.get("predicted_mode") == case.get("expected_mode")
                mode_correct += int(mode_match)
                exact = exact and mode_match
            elif expected_route == "no_trigger":
                no_trigger_total += 1
                no_trigger_match = predicted_route == "no_trigger"
                no_trigger_correct += int(no_trigger_match)
                exact = exact and no_trigger_match
            if expected_route == "handoff":
                handoff_total += 1
                handoff_match = handoff_matches(case, observation)
                handoff_correct += int(handoff_match)
                exact = exact and handoff_match
            exact_correct += int(exact)

    thresholds = corpus["thresholds"]
    metrics = {
        "precision": metric_record(tp, tp + fp, float(thresholds["precision"])),
        "recall": metric_record(tp, tp + fn, float(thresholds["recall"])),
        "mode_accuracy": metric_record(
            mode_correct,
            mode_total,
            float(thresholds["mode_accuracy"]),
        ),
        "specificity": metric_record(
            no_trigger_correct,
            no_trigger_total,
            float(thresholds["specificity"]),
        ),
        "handoff_accuracy": metric_record(
            handoff_correct,
            handoff_total,
            float(thresholds["handoff_accuracy"]),
        ),
        "exact_accuracy": {
            "numerator": exact_correct,
            "denominator": exact_total,
            "value": exact_correct / exact_total if exact_total else None,
            "threshold": None,
            "passed": None,
        },
    }
    zero_denominator_metrics = [
        name for name in METRIC_NAMES if metrics[name]["denominator"] == 0
    ]
    if zero_denominator_metrics:
        insufficiency_reasons.append(
            f"E_ZERO_DENOMINATOR: required metrics have zero denominators: {sorted(zero_denominator_metrics)}"
        )

    threshold_failures = sorted(
        name for name in METRIC_NAMES if metrics[name]["passed"] is False
    )
    stable_reasons: list[str] = []
    if len(selected_ids) < 20:
        stable_reasons.append("fewer than 20 selected cases")
    mode_case_counts = Counter(
        cases_by_id[case_id].get("expected_mode")
        for case_id in selected_ids
        if cases_by_id[case_id].get("expected_route") == "invoke"
    )
    underrepresented_modes = sorted(
        mode for mode in INVOKE_MODES if mode_case_counts.get(mode, 0) < 3
    )
    if underrepresented_modes:
        stable_reasons.append(
            f"fewer than 3 cases for modes: {underrepresented_modes}"
        )
    if any(len(successful_by_case[case_id]) < 3 for case_id in selected_ids):
        stable_reasons.append("fewer than 3 successful fresh runs for at least one selected case")
    if evidence_level != "observed_model_behavior":
        stable_reasons.append("evidence_level is not observed_model_behavior")

    if insufficiency_reasons:
        status = "INSUFFICIENT"
    elif threshold_failures:
        status = "FAIL"
    else:
        status = "PASS"

    if status == "INSUFFICIENT":
        evidence_classification = "insufficient"
    elif evidence_level == "structural_fixture":
        evidence_classification = "fixture_valid"
    else:
        evidence_classification = "observed"

    report = {
        **base_report,
        "split": split,
        "evidence_level": evidence_level,
        "evidence_classification": evidence_classification,
        "selected_case_ids": selected_ids,
        "status": status,
        "exit_code": EXIT_CODES[status],
        "validation_errors": [],
        "insufficiency_reasons": insufficiency_reasons,
        "threshold_failures": threshold_failures,
        "counts": {
            "cases_selected": len(selected_ids),
            "observations_selected": len(selected_records),
            "observations_ignored_by_case_filter": ignored_records,
            "successful_observations": sum(len(items) for items in successful_by_case.values()),
            "errored_observations": len(errored_records),
            "missing_cases": missing_cases,
            "successful_runs_by_case": {
                case_id: len(successful_by_case[case_id]) for case_id in selected_ids
            },
            "insufficient_run_cases": insufficient_run_cases,
        },
        "confusion_matrix": {"tp": tp, "fp": fp, "tn": tn, "fn": fn},
        "metric_definitions": {
            "precision": "active TP / all predicted active, where invoke and handoff are active",
            "recall": "active TP / all expected active, where invoke and handoff are active",
            "mode_accuracy": "exact mode among expected invoke observations",
            "specificity": "predicted no_trigger among expected no_trigger observations",
            "handoff_accuracy": "target and required reason tokens among expected handoff observations",
            "exact_accuracy": "exact route plus applicable mode or handoff contract",
        },
        "metrics": metrics,
        "sample_scope": {
            "stable_statistical_claim": not stable_reasons,
            "reasons": stable_reasons,
            "fixture_results_are_agent_behavior_evidence": False,
        },
    }
    return report, EXIT_CODES[status]


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(
        description=(
            "Validate frozen V1.1 routing observations against a gold corpus. "
            "Exit codes: PASS=0, FAIL=1, INVALID=2, INSUFFICIENT=3."
        )
    )
    parser.add_argument("corpus", type=Path, help="Gold corpus JSON path")
    parser.add_argument("observations", type=Path, help="Frozen observations JSON path")
    parser.add_argument(
        "--case-id",
        action="append",
        default=None,
        help="Evaluate one case ID; repeat to select multiple cases",
    )
    parser.add_argument(
        "--min-runs",
        type=int,
        default=1,
        help="Minimum successful independent observations required per selected case (default: 1)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report, exit_code = evaluate(
        corpus_path=args.corpus,
        observations_path=args.observations,
        selected_case_ids=args.case_id,
        min_runs=args.min_runs,
    )
    emit_report(report)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
