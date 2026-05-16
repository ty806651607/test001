from story_video.storyboard import build_storyboard, split_story
from story_video.subtitles import format_timestamp


def test_split_story_by_chinese_punctuation():
    scenes = split_story("小猫迷路了。它看见萤火虫！天亮回家了。")
    assert scenes == ["小猫迷路了。", "它看见萤火虫！", "天亮回家了。"]


def test_build_storyboard_infers_metadata():
    scenes = build_storyboard("小猫在雨夜迷路了。天亮时，它回到了温暖的家。", scene_seconds=1.5)
    assert len(scenes) == 2
    assert scenes[0].mood == "tense"
    assert scenes[0].subject == "小猫"
    assert scenes[0].start == 0
    assert scenes[1].end == 3.0


def test_format_timestamp():
    assert format_timestamp(65.432) == "00:01:05,432"
