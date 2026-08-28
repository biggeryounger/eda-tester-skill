#!/usr/bin/env python3
"""Deterministic Layer 2B checks for EDA TCL case directories."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path


CASE_DIR = re.compile(r"^(pos|neg)[0-9]{3}_[a-z0-9][a-z0-9_]*$")
RUN_FILE = re.compile(r"^run_([0-9]+)\.tcl$")
CHECKPOINT = re.compile(r"(?m)^[ \t]*(pv_check_log|pv_check_golden|pv_check_qor)(?=\s|$)")
PV_SOURCE = re.compile(
    r"(?m)^[ \t]*source\s+(?:\{)?\$(?:::)?env\(PV_ROOT\)/(?:pv/)?scripts/pv\.tcl(?:\})?[ \t]*(?:#.*)?$"
)
ENV_VARIABLE = re.compile(
    r"(?<![A-Za-z0-9_])(?:\$(?:::)?env|(?:::)?env)\(\s*([^)\r\n]+?)\s*\)"
)
ALLOWED_ENV_VARIABLES = {"PV_ROOT", "PV_TOOL"}
DESIGN_ACTIVATION = re.compile(
    r"(?m)^[ \t]*(?:setup_design|init_design|read_db|restoreDesign|open_block|link_design)(?=\s|$)"
)
DESIGN_SOURCE = re.compile(r"(?m)^[ \t]*source\s+\S*design\.tcl[ \t]*(?:#.*)?$")
MMMC_SOURCE = re.compile(r"(?m)^[ \t]*source\s+\S*mmmc\.tcl[ \t]*(?:#.*)?$")
SETUP_MMMC = re.compile(r"(?m)^[ \t]*set_options\s+setup\.mmmc_file\s+(\S+)[ \t]*(?:#.*)?$")
INIT_MMMC = re.compile(r"(?m)^[ \t]*set\s+init_mmmc_file\s+(\S+)[ \t]*(?:#.*)?$")
SETUP_DESIGN = re.compile(r"(?m)^[ \t]*setup_design(?=\s|$)")
READ_DEF = re.compile(r"(?m)^[ \t]*read_def(?=\s|$)")
HELPER_INIT_COMMAND = re.compile(
    r"(?m)^[ \t]*(?:source\s+\S*pv\.tcl|set_options\b|setup_design\b|read_def\b)"
)
EXTERNAL_SETUP = re.compile(r"(?m)^[ \t]*source\s+\S*(?:case_setup\.tcl|nith)")
MACHINE_PATH = re.compile(r"(?m)(?:/Users/|/home/|[A-Za-z]:\\)")
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD)\b", re.I)
DESIGN_CATEGORY = re.compile(
    r"(?m)^[ \t]*set\s+[A-Za-z0-9_]*"
    r"(?:init_top|top_cell|verilog|netlist|lef|lib|timing|sdc|power_net|ground_net|def)[A-Za-z0-9_]*\b",
    re.I,
)
TCL_SET = re.compile(r"(?m)^[ \t]*set\s+([A-Za-z_][A-Za-z0-9_]*)\s+([^\r\n]+?)\s*(?:#.*)?$")
INPUT_OPTION = re.compile(
    r"(?m)^[ \t]*set_options\s+setup\.(lef_file|verilog|top_cell|power_net|ground_net)\s+(\S+)"
)
READ_DEF_INPUT = re.compile(r"(?m)^[ \t]*read_def\s+(\S+)")
NITH_INIT_BEGIN = "### NITH initialization, please do not change this section"
NITH_INIT_END = "### NITH initialization end"
NITH_INPUT = re.compile(r'nith\.input\[""\]\s*=\s*f?"tcl/\{nith\.PV_TOOL\}/run_([0-9]+)\.tcl"')
NITH_RUN_CALL = re.compile(r"nith_run\s*\(\s*\)")
NITH_DONE_CALL = re.compile(r"nith_done\s*\(\s*\)")
ALLOWED_TOOLS = ("optimus", "itools")
RUN_SUMMARY = re.compile(r"^\s*pv_rpt_checkpoints\s*(?:;\s*)?(?:#.*)?$")
RUN_EXIT = re.compile(r"^\s*exit\s*(?:;\s*)?(?:#.*)?$")


@dataclass(frozen=True)
class TclConventionDiagnostic:
    rule_id: str
    file: Path
    line: int | None
    message: str

    def to_dict(self) -> dict[str, object]:
        return {
            "layer": "L2B",
            "rule_id": self.rule_id,
            "severity": "error",
            "file": str(self.file),
            "line": self.line,
            "message": self.message,
        }


def _line(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def _commands(text: str) -> list[tuple[str, str, int, int]]:
    commands: list[tuple[str, str, int, int]] = []
    for match in CHECKPOINT.finditer(text):
        start = match.start()
        position = match.end()
        depth = 0
        quote = False
        escaped = False
        while position < len(text):
            char = text[position]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"' and depth == 0:
                quote = not quote
            elif not quote and char == "{":
                depth += 1
            elif not quote and char == "}":
                depth = max(0, depth - 1)
            elif char == "\n" and depth == 0 and not quote:
                break
            position += 1
        commands.append((match.group(1), text[match.end():position].strip(), start, position))
    return commands


def _words(value: str) -> list[str]:
    words: list[str] = []
    position = 0
    while position < len(value):
        while position < len(value) and value[position].isspace():
            position += 1
        if position >= len(value):
            break
        opener = value[position]
        if opener in {'{', '"'}:
            closer = '}' if opener == '{' else '"'
            depth = 1
            start = position
            position += 1
            while position < len(value) and depth:
                if opener == '{' and value[position] == '{':
                    depth += 1
                elif value[position] == closer:
                    depth -= 1
                position += 1
            words.append(value[start:position])
        else:
            start = position
            while position < len(value) and not value[position].isspace():
                position += 1
            words.append(value[start:position])
    return words


def _options(words: list[str], allowed: set[str]) -> tuple[dict[str, str], str | None]:
    options: dict[str, str] = {}
    position = 1
    while position < len(words):
        option = words[position]
        if option not in allowed:
            return options, f"unsupported option: {option}"
        if option in options:
            return options, f"duplicate option: {option}"
        if position + 1 >= len(words) or words[position + 1].startswith("-"):
            return options, f"option requires a value: {option}"
        options[option] = words[position + 1]
        position += 2
    return options, None


def _nonempty_word(value: str) -> bool:
    stripped = value.strip()
    return bool(stripped and stripped not in {"{}", '""'})


def _actual_path(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] in {'{', '"'} and stripped[-1] in {'}', '"'}:
        return stripped[1:-1].strip()
    return stripped


def _line_positions_containing(text: str, pattern: re.Pattern[str], value: str) -> list[int]:
    positions: list[int] = []
    for match in pattern.finditer(text):
        line_end = text.find("\n", match.start())
        line = text[match.start():line_end if line_end != -1 else len(text)]
        if value in line:
            positions.append(match.start())
    return positions


def _read(path: Path) -> str | None:
    if not path.is_file() or path.is_symlink():
        return None
    return path.read_text(encoding="utf-8")


def _design_init_block(text: str) -> str | None:
    begin = re.search(r"(?m)^\s*#\s*DESIGN_INIT_BEGIN\s*$", text)
    end = re.search(r"(?m)^\s*#\s*DESIGN_INIT_END\s*$", text)
    if begin and end and begin.end() < end.start():
        return text[begin.end():end.start()]
    return None


def _add(diagnostics: list[TclConventionDiagnostic], rule_id: str, path: Path, text: str, position: int, message: str) -> None:
    diagnostics.append(TclConventionDiagnostic(rule_id, path, _line(text, position) if text else None, message))


def _contiguous_from_one(indices: list[int]) -> bool:
    return bool(indices) and indices == list(range(1, len(indices) + 1))


def _input_category(variable: str) -> str | None:
    name = variable.lower()
    if "lef" in name:
        return "lef_file"
    if "verilog" in name or "netlist" in name:
        return "verilog"
    if "top_cell" in name or "init_top" in name or name in {"top", "top_name"}:
        return "top_cell"
    if "power_net" in name:
        return "power_net"
    if "ground_net" in name:
        return "ground_net"
    if name == "def" or name.startswith("def_") or name.endswith("_def") or "def_file" in name:
        return "def"
    return None


def _variable_reference(value: str) -> str | None:
    match = re.fullmatch(r"\$(?:\{([A-Za-z_][A-Za-z0-9_]*)\}|([A-Za-z_][A-Za-z0-9_]*))", value.strip())
    return (match.group(1) or match.group(2)) if match else None


def _validate_design_variable_reuse(
    design_text: str,
    run_text: str,
    run_path: Path,
    diagnostics: list[TclConventionDiagnostic],
) -> None:
    design_variables = {match.group(1) for match in TCL_SET.finditer(design_text)}
    variables_by_category: dict[str, set[str]] = {}
    for variable in design_variables:
        category = _input_category(variable)
        if category is not None:
            variables_by_category.setdefault(category, set()).add(variable)

    for match in TCL_SET.finditer(run_text):
        if match.group(1) in design_variables:
            _add(
                diagnostics,
                "TCL-DESIGN-002",
                run_path,
                run_text,
                match.start(),
                f"run_N.tcl must reuse ${match.group(1)} from design.tcl instead of redefining it",
            )

    uses: list[tuple[str, str, int]] = [
        (match.group(1), match.group(2), match.start()) for match in INPUT_OPTION.finditer(run_text)
    ]
    uses.extend(("def", match.group(1), match.start()) for match in READ_DEF_INPUT.finditer(run_text))
    for category, value, position in uses:
        candidates = variables_by_category.get(category, set())
        if candidates and _variable_reference(value) not in candidates:
            expected = ", ".join(f"${name}" for name in sorted(candidates))
            _add(
                diagnostics,
                "TCL-DESIGN-002",
                run_path,
                run_text,
                position,
                f"run_N.tcl must use design.tcl variable {expected} for {category}",
            )


def _validate_run_script(
    text: str,
    path: Path,
    polarity: str,
    case_files: list[Path],
    diagnostics: list[TclConventionDiagnostic],
) -> None:
    if EXTERNAL_SETUP.search(text):
        match = EXTERNAL_SETUP.search(text)
        _add(diagnostics, "TCL-RUNNER-002", path, text, match.start() if match else 0, "run script must source only in-tree design.tcl/mmmc.tcl")

    block = _design_init_block(text)
    if block is not None:
        design_src = DESIGN_SOURCE.search(block)
        mmmc_src = MMMC_SOURCE.search(block)
        tool = path.parent.name
        expected_design = re.compile(r"(?m)^[ \t]*source\s+(?:\{)?\./tcl/design\.tcl(?:\})?[ \t]*(?:#.*)?$")
        valid_design_src = expected_design.search(block)
        if design_src is not None and valid_design_src is None:
            diagnostics.append(TclConventionDiagnostic(
                "TCL-RUNNER-002",
                path,
                None,
                "run script executes from the case directory; use ./tcl/design.tcl",
            ))
        activation = DESIGN_ACTIVATION.search(block)
        if tool == "optimus":
            pv_source = PV_SOURCE.search(block)
            mmmc_option = SETUP_MMMC.search(block)
            setup_design = SETUP_DESIGN.search(block)
            read_def = READ_DEF.search(block)
            expected_mmmc_path = f"./tcl/{tool}/mmmc.tcl"
            ordered = bool(
                pv_source is not None
                and mmmc_src is None
                and mmmc_option is not None
                and mmmc_option.group(1) == expected_mmmc_path
                and activation is not None
                and mmmc_option.start() < activation.start()
                and valid_design_src is not None
                and pv_source.start() < valid_design_src.start() < mmmc_option.start()
                and (
                    setup_design is None
                    or (read_def is not None and setup_design.start() < read_def.start())
                )
            )
            message = (
                "Optimus DESIGN_INIT must source PV/design, set setup.mmmc_file without sourcing MMMC, "
                "run setup_design, then read_def"
            )
        elif tool == "itools":
            init_mmmc = INIT_MMMC.search(block)
            expected_mmmc_path = "./tcl/itools/mmmc.tcl"
            ordered = bool(
                valid_design_src is not None
                and mmmc_src is None
                and init_mmmc is not None
                and init_mmmc.group(1) == expected_mmmc_path
                and activation is not None
                and valid_design_src.start() < init_mmmc.start()
                and init_mmmc.start() < activation.start()
            )
            message = "iTools DESIGN_INIT must source ./tcl/design.tcl, set init_mmmc_file ./tcl/itools/mmmc.tcl without sourcing MMMC, then run init_design"
        else:
            ordered = bool(valid_design_src is not None and activation is not None and valid_design_src.start() < activation.start())
            message = f"DESIGN_INIT must source ./tcl/design.tcl before {tool} activation"
        if not ordered:
            diagnostics.append(TclConventionDiagnostic("TCL-RUN-001", path, None, message))

    action_positions = [m.start() for m in re.finditer(r"(?m)^\s*#\s*TEST_ACTION\s*$", text)]
    expects = list(re.finditer(r"(?m)^\s*#\s*EXPECT:\s*(PASS|FAIL)\s*$", text))
    expected = "PASS" if polarity == "pos" else "FAIL"
    markers_ok = (
        len(action_positions) == 1
        and len(expects) == 1
        and expects[0].start() < action_positions[0]
        and expects[0].group(1) == expected
    )
    if not markers_ok:
        diagnostics.append(TclConventionDiagnostic("TCL-SCRIPT-001", path, None, "each run_N.tcl needs exactly one EXPECT marker before exactly one TEST_ACTION marker"))

    commands = _commands(text)
    if commands:
        source = PV_SOURCE.search(text)
        if source is None or source.start() > commands[0][2]:
            _add(diagnostics, "TCL-CHECKPOINT-002", path, text, commands[0][2], "approved PV entry must be sourced before the first checkpoint")
    names: set[str] = set()
    for command, arguments, start, _end in commands:
        words = _words(arguments)
        line = _line(text, start)
        if command == "pv_check_log":
            options, error = _options(words, {"-name", "-filter", "-match", "-log_files"}) if words else ({}, "missing command block")
            block_ok = bool(words and words[0].startswith("{") and words[0] != "{}")
            if not error:
                empty_options = [option for option, value in options.items() if not _nonempty_word(value)]
                if empty_options:
                    error = f"option requires a non-empty value: {empty_options[0]}"
            name = options.get("-name")
            if name and name in names:
                error = f"duplicate checkpoint name: {name}"
            if name:
                names.add(name)
            if not block_ok or error or "===PV_MARKER" in text:
                diagnostics.append(TclConventionDiagnostic("TCL-CHECKPOINT-003", path, line, error or "pv_check_log requires a non-empty command block and valid options"))
        elif command == "pv_check_golden":
            options, error = _options(words, {"-golden", "-filter"}) if words else ({}, "missing output file")
            golden = options.get("-golden", "")
            invalid_mode = re.search(r"set\s+(?:::)?env\(PV_CHECK_MODE\)", text)
            golden_ok = not golden or re.match(r"^(?:\./)?golden/", _actual_path(golden)) is not None
            if not words or words[0].startswith("-") or error or not golden_ok or invalid_mode:
                diagnostics.append(TclConventionDiagnostic("TCL-CHECKPOINT-004", path, line, error or "pv_check_golden arguments or paths are invalid"))

            if words and not words[0].startswith("-"):
                actual = _actual_path(words[0])
                write_positions = _line_positions_containing(
                    text,
                    re.compile(r"(?m)(?:^|\{)\s*write_[A-Za-z0-9_]+(?=\s|$)"),
                    actual,
                )
                if write_positions:
                    producer_before = [position for position in write_positions if position < start]
                    producer_after = [position for position in write_positions if position > start]
                    delete_positions = _line_positions_containing(
                        text,
                        re.compile(r"(?m)^\s*file\s+delete(?:\s+-force)?(?=\s|$)"),
                        actual,
                    )
                    clean_before_write = bool(
                        producer_before
                        and any(position < max(producer_before) for position in delete_positions)
                    )
                    if producer_after or not producer_before or not clean_before_write:
                        diagnostics.append(TclConventionDiagnostic(
                            "TCL-CHECKPOINT-006",
                            path,
                            line,
                            "a same-run golden output must be deleted, generated, then compared in that order",
                        ))
        else:
            options, error = _options(words, {"-name", "-golden", "-tolerance", "-rel_tolerance", "-dir"}) if words else ({}, "missing command block")
            inner = words[0][1:-1].strip() if words and words[0].startswith("{") and words[0].endswith("}") else ""
            command_name = inner.split(None, 1)[0] if inner else ""
            numeric_ok = True
            for option in ("-tolerance", "-rel_tolerance"):
                if option in options:
                    try:
                        number = float(options[option])
                        numeric_ok = numeric_ok and math.isfinite(number) and number >= 0
                    except ValueError:
                        numeric_ok = False
            golden = options.get("-golden", "")
            output_dir = options.get("-dir", "")
            paths_ok = (not golden or golden.startswith("./golden/")) and (not output_dir or not Path(output_dir).is_absolute() and ".." not in Path(output_dir).parts)
            if error or command_name not in {"report_timing", "report_qor", "timeDesign"} or not numeric_ok or not paths_ok:
                diagnostics.append(TclConventionDiagnostic("TCL-CHECKPOINT-005", path, line, error or "pv_check_qor command, tolerance, or path is invalid"))

    action_position = action_positions[0] if len(action_positions) == 1 else None
    init_begins = list(re.finditer(r"(?m)^\s*#\s*DESIGN_INIT_BEGIN\s*$", text))
    init_ends = list(re.finditer(r"(?m)^\s*#\s*DESIGN_INIT_END\s*$", text))
    init_ok = False
    if block is not None and len(init_begins) == 1 and len(init_ends) == 1 and action_position is not None:
        if init_ends[0].end() < action_position:
            init_ok = DESIGN_ACTIVATION.search(block) is not None
    if not init_ok:
        diagnostics.append(TclConventionDiagnostic("TCL-SCRIPT-004", path, None, "DESIGN_INIT block with an EDA activation command must complete before TEST_ACTION"))

    substantive_lines = [
        line for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    tail_ok = (
        len(substantive_lines) >= 2
        and RUN_SUMMARY.fullmatch(substantive_lines[-2]) is not None
        and RUN_EXIT.fullmatch(substantive_lines[-1]) is not None
    )
    if not tail_ok:
        diagnostics.append(TclConventionDiagnostic(
            "TCL-SCRIPT-005",
            path,
            None,
            "each run_N.tcl must end with pv_rpt_checkpoints followed by exit",
        ))


def validate_tcl_conventions(case_dir: Path) -> list[TclConventionDiagnostic]:
    case_dir = case_dir.resolve() if not case_dir.is_symlink() else case_dir.absolute()
    diagnostics: list[TclConventionDiagnostic] = []

    if case_dir.is_symlink() or not case_dir.is_dir():
        return [TclConventionDiagnostic("TCL-SUITE-001", case_dir, None, "input must be a non-symlink case directory")]
    if not CASE_DIR.fullmatch(case_dir.name):
        diagnostics.append(TclConventionDiagnostic("TCL-SUITE-002", case_dir, None, "directory must match posNNN_<scenario> or negNNN_<scenario>"))
    polarity = "pos" if case_dir.name.startswith("pos") else "neg"

    nith_path = case_dir / "nith.run"
    tcl_dir = case_dir / "tcl"
    design_path = tcl_dir / "design.tcl"
    tool_subdirs = sorted([d for d in tcl_dir.iterdir() if d.is_dir()], key=lambda p: p.name) if tcl_dir.is_dir() else []

    valid_tool = len(tool_subdirs) == 1 and tool_subdirs[0].name in ALLOWED_TOOLS
    if not valid_tool:
        diagnostics.append(TclConventionDiagnostic("TCL-STRUCT-002", case_dir, None, "exactly one tcl/<tool>/ subdirectory is required, tool in {optimus, itools}"))
    tool_dir = tool_subdirs[0] if tool_subdirs else None

    design_text = _read(design_path)
    nith_text = _read(nith_path)

    struct_missing = []
    if nith_text is None:
        struct_missing.append("nith.run")
    if design_text is None:
        struct_missing.append("tcl/design.tcl")
    mmmc_path = (tool_dir / "mmmc.tcl") if tool_dir else None
    mmmc_text = _read(mmmc_path) if mmmc_path else None
    if mmmc_text is None:
        struct_missing.append("tcl/<tool>/mmmc.tcl")

    run_files: list[Path] = []
    run_indices: list[int] = []
    if tool_dir and tool_dir.is_dir():
        for entry in sorted(tool_dir.iterdir(), key=lambda p: p.name):
            match = RUN_FILE.fullmatch(entry.name)
            if match and entry.is_file():
                run_files.append(entry)
                run_indices.append(int(match.group(1)))
    if not run_files or not _contiguous_from_one(run_indices):
        struct_missing.append("tcl/<tool>/run_1.tcl..run_N.tcl (contiguous from 1)")
    if struct_missing:
        diagnostics.append(TclConventionDiagnostic("TCL-STRUCT-001", case_dir, None, "case tree incomplete: missing " + ", ".join(struct_missing)))

    tcl_files = [p for p in (design_path, mmmc_path, *run_files) if p is not None and p.is_file()]
    all_files = tcl_files + ([nith_path] if nith_text is not None else [])

    for path in tcl_files:
        text = _read(path) or ""
        machine = MACHINE_PATH.search(text)
        if machine:
            _add(diagnostics, "TCL-RUNNER-001", path, text, machine.start(), "machine-specific absolute path is not portable")
        placeholder = PLACEHOLDER.search(text)
        if placeholder:
            _add(diagnostics, "TCL-SCRIPT-002", path, text, placeholder.start(), "unresolved TODO/TBD placeholder")
        for env in ENV_VARIABLE.finditer(text):
            if env.group(1).strip() not in ALLOWED_ENV_VARIABLES:
                _add(diagnostics, "TCL-SCRIPT-003", path, text, env.start(), f"environment variable {env.group(1).strip()} is not allowed; only PV_ROOT and PV_TOOL are permitted")

    if nith_text is not None:
        placeholder = PLACEHOLDER.search(nith_text)
        if placeholder:
            _add(diagnostics, "TCL-SCRIPT-002", nith_path, nith_text, placeholder.start(), "unresolved TODO/TBD placeholder")
        setup_start = nith_text.find(NITH_INIT_END)
        setup_text = nith_text[setup_start + len(NITH_INIT_END):] if setup_start != -1 else nith_text
        machine = MACHINE_PATH.search(setup_text)
        if machine:
            _add(diagnostics, "TCL-RUNNER-001", nith_path, nith_text, machine.start(), "machine-specific absolute path is not portable in case setup")

    if design_text is not None and not DESIGN_CATEGORY.search(design_text):
        diagnostics.append(TclConventionDiagnostic("TCL-DESIGN-001", design_path, None, "design.tcl must declare top/netlist/lef/lib/sdc input paths"))
    if design_text is not None and not re.search(
        r"(?m)^# Generated from central design profile: [a-z][a-z0-9_]*$", design_text
    ):
        diagnostics.append(TclConventionDiagnostic(
            "TCL-DESIGN-003", design_path, None,
            "design.tcl must be generated from assets/design-profiles.json and record its profile",
        ))

    for helper_path, helper_text in ((design_path, design_text), (mmmc_path, mmmc_text)):
        if helper_text is not None and HELPER_INIT_COMMAND.search(helper_text):
            diagnostics.append(TclConventionDiagnostic(
                "TCL-RUN-001",
                helper_path,
                None,
                "PV source, set_options, setup_design, and read_def belong only in run_N.tcl DESIGN_INIT",
            ))

    if nith_text is not None:
        has_begin = NITH_INIT_BEGIN in nith_text
        has_end = NITH_INIT_END in nith_text
        setup_start = nith_text.find(NITH_INIT_END)
        setup_text = nith_text[setup_start + len(NITH_INIT_END):] if setup_start != -1 else ""
        referenced = sorted(int(x) for x in NITH_INPUT.findall(setup_text))
        run_calls = len(NITH_RUN_CALL.findall(setup_text))
        has_done = bool(NITH_DONE_CALL.search(setup_text))
        nith_ok = (
            has_begin and has_end
            and _contiguous_from_one(referenced)
            and referenced == run_indices
            and run_calls >= len(referenced) >= 1
            and has_done
        )
        if not nith_ok:
            diagnostics.append(TclConventionDiagnostic("TCL-NITH-001", nith_path, None, "nith.run must preserve the NITH init block and reference each run_<N>.tcl in order with nith_run/nith_done"))

    checkpoint_total = 0
    for run_file in run_files:
        text = _read(run_file)
        if text is None:
            continue
        checkpoint_total += len(_commands(text))
        if design_text is not None:
            _validate_design_variable_reuse(design_text, text, run_file, diagnostics)
        _validate_run_script(text, run_file, polarity, tcl_files, diagnostics)
    if checkpoint_total == 0:
        diagnostics.append(TclConventionDiagnostic("TCL-CHECKPOINT-001", case_dir, None, "case tree must call pv_check_log, pv_check_golden, or pv_check_qor"))

    return diagnostics


def convention_report(case_dir: Path) -> dict[str, object]:
    diagnostics = [item.to_dict() for item in validate_tcl_conventions(case_dir)]
    status = "FAIL" if diagnostics else "PASS"
    return {"id": "L2B", "status": status, "input": str(case_dir.resolve()), "diagnostics": diagnostics}
