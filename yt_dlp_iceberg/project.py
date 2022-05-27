import os
import pathlib
import time
from dataclasses import dataclass
from typing import List


# noinspection PyMethodMayBeStatic
from yt_dlp_iceberg.preset import Preset


@dataclass
class Project:
    folder: str
    target: str
    interval_minutes: int = None
    preset: Preset = None
    post_command: str = None
    options: List[str] = None

    def __post_init__(self):
        if self.preset is not None:
            if self.interval_minutes is None:
                if not self.preset.interval_minutes:
                    raise RuntimeError(
                        f"{self.folder}: Either project or preset requires an interval_minutes attribute")
                self.interval_minutes = self.preset.interval_minutes
            if self.options is None and self.preset.options:
                self.options = self.preset.options
            if self.post_command is None and self.preset.post_command:
                self.post_command = self.preset.post_command

    def need_update(self):
        # all functions assume cwd is the project folder

        text = pathlib.Path("last_interval.txt")
        if not text.exists():
            return True
        try:
            last_update = int(text.read_text("utf-8"))
        except ValueError:
            return True
        return last_update < (int(time.time()) - (self.interval_minutes * 60))

    def update_interval_file(self):
        text = pathlib.Path("last_interval.txt")
        text.write_text(str(int(time.time())))

    def run_ytdlp(self, custom_exec: str = "yt-dlp"):
        if ' ' in custom_exec:
            cmd = '"' + custom_exec + '" '
        else:
            cmd = custom_exec + ' '
        cmd += "--download-archive download_archive_state.txt "
        for opt in self.options:
            cmd += opt + " "
        cmd += self.target
        os.system(cmd)
