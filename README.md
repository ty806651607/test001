# Story Video

一个纯 Python 原型：输入一段故事，生成简单程序化动画视频、SRT 字幕和分镜 JSON。

特点：

- 只使用 Python 标准库
- 支持直接输入故事文本或读取 `.txt` 文件
- 自动拆分场景
- 根据关键词推断情绪、颜色、地点和主体
- 输出未压缩 `.avi` 视频
- 同时输出 `.srt` 字幕和 `_storyboard.json` 分镜文件

## 快速开始

```powershell
python -m story_video "小猫在雨夜迷路了。它遇见一只萤火虫，跟着光穿过森林。天亮时，它回到了温暖的家。" --output outputs/cat_story.avi
```

生成文件：

- `outputs/cat_story.avi`
- `outputs/cat_story.srt`
- `outputs/cat_story_storyboard.json`

## 常用参数

```powershell
python -m story_video story.txt --output outputs/story.avi --width 320 --height 180 --fps 8 --scene-seconds 2 --max-scenes 8
```

参数说明：

- `story`：故事文本，或 `.txt` 文件路径
- `--output`：输出 AVI 路径
- `--width` / `--height`：视频尺寸
- `--fps`：帧率
- `--scene-seconds`：每个场景时长
- `--max-scenes`：最多生成多少个场景

## 运行测试

```powershell
python -m pytest -q
```
