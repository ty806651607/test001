from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Scene:
    index: int
    text: str
    start: float
    end: float
    mood: str
    subject: str
    place: str
    palette: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]

    def to_dict(self) -> dict:
        data = asdict(self)
        data["palette"] = [list(color) for color in self.palette]
        return data


PALETTES = {
    "warm": ((255, 220, 151), (242, 124, 84), (94, 48, 35)),
    "cool": ((31, 48, 94), (75, 139, 190), (212, 232, 255)),
    "dark": ((14, 18, 34), (52, 70, 105), (190, 211, 236)),
    "forest": ((22, 66, 52), (70, 132, 88), (212, 221, 160)),
    "bright": ((255, 245, 184), (117, 196, 160), (255, 145, 118)),
}


def read_story(value: str) -> str:
    path = Path(value)
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8").strip()
    return value.strip()


def split_story(story: str, max_scenes: int = 8) -> list[str]:
    cleaned = re.sub(r"\s+", " ", story).strip()
    if not cleaned:
        raise ValueError("Story cannot be empty.")

    parts = [
        part.strip()
        for part in re.split(r"(?<=[。！？!?；;])\s*|\n+", cleaned)
        if part.strip()
    ]
    if len(parts) == 1 and len(parts[0]) > 38:
        parts = [parts[0][i : i + 38] for i in range(0, len(parts[0]), 38)]
    return parts[:max_scenes]


def build_storyboard(
    story: str,
    scene_seconds: float = 2.0,
    max_scenes: int = 8,
) -> list[Scene]:
    if scene_seconds <= 0:
        raise ValueError("scene_seconds must be greater than zero.")

    scenes = []
    for index, text in enumerate(split_story(story, max_scenes=max_scenes), start=1):
        start = (index - 1) * scene_seconds
        end = index * scene_seconds
        mood = infer_mood(text)
        scenes.append(
            Scene(
                index=index,
                text=text,
                start=start,
                end=end,
                mood=mood,
                subject=infer_subject(text),
                place=infer_place(text),
                palette=infer_palette(text, mood),
            )
        )
    return scenes


def infer_mood(text: str) -> str:
    if any(word in text for word in ("雨", "夜", "迷路", "孤独", "害怕", "黑")):
        return "tense"
    if any(word in text for word in ("笑", "开心", "快乐", "阳光", "天亮", "回家", "温暖")):
        return "hopeful"
    if any(word in text for word in ("森林", "树", "草", "山", "河")):
        return "adventurous"
    return "calm"


def infer_subject(text: str) -> str:
    candidates = ("小猫", "猫", "孩子", "女孩", "男孩", "机器人", "龙", "鸟", "船", "星星", "萤火虫")
    for candidate in candidates:
        if candidate in text:
            return candidate
    return "主角"


def infer_place(text: str) -> str:
    places = ("森林", "城市", "家", "海边", "山谷", "学校", "夜空", "雨夜", "河边")
    for place in places:
        if place in text:
            return place
    return "远方"


def infer_palette(text: str, mood: str) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    if any(word in text for word in ("森林", "树", "草", "山")):
        return PALETTES["forest"]
    if any(word in text for word in ("雨", "夜", "黑")):
        return PALETTES["dark"]
    if mood == "hopeful":
        return PALETTES["bright"]
    if mood == "tense":
        return PALETTES["cool"]
    return PALETTES["warm"]
