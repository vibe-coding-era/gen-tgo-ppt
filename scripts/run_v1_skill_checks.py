#!/usr/bin/env python3
"""Compatibility entrypoint for the gen-tgo-ppt-skill V1.1 harness."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


CURRENT_HARNESS = Path(__file__).with_name("run_v11_skill_checks.py")
ENTRYPOINT_ENV = "GEN_TGO_PPT_HARNESS_ENTRYPOINT"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the current V1.1 maintenance harness through the legacy V1 entrypoint.",
        epilog="This wrapper delegates once to run_v11_skill_checks.py and preserves its exit code.",
    )
    parser.add_argument(
        "--temp-root",
        type=Path,
        default=None,
        help="Forward an existing writable fixture workspace root to the V1.1 harness.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
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
