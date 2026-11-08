"""Where the tools for lecture notes live, and their installation: everything inside the project folder.

    python3 scripts/lecture_tools.py install    installs Whisper and pptxgenjs into .lecture-tools/
    python3 scripts/lecture_tools.py check      says what is installed and what is missing

The folders are next to the repository's .git, in the main checkout, so that temporary git worktrees (the queue
worker writes notes in one) use the same tools and work folders. Both are ignored by git and Docker:

    .lecture-tools/whisper-venv/   Python with mlx-whisper (Whisper large-v3 on Apple Silicon)
    .lecture-tools/node/           pptxgenjs for scripts/lecture_presentation.js
    .lecture-work/<video id>/      video, transcript and frames of each lecture (scripts/lecture_sources.py)

The Whisper model itself (about 6 GB) stays in the shared Hugging Face cache ~/.cache/huggingface.
yt-dlp, ffmpeg, soffice and pdftoppm come from Homebrew.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Sequence

PPTXGENJS = "pptxgenjs@3.12.0"
WHISPER_PACKAGE = "mlx-whisper"
SYSTEM_TOOLS = ("yt-dlp", "ffmpeg", "soffice", "pdftoppm", "node", "npm")


def project_folder() -> Path:
    """The main checkout, also when called from a git worktree (its .git is a file pointing to the common one)."""
    here = Path(__file__).resolve().parent
    common = subprocess.run(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
        cwd=here, check=True, capture_output=True, text=True,
    ).stdout.strip()
    return Path(common).parent


def tools_folder() -> Path:
    return project_folder() / ".lecture-tools"


def work_folder(video_id: str) -> Path:
    return project_folder() / ".lecture-work" / video_id


def whisper_command() -> Path:
    return tools_folder() / "whisper-venv" / "bin" / "mlx_whisper"


def node_modules() -> Path:
    return tools_folder() / "node" / "node_modules"


def missing_tools() -> List[str]:
    missing = [tool for tool in SYSTEM_TOOLS if shutil.which(tool) is None]
    if not whisper_command().exists():
        missing.append(str(whisper_command()))
    if not (node_modules() / "pptxgenjs").is_dir():
        missing.append(str(node_modules() / "pptxgenjs"))
    return missing


def install() -> None:
    tools = tools_folder()
    venv = tools / "whisper-venv"
    if not whisper_command().exists():
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        subprocess.run([str(venv / "bin" / "pip"), "install", "--quiet", WHISPER_PACKAGE], check=True)
    node = tools / "node"
    if not (node_modules() / "pptxgenjs").is_dir():
        node.mkdir(parents=True, exist_ok=True)
        subprocess.run(["npm", "install", "--prefix", str(node), "--no-save", "--silent", PPTXGENJS], check=True)


def main(arguments: Sequence[str]) -> int:
    command = arguments[0] if arguments else "check"
    if command == "install":
        install()
    elif command != "check":
        print(__doc__)
        return 2
    missing = missing_tools()
    if missing:
        print("Chybí: " + ", ".join(missing))
        print("Doinstaluj: python3 scripts/lecture_tools.py install; programy z Homebrew: brew install yt-dlp ffmpeg "
              "poppler a LibreOffice.")
        return 1
    print(f"Nástroje jsou připravené v {tools_folder()}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
