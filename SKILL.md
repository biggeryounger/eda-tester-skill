---
name: eda-tester-skill
description: Generate traceable EDA command test designs and runnable TCL test scripts from command manuals, syntax descriptions, or natural-language requirements. Use for decomposing Innovus/iTools, Optimus, or PrimeTime command behavior into positive, negative, boundary, interaction, and environment-dependent cases; producing case directories and TCL; or validating an EDA command test suite against function.json.
---

# EDA Test Case Generation

## Workflow

1. Identify the exact tool, command name, and target tool version. Preserve the product names **Optimus**、**iTools / Innovus**、**PrimeTime**.
2. Select tool-specific background knowledge:
   - For iTools / Innovus, query the `INNOVUS191` corpus at `http://49.1.1.123:5175/` according to `references/innovus-command-corpus.md`. Send only the command name and generic documentation questions; never send design data, logs, internal paths, or other sensitive content. Treat corpus failure or version mismatch as a recorded gap, not permission to invent facts.
   - For Optimus, read `references/optimus-tcl-corpus.md` to obtain the full-flow phase model and MMMC object relationships. Reuse its structure, not its example PDK/design values, and obtain command syntax from target-version documentation.
3. Read all user-provided command descriptions completely and reconcile them with the selected corpus using documented source boundaries. Preserve exact tool and command names.
4. Extract syntax, parameters, types, requiredness, defaults, constraints, interactions, expected messages, environment prerequisites, source provenance, and unresolved gaps.
5. Before producing any test design, ask the user to select one or more strategies from `Smoke case`, `正向覆盖`, and `负向覆盖`. Use the exact interaction and coverage rules in `references/test-strategies.md`. If the current request already contains an explicit selection, restate it and continue without asking again. Do not choose a default for the user.
6. Map the request to feature IDs in `function.json`. Do not invent an ID when an existing feature applies. Before changing a feature to `active`, create its tests, register their paths and command IDs, and run `python3 scripts/validate.py feature <FEATURE_ID>` during implementation.
7. Copy `assets/templates/测试用例设计表.xlsx` as the output test-plan workbook and populate its `cmd` sheet. Preserve the A-J columns and existing formatting. Record the selected strategies and tag every scenario with its source strategy.
8. Build the coverage matrix required by the selected strategies. When multiple strategies are selected, take their union, merge exact duplicate scenarios, and preserve all applicable strategy tags.
9. Name case directories `pos<index>_<scenario>` or `neg<index>_<scenario>`, using a three-digit, command-local index such as `pos001_base` or `neg002_missing_netlist`.
10. Create one `case.toml` and one or more `.tcl` files per case. Keep setup, action, and assertions distinguishable.
11. Use deterministic object names and avoid relying on ambient tool state. Mark cases that require a licensed EDA runtime as `runtime = "eda"`.
12. Run the two-layer validation before handing off results:
   - Layer 1: validate the generated test plan against `references/specs/test-plan-rules.md`.
   - Layer 2A: run `python3 scripts/validate.py tcl <script.tcl>`. Require Nagelfar 1.3.5 and the bundled Innovus/iTools syntax database; preserve `TOOL_UNAVAILABLE` rather than treating a missing or mismatched checker as success.
   - Layer 2B: validate TCL conventions against `references/specs/tcl-script-rules.md`.
13. Keep syntax findings separate from convention findings. Do not use Agent judgment as a substitute for either checker.

## Required case metadata

Use this shape in `case.toml`:

```toml
id = "pos001_required"
feature_ids = ["F-003", "F-008"]
command = "add_net"
polarity = "positive"
runtime = "static"
script = "run.tcl"
expected = "accept"
description = "Accept the minimum required arguments."
```

Keep `id` equal to the directory name. Use `polarity = "negative"` and `expected = "reject"` for expected-fail cases. Use lowercase ASCII snake_case for the scenario segment.

## TCL generation rules

- Put the command under test on a line containing `# TEST_ACTION`.
- Add `# EXPECT: PASS` or `# EXPECT: FAIL` before the action.
- Generate a real case tree with `design/`, `golden/`, `nith.run`, `tcl/case_setup.tcl`, and the applicable `tcl/itools/` or `tcl/optimus/` tool directory. Do not create symbolic links anywhere in the case tree.
- Put tool runs in consecutively numbered `run_<N>.tcl` files and have `nith.run` select them through `nith.PV_TOOL`, invoke each once in order, then call `nith_done()`.
- Load the target environment's explicitly configured PV entry before checkpoint use. Current references contain both `$env(PV_ROOT)/pv/scripts/pv.tcl` and the Optimus flow's `$env(PV_ROOT)/scripts/pv.tcl`; never guess between them. Every case must use at least one suitable checkpoint: `pv_check_log` for log content, `pv_check_golden` for generated files, or `pv_check_qor` for supported timing/QoR metrics.
- Fail explicitly for locally checkable unmet preconditions.
- Do not fake tool output. Separate static validation from actual EDA execution.
- Quote or brace values containing whitespace or Tcl metacharacters.

## References

- Read [references/innovus-command-corpus.md](references/innovus-command-corpus.md) before querying command information for iTools / Innovus.
- Read [references/optimus-tcl-corpus.md](references/optimus-tcl-corpus.md) before generating Optimus full-flow or MMMC TCL.
- Read [references/test-strategies.md](references/test-strategies.md) before asking for a strategy selection or designing coverage.
- Read [references/test-plan.md](references/test-plan.md) when planning coverage, release gates, or runtime validation.
- Read [references/specs/test-plan-rules.md](references/specs/test-plan-rules.md) before validating a generated test plan.
- Read [references/specs/tcl-script-rules.md](references/specs/tcl-script-rules.md) before validating generated TCL conventions.
- Read `function.json` when selecting scope or reporting feature completion.
