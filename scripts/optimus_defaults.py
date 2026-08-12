#!/usr/bin/env python3
"""Resolve an Optimus initialization template without inventing design inputs."""

from __future__ import annotations

import argparse
import json
from typing import Mapping, Optional


EXAMPLE_PROFILE = {
    "optimus_version": "21.1",
    "lef_path": "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library/sec28n_12t25od33_1p8m_7ic_1tmc_alpa1_WITH_NDR.lef $env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library/sc28nhkcp_hsc30p140_rvt_ant.lef",
    "netlist_path": "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/Itools21.1_lfp_util0.65/riscv_core/floorplan.v.gz",
    "top_cell": "riscv_core",
    "power_net": "VDD",
    "ground_net": "VSS",
    "mmmc_path": "./tcl/optimus/mmmc.tcl",
}

TEMPLATE_DEFAULTS = {
    "optimus_version": "21.1",
    "power_net": "VDD",
    "ground_net": "VSS",
    "mmmc_path": "./tcl/optimus/mmmc.tcl",
}
DESIGN_INPUT_FIELDS = ("lef_path", "netlist_path", "top_cell")
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
