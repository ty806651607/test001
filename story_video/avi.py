from __future__ import annotations

import struct
from pathlib import Path


def _fourcc(value: str) -> bytes:
    return value.encode("ascii")


def _chunk(name: str, payload: bytes) -> bytes:
    padding = b"\0" if len(payload) % 2 else b""
    return _fourcc(name) + struct.pack("<I", len(payload)) + payload + padding


def _list(name: str, payload: bytes) -> bytes:
    body = _fourcc(name) + payload
    padding = b"\0" if len(body) % 2 else b""
    return b"LIST" + struct.pack("<I", len(body)) + body + padding


def write_avi(path: Path, frames: list[bytes], width: int, height: int, fps: int) -> None:
    if not frames:
        raise ValueError("At least one frame is required.")
    if width <= 0 or height <= 0 or fps <= 0:
        raise ValueError("width, height, and fps must be positive.")

    row_stride = width * 3
    padded_stride = (row_stride + 3) & ~3
    image_size = padded_stride * height
    frame_count = len(frames)
    usec_per_frame = int(1_000_000 / fps)

    avih = struct.pack(
        "<IIIIIIIIIIIIII",
        usec_per_frame,
        image_size * fps,
        0,
        0x10,
        frame_count,
        0,
        1,
        image_size,
        width,
        height,
        0,
        0,
        0,
        0,
    )
    strh = struct.pack(
        "<4s4sIHHIIIIIIIIiiii",
        b"vids",
        b"DIB ",
        0,
        0,
        0,
        0,
        1,
        fps,
        0,
        frame_count,
        image_size,
        0xFFFFFFFF,
        0,
        0,
        0,
        width,
        height,
    )
    strf = struct.pack(
        "<IiiHHIIiiII",
        40,
        width,
        height,
        1,
        24,
        0,
        image_size,
        0,
        0,
        0,
        0,
    )

    hdrl = _list("hdrl", _chunk("avih", avih) + _list("strl", _chunk("strh", strh) + _chunk("strf", strf)))
    movi_payload = b"".join(_chunk("00db", frame) for frame in frames)
    movi = _list("movi", movi_payload)
    riff_payload = b"AVI " + hdrl + movi
    path.write_bytes(b"RIFF" + struct.pack("<I", len(riff_payload)) + riff_payload)
