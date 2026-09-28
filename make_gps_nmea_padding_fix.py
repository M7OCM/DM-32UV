#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

EXPECTED_SHA256 = "fda860febfcf1a234eed7fa73272112891074aac83746e4f8dfe224a2a700f8f"
OUTPUT_NAME = "DM32.01.L01.048_GPS-NMEA-padding-fix.bin"

PATCHES = [
    (0x0A94F8, b"%04.4f", b"%09.4f"),
    (0x0A9500, b"%05.4f\x00\x00", b"%010.4f\x00"),
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "DM32.01.L01.048.bin")
    if not src.is_file():
        print(f"Input firmware not found: {src}", file=sys.stderr)
        return 1

    original = src.read_bytes()
    digest = sha256(original)
    if digest != EXPECTED_SHA256:
        print("Refusing to patch: input SHA256 does not match the tested firmware.", file=sys.stderr)
        print(f"Expected: {EXPECTED_SHA256}", file=sys.stderr)
        print(f"Actual:   {digest}", file=sys.stderr)
        return 2

    data = bytearray(original)
    for offset, old, new in PATCHES:
        actual = bytes(data[offset:offset + len(old)])
        if actual != old:
            print(f"Refusing to patch: unexpected bytes at 0x{offset:06X}", file=sys.stderr)
            print(f"Expected: {old!r}", file=sys.stderr)
            print(f"Actual:   {actual!r}", file=sys.stderr)
            return 3
        if len(old) != len(new):
            raise RuntimeError("Patch must preserve firmware size")
        data[offset:offset + len(old)] = new

    out = src.with_name(OUTPUT_NAME)
    out.write_bytes(data)
    print(f"Wrote: {out}")
    print(f"SHA256: {sha256(bytes(data))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
