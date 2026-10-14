#!/usr/bin/env python3
"""Resolve an Optimus initialization template without inventing design inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Mapping, Optional


_CENTRAL_CONFIG = json.loads((Path(__file__).resolve().parents[1] / "assets/design-profiles.json").read_text(encoding="utf-8"))
_CENTRAL_EXAMPLE = _CENTRAL_CONFIG["profiles"]["repository_example"]
EXAMPLE_PROFILE = {
    "optimus_version": "21.1",
    "lef_path": " ".join(_CENTRAL_EXAMPLE["lef_files"]),
    "netlist_path": _CENTRAL_EXAMPLE["netlist_file"],
    "def_path": _CENTRAL_EXAMPLE["def_file"],
    "top_cell": _CENTRAL_EXAMPLE["top_cell"],
    "power_net": _CENTRAL_EXAMPLE["power_net"],
    "ground_net": _CENTRAL_EXAMPLE["ground_net"],
    "mmmc_path": "./tcl/optimus/mmmc.tcl",
}

TEMPLATE_DEFAULTS = {
    "optimus_version": "21.1",
    "power_net": "VDD",
    "ground_net": "VSS",
    "mmmc_path": "./tcl/optimus/mmmc.tcl",
}
DESIGN_INPUT_FIELDS = ("lef_path", "netlist_path", "def_path", "top_cell")
ALL_FIELDS = tuple(EXAMPLE_PROFILE)


def resolve_template(
    values: Mapping[str, Optional[str]],
    *,
    use_example_profile: bool = False,
) -> dict[str, object]:
    """Fill the template from user values; example design data is opt-in only."""
    resolved: dict[str, Optional[str]] = {
        key: (EXAMPLE_PROFILE[key] if use_example_profile else TEMPLATE_DEFAULTS.get(key))
        for key in ALL_FIELDS
    }
    for key in ALL_FIELDS:
        value = values.get(key)
        if value is not None and str(value).strip():
            resolved[key] = str(value).strip()
    missing = [key for key in DESIGN_INPUT_FIELDS if not resolved.get(key)]
    return {
        "values": resolved,
        "missing_required": missing,
        "example_profile_selected": use_example_profile,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ALL_FIELDS:
        parser.add_argument("--" + key.replace("_", "-"))
    parser.add_argument("--use-example-profile", action="store_true")
    args = parser.parse_args()
    result = resolve_template(vars(args), use_example_profile=args.use_example_profile)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["missing_required"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
