"""Read Tcl 8 parser tokens through its public C API; never evaluate input.

The Tcl 8 Tcl_Parse/Tcl_Token ABI is defined in tcl.h. Tcl 9 is deliberately
rejected: its structure sizes may differ. No Tcl interpreter is created.
"""
from __future__ import annotations

import ctypes as C
import ctypes.util
import sys
from dataclasses import dataclass, field


class Token(C.Structure):
    _fields_ = [('type', C.c_int), ('start', C.c_void_p), ('size', C.c_int), ('numComponents', C.c_int)]


class Parse(C.Structure):
    _fields_ = [('commentStart', C.c_void_p), ('commentSize', C.c_int),
                ('commandStart', C.c_void_p), ('commandSize', C.c_int),
                ('numWords', C.c_int), ('tokenPtr', C.POINTER(Token)),
                ('numTokens', C.c_int), ('tokensAvailable', C.c_int), ('errorType', C.c_int),
                ('string', C.c_void_p), ('end', C.c_void_p), ('interp', C.c_void_p),
                ('term', C.c_void_p), ('incomplete', C.c_int), ('staticTokens', Token * 20)]


class TclSyntaxError(ValueError):
    def __init__(self, message, line):
        super().__init__(message)
        self.line = line


@dataclass
class Word:
    raw: str
    literal: str | None
    line: int
    substitutions: list[tuple[str, int]] = field(default_factory=list)
    expanded: bool = False


@dataclass
class Command:
    words: list[Word]
    line: int


class TclParser:
    def __init__(self):
        self.lib = None
        for name in ('tcl8.6', 'tcl8.5', 'tcl', 'Tcl'):
            path = ctypes.util.find_library(name)
            if not path:
                continue
            try:
                lib = C.CDLL(path)
                version = [C.c_int() for _ in range(4)]
                lib.Tcl_GetVersion(*(C.byref(v) for v in version))
                if version[0].value != 8 or version[1].value not in (5, 6):
                    continue
                self.lib = lib
                self.version = '.'.join(str(v.value) for v in version[:3])
                break
            except (OSError, AttributeError):
                continue
        if self.lib is None:
            raise RuntimeError('Tcl 8 shared library unavailable (required for non-executing Tcl parsing)')
        self.lib.Tcl_FindExecutable.argtypes = [C.c_char_p]
        self.lib.Tcl_FindExecutable(sys.executable.encode())
        self.lib.Tcl_ParseCommand.argtypes = [C.c_void_p, C.c_void_p, C.c_int, C.c_int, C.POINTER(Parse)]
        self.lib.Tcl_ParseExpr.argtypes = [C.c_void_p, C.c_void_p, C.c_int, C.POINTER(Parse)]
        self.lib.Tcl_FreeParse.argtypes = [C.POINTER(Parse)]
        self.lib.Tcl_SplitList.argtypes = [C.c_void_p, C.c_char_p, C.POINTER(C.c_int), C.POINTER(C.POINTER(C.c_char_p))]
        self.lib.Tcl_Free.argtypes = [C.c_void_p]
        self.lib.Tcl_Concat.argtypes = [C.c_int, C.POINTER(C.c_char_p)]
        self.lib.Tcl_Concat.restype = C.c_void_p
        self.lib.Tcl_UtfBackslash.argtypes = [C.c_void_p, C.POINTER(C.c_int), C.c_void_p]

    def split_list(self, value):
        count, values = C.c_int(), C.POINTER(C.c_char_p)()
        rc = self.lib.Tcl_SplitList(None, value.encode(), C.byref(count), C.byref(values))
        if rc:
            raise ValueError('invalid Tcl list')
        try:
            return [values[i].decode() for i in range(count.value)]
        finally:
            self.lib.Tcl_Free(C.cast(values, C.c_void_p))

    def concat(self, values):
        encoded = [value.encode() for value in values]
        array = (C.c_char_p * len(encoded))(*encoded)
        result = self.lib.Tcl_Concat(len(encoded), array)
        try:
            return C.string_at(result).decode()
        finally:
            self.lib.Tcl_Free(result)

    def expression(self, value, line):
        buf = C.create_string_buffer(value.encode())
        parsed = Parse()
        try:
            rc = self.lib.Tcl_ParseExpr(None, C.addressof(buf), len(value.encode()), C.byref(parsed))
            if rc:
                raise TclSyntaxError(f'invalid Tcl expression (parse code {parsed.errorType})', line)
            substitutions = []
            for i in range(parsed.numTokens):
                token = parsed.tokenPtr[i]
                if token.type == 16:
                    raw = C.string_at(token.start, token.size).decode()
                    offset = token.start - C.addressof(buf)
                    substitutions.append((raw[1:-1], line + value.encode()[:offset].count(b'\n')))
            return substitutions
        finally:
            self.lib.Tcl_FreeParse(C.byref(parsed))

    def parse(self, text, first_line=1):
        data = text.encode()
        if b'\0' in data:
            raise TclSyntaxError('NUL byte is not supported in static scripts', first_line)
        buf = C.create_string_buffer(data)
        base = C.addressof(buf)
        position, commands = 0, []
        line_at = lambda address: first_line + data[:max(0, address - base)].count(b'\n')
        while position < len(data):
            parsed = Parse()
            try:
                rc = self.lib.Tcl_ParseCommand(None, base + position, len(data) - position, 0, C.byref(parsed))
                if rc:
                    raise TclSyntaxError(f'invalid Tcl syntax (parse code {parsed.errorType})', line_at(parsed.term or base + position))
                words, index = [], 0
                for _ in range(parsed.numWords):
                    token = parsed.tokenPtr[index]
                    components = [parsed.tokenPtr[j] for j in range(index + 1, index + 1 + token.numComponents)]
                    literal, substitutions = [], []
                    dynamic = token.type == 256
                    for sub in components:
                        raw = C.string_at(sub.start, sub.size).decode()
                        if sub.type == 4:
                            literal.append(raw)
                        elif sub.type == 8:
                            target, consumed = C.create_string_buffer(8), C.c_int()
                            length = self.lib.Tcl_UtfBackslash(sub.start, C.byref(consumed), C.addressof(target))
                            literal.append(target.raw[:length].decode())
                        elif sub.type in (16, 32):
                            dynamic = True
                            if sub.type == 16:
                                substitutions.append((raw[1:-1], line_at(sub.start)))
                    words.append(Word(C.string_at(token.start, token.size).decode(), None if dynamic else ''.join(literal), line_at(token.start), substitutions, token.type == 256))
                    index += 1 + token.numComponents
                if words:
                    commands.append(Command(words, line_at(parsed.commandStart)))
                end = (parsed.commandStart or base + position) - base + parsed.commandSize
                if end <= position:
                    break
                position = end
            finally:
                self.lib.Tcl_FreeParse(C.byref(parsed))
        return commands
