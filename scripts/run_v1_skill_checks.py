#!/usr/bin/env python3
"""Compatibility entrypoint for the gen-tgo-ppt-skill V1.2 core harness."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


CURRENT_HARNESS = Path(__file__).with_name("run_v11_skill_checks.py")
ENTRYPOINT_ENV = "GEN_TGO_PPT_HARNESS_ENTRYPOINT"
MINIMUM_PYTHON_VERSION = (3, 10)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the V1.2 core maintenance harness through the legacy V1 entrypoint.",
        epilog="This wrapper delegates once to run_v11_skill_checks.py and preserves its exit code.",
    )
    parser.add_argument(
        "--temp-root",
        type=Path,
        default=None,
        help="Forward an existing writable fixture workspace root to the V1.2 core harness.",
    )
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
    env = os.environ.copy()
    env[ENTRYPOINT_ENV] = Path(__file__).name
    command = [sys.executable, "-B", str(CURRENT_HARNESS)]
    if args.temp_root is not None:
        command.extend(["--temp-root", str(args.temp_root)])
    result = subprocess.run(command, env=env)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
