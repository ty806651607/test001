from __future__ import annotations

from pathlib import Path

from .storyboard import Scene


def format_timestamp(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def write_srt(scenes: list[Scene], path: Path) -> None:
    blocks = []
    for scene in scenes:
        blocks.append(
            "\n".join(
                (
                    str(scene.index),
                    f"{format_timestamp(scene.start)} --> {format_timestamp(scene.end)}",
                    scene.text,
                )
            )
        )
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
