---
name: eda-tester-skill
description: Generate traceable EDA command test designs and runnable TCL test scripts from command manuals, syntax descriptions, or natural-language requirements. Use for decomposing Innovus/iTools, Optimus, or PrimeTime command behavior into positive, negative, boundary, interaction, and environment-dependent cases; producing case directories and TCL; or validating an EDA command test suite against function.json.
---

# EDA Test Case Generation

## Workflow

1. Read the source command description completely. Preserve exact tool and command names.
2. Extract syntax, parameters, types, requiredness, defaults, constraints, interactions, expected messages, and environment prerequisites.
3. Map the request to feature IDs in `function.json`. Do not invent an ID when an existing feature applies. Before changing a feature to `active`, create its tests, register their paths and command IDs, and run `python3 scripts/validate.py feature <FEATURE_ID>` during implementation.
4. Copy `assets/templates/测试用例设计表.xlsx` as the output test-plan workbook and populate its `cmd` sheet. Preserve the A-J columns and existing formatting.
5. Build a coverage matrix containing happy path, every option independently, required omissions, invalid types or enums, boundaries, conflicting options, repeated options, object-state preconditions, and regression examples.
6. Name case directories `pos<index>_<scenario>` or `neg<index>_<scenario>`, using a three-digit, command-local index such as `pos001_base` or `neg002_missing_netlist`.
7. Create one `case.toml` and one or more `.tcl` files per case. Keep setup, action, and assertions distinguishable.
8. Use deterministic object names and avoid relying on ambient tool state. Mark cases that require a licensed EDA runtime as `runtime = "eda"`.
9. Run the two-layer validation before handing off results:
   - Layer 1: validate the generated test plan against `references/specs/test-plan-rules.md`.
   - Layer 2A: run `python3 scripts/validate.py tcl <script.tcl>`. Require Nagelfar 1.3.5 and the bundled Innovus/iTools syntax database; preserve `TOOL_UNAVAILABLE` rather than treating a missing or mismatched checker as success.
   - Layer 2B: validate TCL conventions against `references/specs/tcl-script-rules.md`.
10. Keep syntax findings separate from convention findings. Do not use Agent judgment as a substitute for either checker.

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
- Fail explicitly for locally checkable unmet preconditions.
- Do not fake tool output. Separate static validation from actual EDA execution.
- Quote or brace values containing whitespace or Tcl metacharacters.

## References

- Read [references/test-plan.md](references/test-plan.md) when planning coverage, release gates, or runtime validation.
- Read [references/specs/test-plan-rules.md](references/specs/test-plan-rules.md) before validating a generated test plan.
- Read [references/specs/tcl-script-rules.md](references/specs/tcl-script-rules.md) before validating generated TCL conventions.
- Read `function.json` when selecting scope or reporting feature completion.
