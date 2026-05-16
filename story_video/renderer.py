from __future__ import annotations

import math
from pathlib import Path

from .avi import write_avi
from .storyboard import Scene


Color = tuple[int, int, int]


def render_video(scenes: list[Scene], output: Path, width: int = 320, height: int = 180, fps: int = 8) -> None:
    frames: list[bytes] = []
    for scene in scenes:
        frame_count = max(1, int(round((scene.end - scene.start) * fps)))
        for frame_index in range(frame_count):
            t = frame_index / max(1, frame_count - 1)
            frames.append(render_frame(scene, t, width, height))
    write_avi(output, frames, width=width, height=height, fps=fps)


def render_frame(scene: Scene, t: float, width: int, height: int) -> bytes:
    bg_top, bg_bottom, accent = scene.palette
    pixels = bytearray()

    subject_x = int(width * (0.2 + 0.58 * t))
    subject_y = int(height * (0.62 + 0.04 * math.sin(t * math.tau)))
    pulse = int(8 * math.sin(t * math.tau))

    for y in range(height - 1, -1, -1):
        row = bytearray()
        mix = y / max(1, height - 1)
        base = blend(bg_top, bg_bottom, mix)
        for x in range(width):
            color = base
            color = draw_sun_or_moon(color, x, y, width, height, scene, t)
            color = draw_land(color, x, y, width, height, scene)
            color = draw_subject(color, x, y, subject_x, subject_y, accent, pulse)
            color = draw_firefly(color, x, y, width, height, scene, t)
            row.extend((color[2], color[1], color[0]))
        while len(row) % 4:
            row.append(0)
        pixels.extend(row)
    return bytes(pixels)


def blend(a: Color, b: Color, amount: float) -> Color:
    return tuple(int(a[i] * (1 - amount) + b[i] * amount) for i in range(3))


def draw_sun_or_moon(color: Color, x: int, y: int, width: int, height: int, scene: Scene, t: float) -> Color:
    cx = int(width * (0.78 - 0.18 * t))
    cy = int(height * 0.24)
    radius = max(8, min(width, height) // 10)
    distance = (x - cx) ** 2 + (y - cy) ** 2
    if distance < radius * radius:
        light = (255, 238, 169) if scene.mood != "tense" else (205, 221, 245)
        return blend(color, light, 0.82)
    return color


def draw_land(color: Color, x: int, y: int, width: int, height: int, scene: Scene) -> Color:
    horizon = int(height * 0.72)
    wave = int(5 * math.sin((x / max(1, width)) * math.tau * 2))
    if y > horizon + wave:
        land = (45, 82, 60) if scene.place == "森林" else (91, 71, 54)
        return blend(color, land, 0.78)
    if scene.place == "森林" and y > height * 0.38 and x % 37 in (0, 1, 2):
        return (34, 62, 45)
    return color


def draw_subject(color: Color, x: int, y: int, cx: int, cy: int, accent: Color, pulse: int) -> Color:
    body_rx = 17
    body_ry = 13
    head_r = 10
    body = ((x - cx) / body_rx) ** 2 + ((y - cy) / body_ry) ** 2 <= 1
    head = (x - (cx + 13)) ** 2 + (y - (cy - 9)) ** 2 <= head_r * head_r
    if body or head:
        return accent
    if (x - (cx + 8)) ** 2 + (y - (cy - 13)) ** 2 <= 2 + abs(pulse):
        return (24, 24, 24)
    if abs(y - (cy + 13)) <= 1 and cx - 22 <= x <= cx - 10:
        return accent
    return color


def draw_firefly(color: Color, x: int, y: int, width: int, height: int, scene: Scene, t: float) -> Color:
    if "萤火虫" not in scene.text and scene.mood != "hopeful":
        return color
    cx = int(width * (0.3 + 0.42 * t))
    cy = int(height * (0.33 + 0.08 * math.sin(t * math.tau * 2)))
    distance = (x - cx) ** 2 + (y - cy) ** 2
    if distance < 26:
        return (255, 246, 132)
    if distance < 90:
        return blend(color, (255, 246, 132), 0.35)
    return color
