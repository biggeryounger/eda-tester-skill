"""Static Optimus command validation against a provenance-locked help snapshot.

No input script or source command is evaluated. Dynamic values/dispatch and
undocumented semantics are explicit SPEC-GAP, never a guessed PASS.
"""
from __future__ import annotations

import hashlib
from dataclasses import replace
import math
from pathlib import Path
import re

from tcl_static_parser import TclParser, TclSyntaxError, Word

DEFAULT_DATABASE = Path(__file__).resolve().parents[1] / 'references/optimus-syntax/all_cmd_1008.txt'
SOURCE_SHA256 = '1fa52ed045ae3d37a17fb51752478d7f2a28c0a9bbf3741fd77420e0fa07018b'
SNAPSHOT = 'optimus-doc-20261015-1fa52ed045ae'
BUILTINS = set('''after append apply array binary break catch cd chan clock close concat
continue coroutine dict encoding eof error eval exec exit expr fblocked fconfigure
fcopy file fileevent flush for foreach format gets glob global history if incr info
interp join lappend lassign lindex linsert list llength lmap load lrange lrepeat
lreplace lreverse lsearch lset lsort namespace open package pid proc puts pwd read
regexp regsub rename return scan seek set socket source split string subst switch
tailcall tell throw time trace try unknown unload unset update uplevel upvar variable
vwait while yield yieldto zlib'''.split())
PV_COMMANDS = set('''pv_check_log pv_check_golden pv_check_qor pv_rpt_checkpoints
pv_check_point pv_mark_begin pv_mark_end pv_check_mark pv_check_route
pv_parse_route_mark pv_compare_route_json pv_diff_str pv_find_string pv_diff_files
pv_check_golden_img pv_print_nested_list'''.split())
SCRIPT_COMMANDS = {'pv_check_log', 'pv_check_qor', 'pv_check_route', 'catch', 'time'}
TYPES = {'boolean', 'string', 'string_list', 'double', 'object_list', 'enum',
         'integer', 'double_list', 'rect', 'object_list_list', 'point', 'enum_list',
         'int_list', 'point_list', 'double_list_list', 'rect_dbu', 'object',
         'list_string_list', 'operation'}


def load_database(path=None):
    path = DEFAULT_DATABASE if path is None else Path(path)
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError('unsupported or modified command snapshot SHA-256')
    text = raw.decode('utf-8')
    commands, current = {}, None
    for line_no, line in enumerate(text.splitlines(), 1):
        match = re.match(r'^\*\*([^*]+)\*\*\s*-\s*(.*)', line)
        if match:
            name, description = match.groups()
            if name in commands:
                raise ValueError(f'duplicate command at line {line_no}')
            current = {'description': description, 'line': line_no, 'parameters': [], 'relations': []}
            commands[name] = current
            stage = re.search(r'must specify one stage from\s*\{([^}]+)\}', description)
            if stage:
                current['relations'].append({'kind': 'exactly_one', 'options': re.findall(r'-[a-z_]+', stage[1])})
            either = re.search(r'Either (-\w+) or (-\w+) must be specified', description)
            if either:
                current['relations'].append({'kind': 'at_least_one', 'options': list(either.groups())})
        elif line.startswith('|') and not line.startswith(('| Name', '|---')):
            fields = [v.strip() for v in line.strip().strip('|').split('|')]
            if current is None or len(fields) != 3 or fields[1] not in TYPES:
                raise ValueError(f'unsupported table row at line {line_no}')
            name, kind, legal = fields
            current['parameters'].append({'name': name.strip('[] '), 'optional': name.startswith('['),
                                           'type': kind, 'legal': legal, 'line': line_no})
    if len(commands) != 464:
        raise ValueError('snapshot command count is not 464')
    return {'snapshot': SNAPSHOT, 'tool': 'optimus', 'tool_version': None,
            'source_sha256': digest, 'commands': commands}


def _option_word(value):
    if value is None or not value.startswith('-') or value == '-':
        return False
    try:
        float(value)
        return False
    except ValueError:
        try:
            int(value, 0)
            return False
        except ValueError:
            return True


def _status(diagnostics):
    statuses = {d['status'] for d in diagnostics}
    for status in ('FAIL', 'TOOL_UNAVAILABLE', 'SPEC-GAP'):
        if status in statuses:
            return status
    return 'PASS'


def check_scripts(paths, *, tool='optimus', database=None):
    paths = [Path(path) for path in paths]
    syntax, eda = [], []
    def diagnostic(target, rule, status, path, line, message, source_line=None):
        target.append({'rule_id': rule, 'status': status, 'severity': 'error',
                       'file': str(path), 'line': line, 'message': message,
                       'source_line': source_line})
    try:
        parser = TclParser()
    except (RuntimeError, OSError, AttributeError) as exc:
        diagnostic(syntax, 'TCL-PARSER-UNAVAILABLE', 'TOOL_UNAVAILABLE', '', None, str(exc))
        parser = None
    db = None
    try:
        if tool != 'optimus':
            raise ValueError(f'no syntax database for target tool {tool}')
        db = load_database(database)
    except (OSError, ValueError, UnicodeError) as exc:
        diagnostic(eda, 'OPT-DATABASE-UNAVAILABLE', 'TOOL_UNAVAILABLE', '', None, str(exc))
    if parser is None:
        diagnostic(eda, 'OPT-PARSER-UNAVAILABLE', 'TOOL_UNAVAILABLE', '', None, 'command analysis requires the Tcl parser')
    if not paths:
        diagnostic(syntax, 'TCL-INPUT-001', 'FAIL', '', None, 'no Tcl scripts supplied')
    known_procs = set()
    parsed_files = []
    checked, dynamic = 0, 0
    if parser is not None:
        for path in paths:
            path = Path(path)
            try:
                text = path.read_text(encoding='utf-8')
                commands = parser.parse(text)
                parsed_files.append((path, commands))
            except TclSyntaxError as exc:
                diagnostic(syntax, 'TCL-SYNTAX-001', 'FAIL', path, exc.line, str(exc))
            except (OSError, UnicodeError) as exc:
                diagnostic(syntax, 'TCL-INPUT-001', 'FAIL', path, None, str(exc))

    def issue(path, word, code, message, spec=None, status='FAIL'):
        nonlocal dynamic
        if status == 'SPEC-GAP':
            dynamic += 1
        diagnostic(eda, code, status, path, word.line, message, spec.get('line') if spec else None)

    def validate_value(path, word, parameter):
        kind, value, legal = parameter['type'], word.literal, parameter['legal']
        if value is None:
            if kind not in ('string', 'object'):
                issue(path, word, 'OPT-DYNAMIC-001', f'dynamic {parameter["name"]}: cannot prove {kind}/legal values', parameter, 'SPEC-GAP')
            return
        try:
            values = parser.split_list(value) if kind.endswith('_list') or kind in ('rect', 'rect_dbu', 'point') else [value]
            enum = parser.split_list(legal[1:-1]) if legal.startswith('{') and legal.endswith('}') else None
            def number(v, integer=False):
                if integer:
                    if not re.fullmatch(r'[+-]?(?:\d+|0[xX][0-9a-fA-F]+)', v):
                        raise ValueError('expected integer')
                    n = int(v, 16) if 'x' in v.lower() else int(v, 10)
                else:
                    n = float(v)
                    if not math.isfinite(n):
                        raise ValueError('non-finite number')
                match = re.fullmatch(r'\[\s*([^,]+),\s*([^\]]+)\]', legal)
                if match and not float(match[1]) <= n <= float(match[2]):
                    raise ValueError(f'outside {legal}')
            if kind in ('integer', 'int_list', 'rect_dbu'):
                for item in values:
                    number(item, True)
            elif kind in ('double', 'double_list', 'point', 'rect'):
                for item in values:
                    number(item)
            elif kind in ('enum', 'enum_list'):
                if not enum:
                    issue(path, word, 'OPT-SPEC-001', 'enum has no legal-value definition', parameter, 'SPEC-GAP')
                    return
                if any(item not in enum for item in values):
                    raise ValueError(f'expected one of {enum}')
            elif kind in ('object_list_list', 'double_list_list', 'list_string_list', 'point_list'):
                for item in values:
                    inner = parser.split_list(item)
                    if kind in ('double_list_list', 'point_list'):
                        for v in inner:
                            number(v)
                    if kind == 'point_list' and len(inner) != 2:
                        raise ValueError('each point needs two coordinates')
            elif kind == 'operation':
                issue(path, word, 'OPT-SPEC-001', 'operation semantics not defined by source table', parameter, 'SPEC-GAP')
            if kind == 'point' and len(values) != 2:
                raise ValueError('point needs 2 coordinates')
            if kind in ('rect', 'rect_dbu') and len(values) != 4:
                raise ValueError('rect needs 4 coordinates')
        except (ValueError, OverflowError) as exc:
            issue(path, word, 'OPT-TYPE-001', f'{parameter["name"]}: invalid {kind}: {exc}', parameter)

    def validate_command(path, words, spec):
        nonlocal checked
        checked += 1
        if any(w.expanded for w in words):
            issue(path, words[0], 'OPT-DYNAMIC-001', 'argument expansion cannot be resolved statically', spec, 'SPEC-GAP')
            return
        named = {p['name']: p for p in spec['parameters'] if p['name'].startswith('-')}
        positional = [p for p in spec['parameters'] if not p['name'].startswith('-')]
        seen, actual, position, uncertain = set(), [], 1, False
        while position < len(words):
            word = words[position]
            value = word.literal
            if _option_word(value):
                if value not in named:
                    issue(path, word, 'OPT-OPTION-001', f'unknown option {value}', spec)
                    position += 1
                    continue
                parameter = named[value]
                if value in seen:
                    issue(path, word, 'OPT-SPEC-001', f'repeatability of {value} is undocumented', parameter, 'SPEC-GAP')
                seen.add(value)
                if parameter['type'] != 'boolean':
                    if position + 1 == len(words) or _option_word(words[position + 1].literal):
                        issue(path, word, 'OPT-ARG-001', f'missing value for {value}', parameter)
                    else:
                        position += 1
                        validate_value(path, words[position], parameter)
            else:
                actual.append(word)
                if value is None and len(actual) > len(positional):
                    uncertain = True
                    issue(path, word, 'OPT-DYNAMIC-001', 'dynamic argument may contain option dispatch', spec, 'SPEC-GAP')
            position += 1
        for name, parameter in named.items():
            if not parameter['optional'] and name not in seen and not uncertain:
                issue(path, words[0], 'OPT-REQUIRED-001', f'missing required option {name}', parameter)
        required = sum(not p['optional'] for p in positional)
        if len(actual) < required:
            issue(path, words[0], 'OPT-ARG-001', f'expected at least {required} positional arguments, got {len(actual)}', spec)
        if len(actual) > len(positional) and not uncertain:
            # A table does not specify whether a list consumes multiple words.
            if positional and positional[-1]['type'].endswith('_list'):
                issue(path, actual[len(positional)], 'OPT-SPEC-001', 'list positional word multiplicity is undocumented; use one Tcl list word', spec, 'SPEC-GAP')
            else:
                issue(path, actual[len(positional)], 'OPT-ARG-001', 'unexpected positional argument', spec)
        for word, parameter in zip(actual, positional):
            validate_value(path, word, parameter)
        for relation in spec['relations']:
            count = len(seen.intersection(relation['options']))
            if count == 0 and uncertain:
                continue
            if (relation['kind'] == 'exactly_one' and count != 1) or (relation['kind'] == 'at_least_one' and not count):
                issue(path, words[0], 'OPT-RELATION-001', f'{relation["kind"]} required from {relation["options"]}', spec)

    def body(path, word, depth, expression=False, bindings=None):
        if word.literal is None:
            issue(path, word, 'OPT-DYNAMIC-001', 'dynamic script/expression cannot be parsed statically', status='SPEC-GAP')
            return
        if expression:
            for text, line in parser.expression(word.literal, word.line):
                walk(path, parser.parse(text, line), depth + 1, dict(bindings or {}))
        else:
            line = word.line
            walk(path, parser.parse(word.literal, line), depth + 1, dict(bindings or {}))

    def concat_body(path, words, depth, bindings):
        if not words:
            diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, None, 'missing script body')
        elif any(w.literal is None for w in words):
            issue(path, words[0], 'OPT-DYNAMIC-001', 'dynamic concatenated script', status='SPEC-GAP')
        else:
            text = parser.concat([w.literal for w in words])
            walk(path, parser.parse(text, words[0].line), depth + 1, dict(bindings))

    source_stack = set()

    def walk(path, commands, depth=0, bindings=None):
        bindings = {} if bindings is None else bindings
        if depth > 100:
            diagnostic(eda, 'OPT-DYNAMIC-001', 'SPEC-GAP', path, None, 'nested script depth exceeds static limit')
            return
        for cmd in commands:
            words = cmd.words
            name = words[0].literal
            if name is not None and name.lstrip(':') == 'proc' and len(words) >= 4 and words[1].literal:
                known_procs.add(words[1].literal.lstrip(':'))
        for cmd in commands:
            words = cmd.words
            try:
                for word in words:
                    for text, line in word.substitutions:
                        walk(path, parser.parse(text, line), depth + 1, dict(bindings))
                if any(word.substitutions for word in words):
                    bindings.clear()
                resolved = []
                for original in words:
                    match = re.fullmatch(r'\$([A-Za-z_][A-Za-z0-9_:]*)|\$\{([^}]+)\}', original.raw)
                    key = (match[1] or match[2]) if match else None
                    resolved.append(replace(original, literal=bindings[key]) if key in bindings else original)
                words = resolved
                name = words[0].literal
                if name is None:
                    issue(path, words[0], 'OPT-DYNAMIC-001', 'dynamic command name', status='SPEC-GAP')
                    continue
                name = name.removeprefix('::')
                if db is not None and name in db['commands']:
                    validate_command(path, words, db['commands'][name])
                elif name not in BUILTINS | PV_COMMANDS | known_procs and db is not None:
                    issue(path, words[0], 'OPT-CMD-001', f'unknown command {name}; absent from 464-command snapshot and local procs')
                args = words[1:]
                if name == 'set' and len(args) == 2 and args[0].literal is not None:
                    if args[1].literal is None:
                        bindings.pop(args[0].literal, None)
                    else:
                        bindings[args[0].literal] = args[1].literal
                elif name in ('unset', 'incr', 'append', 'lappend') and args and args[0].literal:
                    bindings.pop(args[0].literal, None)
                minimum_arity = {'eval': 1, 'uplevel': 1, 'apply': 1, 'expr': 1, 'try': 1, 'switch': 2, 'catch': 1}
                if name in minimum_arity and len(args) < minimum_arity[name]:
                    diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, f'{name} has too few arguments')
                if name in ('foreach', 'lmap') and (len(args) < 3 or len(args) % 2 != 1):
                    diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, f'{name} needs variable/list pairs and a body')
                exact_arity = {'proc': 3, 'while': 2, 'for': 4}
                if name in exact_arity and len(args) != exact_arity[name]:
                    diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, f'{name} requires {exact_arity[name]} arguments')
                if name == 'if' and len(args) < 2:
                    diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, 'if requires expression and body')
                if name == 'source':
                    target = args[-1] if args else None
                    if target is None:
                        diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, 'source requires a path')
                    elif target.literal is not None:
                        candidate = Path(target.literal)
                        if not candidate.is_absolute():
                            # Normal case paths are relative to the case root, not tcl/optimus.
                            root = next((parent for parent in path.parents if (parent / 'tcl').is_dir()), path.parent)
                            candidate = root / candidate
                        if candidate.resolve() not in {p.resolve() for p in paths}:
                            issue(path, target, 'OPT-SOURCE-001', 'source target is outside inspected files', status='SPEC-GAP')
                        elif candidate.resolve() in source_stack:
                            issue(path, target, 'OPT-SOURCE-001', 'cyclic source requires runtime analysis', status='SPEC-GAP')
                        else:
                            source_stack.add(candidate.resolve())
                            try:
                                for source_path, source_commands in parsed_files:
                                    if source_path.resolve() == candidate.resolve():
                                        walk(source_path, source_commands, depth + 1, bindings)
                                        break
                            finally:
                                source_stack.remove(candidate.resolve())
                    elif not re.fullmatch(r'\$(?:::)?env\(PV_ROOT\)/(?:pv/)?scripts/pv\.tcl', target.raw):
                        issue(path, target, 'OPT-SOURCE-001', 'dynamic source target cannot be inspected', status='SPEC-GAP')
                if name in SCRIPT_COMMANDS and args:
                    body(path, args[0], depth, bindings=bindings)
                elif name == 'proc' and len(args) == 3:
                    if args[1].literal is None:
                        issue(path, args[1], 'OPT-DYNAMIC-001', 'dynamic formal argument list', status='SPEC-GAP')
                    else:
                        try:
                            formals = parser.split_list(args[1].literal)
                            if any(not 1 <= len(parser.split_list(formal)) <= 2 for formal in formals):
                                raise ValueError('formal argument must have name and optional default')
                        except ValueError as exc:
                            diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, str(exc))
                    body(path, args[2], depth, bindings={})
                elif name in ('foreach', 'lmap', 'foreach_in_collection') and len(args) >= 3:
                    body(path, args[-1], depth, bindings=bindings)
                elif name == 'while' and len(args) == 2:
                    body(path, args[0], depth, True, bindings=bindings)
                    body(path, args[1], depth, bindings=bindings)
                elif name == 'for' and len(args) == 4:
                    for i, word in enumerate(args):
                        body(path, word, depth, i == 1, bindings=bindings)
                elif name == 'if':
                    i = 0
                    while i < len(args):
                        marker = args[i].literal
                        if i and marker not in ('elseif', 'else'):
                            diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, 'expected elseif or else')
                            break
                        if marker == 'elseif':
                            i += 1
                            if i == len(args):
                                diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, 'elseif has no expression/body')
                                break
                            marker = args[i].literal
                        if marker == 'else':
                            if i + 2 != len(args):
                                diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, 'else requires exactly one final body')
                            elif i + 1 < len(args):
                                body(path, args[i + 1], depth, bindings=bindings)
                            break
                        body(path, args[i], depth, True, bindings=bindings)
                        i += 1
                        if i < len(args) and args[i].literal == 'then':
                            i += 1
                        if i < len(args):
                            body(path, args[i], depth, bindings=bindings)
                            i += 1
                        else:
                            diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, 'if branch has no body')
                elif name == 'expr':
                    if args and all(w.literal is not None for w in args):
                        word = Word('', ' '.join(w.literal for w in args), args[0].line)
                        body(path, word, depth, True, bindings=bindings)
                    elif args:
                        issue(path, words[0], 'OPT-DYNAMIC-001', 'dynamic expression', status='SPEC-GAP')
                    else:
                        diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, 'expr requires an expression')
                elif name in ('eval', 'uplevel'):
                    scripts = args
                    if name == 'uplevel' and args and args[0].literal is not None and re.fullmatch(r'#?\d+', args[0].literal):
                        scripts = args[1:]
                    concat_body(path, scripts, depth, bindings)
                elif name == 'apply':
                    if not args or args[0].literal is None:
                        issue(path, words[0], 'OPT-DYNAMIC-001', 'dynamic or absent lambda', status='SPEC-GAP')
                    else:
                        try:
                            parts = parser.split_list(args[0].literal)
                            if len(parts) not in (2, 3):
                                raise ValueError('lambda needs argument list, body and optional namespace')
                            body(path, Word('', parts[1], args[0].line), depth, bindings={})
                        except ValueError as exc:
                            diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, str(exc))
                elif name == 'try' and args:
                    body(path, args[0], depth, bindings=bindings)
                    i = 1
                    while i < len(args):
                        marker = args[i].literal
                        size = 2 if marker == 'finally' else 4 if marker in ('on', 'trap') else 0
                        if not size or i + size > len(args) or (marker == 'finally' and i + size != len(args)):
                            diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, 'invalid try handler')
                            break
                        body(path, args[i + size - 1], depth, bindings=bindings)
                        i += size
                elif name == 'switch':
                    i = 0
                    while i < len(args) and args[i].literal and args[i].literal.startswith('-'):
                        flag = args[i].literal
                        i += 1
                        if flag == '--':
                            break
                        if flag in ('-matchvar', '-indexvar'):
                            i += 1
                        elif flag not in ('-exact', '-glob', '-regexp', '-nocase'):
                            diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, 'unknown switch option')
                    pairs = args[i + 1:]
                    if len(pairs) == 1:
                        if pairs[0].literal is None:
                            issue(path, pairs[0], 'OPT-DYNAMIC-001', 'dynamic switch branch list', status='SPEC-GAP')
                            pairs = []
                        else:
                            try:
                                pairs = [Word('', v, pairs[0].line) for v in parser.split_list(pairs[0].literal)]
                            except ValueError as exc:
                                diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, str(exc))
                                pairs = []
                    if len(pairs) % 2 or i >= len(args):
                        diagnostic(syntax, 'TCL-SYNTAX-002', 'FAIL', path, cmd.line, 'switch requires string and pattern/body pairs')
                    for script in pairs[1::2]:
                        if script.literal != '-':
                            body(path, script, depth, bindings=bindings)
                elif name == 'namespace' and len(args) >= 3 and args[0].literal == 'eval':
                    concat_body(path, args[2:], depth, bindings)
                elif name in ('subst', 'interp', 'exec', 'load', 'rename', 'unknown'):
                    issue(path, words[0], 'OPT-DYNAMIC-001', f'{name} requires additional script/dispatch analysis', status='SPEC-GAP')
                # Keep only assignments whose values remain provable. Arbitrary Tcl
                # bodies and local helpers may mutate caller/global variables.
                if name in PV_COMMANDS | known_procs | BUILTINS and name not in {'set', 'source', 'proc'}:
                    bindings.clear()
            except TclSyntaxError as exc:
                bindings.clear()
                diagnostic(syntax, 'TCL-SYNTAX-001', 'FAIL', path, exc.line, str(exc))
    if parser is not None:
        for path, commands in parsed_files:
            walk(path, commands)
    checks = [{'id': 'TCL-SYNTAX', 'status': _status(syntax), 'diagnostics': syntax},
              {'id': 'OPTIMUS-COMMANDS', 'status': _status(eda), 'diagnostics': eda}]
    statuses = [c['status'] for c in checks]
    status = next((s for s in ('FAIL', 'TOOL_UNAVAILABLE', 'SPEC-GAP') if s in statuses), 'PASS')
    return {'status': status, 'checks': checks, 'snapshot': db['snapshot'] if db else None,
            'tool_version': None, 'database_commands': len(db['commands']) if db else 0,
            'commands_checked': checked, 'unresolved_checks': dynamic,
            'parser_version': parser.version if parser else None}
