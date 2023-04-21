# -*- coding: utf-8 -*-
import enum
import io
import typing
import re
import struct


VdfBinaryCallback = typing.Callable[[str, str | int | object, list[str]], None]
VdfTextCallback = typing.Callable[[str, str | object, list[str]], None]


class BinaryNodeType(enum.IntEnum):
    ChildObject = 0
    String = 1
    Int32 = 2
    Float32 = 3
    Pointer = 4
    WideString = 5
    Color = 6
    UInt32 = 7
    End = 8
    ProbablyBinary = 9
    Int64 = 10
    AlternateEnd = 11


def quot(v: str) -> str:
    return '"' + v.replace('"', '\\"') + '"'


def parse(src, listener: VdfBinaryCallback | None = None):
    magic, universe = struct.unpack("<II", src.read(8))

    parser, is_new, end = None, False, 0
    match magic:
        case 0x07_56_44_27:
            parser = parse_app
        case 0x07_56_44_28:
            parser = parse_app
            is_new = True
        case 0x06_56_55_27:
            parser = parse_package
            end = 0xFFFF_FFFF
        case 0x06_56_55_28:
            parser = parse_package
            is_new = True
            end = 0xFFFF_FFFF
        case _:
            print("Unknown magic:", hex(magic))
            return

    while (main_id := struct.unpack("<I", src.read(4))[0]) != end:
        parser(main_id, src, is_new, listener)


def parse_app(appid, src, is_new: bool, listener: VdfBinaryCallback | None):
    s_fmt = "<IIIQ20sI"
    s_size = struct.calcsize(s_fmt)
    (
        size,
        info_state,
        last_updated,
        pics_token,
        appinfo_sha,
        change_number,
    ) = struct.unpack(s_fmt, src.read(s_size))
    vdf_size = size - s_size + 4
    if is_new:
        bin_hash = src.read(20)
        vdf_size -= 20
    else:
        bin_hash = None

    if listener is not None:
        listener(
            "app",
            {
                "app_id": appid,
                "size": size,
                "info_state": info_state,
                "last_updated": last_updated,
                "pics_token": pics_token,
                "appinfo_sha": appinfo_sha,
                "change_number": change_number,
                "data_hash": bin_hash,
            },
            [],
        )

    parser = VdfBinary(src, listener)
    parser.obj_path = ["app"]
    parser.parse()

    if listener is not None:
        listener("app", VdfBinary.OBJ_END, ["app"])


def parse_package(sub_id, src, is_new, listener: VdfBinaryCallback | None):
    s_fmt = "<20sI"
    s_size = struct.calcsize(s_fmt)
    data_hash, change_number = struct.unpack(s_fmt, src.read(s_size))
    if is_new:
        token = struct.unpack("<Q", src.read(8))
    else:
        token = None

    if listener is not None:
        listener(
            "package",
            {
                "sub_id": sub_id,
                "data_hash": data_hash,
                "change_number": change_number,
                "token": token,
            },
            [],
        )

    parser = VdfBinary(src, listener)
    parser.obj_path = ["package"]
    parser.parse()

    if listener is not None:
        listener("package", VdfBinary.OBJ_END, ["package"])


class VdfBinary:
    OBJ_START = object()
    OBJ_END = object()

    def __init__(self, stream: io.BytesIO, listener: VdfBinaryCallback | None = None):
        self._stream = stream
        self.listener: VdfBinaryCallback = listener or self.default_printer
        self.obj_path: list[str] = []

    @classmethod
    def default_printer(cls, k, v, path):
        """Event listener producing a pythonic dict to stdout."""
        indent = "  "
        if v == cls.OBJ_END:
            # Path of end event contains the object that is being ended.
            if len(path) == 1:
                print(indent * (len(path) - 1), "}")
            else:
                print(indent * (len(path) - 1), "},")
        elif v == cls.OBJ_START:
            if path:
                print(indent * len(path), quot(k) + ":", "{")
            else:
                print("", k, "= {")
        elif isinstance(v, str):
            print(indent * len(path), quot(k) + ":", quot(v) + ",")
        else:
            print(indent * len(path), quot(k) + ":", str(v) + ",")

    def parse(self):
        self.consume_header(self._stream)
        self.read_object()

    def read_object(self):
        next_node_type = self.read_node_type(self._stream)
        while next_node_type not in (BinaryNodeType.End, BinaryNodeType.AlternateEnd):
            self.parse_value(next_node_type)
            next_node_type = self.read_node_type(self._stream)

    @staticmethod
    def read_node_type(stream: io.BytesIO) -> BinaryNodeType:
        return BinaryNodeType(ord(stream.read(1)))

    def parse_value(self, node_type: BinaryNodeType):
        key = self.read_zstr(self._stream)
        val = None
        match node_type:
            case BinaryNodeType.ChildObject:
                self.listener(key, self.OBJ_START, self.obj_path)
                self.obj_path.append(key)
                self.read_object()
                self.listener(key, self.OBJ_END, self.obj_path)
                self.obj_path.pop()
            case BinaryNodeType.String:
                val = self.read_zstr(self._stream)
            case BinaryNodeType.Int32 | BinaryNodeType.Color | BinaryNodeType.Pointer:
                (val,) = struct.unpack("<i", self._stream.read(4))
            case BinaryNodeType.Float32:
                (val,) = struct.unpack("<f", self._stream.read(4))
            case BinaryNodeType.WideString:
                raise NotImplementedError
            case BinaryNodeType.UInt32:
                (val,) = struct.unpack("<I", self._stream.read(4))
            case BinaryNodeType.ProbablyBinary:
                raise NotImplementedError
            case BinaryNodeType.Int64:
                (val,) = struct.unpack("<z", self._stream.read(8))

        if val is not None:
            self.listener(key, val, self.obj_path)

    @staticmethod
    def consume_header(stream: io.BytesIO):
        hdr = stream.read(4)
        if len(hdr) < 4:
            if hdr:
                stream.seek(-len(hdr), io.SEEK_CUR)
            return
        if hdr == (0x56, 0x42, 0x4B, 0x56):
            crc32 = stream.read(4)
        else:
            stream.seek(-4, io.SEEK_CUR)

    @staticmethod
    def read_zstr(stream: io.BytesIO) -> str:
        p = 0
        while stream.read(1) != b"\x00":
            p += 1
        if p:
            # p doesn't include 0-terminator, but stream moved to it already.
            stream.seek(-p - 1, io.SEEK_CUR)
            r = stream.read(p).decode()  # Decode only the string (without 0-terminator)
            stream.seek(1, io.SEEK_CUR)  # Skip the 0-terminator
            return r
        return ""


def parse_text(src, listener: VdfTextCallback | None = None):
    parser = VdfText(src, listener)
    parser.parse()


class VdfText:
    OBJ_START = object()
    OBJ_END = object()
    ESCAPES = re.compile(r'\\([\\nrt0"])')

    def __init__(self, stream: io.TextIOBase, listener: VdfTextCallback | None = None):
        self._stream = stream
        self.listener: VdfTextCallback = listener or self.default_printer

    @classmethod
    def default_printer(cls, k, v, path):
        """Event listener producing a pythonic dict to stdout."""
        indent = "  "
        if v == cls.OBJ_END:
            # Path of end event contains the object that is being ended.
            if len(path) == 1:
                print(indent * (len(path) - 1), "}")
            else:
                print(indent * (len(path) - 1), "},")
        elif v == cls.OBJ_START:
            if path:
                print(indent * len(path), quot(k) + ":", "{")
            else:
                print("", k, "= {")
        else:
            print(indent * len(path), quot(k) + ":", quot(v) + ",")

    def parse(self, stack: list[str] = None):
        if stack is None:
            stack = []
        while True:
            key = self.parse_token()
            if key is self.OBJ_END or key is None:
                return
            assert isinstance(key, str)

            value = self.parse_token()
            if value is self.OBJ_START:
                self.listener(key, self.OBJ_START, stack)
                stack.append(key)
                self.parse(stack)
                self.listener(key, self.OBJ_END, stack)
                stack.pop()
            else:
                self.listener(key, value, stack)

    def parse_token(self) -> str | object | None:
        while True:
            tok = self.read_token()
            match tok:
                case "":
                    # EOF
                    return
                case '"':
                    return self.parse_str()
                case "{":
                    return self.OBJ_START
                case "}":
                    return self.OBJ_END
                case "#":
                    self.read_until("\n\r")

    def read_token(self) -> str:
        while (tok := self._stream.read(1)).isspace():
            pass
        return tok

    def read_until(self, terminators: str) -> str:
        out = []
        while (char := self._stream.read(1)) not in terminators:
            out.append(char)
        return "".join(out)

    def parse_str(self) -> str:
        maybe_whole = self.read_until('"')
        while True:
            without_end_escapes = maybe_whole.rstrip("\\")
            if (len(maybe_whole) - len(without_end_escapes)) % 2 == 0:
                # Zero or even amount of escapes,
                # thus the end quote isn't escaped, and we are at end of string.
                return self.unescape_str(maybe_whole)
            # Found escape + ", continue reading.
            maybe_whole += '"' + self.read_until('"')

    @classmethod
    def unescape_str(cls, string: str) -> str:
        return cls.ESCAPES.sub(cls.unescape_replacer, string)

    @staticmethod
    def unescape_replacer(match: re.Match) -> str:
        match match.group(1):
            case "n":
                return "\n"
            case "r":
                return "\r"
            case "t":
                return "\t"
            case "0":
                return "\0"
            case s:
                return s
