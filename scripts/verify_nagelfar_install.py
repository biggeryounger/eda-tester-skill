#!/usr/bin/env python3
"""Verify the real Nagelfar installation against the Innovus fixtures."""

from __future__ import annotations

import sys
from pathlib import Path

import nagelfar_adapter


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "nagelfar"


def main() -> int:
    valid = nagelfar_adapter.run_nagelfar(FIXTURES / "valid_add_net.tcl")
    invalid = nagelfar_adapter.run_nagelfar(FIXTURES / "invalid_add_net_option.tcl")
    checks = (
        (valid.status == "PASS", f"valid fixture expected PASS, got {valid.status}"),
        (valid.engine_version == nagelfar_adapter.NAGELFAR_VERSION, f"expected Nagelfar {nagelfar_adapter.NAGELFAR_VERSION}, got {valid.engine_version}"),
        (invalid.status == "FAIL", f"invalid fixture expected FAIL, got {invalid.status}"),
        (any(item.rule_id == "NAGELFAR-SYNTAX" and item.line == 3 for item in invalid.diagnostics), "invalid fixture did not produce the expected line-3 syntax diagnostic"),
    )
    failures = [message for passed, message in checks if not passed]
    if failures:
        for message in failures:
            print(f"FAIL: {message}", file=sys.stderr)
        return 1
    print(f"PASS: Nagelfar {valid.engine_version} accepted the valid fixture and rejected the invalid fixture.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
