from __future__ import annotations

import argparse
import json
from pathlib import Path

from .renderer import render_video
from .storyboard import build_storyboard, read_story
from .subtitles import write_srt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a simple video from a story.")
    parser.add_argument("story", help="Story text, or a path to a .txt file.")
    parser.add_argument("--output", default="outputs/story.avi", help="Output AVI path.")
    parser.add_argument("--width", type=int, default=320, help="Video width in pixels.")
    parser.add_argument("--height", type=int, default=180, help="Video height in pixels.")
    parser.add_argument("--fps", type=int, default=8, help="Frames per second.")
    parser.add_argument(
        "--scene-seconds",
        type=float,
        default=2.0,
        help="Duration of each generated scene.",
    )
    parser.add_argument("--max-scenes", type=int, default=8, help="Maximum scene count.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    story = read_story(args.story)
    scenes = build_storyboard(
        story,
        scene_seconds=args.scene_seconds,
        max_scenes=args.max_scenes,
    )

    render_video(scenes, output, width=args.width, height=args.height, fps=args.fps)

    srt_path = output.with_suffix(".srt")
    storyboard_path = output.with_name(f"{output.stem}_storyboard.json")
    write_srt(scenes, srt_path)
    storyboard_path.write_text(
        json.dumps([scene.to_dict() for scene in scenes], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote video: {output}")
    print(f"Wrote subtitles: {srt_path}")
    print(f"Wrote storyboard: {storyboard_path}")


if __name__ == "__main__":
    main()
