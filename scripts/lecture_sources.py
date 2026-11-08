"""Prepares the raw material for notes from a recorded lecture: metadata, a Whisper transcript and the frames.

Runs on the computer that writes the notes, not in the app: yt-dlp, ffmpeg and mlx-whisper are not dependencies of
the app. The work folder ends up with

    info.json     metadata from yt-dlp (title, channel, date, length, chapters, description)
    video.mp4     the recording, at most 720p
    prepis.txt    transcript with times, „[mm:ss] text“ per segment
    prepis.srt    the same as subtitles
    snimky/       one frame per distinct screen, slajd_SSSS.jpg after the second it comes from
    snimky.tsv    file name and second of every frame

Usage, with the tools from scripts/lecture_tools.py installed in the project folder:
    .venv/bin/python scripts/lecture_sources.py URL .lecture-work/<video id>
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Sequence

import numpy as np

MAX_VIDEO_HEIGHT = 720
WHISPER_MODEL = "mlx-community/whisper-large-v3-mlx"
AUDIO_SAMPLE_RATE = 16000
PROBE_WIDTH, PROBE_HEIGHT = 160, 90
"""Frames are compared at this size, once per second; small enough to read a whole lecture into memory."""
PIXEL_CHANGE = 25
"""A probe pixel counts as changed when its grey level moves by more than this (of 255)."""
SCREEN_CHANGE_SHARE = 0.02
"""A new screen starts when this share of pixels changes; a speaker's webcam inset stays below it."""
MIN_SCREEN_SECONDS = 3
"""Shorter screens are transitions or video; their frames are left out."""
MAX_FRAME_SECONDS = 9999
"""Frame names have four digits for the second (web/lecture_slides.py)."""
FRAME_QUALITY = 3
"""ffmpeg JPEG quality, 2 (best) to 31."""


class LectureSourceError(RuntimeError):
    """A step of the preparation failed; the message names the step and the command."""


def prepare(url: str, work: Path, whisper: Path) -> None:
    work.mkdir(parents=True, exist_ok=True)
    info = download_metadata(url, work)
    if info["duration"] > MAX_FRAME_SECONDS:
        raise LectureSourceError(f"Záznam má {info['duration']} s, zápisky umí nejvýš {MAX_FRAME_SECONDS} s.")
    video = download_video(url, work)
    transcribe(video, work, whisper)
    frames = extract_frames(video, work / "snimky")
    (work / "snimky.tsv").write_text(
        "soubor\tcas_s\n" + "".join(f"{frame_name(second)}\t{second}\n" for second in frames), encoding="utf-8",
    )
    print(f"Hotovo: {info['title']} ({info['duration']} s), {len(frames)} snímků v {work}")


def download_metadata(url: str, work: Path) -> dict:
    target = work / "info.json"
    if not target.exists():
        _run(["yt-dlp", "--skip-download", "--write-info-json", "-o", str(work / "info"), url], "metadata")
        (work / "info.info.json").rename(target)
    info = json.loads(target.read_text(encoding="utf-8"))
    return {key: info.get(key) for key in ("title", "channel", "upload_date", "duration", "chapters", "description")}


def download_video(url: str, work: Path) -> Path:
    video = work / "video.mp4"
    if not video.exists():
        video_format = (
            f"bv*[height<={MAX_VIDEO_HEIGHT}][ext=mp4]+ba[ext=m4a]/b[height<={MAX_VIDEO_HEIGHT}]"
        )
        _run(["yt-dlp", "-f", video_format, "--merge-output-format", "mp4", "-o", str(video), url], "stažení videa")
    return video


def transcribe(video: Path, work: Path, whisper: Path) -> None:
    if (work / "prepis.srt").exists():
        return
    audio = work / "audio.wav"
    _run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", str(AUDIO_SAMPLE_RATE),
          str(audio)], "zvuk pro přepis")
    _run([str(whisper), str(audio), "--model", WHISPER_MODEL, "--output-format", "all", "--output-dir", str(work),
          "--output-name", "prepis", "--condition-on-previous-text", "False", "--verbose", "False"], "přepis Whisperem")
    write_timed_transcript(work / "prepis.json", work / "prepis.txt")
    audio.unlink()


def write_timed_transcript(segments_json: Path, target: Path) -> None:
    """Whisper's plain text has no times; the notes need them to link chapters and frames into the video."""
    segments = json.loads(segments_json.read_text(encoding="utf-8"))["segments"]
    lines = [f"[{timestamp(int(segment['start']))}] {segment['text'].strip()}" for segment in segments]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def extract_frames(video: Path, target: Path) -> List[int]:
    probes = probe_frames(video)
    seconds = screen_seconds(probes)
    target.mkdir(parents=True, exist_ok=True)
    for second in seconds:
        _run(["ffmpeg", "-v", "error", "-y", "-ss", str(second), "-i", str(video), "-frames:v", "1",
              "-q:v", str(FRAME_QUALITY), str(target / frame_name(second))], f"snímek v {second} s")
    return seconds


def probe_frames(video: Path) -> np.ndarray:
    """Grey frames of PROBE_WIDTH × PROBE_HEIGHT, one per second of the recording."""
    command = ["ffmpeg", "-v", "error", "-i", str(video), "-vf",
               f"fps=1,scale={PROBE_WIDTH}:{PROBE_HEIGHT},format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(command, check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, PROBE_HEIGHT, PROBE_WIDTH)


def screen_seconds(probes: np.ndarray) -> List[int]:
    """The last second of every screen that stays at least MIN_SCREEN_SECONDS: an animated slide is complete then."""
    changed = np.abs(np.diff(probes.astype(np.int16), axis=0)) > PIXEL_CHANGE
    starts = [0] + [int(second) + 1 for second in np.flatnonzero(changed.mean(axis=(1, 2)) > SCREEN_CHANGE_SHARE)]
    ends = starts[1:] + [len(probes)]
    return [end - 1 for start, end in zip(starts, ends) if end - start >= MIN_SCREEN_SECONDS]


def frame_name(second: int) -> str:
    return f"slajd_{second:04d}.jpg"


def timestamp(seconds: int) -> str:
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes:02d}:{secs:02d}"


def _run(command: Sequence[str], step: str) -> None:
    if shutil.which(command[0]) is None and not Path(command[0]).exists():
        raise LectureSourceError(f"{step}: chybí program {command[0]}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise LectureSourceError(f"{step} selhal ({' '.join(command[:3])} …): {result.stderr.strip()[-2000:]}")


def main(arguments: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url")
    parser.add_argument("work", type=Path)
    parser.add_argument("--whisper", type=Path, help="the mlx_whisper command; by default the project's own")
    options = parser.parse_args(arguments)
    if options.whisper is None:
        # Imported here: tests import this module as scripts.lecture_sources, without scripts/ on the path.
        from lecture_tools import whisper_command

        options.whisper = whisper_command()
    try:
        prepare(options.url, options.work, options.whisper)
    except LectureSourceError as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
